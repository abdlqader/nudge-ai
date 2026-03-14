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
            api_key = os.getenv("QWEN_API_KEY")  # Optional for local Qwen
    
    # Qwen doesn't require an API key for local deployment
    if not api_key and model_provider != "qwen":
        raise ValueError(
            f"No API key found. Please set API_KEY or {model_provider.upper()}_API_KEY in your .env file"
        )
    
    # Set default model names if not specified
    if not model_name:
        if model_provider == "gemini":
            model_name = "gemini-pro"
        elif model_provider == "qwen":
            model_name = "qwen-turbo"
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {model_provider}. Use 'gemini' or 'qwen'")
    
    # Create and return the appropriate provider
    if model_provider == "gemini":
        return GeminiProvider(api_key=api_key, model_name=model_name)
    elif model_provider == "qwen":
        base_url = os.getenv("QWEN_BASE_URL")
        return QwenProvider(api_key=api_key, model_name=model_name, base_url=base_url)
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
