#!/usr/bin/env python3
"""
validate_red_team_playbooks.py - 紅隊原子實戰手冊庫自動化品質稽核工具
功能：
1. 檢驗全庫所有 110 篇 Playbook 的 Markdown 程式碼圍欄 (```) 是否 100% 閉合。
2. 檢驗手冊行數與特戰速查規範篇幅 (150 ~ 210 行)。
3. 檢驗特戰速查關鍵字（作戰任務破題、第一動~第五動、實戰、驗收）。
4. 統計 Phase 1 ~ Phase 6 全量篇數與程式碼行數。
5. 稽核紅隊全庫內部 Markdown 超連結完整性，防杜死鏈。
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
RED_TEAM_DIR = os.path.join(BASE_DIR, "knowledge", "red_team")
PLAYBOOKS_DIR = os.path.join(RED_TEAM_DIR, "playbooks")

PHASES = [
    "phase_1_recon_surface",
    "phase_2_perimeter_web",
    "phase_3_domain_dominance",
    "phase_4_host_privesc",
    "phase_5_pivoting_c2",
    "phase_6_evasion_cloud"
]

GOLDEN_KEYWORDS = [
    "作戰任務破題",
    "第一動",
    "第二動",
    "第三動",
    "第四動",
    "第五動",
    "實戰",
    "驗收"
]

def check_playbook_file(fpath):
    issues = []
    safe_fpath = os.path.realpath(fpath)
    with open(safe_fpath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        content = "".join(lines)

    # 1. 圍欄閉合檢查
    in_code = False
    fence_count = 0
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            fence_count += 1
            in_code = not in_code
    if in_code:
        issues.append(f"程式碼圍欄 (```) 未閉合 (共 {fence_count} 個標記)")

    # 2. 篇幅行數檢查
    total_lines = len(lines)
    if total_lines < 140 or total_lines > 220:
        issues.append(f"手冊篇幅偏離特戰速查規範 (當前 {total_lines} 行，標準應在 150~210 行)")

    # 3. 關鍵字完整度檢查
    missing_keywords = []
    for kw in GOLDEN_KEYWORDS:
        if kw not in content:
            missing_keywords.append(kw)
    if missing_keywords:
        issues.append(f"缺少必備作戰章節關鍵字: {', '.join(missing_keywords)}")

    return issues, total_lines

def check_link_integrity():
    md_files = glob.glob(os.path.join(RED_TEAM_DIR, "**", "*.md"), recursive=True)
    broken_links = []
    total_links = 0

    for fpath in md_files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
            txt = fp.read()
        
        # 排除程式碼區塊內的偽鏈接
        txt_no_code = re.sub(r"```[\s\S]*?```", "", txt)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", txt_no_code)
        
        for text, link in links:
            link = link.strip()
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = link.split("#")[0]
            if not path_part:
                continue
            # 排除 Python 代碼或正則語法殘留如 'id'
            if "'" in path_part or '"' in path_part or "[" in path_part:
                continue

            total_links += 1
            tgt = os.path.normpath(os.path.join(os.path.dirname(fpath), path_part))
            if not os.path.exists(tgt):
                rel_fpath = os.path.relpath(fpath, BASE_DIR)
                broken_links.append((rel_fpath, link, tgt))

    return total_links, broken_links

def main():
    print("=" * 70)
    print("🔍 開始執行【紅隊原子實戰手冊庫】品質自動化稽核...")
    print("=" * 70)

    total_playbooks = 0
    total_lines = 0
    phase_stats = {}
    has_error = False

    for phase in PHASES:
        pdir = os.path.join(PLAYBOOKS_DIR, phase)
        if not os.path.isdir(pdir):
            print(f"⚠️ 找不到目錄: {pdir}")
            continue

        md_files = glob.glob(os.path.join(pdir, "**", "R*.md"), recursive=True)
        phase_playbooks = len(md_files)
        phase_lines = 0

        print(f"\n📂 檢測作戰階段: 【{phase}】 (發現 {phase_playbooks} 篇 Playbook)")

        for fpath in sorted(md_files):
            total_playbooks += 1
            fname = os.path.basename(fpath)
            issues, flines = check_playbook_file(fpath)
            phase_lines += flines
            total_lines += flines

            if issues:
                has_error = True
                print(f"  ❌ [{fname}] ({flines} 行):")
                for iss in issues:
                    print(f"     - {iss}")

        phase_stats[phase] = (phase_playbooks, phase_lines)

    print("\n" + "=" * 70)
    print("📊 統計總覽 (Executive Summary)")
    print("=" * 70)
    for phase, (p_count, p_lines) in phase_stats.items():
        avg_lines = (p_lines // p_count) if p_count > 0 else 0
        print(f"  • {phase:30s}: {p_count:2d} 篇 | 總行數: {p_lines:5d} 行 (平均: {avg_lines} 行/篇)")

    print("-" * 70)
    avg_total = (total_lines // total_playbooks) if total_playbooks > 0 else 0
    print(f"  🏁 全庫總計: {total_playbooks} 篇實戰手冊 | 總行數: {total_lines} 行 (平均: {avg_total} 行/篇)")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("🔗 紅隊全庫 Markdown 超連結完整性檢查 (Link Integrity Audit)")
    print("=" * 70)
    total_links, broken_links = check_link_integrity()
    if broken_links:
        has_error = True
        print(f"❌ 發現 {len(broken_links)} 處死鏈:")
        for src, lnk, tgt in broken_links:
            print(f"  - 來源: {src} -> 鏈接: {lnk}")
    else:
        print(f"✅ 紅隊全庫共檢查 {total_links} 處內部超連結，100% 暢通，無任何死鏈！")

    if has_error:
        print("\n❌ 稽核未通過，請修正上述問題！")
        sys.exit(1)
    else:
        print(f"\n🎉 恭喜！紅隊全庫 {total_playbooks} 篇特戰手冊與全量鏈接 100% 通過品質稽核，格式與章節完全合規！")
        sys.exit(0)

if __name__ == "__main__":
    main()
