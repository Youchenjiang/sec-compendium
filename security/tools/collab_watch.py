#!/usr/bin/env python3
"""Watch v2.3 governed task assignments and runtime communication events."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Callable
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
    execution_environment = metadata.get("execution_environment") or protocol.LEGACY_EXECUTION_ENVIRONMENT
    execution_profile = metadata.get("execution_profile", "governed") or "governed"
    lane_id = metadata.get("lane_id", "")
    race_hint = ""
    if execution_profile == "race":
        race_hint = (
            f" RACE MODE lane={lane_id}: publish each resolved question immediately with "
            "python security/tools/collab_race.py answer; do not wait for task DONE before surfacing answers."
        )
    return (
        f"你是 {session}。請讀取 {protocol.relative_posix(task_path)} 的 "
        f"{metadata['task_type']} 任務（execution_environment={execution_environment}）。"
        "先執行 collab_bus.py start，依 evidence contract "
        f"完成分析，且只新增 {protocol.relative_posix(output_path)}；需要澄清時使用 "
        "collab_bus.py send --kind QUESTION，完成後使用 collab_bus.py done。不得修改 "
        "task、CASE_STATE.md、questions.md 或 SCOREBOARD.md。"
        + race_hint
    )


def resolve_node_class(node_class: str) -> str:
    if node_class in {"primary", "remote"}:
        return node_class
    configured = os.environ.get("COLLAB_NODE_CLASS", "").strip().casefold()
    if configured in {"primary", "remote"}:
        return configured
    return "remote"


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


def dispatch_cli(
    program: str,
    exec_args: list[str],
    instruction: str,
    timeout: float | None = None,
) -> int:
    """Launch an interactive agent (the browser/composer transport).

    A hung or crashed composer must never block the governed task: on timeout
    or spawn failure we return a non-zero code so the caller falls back to the
    durable file/CLI handoff.
    """
    try:
        completed = subprocess.run(
            [program, *exec_args, instruction],
            cwd=str(REPO_ROOT),
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"    ⏱️ CLI Agent timed out after {timeout}s")
        return 124
    except OSError as exc:
        print(f"    ❌ CLI Agent spawn failed: {exc}")
        return 127
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
    transport: str = "auto",
    exec_timeout: float | None = 600.0,
    inbox_dir: Path | None = None,
    node_class: str = "auto",
    on_handoff: Callable[[Path, str], None] | None = None,
) -> int:
    announced = 0
    assignments = protocol.discover_assigned_tasks(CASES_DIR, session, case_filters)

    for task_path, metadata in assignments:
        task_key = protocol.relative_posix(task_path)
        current_state = protocol.latest_task_state(metadata["case_id"], metadata["task_id"])
        handoff_path = protocol.handoff_path_for_task(
            session, metadata["case_id"], metadata["task_id"], inbox_dir
        )
        if current_state in protocol.TERMINAL_TASK_STATES:
            protocol.consume_handoff(handoff_path)
            state["seen_tasks"].add(task_key)
            save_state(state_path, state)
            continue

        execution_environment = (
            metadata.get("execution_environment") or protocol.LEGACY_EXECUTION_ENVIRONMENT
        )
        resolved_node_class = resolve_node_class(node_class)
        if (
            execution_environment == "host_local_gateway"
            and resolved_node_class != "primary"
        ):
            raise ValueError(
                f"{metadata['case_id']}/{metadata['task_id']} requires host_local_gateway; "
                f"current node class is {resolved_node_class}"
            )

        output_path = protocol.output_path_for_task(task_path, metadata)
        if current_state in {"ACK", "START"} and handoff_path.exists():
            state["seen_tasks"].add(task_key)
            save_state(state_path, state)
            continue
        if task_key in state["seen_tasks"] and handoff_path.exists():
            continue

        lead = protocol.get_case_lead(metadata["case_id"])
        if lead is None:
            raise ValueError(f"assigned task 所屬 case 沒有有效 Lead: {metadata['case_id']}")

        # ACK is a delivery acknowledgement from the exact-assignee watcher.
        # It does not mean an interactive worker has started; START is that evidence.
        if not has_ack_from_session(metadata["case_id"], metadata["task_id"], session):
            transition_error = protocol.lifecycle_transition_error(current_state, "ACK")
            if transition_error:
                raise ValueError(transition_error)
            protocol.emit_event(
                kind="ACK",
                case_id=metadata["case_id"],
                task_id=metadata["task_id"],
                from_session=session,
                to_session=lead,
                message="Watcher accepted task delivery; worker not started yet",
                task_path=task_path,
            )
            current_state = "ACK"
        else:
            current_state = protocol.latest_task_state(
                metadata["case_id"], metadata["task_id"]
            )

        timestamp = datetime.now().strftime("%H:%M:%S")
        instruction = build_task_instruction(session, task_path, output_path, metadata)
        print(
            f"\n[{timestamp}] 🚨 ASSIGNED {metadata['case_id']}/{metadata['task_id']} "
            f"{metadata['task_type']}"
        )
        print(f"    📂 {task_key}")
        print(f"    📤 {protocol.relative_posix(output_path)}")
        print(f"    📡 ACK (delivery accepted; not START) -> {lead}")
        print(f"    🧭 Environment: {execution_environment} | node={resolved_node_class}")
        if execution_environment == protocol.LEGACY_EXECUTION_ENVIRONMENT:
            print("    ⚠️ legacy task: execution environment was not governed at dispatch time")
        copy_to_clipboard(instruction)
        beep()

        # The durable handoff packet is always written. It is cheap, lives below
        # Git-ignored runtime storage, and gives any browser-less worker a
        # replayable path to finish the task — even if the interactive agent
        # launched but silently did nothing (the T900 failure mode).
        handoff_path = protocol.write_handoff(
            session=session,
            case_id=metadata["case_id"],
            task_id=metadata["task_id"],
            task_type=metadata["task_type"],
            execution_environment=execution_environment,
            current_state=current_state,
            task_path=task_path,
            output_path=output_path,
            instruction=instruction,
            reason="assigned task detected by watcher",
            transport=transport,
            lead_session=lead,
            execution_profile=metadata.get("execution_profile", "governed") or "governed",
            lane_id=metadata.get("lane_id", ""),
            inbox_dir=inbox_dir,
        )
        print(f"    📥 handoff: {protocol.relative_posix(handoff_path)}")

        # A supervisor (e.g. the host-2 resident watcher) can hook the fresh
        # handoff to launch a worker. The hook runs after the durable packet is
        # on disk, so a broken hook can never lose the ACK/handoff.
        if on_handoff is not None:
            try:
                on_handoff(handoff_path, instruction)
            except Exception as exc:  # noqa: BLE001 - isolate worker hook failures
                print(f"    ⚠️ on_handoff hook failed: {exc}")

        wants_agent = (
            transport in {"agent", "auto"}
            and bool(exec_program)
            and current_state == "ACK"
        )
        if wants_agent:
            exit_code = dispatch_cli(exec_program, exec_args, instruction, exec_timeout)
            if exit_code == 0:
                print("    ✅ CLI Agent exit=0")
            else:
                print(
                    f"    ⚠️ CLI Agent exit={exit_code}; falling back to file/CLI "
                    f"handoff at {protocol.relative_posix(handoff_path)}"
                )
        else:
            print("    🗂️ transport=file → worker must consume the handoff inbox")

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
    parser.add_argument(
        "--node-class",
        choices=["auto", "primary", "remote"],
        default="auto",
        help="execution node class; auto uses COLLAB_NODE_CLASS when set and otherwise defaults remote",
    )
    parser.add_argument(
        "--transport",
        choices=["auto", "agent", "file"],
        default="auto",
        help="auto: use agent when --exec-program is set, else file; "
        "agent: launch the interactive agent but always keep the file handoff; "
        "file: never launch an agent, only write the durable handoff inbox packet",
    )
    parser.add_argument(
        "--exec-timeout",
        type=float,
        default=600.0,
        help="seconds before the interactive agent is treated as failed and we fall back",
    )
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
    print("📥 Inbox:  .collab/runtime/inbox/<Session>/<CaseID>/<TaskID>.json")
    print(f"🚚 Transport: {args.transport}")
    print(f"🧭 Node: {resolve_node_class(args.node_class)} (requested={args.node_class})")
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
                transport=args.transport,
                exec_timeout=args.exec_timeout,
                node_class=args.node_class,
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
