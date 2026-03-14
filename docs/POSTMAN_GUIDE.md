# Using the Postman Collection

This guide explains how to use the Nudge AI Agent Postman collection for testing and development.

## Import the Collection

1. Open Postman
2. Click **Import** button
3. Select `NudgeAI.postman_collection.json`
4. The collection will appear in your workspace

## Collection Structure

### 📁 External Auth (Nudge API)
- **Login to Nudge API** - Get JWT token (auto-saves to variable)
- **Register User (Nudge API)** - Create new account

### 📁 AI Agent
- **Health Check** - Verify API is running
- **Agent Status** - View configuration and available tools
- **Send Message (No Auth)** - Test without authentication
- **Send Message (With Auth)** - Authenticated requests
- **Create Task** - Natural language task creation
- **Get All Tasks** - List all user tasks
- **Filter Tasks** - Search and filter tasks
- **Update Task** - Modify task status/details
- **Delete Task** - Remove a task
- **Check Nudge API Health** - Verify Nudge API status
- **Reset Conversation** - Clear chat history

### 📁 Example Workflows
- Complete workflow documentation and examples

## Quick Start

### 1. Configure Variables

The collection uses these variables (pre-configured):

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://localhost:8000` | AI Agent API URL |
| `nudge_api_url` | `http://localhost:8080` | Nudge API URL |
| `auth_token` | (auto-set) | JWT token from login |

To change:
1. Right-click collection → **Edit**
2. Go to **Variables** tab
3. Update **Current Value**

### 2. Login to Get Token

**Run:** `External Auth (Nudge API)` → `Login to Nudge API`

The request automatically:
- Sends login credentials
- Extracts the JWT token from response
- Saves it to `auth_token` variable
- Uses it in subsequent authenticated requests

**Default credentials:**
- Email: `admin@mk.com`
- Password: `Testing123`

### 3. Test the Connection

**Run:** `AI Agent` → `Health Check`

Expected response:
```json
{
  "status": "ok",
  "service": "nudge-ai-agent"
}
```

### 4. Check Agent Status

**Run:** `AI Agent` → `Agent Status`

See:
- AI model provider and name
- Number of available tools
- Tool list
- Nudge API URL

### 5. Send Your First Message

**Run:** `AI Agent` → `Send Message (With Auth)`

Try these messages:
- "Show me all my tasks"
- "Create a task called 'Morning workout' at 6 AM"
- "Find all CREATED tasks"

## Example Requests

### Simple Greeting (No Auth)

```
POST {{base_url}}/agent/message
Content-Type: application/json

{
  "message": "Hello! What can you help me with?"
}
```

### Create a Task (With Auth)

```
POST {{base_url}}/agent/message
Authorization: Bearer {{auth_token}}
Content-Type: application/json

{
  "message": "Create a task called 'Team meeting' at 2 PM for 60 minutes in the Work category"
}
```

### List Tasks (With Auth)

```
POST {{base_url}}/agent/message
Authorization: Bearer {{auth_token}}
Content-Type: application/json

{
  "message": "Show me all my tasks"
}
```

### Filter Tasks (With Auth)

```
POST {{base_url}}/agent/message
Authorization: Bearer {{auth_token}}
Content-Type: application/json

{
  "message": "Find all CREATED tasks in the Work category"
}
```

## Natural Language Examples

The AI understands natural language. Try these:

### Task Creation
- "Create a task called 'Morning workout' at 6 AM for 45 minutes"
- "Add a meeting at 2 PM today for 1 hour"
- "Schedule 'Code review' at 3 PM in the Work category"

### Task Listing
- "Show me all my tasks"
- "What tasks do I have?"
- "List my tasks"

### Filtering
- "Show only CREATED tasks"
- "Find tasks in the Work category"
- "What ACTION tasks do I have?"
- "Search for tasks containing 'meeting'"

### Updates
- "Mark task <task-id> as COMPLETED"
- "Update task <task-id> with actual duration of 30 minutes"
- "Change task <task-id> to COMPLETED status"

### Deletion
- "Delete task <task-id>"
- "Remove task <task-id>"

