# Nudge API Tools

AI agent tools for interacting with the Nudge task management API.

## Overview

This module provides a complete set of tools that allow the AI agent to interact with the Nudge API through natural language. The agent can authenticate users, manage tasks, and perform searches - all through conversational commands.

## Available Tools

### Authentication
- **`register_user`** - Register a new user account
- **`login`** - Authenticate and get JWT token (stored for subsequent requests)
- **`health_check`** - Verify API is running

### Task Management
- **`create_task`** - Create a new task with full details
- **`get_all_tasks`** - List all tasks with optional filtering
- **`get_task_by_id`** - Retrieve a specific task
- **`update_task`** - Update any task field
- **`delete_task`** - Remove a task

## Configuration

Add to your `.env` file:

```bash
# Nudge API Configuration
NUDGE_API_BASE_URL=http://localhost:8080
```

## Usage

### Basic Setup

```python
from ai_agent import AIAgent
from config import get_provider
from tools.nudge_api import nudge_registry

provider = get_provider()
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a Nudge task management assistant.",
    tools=nudge_registry.get_tool_definitions(),
    tool_functions=nudge_registry.get_tool_functions()
)
```

### Natural Language Commands

```python
# Check API health
agent.run("Is the Nudge API running?")

# Login
agent.run("Login with email admin@mk.com and password Testing123")

# Create a task
agent.run("Create a task called 'Morning workout' in the ACTION category for Health")

# List tasks
agent.run("Show me all my tasks")

# Filter tasks
agent.run("Show only CREATED tasks in the Work category")

# Search tasks
agent.run("Find tasks containing 'documentation'")

# Update a task
agent.run("Mark task <task-id> as COMPLETED with actual duration of 45 minutes")

# Delete a task
agent.run("Delete task <task-id>")
```

## Task Categories

- **ACTION** - Active tasks that need completion
- **ANCHOR** - Fixed schedule items (appointments, meetings)
- **TRANSIT** - Travel or commute time

## Task Statuses

- **CREATED** - New task, not started
- **COMPLETED** - Successfully finished
- **FAILED** - Could not complete
- **DEFERRED** - Postponed to later

## Time Format

Times are specified in minutes from midnight:
- 0 = 12:00 AM (midnight)
- 360 = 6:00 AM
- 540 = 9:00 AM
- 720 = 12:00 PM (noon)
- 1080 = 6:00 PM

## Authentication Flow

1. The agent automatically stores the JWT token when you login
2. Subsequent requests use this token automatically
3. Token is valid for 24 hours
4. No need to manually manage tokens

## Example Session

```python
# Run the example
pipenv run python examples/example_nudge_api.py

# Or use main.py for custom interactions
pipenv run python main.py
```

## API Endpoints Mapped

| Tool Function | HTTP Method | Endpoint | Auth Required |
|--------------|-------------|----------|---------------|
| `register_user` | POST | `/auth/register` | No |
| `login` | POST | `/auth/login` | No |
| `health_check` | GET | `/health` | No |
| `create_task` | POST | `/tasks` | Yes |
| `get_all_tasks` | GET | `/tasks` | Yes |
| `get_task_by_id` | GET | `/tasks/:id` | Yes |
| `update_task` | PUT | `/tasks/:id` | Yes |
| `delete_task` | DELETE | `/tasks/:id` | Yes |

## Error Handling

All tools return a consistent response format:

```python
{
    "success": True/False,
    "status_code": 200,
    "data": {...},  # API response
    "error": "..."  # Only present on errors
}
```

The AI agent interprets these responses and provides natural language feedback to the user.

## Development

To extend or modify the tools, edit `/tools/nudge_api.py` and use the `@nudge_registry.tool()` decorator:

```python
@nudge_registry.tool(
    description="Your tool description for the AI"
)
def your_tool(param: str) -> dict:
    """Tool implementation"""
    # Your code here
    return {"success": True, "data": result}
```
