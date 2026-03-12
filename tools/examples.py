"""
Example tools for demonstration purposes
"""

from .registry import ToolRegistry


def create_example_tools() -> ToolRegistry:
    """
    Create a registry with example tools
    
    Returns:
        ToolRegistry with weather and calculator tools
    """
    registry = ToolRegistry()
    
    # Weather tool
    registry.register(
        name="get_weather",
        description="Get the current weather for a location",
        function=get_weather,
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    )
    
    # Calculator tool
    registry.register(
        name="calculator",
        description="Perform basic mathematical operations",
        function=calculator,
        parameters={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The mathematical operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    )
    
    return registry


def get_weather(location: str) -> dict:
    """
    Get weather information for a location
    
    Args:
        location: City name or location
        
    Returns:
        Dictionary with weather information
    """
    # Simulated weather data
    return {
        "location": location,
        "temperature": 22,
        "condition": "sunny",
        "humidity": 45,
        "wind_speed": 10
    }


def calculator(operation: str, a: float, b: float) -> dict:
    """
    Perform basic mathematical operations
    
    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number
        
    Returns:
        Dictionary with operation result
    """
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    
    result = operations.get(operation, "Invalid operation")
    
    return {
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }
