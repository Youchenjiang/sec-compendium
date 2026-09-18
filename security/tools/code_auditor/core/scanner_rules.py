"""Unified PHP vulnerability scanning rules - single source of truth."""
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VulnRule:
    id: str
    name: str
    pattern: str
    severity: str
    category: str
    description: str = ""
    fix: str = ""
    exploit_pattern: Optional[str] = None
    tier: str = "CORE"
    _regex: Optional[re.Pattern] = field(default=None, repr=False, compare=False)

    def _ensure_regex(self):
        if self._regex is None:
            self._regex = re.compile(self.pattern, re.IGNORECASE)
        return self._regex

    def search(self, line):
        return self._ensure_regex().search(line)

    def finditer(self, content):
        return self._ensure_regex().finditer(content)


_ALL_RULES = []

_ALL_RULES.append(VulnRule(id="PHP-RCE-001", name="eval() with user input", pattern=r"\beval\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE|SERVER)", severity="CRITICAL", tier="CORE", category="code_execution", description="eval() executes arbitrary PHP code from user input"))
_ALL_RULES.append(VulnRule(id="PHP-RCE-002", name="assert() with user input", pattern=r"\bassert\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE|SERVER)", severity="CRITICAL", tier="CORE", category="code_execution"))
_ALL_RULES.append(VulnRule(id="PHP-RCE-003", name="preg_replace /e modifier", pattern=r"preg_replace\s*\(\s*['\"].*?/e[a-z]*['\"]", severity="CRITICAL", tier="CORE", category="code_execution"))
_ALL_RULES.append(VulnRule(id="PHP-RCE-004", name="create_function() deprecated RCE", pattern=r"\bcreate_function\s*\(", severity="CRITICAL", tier="BROAD", category="code_execution"))
_ALL_RULES.append(VulnRule(id="PHP-RCE-005", name="Variable function dispatch", pattern=r"\$[a-zA-Z0-9_]+\s*\(\s*\$", severity="HIGH", tier="BROAD", category="code_execution"))
_ALL_RULES.append(VulnRule(id="PHP-RCE-006", name="eval() call", pattern=r"\beval\s*\(", severity="MEDIUM", tier="BROAD", category="code_execution"))
_ALL_RULES.append(VulnRule(id="PHP-CMD-001", name="System command exec with user input", pattern=r"\b(?:system|exec|passthru|shell_exec|popen|proc_open)\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE|SERVER)", severity="CRITICAL", tier="CORE", category="command_injection", exploit_pattern="cmd"))
_ALL_RULES.append(VulnRule(id="PHP-CMD-002", name="Backtick shell execution", pattern=r"\x60[^\x60\$]*\$\x60", severity="HIGH", tier="BROAD", category="command_injection"))
_ALL_RULES.append(VulnRule(id="PHP-CMD-003", name="Command injection via string concat", pattern=r"(?:exec|system|passthru|shell_exec|popen)\s*\(.*\.\s*\$", severity="HIGH", tier="BROAD", category="command_injection"))
_ALL_RULES.append(VulnRule(id="PHP-CMD-004", name="system() call", pattern=r"\bsystem\s*\(", severity="MEDIUM", tier="BROAD", category="command_injection"))
_ALL_RULES.append(VulnRule(id="PHP-CMD-005", name="exec() call", pattern=r"\bexec\s*\(", severity="MEDIUM", tier="BROAD", category="command_injection"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-001", name="file_put_contents with user input", pattern=r"file_put_contents\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)", severity="HIGH", tier="CORE", category="file_operation", exploit_pattern="php://filter"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-002", name="fwrite with user input", pattern=r"fwrite\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)", severity="HIGH", tier="CORE", category="file_operation"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-003", name="file_get_contents with user input", pattern=r"file_get_contents\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)", severity="HIGH", tier="CORE", category="file_operation", exploit_pattern="php://filter/convert.base64-encode/resource=/etc/passwd"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-004", name="file_put_contents() call", pattern=r"\bfile_put_contents\s*\(", severity="MEDIUM", tier="BROAD", category="file_operation"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-005", name="File deletion with variable", pattern=r"\bunlink\s*\(\s*\$", severity="MEDIUM", tier="BROAD", category="file_operation"))
_ALL_RULES.append(VulnRule(id="PHP-FILE-006", name="fwrite/fputs stream write", pattern=r"\b(?:fwrite|fputs)\s*\(", severity="MEDIUM", tier="BROAD", category="file_operation"))
_ALL_RULES.append(VulnRule(id="PHP-INC-001", name="File inclusion with user input (LFI/RFI)", pattern=r"\b(?:include|require|include_once|require_once)\s*\(?.*\$_(?:GET|POST|REQUEST|COOKIE)", severity="HIGH", tier="CORE", category="file_inclusion", exploit_pattern="php://filter/convert.base64-encode/resource=index.php"))
_ALL_RULES.append(VulnRule(id="PHP-INC-002", name="Dynamic include / require", pattern=r"\b(?:include|require|include_once|require_once)\s*\(?\s*\$", severity="HIGH", tier="BROAD", category="file_inclusion"))
_ALL_RULES.append(VulnRule(id="PHP-DESER-001", name="unserialize with user input", pattern=r"unserialize\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)", severity="HIGH", tier="CORE", category="deserialization"))
_ALL_RULES.append(VulnRule(id="PHP-DESER-002", name="unserialize with file content", pattern=r"unserialize\s*\(.*file_get_contents", severity="HIGH", tier="CORE", category="deserialization"))
_ALL_RULES.append(VulnRule(id="PHP-DESER-003", name="unserialize() call", pattern=r"\bunserialize\s*\(", severity="MEDIUM", tier="BROAD", category="deserialization"))
_ALL_RULES.append(VulnRule(id="PHP-SQL-001", name="SQL query with string concatenation", pattern=r"(?:query|execute|exec)\s*\(.*[\"\'].*\.\s*\$", severity="HIGH", tier="BROAD", category="sql_injection"))
_ALL_RULES.append(VulnRule(id="PHP-SQL-002", name="SQL string concatenation with variable", pattern=r"(?:SELECT|INSERT|UPDATE|DELETE|UNION)\s+[^;]{1,80}\.\s*\$", severity="HIGH", tier="BROAD", category="sql_injection"))
_ALL_RULES.append(VulnRule(id="PHP-SQL-003", name="SQL query with direct superglobal", pattern=r"\$_(?:GET|POST|REQUEST|COOKIE)\s*\[.*\].*(?:query|execute)", severity="HIGH", tier="CORE", category="sql_injection"))
_ALL_RULES.append(VulnRule(id="PHP-PATH-001", name="Path traversal in file operations", pattern=r"\b(?:file_get_contents|file_put_contents|fopen|readfile|highlight_file|show_source|unlink)\s*\(.*\$_(?:GET|POST|REQUEST)", severity="HIGH", tier="CORE", category="path_traversal", exploit_pattern="../../../../etc/passwd"))
_ALL_RULES.append(VulnRule(id="PHP-PATH-002", name="Dynamic file read", pattern=r"\b(?:file_get_contents|readfile|highlight_file|show_source)\s*\(\s*\$", severity="MEDIUM", tier="BROAD", category="path_traversal"))
_ALL_RULES.append(VulnRule(id="PHP-TYPE-001", name="Loose comparison with superglobal", pattern=r"===?\s*\$_(?:GET|POST|REQUEST)", severity="MEDIUM", tier="CORE", category="type_juggling"))
_ALL_RULES.append(VulnRule(id="PHP-TYPE-002", name="Loose comparison on hashes", pattern=r"(?:md5|sha1|hash)\s*\([^)]+\)\s*==\s*", severity="MEDIUM", tier="BROAD", category="type_juggling"))
_ALL_RULES.append(VulnRule(id="PHP-AUTH-001", name="Weak password comparison", pattern=r"\b(?:md5|sha1)\s*\(\s*\$.*===?\s*\$", severity="HIGH", tier="BROAD", category="auth_bypass"))
_ALL_RULES.append(VulnRule(id="PHP-AUTH-002", name="strcmp bypass with array", pattern=r"strcmp\s*\(\s*\$.*\$_(?:GET|POST|REQUEST)", severity="HIGH", tier="CORE", category="auth_bypass"))
_ALL_RULES.append(VulnRule(id="PHP-OBJ-001", name="Magic method with dangerous ops", pattern=r"function\s+__(?:wakeup|destruct)\s*\([^)]*\)\s*\{[^}]*(?:file_put_contents|fwrite|unlink|system|exec)", severity="CRITICAL", tier="BROAD", category="object_injection"))
_ALL_RULES.append(VulnRule(id="PHP-CRYPTO-001", name="Weak hashing (MD5/SHA1)", pattern=r"\b(?:md5|sha1)\s*\(", severity="MEDIUM", tier="BROAD", category="weak_crypto"))
_ALL_RULES.append(VulnRule(id="PHP-CRYPTO-002", name="Insecure random generator", pattern=r"\b(?:rand|mt_rand|uniqid)\s*\(", severity="LOW", tier="BROAD", category="weak_crypto"))
_ALL_RULES.append(VulnRule(id="PHP-INFO-001", name="phpinfo() exposed", pattern=r"\bphpinfo\s*\(\s*\)", severity="MEDIUM", tier="BROAD", category="info_disclosure"))
_ALL_RULES.append(VulnRule(id="PHP-INFO-002", name="Error display enabled", pattern=r"display_errors\s*=\s*On|error_reporting\s*\(\s*E_ALL", severity="LOW", tier="BROAD", category="info_disclosure"))
_ALL_RULES.append(VulnRule(id="PHP-INFO-003", name="Debug info dump", pattern=r"\b(?:phpinfo|var_dump|print_r)\s*\(", severity="LOW", tier="BROAD", category="info_disclosure"))
_ALL_RULES.append(VulnRule(id="PHP-SSRF-001", name="Dynamic cURL URL setting", pattern=r"CURLOPT_URL\s*,\s*\$", severity="MEDIUM", tier="BROAD", category="ssrf"))


def get_rules(tier=None, category=None):
    """Return rules filtered by tier and/or category."""
    rules = _ALL_RULES
    if tier:
        rules = [r for r in rules if r.tier == tier]
    if category:
        rules = [r for r in rules if r.category == category]
    return rules


CORE_RULES = [r for r in _ALL_RULES if r.tier == "CORE"]
BROAD_RULES = [r for r in _ALL_RULES if r.tier == "BROAD"]
ALL_RULES = list(_ALL_RULES)
CATEGORIES = sorted({r.category for r in _ALL_RULES})
