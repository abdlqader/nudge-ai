# FastAPI Application - Nudge AI Agent

REST API server that provides endpoints to interact with the AI agent and manages authentication with the Nudge task management system.

📮 **[Postman Collection](../NudgeAI.postman_collection.json)** - Import into Postman for easy testing

## Overview

The FastAPI application serves as the backend for the AI agent, handling:
- User authentication (register/login) with the Nudge API
- Message processing through the AI agent
- Token management for authenticated API calls
- Conversation state management

## Quick Start

### 1. Install Dependencies

```bash
pipenv install
```

### 2. Configure Environment

Ensure your `.env` file has:

```bash
# Model Configuration
MODEL_PROVIDER=qwen
MODEL_NAME=qwen3:8b
QWEN_BASE_URL=http://192.168.1.200:11434
USE_OLLAMA_CLIENT=true

# Nudge API
NUDGE_API_BASE_URL=http://localhost:8080

# Server Port
PORT=8000
```

### 3. Start the Server

```bash
pipenv run python api.py
```

Or with uvicorn directly:

```bash
pipenv run uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "service": "nudge-ai-agent"
}
```

---

### Authentication

Authentication is handled **externally** via the Nudge API. The AI Agent API uses token-based authentication where you:

1. Login to Nudge API directly at `http://localhost:8080/auth/login`
2. Receive a JWT token
3. Pass the token to AI Agent API via `Authorization: Bearer <token>` header

**External Authentication Endpoints (Nudge API):**

#### Register User (Nudge API)

**POST** `http://localhost:8080/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

#### Login (Nudge API)

**POST** `http://localhost:8080/auth/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "admin@mk.com",
  "password": "Testing123"
}
```

**Response:** `200 OK`
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "admin@mk.com",
    "first_name": "Mo",
    "last_name": "Ka"
  }
}
```

**Use this token** in the `Authorization` header for AI Agent requests.

---

### AI Agent

#### Send Message

**POST** `/agent/message`

Send a message to the AI agent. The agent will process the message and may call Nudge API tools to perform task operations.

**Authentication Required:** Pass JWT token via `Authorization: Bearer <token>` header

**Request Headers:**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Create a task called 'Morning workout' starting at 6 AM"
}
```

**Response:** `200 OK`
```json
{
  "response": "I've created a task called 'Morning workout' for you...",
  "tool_calls": [
    {
      "name": "create_task",
      "arguments": {
        "name": "Morning workout",
        "task_category": "ACTION",
        "start_at": 360
      }
    }
  ]
}
```

**Example Messages:**
- "Show me all my tasks"
- "Create a task called 'Team meeting' at 2 PM for 60 minutes"
- "Find all CREATED tasks in the Work category"
- "Mark task <id> as COMPLETED"
- "Delete task <id>"

**Note:** Token is required for task-related operations. Each request must include the Authorization header.

---

#### Agent Status

**GET** `/agent/status`

Get information about the AI agent configuration.

**Response:** `200 OK`
```json
{
  "agent": {
    "provider": "QwenProvider",
    "model": "qwen3:8b",
    "tools_count": 6,
    "available_tools": ["create_task", "get_all_tasks", "get_task_by_id", "update_task", "delete_task", "health_check"]
  },
  "nudge_api_url": "http://localhost:8080",
  "authentication": "Token required via Authorization header for task operations"
}
```

---

#### Reset Conversation

**POST** `/agent/reset`

Clear the conversation history.

**Response:** `200 OK`
```json
{
  "message": "Conversation reset successfully"
}
```

---

## Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/auth/register \
  Login to Nudge API (external)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mk.com",
    "password": "Testing123"
  }'
# Copy the token from response

# Set token as variable
export TOKEN="your-token-here"

# Send message to AI
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN"
  }'

# Check agent status
curl http://localhost:8000/agent/status

# Reset conversation
curl -X POST http://localhost:8000/agent/reset
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@mk.com", "password": "Testing123"}
NUDGE_API_URL = "http://localhost:8080"

# Login to Nudge API
login_response = requests.post(
    f"{NUDGE_API_URL}/auth/login",
    json={"email": "admin@mk.com", "password": "Testing123"}
)
token = login_response.json()["token"]

# Send message to AI with token
message_response = requests.post(
    f"{BASE_URL}/agent/message",
    json={"message": "Create a task called 'Review code' for tomorrow"},
    headers={"Authorization": f"Bearer {token}"}
)
print(message_response.json()["response"])

# Get all tasks
tasks_response = requests.post(
    f"{BASE_URL}/agent/message",
    json={"message": "Show me all my tasks"},
    headers={"Authorization": f"Bearer {token}

```javascript
const BASE_URL = "http://localhost:8000";

// Login
const NUDGE_API_URL = "http://localhost:8080";

// Login to Nudge API
const loginResponse = await fetch(`${NUDGE_API_URL}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "admin@mk.com",
    password: "Testing123"
  })
});
const loginData = await loginResponse.json();
const token = loginData.token;

// Send message to AI with token
const messageResponse = await fetch(`${BASE_URL}/agent/message`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  2 PM"
  })
});
External Authentication Flow:
    Client
      ↓
    Nudge API (/auth/login)
      ↓
    JWT Token
      ↓
    Client stores token

AI Agent Request Flow:
    Client
      ↓
    POST /agent/message
    with Authorization: Bearer <token>
      ↓
    FastAPI extracts & sets token
      ↓
    AI Agent processes message
      ↓
    Tools use token for Nudge API calls
      ↓
    Response to client
      ↓
    FastAPI clears token (per-request isolation)
```

## Features

- **Per-Request Authentication**: Token passed with each request, no server-side session storage
- **Token Isolation**: Each request is isolated, preventing token leakage between users
- **External Auth**: Authentication handled by Nudge API, AI agent focuses on task processing
- **Natural Language Interface**: Talk to the AI in plain English to manage tasks
- **Interactive Documentation**: Built-in Swagger UI at `/docs`
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Clear error messages and proper HTTP status codes
- **Stateful Conversations**: Maintains conversation history per agent instance

- **Automatic Token Management**: Login once, token is stored and used for all AI agent operations
- **Natural Language Interface**: Talk to the AI in plain English to manage tasks
- **Interactive Documentation**: Built-in Swagger UI at `/docs`
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Clear error messages and proper HTTP status codes
- **Stateful Conversations**: Maintains conversation history until reset

## Development

### Running with Auto-Reload

```bash
pipenv run uvicorn api:app --reload --port 8000
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `NUDGE_API_BASE_URL` | Nudge API endpoint | `http://localhost:8080` |
| `MODEL_PROVIDER` | AI model provider | `gemini` |
| `MODEL_NAME` | AI model name | `gemini-pro` |
| `QWEN_BASE_URL` | Qwen/Ollama URL | `http://localhost:11434` |

## Production Deployment

For production, configure CORS origins appropriately in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

And use a production ASGI server:

```bash
pipenv run uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### Port Already in Use

Change the port in `.env`:
```bash
PORT=8001
```

### Nudge API Connection Issues

Verify the Nudge API is running and accessible:
```bash
curl http://localhost:8080/health
```

### AI Model Connection Issues

For Qwen/Ollama, ensure the service is accessible:
```bash
curl http://192.168.1.200:11434/api/tags
```