### API Health
- "Is the Nudge API working?"
- "Check if Nudge API is healthy"
- "Test the Nudge API connection"

## Authentication

### Automatic Token Management

The collection automatically manages authentication:

1. **Login Request** has a Post-response Script:
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.collectionVariables.set("auth_token", jsonData.token);
   }
   ```

2. **Authenticated Requests** use Bearer token:
   - Auth Type: Bearer Token
   - Token: `{{auth_token}}`

### Manual Token Management

If needed, you can manually set the token:

1. Copy token from login response
2. Right-click collection → **Edit**
3. Go to **Variables** tab
4. Paste token in `auth_token` Current Value

### Token Expiry

Tokens expire after 24 hours. If you get 401 errors:
1. Run "Login to Nudge API" again
2. Token will automatically update

## Response Format

All AI Agent responses follow this format:

```json
{
  "response": "AI's natural language response",
  "tool_calls": [
    {
      "name": "tool_name",
      "arguments": { ... }
    }
  ]
}
```

- `response` - Human-readable AI response
- `tool_calls` - Tools used (optional, for debugging)

## Task Reference

### Task Categories
- **ACTION** - Active tasks that need completion
- **ANCHOR** - Fixed schedule items (appointments, meetings)
- **TRANSIT** - Travel or commute time

### Task Statuses
- **CREATED** - New task, not started
- **COMPLETED** - Successfully finished
- **FAILED** - Could not complete
- **DEFERRED** - Postponed to later

### Time Format

Times are in minutes from midnight:
- **0** = 12:00 AM (midnight)
- **360** = 6:00 AM
- **540** = 9:00 AM
- **720** = 12:00 PM (noon)
- **840** = 2:00 PM
- **1080** = 6:00 PM

## Troubleshooting

### Connection Refused

**Error:** `Could not send request`

**Solutions:**
1. Verify AI Agent API is running: `./start_server.sh`
2. Check `base_url` variable matches your server
3. Try: `curl http://localhost:8000/health`

### 401 Unauthorized

**Error:** `Unauthorized` or `401`

**Solutions:**
1. Run "Login to Nudge API" request again
2. Verify token is saved (check Variables tab)
3. Ensure auth is enabled on request (Auth tab)

### Nudge API Connection Error

**Error:** Response mentions Nudge API unavailable

**Solutions:**
1. Verify Nudge API is running
2. Check `nudge_api_url` variable
3. Test: `curl http://localhost:8080/health`

### Empty or Error Response

**Solutions:**
1. Check request body is valid JSON
2. Verify message is in the correct format
3. Look at Console tab for detailed errors

## Tips & Tricks

### Environment Setup

Create environments for different setups:
1. Click **Environments** in Postman
2. Create "Local", "Staging", "Production"
3. Set different `base_url` and `nudge_api_url` values
4. Switch environments as needed

### Save Responses

Right-click response → **Save Response** → **Save as example**
- Builds collection documentation
- Shows expected responses
- Helps team members

### Test Scripts

Add test scripts to verify responses:

```javascript
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('response');
});
```

### Console Logging

Enable Console (View → Show Postman Console) to see:
- Full request/response details
- Token values
- Script execution logs
- Error messages

## Next Steps

- Read [API Documentation](API_DOCUMENTATION.md)
- Learn about [Authentication Flow](AUTHENTICATION.md)
- See [Quick Start Guide](QUICKSTART_API.md)
- Explore [Python Examples](../examples/)

## Working with the Collection

### Organize Folders

Use folders to organize related requests:
- Add new folder: Right-click collection → **Add Folder**
- Drag requests into folders
- Rename folders for clarity

### Share Collection

Export and share with team:
1. Right-click collection → **Export**
2. Choose format (Collection v2.1)
3. Share JSON file
4. Team imports into their Postman

### Keep Updated

When API changes:
1. Update request URLs/bodies
2. Modify variables if needed
3. Re-export and share
4. Document changes in description

## Support

For issues or questions:
- Check [API Documentation](API_DOCUMENTATION.md)
- Review [Authentication Guide](AUTHENTICATION.md)
- See [Examples](../examples/)
- View server logs when running `./start_server.sh`
