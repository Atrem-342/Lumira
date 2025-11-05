"""Tests for the user query analyzer."""

from lumira_tutoragent.core.analyzer import UserQueryAnalyzer


def test_analyzer_detects_subject_and_intent() -> None:
    analyzer = UserQueryAnalyzer()
    result = analyzer.analyze("Explain photosynthesis for grade 6")
    assert result.subject == "biology"
    assert result.intent == "concept"
    assert result.learner_level == "middle_school"
    assert not result.needs_retrieval
