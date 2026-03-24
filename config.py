"""
Configuration helper for AI Agent
Loads settings from .env file
"""

from dotenv import load_dotenv
import os
from ai_agent import GeminiProvider, QwenProvider

# Load environment variables
load_dotenv()


def get_provider():
    """
    Get the configured model provider from environment variables
    
    Returns:
        Model provider instance (GeminiProvider or QwenProvider)
        
    Raises:
        ValueError: If configuration is invalid or missing
    """
    model_provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    model_name = os.getenv("MODEL_NAME")
    api_key = os.getenv("API_KEY")
    
    # Check for provider-specific API keys if general API_KEY not found
    if not api_key:
        if model_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
        elif model_provider == "qwen":
            api_key = os.getenv("OLLAMA_API_KEY")
    
    # Validate API key is present
    if not api_key:
        key_name = "GEMINI_API_KEY" if model_provider == "gemini" else "OLLAMA_API_KEY"
        raise ValueError(
            f"No API key found. Please set {key_name} in your .env file"
        )
    
    # Set default model names if not specified
    if not model_name:
        if model_provider == "gemini":
            model_name = "gemini-pro"
        elif model_provider == "qwen":
            model_name = "qwen2.5:latest"
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {model_provider}. Use 'gemini' or 'qwen'")
    
    # Create and return the appropriate provider
    if model_provider == "gemini":
        return GeminiProvider(api_key=api_key, model_name=model_name)
    elif model_provider == "qwen":
        return QwenProvider(api_key=api_key, model_name=model_name)
    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {model_provider}. Use 'gemini' or 'qwen'")


def get_config():
    """
    Get configuration dictionary from environment
    
    Returns:
        dict: Configuration with provider, model_name, and api_key
    """
    return {
        "provider": os.getenv("MODEL_PROVIDER", "gemini").lower(),
        "model_name": os.getenv("MODEL_NAME", "gemini-pro"),
        "api_key": os.getenv("API_KEY"),
    }
