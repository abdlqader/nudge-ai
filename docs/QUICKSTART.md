# Quick Start Guide

This project uses a modular architecture where each AI model provider is in its own folder, making it easy to add new models.

## Step 1: Install Dependencies

```bash
pipenv install
```

## Step 2: Configure Your API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or: vim .env, code .env, etc.
```

Set these values in `.env`:
```bash
MODEL_PROVIDER=gemini              # Choose: gemini or qwen
MODEL_NAME=gemini-pro              # Or: gemini-1.5-pro, qwen-turbo, qwen-plus, etc.
API_KEY=your-actual-api-key-here   # Your API key from Google AI or Alibaba Cloud
```

## Step 3: Test Your Setup

```bash
pipenv run python examples/simple_example.py
```

You should see:
```
AI Agent initialized successfully!
Provider: GeminiProvider
Model: gemini-pro
✓ Agent ready to use!
```

## Step 4: Start Building

Your main implementation goes in `main.py`:

```bash
pipenv run python main.py
```

The file includes a basic structure - add your tools and logic there.

## Step 5: Learn from Examples

Check the `examples/` folder for demonstrations

### Option A: Simple Usage

```python
from ai_agent import AIAgent
from config import get_provider

# Load from .env automatically
provider = get_provider()

# Create agent
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant."
)

# Chat
result = agent.run("What is Python?")
print(result['response'])
```

### Option B: With Tools

```python
from ai_agent import AIAgent
from config import get_provider

# Define a tool
def get_weather(location: str):
    return {"location": location, "temp": 72, "condition": "sunny"}

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
}]

tool_functions = {"get_weather": get_weather}

# Create agent with tools
provider = get_provider()
agent = AIAgent(
    model_provider=provider,
    system_prompt="You are a helpful assistant with access to tools.",
    tools=tools,
    tool_functions=tool_functions
)

# The agent can now use the tool
result = agent.run("What's the weather in Tokyo?")
print(result['response'])
```

## Step 5: Switch Models

To switch between Gemini and Qwen:

1. Edit `.env` and change `MODEL_PROVIDER`:
   ```bash
   MODEL_PROVIDER=qwen
   MODEL_NAME=qwen-turbo
   API_KEY=your-qwen-api-key
   ```

2. Or switch programmatically:
   ```python
   from ai_agent import QwenProvider
   
   new_provider = QwenProvider(
       api_key="your-qwen-key",
       model_name="qwen-turbo"
   )
   agent.switch_model(new_provider)
   ```

## Getting API Keys

### Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Create an API key
3. Copy it to your `.env` file

### Alibaba Qwen
1. Go to https://dashscope.console.aliyun.com/
2. Get your API key from the dashboard
3. Copy it to your `.env` file

## Common Issues

### "No API key found"
- Make sure you created `.env` (not just `.env.example`)
- Check that `API_KEY` is set in `.env`
- No spaces around the `=` sign

### "Module not found"
- Run `pipenv install` first
- Make sure you're using `pipenv run python` or activated the virtualenv with `pipenv shell`

### "Invalid API key"
- Double-check your API key in `.env`
- Make sure there are no extra spaces or quotes
- Verify the key works with the correct provider

## Next Steps

- Check out [example_usage.py](example_usage.py) for more advanced examples
- Read the full [README.md](README.md) for API documentation
- Create custom tools for your specific use case
