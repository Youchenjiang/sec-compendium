#!/usr/bin/env python3
"""Shared protocol helpers for the governed ``.collab`` case bus."""

from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
COLLAB_DIR = REPO_ROOT / ".collab"
CASES_DIR = COLLAB_DIR / "cases"
RUNTIME_DIR = COLLAB_DIR / "runtime"
EVENTS_DIR = RUNTIME_DIR / "events"

SESSION_RE = re.compile(r"^[A-Za-z0-9._-]+$")
TASK_ID_RE = re.compile(r"^T\d{3,}$")
FIELD_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*[：:]\s*`(?P<value>[^`]+)`")
VALUE_FIELD_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*[：:]\s*(?P<value>.*)$")
CASE_LEAD_RE = re.compile(
    r"^- \*\*主導代理人 \(Lead Session\)\*\*[：:]\s*`(?P<value>[^`]+)`"
)

VALID_TASK_TYPES = {"DISCOVERY", "TRIAGE", "VERIFY", "REVERSE", "REVIEW"}
VALID_EVENT_KINDS = {
    "DISPATCHED",
    "ACK",
    "START",
    "DONE",
    "ERROR",
    "QUESTION",
    "REPLY",
    "NOTE",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_timestamp() -> str:
    return utc_now().isoformat(timespec="milliseconds").replace("+00:00", "Z")


def validate_session(session: str) -> None:
    if not SESSION_RE.fullmatch(session):
        raise ValueError(
            "session 只允許英數、點、底線與連字號，避免 runtime/event 路徑混淆"
        )


def validate_task_id(task_id: str) -> None:
    if not TASK_ID_RE.fullmatch(task_id):
        raise ValueError("Task ID 必須使用 T001、T002 這類格式")


def relative_posix(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def atomic_write_text(path: Path, text: str) -> None:
    """Write text atomically in the destination directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    try:
        temp.write_text(text, encoding="utf-8")
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def parse_task_metadata(task_path: Path) -> dict[str, str]:
    """Return normalized governed metadata from one task file."""
    fields: dict[str, str] = {}
    for line in task_path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.match(line.strip())
        if match:
            fields[match.group("label").strip()] = match.group("value").strip()

    task_type = fields.get("任務類型") or fields.get("Task Type")
    return {
        "case_id": fields.get("所屬大題", ""),
        "questions": fields.get("關聯小題", ""),
        "task_type": task_type or "",
        "target_role": fields.get("Target Role", ""),
        "assignee_session": fields.get("Assignee Session", ""),
        "issuer_session": fields.get("發起 Session", ""),
        "task_id": fields.get("Task ID", ""),
    }


def validate_task_metadata(task_path: Path, metadata: dict[str, str] | None = None) -> list[str]:
    metadata = metadata or parse_task_metadata(task_path)
    errors: list[str] = []

    required = {
        "case_id": "所屬大題",
        "task_type": "任務類型",
        "target_role": "Target Role",
        "assignee_session": "Assignee Session",
        "issuer_session": "發起 Session",
        "task_id": "Task ID",
    }
    for key, label in required.items():
        if not metadata.get(key):
            errors.append(f"missing {label}")

    if metadata.get("task_type") and metadata["task_type"] not in VALID_TASK_TYPES:
        errors.append(f"invalid task type: {metadata['task_type']}")
    if metadata.get("task_id") and not TASK_ID_RE.fullmatch(metadata["task_id"]):
        errors.append(f"invalid Task ID: {metadata['task_id']}")
    for key in ("assignee_session", "issuer_session"):
        value = metadata.get(key)
        if value and not SESSION_RE.fullmatch(value):
            errors.append(f"invalid {key}: {value}")

    expected_case = task_path.parent.parent.name
    if metadata.get("case_id") and metadata["case_id"] != expected_case:
        errors.append(
            f"case mismatch: metadata={metadata['case_id']} path={expected_case}"
        )
    return errors


def case_dir(case_id: str, cases_dir: Path | None = None) -> Path:
    cases_dir = cases_dir or CASES_DIR
    target = cases_dir / case_id
    if not target.is_dir() or case_id == "C00_Template":
        raise ValueError(f"unknown live case: {case_id}")
    return target


def get_case_lead(case_id: str, cases_dir: Path | None = None) -> str | None:
    cases_dir = cases_dir or CASES_DIR
    state_path = case_dir(case_id, cases_dir) / "CASE_STATE.md"
    for line in state_path.read_text(encoding="utf-8").splitlines():
        match = CASE_LEAD_RE.match(line.strip())
        if match:
            value = match.group("value").strip()
            return value if SESSION_RE.fullmatch(value) else None
    return None


def iter_tasks(cases_dir: Path | None = None, case_filters: set[str] | None = None):
    cases_dir = cases_dir or CASES_DIR
    if not cases_dir.exists():
        return
    for current_case in sorted(path for path in cases_dir.iterdir() if path.is_dir()):
        if current_case.name == "C00_Template":
            continue
        if case_filters and current_case.name not in case_filters:
            continue
        tasks_dir = current_case / "tasks"
        if not tasks_dir.is_dir():
            continue
        for task_path in sorted(tasks_dir.glob("*.md")):
            upper_name = task_path.name.upper()
            if upper_name.startswith("README") or "TEMPLATE" in upper_name:
                continue
            yield task_path


def discover_assigned_tasks(
    cases_dir: Path,
    session: str,
    case_filters: set[str] | None = None,
) -> list[tuple[Path, dict[str, str]]]:
    validate_session(session)
    assigned: list[tuple[Path, dict[str, str]]] = []
    for task_path in iter_tasks(cases_dir, case_filters) or []:
        metadata = parse_task_metadata(task_path)
        if metadata["assignee_session"] != session:
            continue
        errors = validate_task_metadata(task_path, metadata)
        if errors:
            raise ValueError(f"invalid assigned task {task_path}: {'; '.join(errors)}")
        assigned.append((task_path, metadata))
    return assigned


def find_task(
    case_id: str,
    task_id: str,
    cases_dir: Path | None = None,
) -> tuple[Path, dict[str, str]]:
    cases_dir = cases_dir or CASES_DIR
    validate_task_id(task_id)
    matches: list[tuple[Path, dict[str, str]]] = []
    for task_path in iter_tasks(cases_dir, {case_id}) or []:
        metadata = parse_task_metadata(task_path)
        if metadata["task_id"] == task_id:
            matches.append((task_path, metadata))
    if not matches:
        raise ValueError(f"task not found: {case_id}/{task_id}")
    if len(matches) != 1:
        raise ValueError(f"duplicate Task ID in {case_id}: {task_id}")
    task_path, metadata = matches[0]
    errors = validate_task_metadata(task_path, metadata)
    if errors:
        raise ValueError(f"invalid task {task_path}: {'; '.join(errors)}")
    return task_path, metadata


def output_path_for_task(task_path: Path, metadata: dict[str, str]) -> Path:
    current_case = task_path.parent.parent
    task_id = metadata["task_id"]
    if metadata["task_type"] == "REVIEW":
        return current_case / "reviews" / f"REVIEW_{task_id}.md"
    return current_case / "findings" / f"FINDING_{task_id}.md"


def parse_markdown_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = VALUE_FIELD_RE.match(line.strip())
        if not match:
            continue
        value = match.group("value").strip()
        if value.startswith("`") and value.endswith("`") and len(value) >= 2:
            value = value[1:-1]
        fields[match.group("label").strip()] = value.strip()
    return fields


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().upper()
    return not normalized or normalized in {"TODO", "TBD", "-"} or "YYYY-MM-DD" in normalized


def validate_governed_output(
    task_path: Path,
    metadata: dict[str, str],
    output_path: Path,
) -> list[str]:
    """Validate that a finding/review is substantively ready for DONE."""
    errors: list[str] = []
    if not output_path.exists():
        return ["governed output does not exist"]

    fields = parse_markdown_fields(output_path)
    if metadata["task_type"] == "REVIEW":
        expected = {
            "對應 Task": metadata["task_id"],
            "Reviewer Session": metadata["assignee_session"],
        }
        for label, expected_value in expected.items():
            if fields.get(label) != expected_value:
                errors.append(f"{label} must equal {expected_value}")
        if fields.get("Verdict") not in {"APPROVED", "CHALLENGED"}:
            errors.append("Verdict must be APPROVED or CHALLENGED")
        if fields.get("可支持答案狀態") not in {"CANDIDATE", "VERIFIED"}:
            errors.append("可支持答案狀態 must be CANDIDATE or VERIFIED")
        for label in ("完成時間", "重現結果", "時間與因果", "替代解釋 / False Positive", "格式檢查"):
            if _is_placeholder(fields.get(label, "")):
                errors.append(f"{label} is incomplete")
    else:
        expected = {
            "對應任務": metadata["task_id"],
            "解答 Session": metadata["assignee_session"],
        }
        for label, expected_value in expected.items():
            if fields.get(label) != expected_value:
                errors.append(f"{label} must equal {expected_value}")
        if fields.get("Confidence") not in {"LOW", "MEDIUM", "HIGH"}:
            errors.append("Confidence must be LOW, MEDIUM, or HIGH")
        for label in (
            "完成時間",
            "Answer / Conclusion",
            "Artifact / Source",
            "取得方法 / Tool",
            "Direct Observation",
            "Reproduction",
            "Known Limitations",
        ):
            if _is_placeholder(fields.get(label, "")):
                errors.append(f"{label} is incomplete")
        if fields.get("建議答案狀態") not in {"CANDIDATE", "VERIFIED"}:
            errors.append("建議答案狀態 must be CANDIDATE or VERIFIED")
        if fields.get("需要額外 review") not in {"YES", "NO"}:
            errors.append("需要額外 review must be YES or NO")

    return errors


def event_dir(case_id: str, task_id: str, events_dir: Path | None = None) -> Path:
    events_dir = events_dir or EVENTS_DIR
    validate_task_id(task_id)
    return events_dir / case_id / task_id


def emit_event(
    *,
    kind: str,
    case_id: str,
    task_id: str,
    from_session: str,
    to_session: str,
    message: str = "",
    task_path: Path | None = None,
    output_path: Path | None = None,
    events_dir: Path | None = None,
) -> Path:
    kind = kind.upper()
    if kind not in VALID_EVENT_KINDS:
        raise ValueError(f"invalid event kind: {kind}")
    validate_session(from_session)
    validate_session(to_session)
    validate_task_id(task_id)

    event_id = uuid.uuid4().hex
    timestamp = utc_timestamp()
    created_ns = time.time_ns()
    payload = {
        "schema": "collab-event/v1",
        "event_id": event_id,
        "created_ns": created_ns,
        "timestamp_utc": timestamp,
        "kind": kind,
        "case_id": case_id,
        "task_id": task_id,
        "from_session": from_session,
        "to_session": to_session,
        "message": message,
    }
    if task_path is not None:
        payload["task_path"] = relative_posix(task_path)
        payload["task_sha256"] = sha256_file(task_path)
    if output_path is not None:
        payload["output_path"] = relative_posix(output_path)
        if output_path.exists():
            payload["output_sha256"] = sha256_file(output_path)

    events_dir = events_dir or EVENTS_DIR
    target_dir = event_dir(case_id, task_id, events_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{created_ns:020d}_{kind}_{from_session}_{event_id[:8]}.json"
    atomic_write_text(target, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return target


def iter_events(events_dir: Path | None = None):
    events_dir = events_dir or EVENTS_DIR
    if not events_dir.exists():
        return
    for event_path in sorted(events_dir.glob("*/*/*.json")):
        try:
            payload = json.loads(event_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == "collab-event/v1":
            yield event_path, payload


def events_for_task(
    case_id: str,
    task_id: str,
    events_dir: Path | None = None,
) -> list[tuple[Path, dict]]:
    events_dir = events_dir or EVENTS_DIR
    results: list[tuple[Path, dict]] = []
    target_dir = event_dir(case_id, task_id, events_dir)
    if not target_dir.exists():
        return results
    for event_path in sorted(target_dir.glob("*.json")):
        try:
            payload = json.loads(event_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == "collab-event/v1":
            results.append((event_path, payload))
    return results


def incoming_events(
    session: str,
    events_dir: Path | None = None,
) -> list[tuple[Path, dict]]:
    events_dir = events_dir or EVENTS_DIR
    validate_session(session)
    results = [
        (path, payload)
        for path, payload in (iter_events(events_dir) or [])
        if payload.get("to_session") == session
    ]
    return sorted(results, key=lambda item: int(item[1].get("created_ns", 0)))


def latest_task_state(
    case_id: str,
    task_id: str,
    events_dir: Path | None = None,
) -> str:
    events_dir = events_dir or EVENTS_DIR
    events = events_for_task(case_id, task_id, events_dir)
    lifecycle = [
        payload.get("kind")
        for _, payload in events
        if payload.get("kind") in {"DISPATCHED", "ACK", "START", "DONE", "ERROR"}
    ]
    return lifecycle[-1] if lifecycle else "DISPATCHED"


def first_task_hash_from_events(
    case_id: str,
    task_id: str,
    events_dir: Path | None = None,
) -> str | None:
    events_dir = events_dir or EVENTS_DIR
    for _, payload in events_for_task(case_id, task_id, events_dir):
        value = payload.get("task_sha256")
        if isinstance(value, str) and value:
            return value
    return None
