"""
Example: Using decorator syntax to define tools
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_agent import AIAgent
from config import get_provider
from tools import ToolRegistry


def main():
    # Create a new registry
    registry = ToolRegistry()
    
    # Define tools using decorator syntax
    @registry.tool(description="Search for information on the internet")
    def web_search(query: str, max_results: int = 5) -> dict:
        """Search the web for information"""
        # Simulated search results
        return {
            "query": query,
            "results": [
                {"title": f"Result {i+1}", "url": f"https://example.com/{i}"}
                for i in range(max_results)
            ]
        }
    
    @registry.tool(description="Get the current time")
    def get_current_time() -> dict:
        """Get the current time"""
        from datetime import datetime
        now = datetime.now()
        return {
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "timestamp": now.timestamp()
        }
    
    @registry.tool(description="Convert temperature between Celsius and Fahrenheit")
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
        """Convert temperature between units"""
        # Convert to Celsius first
        if from_unit.lower() == "fahrenheit":
            celsius = (value - 32) * 5/9
        else:
            celsius = value
        
        # Convert to target unit
        if to_unit.lower() == "fahrenheit":
            result = celsius * 9/5 + 32
        else:
            result = celsius
        
        return {
            "original": {"value": value, "unit": from_unit},
            "converted": {"value": round(result, 2), "unit": to_unit}
        }
    
    print("=" * 60)
    print("Tools Defined with Decorator Syntax")
    print("=" * 60)
    
    # Show registered tools
    print("\nRegistered Tools:")
    for tool in registry.get_all():
        print(f"  • {tool.name}: {tool.description}")
    
    # Test individual tool execution
    print("\n" + "=" * 60)
    print("Testing Tool Execution")
    print("=" * 60)
    
    time_tool = registry.get("get_current_time")
    if time_tool:
        result = time_tool.execute()
        print(f"\nget_current_time() result:")
        print(f"  {result}")
    
    temp_tool = registry.get("convert_temperature")
    if temp_tool:
        result = temp_tool.execute(value=100, from_unit="Celsius", to_unit="Fahrenheit")
        print(f"\nconvert_temperature(100, 'Celsius', 'Fahrenheit') result:")
        print(f"  {result}")
    
    # Create agent with these tools
    try:
        provider = get_provider()
        
        agent = AIAgent(
            model_provider=provider,
            system_prompt="You are a helpful assistant with various utility tools.",
            tools=registry.get_tool_definitions(),
            tool_functions=registry.get_tool_functions()
        )
        
        print("\n✓ Agent created with decorator-defined tools!")
        
    except ValueError as e:
        print(f"\n⚠️  Note: Configure .env to create agent with API")


if __name__ == "__main__":
    main()
