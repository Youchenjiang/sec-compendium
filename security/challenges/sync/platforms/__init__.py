"""
Platform Adapters Registry
"""

from security.challenges.sync.platforms.cyberdefenders import CyberDefendersAdapter
from security.challenges.sync.platforms.hackthebox import HackTheBoxAdapter
from security.challenges.sync.platforms.mta import MTAAdapter

ALL_ADAPTERS = {
    "cyberdefenders": CyberDefendersAdapter,
    "hackthebox": HackTheBoxAdapter,
    "mta": MTAAdapter,
}
