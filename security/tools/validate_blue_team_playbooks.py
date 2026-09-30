#!/usr/bin/env python3
"""
validate_blue_team_playbooks.py - 藍隊原子實戰手冊庫自動化品質稽核工具
功能：
1. 檢驗全庫所有 107 篇 Blue Team Playbook 的 Markdown 程式碼圍欄 (```) 是否 100% 閉合。
2. 檢驗手冊行數與黃金規格篇幅 (>= 200 行，建議完整度 >= 350 行)。
3. 檢驗藍隊黃金七大規格關鍵字（案發現場破題、第一動~第五動、靶場實戰、過關驗收）。
4. 統計 Phase 0 ~ Phase 6 全量篇數與程式碼行數。
5. 稽核藍隊全庫內部 Markdown 超連結完整性，防杜死鏈。
"""

import os
import re
import sys
import glob

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
BLUE_TEAM_DIR = os.path.join(BASE_DIR, "knowledge", "blue_team")
PLAYBOOKS_DIR = os.path.join(BLUE_TEAM_DIR, "playbooks")

PHASES = [
    "phase_0_foundation",
    "phase_1_visibility",
    "phase_2_soc_triage",
    "phase_3_detection_eng",
    "phase_4_hunting_ir",
    "phase_5_deep_dfir",
    "phase_6_capstone"
]

GOLDEN_KEYWORDS = [
    "案發現場破題",
    "第一動",
    "第二動",
    "第三動",
    "第四動",
    "第五動",
    "靶場實戰",
    "過關驗收"
]

MIN_PLAYBOOK_LINES = 200
RECOMMENDED_PLAYBOOK_LINES = 350

