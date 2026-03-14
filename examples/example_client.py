"""
Example Client for FastAPI AI Agent

Demonstrates how to interact with the AI agent via REST API endpoints.
"""

import requests
import json


class NudgeAIClient:
    """Client for interacting with the Nudge AI Agent API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", nudge_api_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.nudge_api_url = nudge_api_url
        self.session = requests.Session()
        self.token = None
    
    def health_check(self):
        """Check if the API is running"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    def login(self, email: str, password: str):
        """Login to Nudge API and store the token"""
        response = requests.post(
            f"{self.nudge_api_url}/auth/login",
            json={"email": email, "password": password}
        )
        result = response.json()
        if "token" in result:
            self.token = result["token"]
        return result
    
    def send_message(self, message: str):
        """Send a message to the AI agent with authentication"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        response = self.session.post(
            f"{self.base_url}/agent/message",
            json={"message": message},
            headers=headers
        )
        return response.json()
    
    def get_status(self):
        """Get agent status and authentication state"""
        response = self.session.get(f"{self.base_url}/agent/status")
        return response.json()
    
    def reset_conversation(self):
        """Reset the conversation history"""
        response = self.session.post(f"{self.base_url}/agent/reset")
        return response.json()


def main():
    """Example usage of the Nudge AI Client"""
    
    print("=== Nudge AI Agent Client Example ===\n")
    
    # Initialize client
    client = NudgeAIClient(
        base_url="http://localhost:8000",
        nudge_api_url="http://localhost:8080"
    )
    
    # 1. Health check
    print("1. Checking API health...")
    health = client.health_check()
    print(f"   Status: {health['status']}\n")
    
    # 2. Login to Nudge API directly
    print("2. Logging in to Nudge API...")
    login_result = client.login("admin@mk.com", "Testing123")
    if "token" in login_result:
        print(f"   ✓ Logged in as: {login_result['user']['email']}")
        print(f"   Token stored for AI agent requests\n")
    else:
        print(f"   ✗ Login failed: {login_result}\n")
        return
    
    # 3. Check agent status
    print("3. Checking agent status...")
    status = client.get_status()
    print(f"   Provider: {status['agent']['provider']}")
    print(f"   Model: {status['agent']['model']}")
    print(f"   Tools: {status['agent']['tools_count']}")
    print(f"   Authenticated: {status['authentication']['authenticated']}\n")
    
    # 4. Send messages to AI agent
    print("4. Interacting with AI agent...\n")
    
    messages = [
        "Check if the Nudge API is healthy",
        "Create a task called 'Complete project documentation' in ACTION category for Work, duration 120 minutes, starting at 9 AM",
        "Show me all my tasks",
        "Find all CREATED tasks"
    ]
    
    for msg in messages:
        print(f"   You: {msg}")
        result = client.send_message(msg)
        response = result.get("response", "")
        print(f"   AI: {response[:200]}...")
        
        if result.get("tool_calls"):
            print(f"   Tools called: {[tc['name'] for tc in result['tool_calls']]}")
        print()
    
    # 5. Interactive mode
    print("\n5. Interactive mode (type 'quit' to exit)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            result = client.send_message(user_input)
            print(f"AI: {result.get('response', 'No response')}\n")
        eCleanup (optional)
    print("\n6. Session complete")
    print(f"   Token used for all AI agent requests")


if __name__ == "__main__":
    print("\nMake sure:")
    print("  1. Nudge API is running: http://localhost:8080")
    print("  2. FastAPI server is running:
if __name__ == "__main__":
    print("\nMake sure the FastAPI server is running:")
    print("  pipenv run python api.py\n")
    
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the API server.")
        print("  Please start the server with: pipenv run python api.py")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
