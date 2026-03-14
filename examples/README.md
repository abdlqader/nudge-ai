# Examples

This folder contains example implementations demonstrating various features of the AI Agent module.

## Running Examples

All examples can be run from the project root:

```bash
# Basic setup verification
pipenv run python examples/simple_example.py

# Structured tools system
pipenv run python examples/example_with_tools.py

# Decorator-style tool definitions
pipenv run python examples/example_decorator_tools.py

# Complete workflow example
pipenv run python examples/example_usage.py

# Custom provider implementation
pipenv run python examples/example_custom_provider.py

# Nudge API integration (direct Python)
pipenv run python examples/example_nudge_api.py

# REST API client (requires FastAPI server running)
pipenv run python examples/example_client.py
```

## Example Files

### [simple_example.py](simple_example.py)
**Purpose:** Basic agent setup and configuration testing

- Loads provider from .env
- Creates a basic agent
- Minimal example for verifying setup

**Use when:** Testing your configuration or getting started.

### [example_with_tools.py](example_with_tools.py)
**Purpose:** Demonstrates structured tools system

- Uses pre-built example tools
- Shows tool registry usage
- Agent creation with tools

**Use when:** Learning how to add tools to your agent.

### [example_decorator_tools.py](example_decorator_tools.py)
**Purpose:** Decorator syntax for defining tools

- Shows `@registry.tool()` decorator
- Demonstrates tool execution testing

**Use when:** Understanding decorator-based tool registration.

### [example_nudge_api.py](example_nudge_api.py)
**Purpose:** Direct Python integration with Nudge API

- Shows all 6 Nudge API tools
- Interactive conversation mode
- Task management through natural language

**Use when:** Using the agent directly in Python code.

### [example_client.py](example_client.py)
**Purpose:** REST API client for FastAPI server

- HTTP-based interaction with AI agent
- Login/logout flow
- Message sending via API endpoints
- Interactive chat mode

**Requirements:** FastAPI server must be running (`pipenv run python api.py`)

**Use when:** Building web/mobile apps or microservices.
- Multiple tool definitions

**Use when:** Creating custom tools with clean syntax.

### [example_usage.py](example_usage.py)
**Purpose:** Complete workflow example

- Environment configuration
- Provider switching
- Tool integration
- System prompt management

**Use when:** Understanding the full agent lifecycle.

### [example_custom_provider.py](example_custom_provider.py)
**Purpose:** Adding custom model providers

- Shows how to implement a new provider (OpenAI example)
- Extends the provider system
- Provider base class usage

**Use when:** Adding support for new AI models.

## Quick Start

1. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

2. **Test setup:**
   ```bash
   pipenv run python examples/simple_example.py
   ```

3. **Try tools:**
   ```bash
   pipenv run python examples/example_with_tools.py
   ```

4. **Start building:**
   ```bash
   # Use main.py for your implementation
   pipenv run python main.py
   ```

## Learning Path

1. **Start here:** `simple_example.py` - Verify your setup works
2. **Add tools:** `example_with_tools.py` - Learn the tools system
3. **Custom tools:** `example_decorator_tools.py` - Create your own tools
4. **Full workflow:** `example_usage.py` - See everything together
5. **Extend:** `example_custom_provider.py` - Add new AI models

## Documentation

- **Main README:** [../README.md](../README.md)
- **Documentation Hub:** [../docs/README.md](../docs/README.md)
- **Quick Start:** [../docs/QUICKSTART.md](../docs/QUICKSTART.md)
- **Tools Guide:** [../tools/README.md](../tools/README.md)
- **Providers Guide:** [../ai_agent/providers/README.md](../ai_agent/providers/README.md)
- **Architecture:** [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

## Tips

- All examples require `.env` configuration (API keys)
- Examples are self-contained and can be run independently
- Check comments in each file for customization options
- Examples use simulated/mock data for tool demonstrations
- Uncomment example queries to test with real API calls