def check_playbook_file(fpath):
    issues = []
    safe_fpath = os.path.realpath(fpath)
    with open(safe_fpath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        content = "".join(lines)

    # 1. 圍欄閉合檢查
    in_code = False
    fence_count = 0
    for line in lines:
        if line.strip().startswith("```"):
            fence_count += 1
            in_code = not in_code
    if in_code:
        issues.append(f"程式碼圍欄 (```) 未正常閉合 (共 {fence_count} 個標記，奇數)")

    # 2. 篇幅行數檢查
    total_lines = len(lines)
    if total_lines < MIN_PLAYBOOK_LINES:
        issues.append(
            f"未達最低行數門檻 ({total_lines}/{MIN_PLAYBOOK_LINES} 行, 建議完整度 >= {RECOMMENDED_PLAYBOOK_LINES} 行)"
        )

    # 3. 關鍵字完整度檢查
    missing_keywords = []
    for kw in GOLDEN_KEYWORDS:
        if kw not in content:
            missing_keywords.append(kw)
    if missing_keywords:
        issues.append(f"缺少必備作戰章節關鍵字: {', '.join(missing_keywords)}")

    return issues, total_lines, fence_count

def _extract_target_path(fpath, raw_link):
    link = raw_link.strip()
    if link.startswith(("http://", "https://", "mailto:", "#")):
        return None
    path_part = link.split("#")[0]
    if not path_part or any(char in path_part for char in ("'", '"', "[")):
        return None
    return os.path.normpath(os.path.join(os.path.dirname(fpath), path_part))

def _audit_file_links(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
        txt = fp.read()

    txt_no_code = re.sub(r"```[\s\S]*?```", "", txt)
    clean_content = re.sub(r'`[^`\n]+`', '', txt_no_code)
    links = re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", clean_content)

    checked = 0
    broken = []
    for _, raw_link in links:
        tgt = _extract_target_path(fpath, raw_link)
        if not tgt:
            continue
        checked += 1
        if not os.path.exists(tgt):
            rel_fpath = os.path.relpath(fpath, BASE_DIR)
            broken.append((rel_fpath, raw_link, tgt))
    return checked, broken

def check_link_integrity():
    md_files = glob.glob(os.path.join(BLUE_TEAM_DIR, "**", "*.md"), recursive=True)
    broken_links = []
    total_links = 0
    for fpath in md_files:
        count, broken = _audit_file_links(fpath)
        total_links += count
        broken_links.extend(broken)
    return total_links, broken_links

def _get_active_phase_files(pdir):
    raw_files = sorted(glob.glob(os.path.join(pdir, "**", "*.md"), recursive=True))
    return [
        f for f in raw_files
        if os.path.basename(f).lower() != "readme.md" and "ranges" not in os.path.normpath(f).split(os.sep)
    ]

def _audit_phase(phase):
    pdir = os.path.join(PLAYBOOKS_DIR, phase)
    if not os.path.isdir(pdir):
        print(f"⚠️ 找不到目錄: {pdir}")
        return 0, 0, False

    active_files = _get_active_phase_files(pdir)
    print(f"\n📂 檢測防禦階段: 【{phase}】 (發現 {len(active_files)} 篇 Playbook)")

    phase_lines = 0
    has_error = False
    for fpath in active_files:
        fname = os.path.basename(fpath)
        issues, flines, fences = check_playbook_file(fpath)
        phase_lines += flines
        if issues:
            has_error = True
            print(f"  ❌ [{fname}] ({flines} 行 | {fences} 圍欄):")
            for iss in issues:
                print(f"     - {iss}")
        else:
            print(f"  ✅ [{fname:<48}] ({flines:>4} 行 | {fences:>2} 圍欄)")

    return len(active_files), phase_lines, has_error

def _print_summary(phase_stats, total_playbooks, total_lines):
    print("\n" + "=" * 75)
    print("📊 統計總覽 (Executive Summary)")
    print("=" * 75)
    for phase, (p_count, p_lines) in phase_stats.items():
        avg_lines = (p_lines // p_count) if p_count > 0 else 0
        print(f"  • {phase:25s}: {p_count:2d} 篇 | 總行數: {p_lines:5d} 行 (平均: {avg_lines} 行/篇)")

    print("-" * 75)
    avg_total = (total_lines // total_playbooks) if total_playbooks > 0 else 0
    print(f"  🏁 藍隊全庫總計: {total_playbooks} 篇實戰手冊 | 總行數: {total_lines} 行 (平均: {avg_total} 行/篇)")
    print("=" * 75)

def _audit_and_report_links():
    print("\n" + "=" * 75)
    print("🔗 藍隊全庫 Markdown 超連結完整性檢查 (Link Integrity Audit)")
    print("=" * 75)
    total_links, broken_links = check_link_integrity()
    if broken_links:
        print(f"❌ 發現 {len(broken_links)} 處死鏈:")
        for src, lnk, _ in broken_links:
            print(f"  - 來源: {src} -> 鏈接: {lnk}")
        return True
    print(f"✅ 藍隊全庫共檢查 {total_links} 處內部超連結，100% 暢通，無任何死鏈！")
    return False

def main():
    print("=" * 75)
    print("🛡️  開始執行【藍隊原子實戰手冊庫】品質自動化稽核...")
    print("=" * 75)

    total_playbooks = 0
    total_lines = 0
    phase_stats = {}
    has_error = False

    for phase in PHASES:
        p_count, p_lines, p_err = _audit_phase(phase)
        total_playbooks += p_count
        total_lines += p_lines
        has_error = has_error or p_err
        phase_stats[phase] = (p_count, p_lines)

    _print_summary(phase_stats, total_playbooks, total_lines)
    link_err = _audit_and_report_links()
    has_error = has_error or link_err

    if has_error:
        print("\n❌ 稽核未通過，請修正上述問題！")
        sys.exit(1)

    print(f"\n🎉 恭喜！藍隊全庫 {total_playbooks} 篇原子手冊與全量鏈接 100% 通過品質稽核，格式與章節完全合規！")
    sys.exit(0)

if __name__ == "__main__":
    main()
