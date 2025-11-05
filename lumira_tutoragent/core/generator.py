"""Explanation generation utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .analyzer import AnalysisResult
from .planner import PlanStep
from .rag import RetrievalAugmentationEngine, RetrievalResult


@dataclass(slots=True)
class ExplanationSegment:
    """Single section of a generated explanation."""

    step_title: str
    content: str
    references: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON friendly dictionary."""

        return {
            "step_title": self.step_title,
            "content": self.content,
            "references": list(self.references),
        }


class ExplanationGenerator:
    """Generate human-friendly explanations following a pedagogical plan."""

    def __init__(self, retrieval_engine: RetrievalAugmentationEngine | None = None) -> None:
        self._retrieval_engine = retrieval_engine

    def generate(self, analysis: AnalysisResult, plan: Sequence[PlanStep]) -> list[ExplanationSegment]:
        """Return explanation segments synthesised from *analysis* and *plan*."""

        retrievals: Iterable[RetrievalResult] = ()
        if analysis.needs_retrieval and self._retrieval_engine:
            retrievals = self._retrieval_engine.retrieve(analysis)
        references = tuple(result.source for result in retrievals)

        segments: List[ExplanationSegment] = []
        for step in plan:
            content = self._render_step(step, analysis)
            segments.append(ExplanationSegment(step_title=step.title, content=content, references=references))
        return segments

    def _render_step(self, step: PlanStep, analysis: AnalysisResult) -> str:
        """Render textual content for a plan *step* using *analysis* metadata."""

        base_intro = (
            f"Topic area: {analysis.subject}. Difficulty: {analysis.difficulty}. Learner level: {analysis.learner_level}."
        )
        if step.title == "Activation":
            return f"{base_intro} Let's recall what you already know about this topic. {step.description}"
        if step.title == "Metaphor":
            return f"Imagine the concept as something familiar to your daily life. {step.description}"
        if step.title == "Formal Definition":
            return (
                "Now we can outline the formal definition using clear language suitable for the learner's level. "
                f"{step.description}"
            )
        if step.title == "Real-life Example":
            return f"Consider a concrete example that matches everyday experiences. {step.description}"
        if step.title == "Typical Mistake":
            return f"Watch out for confusion or misconceptions. {step.description}"
        if step.title == "Check-for-Understanding":
            return (
                "Try to answer a reflective question or mini challenge to verify understanding. "
                f"{step.description}"
            )
        if step.title == "Summary":
            return f"Summarise the most important takeaways in a learner-friendly tone. {step.description}"
        return f"{base_intro} {step.description}"
