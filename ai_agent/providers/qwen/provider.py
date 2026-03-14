"""
Alibaba Qwen model provider implementation
Optimized for Ollama deployment with native client support
"""

from typing import Any, Dict, List, Optional
import json
import os
from ...base import ModelProvider


class QwenProvider(ModelProvider):
    """Qwen model provider for local Ollama deployment"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "qwen-turbo", base_url: Optional[str] = None):
        """
        Initialize Qwen provider
        
        Args:
            api_key: Optional API key (not required for local Ollama)
            model_name: Model name (e.g., 'qwen3:8b', 'qwen-turbo', 'qwen-plus')
            base_url: Base URL for Qwen/Ollama (reads from QWEN_BASE_URL env var)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url or os.getenv("QWEN_BASE_URL")
        self._client = None
        self._use_ollama = os.getenv("USE_OLLAMA_CLIENT", "true").lower() == "true"
    
    def _init_client(self):
        """Lazy initialization - uses native Ollama client if available"""
        if self._client is None:
            if self._use_ollama:
                try:
                    from ollama import Client
                    # Native Ollama client - simpler and more direct
                    host = self.base_url.replace('/v1', '').rstrip('/')
                    self._client = Client(host=host)
                    print(f"✓ Using native Ollama client at {host}")
                    return self._client
                except ImportError:
                    print("Warning: ollama package not found, falling back to OpenAI client")
                    self._use_ollama = False
            
            # Fallback to OpenAI-compatible client
            from openai import OpenAI
            self._client = OpenAI(
                api_key=self.api_key or "dummy-key",
                base_url=self.base_url if self.base_url.endswith('/v1') else f"{self.base_url}/v1"
            )
            print(f"✓ Using OpenAI-compatible client at {self.base_url}")
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Qwen/Ollama"""
        client = self._init_client()
        
        if self._use_ollama:
            return self._generate_ollama(client, messages, tools, **kwargs)
        else:
            return self._generate_openai(client, messages, tools, **kwargs)
    
    def _generate_ollama(self, client, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]], **kwargs):
        """Generate using native Ollama client"""
        options = kwargs.get('options', {})
        
        # Convert tools to Ollama format if provided
        ollama_tools = None
        if tools:
            ollama_tools = tools  # Ollama uses same format as OpenAI
        
        response = client.chat(
            model=self.model_name,
            messages=messages,
            tools=ollama_tools,
            options=options
        )
        
        return self._parse_ollama_response(response)
    
    def _generate_openai(self, client, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]], **kwargs):
        """Generate using OpenAI-compatible client"""
        api_params = {
            'model': self.model_name,
            'messages': messages,
            **kwargs
        }
        
        if tools:
            api_params['tools'] = tools
            api_params['tool_choice'] = kwargs.get('tool_choice', 'auto')
        
        response = client.chat.completions.create(**api_params)
        return self._parse_openai_response(response)
    
    def _parse_ollama_response(self, response) -> Dict[str, Any]:
        """Parse native Ollama response"""
        result = {
            'content': None,
            'tool_calls': [],
            'finish_reason': 'stop'
        }
        
        message = response.get('message', {})
        result['content'] = message.get('content')
        
        # Parse tool calls if present
        if 'tool_calls' in message:
            for tool_call in message['tool_calls']:
                result['tool_calls'].append({
                    'id': tool_call.get('id', 'call_' + str(hash(str(tool_call)))),
                    'name': tool_call['function']['name'],
                    'arguments': tool_call['function']['arguments']
                })
        
        result['finish_reason'] = response.get('done_reason', 'stop')
        return result
    
    def _parse_openai_response(self, response) -> Dict[str, Any]:
        """Parse OpenAI-compatible response"""
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
