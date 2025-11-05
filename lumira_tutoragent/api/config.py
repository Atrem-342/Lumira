"""API configuration utilities with explicit placeholder locations."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

_PLACEHOLDER_SETTINGS: Dict[str, str] = {
    "OPENAI_API_KEY": "PASTE_YOUR_OPENAI_KEY_HERE",
    "OPENROUTER_API_KEY": "PASTE_YOUR_OPENROUTER_KEY_HERE",
    "GROQ_API_KEY": "PASTE_YOUR_GROQ_KEY_HERE",
    "FACTCHECKER_API_URL": "https://api.yourfactchecker.com/v1",
    "FACTCHECKER_API_KEY": "PASTE_FACTCHECKER_KEY_HERE",
}
"""Default values indicating where to place your API keys and endpoints."""


def load_env_file(path: str | os.PathLike[str] = ".env") -> None:
    """Populate ``os.environ`` from a ``.env`` file without external dependencies."""

    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def get_api_settings() -> Dict[str, str]:
    """Return API configuration values honouring placeholders.

    The returned dictionary highlights the **empty places** where credentials must be
    inserted: update the ``_PLACEHOLDER_SETTINGS`` mapping or provide a ``.env`` file
    with the same keys.
    """

    load_env_file()
    settings = {key: os.environ.get(key, placeholder) for key, placeholder in _PLACEHOLDER_SETTINGS.items()}
    return settings
