#!/usr/bin/env python3
"""
collab_watch.py - Multi-Agent Mailbox Watcher & Auto-Dispatcher
監聽 .collab/inboxes/[role] 目錄，當有新任務落地時，自動觸發 Agent 或發出桌面提示。

用法範例：
  1. 純監聽提示（適用 Cursor / Windsurf）：
     python security/tools/collab_watch.py --role subagent_1_triage

  2. 全自動調用 CLI Agent（適用 Claude Code / Aider 等）：
     python security/tools/collab_watch.py --role subagent_2_reverse --exec "claude -p"
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 定位專案根目錄
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
COLLAB_DIR = REPO_ROOT / ".collab"
INBOXES_DIR = COLLAB_DIR / "inboxes"
OUTBOXES_DIR = COLLAB_DIR / "outboxes"

def beep():
    """發出終端提示音"""
    if sys.platform == "win32":
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            sys.stdout.write("\a")
            sys.stdout.flush()
    else:
        sys.stdout.write("\a")
        sys.stdout.flush()

def copy_to_clipboard(text: str):
    """將文字複製到系統剪貼簿 (跨平台相容)"""
    try:
        if sys.platform == "win32":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Mailbox Watcher")
    parser.add_argument("--role", required=True, 
                        choices=["subagent_1_triage", "subagent_2_reverse", "subagent_3_review", "main_engine"],
                        help="指定要監聽的角色收件匣名稱")
    parser.add_argument("--interval", type=float, default=1.5, help="輪巡間隔秒數 (預設: 1.5 秒)")
    parser.add_argument("--exec", dest="exec_cmd", default=None, help="可選: 偵測到任務時自動呼叫的 CLI Agent 命令 (例: 'claude -p')")
    
    args = parser.parse_args()

    target_inbox = INBOXES_DIR / args.role
    target_outbox = OUTBOXES_DIR / args.role
    
    target_inbox.mkdir(parents=True, exist_ok=True)
    target_outbox.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"🤖 Collab Watcher 已啟動！正在監聽角色: [{args.role}]")
    print(f"📂 監聽收件匣: {target_inbox}")
    print(f"📤 成果寄件匣: {target_outbox}")
    print(f"⏱️ 輪巡間隔: {args.interval} 秒")
    if args.exec_cmd:
        print(f"⚡ 自動執行模式: '{args.exec_cmd}'")
    else:
        print("🔔 提示模式: 偵測到任務將發出聲音提示並自動複製指令至剪貼簿")
    print("=" * 60)
    print("🟢 等待新任務中... (按 Ctrl+C 可停止)")

    seen_files = set(f.name for f in target_inbox.iterdir() if f.is_file() and not f.name.startswith("."))

    while True:
        try:
            time.sleep(args.interval)
            current_files = set(f.name for f in target_inbox.iterdir() if f.is_file() and not f.name.startswith("."))
            new_files = current_files - seen_files

            for new_file in sorted(new_files):
                task_path = target_inbox / new_file
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] 🚨 收到新任務！檔案: {new_file}")

                # 讀取任務標題
                try:
                    with open(task_path, "r", encoding="utf-8") as f:
                        first_line = f.readline().strip()
                        print(f"    📋 任務摘要: {first_line}")
                except Exception:
                    pass

                beep()

                # 自動生成觸發語法
                one_liner = f"請讀取 {task_path.as_posix()} 進行分析，並將結果輸出至 {target_outbox.as_posix()}/FINDING_{new_file}"
                copy_to_clipboard(one_liner)
                print(f"    📋 已將一鍵指令複製到剪貼簿！可在 IDE 直接按 Ctrl+V 貼上。")

                # 若指定了自動執行 CLI Agent
                if args.exec_cmd:
                    print(f"    🚀 自動啟動 CLI Agent 執行分析...")
                    full_cmd = f"{args.exec_cmd} \"{one_liner}\""
                    try:
                        subprocess.run(full_cmd, shell=True, cwd=str(REPO_ROOT))
                        print(f"    ✅ Agent 執行完畢！")
                    except Exception as e:
                        print(f"    ❌ Agent 執行失敗: {e}")

                seen_files.add(new_file)

        except KeyboardInterrupt:
            print("\n🛑 監聽已停止。")
            break
        except Exception as e:
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
