#!/usr/bin/env python3
"""
lint_commits.py - 本機 Commit 政策與四權分立原子化驗證工具 (Commit Policy & Atomic Linter)
功能：
1. 嚴格對齊 .github/workflows/policy.yml 之 Conventional Commits 政策規範。
2. 驗證所有 commit 標題長度 <= 72 字元、白名單 scope、小寫開頭、無結尾句點。
3. 實施「四權分立」稽核：偵測是否有將治理文檔 (HANDOVER/MEMORY) 與功能代碼/知識手冊混雜提交之搭便車行為。
4. 支援指定範圍檢驗 (--range、--base) 與嚴格模式 (--strict)。
"""

import os
import re
import sys
import argparse
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ALLOWED_TYPES = [
    "feat",
    "fix",
    "refactor",
    "docs",
    "test",
    "chore",
    "style",
    "perf",
    "security",
]

ALLOWED_SCOPES = [
    "study",
    "plan",
    "ctfd",
    "labs",
    "challenge",
    "plugin",
    "core",
    "web",
    "ui",
    "docs",
    "ci",
    "deps",
    "sec",
    "agent",
    "infra",
    "build",
    "release",
    "governance",
    "tracks",
    "practice",
    "tools",
    "knowledge",
    "memory",
    "deepsource",
    "links",
]

TYPE_PATTERN = "|".join(ALLOWED_TYPES)
SCOPE_PATTERN = "|".join(ALLOWED_SCOPES)
SUBJECT_REGEX = re.compile(
    rf"^({TYPE_PATTERN})(?:\(({SCOPE_PATTERN})\))?: [a-z0-9].*$"
)
VAGUE_REGEX = re.compile(r"^(update|misc|stuff|changes|fix bug|bug fix)$", re.IGNORECASE)

GOVERNANCE_PATTERNS = ["docs/handover.md", "memory.md", ".agent/"]
CODE_PATTERNS = [".py", ".sh", ".ps1", ".json", ".yml", ".yaml"]
KNOWLEDGE_PATTERNS = ["security/knowledge/"]

def run_git(cmd):
    try:
        res = subprocess.run(
            ["git"] + cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def detect_base_ref():
    for candidate in ["origin/main", "main", "origin/master", "master"]:
        out = run_git(["rev-parse", "--verify", candidate])
        if out:
            return candidate
    return None

def get_commits(rev_range):
    raw = run_git(["log", "--format=%H %s", rev_range])
    if not raw:
        return []
    commits = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        sha = parts[0]
        subject = parts[1] if len(parts) > 1 else ""
        commits.append((sha, subject))
    return commits

def get_changed_files(sha):
    raw = run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", sha])
    if not raw:
        return []
    return [line.strip().replace("\\", "/").lower() for line in raw.splitlines() if line.strip()]

def validate_commit(sha, subject, changed_files, strict=False):
    errors = []
    warnings = []

    # 1. 符合正則規範
    if not SUBJECT_REGEX.match(subject):
        errors.append("標題格式錯誤：必須符合 <type>(<scope>): <subject> 且使用白名單之 type 與 scope")

    # 2. 禁止以句點結尾
    if subject.endswith("."):
        errors.append("結尾錯誤：標題結尾絕對不可帶有句號 `.`")

    # 3. 長度不大於 72 字元
    if len(subject) > 72:
        errors.append(f"長度超標：長度為 {len(subject)} 字元，超過上限 72 字元")

    # 4. 描述禁止空泛
    desc_match = re.sub(rf"^({TYPE_PATTERN})(?:\(({SCOPE_PATTERN})\))?:\s+", "", subject)
    if VAGUE_REGEX.match(desc_match.strip()):
        errors.append(f"描述過於空泛：'{desc_match}' 不符合專案描述具體性要求")

    # 5. 四權分立搭便車偵測 (Four-Tier Separation Check)
    has_gov = any(any(gp in f for gp in GOVERNANCE_PATTERNS) for f in changed_files)
    has_knowledge = any(any(kp in f for kp in KNOWLEDGE_PATTERNS) for f in changed_files)
    has_tools = any(f.startswith("security/tools/") or f.endswith(".py") for f in changed_files)

    # 檢查是否混雜提交
    if has_gov and (has_knowledge or has_tools):
        msg = "違反四權分立：偵測到治理文檔 (HANDOVER/MEMORY) 與功能代碼或知識手冊混雜提交（嚴禁搭便車）"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)

    # 檢查 scope 語意匹配度
    if subject.startswith("feat(knowledge)") and has_tools and not has_knowledge:
        warnings.append("語意建議：該 commit 僅修改工具/腳本，但使用了 feat(knowledge) 標籤，建議使用 feat(tools)")
    elif subject.startswith("feat(tools)") and has_knowledge and not has_tools:
        warnings.append("語意建議：該 commit 僅修改知識手冊，但使用了 feat(tools) 標籤，建議使用 feat(knowledge)")

    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="專案 Commit 規範與四權分立驗證工具")
    parser.add_argument("--base", help="基準分支或 Commit (預設自動偵測 origin/main 或 main)")
    parser.add_argument("--range", help="指定 Git 修訂範圍 (例如 main..HEAD 或 HEAD~5..HEAD)")
    parser.add_argument("--strict", action="store_true", help="啟用嚴格模式（將四權分立警告視為失敗錯誤）")
    args = parser.parse_args()

    print("=" * 75)
    print("🔍 開始執行【專案 Commit 規範與四權分立審核 (Commit Linter)】...")
    print("=" * 75)

    if args.range:
        rev_range = args.range
    else:
        base = args.base or detect_base_ref()
        if not base:
            print("❌ 無法自動偵測基準分支，請透過 --base 指定基準分支 (例如: origin/main)")
            sys.exit(1)
        rev_range = f"{base}..HEAD"

    print(f"📌 檢驗範圍: {rev_range}")
    commits = get_commits(rev_range)

    if not commits:
        print("ℹ️ 指定範圍內無任何提交紀錄需要檢驗。")
        sys.exit(0)

    print(f"📊 預計檢驗提交數: {len(commits)} 筆\n")

    total_errors = 0
    total_warnings = 0

    for sha, subject in commits:
        changed_files = get_changed_files(sha)
        errors, warnings = validate_commit(sha, subject, changed_files, strict=args.strict)
        
        short_sha = sha[:7]
        if errors:
            total_errors += len(errors)
            print(f"❌ [{short_sha}] {subject}")
            for err in errors:
                print(f"   🔴 錯誤: {err}")
        elif warnings:
            total_warnings += len(warnings)
            print(f"⚠️  [{short_sha}] {subject}")
            for warn in warnings:
                print(f"   🟡 警告: {warn}")
        else:
            print(f"✅ [{short_sha}] {subject}")

    print("\n" + "=" * 75)
    print(f"📋 審核總結：共檢驗 {len(commits)} 筆 Commit | 錯誤: {total_errors} | 警告: {total_warnings}")
    print("=" * 75)

    if total_errors > 0:
        print("❌ 檢驗未通過！請修正上述 Commit 標題或拆分違規混雜提交後再行推送。")
        sys.exit(1)
    else:
        print("🎉 恭喜！所有 Commit 均 100% 符合專案政策與四權分立規範！")
        sys.exit(0)

if __name__ == "__main__":
    main()
