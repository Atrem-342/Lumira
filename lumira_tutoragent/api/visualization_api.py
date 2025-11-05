"""Visualization helper placeholders for Lumira TutorAgent."""

from __future__ import annotations

from typing import Dict


def render_mermaid_diagram(description: str) -> Dict[str, str]:
    """Return Mermaid.js source for *description* (placeholder)."""

    return {
        "description": description,
        "mermaid": "graph TD; A[Placeholder] --> B[Connect your visualization API];",
    }


def render_plotly_chart(spec: dict) -> Dict[str, object]:
    """Return a stub Plotly-compatible specification."""

    return {"spec": spec, "note": "Integrate Plotly or matplotlib rendering here."}
