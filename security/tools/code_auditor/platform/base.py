"""
Abstract Base Platform Client for Code Auditor.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BasePlatformClient(ABC):
    """Abstract interface for audit targets and competition platforms."""

    @abstractmethod
    def login(self) -> bool:
        """Authenticate with the target platform."""
        pass

    @abstractmethod
    def get_targets(self) -> List[Dict[str, Any]]:
        """Fetch list of target packages or repositories to audit."""
        pass

    @abstractmethod
    def submit(self, target_id: str, exploit_content: str) -> Dict[str, Any]:
        """Submit an exploit or audit finding."""
        pass

    @abstractmethod
    def get_status(self, submission_id: str) -> Dict[str, Any]:
        """Check status of a submission."""
        pass
