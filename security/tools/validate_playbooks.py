#!/usr/bin/env python3
"""
validate_playbooks.py - 藍隊原子實戰手冊庫自動化品質稽核工具
功能：
1. 檢驗全庫所有 Playbook 的 Markdown 程式碼圍欄 (```) 是否 100% 閉合。
2. 檢驗手冊行數與基礎篇幅。
3. 檢驗七大黃金規格關鍵字（案發現場破題、第一動~第五動、靶場實戰、過關驗收）。
4. 檢驗本地超連結有效性 (Broken Links 檢測)。
5. 統計各階段已完成篇數與程式碼行數。
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
PLAYBOOKS_DIR = os.path.join(BASE_DIR, "blue_team", "playbooks")

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
    with open(safe_fpath, "r", encoding="utf-8", errors="ignore") as f:  # skipcq: PTC-W6004
        lines = f.readlines()
        content = "".join(lines)

    # 1. 圍欄閉合檢查
    in_code = False
    fence_count = 0
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            fence_count += 1
    if in_code:
        issues.append("代碼圍欄未閉合 (Unbalanced code fences)")

    # 2. 行數檢查
    if len(lines) < MIN_PLAYBOOK_LINES:
        issues.append(
            f"未達最低行數門檻 ({len(lines)}/{MIN_PLAYBOOK_LINES} 行, 建議完整度 >= {RECOMMENDED_PLAYBOOK_LINES} 行)"
        )

    # 3. 七大規格關鍵字檢查
    missing_kw = []
    for kw in GOLDEN_KEYWORDS:
        if kw not in content:
            missing_kw.append(kw)
    if missing_kw:
        issues.append(f"缺少黃金規格章節: {', '.join(missing_kw)}")

    return len(lines), fence_count, issues

def check_broken_links():
    md_files = glob.glob(os.path.join(BASE_DIR, "blue_team", "**/*.md"), recursive=True)
    broken = []
    for fpath in md_files:
        safe_fpath = os.path.realpath(fpath)
        with open(safe_fpath, "r", encoding="utf-8", errors="ignore") as f:  # skipcq: PTC-W6004
            content = f.read()
        # 移除代碼區塊與行內反引號，避免如 `<?=$_GET[1]($_POST[2]);?>` 被正則誤判為 Markdown 連結
        clean_content = re.sub(r'```[\s\S]*?```', '', content)
        clean_content = re.sub(r'`[^`\n]+`', '', clean_content)
        links = re.findall(r'\[([^\]]+)\]\(([^)\s]+)\)', clean_content)
        for _, link in links:
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = link.split("#")[0]
            if not target_path:
                continue
            abs_target = os.path.normpath(os.path.join(os.path.dirname(fpath), target_path))
            if not os.path.exists(abs_target):
                rel_source = os.path.relpath(fpath, BASE_DIR)
                broken.append((rel_source, link))
    return broken

def audit_phase(phase):
    pdir = os.path.join(PLAYBOOKS_DIR, phase)
    if not os.path.exists(pdir):
        return 0, 0, True

    files = sorted(glob.glob(os.path.join(pdir, "**", "*.md"), recursive=True))
    active_files = [f for f in files if os.path.basename(f).lower() != "readme.md"]
    phase_lines = 0
    phase_passed = True

    print(f"\n📂 檢驗階段：{phase} (共 {len(active_files)} 篇實戰手冊)")
    for f in active_files:
        bname = os.path.basename(f)
        lines_cnt, fences, issues = check_playbook_file(f)
        phase_lines += lines_cnt

        if issues:
            phase_passed = False
            print(f"  ⚠️ [{bname}] ({lines_cnt} 行) -> {'; '.join(issues)}")
        else:
            print(f"  ✅ [{bname:<48}] ({lines_cnt:>4} 行 | {fences:>2} 圍欄)")

    return len(active_files), phase_lines, phase_passed

def audit_link_integrity():
    print("\n" + "=" * 75)
    print("🔗 全庫超連結完整性檢查 (Link Integrity Audit)")
    print("=" * 75)
    broken_links = check_broken_links()
    if broken_links:
        print(f"❌ 發現 {len(broken_links)} 處死鏈 (Broken Links):")
        for src, lnk in broken_links:
            print(f"   來源: {src} -> 目標: {lnk}")
        return False

    print("✅ 全庫所有內部超連結 100% 暢通，無任何死鏈！")
    return True

def main():
    print("=" * 75)
    print("🛡️  藍隊原子實戰手冊庫自動化品質稽核 (Playbooks Automated Validator)")
    print("=" * 75)

    total_playbooks = 0
    total_lines = 0
    phase_stats = {}
    all_passed = True

    for phase in PHASES:
        cnt, plines, passed = audit_phase(phase)
        if cnt > 0:
            phase_stats[phase] = (cnt, plines)
            total_playbooks += cnt
            total_lines += plines
            if not passed:
                all_passed = False

    links_passed = audit_link_integrity()
    if not links_passed:
        all_passed = False

    print("\n" + "=" * 75)
    print("📊 稽核總結報告")
    print("=" * 75)
    for p, (cnt, lcnt) in phase_stats.items():
        print(f" - {p:<25}: {cnt:>2} 篇 | 累計 {lcnt:>5} 行")
    print("-" * 75)
    print(f"手冊總數: {total_playbooks} 篇 | 程式碼總行數: {total_lines} 行")

    if all_passed:
        print("\n🎉 驗收結果：【ALL PASSED】所有手冊與連結完全符合品質基準線！")
        sys.exit(0)
    else:
        print("\n⚠️ 驗收結果：【ATTENTION】部分項目未達標，請檢閱上方警示進行優化。")
        sys.exit(1)

if __name__ == "__main__":
    main()
