"""
AI Agent Module with Multi-Model Support

Supports switching between different AI models with tool/function calling capabilities.
"""

from .base import ModelProvider
from .agent import AIAgent
from .providers import GeminiProvider, QwenProvider

__version__ = "1.0.0"

__all__ = [
    'ModelProvider',
    'AIAgent',
    'GeminiProvider',
    'QwenProvider',
]
