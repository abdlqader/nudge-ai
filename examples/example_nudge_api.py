"""
Example: Using AI Agent with Nudge API Tools

This example demonstrates how to interact with the Nudge task management API
through natural language using the AI agent.
"""

from ai_agent import AIAgent
from config import get_provider
from tools.nudge_api import nudge_registry


def main():
    # Initialize provider
    provider = get_provider()
    
    # Create agent with Nudge API tools
    agent = AIAgent(
        model_provider=provider,
        system_prompt="""You are an AI assistant for the Nudge task management system. 
You can help users manage their tasks, authenticate, and interact with the Nudge API.

Important notes:
- Users must login before performing task operations
- Task categories: ACTION, ANCHOR, TRANSIT
- Task statuses: CREATED, COMPLETED, FAILED, DEFERRED
- Times are in minutes from midnight (e.g., 540 = 9:00 AM)""",
        tools=nudge_registry.get_tool_definitions(),
        tool_functions=nudge_registry.get_tool_functions()
    )
    
    print("=== Nudge API AI Assistant ===\n")
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {provider.model_name}")
    print(f"Registered tools: {len(nudge_registry.get_all())}\n")
    
    # Example 1: Check API health
    print("Example 1: Checking API health")
    print("-" * 50)
    result = agent.run("Check if the Nudge API is healthy")
    print(f"Response: {result['response']}\n")
    
    # Example 2: Login
    print("Example 2: Login to the system")
    print("-" * 50)
    result = agent.run("Login with email admin@mk.com and password Testing123")
    print(f"Response: {result['response']}\n")
    
    # Example 3: Create a task
    print("Example 3: Creating a task")
    print("-" * 50)
    result = agent.run(
        "Create a task called 'Complete project documentation' "
        "in the ACTION category for the Work category, "
        "with expected duration of 120 minutes, starting at 9:00 AM"
    )
    print(f"Response: {result['response']}\n")
    
    # Example 4: Get all tasks
    print("Example 4: Listing all tasks")
    print("-" * 50)
    result = agent.run("Show me all my tasks")
    print(f"Response: {result['response']}\n")
    
    # Example 5: Search tasks
    print("Example 5: Searching for tasks")
    print("-" * 50)
    result = agent.run("Find all tasks with status CREATED in the Work category")
    print(f"Response: {result['response']}\n")
    
    # Interactive mode (optional)
    print("\n=== Interactive Mode ===")
    print("You can now chat with the assistant. Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = agent.run(user_input)
        print(f"Assistant: {result['response']}\n")


if __name__ == "__main__":
    main()
