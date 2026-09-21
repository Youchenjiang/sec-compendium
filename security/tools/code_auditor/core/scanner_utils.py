"""
Shared PHP file scanning utilities.

Uses unified rules from lib.scanner_rules.
"""
import re
import time
from pathlib import Path
from typing import List

from .scanner_rules import VulnRule, CORE_RULES as CORE_PATTERNS

# Directories to skip when scanning PHP packages
SKIP_DIRS = frozenset({
    "tests", "test", "fixtures", "fixture", "spec", "features",
    "docs", "doc", "examples", "example", "vendor",
    "phpunit", ".git", "__pycache__",
})

ENTRY_FILENAMES = frozenset({
    "index.php", "install.php", "setup.php", "main.php",
    "server.php", "app.php", "console.php",
})

SUPERGLOBALS = re.compile(r"\$_(?:GET|POST|REQUEST|COOKIE|SERVER|FILES)")

# Filename-based patterns (match against file path, not content)
FILENAME_PATTERNS: List[VulnRule] = [
    VulnRule(id="FNAME-001", name="Installer/setup",
             pattern=r"(?:install|setup|wizard|configure|build)\.php$",
             severity="HIGH", tier="BROAD", category="filename"),
    VulnRule(id="FNAME-002", name="Admin backend",
             pattern=r"(?:admin|administrator|backend|manage|dashboard)/.*?\.php$|admin\.php$",
             severity="HIGH", tier="BROAD", category="filename"),
    VulnRule(id="FNAME-003", name="Test/debug",
             pattern=r"(?:test|tests|debug|probe|bench|benchmark|check|diag|doctor)\.php$",
             severity="MEDIUM", tier="BROAD", category="filename"),
    VulnRule(id="FNAME-004", name="API/webhook",
             pattern=r"(?:api|webhook|callback|notify|gateway|endpoint|ipn)\.php$",
             severity="MEDIUM", tier="BROAD", category="filename"),
    VulnRule(id="FNAME-005", name="Upload/download",
             pattern=r"(?:upload|uploader|download|fetch|attachment|export|import)\.php$",
             severity="MEDIUM", tier="BROAD", category="filename"),
    VulnRule(id="FNAME-006", name="Mock server",
             pattern=r"(?:mock|server|stub|fake|emulator|simulator)/.*?\.php$|server\.php$",
             severity="MEDIUM", tier="BROAD", category="filename"),
]


def iter_php_files(pkg_dir, skip_tests=True, skip_vendor=True):
    for php_file in pkg_dir.rglob("*.php"):
        parts = {p.lower() for p in php_file.parts}
        if skip_tests and parts & SKIP_DIRS:
            continue
        if skip_vendor and "vendor" in parts:
            continue
        yield php_file


def read_php_file(path):
    for _ in range(5):
        try:
            return Path(path).read_text(encoding="utf-8", errors="ignore")
        except (PermissionError, OSError):
            time.sleep(0.05)
        except Exception:
            return None
    return None


def is_comment(line):
    return line.startswith(("//", "#", "/*", "*"))


# Matches /* ... */ on a single line (non-greedy) and // or # trailing comments
_BLOCK_OPEN = re.compile(r"/\*")
_BLOCK_CLOSE = re.compile(r"\*/")
_LINE_COMMENT = re.compile(r"(//|#).*$")
_STRING_LIT = re.compile(r"""(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')""")


def _mask_strings(line):
    """Replace string literal contents with spaces to avoid false comment matches."""
    return _STRING_LIT.sub(lambda m: '"' + " " * (len(m.group()) - 2) + '"', line)


def strip_comments(line, in_block=False):
    """
    Strip PHP comments from a line while tracking block comment state across lines.
    Returns (sanitized_code, in_block_comment).
    """
    if in_block:
        close = _BLOCK_CLOSE.search(line)
        if close:
            line = line[close.end():]
            in_block = False
        else:
            return "", True

    # Mask string literals so /* or // inside strings aren't treated as comments
    masked = _mask_strings(line)

    # Handle block comment start
    open_m = _BLOCK_OPEN.search(masked)
    if open_m:
        before = line[: open_m.start()]
        rest = masked[open_m.end():]
        close = _BLOCK_CLOSE.search(rest)
        if close:
            # Block comment closed on same line — strip it and recurse
            tail = line[open_m.end() + close.end():]
            code, in_block = strip_comments(before + tail, False)
        else:
            in_block = True
            code = _LINE_COMMENT.sub("", before).strip()
        return code, in_block

    # Strip trailing line comments
    code = _LINE_COMMENT.sub("", line).strip()
    return code, False


def has_superglobal(content):
    return bool(SUPERGLOBALS.search(content))


def scan_line(line, patterns=None):
    if patterns is None:
        patterns = CORE_PATTERNS
    results = []
    for p in patterns:
        if p.search(line):
            results.append({
                "type": p.name,
                "severity": p.severity,
                "desc": p.description,
            })
    return results


def scan_package(pkg_dir, patterns=None):
    if patterns is None:
        patterns = CORE_PATTERNS
    findings = []
    for php_file in iter_php_files(pkg_dir):
        content = read_php_file(php_file)
        if content is None:
            continue
        rel_path = str(php_file.relative_to(pkg_dir))
        lines = content.split("\n")
        in_block = False
        for idx, line in enumerate(lines, 1):
            stripped, in_block = strip_comments(line, in_block)
            if not stripped:
                continue
            matches = scan_line(stripped, patterns)
            for m in matches:
                findings.append({
                    "file": rel_path,
                    "line": idx,
                    "code": stripped[:120],
                    "type": m["type"],
                    "severity": m["severity"],
                    "desc": m["desc"],
                })
    return findings
