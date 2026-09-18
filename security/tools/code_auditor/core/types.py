"""
Shared data types for Code Auditor engine.
"""
from dataclasses import dataclass


@dataclass
class Vulnerability:
    """Represents a found vulnerability in a PHP package with dual object and dict access."""
    vuln_type: str
    file_path: str
    line_number: int
    code_snippet: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str = ""
    exploit_hint: str = ""  # Hint for exploit generation
    rule_id: str = ""
    category: str = ""

    def __getitem__(self, key: str):
        mapping = {
            "type": self.vuln_type,
            "vuln_type": self.vuln_type,
            "rule_name": self.vuln_type,
            "file": self.file_path,
            "file_path": self.file_path,
            "path": self.file_path,
            "line": self.line_number,
            "line_number": self.line_number,
            "code": self.code_snippet,
            "code_snippet": self.code_snippet,
            "severity": self.severity,
            "description": self.description,
            "desc": self.description,
            "exploit_hint": self.exploit_hint,
            "rule_id": self.rule_id,
            "category": self.category,
        }
        if key in mapping:
            return mapping[key]
        raise KeyError(key)

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: str) -> bool:
        return key in (
            "type", "vuln_type", "rule_name", "file", "file_path", "path",
            "line", "line_number", "code", "code_snippet", "severity",
            "description", "desc", "exploit_hint", "rule_id", "category",
        )

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def items(self):
        return self.to_dict().items()

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "rule_name": self.vuln_type,
            "type": self.vuln_type,
            "vuln_type": self.vuln_type,
            "severity": self.severity,
            "category": self.category,
            "file": self.file_path,
            "file_path": self.file_path,
            "line": self.line_number,
            "line_number": self.line_number,
            "code": self.code_snippet,
            "code_snippet": self.code_snippet,
            "description": self.description,
            "exploit_hint": self.exploit_hint,
        }
