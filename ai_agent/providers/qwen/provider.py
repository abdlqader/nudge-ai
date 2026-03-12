"""
Alibaba Qwen model provider implementation
"""

from typing import Any, Dict, List, Optional
import json
from ...base import ModelProvider


class QwenProvider(ModelProvider):
    """Alibaba Qwen model provider"""
    
    def __init__(self, api_key: str, model_name: str = "qwen-turbo"):
        """
        Initialize Qwen provider
        
        Args:
            api_key: Alibaba Cloud API key
            model_name: Model name (e.g., 'qwen-turbo', 'qwen-plus', 'qwen-max')
        """
        self.api_key = api_key
        self.model_name = model_name
        self._client = None
    
    def _init_client(self):
        """Lazy initialization of the Qwen client"""
        if self._client is None:
            from openai import OpenAI
            # Qwen uses OpenAI-compatible API
            self._client = OpenAI(
                api_key=self.api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Qwen"""
        client = self._init_client()
        
        # Prepare API call parameters
        api_params = {
            'model': self.model_name,
            'messages': messages,
            **kwargs
        }
        
        if tools:
            api_params['tools'] = tools
            api_params['tool_choice'] = kwargs.get('tool_choice', 'auto')
        
        response = client.chat.completions.create(**api_params)
        
        return self._parse_response(response)
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse Qwen response"""
        result = {
            'content': None,
            'tool_calls': [],
            'finish_reason': 'stop'
        }
        
        if response.choices:
            choice = response.choices[0]
            message = choice.message
            
            if message.content:
                result['content'] = message.content
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    result['tool_calls'].append({
                        'id': tool_call.id,
                        'name': tool_call.function.name,
                        'arguments': json.loads(tool_call.function.arguments)
                    })
            
            result['finish_reason'] = choice.finish_reason
        
        return result
    
    def supports_tools(self) -> bool:
        """Qwen supports tool calling"""
        return True
