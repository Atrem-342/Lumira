"""Teacher dashboard helpers for Lumira TutorAgent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from ..core.memory import LearnerProfile


@dataclass(slots=True)
class ProgressReport:
    """Summary of learner progress for display in the dashboard."""

    learner_id: str
    completed_topics: tuple[str, ...]
    misconceptions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return JSON ready representation."""

        return {
            "learner_id": self.learner_id,
            "completed_topics": list(self.completed_topics),
            "misconceptions": list(self.misconceptions),
        }


def build_progress_reports(profiles: Dict[str, LearnerProfile]) -> Iterable[ProgressReport]:
    """Convert *profiles* into dashboard friendly progress reports."""

    for learner_id, profile in profiles.items():
        yield ProgressReport(
            learner_id=learner_id,
            completed_topics=tuple(profile.completed_topics),
            misconceptions=tuple(profile.misconceptions),
        )
