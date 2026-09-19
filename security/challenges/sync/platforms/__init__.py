"""
Platform Adapters Registry
"""

from security.challenges.sync.platforms.cyberdefenders import CyberDefendersAdapter
from security.challenges.sync.platforms.cylab_picoctf import CyLabAdapter
from security.challenges.sync.platforms.hackthebox import HackTheBoxAdapter
from security.challenges.sync.platforms.mta import MTAAdapter
from security.challenges.sync.platforms.portswigger import PortSwiggerAdapter

ALL_ADAPTERS = {
    "cyberdefenders": CyberDefendersAdapter,
    "hackthebox": HackTheBoxAdapter,
    "mta": MTAAdapter,
    "portswigger": PortSwiggerAdapter,
    "cylab_picoctf": CyLabAdapter,
}
