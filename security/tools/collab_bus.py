#!/usr/bin/env python3
"""Command-line communication layer for the v2.2 Governed Case Bus."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import collab_protocol as protocol


def render_task_markdown(args: argparse.Namespace) -> str:
    questions = args.question or "None"
    skills = args.skills or "unspecified"
    context = args.context or "None provided."
    return f"""# TASK: {args.task_id} - {args.title}

## 1. 任務基本資訊
- **所屬大題**：`{args.case}`
- **關聯小題**：`{questions}`
- **任務類型**：`{args.task_type}`
- **Target Role**：`{args.target_role}`
- **Assignee Session**：`{args.assignee_session}`
- **發起 Session**：`{args.actor_session}`
- **發起時間**：`{protocol.utc_timestamp()}`
- **期望技能**：`{skills}`
- **Task ID**：`{args.task_id}`

---

## 2. 案情背景與目標
{args.objective}

---

## 3. 待分析資料片段 (Context Payload)
{context}

---

## 4. 接單 Session 輸出規範
1. 不得修改本 task；發布後 task immutable。
2. 只新增本 task 的 governed output，不修改 `CASE_STATE.md`、`questions.md` 或 `SCOREBOARD.md`。
3. Finding 必須提供 artifact/source、tool/method、direct observation、reproduction、known limitations 與 confidence。
4. `VERIFY` 若既有候選皆不成立，必須明確回報「皆非」並提供反證。
5. 完成後使用 `collab_bus.py done` 發送 runtime `DONE` event 給 Case Lead。
"""


def ensure_actor_is_case_lead(case_id: str, actor_session: str) -> str:
    protocol.validate_session(actor_session)
    lead = protocol.get_case_lead(case_id)
    if lead is None:
        raise ValueError(f"case 尚未有有效 Lead Session: {case_id}")
    if actor_session != lead:
        raise ValueError(
            f"actor 不是 {case_id} 的 Case Lead: actor={actor_session} lead={lead}"
        )
    return lead


def find_case_task_ids(case_id: str) -> set[str]:
    return {
        protocol.parse_task_metadata(path)["task_id"]
        for path in (protocol.iter_tasks(protocol.CASES_DIR, {case_id}) or [])
        if protocol.parse_task_metadata(path)["task_id"]
    }


def command_new_task(args: argparse.Namespace) -> int:
    ensure_actor_is_case_lead(args.case, args.actor_session)
    protocol.validate_session(args.assignee_session)
    protocol.validate_task_id(args.task_id)
    if args.task_type not in protocol.VALID_TASK_TYPES:
        raise ValueError(f"invalid task type: {args.task_type}")
    if args.task_id in find_case_task_ids(args.case):
        raise ValueError(f"duplicate Task ID in {args.case}: {args.task_id}")

    current_case = protocol.case_dir(args.case)
    task_path = current_case / "tasks" / f"{args.task_id}_{args.task_type}.md"
    if task_path.exists():
        raise ValueError(f"task already exists: {task_path}")

    protocol.atomic_write_text(task_path, render_task_markdown(args))
    try:
        protocol.emit_event(
            kind="DISPATCHED",
            case_id=args.case,
            task_id=args.task_id,
            from_session=args.actor_session,
            to_session=args.assignee_session,
            message=args.title,
            task_path=task_path,
        )
    except Exception:
        task_path.unlink(missing_ok=True)
        raise
    print(protocol.relative_posix(task_path))
    return 0


def task_and_assignee(case_id: str, task_id: str, session: str):
    protocol.validate_session(session)
    task_path, metadata = protocol.find_task(case_id, task_id)
    if metadata["assignee_session"] != session:
        raise ValueError(
            f"session 不是 task assignee: session={session} assignee={metadata['assignee_session']}"
        )
    return task_path, metadata


def emit_worker_event(args: argparse.Namespace, kind: str) -> int:
    task_path, metadata = task_and_assignee(args.case, args.task_id, args.session)
    lead = protocol.get_case_lead(args.case)
    if lead is None:
        raise ValueError(f"case 尚未有有效 Lead Session: {args.case}")

    output_path = protocol.output_path_for_task(task_path, metadata)
    prior_events = [payload for _, payload in protocol.events_for_task(args.case, args.task_id)]
    if kind == "START" and not any(
        payload.get("kind") == "ACK" and payload.get("from_session") == args.session
        for payload in prior_events
    ):
        raise ValueError("START 前必須由同一 Assignee Session 先送 ACK")
    if kind == "DONE":
        if not any(
            payload.get("kind") == "ACK" and payload.get("from_session") == args.session
            for payload in prior_events
        ):
            raise ValueError("DONE 前缺少同一 Assignee Session 的 ACK")
        if not any(
            payload.get("kind") == "START" and payload.get("from_session") == args.session
            for payload in prior_events
        ):
            raise ValueError("DONE 前缺少同一 Assignee Session 的 START")
        if not output_path.exists():
            raise ValueError(f"DONE 前 governed output 必須存在: {output_path}")
        original_hash = protocol.first_task_hash_from_events(args.case, args.task_id)
        current_hash = protocol.sha256_file(task_path)
        if original_hash and current_hash != original_hash:
            raise ValueError("immutable task hash 已改變；拒絕送出 DONE")
        output_errors = protocol.validate_governed_output(task_path, metadata, output_path)
        if output_errors:
            raise ValueError("DONE output contract 未通過: " + "; ".join(output_errors))

    protocol.emit_event(
        kind=kind,
        case_id=args.case,
        task_id=args.task_id,
        from_session=args.session,
        to_session=lead,
        message=getattr(args, "message", "") or "",
        task_path=task_path,
        output_path=output_path if output_path.exists() else None,
    )
    print(f"{kind} {args.case}/{args.task_id} -> {lead}")
    return 0


def command_init_output(args: argparse.Namespace) -> int:
    task_path, metadata = task_and_assignee(args.case, args.task_id, args.session)
    output_path = protocol.output_path_for_task(task_path, metadata)
    if output_path.exists():
        raise ValueError(f"output already exists: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if metadata["task_type"] == "REVIEW":
        body = f"""# REVIEW: {metadata['task_id']} 獨立審查

