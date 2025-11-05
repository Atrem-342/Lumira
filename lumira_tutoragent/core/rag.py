"""Retrieval augmented generation utilities for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .analyzer import AnalysisResult


@dataclass(slots=True)
class RetrievalResult:
    """Single chunk retrieved from the knowledge base."""

    source: str
    snippet: str

    def to_dict(self) -> dict[str, str]:
        """Return JSON serialisable dict."""

        return {"source": self.source, "snippet": self.snippet}


class RetrievalAugmentationEngine:
    """Tiny retrieval layer wrapper around static curriculum snippets."""

    def __init__(self, curriculum_dir: str | Path | None = None) -> None:
        self.curriculum_dir = Path(curriculum_dir) if curriculum_dir else None

    def retrieve(self, analysis: AnalysisResult) -> Iterable[RetrievalResult]:
        """Yield :class:`RetrievalResult` objects for the analysed topic."""

        if not self.curriculum_dir or not self.curriculum_dir.exists():
            yield RetrievalResult(
                source="placeholder://curriculum",
                snippet=(
                    "Knowledge retrieval placeholder. Insert integration with your corpus or API by "
                    "modifying RetrievalAugmentationEngine.retrieve."
                ),
            )
            return

        topic_path = self.curriculum_dir / f"{analysis.subject}.txt"
        if topic_path.exists():
            snippet = topic_path.read_text(encoding="utf-8").strip().splitlines()[0]
            yield RetrievalResult(source=str(topic_path), snippet=snippet)
        else:
            yield RetrievalResult(
                source="placeholder://curriculum",
                snippet="No curriculum file found. Provide your own data in data/curriculum/",
            )
