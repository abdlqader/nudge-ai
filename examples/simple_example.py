"""
Simple example using environment configuration
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_agent import AIAgent
from config import get_provider


def main():
    try:
        # Get provider from .env configuration
        provider = get_provider()
        
        print("AI Agent initialized successfully!")
        print(f"Provider: {provider.__class__.__name__}")
        print(f"Model: {provider.model_name}")
        
        # Create agent with a simple system prompt
        agent = AIAgent(
            model_provider=provider,
            system_prompt="You are a helpful AI assistant."
        )
        
        # Example conversation (uncomment to test with real API)
        # result = agent.run("Hello! Can you introduce yourself?")
        # print(f"\nResponse: {result['response']}")
        
        print("\n✓ Agent ready to use!")
        print("Uncomment the example code above to test with your API.")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Copied .env.example to .env")
        print("2. Set your API_KEY in the .env file")
        print("3. Optionally set MODEL_PROVIDER and MODEL_NAME")


if __name__ == "__main__":
    main()
