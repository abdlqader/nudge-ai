"""
Google Gemini model provider implementation
"""

from typing import Any, Dict, List, Optional
from ...base import ModelProvider


class GeminiProvider(ModelProvider):
    """Google Gemini model provider"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initialize Gemini provider
        
        Args:
            api_key: Google AI API key
            model_name: Model name (e.g., 'gemini-pro', 'gemini-1.5-pro')
        """
        self.api_key = api_key
        self.model_name = model_name
        self._client = None
    
    def _init_client(self):
        """Lazy initialization of the Gemini client"""
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model_name)
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Gemini"""
        client = self._init_client()
        
        # Convert messages to Gemini format
        prompt = self._format_messages(messages)
        
        # Configure generation
        generation_config = kwargs.get('generation_config', {})
        
        if tools:
            # Convert tools to Gemini function declarations
            gemini_tools = self._convert_tools(tools)
            response = client.generate_content(
                prompt,
                tools=gemini_tools,
                generation_config=generation_config
            )
        else:
            response = client.generate_content(
                prompt,
                generation_config=generation_config
            )
        
        return self._parse_response(response)
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for Gemini"""
        formatted = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                formatted.append(f"System: {content}")
            elif role == 'user':
                formatted.append(f"User: {content}")
            elif role == 'assistant':
                formatted.append(f"Assistant: {content}")
        return "\n\n".join(formatted)
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Any]:
        """Convert generic tool format to Gemini format"""
        from google.generativeai.types import FunctionDeclaration, Tool
        
        function_declarations = []
        for tool in tools:
            if tool.get('type') == 'function':
                func_info = tool.get('function', {})
                function_declarations.append(
                    FunctionDeclaration(
                        name=func_info.get('name'),
                        description=func_info.get('description'),
                        parameters=func_info.get('parameters', {})
                    )
                )
        
        return [Tool(function_declarations=function_declarations)] if function_declarations else []
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse Gemini response"""
        result = {
            'content': None,
            'tool_calls': [],
            'finish_reason': 'stop'
        }
        
        if hasattr(response, 'text'):
            result['content'] = response.text
        
        # Check for function calls
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call'):
                        fc = part.function_call
                        result['tool_calls'].append({
                            'name': fc.name,
                            'arguments': dict(fc.args)
                        })
        
        return result
    
    def supports_tools(self) -> bool:
        """Gemini supports tool calling"""
        return True
