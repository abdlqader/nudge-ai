# AI Agent Module

A flexible Python module for creating AI agents with multi-model support and tool calling capabilities.

**✨ Modular Architecture** - Each model provider in its own folder, making it easy to add new models without touching existing code.

## Features

- **Multi-Model Support**: Easily switch between Google Gemini, Alibaba Qwen, and other models
- **Modular Design**: Each provider is isolated in its own folder - add new models without modifying existing code
- **Tool/Function Calling**: Define custom tools that the AI can use
- **Conversation Management**: Maintains conversation history with system prompts
- **Flexible Configuration**: Environment-based config with dotenv
- **Extensible Architecture**: Plugin-style provider system ([see guide](ai_agent/providers/README.md))
- **Nudge API Integration**: Pre-built tools for task management API ([see Nudge tools](tools/README_NUDGE.md))

📘 **[View Documentation](docs/README.md)** - Complete guides and architecture details

## Installation

```bash
# Install pipenv if you haven't already
pip install pipenv

# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and configure your settings:
```bash
MODEL_PROVIDER=gemini    # or 'qwen'
MODEL_NAME=gemini-pro    # or 'qwen-turbo', etc.
API_KEY=your-api-key-here
NUDGE_API_BASE_URL=http://localhost:8080  # For Nudge API integration
PORT=8000  # For FastAPI server
```

3. Run the FastAPI server (recommended for production use):
```bash
pipenv run python api.py
# Or with uvicorn:
pipenv run uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

4. Or run standalone examples:
```bash
pipenv run python main.py
pipenv run python examples/simple_example.py
```

## Quick Start

### Simple Usage (Recommended)

The easiest way to get started is using the config helper and tool registry:

```python
from ai_agent import AIAgent
from config import get_provider
from tools import create_example_tools

# Automatically loads from .env file
provider = get_provider()

# Get pre-built tools
tool_registry = create_example_tools()

# Create agent
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant.",
    tools=tool_registry.get_tool_definitions(),
    tool_functions=tool_registry.get_tool_functions()
)

# Use the agent
result = agent.run("What's the weather in Tokyo?")
print(result['response'])
```

### Manual Configuration

If you prefer more control:

```python
from ai_agent import AIAgent, GeminiProvider, QwenProvider
from dotenv import load_dotenv
import os

# Load configuration from .env
load_dotenv()

model_provider = os.getenv("MODEL_PROVIDER", "gemini")
model_name = os.getenv("MODEL_NAME", "gemini-pro")
api_key = os.getenv("API_KEY")

# Create provider based on configuration
if model_provider == "gemini":
    provider = GeminiProvider(api_key=api_key, model_name=model_name)
elif model_provider == "qwen":
    base_url = os.getenv("QWEN_BASE_URL")
    provider = QwenProvider(api_key=api_key, model_name=model_name, base_url=base_url)
```

### 2. Define Tools (Structured System)

Tools now use a structured registry system for better organization:

```python
from tools import ToolRegistry

# Create a tool registry
registry = ToolRegistry()

# Option 1: Using decorator (recommended)
@registry.tool(description="Get weather for a location")
def get_weather(location: str) -> dict:
    return {"location": location, "temp": 72, "condition": "sunny"}

# Option 2: Manual registration
def my_calculator(a: float, b: float, operation: str) -> dict:
    return {"result": a + b if operation == "add" else a - b}

registry.register(
    name="calculator",
    description="Perform calculations",
    function=my_calculator,
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"},
            "operation": {"type": "string", "enum": ["add", "subtract"]}
        },
        "required": ["a", "b", "operation"]
    }
)
```

Or use pre-built example tools:

```python
from tools import create_example_tools

tool_registry = create_example_tools()  # Weather and calculator tools
```
 with tools from registry
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant.",
    tools=tool_registry.get_tool_definitions(),
    tool_functions=tool_registry.get_tool_functions()
# Create agent
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant.",
    tools=tools,
    tool_functions=tool_functions
)

# Run a query
result = agent.run("What's the weather in New York?")
print(result['response'])

