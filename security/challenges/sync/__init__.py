"""
Challenge Sync Framework

A unified, modular framework for synchronizing, standardizing, and cataloging
cybersecurity challenge and lab datasets across multiple training platforms.
"""

from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.base import BaseChallengeAdapter

__all__ = ["ChallengeItem", "BaseChallengeAdapter"]
