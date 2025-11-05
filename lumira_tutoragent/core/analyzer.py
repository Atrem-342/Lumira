"""User query analysis utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class AnalysisResult:
    """Structured result of analyzing a learner's query."""

    intent: str
    subject: str
    difficulty: str
    learner_level: str
    needs_retrieval: bool
    language: str

    def to_dict(self) -> dict[str, str | bool]:
        """Return a JSON-serialisable dictionary representation."""

        return {
            "intent": self.intent,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "learner_level": self.learner_level,
            "needs_retrieval": self.needs_retrieval,
            "language": self.language,
        }


class UserQueryAnalyzer:
    """Analyze raw learner queries to determine tutoring strategy."""

    _SUBJECT_KEYWORDS: dict[str, tuple[str, ...]] = {
        "mathematics": ("algebra", "geometry", "calculus", "integral", "equation"),
        "physics": ("force", "energy", "motion", "optics", "quantum"),
        "chemistry": ("molecule", "reaction", "atom", "compound"),
        "biology": ("cell", "photosynthesis", "organism", "genetics"),
        "computer science": ("algorithm", "code", "program", "data"),
        "history": ("war", "revolution", "empire", "histor"),
        "language arts": ("poem", "literature", "essay", "grammar"),
    }

    _LEVEL_KEYWORDS: dict[str, tuple[str, ...]] = {
        "elementary": ("grade 3", "начальная школа", "elementary"),
        "middle_school": ("grade 6", "6 класс", "middle"),
        "high_school": ("grade 10", "вуз", "high"),
        "university": ("university", "college", "бакалавр"),
    }

    _INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
        "concept": ("explain", "что такое", "define"),
        "procedure": ("how to", "как сделать", "solve"),
        "fact": ("когда", "who", "что случилось"),
    }

    def analyze(self, query: str, *, language: Optional[str] = None) -> AnalysisResult:
        """Return an :class:`AnalysisResult` extracted from *query* heuristics."""

        normalized = query.lower()
        detected_language = language or ("ru" if any("а" <= ch <= "я" for ch in normalized) else "en")
        subject = self._detect_subject(normalized)
        intent = self._detect_intent(normalized)
        learner_level = self._detect_level(normalized)
        difficulty = self._estimate_difficulty(normalized)
        needs_retrieval = any(kw in normalized for kw in ("latest", "новое", "данные", "статистика"))
        return AnalysisResult(
            intent=intent,
            subject=subject,
            difficulty=difficulty,
            learner_level=learner_level,
            needs_retrieval=needs_retrieval,
            language=detected_language,
        )

    def _detect_subject(self, text: str) -> str:
        for subject, keywords in self._SUBJECT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return subject
        return "general"

    def _detect_intent(self, text: str) -> str:
        for intent, keywords in self._INTENT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return intent
        return "concept"

    def _detect_level(self, text: str) -> str:
        for level, keywords in self._LEVEL_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return level
        return "middle_school"

    def _estimate_difficulty(self, text: str) -> str:
        if any(word in text for word in ("advanced", "сложн", "difficult")):
            return "advanced"
        if any(word in text for word in ("basic", "прост", "simple")):
            return "beginner"
        return "intermediate"
