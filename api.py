"""
FastAPI Application for AI Agent with Nudge API Integration

This application provides REST endpoints to interact with the AI agent
and manages authentication with the Nudge API.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv

from ai_agent import AIAgent
from config import get_provider
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
            system_prompt="""You are an AI assistant for the Nudge task management system. 
You can help users manage their tasks and interact with the Nudge API.

Available capabilities:
- Task management (create, read, update, delete tasks)
- Task filtering and searchin

Important notes:
- Task categories: ACTION, ANCHOR, TRANSIT
- Task statuses: CREATED, COMPLETED, FAILED, DEFERRED
- Times are in minutes from midnight (e.g., 540 = 9:00 AM) in integer format

Always be helpful and guide users through their task management needs.""",
            tools=nudge_registry.get_tool_definitions(),
            tool_functions=nudge_registry.get_tool_functions()
        )
    return _agent


def get_nudge_base_url() -> str:
    """Get Nudge API base URL"""
    return os.getenv("NUDGE_API_BASE_URL", "http://localhost:8080")


# Pydantic models
class MessageRequest(BaseModel):
    message: str = Field(..., description="User message to the AI agent")


class MessageResponse(BaseModel):
    response: str = Field(..., description="AI agent response")
    tool_calls: Optional[list] = Field(default=None, description="Tools called by the agent")


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
    Send a message to the AI agent (STATELESS - token required per request)
    
    The AI agent will process the message and may call Nudge API tools
    to complete task management operations.
    
    STATELESS AUTHENTICATION:
    - Provide JWT token via Authorization header with EVERY request: "Bearer <token>"
    - The token is request-scoped and thread-safe (using contextvars)
    - No session state is maintained between requests
    - Token is automatically cleared after each request completes
    - Each request is completely independent
    
    Example:
        curl -X POST http://localhost:8000/agent/message \
             -H "Authorization: Bearer <your-token>" \
             -H "Content-Type: application/json" \
             -d '{"message": "Show me all my tasks"}'
    """
    # Extract token from Authorization header
    token = None
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            # If Authorization header doesn't follow Bearer format, use as-is
            token = authorization
    
    # Set token for this request (request-scoped, thread-safe)
    if token:
        set_auth_token(token)
    
    try:
        agent = get_agent()
        result = agent.run(request.message)
        
        return MessageResponse(
            response=result.get("response", ""),
            tool_calls=result.get("tool_calls")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI agent error: {str(e)}")
    finally:
        # Clear token after request to avoid token leakage between requests
        clear_auth_token()


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


# Conversation management
@app.post("/agent/reset")
async def reset_conversation():
    """
    Reset the AI agent conversation history
    
    Clears the conversation history but keeps authentication token.
    """
    agent = get_agent()
    agent.reset_conversation()
    return {"message": "Conversation reset successfully"}


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
