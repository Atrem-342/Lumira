"""High-level orchestration helpers for building a web app interface."""

from __future__ import annotations

from typing import Dict

from ..core import (
    ExplanationGenerator,
    ExplanationPlanGenerator,
    FactChecker,
    ProfileMemory,
    QuizGenerator,
    RetrievalAugmentationEngine,
    UserQueryAnalyzer,
)


def run_tutoring_cycle(query: str) -> Dict[str, object]:
    """Execute an end-to-end tutoring flow for *query* returning JSON data."""

    analyzer = UserQueryAnalyzer()
    analysis = analyzer.analyze(query)

    planner = ExplanationPlanGenerator()
    plan = planner.create_plan(analysis)

    retrieval_engine = RetrievalAugmentationEngine()
    generator = ExplanationGenerator(retrieval_engine=retrieval_engine)
    explanation = generator.generate(analysis, plan)

    fact_checker = FactChecker()
    fact_results = fact_checker.check(explanation)

    quiz_generator = QuizGenerator()
    quiz = quiz_generator.create_quiz(explanation)

    memory = ProfileMemory()
    profile = memory.update_profile("demo-learner", completed_topic=analysis.subject)

    return {
        "analysis": analysis.to_dict(),
        "plan": [step.to_dict() for step in plan],
        "explanation": [segment.to_dict() for segment in explanation],
        "fact_check": [result.to_dict() for result in fact_results],
        "quiz": [item.to_dict() for item in quiz],
        "profile": profile.to_dict(),
    }
