"""
Example: Adding a custom provider (OpenAI)

This demonstrates how to add a new model provider to the system.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from typing import Any, Dict, List, Optional
import json
from ai_agent.base import ModelProvider


class OpenAIProvider(ModelProvider):
    """
    Example: OpenAI model provider
    
    This shows how to implement a new provider.
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model_name: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
        """
        self.api_key = api_key
        self.model_name = model_name
        self._client = None
    
    def _init_client(self):
        """Lazy initialization of the OpenAI client"""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
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
        """Parse OpenAI response"""
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
        """OpenAI supports tool calling"""
        return True


# Example usage
if __name__ == "__main__":
    from ai_agent import AIAgent
    import os
    
    # Create provider
    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY", "your-key"),
        model_name="gpt-4"
    )
    
    # Create agent
    agent = AIAgent(
        model_provider=provider,
        system_prompt="You are a helpful assistant."
    )
    
    print("✓ OpenAI provider created successfully!")
    print(f"Model: {provider.model_name}")
    print("\nTo use this provider:")
    print("1. Install: pip install openai")
    print("2. Set OPENAI_API_KEY environment variable")
    print("3. Run: agent.run('Your message')")
