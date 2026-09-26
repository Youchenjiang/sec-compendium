#!/usr/bin/env python3
"""Watch v2.2 governed task assignments and runtime communication events."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import collab_protocol as protocol


REPO_ROOT = protocol.REPO_ROOT
CASES_DIR = protocol.CASES_DIR
RUNTIME_DIR = protocol.RUNTIME_DIR / "watchers"

# Compatibility exports used by tests and callers from the first watcher revision.
parse_task_metadata = protocol.parse_task_metadata
discover_assigned_tasks = protocol.discover_assigned_tasks
output_path_for_task = protocol.output_path_for_task


def load_state(state_path: Path) -> dict[str, set[str]]:
    """Load per-session watcher state. Corrupt state is treated as empty."""
    empty = {"seen_tasks": set(), "seen_events": set()}
    if not state_path.exists():
        return empty
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty

    return {
        "seen_tasks": {
            item for item in payload.get("seen_tasks", []) if isinstance(item, str)
        },
        "seen_events": {
            item for item in payload.get("seen_events", []) if isinstance(item, str)
        },
    }


def save_state(state_path: Path, state: dict[str, set[str]]) -> None:
    """Persist watcher state below Git-ignored runtime storage."""
    payload = {
        "seen_tasks": sorted(state["seen_tasks"]),
        "seen_events": sorted(state["seen_events"]),
    }
    protocol.atomic_write_text(state_path, json.dumps(payload, indent=2) + "\n")


def load_seen(state_path: Path) -> set[str]:
    """Compatibility helper for the original watcher test surface."""
    return load_state(state_path)["seen_tasks"]


def save_seen(state_path: Path, seen: set[str]) -> None:
    """Compatibility helper for the original watcher test surface."""
    save_state(state_path, {"seen_tasks": set(seen), "seen_events": set()})


def beep() -> None:
    if sys.platform == "win32":
        try:
            import winsound

            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            return
        except Exception:
            pass
    sys.stdout.write("\a")
    sys.stdout.flush()


def copy_to_clipboard(text: str) -> None:
    try:
        if sys.platform == "win32":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode("utf-8"),
                check=True,
            )
    except (OSError, subprocess.SubprocessError):
        pass


def build_task_instruction(
    session: str,
    task_path: Path,
    output_path: Path,
    metadata: dict[str, str],
) -> str:
    return (
        f"你是 {session}。請讀取 {protocol.relative_posix(task_path)} 的 "
        f"{metadata['task_type']} 任務。先執行 collab_bus.py start，依 evidence contract "
        f"完成分析，且只新增 {protocol.relative_posix(output_path)}；需要澄清時使用 "
        "collab_bus.py send --kind QUESTION，完成後使用 collab_bus.py done。不得修改 "
        "task、CASE_STATE.md、questions.md 或 SCOREBOARD.md。"
    )


def build_event_instruction(session: str, payload: dict) -> str:
    kind = payload.get("kind", "EVENT")
    source = payload.get("from_session", "unknown")
    case_id = payload.get("case_id", "unknown")
    task_id = payload.get("task_id", "unknown")
    message = payload.get("message", "")
    if kind == "QUESTION":
        return (
            f"你是 {session}。{source} 對 {case_id}/{task_id} 提出 QUESTION：{message} "
            "請讀取對應 task 與既有 evidence，使用 collab_bus.py send --kind REPLY 回覆；"
            "不要直接修改對方 finding。"
        )
    return (
        f"你是 {session}。收到 {source} 對 {case_id}/{task_id} 的 {kind} event："
        f"{message or '(no message)'}。請依 Case Lead / assignee ownership 處理。"
    )


def dispatch_cli(program: str, exec_args: list[str], instruction: str) -> int:
    completed = subprocess.run(
        [program, *exec_args, instruction],
        cwd=str(REPO_ROOT),
        check=False,
    )
    return completed.returncode


def has_ack_from_session(case_id: str, task_id: str, session: str) -> bool:
    return any(
        payload.get("kind") == "ACK" and payload.get("from_session") == session
        for _, payload in protocol.events_for_task(case_id, task_id)
    )


def process_assignments(
    session: str,
    case_filters: set[str] | None,
    state: dict[str, set[str]],
    state_path: Path,
    exec_program: str | None,
    exec_args: list[str],
) -> int:
    announced = 0
    assignments = protocol.discover_assigned_tasks(CASES_DIR, session, case_filters)

    for task_path, metadata in assignments:
        task_key = protocol.relative_posix(task_path)
        if task_key in state["seen_tasks"]:
            continue

        output_path = protocol.output_path_for_task(task_path, metadata)
        if output_path.exists():
            state["seen_tasks"].add(task_key)
            save_state(state_path, state)
            continue

        lead = protocol.get_case_lead(metadata["case_id"])
        if lead is None:
            raise ValueError(f"assigned task 所屬 case 沒有有效 Lead: {metadata['case_id']}")

        if not has_ack_from_session(metadata["case_id"], metadata["task_id"], session):
            protocol.emit_event(
                kind="ACK",
                case_id=metadata["case_id"],
                task_id=metadata["task_id"],
                from_session=session,
                to_session=lead,
                message="Watcher detected assigned task",
                task_path=task_path,
            )

        timestamp = datetime.now().strftime("%H:%M:%S")
        instruction = build_task_instruction(session, task_path, output_path, metadata)
        print(
            f"\n[{timestamp}] 🚨 ASSIGNED {metadata['case_id']}/{metadata['task_id']} "
            f"{metadata['task_type']}"
        )
        print(f"    📂 {task_key}")
        print(f"    📤 {protocol.relative_posix(output_path)}")
        print(f"    📡 ACK -> {lead}")
        copy_to_clipboard(instruction)
        beep()

        if exec_program:
            exit_code = dispatch_cli(exec_program, exec_args, instruction)
            print(f"    {'✅' if exit_code == 0 else '❌'} CLI Agent exit={exit_code}")

        state["seen_tasks"].add(task_key)
        save_state(state_path, state)
        announced += 1

    return announced


def process_incoming_events(
    session: str,
    case_filters: set[str] | None,
    state: dict[str, set[str]],
    state_path: Path,
) -> int:
    announced = 0
    for event_path, payload in protocol.incoming_events(session):
        if case_filters and payload.get("case_id") not in case_filters:
            continue
        event_id = payload.get("event_id")
        if not isinstance(event_id, str) or event_id in state["seen_events"]:
            continue
        # DISPATCHED is represented by the actual task notification; suppress duplicate noise.
        if payload.get("kind") == "DISPATCHED":
            state["seen_events"].add(event_id)
            save_state(state_path, state)
            continue

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(
            f"\n[{timestamp}] 📡 {payload.get('kind')} "
            f"{payload.get('case_id')}/{payload.get('task_id')} "
            f"from={payload.get('from_session')}"
        )
        if payload.get("message"):
            print(f"    💬 {payload['message']}")
        copy_to_clipboard(build_event_instruction(session, payload))
        beep()

        state["seen_events"].add(event_id)
        save_state(state_path, state)
        announced += 1
    return announced


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Governed .collab task + event watcher")
    parser.add_argument("--session", required=True)
    parser.add_argument("--case", action="append", dest="cases", default=[])
    parser.add_argument("--interval", type=float, default=1.5)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--reset-seen", action="store_true")
    parser.add_argument("--exec-program", default=None)
    parser.add_argument("--exec-arg", action="append", default=[])
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        protocol.validate_session(args.session)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if args.interval <= 0:
        raise SystemExit("--interval 必須大於 0")

    state_path = RUNTIME_DIR / f"{args.session}.json"
    if args.reset_seen and state_path.exists():
        state_path.unlink()
    state = load_state(state_path)
    case_filters = set(args.cases) or None

    print("=" * 72)
    print(f"🤖 Governed Collab Watcher | session={args.session}")
    print("📂 Tasks: .collab/cases/<CaseID>/tasks/")
    print("📡 Events: .collab/runtime/events/<CaseID>/<TaskID>/")
    print(f"💾 State: {state_path}")
    print(f"🎯 Cases: {', '.join(sorted(case_filters)) if case_filters else 'ALL'}")
    print("=" * 72)

    while True:
        try:
            process_assignments(
                session=args.session,
                case_filters=case_filters,
                state=state,
                state_path=state_path,
                exec_program=args.exec_program,
                exec_args=args.exec_arg,
            )
            process_incoming_events(args.session, case_filters, state, state_path)
            if args.once:
                return 0
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n🛑 監聽已停止。")
            return 0
        except (OSError, ValueError) as exc:
            print(f"⚠️ watcher error: {exc}", file=sys.stderr)
            if args.once:
                return 2
            time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
