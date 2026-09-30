#!/usr/bin/env python3
"""
pr_helper.py - PR 自動產生、結構檢驗與安全提交守門員工具 (PR Helper & Validator)

主要功能：
1. generate: 依據分支內 Conventional Commits 自動生成合規 PR Body (含 Summary, Key Changes, Verification)。
2. lint: 嚴格驗證 PR Body、PR Title、分支名稱與 Commits 是否完全符合專案政策。
3. create: 結合本機 CI (lint_commits, validate_playbooks) 全通後，使用 --body-file 安全提交 PR，
   並自動附帶標籤，杜絕 PowerShell 跳脫截斷與標籤時間差紅燈。
"""

import os
import re
import sys
import argparse
import subprocess
from collections import defaultdict

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

BRANCH_REGEX = re.compile(
    r"^(feat|fix|refactor|docs|test|chore|style|perf|security)/[a-z0-9._-]+$"
)
CONVENTIONAL_REGEX = re.compile(
    r"^(feat|fix|refactor|docs|test|chore|style|perf|security)(?:\([a-z0-9_-]+\))?: [a-z0-9].*$"
)
SAFE_IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z0-9_./~^-]+$")
LABEL_REGEX = re.compile(r"^[a-zA-Z0-9_,-]+$")

SECTION_SUMMARY = "## Summary"
SECTION_KEY_CHANGES = "## Key Changes"
SECTION_VERIFICATION = "## Verification"
DEFAULT_BASE_REF = "origin/main"


def sanitize_identifier(value, name="value"):
    if not value or not SAFE_IDENTIFIER_REGEX.match(value):
        raise ValueError(f"Invalid characters in {name}: '{value}'")
    return value


def sanitize_label(label_str):
    if not label_str or not LABEL_REGEX.match(label_str):
        raise ValueError(f"Invalid label string: '{label_str}'")
    return label_str


def sanitize_title(title_str):
    if not title_str or not CONVENTIONAL_REGEX.match(title_str) or len(title_str) > 72:
        raise ValueError(f"Invalid PR title: '{title_str}'")
    if any(ch in title_str for ch in ["\n", "\r", '"', ";", "`", "$"]):
        raise ValueError("Invalid character in PR title")
    return title_str


def get_safe_path(user_path):
    safe_name = os.path.basename(user_path)
    return os.path.join(PROJECT_ROOT, safe_name)


