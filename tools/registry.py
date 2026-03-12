"""
Tool system for AI Agent

Provides a structured way to define and register tools/functions
that the AI agent can use.
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
import inspect


@dataclass
class Tool:
    """
    Structured tool definition
    
    Attributes:
        name: Tool function name
        description: What the tool does
        function: The actual Python function to call
        parameters: JSON schema for parameters
    """
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool function with given arguments"""
        return self.function(**kwargs)


class ToolRegistry:
    """
    Registry for managing tools
    
    Provides a centralized way to register, retrieve, and manage tools.
    """
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Tool:
        """
        Register a new tool
        
        Args:
            name: Tool name
            description: Tool description
            function: Python function to call
            parameters: JSON schema for parameters (auto-generated if None)
            
        Returns:
            The registered Tool object
        """
        if parameters is None:
            parameters = self._generate_parameters(function)
        
        tool = Tool(
            name=name,
            description=description,
            function=function,
            parameters=parameters
        )
        
        self._tools[name] = tool
        return tool
    
    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Decorator for registering tools
        
        Usage:
            @registry.tool(description="Get weather info")
            def get_weather(location: str) -> dict:
                return {...}
        """
        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            tool_desc = description or func.__doc__ or f"Execute {tool_name}"
            
            self.register(
                name=tool_name,
                description=tool_desc,
                function=func,
                parameters=parameters
            )
            
            return func
        
        return decorator
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def get_all(self) -> List[Tool]:
        """Get all registered tools"""
        return list(self._tools.values())
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all tools in OpenAI format"""
        return [tool.to_openai_format() for tool in self._tools.values()]
    
    def get_tool_functions(self) -> Dict[str, Callable]:
        """Get dictionary mapping tool names to functions"""
        return {name: tool.function for name, tool in self._tools.items()}
    
    def remove(self, name: str) -> bool:
        """Remove a tool by name"""
        if name in self._tools:
            del self._tools[name]
            return True
        return False
    
    def clear(self):
        """Clear all registered tools"""
        self._tools.clear()
    
    def _generate_parameters(self, func: Callable) -> Dict[str, Any]:
        """
        Auto-generate parameter schema from function signature
        
        Note: This is a basic implementation. For production use,
        consider using libraries like pydantic or inspect more thoroughly.
        """
        sig = inspect.signature(func)
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self' or param_name == 'cls':
                continue
            
            # Basic type inference
            param_type = "string"  # default
            if param.annotation != inspect.Parameter.empty:
                annotation = param.annotation
                if annotation == int:
                    param_type = "integer"
                elif annotation == float:
                    param_type = "number"
                elif annotation == bool:
                    param_type = "boolean"
                elif annotation == list:
                    param_type = "array"
                elif annotation == dict:
                    param_type = "object"
            
            properties[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }
            
            # If no default value, it's required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }


# Global default registry
default_registry = ToolRegistry()


def register_tool(
    name: str,
    description: str,
    function: Callable,
    parameters: Optional[Dict[str, Any]] = None
) -> Tool:
    """Register a tool in the default registry"""
    return default_registry.register(name, description, function, parameters)


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None
):
    """Decorator for registering tools in the default registry"""
    return default_registry.tool(name, description, parameters)
