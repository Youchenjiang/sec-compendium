"""
Challenge Sync Data Models

Defines the normalized ChallengeItem data structure representing a lab, machine,
or exercise from any cybersecurity learning or competition platform.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ChallengeItem:
    """Normalized challenge item across all training platforms."""

    id: str
    title: str
    platform: str
    tier: str  # e.g., 'FREE', 'VIP', 'VIP+', 'PREMIUM'
    difficulty: str  # e.g., 'Very Easy', 'Easy', 'Medium', 'Hard', 'Insane'
    category: str  # Primary domain/category
    url: str
    description: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_free(self) -> bool:
        """Check if the challenge is available on the free tier."""
        tier_normalized = self.tier.strip().upper()
        return "FREE" in tier_normalized or "🟢" in self.tier

    @property
    def clean_description(self) -> str:
        """Return clean single-line description for table rendering."""
        if not self.description:
            return ""
        return (
            self.description.replace("\r\n", " ")
            .replace("\n", " ")
            .replace("|", "\\|")
            .strip()
        )
