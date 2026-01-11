"""
Model Backend Abstraction

This module provides a unified interface for different model backends:
- Anthropic API (paid, cloud-based)
- Ollama (free, local models)
- Future: HuggingFace, OpenAI, etc.
"""

from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from enum import Enum


class BackendType(Enum):
    """Available model backends."""
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class ModelBackend(ABC):
    """Abstract base class for model backends."""

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate a response given messages and system prompt.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System prompt to guide behavior
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this backend is available."""
        pass


class AnthropicBackend(ModelBackend):
    """Anthropic API backend (paid, requires API key)."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        max_tokens: int = 1024
    ) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text

    def is_available(self) -> bool:
        try:
            # Try a minimal API call
            self.client.messages.create(
                model=self.model,
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except Exception:
            return False


class OllamaBackend(ModelBackend):
    """
    Ollama backend (free, local models).

    Requires Ollama to be installed and running locally.
    Install: https://ollama.ai
    Start: ollama serve
    Pull model: ollama pull llama3.2
    """

    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        max_tokens: int = 1024
    ) -> str:
        import requests

        # Ollama API format
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages
            ],
            "stream": False,
            "options": {
                "num_predict": max_tokens
            }
        }

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")

        result = response.json()
        return result["message"]["content"]

    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


def create_backend(
    backend_type: BackendType,
    **kwargs
) -> ModelBackend:
    """
    Factory function to create a model backend.

    Args:
        backend_type: Type of backend to create
        **kwargs: Backend-specific configuration
            For ANTHROPIC: api_key (required), model (optional)
            For OLLAMA: model (optional, default "llama3.2"), base_url (optional)

    Returns:
        ModelBackend instance

    Examples:
        # Anthropic (paid)
        backend = create_backend(
            BackendType.ANTHROPIC,
            api_key="your-api-key",
            model="claude-sonnet-4-5-20250929"
        )

        # Ollama (free, local)
        backend = create_backend(
            BackendType.OLLAMA,
            model="llama3.2"
        )
    """
    if backend_type == BackendType.ANTHROPIC:
        api_key = kwargs.get("api_key")
        if not api_key:
            raise ValueError("api_key is required for Anthropic backend")
        model = kwargs.get("model", "claude-sonnet-4-5-20250929")
        return AnthropicBackend(api_key=api_key, model=model)

    elif backend_type == BackendType.OLLAMA:
        model = kwargs.get("model", "llama3.2")
        base_url = kwargs.get("base_url", "http://localhost:11434")
        return OllamaBackend(model=model, base_url=base_url)

    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


# Recommended free models for Ollama
OLLAMA_MODELS = {
    "llama3.2": {
        "name": "Llama 3.2 (3B)",
        "size": "2GB",
        "description": "Fast and efficient, good for quick conversations"
    },
    "llama3.2:1b": {
        "name": "Llama 3.2 (1B)",
        "size": "1.3GB",
        "description": "Very lightweight, great for testing"
    },
    "llama3.1": {
        "name": "Llama 3.1 (8B)",
        "size": "4.7GB",
        "description": "Balanced performance and quality"
    },
    "mistral": {
        "name": "Mistral (7B)",
        "size": "4.1GB",
        "description": "High quality, good reasoning"
    },
    "qwen2.5": {
        "name": "Qwen 2.5 (7B)",
        "size": "4.7GB",
        "description": "Strong general capabilities"
    },
    "phi3.5": {
        "name": "Phi 3.5 (3.8B)",
        "size": "2.2GB",
        "description": "Compact but capable"
    }
}
