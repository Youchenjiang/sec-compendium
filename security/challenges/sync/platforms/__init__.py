"""
Platform Adapters Registry
"""

from security.challenges.sync.platforms.cryptohack import CryptoHackAdapter
from security.challenges.sync.platforms.cyberdefenders import CyberDefendersAdapter
from security.challenges.sync.platforms.cylab_picoctf import CyLabAdapter
from security.challenges.sync.platforms.hackthebox import HackTheBoxAdapter
from security.challenges.sync.platforms.mta import MTAAdapter
from security.challenges.sync.platforms.portswigger import PortSwiggerAdapter
from security.challenges.sync.platforms.rootme import RootMeAdapter
from security.challenges.sync.platforms.tryhackme import TryHackMeAdapter

ALL_ADAPTERS = {
    "cyberdefenders": CyberDefendersAdapter,
    "hackthebox": HackTheBoxAdapter,
    "mta": MTAAdapter,
    "portswigger": PortSwiggerAdapter,
    "cylab_picoctf": CyLabAdapter,
    "cryptohack": CryptoHackAdapter,
    "tryhackme": TryHackMeAdapter,
    "rootme": RootMeAdapter,
}

