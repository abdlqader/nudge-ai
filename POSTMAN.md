# Postman Collection - Quick Guide

Import [NudgeAI.postman_collection.json](NudgeAI.postman_collection.json) into Postman to test the AI Agent API.

## Quick Start

1. **Import Collection**: Open Postman → Import → Select `NudgeAI.postman_collection.json`

2. **Login**: Run `External Auth (Nudge API)` → `Login to Nudge API`
   - Token automatically saves to `auth_token` variable
   - Default: `admin@mk.com` / `Testing123`

3. **Test**: Run `AI Agent` → `Send Message (With Auth)`
   - Try: "Show me all my tasks"

## What's Included

### 📁 External Auth (Nudge API)
- Login to Nudge API (auto-saves token)
- Register new user

### 📁 AI Agent  
- Health Check
- Agent Status
- Send Message (with/without auth)
- Create Task
- Get All Tasks
- Filter Tasks
- Update Task
- Delete Task
- Check Nudge API Health
- Reset Conversation

### 📁 Example Workflows
- Complete workflow guide
- Natural language examples
- Task reference

## Features

✅ **Auto Token Management** - Login saves token automatically  
✅ **Bearer Auth** - Authenticated requests use saved token  
✅ **Example Responses** - See what to expect  
✅ **Pre-configured Variables** - localhost URLs ready to go  

## Variables

| Variable | Default | Change in |
|----------|---------|-----------|
| `base_url` | `http://localhost:8000` | Collection Variables |
| `nudge_api_url` | `http://localhost:8080` | Collection Variables |
| `auth_token` | (auto-set on login) | - |

## Natural Language Examples

Try these messages:
- "Create a task called 'Team meeting' at 2 PM"
- "Show me all my tasks"
- "Find all CREATED tasks in Work category"
- "Mark task {id} as COMPLETED"
- "Delete task {id}"

## Full Documentation

📘 **[Complete Postman Guide](docs/POSTMAN_GUIDE.md)** - Detailed usage instructions

## Troubleshooting

**Connection Error?**
- Start server: `./start_server.sh`
- Check: `curl http://localhost:8000/health`

**401 Unauthorized?**
- Run "Login to Nudge API" again
- Check token in Variables tab

**Nudge API unavailable?**
- Verify Nudge API is running
- Check: `curl http://localhost:8080/health`

## Need Help?

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Authentication Guide](docs/AUTHENTICATION.md)
- [Postman Guide](docs/POSTMAN_GUIDE.md)