# Switch to a different model by creating a new provider
# For local Qwen, specify base_url
new_provider = QwenProvider(
    model_name="qwen-turbo",
    base_url="http://192.168.1.200:11434"  # Or use QWEN_BASE_URL env var
)
agent.switch_model(new_provider)

# Continue conversation
result = agent.run("What about London?")
print(result['response'])
```

## API Reference

### AIAgent

Main agent class for interacting with AI models.

#### Constructor

```python
AIAgent(
    model_provider: ModelProvider,
    system_prompt: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_functions: Optional[Dict[str, Callable]] = None
)
```

#### Methods

- `run(message: str, max_iterations: int = 5, **kwargs)`: Run the agent with a message
- `switch_model(new_provider: ModelProvider)`: Switch to a different model
- `update_system_prompt(system_prompt: str)`: Update the system prompt
- `add_tools(tools: List[Dict], tool_functions: Dict)`: Add or update tools
- `reset_conversation()`: Clear conversation history
- `get_conversation_history()`: Get current conversation history

### GeminiProvider

Provider for Google Gemini models.

```python
GeminiProvider(
    api_key: str,
    model_name: str = "gemini-pro"
)
```

### QwenProvider

Provider for Alibaba Qwen models (supports cloud and local deployment).

```python
QwenProvider(
    api_key: Optional[str] = None,  # Optional for local deployment
    model_name: str = "qwen-turbo",
    base_url: Optional[str] = None  # Reads from QWEN_BASE_URL env var
)
```

**Local Deployment**: When running Qwen on your local network, set `QWEN_BASE_URL` in your `.env` file. API key is optional for local setups.

## Nudge API Integration

The AI agent includes a FastAPI server and pre-built tools for interacting with the Nudge task management API.

📖 **[FastAPI Documentation](API_DOCUMENTATION.md)** - Complete API reference  
🔐 **[Authentication Guide](AUTHENTICATION.md)** - External auth flow explained  
📮 **[Postman Collection](NudgeAI.postman_collection.json)** - [Quick Guide](POSTMAN.md) | [Full Guide](docs/POSTMAN_GUIDE.md)

### Authentication Flow

1. **Login to Nudge API** (external): Get JWT token from `http://localhost:8080/auth/login`
2. **Pass token to AI Agent**: Include `Authorization: Bearer <token>` header in requests
3. **AI uses token**: Tools automatically use the token to call Nudge API

**Key Feature**: Per-request authentication - no server-side session storage

### FastAPI Server (Recommended)

Start the REST API server to interact with the AI agent via HTTP endpoints:

```bash
pipenv run python api.py
# Server runs on http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

**Available Endpoints:**
- `POST /agent/message` - Send message to AI (requires Authorization header with token)
- `GET /agent/status` - Check agent and tool status
- `POST /agent/reset` - Reset conversation

**Authentication**: Login via Nudge API, pass token in Authorization header.

**Example Usage:**
```bash
# Login
curl -X to Nudge API (external)
TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mk.com", "password": "Testing123"}' \
  | jq -r '.token')

# Send message to AI with token
curl -X POST http://localhost:8000/agent/message \
  -H "Authorization: Bearer $TOKEN"
  -d '{"message": "Show me all my tasks"}'
```

### Python SDK Usage

Alternatively, use the agent directly in Python:

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

# Natural language commands (authentication is handled by FastAPI endpoints)
agent.run("Create a task called 'Morning workout' starting at 6 AM")
agent.run("Show me all my tasks")
```

### Available Tools

- **Task Management**: `create_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`, `health_check`

**Note**: Authentication is handled by the FastAPI endpoints (`/auth/login`, `/auth/register`). The token is automatically used by the tools.

### Configuration

Add to your `.env`:
```bash
NUDGE_API_BASE_URL=http://localhost:8080
```

### Run Examples

```bash
# Interactive Nudge API assistant
pipenv run python examples/example_nudge_api.py

# Or use main.py (already configured for Nudge API)
pipenv run python main.py
```

## Advanced Usage

### Custom Model Provider

