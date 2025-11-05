"""Learner profile memory utilities for Lumira TutorAgent."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass(slots=True)
class LearnerProfile:
    """Representation of a learner's long-term tutoring profile."""

    learner_id: str
    level: str
    interests: List[str] = field(default_factory=list)
    completed_topics: List[str] = field(default_factory=list)
    misconceptions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return JSON serialisable data."""

        return {
            "learner_id": self.learner_id,
            "level": self.level,
            "interests": list(self.interests),
            "completed_topics": list(self.completed_topics),
            "misconceptions": list(self.misconceptions),
        }


class ProfileMemory:
    """Persist learner profiles to the local data directory."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        base_path = Path(storage_path) if storage_path else Path("lumira_tutoragent/data/user_profiles.json")
        self._storage_path = base_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, LearnerProfile]:
        """Load all learner profiles from storage."""

        if not self._storage_path.exists():
            return {}
        raw_data = json.loads(self._storage_path.read_text(encoding="utf-8"))
        profiles = {
            learner_id: LearnerProfile(
                learner_id=learner_id,
                level=data.get("level", "middle_school"),
                interests=list(data.get("interests", [])),
                completed_topics=list(data.get("completed_topics", [])),
                misconceptions=list(data.get("misconceptions", [])),
            )
            for learner_id, data in raw_data.items()
        }
        return profiles

    def save(self, profiles: Dict[str, LearnerProfile]) -> None:
        """Persist *profiles* to disk."""

        serialised = {learner_id: profile.to_dict() for learner_id, profile in profiles.items()}
        self._storage_path.write_text(json.dumps(serialised, ensure_ascii=False, indent=2), encoding="utf-8")

    def update_profile(
        self,
        learner_id: str,
        *,
        level: str | None = None,
        completed_topic: str | None = None,
        misconception: str | None = None,
    ) -> LearnerProfile:
        """Update the stored profile of *learner_id* and return the new state."""

        profiles = self.load()
        profile = profiles.get(learner_id)
        if profile is None:
            profile = LearnerProfile(learner_id=learner_id, level=level or "middle_school")
        if level:
            profile.level = level
        if completed_topic and completed_topic not in profile.completed_topics:
            profile.completed_topics.append(completed_topic)
        if misconception and misconception not in profile.misconceptions:
            profile.misconceptions.append(misconception)
        profiles[learner_id] = profile
        self.save(profiles)
        return profile
