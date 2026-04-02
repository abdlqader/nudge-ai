"""
AI Agent with multi-model support and tool calling capabilities
"""

from typing import Any, Dict, List, Optional, Callable
import json
from .base import ModelProvider


class AIAgent:
    """
    AI Agent with multi-model support and tool calling capabilities
    """
    
    def __init__(
        self,
        model_provider: ModelProvider,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_functions: Optional[Dict[str, Callable]] = None
    ):
        """
        Initialize AI Agent
        
        Args:
            model_provider: Model provider instance (GeminiProvider, QwenProvider, etc.)
            system_prompt: System prompt for the agent
            tools: List of tool definitions (OpenAI function format)
            tool_functions: Dictionary mapping tool names to actual functions
        """
        self.model_provider = model_provider
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.tool_functions = tool_functions or {}
        self.conversation_history: List[Dict[str, str]] = []
        
        # Add system prompt to history
        if system_prompt:
            self.conversation_history.append({
                'role': 'system',
                'content': system_prompt
            })
    
    def switch_model(self, new_provider: ModelProvider):
        """
        Switch to a different model provider
        
        Args:
            new_provider: New model provider instance
        """
        self.model_provider = new_provider
    
    def update_system_prompt(self, system_prompt: str):
        """
        Update the system prompt
        
        Args:
            system_prompt: New system prompt
        """
        self.system_prompt = system_prompt
        
        # Update in conversation history
        if self.conversation_history and self.conversation_history[0]['role'] == 'system':
            self.conversation_history[0]['content'] = system_prompt
        else:
            self.conversation_history.insert(0, {
                'role': 'system',
                'content': system_prompt
            })
    
    def add_tools(self, tools: List[Dict[str, Any]], tool_functions: Dict[str, Callable]):
        """
        Add or update tools
        
        Args:
            tools: List of tool definitions
            tool_functions: Dictionary mapping tool names to functions
        """
        self.tools = tools
        self.tool_functions.update(tool_functions)
    
    def run(
        self,
        message: str,
        max_iterations: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the agent with a user message
        
        Args:
            message: User input message
            max_iterations: Maximum number of tool calling iterations
            **kwargs: Additional parameters for the model
            
        Returns:
            Dictionary with final response and metadata
        """
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        iterations = 0
        while iterations < max_iterations:
            # Generate response
            response = self.model_provider.generate(
                messages=self.conversation_history,
                tools=self.tools if self.tools else None,
                **kwargs
            )
            
            # If no tool calls, return the response
            if not response['tool_calls']:
                if response['content']:
                    self.conversation_history.append({
                        'role': 'assistant',
                        'content': response['content']
                    })
                return {
                    'response': response['content'],
                    'iterations': iterations + 1,
                    'tool_calls': []
                }
            
            # Execute tool calls
            tool_results = []
            for tool_call in response['tool_calls']:
                tool_name = tool_call['name']
                tool_args = tool_call.get('arguments', {})
                
                if tool_name in self.tool_functions:
                    try:
                        result = self.tool_functions[tool_name](**tool_args)
                        tool_results.append({
                            'tool': tool_name,
                            'result': result,
                            'success': True
                        })
                        
                        # Add tool result to conversation
                        self.conversation_history.append({
                            'role': 'assistant',
                            'content': f"Called {tool_name} with {tool_args}"
                        })
                        self.conversation_history.append({
                            'role': 'user',
                            'content': f"Tool result: {json.dumps(result)}"
                        })
                    except Exception as e:
                        tool_results.append({
                            'tool': tool_name,
                            'error': str(e),
                            'success': False
                        })
                        
                        self.conversation_history.append({
                            'role': 'user',
                            'content': f"Tool {tool_name} error: {str(e)}"
                        })
            
            iterations += 1
        
        # Max iterations reached
        return {
            'response': "Max iterations reached without final answer",
            'iterations': iterations,
            'tool_calls': tool_results
        }
    
    def reset_conversation(self):
        """Reset conversation history, keeping system prompt"""
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({
                'role': 'system',
                'content': self.system_prompt
            })
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.conversation_history.copy()

    def run_stateless(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_iterations: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the agent without touching internal conversation state.

        Accepts an external conversation history and returns the updated history
        alongside the response, making this safe for multi-user / concurrent use.

        Args:
            message: User input message
            conversation_history: Prior turns (role/content dicts, no system messages).
                                  Pass the value returned by a previous call to maintain context.
            max_iterations: Maximum tool-calling iterations before giving up
            **kwargs: Extra parameters forwarded to the model provider

        Returns:
            Dict with keys: response, iterations, tool_calls, conversation_history
        """
        # Build working history: prepend system prompt, exclude system from client history
        history: List[Dict[str, str]] = []
        if self.system_prompt:
            history.append({'role': 'system', 'content': self.system_prompt})
        if conversation_history:
            for msg in conversation_history:
                if msg.get('role') != 'system':
                    history.append(msg)
        history.append({'role': 'user', 'content': message})

        iterations = 0
        tool_calls_made = []

        while iterations < max_iterations:
            response = self.model_provider.generate(
                messages=history,
                tools=self.tools if self.tools else None,
                **kwargs
            )

            if not response['tool_calls']:
                if response['content']:
                    history.append({'role': 'assistant', 'content': response['content']})
                client_history = [m for m in history if m['role'] != 'system']
                return {
                    'response': response['content'],
                    'iterations': iterations + 1,
                    'tool_calls': tool_calls_made,
                    'conversation_history': client_history,
                }

            for tool_call in response['tool_calls']:
                tool_name = tool_call['name']
                tool_args = tool_call.get('arguments', {})
                if tool_name in self.tool_functions:
                    try:
                        result = self.tool_functions[tool_name](**tool_args)
                        tool_calls_made.append({'tool': tool_name, 'result': result, 'success': True})
                        history.append({'role': 'assistant', 'content': f"Called {tool_name} with {tool_args}"})
                        history.append({'role': 'user', 'content': f"Tool result: {json.dumps(result)}"})
                    except Exception as e:
                        tool_calls_made.append({'tool': tool_name, 'error': str(e), 'success': False})
                        history.append({'role': 'user', 'content': f"Tool {tool_name} error: {str(e)}"})
                else:
                    tool_calls_made.append({'tool': tool_name, 'error': 'Tool not found', 'success': False})

            iterations += 1

        client_history = [m for m in history if m['role'] != 'system']
        return {
            'response': "Max iterations reached without final answer",
            'iterations': iterations,
            'tool_calls': tool_calls_made,
            'conversation_history': client_history,
        }

    def run_stream(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_iterations: int = 5,
        **kwargs
    ):
        """
        Synchronous generator that yields SSE event dicts as the agent works.

        Does NOT modify internal conversation state (safe for concurrent use).

        Yields dicts with a 'type' field:
            tool_start  — {type, tool, args}
            tool_end    — {type, tool, success, result?, error?}
            message     — {type, content}  (final text response)
            done        — {type, tool_calls, conversation_history}
            error       — {type, message}
        """
        history: List[Dict[str, str]] = []
        if self.system_prompt:
            history.append({'role': 'system', 'content': self.system_prompt})
        if conversation_history:
            for msg in conversation_history:
                if msg.get('role') != 'system':
                    history.append(msg)
        history.append({'role': 'user', 'content': message})

        iterations = 0
        tool_calls_made = []

        try:
            while iterations < max_iterations:
                response = self.model_provider.generate(
                    messages=history,
                    tools=self.tools if self.tools else None,
                    **kwargs
                )

                if not response['tool_calls']:
                    if response['content']:
                        history.append({'role': 'assistant', 'content': response['content']})
                        yield {'type': 'message', 'content': response['content']}
                    client_history = [m for m in history if m['role'] != 'system']
                    yield {
                        'type': 'done',
                        'tool_calls': tool_calls_made,
                        'conversation_history': client_history,
                    }
                    return

                for tool_call in response['tool_calls']:
                    tool_name = tool_call['name']
                    tool_args = tool_call.get('arguments', {})
                    yield {'type': 'tool_start', 'tool': tool_name, 'args': tool_args}

                    if tool_name in self.tool_functions:
                        try:
                            result = self.tool_functions[tool_name](**tool_args)
                            tool_calls_made.append({'tool': tool_name, 'result': result, 'success': True})
                            yield {'type': 'tool_end', 'tool': tool_name, 'success': True, 'result': result}
                            history.append({'role': 'assistant', 'content': f"Called {tool_name} with {tool_args}"})
                            history.append({'role': 'user', 'content': f"Tool result: {json.dumps(result)}"})
                        except Exception as e:
                            tool_calls_made.append({'tool': tool_name, 'error': str(e), 'success': False})
                            yield {'type': 'tool_end', 'tool': tool_name, 'success': False, 'error': str(e)}
                            history.append({'role': 'user', 'content': f"Tool {tool_name} error: {str(e)}"})
                    else:
                        yield {'type': 'tool_end', 'tool': tool_name, 'success': False, 'error': f"Tool '{tool_name}' not found"}

                iterations += 1

            # Max iterations reached
            client_history = [m for m in history if m['role'] != 'system']
            yield {
                'type': 'done',
                'tool_calls': tool_calls_made,
                'conversation_history': client_history,
            }
        except Exception as e:
            yield {'type': 'error', 'message': str(e)}
