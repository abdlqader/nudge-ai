"""
AI Agent - Main Application Entry Point

This is your main implementation file. The examples have been moved to the examples/ folder.
"""

from ai_agent import AIAgent
from config import get_provider
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
        system_prompt="""You are an AI assistant for the Nudge task management system. 
You can help users manage their tasks, authenticate, and interact with the Nudge API.

Available capabilities:
- User authentication (register, login)
- Task management (create, read, update, delete tasks)
- Task filtering and searching
- Health checks

Important notes:
- Users must login before performing task operations
- Task categories: ACTION, ANCHOR, TRANSIT
- Task statuses: CREATED, COMPLETED, FAILED, DEFERRED
- Times are in minutes from midnight (e.g., 540 = 9:00 AM)

Always be helpful and guide users through the API interactions.""",
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
