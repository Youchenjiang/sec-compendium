#!/usr/bin/env python3
"""
Hack The Box Full Challenge Catalog Sync Tool

Fetches ALL challenges, machines, and sherlocks directly from Hack The Box API:
1. Starting Point Machines (14 total: 10 FREE, 4 VIP+)
2. Active Machines (20 FREE)
3. Retired Machines (532 VIP+)
4. Sherlocks DFIR Labs (231 total: 119 FREE, 112 VIP)
5. CTF Challenges (853 total: 210 FREE, 643 VIP)

Generates:
1. security/challenges/hackthebox_all_challenges_2026.csv (Full 1600+ dataset)
2. security/challenges/hackthebox_all_challenges_catalog.md (Verified Free subset)
"""

import csv
import json
import os
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

def load_env_token():
    # 1. Check environment variable
    token = os.environ.get("HTB_API_TOKEN")
    if token:
        return token
    # 2. Check local .env file
    repo_root = Path(__file__).resolve().parent.parent.parent
    env_file = repo_root / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("HTB_API_TOKEN=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

TOKEN = load_env_token()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_starting_point():
    print("1. Fetching Starting Point Machines...")
    candidates = [
        ("Meow", "Linux", "Very Easy", "Telnet 服務探測、無密碼 root 登入直接獲取 Flag"),
        ("Fawn", "Linux", "Very Easy", "FTP 服務枚舉、匿名訪客存取 (Anonymous Login) 下載機密檔案"),
        ("Dancing", "Windows", "Very Easy", "SMB 共享資源枚舉、無密碼訪客存取與管理員備份洩漏"),
        ("Explosion", "Windows", "Very Easy", "RDP 服務枚舉 (官方標註為 VIP+)"),
        ("Crocodile", "Linux", "Easy", "FTP 服務洩漏憑證、Web 管理後台預設帳密突破"),
        ("Responder", "Windows", "Easy", "Web LFI 本地檔案包含、LLMNR/NBT-NS 毒化、NTLM 雜湊捕捉提權"),
        ("Three", "Linux", "Easy", "子域名探勘、AWS S3 儲存貯體未授權寫入與 PHP WebShell"),
        ("Bike", "Linux", "Easy", "Node.js SSTI 模板注入 (官方標註為 VIP+)"),
        ("Vaccine", "Linux", "Easy", "SQL 注入攻擊 (SQLi)、資料庫密碼雜湊破解與 Sudo 提權"),
        ("Archetype", "Windows", "Easy", "MSSQL 滲透、xp_cmdshell 遠端指令執行、Windows 登錄檔密碼提權"),
        ("Oopsie", "Linux", "Easy", "Web 權限繞過、IDOR 不安全直接物件參考、SUID 二進位提權"),
        ("Markup", "Windows", "Easy", "XXE 實體注入攻擊 (官方標註為 VIP+)"),
        ("Included", "Linux", "Easy", "TFTP 服務利用與 UDP 滲透 (官方標註為 VIP+)"),
        ("Unified", "Linux", "Medium", "Log4j (CVE-2021-44228) 漏洞利用、UniFi 平台無檔案反彈 Shell")
    ]
    
    results = []
    for name, os_type, diff, desc in candidates:
        data = fetch_json(f"https://labs.hackthebox.com/api/v4/machine/profile/{name}")
        info = data.get("info", {}) if data else {}
        req_sub = info.get("requiredSubscription")
        is_free = (req_sub is None or req_sub != "VIP+") and not info.get("show_go_vip") and info.get("free") is not False
        results.append({
            "name": name,
            "category": "Starting Point (Machine)",
            "tier": "🟢 FREE" if is_free else "🔴 VIP+",
            "difficulty": diff,
            "os": os_type,
            "url": f"https://app.hackthebox.com/machines/{name}",
            "scenario": desc
        })
    print(f"   Fetched {len(results)} Starting Point machines.")
    return results

def get_active_machines():
    print("2. Fetching Active Machines (Current Free Rotation)...")
    data = fetch_json("https://labs.hackthebox.com/api/v4/machine/paginated?free=1&per_page=100")
    machines = data.get("data", []) if data else []
    results = []
    for m in machines:
        results.append({
            "name": m.get("name"),
            "category": "Machine (Active Pentest)",
            "tier": "🟢 FREE",
            "difficulty": m.get("difficultyText", "Unknown"),
            "os": m.get("os", "Linux"),
            "url": f"https://app.hackthebox.com/machines/{m.get('name')}",
            "scenario": f"當期線上常規主機攻堅演練 ({m.get('points')} pts) ｜ 發布日期: {m.get('release', '')[:10]}"
        })
    print(f"   Fetched {len(results)} Active machines.")
    return results

def get_retired_machines():
    print("3. Fetching Retired Machines (Archive VIP+)...")
    results = []
    page = 1
    while True:
        data = fetch_json(f"https://labs.hackthebox.com/api/v4/machine/list/retired/paginated?per_page=100&page={page}")
        if not data or not data.get("data"):
            break
        for m in data["data"]:
            results.append({
                "name": m.get("name"),
                "category": "Machine (Retired Archive)",
                "tier": "🔴 VIP+",
                "difficulty": m.get("difficultyText", "Unknown"),
                "os": m.get("os", "Linux"),
                "url": f"https://app.hackthebox.com/machines/{m.get('name')}",
                "scenario": f"歷史經典滲透主機歸檔（需 VIP+ 訂閱啟動）｜ 發布日期: {m.get('release', '')[:10]}"
            })
        last_page = data.get("meta", {}).get("last_page", 1)
        if page >= last_page:
            break
        page += 1
        time.sleep(0.05)
    print(f"   Fetched {len(results)} Retired machines.")
    return results

def get_sherlocks():
    print("4. Fetching Sherlocks (DFIR/SOC Labs)...")
    results = []
    page = 1
    while True:
        data = fetch_json(f"https://labs.hackthebox.com/api/v4/sherlocks?per_page=100&page={page}")
        if not data or not data.get("data"):
            break
        for s in data["data"]:
            state = s.get("state")
            is_free = state in ("active", "retired_free")
            results.append({
                "name": s.get("name"),
                "category": f"Sherlock ({s.get('category_name', 'DFIR')})",
                "tier": "🟢 FREE" if is_free else "🔴 VIP",
                "difficulty": (s.get("difficulty") or "Medium").capitalize(),
                "os": "Multi/Forensics",
                "url": f"https://app.hackthebox.com/sherlocks/{s.get('name')}",
                "scenario": f"藍隊事件響應與取證分析實戰（包含日誌、封包流量或記憶體映像檔分析，開放線上提交答案）"
            })
        last_page = data.get("meta", {}).get("last_page", 1)
        if page >= last_page:
            break
        page += 1
        time.sleep(0.05)
    print(f"   Fetched {len(results)} Sherlocks.")
    return results

def get_challenges():
    print("5. Fetching CTF Challenges...")
    results = []
    page = 1
    while True:
        data = fetch_json(f"https://labs.hackthebox.com/api/v4/challenges?per_page=100&page={page}")
        if not data or not data.get("data"):
            break
        for c in data["data"]:
            state = c.get("state")
            is_free = state in ("active", "retired_free")
            results.append({
                "name": c.get("name"),
                "category": f"Challenge ({c.get('category_name', 'General')})",
                "tier": "🟢 FREE" if is_free else "🔴 VIP",
                "difficulty": (c.get("difficulty") or "Medium").capitalize(),
                "os": "CTF Challenge",
                "url": f"https://app.hackthebox.com/challenges/{c.get('name')}",
                "scenario": f"獨立專題 CTF 解題挑戰（{c.get('category_name')} 領域實戰）"
            })
        last_page = data.get("meta", {}).get("last_page", 1)
        if page >= last_page:
            break
        page += 1
        time.sleep(0.05)
    print(f"   Fetched {len(results)} Challenges.")
    return results

def main():
    repo_root = Path("c:/Users/LabStrix/Documents/GitHub/Youchen/Security/ctfd-kit")
    challenges_dir = repo_root / "security" / "challenges"
    challenges_dir.mkdir(parents=True, exist_ok=True)

    output_csv = challenges_dir / "hackthebox_all_challenges_2026.csv"
    output_md = challenges_dir / "hackthebox_all_challenges_catalog.md"

    sp = get_starting_point()
    active_m = get_active_machines()
    retired_m = get_retired_machines()
    sherlocks = get_sherlocks()
    challenges = get_challenges()

    all_items = sp + active_m + retired_m + sherlocks + challenges
    free_items = [i for i in all_items if i["tier"] == "🟢 FREE"]
    vip_items = [i for i in all_items if "VIP" in i["tier"]]

    print(f"\n================ SUMMARY ================")
    print(f"Total Platform Challenges & Labs: {len(all_items)}")
    print(f"Total Completely FREE Labs:       {len(free_items)}")
    print(f"Total VIP / VIP+ Labs:            {len(vip_items)}")
    print(f"=========================================\n")

    # 1. Write Full CSV
    with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Tier", "Difficulty", "OS", "Category", "URL", "Scenario"])
        for item in all_items:
            writer.writerow([
                item["name"],
                item["tier"],
                item["difficulty"],
                item["os"],
                item["category"],
                item["url"],
                item["scenario"]
            ])
    print(f"Written Full CSV: {output_csv}")

    # 2. Write Markdown Catalog for Free Items
    lines = [
        "# 📦 Hack The Box 官方全量挑戰與 Free/VIP 目錄清單 (2026)",
        "",
        f"> 來源依據：Hack The Box 官方即時 API 全庫提取 ｜ 統計：全平台收錄共 **{len(all_items)}** 題（包含 Machines、Sherlocks、Challenges），其中 **{len(free_items)} 題完全免費可用 (Non-VIP)**，{len(vip_items)} 題標註為 VIP/VIP+ 需付費訂閱。",
        "",
        "| 序號 | 挑戰名稱 (Lab Title) | 存取權限 (Tier) | 難度 (Difficulty) | 作業系統 / 類型 | 領域分類 (Category) | 核心情境與技術概要 (Scenario) |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |"
    ]

    for idx, item in enumerate(free_items, 1):
        lines.append(
            f"| {idx} | **[{item['name']}]({item['url']})** | {item['tier']} | `{item['difficulty']}` | {item['os']} | {item['category']} | {item['scenario']} |"
        )

    lines.append("")
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written Free Catalog: {output_md}")

if __name__ == "__main__":
    main()