You can create custom model providers by inheriting from `ModelProvider`:

```python
from ai_agent.base import ModelProvider

class CustomProvider(ModelProvider):
    def generate(self, messages, tools=None, **kwargs):
        # Your implementation
        return {
            'content': 'Generated text',
            'tool_calls': [],
            'finish_reason': 'stop'
        }
    
    def supports_tools(self):
        return True  # or False
```

For a complete guide on adding new providers to the project structure, see [ai_agent/providers/README.md](ai_agent/providers/README.md).

📚 **More Documentation:** See [docs/](docs/) folder for detailed guides on architecture, project structure, and more.

### Environment Variables
Configuration is managed through a `.env` file:

```bash
# Required
MODEL_PROVIDER=gemini          # 'gemini' or 'qwen'
MODEL_NAME=gemini-pro          # Model variant
API_KEY=your-api-key-here      # Your API key (not required for local Qwen)

# Optional: Separate keys for each provider
GEMINI_API_KEY=your-gemini-key
QWEN_API_KEY=your-qwen-key     # Optional for local Qwen

# Qwen Local Deployment (OpenAI-compatible endpoint)
# Example: http://192.168.1.200:11434
QWEN_BASE_URL=http://localhost:11434
```

The `.env` file is automatically loaded by the example script. For custom scripts:

```python
from dotenv import load_dotenv
import os

load_dotenv()
provider_type = os.getenv("MODEL_PROVIDER")
api_key = os.getenv("
api_key = os.getenv("GEMINI_API_KEY")
```

## Examples

Run the examples:

```Project Structure

```
nudge-ai/
├── ai_agent/                      # Main package (modular structure)
│   ├── __init__.py               # Package exports
│   ├── base.py                   # Abstract ModelProvider base class
│   ├── agent.py                  # AIAgent implementation
│   └── providers/                # Model providers (extensible)
│       ├── __init__.py           # Provider exports
│       ├── README.md             # Guide for adding new providers
│       ├── gemini/               # Google Gemini provider
│       │   ├── __init__.py
│       │   └── provider.py
│       └── qwen/                 # Alibaba Qwen provider
│           ├── __init__.py
│           └── provider.py
├── config.py                     # Configuration helper (loads from .env)
├── test_config.py                # Test your .env configuration
├── simple_example.py             # Simple usage example
├── example_usage.py              # Full example with tools
├── Pipfile                       # Pipenv dependencies
├── docs/                          # Documentation folder
│   ├── README.md                 # Documentation index
│   ├── QUICKSTART.md             # Quick start guide
│   ├── ARCHITECTURE.md           # System design
│   └── ...                       # More documentation
├── .env.example                  # Template for environment variables
├── .env                          # Your actual config (create from .env.example)
└── README.md                     # This file (main entry point)
```

### Adding New Model Providers

The modular structure makes it easy to add support for new AI models. See [ai_agent/providers/README.md](ai_agent/providers/README.md) for a complete guide.

### Creating Custom Tools

Tools are now structured using a registry system. See [tools/README.md](tools/README.md) for a complete guide.

## Examples

All examples are in the [examples/](examples/) folder:

- **[simple_example.py](examples/simple_example.py)** - Basic agent setup
- **[example_with_tools.py](examples/example_with_tools.py)** - Using pre-built tools
- **[example_decorator_tools.py](examples/example_decorator_tools.py)** - Decorator syntax for tools
- **[example_usage.py](examples/example_usage.py)** - Complete workflow example
- **[example_custom_provider.py](examples/example_custom_provider.py)** - Adding custom providers

Run any example:
```bash
pipenv run python examples/<filename>.py
```

See [examples/README.md](examples/README.md) for detailed documentation.

## API Reference

- Python 3.8+
- pipenv
- google-generativeai >= 0.3.0
- openai >= 1.0.0

All Python dependencies are managed via Pipfile.

To run your application:
```bash
pipenv run python main.py
```

To run examples:
```bash
pipenv run python examples/simple_example.py
pipenv run python examples/example_with_tools.py
```

## License

MIT License
