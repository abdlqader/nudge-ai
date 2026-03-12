# Tools System Guide

## Overview

The tools system provides a structured way to define, register, and manage tools (functions) that the AI agent can use. Instead of hardcoding tool definitions in your main code, tools are now organized in a modular, reusable system.

## Architecture

```
tools/
├── __init__.py          # Package exports
├── registry.py          # ToolRegistry and Tool classes
└── examples.py          # Example tool implementations
```

## Basic Usage

### 1. Using Pre-defined Tools

```python
from ai_agent import AIAgent
from config import get_provider
from tools import create_example_tools

# Get tools from example registry
tool_registry = create_example_tools()

# Create agent with tools
provider = get_provider()
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant.",
    tools=tool_registry.get_tool_definitions(),
    tool_functions=tool_registry.get_tool_functions()
)
```

### 2. Creating Custom Tools with Registry

```python
from tools import ToolRegistry

# Create a new registry
registry = ToolRegistry()

# Define your function
def my_tool(param1: str, param2: int) -> dict:
    return {"result": f"{param1} - {param2}"}

# Register it
registry.register(
    name="my_tool",
    description="Does something useful",
    function=my_tool,
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "First parameter"},
            "param2": {"type": "integer", "description": "Second parameter"}
        },
        "required": ["param1", "param2"]
    }
)

# Use with agent
agent = AIAgent(
    model_provider=provider,
    tools=registry.get_tool_definitions(),
    tool_functions=registry.get_tool_functions()
)
```

### 3. Using Decorator Syntax (Recommended)

```python
from tools import ToolRegistry

registry = ToolRegistry()

@registry.tool(description="Search the web for information")
def web_search(query: str, max_results: int = 5) -> dict:
    """Search the web"""
    return {"query": query, "results": [...]}

@registry.tool(description="Get current weather")
def get_weather(location: str) -> dict:
    """Get weather for a location"""
    return {"location": location, "temp": 72}

# All decorated functions are automatically registered
agent = AIAgent(
    model_provider=provider,
    tools=registry.get_tool_definitions(),
    tool_functions=registry.get_tool_functions()
)
```

## Tool Class

The `Tool` class represents a single tool:

```python
from tools import Tool

tool = Tool(
    name="my_function",
    description="What it does",
    function=my_function,
    parameters={...}
)

# Convert to OpenAI format
openai_format = tool.to_openai_format()

# Execute the tool
result = tool.execute(arg1="value", arg2=123)
```

## ToolRegistry Class

The `ToolRegistry` class manages multiple tools:

### Methods

**`register(name, description, function, parameters=None)`**
Register a tool manually.

**`tool(name=None, description=None, parameters=None)`**
Decorator for registering tools.

**`get(name)`**
Get a specific tool by name.

**`get_all()`**
Get list of all registered tools.

**`get_tool_definitions()`**
Get all tools in OpenAI function calling format.

**`get_tool_functions()`**
Get dictionary mapping tool names to callable functions.

**`remove(name)`**
Remove a tool by name.

**`clear()`**
Remove all tools.

## Parameter Schema

Tools use JSON Schema for parameters (OpenAI function calling format):

```python
parameters = {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "City name"
        },
        "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "Temperature units"
        },
        "days": {
            "type": "integer",
            "description": "Number of days to forecast"
        }
    },
    "required": ["location"]  # Optional parameters not in required
}
```

### Supported Types

- `string` - Text
- `integer` - Whole numbers
- `number` - Integers or floats
- `boolean` - True/False
- `array` - Lists
- `object` - Nested objects
- `enum` - Fixed set of values

## Auto-generated Parameters

If you don't provide parameters, the registry can auto-generate them from function signatures:

```python
@registry.tool(description="Calculate sum")
def add_numbers(a: int, b: int, c: int = 0) -> int:
    return a + b + c

# Parameters automatically generated:
# {
#     "type": "object",
#     "properties": {
#         "a": {"type": "integer", "description": "Parameter a"},
#         "b": {"type": "integer", "description": "Parameter b"},
#         "c": {"type": "integer", "description": "Parameter c"}
#     },
#     "required": ["a", "b"]  # c is optional (has default)
# }
```

## Creating Tool Collections

Organize related tools in separate files:

```python
# tools/weather_tools.py
from .registry import ToolRegistry

def create_weather_tools():
    registry = ToolRegistry()
    
    @registry.tool(description="Get current weather")
    def current_weather(location: str):
        return {...}
    
    @registry.tool(description="Get forecast")
    def weather_forecast(location: str, days: int):
        return {...}
    
    return registry

# tools/math_tools.py
def create_math_tools():
    registry = ToolRegistry()
    
    @registry.tool(description="Calculate")
    def calculator(operation: str, a: float, b: float):
        return {...}
    
    return registry
```

Then combine them:

```python
from tools.weather_tools import create_weather_tools
from tools.math_tools import create_math_tools

# Merge registries
weather_reg = create_weather_tools()
math_reg = create_math_tools()

all_tools = weather_reg.get_tool_definitions() + math_reg.get_tool_definitions()
all_functions = {**weather_reg.get_tool_functions(), **math_reg.get_tool_functions()}

agent = AIAgent(
    model_provider=provider,
    tools=all_tools,
    tool_functions=all_functions
)
```

## Global Registry

Use the global default registry for simple cases:

```python
from tools import tool, default_registry

@tool(description="My tool")
def my_function(x: str):
    return {"result": x}

# Access via default_registry
agent = AIAgent(
    model_provider=provider,
    tools=default_registry.get_tool_definitions(),
    tool_functions=default_registry.get_tool_functions()
)
```

## Testing Tools

Test tools independently before using with agent:

```python
registry = ToolRegistry()

@registry.tool(description="Add numbers")
def add(a: int, b: int) -> int:
    return a + b

# Get the tool
add_tool = registry.get("add")

# Test execution
result = add_tool.execute(a=5, b=3)
print(result)  # 8

# Test with agent
agent = AIAgent(
    model_provider=provider,
    tools=registry.get_tool_definitions(),
    tool_functions=registry.get_tool_functions()
)
```

## Examples

See the example files:
- **[example_with_tools.py](../examples/example_with_tools.py)** - Basic tool usage
- **[example_decorator_tools.py](../examples/example_decorator_tools.py)** - Decorator syntax
- **[example_usage.py](../examples/example_usage.py)** - Updated to use tool registry

## Benefits

✅ **Organized** - Tools in separate, reusable modules
✅ **Type-safe** - Clear function signatures and parameter schemas
✅ **Testable** - Test tools independently
✅ **Discoverable** - List and inspect registered tools
✅ **Maintainable** - Add/remove tools without changing agent code
✅ **Reusable** - Share tool collections across projects
