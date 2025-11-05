"""Tests for the fact checker placeholder."""

from lumira_tutoragent.core.fact_checker import FactChecker
from lumira_tutoragent.core.generator import ExplanationSegment


def test_fact_checker_returns_results() -> None:
    segments = [
        ExplanationSegment(step_title="Formal Definition", content="This definition is well-known."),
        ExplanationSegment(step_title="Summary", content="General wrap up."),
    ]
    checker = FactChecker()
    results = checker.check(segments)
    assert len(results) == 2
    assert {result.verdict for result in results} <= FactChecker.SUPPORTED_VERDICTS
