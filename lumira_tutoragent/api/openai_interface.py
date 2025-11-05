"""OpenAI-compatible interface placeholders for Lumira TutorAgent."""

from __future__ import annotations

from typing import Any, Dict

from .config import get_api_settings


class OpenAIClient:
    """Lightweight wrapper for OpenAI compatible models with placeholders."""

    def __init__(self) -> None:
        self.settings = get_api_settings()

    def create_completion(self, prompt: str, *, model: str = "gpt-4o-mini", **kwargs: Any) -> Dict[str, Any]:
        """Return a placeholder completion response for *prompt*.

        Replace this implementation with a real API call using ``requests`` or ``openai``
        once credentials are provided.
        """

        del kwargs
        return {
            "model": model,
            "prompt": prompt,
            "message": "This is a placeholder response. Integrate OpenAI API here.",
            "api_keys_defined": bool(self.settings.get("OPENAI_API_KEY")),
        }