## 1. 審查資訊
- **對應 Task**：`{metadata['task_id']}`
- **Reviewer Session**：`{args.session}`
- **完成時間**：`{protocol.utc_timestamp()}`

## 2. 審查結論
- **Verdict**：`TODO`
- **可支持答案狀態**：`TODO`

## 3. Evidence Cross-check
- **重現結果**：TODO
- **時間與因果**：TODO
- **替代解釋 / False Positive**：TODO
- **格式檢查**：TODO

## 4. Blockers / Residual Risk
-
"""
    else:
        body = f"""# FINDING: {metadata['task_id']} 成果回報

## 1. 成果回報資訊
- **對應任務**：`{metadata['task_id']}`
- **解決小題**：`{metadata['questions'] or 'None'}`
- **解答 Session**：`{args.session}`
- **完成時間**：`{protocol.utc_timestamp()}`
- **Confidence**：`TODO`

## 2. 核心結論與關鍵答案 (Direct Answers)
- **Answer / Conclusion**：TODO

## 3. Evidence Contract
- **Artifact / Source**：TODO
- **Artifact hash（若可得）**：TODO
- **取得方法 / Tool**：TODO
- **Direct Observation**：TODO
- **Reproduction**：TODO
- **Known Limitations**：TODO

## 4. 分析與推論 (Analysis)
-

