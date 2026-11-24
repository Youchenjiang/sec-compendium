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
INBOX_DIR = RUNTIME_DIR / "inbox"

SESSION_RE = re.compile(r"^[A-Za-z0-9._-]+$")
TASK_ID_RE = re.compile(r"^T\d{3,}$")
FINDING_ID_RE = re.compile(r"^FINDING_T\d{3,}$")
FIELD_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*[：:]\s*`(?P<value>[^`]+)`")
# ``value`` is always ``.strip()``-ed by callers, so no leading ``\s*`` is needed
# (dropping it removes the ``\s*``/``.*`` overlap that caused backtracking).
VALUE_FIELD_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*[：:](?P<value>.*)$")
CASE_LEAD_RE = re.compile(
    r"^- \*\*主導代理人 \(Lead Session\)\*\*[：:]\s*`(?P<value>[^`]+)`"
)

# Cloud-sync engines (Google Drive / Dropbox / OneDrive) create sibling copies when
# the same path is written from two hosts. Those copies are never governed artifacts.
# Match the trailing parenthetical (before an optional extension); the
# "conflicted copy" marker is checked on the captured text to avoid backtracking.
SYNC_CONFLICT_RE = re.compile(r"\s\((?P<note>[^)]*)\)(?=(?:\.[^.]+)?$)")
SYNC_CONFLICT_MARKER = "conflicted copy"
EVENT_SCHEMA = "collab-event/v1"

VALID_TASK_TYPES = {"DISCOVERY", "TRIAGE", "VERIFY", "REVERSE", "REVIEW"}
VALID_EXECUTION_ENVIRONMENTS = {"host_local_gateway", "portable_text_any"}
VALID_EXECUTION_PROFILES = {"governed", "race"}
LANE_ID_RE = re.compile(r"^L\d{2,}$", re.IGNORECASE)
LEGACY_EXECUTION_ENVIRONMENT = "legacy_unspecified"
CURRENT_TASK_CONTRACT = "v2.3"
TERMINAL_TASK_STATES = {"DONE", "ERROR"}
VALID_EVENT_KINDS = {
    "DISPATCHED",
    "DISPATCH_FAILED",
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
        "protocol_contract": fields.get("Protocol Contract", ""),
        "target_role": fields.get("Target Role", ""),
        "assignee_session": fields.get("Assignee Session", ""),
        "issuer_session": fields.get("發起 Session", ""),
        "execution_environment": fields.get("執行環境", "") or fields.get("Execution Environment", ""),
        "execution_profile": fields.get("Execution Profile", "") or "governed",
        "lane_id": fields.get("Lane ID", ""),
        "review_target_finding": fields.get("Review Target Finding", ""),
        "task_id": fields.get("Task ID", ""),
    }


def _execution_profile_errors(metadata: dict[str, str]) -> list[str]:
    errors: list[str] = []
    execution_profile = metadata.get("execution_profile", "governed") or "governed"
    lane_id = metadata.get("lane_id", "")
    if execution_profile not in VALID_EXECUTION_PROFILES:
        errors.append(f"invalid execution profile: {execution_profile}")
    if execution_profile == "race":
        if not lane_id:
            errors.append("race task missing Lane ID")
        elif not LANE_ID_RE.fullmatch(lane_id):
            errors.append(f"invalid Lane ID: {lane_id}")
        if metadata.get("task_type") == "REVIEW":
            errors.append("REVIEW tasks are not race lanes")
    elif lane_id:
        errors.append("Lane ID is only valid for race tasks")
    return errors


def _contract_errors(
    contract: str, execution_environment: str, allow_legacy: bool
) -> list[str]:
    errors: list[str] = []
    if not contract and not allow_legacy:
        errors.append("missing Protocol Contract")
    if contract and contract != CURRENT_TASK_CONTRACT:
        errors.append(f"unsupported Protocol Contract: {contract}")
    if contract == CURRENT_TASK_CONTRACT and not execution_environment:
        errors.append("missing 執行環境")
    if execution_environment and execution_environment not in VALID_EXECUTION_ENVIRONMENTS:
        errors.append(f"invalid execution environment: {execution_environment}")
    return errors


def _review_target_errors(
    task_path: Path, metadata: dict[str, str], contract: str
) -> list[str]:
    review_target_finding = metadata.get("review_target_finding", "")
    if metadata.get("task_type") != "REVIEW":
        if review_target_finding:
            return ["Review Target Finding is only valid for REVIEW tasks"]
        return []
    errors: list[str] = []
    if contract == CURRENT_TASK_CONTRACT and not review_target_finding:
        errors.append("missing Review Target Finding")
    if review_target_finding and not FINDING_ID_RE.fullmatch(review_target_finding):
        errors.append(f"invalid Review Target Finding: {review_target_finding}")
    if review_target_finding:
        finding_path = task_path.parent.parent / "findings" / f"{review_target_finding}.md"
        if not finding_path.is_file():
            errors.append(f"review target finding does not exist: {review_target_finding}")
    return errors


def validate_task_metadata(
    task_path: Path,
    metadata: dict[str, str] | None = None,
    *,
    allow_legacy: bool = False,
) -> list[str]:
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
    contract = metadata.get("protocol_contract", "")
    errors.extend(_execution_profile_errors(metadata))
    errors.extend(
        _contract_errors(contract, metadata.get("execution_environment", ""), allow_legacy)
    )
    errors.extend(_review_target_errors(task_path, metadata, contract))
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
        yield from _case_task_files(current_case / "tasks")


def _case_task_files(tasks_dir: Path):
    if not tasks_dir.is_dir():
        return
    for task_path in sorted(tasks_dir.glob("*.md")):
        upper_name = task_path.name.upper()
        if upper_name.startswith("README") or "TEMPLATE" in upper_name:
            continue
        yield task_path


def discover_assigned_tasks(
    cases_dir: Path,
    session: str,
    case_filters: set[str] | None = None,
    events_dir: Path | None = None,
) -> list[tuple[Path, dict[str, str]]]:
    validate_session(session)
    assigned: list[tuple[Path, dict[str, str]]] = []
    for task_path in iter_tasks(cases_dir, case_filters) or []:
        metadata = parse_task_metadata(task_path)
        if metadata["assignee_session"] != session:
            continue
        anchor_errors = validate_task_dispatch_anchor(
            task_path, metadata, events_dir=events_dir
        )
        allow_legacy = not metadata.get("protocol_contract") and not anchor_errors
        errors = validate_task_metadata(
            task_path, metadata, allow_legacy=allow_legacy
        )
        errors.extend(anchor_errors)
        if metadata.get("task_type") == "REVIEW" and metadata.get(
            "review_target_finding"
        ):
            errors.extend(
                validate_finding_provenance(
                    metadata["case_id"],
                    metadata["review_target_finding"],
                    cases_dir=cases_dir,
                    events_dir=events_dir,
                )
            )
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
    # Retrieval supports already-published pre-v2.3 tasks. Mutating/dispatching
    # callers must additionally require the canonical DISPATCHED anchor.
    errors = validate_task_metadata(task_path, metadata, allow_legacy=True)
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


def _mismatched_fields(fields: dict[str, str], expected: dict[str, str]) -> list[str]:
    return [
        f"{label} must equal {expected_value}"
        for label, expected_value in expected.items()
        if fields.get(label) != expected_value
    ]


def _incomplete_fields(fields: dict[str, str], labels: tuple[str, ...]) -> list[str]:
    return [
        f"{label} is incomplete"
        for label in labels
        if _is_placeholder(fields.get(label, ""))
    ]


def _review_output_errors(fields: dict[str, str], metadata: dict[str, str]) -> list[str]:
    errors = _mismatched_fields(
        fields,
        {
            "對應 Task": metadata["task_id"],
            "對應 Finding": metadata.get("review_target_finding", ""),
            "Reviewer Session": metadata["assignee_session"],
        },
    )
    if fields.get("Verdict") not in {"APPROVED", "CHALLENGED"}:
        errors.append("Verdict must be APPROVED or CHALLENGED")
    if fields.get("可支持答案狀態") not in {"CANDIDATE", "VERIFIED"}:
        errors.append("可支持答案狀態 must be CANDIDATE or VERIFIED")
    errors.extend(
        _incomplete_fields(
            fields,
            ("完成時間", "重現結果", "時間與因果", "替代解釋 / False Positive", "格式檢查"),
        )
    )
    return errors


def _finding_output_errors(fields: dict[str, str], metadata: dict[str, str]) -> list[str]:
    errors = _mismatched_fields(
        fields,
        {
            "對應任務": metadata["task_id"],
            "解答 Session": metadata["assignee_session"],
        },
    )
    if fields.get("Confidence") not in {"LOW", "MEDIUM", "HIGH"}:
        errors.append("Confidence must be LOW, MEDIUM, or HIGH")
    errors.extend(
        _incomplete_fields(
            fields,
            (
                "完成時間",
                "Answer / Conclusion",
                "Artifact / Source",
                "取得方法 / Tool",
                "Direct Observation",
                "Reproduction",
                "Known Limitations",
            ),
        )
    )
    if fields.get("建議答案狀態") not in {"CANDIDATE", "VERIFIED"}:
        errors.append("建議答案狀態 must be CANDIDATE or VERIFIED")
    if fields.get("需要額外 review") not in {"YES", "NO"}:
        errors.append("需要額外 review must be YES or NO")
    return errors


def validate_governed_output(
    metadata: dict[str, str],
    output_path: Path,
) -> list[str]:
    """Validate that a finding/review is substantively ready for DONE."""
    if not output_path.exists():
        return ["governed output does not exist"]

    fields = parse_markdown_fields(output_path)
    if metadata["task_type"] == "REVIEW":
        return _review_output_errors(fields, metadata)
    return _finding_output_errors(fields, metadata)


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
        "schema": EVENT_SCHEMA,
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
        if is_sync_artifact(event_path):
            continue
        try:
            payload = json.loads(event_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == EVENT_SCHEMA:
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
        if is_sync_artifact(event_path):
            continue
        try:
            payload = json.loads(event_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == EVENT_SCHEMA:
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


def is_sync_artifact(path: Path) -> bool:
    """True when a runtime filename is a cloud-sync duplicate/partial, not real data.

    The governed runtime lives under a cloud-synced tree, so the sync engine may
    emit ``X (conflicted copy).json``, dotfile temp fragments, or editor backups.
    Readers must never treat those as events or handoffs.
    """
    name = path.name
    if name.startswith(".") or name.endswith("~"):
        return True
    match = SYNC_CONFLICT_RE.search(name)
    return bool(match) and SYNC_CONFLICT_MARKER in match.group("note").casefold()


def iter_sync_artifacts(*roots: Path):
    """Yield cloud-sync duplicate/partial files found below the given roots."""
    for root in roots:
        if not root.exists():
            continue
        for candidate in sorted(root.rglob("*")):
            if candidate.is_file() and is_sync_artifact(candidate):
                yield candidate


def handoff_dir(session: str, inbox_dir: Path | None = None) -> Path:
    """Return the Git-ignored inbox directory for one worker session."""
    validate_session(session)
    return (inbox_dir or INBOX_DIR) / session


def write_handoff(
    *,
    session: str,
    case_id: str,
    task_id: str,
    task_type: str,
    execution_environment: str,
    current_state: str,
    task_path: Path,
    output_path: Path,
    instruction: str,
    reason: str,
    transport: str,
    lead_session: str | None,
    execution_profile: str = "governed",
    lane_id: str = "",
    inbox_dir: Path | None = None,
) -> Path:
    """Persist a durable, browser-free handoff packet for one assigned task.

    The packet is the pure file/CLI fallback transport: any worker (agent or
    human) that can read the repo can pick it up without an interactive
    composer/browser, and replay the exact governed commands to finish the task.
    """
    validate_session(session)
    validate_task_id(task_id)
    if execution_environment not in VALID_EXECUTION_ENVIRONMENTS | {LEGACY_EXECUTION_ENVIRONMENT}:
        raise ValueError(f"invalid execution environment: {execution_environment}")
    task_sha256 = sha256_file(task_path)
    if current_state in TERMINAL_TASK_STATES:
        raise ValueError(f"cannot write handoff for terminal task state: {current_state}")
    commands: list[str] = []
    if current_state == "ACK":
        commands.append(
            f"python security/tools/collab_bus.py start --case {case_id} "
            f"--task-id {task_id} --session {session}"
        )
    elif current_state != "START":
        raise ValueError(f"handoff requires ACK or START state, got: {current_state}")
    if not output_path.exists():
        commands.append(
            f"python security/tools/collab_bus.py init-output --case {case_id} "
            f"--task-id {task_id} --session {session}"
        )
    ready_message = "review ready" if task_type == "REVIEW" else "finding ready"
    commands.append(
        f"python security/tools/collab_bus.py done --case {case_id} "
        f"--task-id {task_id} --session {session} --message \"{ready_message}\""
    )
    payload = {
        "schema": "collab-handoff/v1",
        "created_utc": utc_timestamp(),
        "session": session,
        "case_id": case_id,
        "task_id": task_id,
        "task_type": task_type,
        "execution_environment": execution_environment,
        "execution_profile": execution_profile,
        "lane_id": lane_id,
        "task_state": current_state,
        "task_path": relative_posix(task_path),
        "task_sha256": task_sha256,
        "output_path": relative_posix(output_path),
        "lead_session": lead_session,
        "reason": reason,
        "transport": transport,
        "instruction": instruction,
        "required_commands": commands,
    }
    target = handoff_dir(session, inbox_dir) / case_id / f"{task_id}.json"
    atomic_write_text(target, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return target


def iter_handoffs(session: str, inbox_dir: Path | None = None):
    """Yield ``(path, payload)`` for every durable handoff queued for a session."""
    base = handoff_dir(session, inbox_dir)
    if not base.exists():
        return
    for handoff_path in sorted(base.glob("*/*.json")):
        if is_sync_artifact(handoff_path):
            continue
        try:
            payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == "collab-handoff/v1":
            yield handoff_path, payload


def consume_handoff(handoff_path: Path) -> None:
    """Remove a resolved handoff packet (best effort)."""
    handoff_path.unlink(missing_ok=True)


def handoff_path_for_task(
    session: str,
    case_id: str,
    task_id: str,
    inbox_dir: Path | None = None,
) -> Path:
    validate_session(session)
    validate_task_id(task_id)
    return handoff_dir(session, inbox_dir) / case_id / f"{task_id}.json"


def lifecycle_transition_error(current_state: str, next_kind: str) -> str | None:
    """Return an error for an invalid worker lifecycle transition."""
    next_kind = next_kind.upper()
    if current_state in TERMINAL_TASK_STATES:
        return f"task 已是 terminal state {current_state}，不可再送 {next_kind}"

    allowed_from = {
        "ACK": {"DISPATCHED", "DISPATCH_FAILED"},
        "START": {"ACK"},
        "DONE": {"START"},
        "ERROR": {"ACK", "START"},
    }
    if next_kind not in allowed_from:
        return None
    if current_state not in allowed_from[next_kind]:
        expected = "/".join(sorted(allowed_from[next_kind]))
        return f"{next_kind} 前必須為 {expected}；current={current_state}"
    return None


def task_state_from_event_payloads(payloads: list[dict]) -> str:
    """Resolve task lifecycle state without trusting cross-host wall-clock order."""
    kinds = {payload.get("kind") for payload in payloads}
    for state in ("DONE", "ERROR", "START", "ACK", "DISPATCH_FAILED", "DISPATCHED"):
        if state in kinds:
            return state
    return "DISPATCHED"


def validate_lifecycle_events(payloads: list[dict]) -> list[str]:
    """Validate lifecycle invariants without assuming clocks are synchronized."""
    lifecycle_kinds = ("DISPATCHED", "DISPATCH_FAILED", "ACK", "START", "DONE", "ERROR")
    counts = {
        kind: sum(1 for payload in payloads if payload.get("kind") == kind)
        for kind in lifecycle_kinds
    }
    errors: list[str] = []
    if counts["DISPATCHED"] != 1:
        errors.append(f"expected exactly one DISPATCHED event, got {counts['DISPATCHED']}")
    for kind in ("DISPATCH_FAILED", "ACK", "START", "DONE", "ERROR"):
        if counts[kind] > 1:
            errors.append(f"duplicate {kind} events: {counts[kind]}")
    if counts["START"] and not counts["ACK"]:
        errors.append("START exists without ACK")
    if counts["DONE"] and not counts["START"]:
        errors.append("DONE exists without START")
    if counts["ERROR"] and not counts["ACK"]:
        errors.append("ERROR exists without ACK")
    if counts["DONE"] and counts["ERROR"]:
        errors.append("conflicting terminal events: DONE and ERROR")
    return errors


def _anchored_path_errors(kind: str, anchored_path: str, output_path: Path) -> list[str]:
    try:
        current_rel = relative_posix(output_path)
    except ValueError:
        current_rel = output_path.as_posix()
    if anchored_path != current_rel:
        return [f"{kind} output path mismatch: event={anchored_path} current={current_rel}"]
    return []


def _anchored_hash_errors(
    kind: str, anchored_hash: str, output_path: Path, task_ref: str
) -> list[str]:
    if not output_path.is_file():
        return [f"{kind} anchored governed output is missing: {output_path}"]
    current_hash = sha256_file(output_path)
    if current_hash != anchored_hash:
        return [
            f"terminal output hash 已改變: {task_ref} "
            f"event={anchored_hash} current={current_hash}"
        ]
    return []


def validate_terminal_output_anchor(
    task_path: Path,
    metadata: dict[str, str],
    events_dir: Path | None = None,
) -> list[str]:
    """Fail closed when a governed output drifts after DONE/ERROR.

    Terminal events content-address the governed output at the instant the task
    closes.  A later direct edit must not silently replace that evidence.
    """
    case_id = metadata.get("case_id", "")
    task_id = metadata.get("task_id", "")
    if not case_id or not task_id:
        return ["cannot validate terminal output anchor with incomplete task metadata"]

    terminal_payloads = [
        payload
        for _, payload in events_for_task(case_id, task_id, events_dir)
        if payload.get("kind") in TERMINAL_TASK_STATES
    ]
    if not terminal_payloads:
        return []
    if len(terminal_payloads) != 1:
        return [f"expected exactly one terminal event, got {len(terminal_payloads)}"]

    payload = terminal_payloads[0]
    kind = payload.get("kind", "terminal")
    output_path = output_path_for_task(task_path, metadata)
    anchored_hash = payload.get("output_sha256")
    anchored_path = payload.get("output_path")

    if anchored_path:
        path_errors = _anchored_path_errors(kind, anchored_path, output_path)
        if path_errors:
            return path_errors

    if anchored_hash:
        return _anchored_hash_errors(
            kind, anchored_hash, output_path, f"{case_id}/{task_id}"
        )

    if kind == "DONE":
        return ["DONE event missing output_sha256 anchor"]
    if output_path.exists():
        return [
            f"governed output appeared after terminal {kind} without an output hash anchor"
        ]
    return []


def validate_finding_provenance(
    case_id: str,
    finding_id: str,
    cases_dir: Path | None = None,
    events_dir: Path | None = None,
) -> list[str]:
    """Validate that a review target is the exact output anchored by DONE."""
    if not FINDING_ID_RE.fullmatch(finding_id):
        return [f"invalid finding id: {finding_id}"]
    task_id = finding_id.removeprefix("FINDING_")
    try:
        source_task, source_metadata = find_task(case_id, task_id, cases_dir)
    except ValueError as exc:
        return [f"review target source task invalid: {exc}"]

    if source_metadata.get("task_type") == "REVIEW":
        return [f"review target must originate from a finding task: {finding_id}"]

    errors = validate_task_dispatch_anchor(
        source_task, source_metadata, events_dir=events_dir
    )
    state = latest_task_state(case_id, task_id, events_dir)
    if state != "DONE":
        errors.append(f"review target source task is not DONE: {case_id}/{task_id} state={state}")

    expected_output = output_path_for_task(source_task, source_metadata)
    expected_target = source_task.parent.parent / "findings" / f"{finding_id}.md"
    if expected_output.resolve() != expected_target.resolve():
        errors.append(
            f"review target path mismatch: source output={expected_output} target={expected_target}"
        )
    errors.extend(
        validate_terminal_output_anchor(
            source_task, source_metadata, events_dir=events_dir
        )
    )
    return errors


def require_finding_provenance(
    case_id: str,
    finding_id: str,
    cases_dir: Path | None = None,
    events_dir: Path | None = None,
) -> None:
    errors = validate_finding_provenance(
        case_id, finding_id, cases_dir=cases_dir, events_dir=events_dir
    )
    if errors:
        raise ValueError("; ".join(errors))


def latest_task_state(
    case_id: str,
    task_id: str,
    events_dir: Path | None = None,
) -> str:
    events_dir = events_dir or EVENTS_DIR
    payloads = [
        payload for _, payload in events_for_task(case_id, task_id, events_dir)
    ]
    return task_state_from_event_payloads(payloads)


def first_task_hash_from_events(
    case_id: str,
    task_id: str,
    events_dir: Path | None = None,
    expected_issuer: str | None = None,
) -> str | None:
    events_dir = events_dir or EVENTS_DIR
    dispatched = [
        payload
        for _, payload in events_for_task(case_id, task_id, events_dir)
        if payload.get("kind") == "DISPATCHED"
    ]
    if len(dispatched) > 1:
        raise ValueError(f"multiple DISPATCHED events: {case_id}/{task_id}")
    if not dispatched:
        return None
    payload = dispatched[0]
    if expected_issuer is not None and payload.get("from_session") != expected_issuer:
        raise ValueError(
            f"DISPATCHED issuer mismatch: event={payload.get('from_session')} "
            f"task={expected_issuer}"
        )
    value = payload.get("task_sha256")
    return value if isinstance(value, str) and value else None


def validate_task_dispatch_anchor(
    task_path: Path,
    metadata: dict[str, str],
    events_dir: Path | None = None,
) -> list[str]:
    """Validate the canonical DISPATCHED event before trusting task contents."""
    case_id = metadata.get("case_id", "")
    task_id = metadata.get("task_id", "")
    issuer = metadata.get("issuer_session", "")
    if not case_id or not task_id or not issuer:
        return ["cannot validate DISPATCHED anchor with incomplete task metadata"]
    try:
        anchored_hash = first_task_hash_from_events(
            case_id,
            task_id,
            events_dir=events_dir,
            expected_issuer=issuer,
        )
    except ValueError as exc:
        return [str(exc)]
    if not anchored_hash:
        return ["missing canonical DISPATCHED anchor"]
    current_hash = sha256_file(task_path)
    if current_hash != anchored_hash:
        return ["immutable task hash 已改變；與 canonical DISPATCHED anchor 不一致"]
    return []


def require_task_dispatch_anchor(
    task_path: Path,
    metadata: dict[str, str],
    events_dir: Path | None = None,
) -> None:
    errors = validate_task_dispatch_anchor(task_path, metadata, events_dir)
    if errors:
        raise ValueError("; ".join(errors))
