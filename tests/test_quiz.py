"""Tests for the quiz generator."""

from lumira_tutoragent.core.generator import ExplanationSegment
from lumira_tutoragent.core.quiz import QuizGenerator


def test_quiz_generator_creates_questions() -> None:
    segments = [
        ExplanationSegment(step_title="Activation", content="Recall something."),
        ExplanationSegment(step_title="Summary", content="Wrap up."),
    ]
    quiz = QuizGenerator().create_quiz(segments)
    assert len(quiz) >= 1
    assert all(item.answer_index == 0 for item in quiz)