## 5. 建議下一步
- **建議答案狀態**：`TODO`
- **需要額外 review**：`TODO`
- **尚未解決問題**：TODO
"""
    protocol.atomic_write_text(output_path, body)
    print(protocol.relative_posix(output_path))
    return 0


def command_send(args: argparse.Namespace) -> int:
    task_path, metadata = protocol.find_task(args.case, args.task_id)
    lead = protocol.get_case_lead(args.case)
    if lead is None:
        raise ValueError(f"case 尚未有有效 Lead Session: {args.case}")
    participants = {lead, metadata["assignee_session"]}
    if args.from_session not in participants or args.to_session not in participants:
        raise ValueError("task-scoped message 只能在 Case Lead 與唯一 assignee 之間傳遞")
    if args.from_session == args.to_session:
        raise ValueError("from-session 與 to-session 不可相同")
    protocol.emit_event(
        kind=args.kind,
        case_id=args.case,
        task_id=args.task_id,
        from_session=args.from_session,
        to_session=args.to_session,
        message=args.message,
        task_path=task_path,
    )
    print(f"{args.kind} {args.from_session} -> {args.to_session}")
    return 0


def command_dispatch_failed(args: argparse.Namespace) -> int:
    lead = ensure_actor_is_case_lead(args.case, args.session)
    task_path, metadata = protocol.find_task(args.case, args.task_id)
    prior_events = [payload for _, payload in protocol.events_for_task(args.case, args.task_id)]
    if any(payload.get("kind") == "ACK" for payload in prior_events):
        raise ValueError("已有 ACK 的 task 不可標記為 DISPATCH_FAILED；請使用 worker ERROR")
    if any(payload.get("kind") == "DISPATCH_FAILED" for payload in prior_events):
        raise ValueError("task 已存在 DISPATCH_FAILED event")
    protocol.emit_event(
        kind="DISPATCH_FAILED",
        case_id=args.case,
        task_id=args.task_id,
        from_session=lead,
        to_session=metadata["assignee_session"],
        message=args.message,
        task_path=task_path,
    )
    print(f"DISPATCH_FAILED {args.case}/{args.task_id} -> {metadata['assignee_session']}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    case_filters = set(args.case) if args.case else None
    found = protocol.discover_assigned_tasks(protocol.CASES_DIR, args.session, case_filters)
    if not found:
        print("No assigned tasks.")
        return 0
    for task_path, metadata in found:
        state = protocol.latest_task_state(metadata["case_id"], metadata["task_id"])
        output = protocol.output_path_for_task(task_path, metadata)
        print(
            f"{metadata['case_id']} {metadata['task_id']} {metadata['task_type']} "
            f"state={state} output={'yes' if output.exists() else 'no'} "
            f"path={protocol.relative_posix(task_path)}"
        )
    return 0


def command_status(args: argparse.Namespace) -> int:
    case_filters = {args.case} if args.case else None
    rows = []
    for task_path in protocol.iter_tasks(protocol.CASES_DIR, case_filters) or []:
        metadata = protocol.parse_task_metadata(task_path)
        errors = protocol.validate_task_metadata(task_path, metadata)
        state = "INVALID" if errors else protocol.latest_task_state(
            metadata["case_id"], metadata["task_id"]
        )
        if args.session and metadata.get("assignee_session") != args.session:
            continue
        output = protocol.output_path_for_task(task_path, metadata) if not errors else None
        rows.append(
            (
                metadata.get("case_id", "?"),
                metadata.get("task_id", "?"),
                metadata.get("task_type", "?"),
                metadata.get("assignee_session", "?"),
                state,
                "yes" if output and output.exists() else "no",
            )
        )
    if not rows:
        print("No tasks.")
        return 0
    print("CASE TASK TYPE ASSIGNEE STATE OUTPUT")
    for row in rows:
        print(" ".join(row))
    return 0


def command_events(args: argparse.Namespace) -> int:
    protocol.validate_session(args.session)
    rows = []
    for _, payload in protocol.iter_events() or []:
        if args.case and payload.get("case_id") != args.case:
            continue
        if args.task_id and payload.get("task_id") != args.task_id:
            continue
        incoming = payload.get("to_session") == args.session
        outgoing = payload.get("from_session") == args.session
        if args.direction == "in" and not incoming:
            continue
        if args.direction == "out" and not outgoing:
            continue
        if args.direction == "all" and not (incoming or outgoing):
            continue
        rows.append(payload)

    if not rows:
        print("No events.")
        return 0
    rows.sort(key=lambda payload: int(payload.get("created_ns", 0)))
    for payload in rows:
        print(
            f"{payload.get('timestamp_utc')} {payload.get('kind')} "
            f"{payload.get('case_id')}/{payload.get('task_id')} "
            f"{payload.get('from_session')}->{payload.get('to_session')} "
            f"{payload.get('message') or ''}"
        )
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    gitignore = protocol.REPO_ROOT / ".gitignore"
    ignore_text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if "/.collab/runtime/" not in ignore_text:
        errors.append(".collab/runtime/ is not explicitly Git-ignored")

    seen_ids: dict[tuple[str, str], Path] = {}
    case_filters = {args.case} if args.case else None
    for task_path in protocol.iter_tasks(protocol.CASES_DIR, case_filters) or []:
        metadata = protocol.parse_task_metadata(task_path)
        task_errors = protocol.validate_task_metadata(task_path, metadata)
        for error in task_errors:
            errors.append(f"{protocol.relative_posix(task_path)}: {error}")

        key = (metadata.get("case_id", ""), metadata.get("task_id", ""))
        if key[1]:
            if key in seen_ids:
                errors.append(
                    f"duplicate Task ID {key[0]}/{key[1]}: "
                    f"{seen_ids[key]} and {task_path}"
                )
            seen_ids[key] = task_path

        if not task_errors:
            lead = protocol.get_case_lead(metadata["case_id"])
            if lead is None:
                warnings.append(f"{metadata['case_id']}: no valid Case Lead")

            first_hash = protocol.first_task_hash_from_events(
                metadata["case_id"], metadata["task_id"]
            )
            if first_hash and protocol.sha256_file(task_path) != first_hash:
                errors.append(
                    f"immutable task changed: {metadata['case_id']}/{metadata['task_id']}"
                )

    for warning in sorted(set(warnings)):
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}")

    if errors:
        print(f"DOCTOR FAIL errors={len(errors)} warnings={len(set(warnings))}")
        return 2
    print(f"DOCTOR PASS warnings={len(set(warnings))}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Governed .collab communication CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    new_task = sub.add_parser("new-task", help="Case Lead creates one immutable task")
    new_task.add_argument("--case", required=True)
    new_task.add_argument("--actor-session", required=True)
    new_task.add_argument("--task-id", required=True)
    new_task.add_argument("--type", dest="task_type", required=True, choices=sorted(protocol.VALID_TASK_TYPES))
    new_task.add_argument("--target-role", required=True)
    new_task.add_argument("--assignee-session", required=True)
    new_task.add_argument("--question", default="")
    new_task.add_argument("--title", required=True)
    new_task.add_argument("--objective", required=True)
    new_task.add_argument("--context", default="")
    new_task.add_argument("--skills", default="")
    new_task.set_defaults(func=command_new_task)

    init_output = sub.add_parser("init-output", help="Create the governed output skeleton")
    init_output.add_argument("--case", required=True)
    init_output.add_argument("--task-id", required=True)
    init_output.add_argument("--session", required=True)
    init_output.set_defaults(func=command_init_output)

    for name, kind in (("ack", "ACK"), ("start", "START"), ("done", "DONE"), ("error", "ERROR")):
        event = sub.add_parser(name, help=f"Emit {kind} to the Case Lead")
        event.add_argument("--case", required=True)
        event.add_argument("--task-id", required=True)
        event.add_argument("--session", required=True)
        event.add_argument("--message", default="")
        event.set_defaults(func=lambda args, event_kind=kind: emit_worker_event(args, event_kind))

    send = sub.add_parser("send", help="Send a task-scoped runtime message")
    send.add_argument("--case", required=True)
    send.add_argument("--task-id", required=True)
    send.add_argument("--from-session", required=True)
    send.add_argument("--to-session", required=True)
    send.add_argument("--kind", required=True, choices=["QUESTION", "REPLY", "NOTE"])
    send.add_argument("--message", required=True)
    send.set_defaults(func=command_send)

    dispatch_failed = sub.add_parser(
        "dispatch-failed",
        help="Case Lead records a pre-ACK worker transport/bootstrap failure",
    )
    dispatch_failed.add_argument("--case", required=True)
    dispatch_failed.add_argument("--task-id", required=True)
    dispatch_failed.add_argument("--session", required=True)
    dispatch_failed.add_argument("--message", required=True)
    dispatch_failed.set_defaults(func=command_dispatch_failed)

    listing = sub.add_parser("list", help="List tasks assigned to one session")
    listing.add_argument("--session", required=True)
    listing.add_argument("--case", action="append", default=[])
    listing.set_defaults(func=command_list)

    status = sub.add_parser("status", help="Summarize task communication state")
    status.add_argument("--case")
    status.add_argument("--session")
    status.set_defaults(func=command_status)

    events = sub.add_parser("events", help="Show task-scoped runtime communication history")
    events.add_argument("--session", required=True)
    events.add_argument("--case")
    events.add_argument("--task-id")
    events.add_argument("--direction", choices=["in", "out", "all"], default="all")
    events.set_defaults(func=command_events)

    doctor = sub.add_parser("doctor", help="Validate the communication contract")
    doctor.add_argument("--case")
    doctor.set_defaults(func=command_doctor)
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
