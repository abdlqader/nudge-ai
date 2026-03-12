"""
Example usage of the AI Agent module with structured tools
"""

import sys
from pathlib import Path
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_agent import AIAgent, GeminiProvider, QwenProvider
from dotenv import load_dotenv
from tools import create_example_tools

# Load environment variables
load_dotenv()


def main():
    # Load configuration from environment
    model_provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    model_name = os.getenv("MODEL_NAME", "gemini-pro")
    api_key = os.getenv("API_KEY")
    
    # Create tools using the structured registry system
    tool_registry = create_example_tools()
    
    # Get tools in OpenAI format and as callable functions
    tools = tool_registry.get_tool_definitions()
    tool_functions = tool_registry.get_tool_functions()
    
    print(f"\nRegistered {len(tools)} tools:")
    for tool_def in tools:
        print(f"  • {tool_def['function']['name']}")
    
    # Initialize provider based on environment configuration
    print("=" * 50)
    print(f"Initializing AI Agent with {model_provider.upper()}")
    print("=" * 50)
    
    if not api_key:
        print("ERROR: API_KEY not found in environment variables.")
        print("Please copy .env.example to .env and add your API key.")
        return
    
    # Create the appropriate provider
    if model_provider == "gemini":
        provider = GeminiProvider(api_key=api_key, model_name=model_name)
        print(f"Using Gemini model: {model_name}")
    elif model_provider == "qwen":
        provider = QwenProvider(api_key=api_key, model_name=model_name)
        print(f"Using Qwen model: {model_name}")
    else:
        print(f"ERROR: Unknown provider '{model_provider}'. Use 'gemini' or 'qwen'.")
        return
    
    # Create agent
    agent = AIAgent(
        model_provider=provider,
        system_prompt="You are a helpful assistant with access to tools.",
        tools=tools,
        tool_functions=tool_functions
    )
    
    print("\nAgent initialized successfully!")
    print("\nTo test the agent, uncomment the example queries below:")
    
    # Example query 1
    # print("\n" + "-" * 50)
    # result = agent.run("What's the weather in New York?")
    # print(f"Response: {result['response']}")
    # print(f"Iterations: {result['iterations']}")
    
    # Example query 2
    # print("\n" + "-" * 50)
    # result = agent.run("Calculate 15 multiplied by 7")
    # print(f"Response: {result['response']}")
    # print(f"Iterations: {result['iterations']}")
    
    # Example: Switching to a different provider
    print("\n" + "=" * 50)
    print("Example: Switching Providers")
    print("=" * 50)
    
    # To switch providers, uncomment below:
    # other_provider = "qwen" if model_provider == "gemini" else "gemini"
    # other_api_key = os.getenv(f"{other_provider.upper()}_API_KEY")
    # if other_api_key:
    #     if other_provider == "gemini":
    #         new_provider = GeminiProvider(api_key=other_api_key)
    #     else:
    #         new_provider = QwenProvider(api_key=other_api_key)
    #     agent.switch_model(new_provider)
    #     print(f"Switched to {other_provider}")
    
    print("Check the code to see how to switch providers.")
    
    # Example: Custom Agent Configuration
    print("\n" + "=" * 50)
    print("Example: Custom Agent Configuration")
    print("=" * 50)
    
    custom_agent = AIAgent(
        model_provider=provider,
        system_prompt="You are a math tutor. Help students solve problems step by step."
    )
    
    # Later, add tools
    custom_agent.add_tools(tools, tool_functions)
    
    print("Custom agent configured successfully")
    
    # Example: Updating system prompt
    print("\n" + "=" * 50)
    print("Example: Updating System Prompt")
    print("=" * 50)
    
    agent.update_system_prompt(
        "You are a weather expert. Provide detailed weather analysis."
    )
    
    print("System prompt updated")


if __name__ == "__main__":
    main()
