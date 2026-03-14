"""
AI Agent - Main Application Entry Point

This is your main implementation file. The examples have been moved to the examples/ folder.
"""

from ai_agent import AIAgent
from config import get_provider
from tools import ToolRegistry


def main():
    """
    Main application logic goes here
    """
    # Initialize provider from .env configuration
    provider = get_provider()
    
    # Create your tool registry
    registry = ToolRegistry()
    
    # TODO: Define your tools here
    # @registry.tool(description="Your tool description")
    # def your_tool(param: str) -> dict:
    #     return {"result": "..."}
    
    # Create agent
    agent = AIAgent(
        model_provider=provider,
        system_prompt="You are an astronaut AI assistant.",
        tools=registry.get_tool_definitions(),
        tool_functions=registry.get_tool_functions()
    )
    
    # TODO: Implement your application logic here
    print("AI Agent initialized successfully!")
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {provider.model_name}")
    print(f"Registered tools: {len(registry.get_all())}")
    
    # Example usage:
    result = agent.run("Hello, who you are?")
    print(result['response'])


if __name__ == "__main__":
    main()
