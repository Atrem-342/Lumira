"""Tests for explanation generation."""

from lumira_tutoragent.core.analyzer import AnalysisResult
from lumira_tutoragent.core.generator import ExplanationGenerator
from lumira_tutoragent.core.planner import ExplanationPlanGenerator


def make_analysis() -> AnalysisResult:
    return AnalysisResult(
        intent="concept",
        subject="physics",
        difficulty="intermediate",
        learner_level="high_school",
        needs_retrieval=False,
        language="en",
    )


def test_generator_produces_segments() -> None:
    plan = ExplanationPlanGenerator().create_plan(make_analysis())
    generator = ExplanationGenerator()
    explanation = generator.generate(make_analysis(), plan)
    assert len(explanation) == len(plan)
    assert all(segment.references == () for segment in explanation)
