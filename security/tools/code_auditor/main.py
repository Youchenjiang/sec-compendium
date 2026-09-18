#!/usr/bin/env python3
"""
Code Auditor - Main Orchestrator & CLI Entrypoint
Automated white-box static analysis, PoC generation, sandbox verification, and reporting.
"""
import sys
import argparse
from pathlib import Path

if __package__ in (None, ""):
    _CURRENT = Path(__file__).resolve().parent
    _REPO_ROOT = _CURRENT.parent.parent.parent
    if str(_REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(_REPO_ROOT))
    from security.tools.code_auditor.engine import CodeAuditor
    from security.tools.code_auditor.platform.wargame import WargamePlatformClient
    from security.tools.code_auditor import config
else:
    from .engine import CodeAuditor
    from .platform.wargame import WargamePlatformClient
    from . import config


def main():
    parser = argparse.ArgumentParser(
        description="Code Auditor - Automated White-Box Security Audit & PoC Verification Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--local-dir", help="Audit local directory or project source code")
    parser.add_argument("--url", help="Platform base URL (for wargame/CTF competitions)")
    parser.add_argument("--email", help="Platform account email")
    parser.add_argument("--password", help="Platform account password")
    parser.add_argument("--dist-dir", help="Path to dist package containing vendor or challenge code")
    parser.add_argument("--target", help="Filter analysis to a specific target name")
    parser.add_argument("--scan-only", action="store_true", help="Perform static analysis only (no exploit generation)")
    parser.add_argument("--verify", action="store_true", help="Verify generated exploits in Docker sandbox")
    parser.add_argument("--no-submit", action="store_true", help="Do not submit exploits to platform")

    args = parser.parse_args()

    # Determine mode
    if args.local_dir:
        auditor = CodeAuditor(
            dist_dir=args.dist_dir or args.local_dir,
            enable_sandbox=args.verify,
        )
        auditor.audit_directory(
            target_dir=args.local_dir,
            scan_only=args.scan_only,
            verify=args.verify,
        )
    else:
        client = WargamePlatformClient(
            base_url=args.url or config.PLATFORM_BASE_URL,
            email=args.email or config.EMAIL,
            password=args.password or config.PASSWORD,
        )
        auditor = CodeAuditor(
            platform_client=client,
            dist_dir=args.dist_dir,
            enable_sandbox=args.verify,
        )
        auditor.run(
            target_name=args.target,
            scan_only=args.scan_only,
            verify=args.verify,
            no_submit=args.no_submit,
        )


if __name__ == "__main__":
    main()
