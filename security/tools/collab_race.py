#!/usr/bin/env python3
"""Race-mode orchestration for the .collab case bus.

Race mode deliberately reuses governed tasks for durable worker assignment while
moving answer readiness onto a separate append-only event stream.  A worker can
publish useful answers before its governed task reaches DONE, so ACK/START/DONE
remain audit signals instead of the scoring critical path.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import collab_bus
import collab_protocol as protocol

RACE_DIR = protocol.RUNTIME_DIR / "race"
RACE_SCHEMA = "collab-race-event/v1"
QUESTION_RE = re.compile(r"^Q\d{2,}$", re.IGNORECASE)
LANE_RE = re.compile(r"^L\d{2,}$", re.IGNORECASE)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
ANSWER_STATES = {"CANDIDATE", "READY"}
CONTROL_STATES = {"SUBMITTED", "ACCEPTED", "REJECTED"}
RACE_EVENT_KINDS = {
    "PREFLIGHT_PASSED",
    "PREFLIGHT_FAILED",
    "SESSION_OPEN",
    "LANE_DISPATCHED",
    "LANE_ASSISTED",
    "ANSWER_CANDIDATE",
    "ANSWER_READY",
    "ANSWER_WITHDRAWN",
    "ANSWER_SUBMITTED",
    "ANSWER_ACCEPTED",
    "ANSWER_REJECTED",
    "SESSION_CLOSED",
    "NOTE",
}


def _race_case_dir(case_id: str, race_dir: Path | None = None) -> Path:
    return (race_dir or RACE_DIR) / case_id


def _event_dir(case_id: str, race_dir: Path | None = None) -> Path:
    return _race_case_dir(case_id, race_dir) / "events"


def _write_event(
    *,
    kind: str,
    case_id: str,
    actor_session: str,
    data: dict | None = None,
    race_dir: Path | None = None,
) -> Path:
    kind = kind.upper()
    if kind not in RACE_EVENT_KINDS:
        raise ValueError(f"invalid race event kind: {kind}")
    protocol.validate_session(actor_session)
    protocol.case_dir(case_id)
    event_id = uuid.uuid4().hex
    created_ns = time.time_ns()
    payload = {
        "schema": RACE_SCHEMA,
        "event_id": event_id,
        "created_ns": created_ns,
        "timestamp_utc": protocol.utc_timestamp(),
        "kind": kind,
        "case_id": case_id,
        "actor_session": actor_session,
        "data": data or {},
    }
    target_dir = _event_dir(case_id, race_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{created_ns:020d}_{kind}_{actor_session}_{event_id[:8]}.json"
    protocol.atomic_write_text(target, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return target


def iter_race_events(case_id: str, race_dir: Path | None = None) -> list[tuple[Path, dict]]:
    target_dir = _event_dir(case_id, race_dir)
    if not target_dir.exists():
        return []
    rows: list[tuple[Path, dict]] = []
    for path in target_dir.glob("*.json"):
        if protocol.is_sync_artifact(path):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == RACE_SCHEMA and payload.get("case_id") == case_id:
            rows.append((path, payload))
    return sorted(rows, key=lambda row: int(row[1].get("created_ns", 0)))


def _case_lead(case_id: str, actor_session: str) -> str:
    return collab_bus.ensure_actor_is_case_lead(case_id, actor_session)


def _session_open_event(case_id: str, race_dir: Path | None = None) -> dict | None:
    opens = [p for _, p in iter_race_events(case_id, race_dir) if p.get("kind") == "SESSION_OPEN"]
    return opens[0] if opens else None


def _latest_preflight_event(case_id: str, race_dir: Path | None = None) -> dict | None:
    rows = [
        payload
        for _, payload in iter_race_events(case_id, race_dir)
        if payload.get("kind") in {"PREFLIGHT_PASSED", "PREFLIGHT_FAILED"}
    ]
    return rows[-1] if rows else None


def require_open(case_id: str, race_dir: Path | None = None) -> dict:
    event = _session_open_event(case_id, race_dir)
    if event is None:
        raise ValueError(f"race session is not open: {case_id}")
    if any(p.get("kind") == "SESSION_CLOSED" for _, p in iter_race_events(case_id, race_dir)):
        raise ValueError(f"race session is already closed: {case_id}")
    return event


def command_open(args: argparse.Namespace) -> int:
    _case_lead(args.case, args.lead_session)
    if _session_open_event(args.case) is not None:
        raise ValueError(f"race session already exists: {args.case}")
    require_dfir_preflight = bool(getattr(args, "require_dfir_preflight", False))
    if require_dfir_preflight:
        preflight = _latest_preflight_event(args.case)
        if preflight is None or preflight.get("kind") != "PREFLIGHT_PASSED":
            raise ValueError("DFIR preflight must pass before opening this race")
    worker_start_slo_seconds = int(getattr(args, "worker_start_slo_seconds", 60))
    if worker_start_slo_seconds <= 0:
        raise ValueError("worker start SLO must be positive")
    _write_event(
        kind="SESSION_OPEN",
        case_id=args.case,
        actor_session=args.lead_session,
        data={
            "budget_minutes": args.budget_minutes,
            "target_ready_ratio": args.target_ready_ratio,
            "worker_start_slo_seconds": worker_start_slo_seconds,
            "dfir_preflight_required": require_dfir_preflight,
        },
    )
    print(f"RACE OPEN {args.case} budget={args.budget_minutes}m")
    return 0


def command_preflight(args: argparse.Namespace) -> int:
    lead = _case_lead(args.case, args.lead_session)
    if _session_open_event(args.case) is not None:
        raise ValueError("DFIR preflight must run before the race clock starts")
    python_executable = str(getattr(args, "dfir_python", "") or sys.executable)
    script = Path(__file__).with_name("dfir_query.py")
    image = str(getattr(args, "image", "") or "")
    evidence_root = str(getattr(args, "evidence_root", "") or "")
    if bool(image) == bool(evidence_root):
        raise ValueError("preflight requires exactly one of --image or --evidence-root")
    source_flag, source_value = (
        ("--image", image) if image else ("--evidence-root", evidence_root)
    )
    command = [python_executable, str(script), "preflight", source_flag, source_value]
    try:
        completed = subprocess.run(
            command,
            cwd=str(protocol.REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=float(args.timeout_seconds),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        payload = {
            "ready": False,
            "python": python_executable,
            "source": source_value,
            "errors": [f"preflight timed out after {args.timeout_seconds}s"],
        }
        _write_event(
            kind="PREFLIGHT_FAILED",
            case_id=args.case,
            actor_session=lead,
            data=payload,
        )
        raise ValueError(payload["errors"][0]) from exc
    except OSError as exc:
        payload = {
            "ready": False,
            "python": python_executable,
            "source": source_value,
            "errors": [f"preflight launcher failed: {type(exc).__name__}: {exc}"],
        }
        _write_event(
            kind="PREFLIGHT_FAILED",
            case_id=args.case,
            actor_session=lead,
            data=payload,
        )
        raise ValueError(payload["errors"][0]) from exc

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        result = {
            "ready": False,
            "python": python_executable,
            "image": args.image,
            "errors": [
                "preflight returned invalid JSON",
                completed.stderr.strip() or completed.stdout.strip(),
            ],
        }
    result["launcher_python"] = python_executable
    result["exit_code"] = completed.returncode
    kind = "PREFLIGHT_PASSED" if completed.returncode == 0 and result.get("ready") else "PREFLIGHT_FAILED"
    _write_event(
        kind=kind,
        case_id=args.case,
        actor_session=lead,
        data=result,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if kind == "PREFLIGHT_PASSED" else 2


def _parse_questions(value: str) -> list[str]:
    questions = [q.strip().upper() for q in value.split(",") if q.strip()]
    if not questions:
        raise ValueError("lane requires at least one question")
    bad = [q for q in questions if not QUESTION_RE.fullmatch(q)]
    if bad:
        raise ValueError(f"invalid question id(s): {', '.join(bad)}")
    return list(dict.fromkeys(questions))


def command_lane(args: argparse.Namespace) -> int:
    require_open(args.case)
    _case_lead(args.case, args.lead_session)
    lane_id = args.lane_id.upper()
    if not LANE_RE.fullmatch(lane_id):
        raise ValueError("lane id must look like L01")
    questions = _parse_questions(args.questions)
    existing = [
        p for _, p in iter_race_events(args.case)
        if p.get("kind") == "LANE_DISPATCHED" and p.get("data", {}).get("lane_id") == lane_id
    ]
    if existing:
        raise ValueError(f"duplicate lane id: {lane_id}")

    task_args = argparse.Namespace(
        case=args.case,
        actor_session=args.lead_session,
        task_id=args.task_id,
        task_type=args.task_type,
        target_role=args.target_role,
        assignee_session=args.assignee_session,
        execution_environment=args.execution_environment,
        execution_profile="race",
        lane_id=lane_id,
        review_target_finding="",
        question=", ".join(questions),
        title=f"[{lane_id}] {args.domain}",
        objective=args.objective,
        context=(
            f"RACE MODE {lane_id}: publish each useful answer immediately with "
            f"collab_race.py answer; do not wait for task DONE.\n" + (args.context or "")
        ),
        skills=args.skills,
    )
    collab_bus.command_new_task(task_args)
    task_path, metadata = protocol.find_task(args.case, args.task_id)
    _write_event(
        kind="LANE_DISPATCHED",
        case_id=args.case,
        actor_session=args.lead_session,
        data={
            "lane_id": lane_id,
            "task_id": args.task_id,
            "task_sha256": protocol.sha256_file(task_path),
            "assignee_session": metadata["assignee_session"],
            "domain": args.domain,
            "questions": questions,
        },
    )
    if metadata["assignee_session"] == args.lead_session:
        worker_args = argparse.Namespace(
            case=args.case,
            task_id=args.task_id,
            session=args.lead_session,
            message="Race Lead self-lane auto bootstrap",
        )
        collab_bus.emit_worker_event(worker_args, "ACK")
        collab_bus.emit_worker_event(worker_args, "START")
    print(f"RACE LANE {args.case}/{lane_id} -> {args.assignee_session} questions={','.join(questions)}")
    return 0


def _lane_for_task(case_id: str, task_id: str, race_dir: Path | None = None) -> dict:
    require_open(case_id, race_dir)
    lanes = [
        p.get("data", {}) for _, p in iter_race_events(case_id, race_dir)
        if p.get("kind") == "LANE_DISPATCHED" and p.get("data", {}).get("task_id") == task_id
    ]
    if len(lanes) != 1:
        raise ValueError(f"task is not mapped to exactly one race lane: {case_id}/{task_id}")
    return lanes[0]


def _assist_events(case_id: str, task_id: str, race_dir: Path | None = None) -> list[dict]:
    return [
        payload
        for _, payload in iter_race_events(case_id, race_dir)
        if payload.get("kind") == "LANE_ASSISTED"
        and payload.get("data", {}).get("task_id") == task_id
    ]


def _latest_assist_event(
    case_id: str,
    task_id: str,
    race_dir: Path | None = None,
    *,
    before_ns: int | None = None,
) -> dict | None:
    rows = _assist_events(case_id, task_id, race_dir)
    if before_ns is not None:
        rows = [
            payload
            for payload in rows
            if int(payload.get("created_ns", 0)) < before_ns
        ]
    return rows[-1] if rows else None


def _lane_has_assist(case_id: str, task_id: str, race_dir: Path | None = None) -> bool:
    return _latest_assist_event(case_id, task_id, race_dir) is not None


def race_watchdog(
    case_id: str,
    *,
    start_slo_seconds: int | None = None,
    race_dir: Path | None = None,
    now_ns: int | None = None,
) -> list[dict]:
    opened = _session_open_event(case_id, race_dir)
    if opened is None:
        raise ValueError(f"race session does not exist: {case_id}")
    configured_slo = int(opened.get("data", {}).get("worker_start_slo_seconds", 60))
    slo = configured_slo if start_slo_seconds is None else int(start_slo_seconds)
    if slo <= 0:
        raise ValueError("worker start SLO must be positive")
    closed = next(
        (
            payload
            for _, payload in reversed(iter_race_events(case_id, race_dir))
            if payload.get("kind") == "SESSION_CLOSED"
        ),
        None,
    )
    if now_ns is not None:
        clock_ns = int(now_ns)
    elif closed:
        clock_ns = int(closed.get("created_ns"))
    else:
        clock_ns = int(time.time_ns())
    rows: list[dict] = []
    for _, event in iter_race_events(case_id, race_dir):
        if event.get("kind") != "LANE_DISPATCHED":
            continue
        data = event.get("data", {})
        task_id = data.get("task_id", "")
        starts = [
            int(payload.get("created_ns", 0))
            for _, payload in protocol.events_for_task(case_id, task_id)
            if payload.get("kind") == "START"
        ]
        dispatch_ns = int(event.get("created_ns", 0))
        first_start_ns = min(starts) if starts else None
        age_seconds = max(0.0, (clock_ns - dispatch_ns) / 1e9)
        started = first_start_ns is not None
        start_seconds = None if first_start_ns is None else (first_start_ns - dispatch_ns) / 1e9
        rows.append({
            "lane_id": data.get("lane_id", ""),
            "task_id": task_id,
            "assignee_session": data.get("assignee_session", ""),
            "started": started,
            "start_seconds_after_dispatch": start_seconds,
            "age_seconds": age_seconds,
            "overdue": (not started and age_seconds >= slo),
            "assisted": _lane_has_assist(case_id, task_id, race_dir),
            "start_slo_seconds": slo,
        })
    return rows


def _yes_no(flag: bool) -> str:
    return "YES" if flag else "NO"


def _assist_overdue_lanes(args: argparse.Namespace, overdue: list[dict]) -> None:
    if not getattr(args, "lead_session", ""):
        raise ValueError("--lead-session is required with --assist-overdue")
    require_open(args.case)
    for row in overdue:
        command_assist(argparse.Namespace(
            case=args.case,
            lead_session=args.lead_session,
            task_id=row["task_id"],
            reason=(
                f"worker START exceeded {row['start_slo_seconds']}s SLO; "
                "Lead assist enabled for cheap-pivot fallback"
            ),
        ))


def _format_watchdog_row(row: dict, assist_overdue: bool) -> str:
    start_after = row["start_seconds_after_dispatch"]
    start_s = "-" if start_after is None else f"{start_after:.3f}"
    assisted = row["assisted"] or (row["overdue"] and assist_overdue)
    return (
        f"{row['lane_id']} {row['task_id']} "
        f"{_yes_no(row['started'])} "
        f"{_yes_no(row['overdue'])} "
        f"{_yes_no(assisted)} "
        f"{row['age_seconds']:.3f} {start_s}"
    )


def command_watchdog(args: argparse.Namespace) -> int:
    start_slo = getattr(args, "start_slo_seconds", None)
    rows = race_watchdog(args.case, start_slo_seconds=start_slo)
    overdue = [row for row in rows if row["overdue"]]
    assist_overdue = bool(getattr(args, "assist_overdue", False))
    if assist_overdue:
        _assist_overdue_lanes(args, overdue)
    print("LANE TASK STARTED OVERDUE ASSISTED AGE_S START_S")
    for row in rows:
        print(_format_watchdog_row(row, assist_overdue))
    return 0


def command_assist(args: argparse.Namespace) -> int:
    require_open(args.case)
    lead = _case_lead(args.case, args.lead_session)
    lane = _lane_for_task(args.case, args.task_id)
    if _lane_has_assist(args.case, args.task_id):
        print(f"RACE ASSIST {args.case}/{lane['lane_id']} already active")
    else:
        _write_event(
            kind="LANE_ASSISTED",
            case_id=args.case,
            actor_session=lead,
            data={
                "lane_id": lane["lane_id"],
                "task_id": args.task_id,
                "assignee_session": lane["assignee_session"],
                "reason": args.reason,
            },
        )
        print(f"RACE ASSIST {args.case}/{lane['lane_id']} task={args.task_id}")
    return 0


def _secret_answer_fields(args: argparse.Namespace) -> tuple[str, dict]:
    secret_ref = str(getattr(args, "secret_ref", "") or "").strip()
    secret_sha256 = str(getattr(args, "secret_sha256", "") or "").strip().lower()
    secret_exact = bool(getattr(args, "secret_exact", False))
    secret_mode = bool(secret_ref or secret_sha256 or secret_exact)
    answer = str(getattr(args, "answer", "") or "").strip()
    if not secret_mode:
        if not answer:
            raise ValueError("answer requires --answer or secret reference metadata")
        return answer, {}
    if answer:
        raise ValueError("secret answer must not include plaintext --answer")
    if not secret_ref:
        raise ValueError("secret answer requires --secret-ref")
    if not SHA256_RE.fullmatch(secret_sha256):
        raise ValueError("secret answer requires a 64-hex --secret-sha256")
    if not secret_exact:
        raise ValueError("secret answer requires --secret-exact")
    display = f"[REDACTED: host-local {secret_ref}]"
    return display, {
        "answer_kind": "secret_ref",
        "secret_ref": secret_ref,
        "secret_sha256": secret_sha256,
        "secret_exact": True,
        "secret_storage": "host_local_volatile",
    }


def _candidate_identity(candidate: dict) -> str:
    if candidate.get("answer_kind") == "secret_ref" and candidate.get("secret_sha256"):
        return f"secret:{str(candidate['secret_sha256']).casefold()}"
    return f"answer:{_normalize_answer(str(candidate.get('answer', '')))}"


def _same_active_answer(candidate: dict, payload: dict, state: str) -> bool:
    return (
        candidate.get("kind") == f"ANSWER_{state}"
        and _candidate_identity(candidate) == _candidate_identity(payload)
        and candidate.get("confidence") == payload.get("confidence")
        and set(candidate.get("evidence", [])) == set(payload.get("evidence", []))
        and bool(candidate.get("semantic_risk")) == bool(payload.get("semantic_risk"))
        and bool(candidate.get("needs_review")) == bool(payload.get("needs_review"))
        and candidate.get("answer_kind") == payload.get("answer_kind")
        and candidate.get("secret_ref") == payload.get("secret_ref")
        and candidate.get("secret_sha256") == payload.get("secret_sha256")
        and bool(candidate.get("secret_exact")) == bool(payload.get("secret_exact"))
    )


def _answer_assist_event(args: argparse.Namespace, metadata: dict) -> dict | None:
    """Authorize the answer actor; return the assist event a Lead answer relies on."""
    lead = protocol.get_case_lead(args.case)
    if args.session not in {metadata["assignee_session"], lead}:
        raise ValueError("answer actor must be the lane assignee or Case Lead")
    if args.session != lead or args.session == metadata["assignee_session"]:
        return None
    assist_event = _latest_assist_event(args.case, args.task_id)
    if assist_event is None:
        raise ValueError("Case Lead answer requires an explicit lane assist event")
    return assist_event


def _unlocked_board_row(case_id: str, question: str) -> dict | None:
    current = build_board(case_id).get(question)
    if current and current["state"] in {"SUBMITTED", "ACCEPTED"}:
        raise ValueError(f"answer is locked in state {current['state']}: {question}")
    return current


def _resolve_answer_state(args: argparse.Namespace, evidence: list[str]) -> str:
    requested = args.state.upper() if args.state != "auto" else ""
    auto_ready = (
        args.confidence == "high"
        and len(evidence) >= 2
        and not args.semantic_risk
        and not args.needs_review
    )
    state = requested or ("READY" if auto_ready else "CANDIDATE")
    if state not in ANSWER_STATES:
        raise ValueError(f"invalid answer state: {state}")
    if state == "READY" and not auto_ready:
        raise ValueError("READY requires high confidence, two unique evidence references, and no review risk")
    return state


def _actor_candidate(current: dict | None, session: str, task_id: str) -> dict | None:
    return next(
        (
            candidate
            for candidate in (current or {}).get("candidates", [])
            if candidate.get("actor_session") == session
            and candidate.get("task_id") == task_id
        ),
        None,
    )


def command_answer(args: argparse.Namespace) -> int:
    lane = _lane_for_task(args.case, args.task_id)
    task_path, metadata = protocol.find_task(args.case, args.task_id)
    protocol.require_task_dispatch_anchor(task_path, metadata)
    task_state = protocol.latest_task_state(args.case, args.task_id)
    if task_state in {"ERROR", "DISPATCH_FAILED"}:
        raise ValueError(f"cannot publish answer from failed task state {task_state}")
    assist_event = _answer_assist_event(args, metadata)
    question = args.question.upper()
    if question not in lane["questions"]:
        raise ValueError(f"question {question} is outside lane {lane['lane_id']}")
    current = _unlocked_board_row(args.case, question)
    evidence = list(dict.fromkeys(item.strip() for item in args.evidence if item.strip()))
    if not evidence:
        raise ValueError("answer requires at least one evidence reference")
    state = _resolve_answer_state(args, evidence)
    answer, secret_fields = _secret_answer_fields(args)
    payload = {
        "lane_id": lane["lane_id"],
        "task_id": args.task_id,
        "task_sha256": protocol.sha256_file(task_path),
        "question_id": question,
        "answer": answer,
        "confidence": args.confidence,
        "evidence": evidence,
        "semantic_risk": bool(args.semantic_risk),
        "needs_review": bool(args.needs_review),
        **secret_fields,
    }
    if assist_event is not None:
        payload["assist_event_id"] = assist_event["event_id"]
    current_candidate = _actor_candidate(current, args.session, args.task_id)
    if current_candidate and _same_active_answer(current_candidate, payload, state):
        print(f"ANSWER {state} {args.case}/{question} lane={lane['lane_id']} unchanged")
    else:
        _write_event(
            kind=f"ANSWER_{state}",
            case_id=args.case,
            actor_session=args.session,
            data=payload,
        )
        print(f"ANSWER {state} {args.case}/{question} lane={lane['lane_id']}")
    return 0


def command_withdraw(args: argparse.Namespace) -> int:
    lane = _lane_for_task(args.case, args.task_id)
    _, metadata = protocol.find_task(args.case, args.task_id)
    lead = protocol.get_case_lead(args.case)
    if args.session not in {metadata["assignee_session"], lead}:
        raise ValueError("withdraw actor must be the lane assignee or Case Lead")
    question = args.question.upper()
    if question not in lane["questions"]:
        raise ValueError(f"question {question} is outside lane {lane['lane_id']}")
    current = build_board(args.case).get(question)
    if current and current["state"] in {"SUBMITTED", "ACCEPTED"}:
        raise ValueError(f"answer is locked in state {current['state']}: {question}")
    _write_event(
        kind="ANSWER_WITHDRAWN",
        case_id=args.case,
        actor_session=args.session,
        data={"lane_id": lane["lane_id"], "task_id": args.task_id, "question_id": question, "reason": args.reason},
    )
    print(f"ANSWER WITHDRAWN {args.case}/{question} lane={lane['lane_id']}")
    return 0


def command_control(args: argparse.Namespace, state: str) -> int:
    require_open(args.case)
    lead = _case_lead(args.case, args.lead_session)
    question = args.question.upper()
    if not QUESTION_RE.fullmatch(question):
        raise ValueError(f"invalid question id: {question}")
    board = build_board(args.case)
    row = board.get(question)
    if state == "SUBMITTED" and (not row or row["state"] != "READY"):
        raise ValueError(f"only READY answers may be submitted: {question}")
    if state == "SUBMITTED" and row and row.get("needs_review"):
        raise ValueError(f"answer still requires review: {question}")
    if state in {"ACCEPTED", "REJECTED"} and (not row or row["state"] != "SUBMITTED"):
        raise ValueError(f"{state} requires SUBMITTED state: {question}")
    validated_answer = (row or {}).get("answer", "")
    if args.answer and _normalize_answer(args.answer) != _normalize_answer(validated_answer):
        raise ValueError(f"control event cannot replace validated answer: {question}")
    _write_event(
        kind=f"ANSWER_{state}", case_id=args.case, actor_session=lead,
        data={"question_id": question, "answer": validated_answer, "note": args.note},
    )
    print(f"ANSWER {state} {args.case}/{question}")
    return 0


def _normalize_answer(value: str) -> str:
    return " ".join(value.casefold().split())


def _answer_record(event: dict, kind: str, data: dict) -> dict:
    return {**data, "kind": kind, "actor_session": event.get("actor_session"), "created_ns": event.get("created_ns")}


def _collect_answer_events(events: list[dict]) -> tuple[dict[str, dict[tuple[str, str], dict]], dict[str, dict]]:
    active: dict[str, dict[tuple[str, str], dict]] = defaultdict(dict)
    controls: dict[str, dict] = {}
    for event in events:
        kind = event.get("kind", "")
        data = event.get("data", {})
        q = str(data.get("question_id", "")).upper()
        if not q:
            continue
        key = (event.get("actor_session", ""), data.get("task_id", ""))
        if kind in {"ANSWER_CANDIDATE", "ANSWER_READY"}:
            active[q][key] = _answer_record(event, kind, data)
        elif kind == "ANSWER_WITHDRAWN":
            active[q].pop(key, None)
        elif kind in {"ANSWER_SUBMITTED", "ANSWER_ACCEPTED", "ANSWER_REJECTED"}:
            controls[q] = _answer_record(event, kind, data)
    return active, controls


def _board_state(candidates: list[dict], distinct: set[str], control: dict | None) -> tuple[str, str]:
    latest_candidate_ns = max((int(c.get("created_ns", 0)) for c in candidates), default=0)
    if control and int(control.get("created_ns", 0)) >= latest_candidate_ns:
        return control["kind"].removeprefix("ANSWER_"), control.get("answer", "")
    if len(distinct) > 1:
        return "CONFLICT", " | ".join(sorted({c.get("answer", "") for c in candidates}))
    if candidates:
        state = "READY" if any(c["kind"] == "ANSWER_READY" for c in candidates) else "CANDIDATE"
        winner = max(candidates, key=lambda c: (c["kind"] == "ANSWER_READY", int(c.get("created_ns", 0))))
        return state, winner.get("answer", "")
    return "OPEN", ""


def _board_row(candidates: list[dict], control: dict | None) -> dict:
    distinct = {_candidate_identity(c) for c in candidates if c.get("answer", "")}
    state, answer = _board_state(candidates, distinct, control)
    needs_review = len(distinct) > 1 or any(c.get("needs_review") or c.get("semantic_risk") for c in candidates)
    return {
        "state": state,
        "answer": answer,
        "needs_review": needs_review,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def build_board(
    case_id: str,
    race_dir: Path | None = None,
    *,
    at_ns: int | None = None,
) -> dict[str, dict]:
    events = [
        p for _, p in iter_race_events(case_id, race_dir)
        if at_ns is None or int(p.get("created_ns", 0)) <= at_ns
    ]
    active, controls = _collect_answer_events(events)
    board: dict[str, dict] = {}
    all_questions = sorted(set(active) | set(controls))
    for q in all_questions:
        board[q] = _board_row(list(active.get(q, {}).values()), controls.get(q))
    return board


def _lane_questions(
    case_id: str,
    race_dir: Path | None = None,
    *,
    at_ns: int | None = None,
) -> list[str]:
    questions: list[str] = []
    for _, event in iter_race_events(case_id, race_dir):
        if at_ns is not None and int(event.get("created_ns", 0)) > at_ns:
            continue
        if event.get("kind") == "LANE_DISPATCHED":
            questions.extend(event.get("data", {}).get("questions", []))
    return list(dict.fromkeys(questions))


def _parse_elapsed_seconds(value: str) -> float:
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([smh]?)", value.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("--at must be elapsed time such as 900s, 15m, or 0.5h")
    amount = float(match.group(1))
    scale = {"": 1.0, "s": 1.0, "m": 60.0, "h": 3600.0}[match.group(2).casefold()]
    return amount * scale


def command_board(args: argparse.Namespace) -> int:
    opened = _session_open_event(args.case)
    if opened is None:
        raise ValueError(f"race session does not exist: {args.case}")
    cutoff_ns = None
    at_value = str(getattr(args, "at", "") or "").strip()
    if at_value:
        cutoff_ns = int(opened["created_ns"]) + int(_parse_elapsed_seconds(at_value) * 1e9)
    board = build_board(args.case, at_ns=cutoff_ns)
    questions = sorted(set(_lane_questions(args.case, at_ns=cutoff_ns)) | set(board))
    print("QUESTION STATE REVIEW ANSWER")
    for q in questions:
        row = board.get(q, {"state": "OPEN", "answer": "", "needs_review": False})
        print(f"{q} {row['state']} {'YES' if row['needs_review'] else 'NO'} {row['answer']}")
    return 0


def command_review_queue(args: argparse.Namespace) -> int:
    if _session_open_event(args.case) is None:
        raise ValueError(f"race session does not exist: {args.case}")
    board = build_board(args.case)
    rows = [(q, row) for q, row in sorted(board.items()) if row.get("needs_review") or row.get("state") == "CONFLICT"]
    if not rows:
        print("Review queue empty.")
        return 0
    print("QUESTION STATE CANDIDATES ANSWER")
    for q, row in rows:
        print(f"{q} {row['state']} {row['candidate_count']} {row['answer']}")
    return 0


_READY_STATES = {"READY", "SUBMITTED", "ACCEPTED"}
_MILESTONE_EVENT_KINDS = {
    "ANSWER_CANDIDATE",
    "ANSWER_READY",
    "ANSWER_WITHDRAWN",
    "ANSWER_SUBMITTED",
    "ANSWER_ACCEPTED",
    "ANSWER_REJECTED",
}


def _seconds_since(t0: int, ns: int | None) -> float | None:
    return None if ns is None else (ns - t0) / 1e9


def _first_event_ns(events: list[dict], kinds: set[str]) -> int | None:
    vals = [int(p["created_ns"]) for p in events if p.get("kind") in kinds]
    return min(vals) if vals else None


def _first_worker_start_ns(case_id: str, task_id: str) -> int | None:
    starts = [
        int(payload.get("created_ns", 0))
        for _, payload in protocol.events_for_task(case_id, task_id)
        if payload.get("kind") == "START"
    ]
    return min(starts) if starts else None


def _worker_start_stats(
    case_id: str, lane_events: list[dict], task_ids: list, start_slo_seconds: int
) -> tuple[list[int], int]:
    start_ns: list[int] = []
    breaches = 0
    for task_id in task_ids:
        if not task_id:
            continue
        first_start = _first_worker_start_ns(case_id, task_id)
        if first_start is None:
            continue
        start_ns.append(first_start)
        lane_event = next(
            (
                event for event in lane_events
                if event.get("data", {}).get("task_id") == task_id
            ),
            None,
        )
        if (
            lane_event is not None
            and (first_start - int(lane_event["created_ns"])) / 1e9 > start_slo_seconds
        ):
            breaches += 1
    return start_ns, breaches


def _ready_count(board: dict, questions: list[str]) -> int:
    return sum(1 for q in questions if board.get(q, {}).get("state") in _READY_STATES)


def _ready_ratio_at(
    case_id: str,
    race_dir: Path | None,
    questions: list[str],
    *,
    t0: int,
    tend: int,
    closed: bool,
    minutes: int,
) -> float | None:
    cutoff = t0 + int(minutes * 60 * 1e9)
    if not closed and tend < cutoff:
        return None
    snapshot_ns = min(cutoff, tend) if closed else cutoff
    count = _ready_count(build_board(case_id, race_dir, at_ns=snapshot_ns), questions)
    return (count / len(questions)) if questions else 0.0


def _milestone_seconds(
    case_id: str,
    race_dir: Path | None,
    events: list[dict],
    questions: list[str],
    t0: int,
    target_ratio: float,
) -> float | None:
    if not questions:
        return None
    needed = math.ceil(len(questions) * target_ratio)
    for event in events:
        if event.get("kind") not in _MILESTONE_EVENT_KINDS:
            continue
        event_ns = int(event.get("created_ns", 0))
        snapshot = build_board(case_id, race_dir, at_ns=event_ns)
        if _ready_count(snapshot, questions) >= needed:
            return (event_ns - t0) / 1e9
    return None


def race_metrics(case_id: str, race_dir: Path | None = None) -> dict:
    events = [p for _, p in iter_race_events(case_id, race_dir)]
    opened = next((p for p in events if p.get("kind") == "SESSION_OPEN"), None)
    if opened is None:
        raise ValueError(f"race session does not exist: {case_id}")
    closed = next((p for p in reversed(events) if p.get("kind") == "SESSION_CLOSED"), None)
    t0 = int(opened["created_ns"])
    tend = int(closed["created_ns"]) if closed else time.time_ns()

    lane_events = [p for p in events if p.get("kind") == "LANE_DISPATCHED"]
    lane_dispatch_ns = [int(p["created_ns"]) for p in lane_events]
    task_ids = [p.get("data", {}).get("task_id") for p in lane_events]
    start_slo_seconds = int(opened.get("data", {}).get("worker_start_slo_seconds", 60))
    start_ns, start_slo_breaches = _worker_start_stats(case_id, lane_events, task_ids, start_slo_seconds)

    questions = _lane_questions(case_id, race_dir)
    ready = _ready_count(build_board(case_id, race_dir), questions)
    all_started = bool(task_ids) and len(start_ns) == len(task_ids)
    window = {"t0": t0, "tend": tend, "closed": closed is not None}

    return {
        "elapsed_seconds": (tend - t0) / 1e9,
        "first_lane_seconds": _seconds_since(t0, min(lane_dispatch_ns, default=None)),
        "routing_complete_seconds": _seconds_since(t0, max(lane_dispatch_ns, default=None)),
        "first_worker_start_seconds": _seconds_since(t0, min(start_ns, default=None)),
        "all_lanes_started_seconds": _seconds_since(t0, max(start_ns)) if all_started else None,
        "worker_start_slo_seconds": start_slo_seconds,
        "worker_start_slo_breaches": start_slo_breaches,
        "first_candidate_seconds": _seconds_since(t0, _first_event_ns(events, {"ANSWER_CANDIDATE", "ANSWER_READY"})),
        "first_ready_seconds": _seconds_since(t0, _first_event_ns(events, {"ANSWER_READY"})),
        "ready_50_seconds": _milestone_seconds(case_id, race_dir, events, questions, t0, 0.50),
        "ready_80_seconds": _milestone_seconds(case_id, race_dir, events, questions, t0, 0.80),
        "ready_100_seconds": _milestone_seconds(case_id, race_dir, events, questions, t0, 1.00),
        "question_count": len(questions),
        "ready_count": ready,
        "ready_ratio": (ready / len(questions)) if questions else 0.0,
        "ready_ratio_at_15m": _ready_ratio_at(case_id, race_dir, questions, minutes=15, **window),
        "ready_ratio_at_30m": _ready_ratio_at(case_id, race_dir, questions, minutes=30, **window),
        "budget_minutes": opened.get("data", {}).get("budget_minutes", 30),
        "closed": closed is not None,
        "clock_semantics": {
            "routing_metrics": "lead-local event clock",
            "worker_answer_metrics": "observed event clock; exact cross-host latency requires synchronized clocks",
        },
    }


def command_metrics(args: argparse.Namespace) -> int:
    metrics = race_metrics(args.case)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


def command_close(args: argparse.Namespace) -> int:
    require_open(args.case)
    lead = _case_lead(args.case, args.lead_session)
    metrics = race_metrics(args.case)
    _write_event(kind="SESSION_CLOSED", case_id=args.case, actor_session=lead, data={"metrics": metrics, "note": args.note})
    print(f"RACE CLOSED {args.case} ready={metrics['ready_count']}/{metrics['question_count']}")
    return 0



_LEAD_ONLY_KINDS = {"ANSWER_SUBMITTED", "ANSWER_ACCEPTED", "ANSWER_REJECTED", "SESSION_OPEN", "SESSION_CLOSED"}
_ACTIVE_ANSWER_KINDS = {"ANSWER_CANDIDATE", "ANSWER_READY"}


@dataclass
class _RaceValidation:
    """Shared state while validating one race case event stream."""

    case_id: str
    race_dir: Path | None
    lead: str
    opens: list[dict]
    assist_by_id: dict
    errors: list[str]
    lanes: dict[str, dict]
    task_to_lane: dict[str, dict]


def _validate_session_markers(events: list[dict], opens: list[dict], closes: list[dict], errors: list[str]) -> None:
    if len(opens) != 1:
        errors.append(f"expected exactly one SESSION_OPEN, got {len(opens)}")
    if len(closes) > 1:
        errors.append(f"expected at most one SESSION_CLOSED, got {len(closes)}")
    if not opens:
        return
    opened = opens[0]
    if not opened.get("data", {}).get("dfir_preflight_required"):
        return
    prior_preflight = [
        event
        for event in events
        if event.get("kind") == "PREFLIGHT_PASSED"
        and int(event.get("created_ns", 0)) < int(opened.get("created_ns", 0))
    ]
    if not prior_preflight:
        errors.append("race required DFIR preflight but no prior PREFLIGHT_PASSED exists")


def _validate_preflight_event(ctx: _RaceValidation, event: dict, kind: str, actor: str) -> None:
    if actor != ctx.lead:
        ctx.errors.append(f"preflight event emitted by non-lead: {actor}")
    if ctx.opens and int(event.get("created_ns", 0)) > int(ctx.opens[0].get("created_ns", 0)):
        ctx.errors.append(f"preflight event emitted after SESSION_OPEN: {kind}")


def _validate_lane_dispatch(ctx: _RaceValidation, data: dict) -> None:
    lane_id = data.get("lane_id", "")
    task_id = data.get("task_id", "")
    if lane_id in ctx.lanes:
        ctx.errors.append(f"duplicate lane id: {lane_id}")
    if task_id in ctx.task_to_lane:
        ctx.errors.append(f"task mapped to multiple lanes: {task_id}")
    ctx.lanes[lane_id] = data
    ctx.task_to_lane[task_id] = data
    try:
        task_path, metadata = protocol.find_task(ctx.case_id, task_id)
        if data.get("task_sha256") != protocol.sha256_file(task_path):
            ctx.errors.append(f"lane task hash drift: {lane_id}/{task_id}")
        if data.get("assignee_session") != metadata.get("assignee_session"):
            ctx.errors.append(f"lane assignee mismatch: {lane_id}/{task_id}")
        ctx.errors.extend(
            f"{lane_id}/{task_id}: {e}"
            for e in protocol.validate_task_dispatch_anchor(task_path, metadata)
        )
    except ValueError as exc:
        ctx.errors.append(f"invalid lane task {lane_id}/{task_id}: {exc}")


def _validate_lane_assist(ctx: _RaceValidation, data: dict, actor: str) -> None:
    task_id = data.get("task_id", "")
    lane = ctx.task_to_lane.get(task_id)
    if actor != ctx.lead:
        ctx.errors.append(f"lane assist emitted by non-lead: {actor} task={task_id}")
    if lane is None:
        ctx.errors.append(f"lane assist references unmapped task: {task_id}")
    elif data.get("lane_id") != lane.get("lane_id"):
        ctx.errors.append(f"lane assist lane mismatch: {task_id}")


def _validate_referenced_assist(
    ctx: _RaceValidation, event: dict, lane: dict, task_id: str, assist_event_id: str
) -> None:
    assist = ctx.assist_by_id.get(assist_event_id)
    if assist is None:
        ctx.errors.append(
            f"lead answer references missing lane assist event: {task_id}/{assist_event_id}"
        )
        return
    assist_data = assist.get("data", {})
    if assist.get("actor_session") != ctx.lead:
        ctx.errors.append(f"lead answer assist actor mismatch: {task_id}")
    if assist_data.get("task_id") != task_id:
        ctx.errors.append(f"lead answer assist task mismatch: {task_id}")
    if assist_data.get("lane_id") != lane.get("lane_id"):
        ctx.errors.append(f"lead answer assist lane mismatch: {task_id}")
    if int(assist.get("created_ns", 0)) >= int(event.get("created_ns", 0)):
        ctx.errors.append(f"lead answer lane assist must predate answer: {task_id}")


def _validate_lead_answer_assist(ctx: _RaceValidation, event: dict, data: dict, lane: dict, task_id: str) -> None:
    assist_event_id = data.get("assist_event_id")
    if assist_event_id:
        _validate_referenced_assist(ctx, event, lane, task_id, assist_event_id)
        return
    prior_assist = _latest_assist_event(
        ctx.case_id,
        task_id,
        ctx.race_dir,
        before_ns=int(event.get("created_ns", 0)),
    )
    if prior_assist is None:
        ctx.errors.append(f"lead answer lane assist must predate answer: {task_id}")


def _validate_secret_answer(data: dict, label: str, errors: list[str]) -> None:
    expected = f"[REDACTED: host-local {data.get('secret_ref', '')}]"
    if not data.get("secret_exact"):
        errors.append(f"secret answer not marked exact: {label}")
    if not SHA256_RE.fullmatch(str(data.get("secret_sha256", ""))):
        errors.append(f"secret answer has invalid SHA-256: {label}")
    if not str(data.get("secret_ref", "")).strip():
        errors.append(f"secret answer missing ref: {label}")
    if data.get("answer") != expected:
        errors.append(f"secret answer display is not canonical redaction: {label}")


def _validate_active_answer_payload(ctx: _RaceValidation, kind: str, data: dict, task_id: str, q: str) -> None:
    label = f"{task_id}/{q}"
    if not str(data.get("answer", "")).strip():
        ctx.errors.append(f"empty answer: {label}")
    if not data.get("evidence"):
        ctx.errors.append(f"answer without evidence: {label}")
    if data.get("answer_kind") == "secret_ref":
        _validate_secret_answer(data, label, ctx.errors)
    try:
        task_path, _ = protocol.find_task(ctx.case_id, task_id)
        if data.get("task_sha256") != protocol.sha256_file(task_path):
            ctx.errors.append(f"answer task hash drift: {label}")
    except ValueError as exc:
        ctx.errors.append(f"invalid answer task {label}: {exc}")
    if kind == "ANSWER_READY" and (data.get("semantic_risk") or data.get("needs_review")):
        ctx.errors.append(f"READY answer carries review risk: {label}")


def _validate_answer_event(ctx: _RaceValidation, event: dict, kind: str, data: dict, actor: str) -> None:
    task_id = data.get("task_id", "")
    lane = ctx.task_to_lane.get(task_id)
    if lane is None:
        ctx.errors.append(f"answer references unmapped task: {task_id}")
        return
    if actor not in {lane.get("assignee_session"), ctx.lead}:
        ctx.errors.append(f"unauthorized answer actor: {actor} task={task_id}")
    if actor == ctx.lead and actor != lane.get("assignee_session"):
        _validate_lead_answer_assist(ctx, event, data, lane, task_id)
    q = str(data.get("question_id", "")).upper()
    if q not in lane.get("questions", []):
        ctx.errors.append(f"answer question outside lane: {task_id}/{q}")
    if kind in _ACTIVE_ANSWER_KINDS:
        _validate_active_answer_payload(ctx, kind, data, task_id, q)


def _validate_race_event(ctx: _RaceValidation, event: dict, close_ns: int | None) -> None:
    kind = event.get("kind")
    data = event.get("data", {})
    actor = event.get("actor_session", "")
    if (
        close_ns is not None
        and int(event.get("created_ns", 0)) > close_ns
        and kind not in {"NOTE"}
    ):
        ctx.errors.append(f"event emitted after SESSION_CLOSED: {kind}")
    if kind in {"PREFLIGHT_PASSED", "PREFLIGHT_FAILED"}:
        _validate_preflight_event(ctx, event, kind, actor)
    elif kind == "LANE_DISPATCHED":
        _validate_lane_dispatch(ctx, data)
    elif kind == "LANE_ASSISTED":
        _validate_lane_assist(ctx, data, actor)
    elif kind in {"ANSWER_CANDIDATE", "ANSWER_READY", "ANSWER_WITHDRAWN"}:
        _validate_answer_event(ctx, event, kind, data, actor)
    elif kind in _LEAD_ONLY_KINDS and actor != ctx.lead:
        ctx.errors.append(f"lead-only event emitted by {actor}: {kind}")


def validate_race_case(case_id: str, race_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    rows = iter_race_events(case_id, race_dir)
    events = [p for _, p in rows]
    opens = [p for p in events if p.get("kind") == "SESSION_OPEN"]
    closes = [p for p in events if p.get("kind") == "SESSION_CLOSED"]
    _validate_session_markers(events, opens, closes, errors)
    close_ns = int(closes[0].get("created_ns", 0)) if closes else None
    ctx = _RaceValidation(
        case_id=case_id,
        race_dir=race_dir,
        lead=protocol.get_case_lead(case_id),
        opens=opens,
        assist_by_id={
            event.get("event_id"): event
            for event in events
            if event.get("kind") == "LANE_ASSISTED" and event.get("event_id")
        },
        errors=errors,
        lanes={},
        task_to_lane={},
    )
    for event in events:
        _validate_race_event(ctx, event, close_ns)
    return errors


def command_doctor(args: argparse.Namespace) -> int:
    errors = validate_race_case(args.case)
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"RACE DOCTOR FAIL errors={len(errors)}")
        return 2
    print("RACE DOCTOR PASS")
    return 0

def add_subcommands(parser: argparse.ArgumentParser) -> None:
    sub = parser.add_subparsers(dest="race_command", required=True)
    p = sub.add_parser("preflight", help="Run DFIR capability checks before starting the Race clock")
    p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--image")
    source.add_argument("--evidence-root")
    p.add_argument("--dfir-python", default=sys.executable)
    p.add_argument("--timeout-seconds", type=float, default=30.0)
    p.set_defaults(func=command_preflight)

    p = sub.add_parser("open", help="Start a timed race session")
    p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True)
    p.add_argument("--budget-minutes", type=int, default=30); p.add_argument("--target-ready-ratio", type=float, default=0.8)
    p.add_argument("--worker-start-slo-seconds", type=int, default=60)
    p.add_argument("--require-dfir-preflight", action="store_true")
    p.set_defaults(func=command_open)

    p = sub.add_parser("lane", help="Create one governed multi-question investigation lane")
    p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True); p.add_argument("--lane-id", required=True)
    p.add_argument("--task-id", required=True); p.add_argument("--type", dest="task_type", choices=["DISCOVERY","TRIAGE","VERIFY","REVERSE"], default="TRIAGE")
    p.add_argument("--target-role", required=True); p.add_argument("--assignee-session", required=True)
    p.add_argument("--execution-environment", choices=sorted(protocol.VALID_EXECUTION_ENVIRONMENTS), required=True)
    p.add_argument("--questions", required=True); p.add_argument("--domain", required=True); p.add_argument("--objective", required=True)
    p.add_argument("--context", default=""); p.add_argument("--skills", default="")
    p.set_defaults(func=command_lane)

    p = sub.add_parser("answer", help="Publish a candidate/ready answer before task DONE")
    p.add_argument("--case", required=True); p.add_argument("--task-id", required=True); p.add_argument("--session", required=True); p.add_argument("--question", required=True)
    answer_source = p.add_mutually_exclusive_group(required=True)
    answer_source.add_argument("--answer")
    answer_source.add_argument("--secret-ref")
    p.add_argument("--secret-sha256", default="")
    p.add_argument("--secret-exact", action="store_true")
    p.add_argument("--confidence", choices=["low","medium","high"], required=True)
    p.add_argument("--evidence", action="append", default=[], required=True); p.add_argument("--state", choices=["auto","candidate","ready"], default="auto")
    p.add_argument("--semantic-risk", action="store_true"); p.add_argument("--needs-review", action="store_true")
    p.set_defaults(func=command_answer)

    p = sub.add_parser("withdraw", help="Withdraw this lane's active answer")
    p.add_argument("--case", required=True); p.add_argument("--task-id", required=True); p.add_argument("--session", required=True); p.add_argument("--question", required=True); p.add_argument("--reason", required=True)
    p.set_defaults(func=command_withdraw)

    p = sub.add_parser("assist", help="Authorize Case Lead assistance on an existing race lane")
    p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True)
    p.add_argument("--task-id", required=True); p.add_argument("--reason", required=True)
    p.set_defaults(func=command_assist)

    p = sub.add_parser("watchdog", help="Report lanes that missed the worker START SLO")
    p.add_argument("--case", required=True)
    p.add_argument("--start-slo-seconds", type=int)
    p.add_argument("--lead-session", default="")
    p.add_argument("--assist-overdue", action="store_true")
    p.set_defaults(func=command_watchdog)

    for name, state in (("submit","SUBMITTED"),("accept","ACCEPTED"),("reject","REJECTED")):
        p = sub.add_parser(name, help=f"Mark one race answer {state.lower()}")
        p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True); p.add_argument("--question", required=True)
        p.add_argument("--answer", default=""); p.add_argument("--note", default="")
        p.set_defaults(func=lambda args, s=state: command_control(args, s))

    p = sub.add_parser("board", help="Render the derived live or historical answer board")
    p.add_argument("--case", required=True); p.add_argument("--at", default="")
    p.set_defaults(func=command_board)
    p = sub.add_parser("review-queue", help="Show only conflicted / review-required answers")
    p.add_argument("--case", required=True); p.set_defaults(func=command_review_queue)
    p = sub.add_parser("metrics", help="Show race latency/coverage metrics")
    p.add_argument("--case", required=True); p.set_defaults(func=command_metrics)
    p = sub.add_parser("doctor", help="Validate race event provenance and lane invariants")
    p.add_argument("--case", required=True); p.set_defaults(func=command_doctor)
    p = sub.add_parser("close", help="Close a race session and freeze final metrics event")
    p.add_argument("--case", required=True); p.add_argument("--lead-session", required=True); p.add_argument("--note", default="")
    p.set_defaults(func=command_close)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Race-mode orchestration for .collab")
    add_subcommands(parser)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
