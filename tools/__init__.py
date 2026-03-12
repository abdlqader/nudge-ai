"""
Tools package for AI Agent

Provides a structured system for defining, registering, and managing tools.
"""

from .registry import Tool, ToolRegistry, register_tool, tool, default_registry
from .examples import create_example_tools, get_weather, calculator

__all__ = [
    'Tool',
    'ToolRegistry',
    'register_tool',
    'tool',
    'default_registry',
    'create_example_tools',
    'get_weather',
    'calculator',
]
