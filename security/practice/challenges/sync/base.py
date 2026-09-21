"""
Base Challenge Adapter Interface

Defines the abstract base class that all platform adapters must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List
from .models import ChallengeItem


class BaseChallengeAdapter(ABC):
    """Abstract base class for challenge platform synchronization."""

    platform_id: str = ""
    display_name: str = ""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.target_dir = (
            repo_root / "security" / "practice" / "challenges" / "platforms" / self.platform_id
        )

    @abstractmethod
    def fetch_challenges(self) -> List[ChallengeItem]:
        """Fetch and normalize challenge items from the remote platform API or website."""
        pass

    @abstractmethod
    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        """Generate platform CSV and Markdown catalog files. Returns list of generated paths."""
        pass

    def sync(self) -> Dict[str, Any]:
        """Execute full synchronization pipeline for this platform."""
        print("\n========================================================")
        print(f"[*] Syncing [{self.display_name}] (ID: {self.platform_id})")
        print("========================================================")

        self.target_dir.mkdir(parents=True, exist_ok=True)
        challenges = self.fetch_challenges()

        total = len(challenges)
        free_count = sum(1 for c in challenges if c.is_free)

        print(f"  [Info] Total challenges fetched: {total}")
        print(f"  [Info] Free tier challenges:     {free_count}")

        generated_files = self.write_outputs(challenges)

        return {
            "platform_id": self.platform_id,
            "display_name": self.display_name,
            "total": total,
            "free_count": free_count,
            "generated_files": [str(p) for p in generated_files],
        }
