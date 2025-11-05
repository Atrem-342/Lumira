"""Student-facing UI helpers for Lumira TutorAgent."""

from __future__ import annotations

from typing import Iterable, List

from ..core.generator import ExplanationSegment
from ..core.quiz import QuizItem


def render_explanation(segments: Iterable[ExplanationSegment]) -> List[str]:
    """Return formatted strings for each explanation segment."""

    return [f"## {segment.step_title}\n{segment.content}" for segment in segments]


def render_quiz(quiz_items: Iterable[QuizItem]) -> List[str]:
    """Return formatted quiz questions for console or markdown display."""

    rendered = []
    for item in quiz_items:
        choices = "\n".join(f"- {choice}" for choice in item.choices)
        rendered.append(f"**Question:** {item.prompt}\n{choices}")
    return rendered
