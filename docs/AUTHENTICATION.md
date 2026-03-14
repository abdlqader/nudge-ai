# Authentication Flow

## Overview

The AI Agent API uses **external authentication** provided by the Nudge API. Authentication tokens are passed per-request via HTTP headers.

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Login to Nudge API                                 │
│                                                              │
│  POST http://localhost:8080/auth/login                      │
│  Body: { "email": "...", "password": "..." }                │
│                                                              │
│  Response: { "token": "eyJhbG...", "user": {...} }          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                     Store Token (Client)
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Send Message to AI Agent                           │
│                                                              │
│  POST http://localhost:8000/agent/message                   │
│  Headers:                                                    │
│    - Authorization: Bearer <token>                           │
│    - Content-Type: application/json                          │
│  Body: { "message": "Show me all my tasks" }                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: FastAPI Server Processing                          │
│                                                              │
│  1. Extract token from Authorization header                 │
│  2. Set token in tools module (set_auth_token)              │
│  3. AI Agent processes message                              │
│  4. Tools use token to call Nudge API                       │
│  5. Return response to client                               │
│  6. Clear token (clear_auth_token) - per-request isolation  │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ Per-Request Authentication
- Token is provided with **each request**
- No server-side session storage
- Stateless and scalable

### ✅ Token Isolation
- Token is set at request start
- Cleared at request end
- Prevents token leakage between requests

### ✅ External Auth Management
- Authentication handled by Nudge API
- AI Agent API focuses on processing
- Clean separation of concerns

## Implementation

### Server Side (api.py)

```python
@app.post("/agent/message")
async def send_message(
    request: MessageRequest,
    authorization: Optional[str] = Header(None)
):
    # Extract token from Authorization header
    token = None
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
    
    # Set token for this request
    if token:
        set_auth_token(token)
    
    try:
        agent = get_agent()
        result = agent.run(request.message)
        return result
    finally:
        # Clear token after request
        clear_auth_token()
```

### Tools Module (tools/nudge_api.py)

```python
# Global variable for current request's token
_auth_token: Optional[str] = None

def set_auth_token(token: str) -> None:
    """Set token for current request"""
    global _auth_token
    _auth_token = token

def clear_auth_token() -> None:
    """Clear token after request"""
    global _auth_token
    _auth_token = None

def _get_headers(include_auth: bool = False) -> Dict[str, str]:
    """Get headers with token if available"""
    headers = {"Content-Type": "application/json"}
    if include_auth and _auth_token:
        headers["Authorization"] = f"Bearer {_auth_token}"
    return headers
```

## Usage Examples

### cURL

```bash
# 1. Login to Nudge API
TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mk.com", "password": "Testing123"}' \
  | jq -r '.token')

# 2. Use token with AI Agent
curl -X POST http://localhost:8000/agent/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all my tasks"}'
```

### Python

```python
import requests

# Login
response = requests.post(
    "http://localhost:8080/auth/login",
    json={"email": "admin@mk.com", "password": "Testing123"}
)
token = response.json()["token"]

# Use token
response = requests.post(
    "http://localhost:8000/agent/message",
    json={"message": "Show me all my tasks"},
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json()["response"])
```

### JavaScript

```javascript
// Login
const loginRes = await fetch("http://localhost:8080/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "admin@mk.com", password: "Testing123" })
});
const { token } = await loginRes.json();

// Use token
const msgRes = await fetch("http://localhost:8000/agent/message", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ message: "Show me all my tasks" })
});
const result = await msgRes.json();
console.log(result.response);
```

## Security Considerations

### ✅ Advantages
1. **No Server State**: No sessions to manage or clean up
2. **Horizontal Scaling**: Each request is independent
3. **Token Isolation**: No cross-request token leakage
4. **Standard OAuth**: Uses standard Bearer token pattern

### ⚠️ Important Notes
1. **Token Storage**: Client responsible for storing token securely
2. **Token Expiry**: Tokens expire after 24 hours (Nudge API default)
3. **HTTPS**: Use HTTPS in production to protect tokens in transit
4. **Token Refresh**: Implement token refresh flow for long sessions

## Testing

### Quick Test Script

```bash
# Run the test script
./test_api.sh
```

### Manual Testing

```bash
# 1. Start services
# Terminal 1: Start Nudge API
# Terminal 2: Start AI Agent API
./start_server.sh

# Terminal 3: Test
export TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mk.com", "password": "Testing123"}' \
  | jq -r '.token')

curl -X POST http://localhost:8000/agent/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a task called Test at 9 AM"}'
```

## Endpoints Summary

| Endpoint | Auth Required | Description |
|----------|---------------|-------------|
| `/health` | No | Health check |
| `/agent/status` | No | Agent info |
| `/agent/message` | **Yes** | Send message to AI |
| `/agent/reset` | No | Reset conversation |

**Auth Format**: `Authorization: Bearer <token>`

## Documentation

- **Full API Docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Quick Start**: [QUICKSTART_API.md](QUICKSTART_API.md)
- **Main README**: [README.md](README.md)
