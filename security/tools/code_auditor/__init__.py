"""Code Auditor - Automated White-Box Security Audit & Dynamic Verification Engine"""
__version__ = "1.0.0"

from .core.scanner import Scanner, scan_file, scan_directory
from .core.types import Vulnerability
from .core.output import save_json, save_findings, save_summary, print_finding
from .generator.exploit_gen import ExploitGenerator, create_generator
from .sandbox.docker_tester import DockerTester, create_tester
from .storage.recorder import Storage, RunRecord
from .platform.base import BasePlatformClient
from .platform.local import LocalDirectoryClient
from .platform.wargame import WargamePlatformClient
from .engine import CodeAuditor

__all__ = [
    "CodeAuditor",
    "Scanner",
    "Vulnerability",
    "ExploitGenerator",
    "DockerTester",
    "Storage",
    "RunRecord",
    "BasePlatformClient",
    "LocalDirectoryClient",
    "WargamePlatformClient",
    "create_generator",
    "create_tester",
    "scan_file",
    "scan_directory",
    "save_json",
    "save_findings",
    "save_summary",
    "print_finding",
]
