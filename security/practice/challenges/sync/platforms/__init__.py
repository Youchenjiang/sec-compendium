"""
Platform Adapters Registry
"""

from .cryptohack import CryptoHackAdapter
from .cyberdefenders import CyberDefendersAdapter
from .cylab_picoctf import CyLabAdapter
from .hackthebox import HackTheBoxAdapter
from .mta import MTAAdapter
from .portswigger import PortSwiggerAdapter
from .rootme import RootMeAdapter
from .tryhackme import TryHackMeAdapter

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

