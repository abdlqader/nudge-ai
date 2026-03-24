"""
AI Agent - Main Application Entry Point

This is your main implementation file. The examples have been moved to the examples/ folder.
"""

from ai_agent import AIAgent
from config import get_provider, SYSTEM_PROMPT
from tools.nudge_api import nudge_registry


def main():
    """
    Main application logic goes here
    """
    # Initialize provider from .env configuration
    provider = get_provider()
    
    # Use Nudge API tools registry
    registry = nudge_registry
    
    # Create agent with Nudge API tools
    agent = AIAgent(
        model_provider=provider,
        system_prompt=SYSTEM_PROMPT,
        tools=registry.get_tool_definitions(),
        tool_functions=registry.get_tool_functions()
    )
    
    # TODO: Implement your application logic here
    print("AI Agent initialized successfully!")
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {provider.model_name}")
    print(f"Registered tools: {len(registry.get_all())}")
    
    # Example usage:
    result = agent.run("Check if the Nudge API is healthy, then login with email admin@mk.com and password Testing123")
    print(result['response'])


if __name__ == "__main__":
    main()
