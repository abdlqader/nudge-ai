"""
Model providers package

To add a new provider:
1. Create a new folder: providers/your_provider/
2. Create __init__.py and provider.py in that folder
3. Implement YourProvider class inheriting from ModelProvider
4. Import it here
"""

from .gemini import GeminiProvider
from .qwen import QwenProvider

__all__ = ['GeminiProvider', 'QwenProvider']
