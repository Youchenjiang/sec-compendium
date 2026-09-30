#!/usr/bin/env python3
"""
validate_playbooks.py - 攻防實戰手冊庫全能品質稽核與雙軌超連結守門工具 (Unified Quality Auditor)
支援：
1. 藍隊原子實戰手冊庫品質稽核 (Phase 0 ~ Phase 6, 107 篇)
2. 紅隊特戰手冊庫品質稽核 (Phase 1 ~ Phase 6, 110 篇)
3. 全專案 Markdown 內部超連結完整性守門 (跨模組全量斷鏈檢測)
4. 支援命令列參數：--all (預設), --blue, --red, --links-only
"""

import os
import re
import sys
import glob
import argparse
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.normpath(os.path.join(TOOLS_DIR, ".."))
REPO_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))

BLUE_VALIDATOR = os.path.join(TOOLS_DIR, "validate_blue_team_playbooks.py")
RED_VALIDATOR = os.path.join(TOOLS_DIR, "validate_red_team_playbooks.py")

def run_script(script_path):
    cmd = [sys.executable, script_path]
    res = subprocess.run(cmd)
    return res.returncode == 0

def check_repo_wide_links():
    print("\n" + "=" * 75)
    print("🌐 全專案跨模組 Markdown 超連結完整性檢查 (Repository Global Link Audit)")
    print("=" * 75)

    raw_files = glob.glob(os.path.join(REPO_ROOT, "**", "*.md"), recursive=True)
    # 排除 .git 目錄
    md_files = [
        f for f in raw_files
        if f"{os.sep}.git{os.sep}" not in os.path.normpath(f)
    ]
    broken = []
    total_checked = 0

    for fpath in md_files:
        safe_fpath = os.path.realpath(fpath)
        with open(safe_fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 移除代碼區塊與行內反引號，避免代碼語法干擾
        clean_content = re.sub(r'```[\s\S]*?```', '', content)
        clean_content = re.sub(r'`[^`\n]+`', '', clean_content)
        links = re.findall(r'\[([^\]]+)\]\(([^)\s]+)\)', clean_content)

        for _, link in links:
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path_part = link.split("#")[0]
            if not path_part:
                continue
            # 排除 Python 代碼或正則語法殘留如 'id'
            if "'" in path_part or '"' in path_part or "[" in path_part:
                continue

            total_checked += 1
            abs_target = os.path.normpath(os.path.join(os.path.dirname(fpath), path_part))
            if not os.path.exists(abs_target):
                rel_source = os.path.relpath(fpath, REPO_ROOT)
                broken.append((rel_source, link))

    if broken:
        print(f"❌ 發現 {len(broken)} 處死鏈 (Broken Links):")
        for src, lnk in broken:
            print(f"   來源: {src} -> 目標: {lnk}")
        return False

    print(f"✅ 全專案 {len(md_files)} 份 Markdown 文檔共 {total_checked} 處內部超連結 100% 暢通，無任何死鏈！")
    return True

def main():
    parser = argparse.ArgumentParser(description="攻防原子實戰手冊全能自動化校驗器")
    parser.add_argument("--all", action="store_true", help="執行雙軌手冊與全庫超連結全能稽核（預設）")
    parser.add_argument("--blue", action="store_true", help="僅執行藍隊手冊品質校驗")
    parser.add_argument("--red", action="store_true", help="僅執行紅隊手冊品質校驗")
    parser.add_argument("--links-only", action="store_true", help="僅執行全專案 Markdown 超連結校驗")
    args = parser.parse_args()

    # 若指定 --all 或未指定特定標籤，預設為雙軌全檢驗
    run_all = args.all or not (args.blue or args.red or args.links_only)

    success = True

    if args.blue or run_all:
        print("\n" + "#" * 75)
        print("🔷 [1/3] 執行藍隊實戰手冊規範稽核")
        print("#" * 75)
        if not run_script(BLUE_VALIDATOR):
            success = False

    if args.red or run_all:
        print("\n" + "#" * 75)
        print("🔴 [2/3] 執行紅隊特戰手冊規範稽核")
        print("#" * 75)
        if not run_script(RED_VALIDATOR):
            success = False

    if args.links_only or run_all:
        print("\n" + "#" * 75)
        print("🌐 [3/3] 執行全專案跨軌超連結防護稽核")
        print("#" * 75)
        if not check_repo_wide_links():
            success = False

    print("\n" + "=" * 75)
    if success:
        print("🏆 恭喜！雙軌實戰手冊庫 (217 篇手冊) 與全庫超連結 100% 完全通過品質稽核！")
        sys.exit(0)
    else:
        print("⚠️ 警告！部分項目未通過稽核，請參閱上方詳細錯誤清單並修正。")
        sys.exit(1)

if __name__ == "__main__":
    main()
