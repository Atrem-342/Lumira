"""Fact checking utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .generator import ExplanationSegment


@dataclass(slots=True)
class FactCheckResult:
    """Result of verifying a single claim."""

    claim: str
    verdict: str
    confidence: float
    citations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON serialisable dictionary."""

        return {
            "claim": self.claim,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "citations": list(self.citations),
        }


class FactChecker:
    """Perform lightweight fact checking via external services or heuristics."""

    SUPPORTED_VERDICTS = {"supported", "refuted", "uncertain"}

    def check(self, segments: Iterable[ExplanationSegment]) -> List[FactCheckResult]:
        """Return dummy :class:`FactCheckResult` entries for *segments* claims."""

        results: List[FactCheckResult] = []
        for segment in segments:
            verdict = "uncertain"
            confidence = 0.5
            if "definition" in segment.content.lower():
                verdict = "supported"
                confidence = 0.7
            results.append(
                FactCheckResult(
                    claim=segment.content[:200],
                    verdict=verdict,
                    confidence=confidence,
                    citations=segment.references,
                )
            )
        return results