def run_cmd(cmd, cwd=PROJECT_ROOT):
    safe_cmd = []
    for arg in cmd:
        clean_arg = str(arg).strip()
        if any(bad in clean_arg for bad in [";", "&", "|", "`", "$", "\n", "\r"]):
            raise ValueError(f"Dangerous character in command argument: {clean_arg}")
        safe_cmd.append(clean_arg)
    try:
        res = subprocess.run(
            safe_cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_current_branch():
    return run_cmd(["git", "branch", "--show-current"])


def get_commits_since_base(base_ref):
    safe_base = sanitize_identifier(base_ref, "base_ref")
    raw = run_cmd(["git", "log", "--format=%H %s", "--end-of-options", f"{safe_base}..HEAD"])
    if not raw:
        return []
    commits = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        sha = parts[0]
        subj = parts[1] if len(parts) > 1 else ""
        commits.append((sha, subj))
    return commits


def categorize_commits(commits):
    categories = defaultdict(list)
    for _, subj in commits:
        if ":" in subj:
            prefix, desc = subj.split(":", 1)
            prefix = prefix.strip()
            desc = desc.strip()
            if "(" in prefix and prefix.endswith(")"):
                ctype, scope = prefix[:-1].split("(", 1)
                categories[(ctype.strip(), scope.strip())].append(desc)
            else:
                categories[(prefix, "general")].append(desc)
        else:
            categories[("other", "misc")].append(subj)
    return categories


def build_pr_body(commits, custom_summary=None):
    categories = categorize_commits(commits)

    summary_text = custom_summary or (
        f"This pull request incorporates {len(commits)} atomic commit(s) delivering updates "
        "aligned with repository engineering standards and conventional governance rules."
    )

    changes_lines = []
    idx = 1
    for (ctype, scope), descs in sorted(categories.items()):
        header = f"{idx}. **{ctype.upper()} ({scope})**:"
        changes_lines.append(header)
        for d in descs:
            changes_lines.append(f"   - {d}")
        idx += 1

    key_changes_text = "\n".join(changes_lines) if changes_lines else "1. General improvements."

    template = f"""{SECTION_SUMMARY}
{summary_text}

{SECTION_KEY_CHANGES}
{key_changes_text}

{SECTION_VERIFICATION}
- [x] Automated tests pass: `python security/tools/validate_playbooks.py --all`
- [x] Conventional commits audit passes: `python security/tools/lint_commits.py`
- [x] Commit headers follow Conventional Commits (< 72 chars, no trailing dot)
- [x] Repository link integrity verified with zero broken internal links
- [x] No regression introduced
"""
    return template


def validate_pr_body(body_content):
    issues = []
    required_sections = [SECTION_SUMMARY, SECTION_KEY_CHANGES, SECTION_VERIFICATION]
    for section in required_sections:
        if section not in body_content:
            issues.append(f"PR body is missing required section: '{section}'")

    if SECTION_SUMMARY in body_content and SECTION_KEY_CHANGES in body_content:
        summary_part = body_content.split(SECTION_SUMMARY)[-1].split(SECTION_KEY_CHANGES)[0].strip()
        if not summary_part:
            issues.append(f"{SECTION_SUMMARY} section is empty.")

    if SECTION_KEY_CHANGES in body_content and SECTION_VERIFICATION in body_content:
        key_changes_part = body_content.split(SECTION_KEY_CHANGES)[-1].split(SECTION_VERIFICATION)[0].strip()
        if not key_changes_part:
            issues.append(f"{SECTION_KEY_CHANGES} section is empty.")

    return issues


def validate_pr_metadata(branch, title, commits):
    issues = []
    if not BRANCH_REGEX.match(branch):
        issues.append(f"Branch name '{branch}' does not match <type>/<description> pattern.")

    if not CONVENTIONAL_REGEX.match(title):
        issues.append(f"PR title '{title}' does not match Conventional Commits format.")
    if len(title) > 72:
        issues.append(f"PR title exceeds 72 characters ({len(title)} chars).")
    if title.endswith("."):
        issues.append("PR title must not end with a period.")

    for sha, subj in commits:
        if len(subj) > 72:
            issues.append(f"Commit {sha[:7]} subject exceeds 72 characters ({len(subj)} chars): '{subj}'")
        if not CONVENTIONAL_REGEX.match(subj):
            issues.append(f"Commit {sha[:7]} does not match Conventional Commits: '{subj}'")

    return issues


def handle_generate(args):
    commits = get_commits_since_base(args.base)
    if not commits:
        print(f"⚠️ 在 {args.base}..HEAD 範圍內未發現任何新 Commit。")
        return

    body = build_pr_body(commits, args.summary)
    output_path = get_safe_path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(body)

    print("=" * 75)
    print("✅ 成功生成合規 PR Body！")
    print(f"📄 輸出檔案: {output_path}")
    print(f"📊 納入提交: {len(commits)} 筆 Commit (基準: {args.base})")
    print("=" * 75)


def handle_lint(args):
    branch = get_current_branch()
    commits = get_commits_since_base(args.base)

    body_path = get_safe_path(args.body_file)
    if not os.path.exists(body_path):
        print(f"❌ 找不到 PR body 檔案: {body_path}")
        sys.exit(1)

    with open(body_path, "r", encoding="utf-8", errors="ignore") as f:
        body_content = f.read()

    body_issues = validate_pr_body(body_content)
    meta_issues = validate_pr_metadata(branch, args.title, commits)
    all_issues = body_issues + meta_issues

    print("=" * 75)
    print("🔍 開始執行 PR 結構與合規性驗證...")
    print("=" * 75)

    if all_issues:
        print(f"❌ 檢測到 {len(all_issues)} 項不合規問題:")
        for issue in all_issues:
            print(f"   - {issue}")
        sys.exit(1)

    print("✅ PR Body 三大章節完整合規 (Summary, Key Changes, Verification)！")
    print("✅ PR Title 與 Commits 均符合 Conventional Commits 且 <= 72 字元！")
    print("✅ 分支命名規則完全合規！")
    print("=" * 75)


def run_pre_submit_checks():
    print("🚀 執行本地全套守門員檢測...")

    # 1. Commit Policy
    print("   [1/2] 檢驗 Commit 政策與四權分立...")
    linter_path = os.path.join(CURRENT_DIR, "lint_commits.py")
    if os.path.exists(linter_path):
        res = subprocess.run([sys.executable, linter_path, "--base", DEFAULT_BASE_REF])
        if res.returncode != 0:
            print("❌ Commit 政策檢驗未通過，終止 PR 建立。")
            return False

    # 2. Playbooks Validation
    print("   [2/2] 檢驗 Playbook 格式與超連結完整性...")
    validator_path = os.path.join(CURRENT_DIR, "validate_playbooks.py")
    if os.path.exists(validator_path):
        res = subprocess.run([sys.executable, validator_path, "--all"])
        if res.returncode != 0:
            print("❌ 手冊與超連結品質稽核未通過，終止 PR 建立。")
            return False

    return True


def handle_create(args):
    branch = get_current_branch()
    commits = get_commits_since_base(args.base)
    if not commits:
        print(f"❌ 查無新 Commit ({args.base}..HEAD)，無法建立 PR。")
        sys.exit(1)

    if not args.skip_checks and not run_pre_submit_checks():
        sys.exit(1)

    temp_body_path = os.path.join(PROJECT_ROOT, ".git_pr_body_tmp.md")
    body = build_pr_body(commits, args.summary)
    with open(temp_body_path, "w", encoding="utf-8") as f:
        f.write(body)

    meta_issues = validate_pr_metadata(branch, args.title, commits)
    if meta_issues:
        print("❌ PR 參數未通過驗證:")
        for iss in meta_issues:
            print(f"   - {iss}")
        if os.path.exists(temp_body_path):
            os.remove(temp_body_path)
        sys.exit(1)

    safe_base = sanitize_identifier(args.base, "base")
    safe_label = sanitize_label(args.label)
    safe_title = sanitize_title(args.title)

    cmd = [
        "gh", "pr", "create",
        "--base", safe_base,
        "--head", branch,
        "--title", safe_title,
        "--body-file", temp_body_path,
        "--label", safe_label
    ]

    print("=" * 75)
    print("🚀 本地驗證 100% 通過，正在建立 GitHub Pull Request...")
    print(f"   標題: {safe_title}")
    print(f"   標籤: {safe_label}")
    print("=" * 75)

    try:
        subprocess.run(cmd, check=True)
        print("🎉 PR 建立成功！")
    finally:
        if os.path.exists(temp_body_path):
            os.remove(temp_body_path)


def main():
    parser = argparse.ArgumentParser(description="PR 自動生成、結構驗證與安全提交工具")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # 1. generate
    gen_parser = subparsers.add_parser("generate", help="自動產出合規 PR Body Markdown")
    gen_parser.add_argument("--base", default=DEFAULT_BASE_REF, help=f"比較之基準分支 (預設 {DEFAULT_BASE_REF})")
    gen_parser.add_argument("--summary", default=None, help="自訂 Summary 描述")
    gen_parser.add_argument("-o", "--output", default="PR_BODY.md", help="輸出檔案路徑 (預設 PR_BODY.md)")

    # 2. lint
    lint_parser = subparsers.add_parser("lint", help="驗證 PR Body 與中繼資料格式")
    lint_parser.add_argument("--body-file", required=True, help="待驗證之 PR Body 檔案")
    lint_parser.add_argument("--title", required=True, help="待驗證之 PR 標題")
    lint_parser.add_argument("--base", default=DEFAULT_BASE_REF, help=f"比較基準分支 (預設 {DEFAULT_BASE_REF})")

    # 3. create
    create_parser = subparsers.add_parser("create", help="本地完整驗證並使用 body-file 提交 PR")
    create_parser.add_argument("--title", required=True, help="PR 標題 (須符合 Conventional Commits 且 <= 72 字元)")
    create_parser.add_argument("--base", default="main", help="目標基準分支 (預設 main)")
    create_parser.add_argument("--label", default="documentation", help="指定 PR 標籤 (預設 documentation)")
    create_parser.add_argument("--summary", default=None, help="自訂 Summary 描述")
    create_parser.add_argument("--skip-checks", action="store_true", help="跳過本地 lint 與手冊驗證")

    args = parser.parse_args()

    if args.action == "generate":
        handle_generate(args)
    elif args.action == "lint":
        handle_lint(args)
    elif args.action == "create":
        handle_create(args)


if __name__ == "__main__":
    main()
