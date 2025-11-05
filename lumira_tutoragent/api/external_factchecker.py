"""External fact-checker integration placeholders for Lumira TutorAgent."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ..core.generator import ExplanationSegment
from .config import get_api_settings


def format_payload(segments: Iterable[ExplanationSegment]) -> Dict[str, Any]:
    """Prepare JSON payload expected by an external fact-checking API."""

    claims = [segment.content for segment in segments]
    return {"claims": claims, "metadata": {"source": "Lumira TutorAgent"}}


def call_external_factchecker(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send *payload* to the external fact-checking service (placeholder)."""

    settings = get_api_settings()
    return {
        "status": "placeholder",
        "payload": payload,
        "endpoint": settings.get("FACTCHECKER_API_URL"),
        "api_key_provided": bool(settings.get("FACTCHECKER_API_KEY")),
    }


def interpret_factchecker_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert the placeholder *response* into a list of fact-check results."""

    claims = response.get("payload", {}).get("claims", [])
    return [
        {
            "claim": claim,
            "verdict": "uncertain",
            "confidence": 0.0,
            "citations": [],
        }
        for claim in claims
    ]
