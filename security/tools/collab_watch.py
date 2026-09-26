#!/usr/bin/env python3
"""Watch governed ``.collab/cases/*/tasks`` assignments for one AI session.

The watcher follows the v2.2 Governed Case Bus contract:

* tasks are immutable and live only under ``cases/<case>/tasks``;
* every task has exactly one ``Assignee Session``;
* normal work is written to ``findings/`` and REVIEW work to ``reviews/``;
* local watcher state lives under Git-ignored ``.collab/runtime/``.

Examples:

  python security/tools/collab_watch.py --session Session-C01-Triage
  python security/tools/collab_watch.py --session Session-C01-Review --case C01_BottleOut
  python security/tools/collab_watch.py --session Session-C01-Triage --once

Optional safe CLI dispatch (no shell=True):

  python security/tools/collab_watch.py --session Session-C01-Triage \
      --exec-program claude --exec-arg=-p
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
COLLAB_DIR = REPO_ROOT / ".collab"
CASES_DIR = COLLAB_DIR / "cases"
RUNTIME_DIR = COLLAB_DIR / "runtime" / "watchers"

SESSION_RE = re.compile(r"^[A-Za-z0-9._-]+$")
FIELD_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*[：:]\s*`(?P<value>[^`]+)`")
VALID_TASK_TYPES = {"DISCOVERY", "TRIAGE", "VERIFY", "REVERSE", "REVIEW"}


def parse_task_metadata(task_path: Path) -> dict[str, str]:
    """Return normalized metadata fields from one governed task file."""
    fields: dict[str, str] = {}
    for line in task_path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.match(line.strip())
        if match:
            fields[match.group("label").strip()] = match.group("value").strip()

    task_type = fields.get("任務類型") or fields.get("Task Type")
    metadata = {
        "task_id": fields.get("Task ID", ""),
        "task_type": task_type or "",
        "assignee_session": fields.get("Assignee Session", ""),
    }
    return metadata


def discover_assigned_tasks(
    cases_dir: Path,
    session: str,
    case_filters: set[str] | None = None,
) -> list[tuple[Path, dict[str, str]]]:
    """Discover valid tasks assigned exactly to ``session``."""
    assigned: list[tuple[Path, dict[str, str]]] = []
    if not cases_dir.exists():
        return assigned

    for case_dir in sorted(path for path in cases_dir.iterdir() if path.is_dir()):
        if case_dir.name == "C00_Template":
            continue
        if case_filters and case_dir.name not in case_filters:
            continue

        tasks_dir = case_dir / "tasks"
        if not tasks_dir.is_dir():
            continue

        for task_path in sorted(tasks_dir.glob("*.md")):
            if task_path.name.upper().startswith("README") or "TEMPLATE" in task_path.name.upper():
                continue

            metadata = parse_task_metadata(task_path)
            if metadata["assignee_session"] != session:
                continue
            if not metadata["task_id"]:
                raise ValueError(f"Assigned task is missing Task ID: {task_path}")
            if metadata["task_type"] not in VALID_TASK_TYPES:
                raise ValueError(
                    f"Assigned task has invalid task type {metadata['task_type']!r}: {task_path}"
                )
            assigned.append((task_path, metadata))

    return assigned


def output_path_for_task(task_path: Path, metadata: dict[str, str]) -> Path:
    """Return the governed output path for a task without creating it."""
    case_dir = task_path.parent.parent
    task_id = metadata["task_id"]
    if metadata["task_type"] == "REVIEW":
        return case_dir / "reviews" / f"REVIEW_{task_id}.md"
    return case_dir / "findings" / f"FINDING_{task_id}.md"


def load_seen(state_path: Path) -> set[str]:
    """Load local runtime watcher state. Corrupt state is treated as empty."""
    if not state_path.exists():
        return set()
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
        seen = payload.get("seen", [])
        return {item for item in seen if isinstance(item, str)}
    except (OSError, json.JSONDecodeError, AttributeError):
        return set()


def save_seen(state_path: Path, seen: set[str]) -> None:
    """Persist watcher state below Git-ignored ``.collab/runtime``."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"seen": sorted(seen)}
    state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def beep() -> None:
    """Emit a best-effort local notification sound."""
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
    """Best-effort cross-platform clipboard copy without failing the watcher."""
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


