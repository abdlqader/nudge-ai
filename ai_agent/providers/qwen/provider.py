"""
Qwen model provider implementation
Cloud-based access via Ollama Cloud API
"""

from typing import Any, Dict, List, Optional
import json
import os
from ...base import ModelProvider


class QwenProvider(ModelProvider):
    """Qwen model provider for Ollama Cloud API"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "qwen2.5:latest"):
        """
        Initialize Qwen provider
        
        Args:
            api_key: Ollama Cloud API key (required, reads from OLLAMA_API_KEY env var)
            model_name: Model name (e.g., 'qwen2.5:latest', 'qwen2.5:7b', etc.)
        """
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        if not self.api_key:
            raise ValueError("OLLAMA_API_KEY is required for cloud access. Please set it in your .env file.")
        
        self.model_name = model_name
        self._client = None
    
    def _init_client(self):
        """Initialize native Ollama client for Ollama Cloud API"""
        if self._client is None:
            from ollama import Client
            self._client = Client(
                host="https://ollama.com",
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            print(f"✓ Connected to Ollama Cloud API at https://ollama.com")
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Ollama Cloud API"""
        client = self._init_client()
        
        # Prepare API call parameters
        api_params = {
            'model': self.model_name,
            'messages': messages
        }
        
        if tools:
            api_params['tools'] = tools
        
        # Add any additional options
        if 'options' in kwargs:
            api_params['options'] = kwargs['options']
        
        # Call Ollama native API
        response = client.chat(**api_params)
        return self._parse_response(response)
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse Ollama Cloud API response"""
        result = {
            'content': None,
            'tool_calls': [],
            'finish_reason': 'stop'
        }
        
        # Ollama returns message directly
        message = response.get('message', {})
        
        if 'content' in message:
            result['content'] = message['content']
        
        # Parse tool calls if present
        if 'tool_calls' in message and message['tool_calls']:
            for tool_call in message['tool_calls']:
                result['tool_calls'].append({
                    'id': tool_call.get('id', f"call_{hash(str(tool_call))}"),
                    'name': tool_call['function']['name'],
                    'arguments': tool_call['function'].get('arguments', {})
                })
        
        result['finish_reason'] = response.get('done_reason', 'stop')
        return result
    
    def supports_tools(self) -> bool:
        """Qwen supports tool calling"""
        return True
