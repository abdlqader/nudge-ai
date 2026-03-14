# Quick Start Guide - FastAPI Server

## Postman Collection

📮 **[Import Postman Collection](../NudgeAI.postman_collection.json)**

The collection includes:
- External authentication flow (Nudge API login)
- All AI Agent endpoints with examples
- Automatic token management
- Example workflows and natural language queries

**Quick Setup:**
1. Import `NudgeAI.postman_collection.json` into Postman
2. Run "Login to Nudge API" request (token auto-saves)
3. Use any "Send Message" request with authentication

## Start the Server

```bash
# Using the startup script (recommended)
./start_server.sh

# Or directly with Python
pipenv run python api.py

# Or with uvicorn for development (auto-reload)
pipenv run uvicorn api:app --reload --port 8000
```

Server will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test with cURL

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Login to Nudge API (external - not part of AI agent API)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mk.com", "password": "Testing123"}'
# Save the token from response

# 3. Send message to AI with token
export TOKEN="your-token-here"
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Show me all my tasks"}'

# 4. Check status
curl http://localhost:8000/agent/status

# 5. Create a task (with token)
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Create a task called Morning workout at 6 AM for 45 minutes"}'
```

## Quick Test with Python

```python
import requests

BASE_URL = "http://localhost:8000"
NUDGE_API_URL = "http://localhost:8080"

# Login to Nudge API
response = requests.post(
    f"{NUDGE_API_URL}/auth/login",
    json={"email": "admin@mk.com", "password": "Testing123"}
)
token = response.json()["token"]

# Send message to AI with token
response = requests.post(
    f"{BASE_URL}/agent/message",
    json={"message": "Show me all my tasks"},
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json()["response"])
```

## Run the Example Client

```bash
# Make sure server is running first
pipenv run python examples/example_client.py
```

## Environment Configuration

Create/edit `.env`:

```bash
# Required
MODEL_PROVIDER=qwen
MODEL_NAME=qwen3:8b
QWEN_BASE_URL=http://192.168.1.200:11434
USE_OLLAMA_CLIENT=true

# Nudge API
NUDGE_API_BASE_URL=http://localhost:8080

# Server
PORT=8000
```

## Common Issues

### Port Already in Use
```bash
# Change port in .env
PORT=8001
```

### Nudge API Not Available
```bash
# Check if Nudge API is running
curl http://localhost:8080/health
```

### Model Connection Issues
```bash
# For Qwen/Ollama
curl http://192.168.1.200:11434/api/tags
```

## Architecture Flow

    ↓
Login to Nudge API (http://localhost:8080/auth/login)
    ↓
Get JWT Token
    ↓
Send message to AI Agent (http://localhost:8000/agent/message)
    with Authorization: Bearer <token>
    ↓
FastAPI sets token for request
    ↓
AI Agent processes message
    ↓
Tools use token to call Nudge API (/tasks/*)
    ↓
Response to Client
    ↓
FastAPI clears token (per-request isolation)*)
    │       ↓
    └── Response to Client
```gent/message` | POST | Send message to AI (requires Authorization header) |
| `/agent/status` | GET | Get agent status |
| `/agent/reset` | POST | Reset conversation |

**Note:** Authentication is handled externally. Login via Nudge API (`http://localhost:8080/auth/login`) and pass the token to `/agent/message` via `Authorization: Bearer <token>` header.
| `/health` | GET | Health check |
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | Login and get token |
| `/auth/logout` | POST | Clear token |
| `/agent/message` | POST | Send message to AI |
| `/agent/status` | GET | Get agent status |
| `/agent/reset` | POST | Reset conversation |

## Natural Language Examples

Once logged in, you can send these messages:

- "Show me all my tasks"
- "Create a task called 'Team meeting' at 2 PM for 60 minutes"
- "Find all CREATED tasks in the Work category"
- "Update task <id> to COMPLETED status"
- "Delete task <id>"
- "Search for tasks containing 'documentation'"
- "Show me all ACTION tasks"
- "Create a workout task at 6 AM"

## Documentation

- **Full API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Nudge Tools**: [tools/README_NUDGE.md](tools/README_NUDGE.md)
- **Project README**: [README.md](README.md)
- **Examples**: [examples/README.md](examples/README.md)
