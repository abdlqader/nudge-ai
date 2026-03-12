"""
Example: Using the structured tools system
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_agent import AIAgent
from config import get_provider
from tools import create_example_tools


def main():
    try:
        # Get provider from .env configuration
        provider = get_provider()
        
        print("=" * 60)
        print("AI Agent with Structured Tools")
        print("=" * 60)
        print(f"Provider: {provider.__class__.__name__}")
        print(f"Model: {provider.model_name}")
        
        # Create example tools using the registry system
        tool_registry = create_example_tools()
        
        # Display registered tools
        print(f"\nRegistered Tools:")
        for tool in tool_registry.get_all():
            print(f"  • {tool.name}: {tool.description}")
        
        # Create agent with tools from registry
        agent = AIAgent(
            model_provider=provider,
            system_prompt="You are a helpful assistant with access to tools.",
            tools=tool_registry.get_tool_definitions(),
            tool_functions=tool_registry.get_tool_functions()
        )
        
        print("\n✓ Agent initialized successfully with structured tools!")
        
        # Example usage (uncomment to test with real API)
        # print("\n" + "=" * 60)
        # print("Example Query")
        # print("=" * 60)
        # result = agent.run("What's the weather like in Tokyo?")
        # print(f"\nResponse: {result['response']}")
        # print(f"Iterations: {result['iterations']}")
        
        print("\nUncomment the example code above to test with your API.")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nMake sure you have configured your .env file.")


if __name__ == "__main__":
    main()
