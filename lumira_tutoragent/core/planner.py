"""Explanation planning utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .analyzer import AnalysisResult


@dataclass(slots=True)
class PlanStep:
    """Single step within an explanation plan."""

    title: str
    description: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON ready representation."""

        return {"title": self.title, "description": self.description}


class ExplanationPlanGenerator:
    """Generate structured plans aligned with pedagogical best practices."""

    DEFAULT_STRUCTURE: List[tuple[str, str]] = [
        ("Activation", "Activate prior knowledge relevant to the topic."),
        ("Metaphor", "Provide an intuitive metaphor or analogy."),
        ("Formal Definition", "Introduce formal definitions or formulas."),
        ("Real-life Example", "Ground the concept in an everyday scenario."),
        ("Typical Mistake", "Warn about a common misconception."),
        ("Check-for-Understanding", "Pose a mini question."),
        ("Summary", "Conclude with a concise recap."),
    ]

    def create_plan(self, analysis: AnalysisResult, *, steps: Iterable[tuple[str, str]] | None = None) -> list[PlanStep]:
        """Return a list of :class:`PlanStep` instances tailored to *analysis*."""

        structure = list(steps) if steps is not None else self.DEFAULT_STRUCTURE
        plan: list[PlanStep] = []
        for title, description in structure:
            contextual_description = description
            if analysis.subject != "general":
                contextual_description = f"{description} (Subject: {analysis.subject})."
            plan.append(PlanStep(title=title, description=contextual_description))
        return plan
