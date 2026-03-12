"""
Base classes for AI model providers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ModelProvider(ABC):
    """Abstract base class for AI model providers"""
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response from the model
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary containing:
                - content: Generated text response
                - tool_calls: List of tool calls (if any)
                - finish_reason: Reason for completion
        """
        pass
    
    @abstractmethod
    def supports_tools(self) -> bool:
        """
        Check if the model supports tool/function calling
        
        Returns:
            True if tools are supported, False otherwise
        """
        pass
