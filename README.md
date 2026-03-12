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
```

3. Test the configuration (without making API calls):
```bash
pipenv run python test_config.py
```

4. Run your main application:
```bash
pipenv run python main.py
```

Or run an example:
```bash
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
    provider = QwenProvider(api_key=api_key, model_name=model_name)
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
new_provider = QwenProvider(api_key=qwen_api_key, model_name="qwen-turbo")
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

Provider for Alibaba Qwen models.

```python
QwenProvider(
    api_key: str,
    model_name: str = "qwen-turbo"
)
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
API_KEY=your-api-key-here      # Your API key

# Optional: Separate keys for each provider
GEMINI_API_KEY=your-gemini-key
QWEN_API_KEY=your-qwen-key
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
