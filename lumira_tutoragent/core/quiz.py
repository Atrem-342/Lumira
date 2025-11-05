"""Quiz generation utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .generator import ExplanationSegment


@dataclass(slots=True)
class QuizItem:
    """A single question in a reflection quiz."""

    prompt: str
    choices: tuple[str, ...]
    answer_index: int

    def to_dict(self) -> dict[str, object]:
        """Return JSON serialisable dict."""

        return {
            "prompt": self.prompt,
            "choices": list(self.choices),
            "answer_index": self.answer_index,
        }


class QuizGenerator:
    """Generate lightweight quizzes for formative assessment."""

    def create_quiz(self, segments: Iterable[ExplanationSegment]) -> List[QuizItem]:
        """Build simple quiz questions derived from explanation *segments*."""

        questions: List[QuizItem] = []
        for index, segment in enumerate(segments):
            prompt = f"What is the key idea of the step '{segment.step_title}'?"
            choices = (
                segment.content[:100] + "...",
                "A completely unrelated idea",
                "An opposite misconception",
            )
            questions.append(QuizItem(prompt=prompt, choices=choices, answer_index=0))
            if index >= 1:
                break
        if not questions:
            questions.append(
                QuizItem(
                    prompt="What did you learn from this explanation?",
                    choices=("A new concept", "Nothing", "I'm unsure"),
                    answer_index=0,
                )
            )
        return questions
