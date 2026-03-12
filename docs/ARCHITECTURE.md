# Project Architecture

## Overview

The AI Agent module is designed with a modular, extensible architecture that makes it easy to add support for new AI model providers without modifying existing code.

## Core Components

### 1. Base Classes (`ai_agent/base.py`)

Defines the `ModelProvider` abstract base class that all providers must implement:

```python
class ModelProvider(ABC):
    @abstractmethod
    def generate(messages, tools, **kwargs) -> Dict
    
    @abstractmethod
    def supports_tools() -> bool
```

### 2. Agent (`ai_agent/agent.py`)

The `AIAgent` class handles:
- Conversation management
- Tool/function calling loop
- Model switching
- System prompt management

### 3. Providers (`ai_agent/providers/`)

Each provider is in its own folder with:
- `__init__.py` - Exports the provider class
- `provider.py` - Implementation inheriting from `ModelProvider`

Current providers:
- **Gemini** (`providers/gemini/`) - Google's Gemini models
- **Qwen** (`providers/qwen/`) - Alibaba's Qwen models

## Design Principles

### 1. Separation of Concerns

Each component has a single responsibility:
- **Base**: Define the contract
- **Agent**: Manage conversation and tools
- **Providers**: Implement model-specific logic

### 2. Open/Closed Principle

The system is:
- **Open for extension**: Add new providers without modifying existing code
- **Closed for modification**: Core classes don't need changes

### 3. Dependency Inversion

The agent depends on the `ModelProvider` abstraction, not concrete implementations, allowing any provider to be used interchangeably.

## Adding a New Provider

### Minimal Steps

1. Create folder: `ai_agent/providers/my_model/`
2. Implement `MyModelProvider(ModelProvider)` in `provider.py`
3. Export in `__init__.py`
4. Register in `providers/__init__.py`

### Example Structure

```
ai_agent/providers/my_model/
├── __init__.py
│   from .provider import MyModelProvider
│   __all__ = ['MyModelProvider']
│
└── provider.py
    class MyModelProvider(ModelProvider):
        def generate(...): ...
        def supports_tools(): ...
```

See [providers/README.md](ai_agent/providers/README.md) for detailed guide.

## Data Flow

```
User Input
    ↓
AIAgent.run()
    ↓
ModelProvider.generate()
    ↓
Provider-specific API call
    ↓
Parse response to standard format
    ↓
Tool execution (if needed)
    ↓
Loop until final response
    ↓
Return to user
```

## Standard Response Format

All providers must return:

```python
{
    'content': str | None,
    'tool_calls': [
        {
            'name': str,
            'arguments': dict
        }
    ],
    'finish_reason': str
}
```

This standardization allows:
- Seamless model switching
- Provider-agnostic agent code
- Consistent tool handling

## Configuration

Environment-based configuration (`config.py`) provides:
- Automatic provider instantiation
- API key management
- Model selection

This keeps application code clean:

```python
from config import get_provider

provider = get_provider()  # Reads .env
agent = AIAgent(provider)  # Ready to use
```

## Benefits

### For Users
- Simple API regardless of provider
- Easy to switch models
- Add new providers without breaking existing code

### For Developers
- Clear structure for contributions
- Minimal code duplication
- Easy to test individual providers

### For Maintainability
- Changes isolated to specific providers
- Core agent logic stays stable
- Provider bugs don't affect others

## Future Extensions

The architecture supports:
- Multiple providers simultaneously
- Provider-specific optimizations
- Custom tool formats per provider
- Provider capabilities negotiation
- Streaming responses
- Async operations

All without changing the core architecture.