def relative_posix(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def build_one_liner(
    session: str,
    task_path: Path,
    output_path: Path,
    metadata: dict[str, str],
) -> str:
    """Build a role-neutral instruction that preserves v2.2 ownership."""
    return (
        f"你是 {session}。請讀取 {relative_posix(task_path)} 的 "
        f"{metadata['task_type']} 任務，依 evidence contract 完成分析，且只新增 "
        f"{relative_posix(output_path)}；不得修改 task、CASE_STATE.md、questions.md 或 "
        "SCOREBOARD.md。"
    )


def dispatch_cli(program: str, exec_args: list[str], instruction: str) -> int:
    """Dispatch one prompt without invoking a shell."""
    completed = subprocess.run(
        [program, *exec_args, instruction],
        cwd=str(REPO_ROOT),
        check=False,
    )
    return completed.returncode


def process_assignments(
    session: str,
    case_filters: set[str] | None,
    seen: set[str],
    state_path: Path,
    exec_program: str | None,
    exec_args: list[str],
) -> int:
    """Process newly assigned tasks once and return the number announced."""
    announced = 0
    assignments = discover_assigned_tasks(CASES_DIR, session, case_filters)

    for task_path, metadata in assignments:
        task_key = relative_posix(task_path)
        if task_key in seen:
            continue

        output_path = output_path_for_task(task_path, metadata)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if output_path.exists():
            print(
                f"[{timestamp}] ℹ️ 已存在輸出，標記為已看過: "
                f"{relative_posix(output_path)}"
            )
            seen.add(task_key)
            save_seen(state_path, seen)
            continue

        instruction = build_one_liner(session, task_path, output_path, metadata)
        print(
            f"\n[{timestamp}] 🚨 新指派 {metadata['task_type']} "
            f"{metadata['task_id']}: {task_key}"
        )
        print(f"    📤 Governed output: {relative_posix(output_path)}")
        copy_to_clipboard(instruction)
        beep()
        print("    📋 已將符合 v2.2 ownership 的指令複製到剪貼簿。")

        if exec_program:
            print(f"    🚀 執行 CLI Agent: {exec_program}")
            exit_code = dispatch_cli(exec_program, exec_args, instruction)
            print(f"    {'✅' if exit_code == 0 else '❌'} CLI Agent exit={exit_code}")

        seen.add(task_key)
        save_seen(state_path, seen)
        announced += 1

    return announced


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Governed .collab case-task watcher")
    parser.add_argument(
        "--session",
        required=True,
        help="本 watcher 所屬的唯一 Session 名稱，例如 Session-C01-Triage",
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        default=[],
        help="只監聽指定 case；可重複使用，例如 --case C01_BottleOut",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.5,
        help="輪巡間隔秒數（預設 1.5）",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="只掃描一次後退出，適合 smoke test / automation",
    )
    parser.add_argument(
        "--reset-seen",
        action="store_true",
        help="清除本 Session 的 runtime seen-state 後再掃描",
    )
    parser.add_argument(
        "--exec-program",
        default=None,
        help="可選：收到任務後執行的 CLI Agent 程式名稱或路徑（不經 shell）",
    )
    parser.add_argument(
        "--exec-arg",
        action="append",
        default=[],
        help="傳給 CLI Agent 的固定參數；可重複，例如 --exec-arg=-p",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not SESSION_RE.fullmatch(args.session):
        raise SystemExit(
            "--session 只允許英數、點、底線與連字號，避免 runtime state 路徑混淆"
        )
    if args.interval <= 0:
        raise SystemExit("--interval 必須大於 0")

    state_path = RUNTIME_DIR / f"{args.session}.json"
    if args.reset_seen and state_path.exists():
        state_path.unlink()
    seen = load_seen(state_path)
    case_filters = set(args.cases) or None

    print("=" * 72)
    print(f"🤖 Governed Collab Watcher | session={args.session}")
    print(f"📂 Task bus: {CASES_DIR / '<CaseID>' / 'tasks'}")
    print(f"💾 Seen state: {state_path}")
    print(f"🎯 Case filter: {', '.join(sorted(case_filters)) if case_filters else 'ALL'}")
    print("🔒 只處理 Assignee Session 精確匹配的 task；不修改 task/state/questions。")
    print("=" * 72)

    while True:
        try:
            process_assignments(
                session=args.session,
                case_filters=case_filters,
                seen=seen,
                state_path=state_path,
                exec_program=args.exec_program,
                exec_args=args.exec_arg,
            )
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
