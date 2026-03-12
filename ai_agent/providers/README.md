# Adding New Model Providers

This guide explains how to add support for new AI model providers.

## Structure

Each provider should be in its own folder:

```
ai_agent/providers/
├── __init__.py
├── gemini/
│   ├── __init__.py
│   └── provider.py
├── qwen/
│   ├── __init__.py
│   └── provider.py
└── your_provider/
    ├── __init__.py
    └── provider.py
```

## Steps to Add a New Provider

### 1. Create Provider Folder

```bash
mkdir -p ai_agent/providers/your_provider
```

### 2. Create `__init__.py`

```python
# ai_agent/providers/your_provider/__init__.py
"""
Your Provider description
"""

from .provider import YourProvider

__all__ = ['YourProvider']
```

### 3. Create `provider.py`

Implement your provider by inheriting from `ModelProvider`:

```python
# ai_agent/providers/your_provider/provider.py
"""
Your Provider implementation
"""

from typing import Any, Dict, List, Optional
from ...base import ModelProvider


class YourProvider(ModelProvider):
    """Your model provider"""
    
    def __init__(self, api_key: str, model_name: str = "default-model"):
        """
        Initialize Your Provider
        
        Args:
            api_key: Your API key
            model_name: Model name
        """
        self.api_key = api_key
        self.model_name = model_name
        self._client = None
    
    def _init_client(self):
        """Lazy initialization of the client"""
        if self._client is None:
            # Initialize your client here
            # import your_sdk
            # self._client = your_sdk.Client(api_key=self.api_key)
            pass
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using Your Provider
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
            **kwargs: Additional parameters
            
        Returns:
            Dict with 'content', 'tool_calls', and 'finish_reason'
        """
        client = self._init_client()
        
        # Call your API
        # response = client.generate(messages=messages, tools=tools, **kwargs)
        
        # Parse and return in standard format
        return {
            'content': "Generated text",
            'tool_calls': [],  # List of dicts with 'name' and 'arguments'
            'finish_reason': 'stop'
        }
    
    def supports_tools(self) -> bool:
        """Whether this provider supports tool calling"""
        return True  # or False
```

### 4. Register the Provider

Add your provider to `ai_agent/providers/__init__.py`:

```python
from .gemini import GeminiProvider
from .qwen import QwenProvider
from .your_provider import YourProvider  # Add this

__all__ = ['GeminiProvider', 'QwenProvider', 'YourProvider']  # Add here
```

### 5. Update Main Package

Add import to `ai_agent/__init__.py`:

```python
from .providers import GeminiProvider, QwenProvider, YourProvider

__all__ = [
    'ModelProvider',
    'AIAgent',
    'GeminiProvider',
    'QwenProvider',
    'YourProvider',  # Add here
]
```

### 6. Update Configuration Helper

Add support in `config.py`:

```python
def get_provider():
    model_provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    # ... existing code ...
    
    # Add your provider
    if model_provider == "gemini":
        return GeminiProvider(api_key=api_key, model_name=model_name)
    elif model_provider == "qwen":
        return QwenProvider(api_key=api_key, model_name=model_name)
    elif model_provider == "your_provider":
        from ai_agent import YourProvider
        return YourProvider(api_key=api_key, model_name=model_name)
    # ... rest of code ...
```

## Response Format

All providers must return responses in this format:

```python
{
    'content': str or None,           # Generated text
    'tool_calls': [                   # List of tool calls (empty if none)
        {
            'name': str,              # Tool/function name
            'arguments': dict,        # Tool arguments
            'id': str (optional)      # Tool call ID
        }
    ],
    'finish_reason': str              # 'stop', 'tool_calls', etc.
}
```

## Tool Format

Tools use OpenAI function calling format:

```python
{
    "type": "function",
    "function": {
        "name": "function_name",
        "description": "What the function does",
        "parameters": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param_name"]
        }
    }
}
```

## Testing Your Provider

```python
from ai_agent import AIAgent, YourProvider

provider = YourProvider(api_key="your-key", model_name="model-name")

agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant."
)

result = agent.run("Hello!")
print(result['response'])
```

## Examples

Check the existing implementations:
- **Gemini**: `ai_agent/providers/gemini/provider.py`
- **Qwen**: `ai_agent/providers/qwen/provider.py`

Both demonstrate:
- Lazy client initialization
- Message formatting
- Tool conversion
- Response parsing
