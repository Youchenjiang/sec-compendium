"""
Local Directory Client for Offline Code Auditing.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from .base import BasePlatformClient


class LocalDirectoryClient(BasePlatformClient):
    """Client for auditing local directories without remote platform."""

    def __init__(self, target_dir: str, package_name: str = None):
        self.target_dir = Path(target_dir).resolve()
        self.package_name = package_name

    def login(self) -> bool:
        return True

    def get_targets(self) -> List[Dict[str, Any]]:
        if not self.target_dir.exists():
            return []
        pkg_name = self.package_name or self.target_dir.name
        composer_json = self.target_dir / "composer.json"
        if composer_json.exists():
            try:
                cdata = json.loads(composer_json.read_text(encoding="utf-8"))
                pkg_name = cdata.get("name", pkg_name)
            except Exception:
                pass
        return [{
            "id": "local",
            "name": pkg_name,
            "version": "local",
            "php_version": "8.4",
            "source_path": str(self.target_dir),
        }]

    def submit(self, target_id: str, exploit_content: str) -> Dict[str, Any]:
        return {"status": "skipped", "message": "Local offline mode"}

    def get_status(self, submission_id: str) -> Dict[str, Any]:
        return {"status": "local_completed"}
