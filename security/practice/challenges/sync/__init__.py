"""
Challenge Sync Framework

A unified, modular framework for synchronizing, standardizing, and cataloging
cybersecurity challenge and lab datasets across multiple training platforms.
"""

from .models import ChallengeItem
from .base import BaseChallengeAdapter

__all__ = ["ChallengeItem", "BaseChallengeAdapter"]
