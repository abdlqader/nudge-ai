"""
FastAPI Application for AI Agent with Nudge API Integration

This application provides REST endpoints to interact with the AI agent
and manages authentication with the Nudge API.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio
import json
import os
import queue
import threading
from dotenv import load_dotenv

from ai_agent import AIAgent
from config import get_provider, SYSTEM_PROMPT
from tools.nudge_api import nudge_registry, set_auth_token, clear_auth_token, get_auth_status

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Nudge AI Agent API",
    description="AI-powered assistant for Nudge task management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI agent (singleton)
_agent: Optional[AIAgent] = None


def get_agent() -> AIAgent:
    """Get or create the AI agent instance"""
    global _agent
    if _agent is None:
        provider = get_provider()
        _agent = AIAgent(
            model_provider=provider,
            system_prompt=SYSTEM_PROMPT,
            tools=nudge_registry.get_tool_definitions(),
            tool_functions=nudge_registry.get_tool_functions()
        )
    return _agent


def get_nudge_base_url() -> str:
    """Get Nudge API base URL"""
    return os.getenv("NUDGE_API_BASE_URL", "http://localhost:8080")


def _extract_token(authorization: Optional[str]) -> Optional[str]:
    """Extract Bearer token from Authorization header value."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return authorization


# Pydantic models

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class MessageRequest(BaseModel):
    message: str = Field(..., description="User message to the AI agent")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=None,
        description=(
            "Previous conversation turns. Pass the conversation_history from the last "
            "response to maintain multi-turn context. Omit to start a new conversation."
        )
    )


class MessageResponse(BaseModel):
    response: str = Field(..., description="AI agent response")
    tool_calls: Optional[list] = Field(default=None, description="Tools called during processing")
    conversation_history: List[ChatMessage] = Field(
        ...,
        description="Updated conversation history. Pass this back in the next request to maintain context."
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "ok", "service": "nudge-ai-agent"}


# AI Agent endpoint
@app.post("/agent/message", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    authorization: Optional[str] = Header(None, description="Bearer token from Nudge API")
):
    """
    Send a message to the AI agent and receive the full response at once.

    **Stateless design** — the server holds no per-user session. Pass
    `conversation_history` from the previous response to maintain multi-turn context;
    omit it to start a fresh conversation.

    **Authentication** — provide your Nudge JWT via `Authorization: Bearer <token>`
    with every request. The token is request-scoped and cleared immediately after.

    For real-time streaming of tool activity and the response, use `POST /agent/stream`.
    """
    token = _extract_token(authorization)
    if token:
        set_auth_token(token)
    try:
        history = [m.model_dump() for m in request.conversation_history] if request.conversation_history else []
        agent = get_agent()
        result = agent.run_stateless(request.message, conversation_history=history)
        return MessageResponse(
            response=result.get("response", ""),
            tool_calls=result.get("tool_calls"),
            conversation_history=[ChatMessage(**m) for m in result.get("conversation_history", [])]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI agent error: {str(e)}")
    finally:
        clear_auth_token()


@app.post("/agent/stream")
async def stream_message(
    request: MessageRequest,
    authorization: Optional[str] = Header(None, description="Bearer token from Nudge API")
):
    """
    Stream the AI agent's response using **Server-Sent Events (SSE)**.

    Use this endpoint for chat UIs where you want to show tool activity and the
    response as they happen, rather than waiting for the full result.

    **How to connect:** send a normal `POST` with `Accept: text/event-stream`.
    Each line starting with `data:` is a JSON object with a `type` field:

    | type | payload fields | description |
    |---|---|---|
    | `tool_start` | `tool`, `args` | Agent is executing a tool |
    | `tool_end` | `tool`, `success`, `result?`, `error?` | Tool finished |
    | `message` | `content` | Final text response from the model |
    | `done` | `tool_calls`, `conversation_history` | Stream complete |
    | `error` | `message` | Fatal error |

    Pass `conversation_history` from the `done` event back in the next request
    to maintain multi-turn context.
    """
    token = _extract_token(authorization)

    async def event_generator():
        if token:
            set_auth_token(token)
        try:
            history = (
                [m.model_dump() for m in request.conversation_history]
                if request.conversation_history
                else []
            )
            agent = get_agent()
            event_queue: queue.Queue = queue.Queue()

            def producer():
                try:
                    for event in agent.run_stream(request.message, conversation_history=history):
                        event_queue.put(event)
                except Exception as exc:
                    event_queue.put({'type': 'error', 'message': str(exc)})
                finally:
                    event_queue.put(None)  # sentinel

            thread = threading.Thread(target=producer, daemon=True)
            thread.start()

            loop = asyncio.get_event_loop()
            while True:
                event = await loop.run_in_executor(None, event_queue.get)
                if event is None:
                    break
                yield f"data: {json.dumps(event)}\n\n"

            thread.join()
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            clear_auth_token()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/agent/status")
async def agent_status():
    """
    Get AI agent status and authentication state
    
    Returns information about the AI agent and whether a user is authenticated.
    """
    from tools.nudge_api import get_auth_status
    
    agent = get_agent()
    auth_status = get_auth_status()
    
    return {
        "agent": {
            "provider": agent.model_provider.__class__.__name__,
            "model": agent.model_provider.model_name,
            "tools_count": len(nudge_registry.get_all())
        },
        "authentication": auth_status,
        "nudge_api_url": get_nudge_base_url()
    }





if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
