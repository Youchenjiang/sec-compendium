#!/usr/bin/env python3
"""
CyberDefenders Challenge Catalog Sync Tool

Fetches all blue team challenges directly from CyberDefenders official API:
https://cyberdefenders.org/api/blueteam-ctf-challenges/

Generates:
1. security/challenges/cyberdefenders_all_challenges_2026.csv
2. security/challenges/cyberdefenders_learning_paths_catalog.md
3. security/challenges/cyberdefenders_all_challenges_catalog.md
"""

import csv
import json
import math
import os
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

API_URL_TEMPLATE = "https://cyberdefenders.org/api/blueteam-ctf-challenges/?page={page}&size={size}&sort=easiest-to-hardest"
PAGE_SIZE = 10


def fetch_page(page: int, size: int = PAGE_SIZE) -> dict:
    url = API_URL_TEMPLATE.format(page=page, size=size)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_labs() -> list:
    print("Fetching first page to determine total pagination...")
    first_resp = fetch_page(1)
    pagination = first_resp.get("data", {}).get("pagination", {})
    total_pages = pagination.get("total_pages", 1)
    total_items = pagination.get("total_items", 0)

    print(f"API Metadata: {total_pages} pages, {total_items} total challenges.")

    all_labs = list(first_resp.get("data", {}).get("labs", []))

    for page in range(2, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...", end="\r", flush=True)
        resp = fetch_page(page)
        labs = resp.get("data", {}).get("labs", [])
        all_labs.extend(labs)
        time.sleep(0.15)

    print(f"\nSuccessfully fetched {len(all_labs)} challenges from API.")
    return all_labs


def format_duration(seconds: int) -> str:
    if not seconds:
        return ""
    mins = int(round(seconds / 60))
    if mins < 60:
        return f"{mins}m"
    hours = mins // 60
    rem_mins = mins % 60
    if rem_mins == 0:
        return f"{hours}h"
    return f"{hours}h {rem_mins}m"


def write_csv(labs: list, output_path: Path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "tier", "is_retired", "diff", "time_min", "categories", "slug", "desc"])
        for lab in labs:
            tier = "PREMIUM" if lab.get("is_pro") else "FREE"
            diff = (lab.get("difficulty") or "Unknown").capitalize()
            seconds = lab.get("estimated_time_in_seconds") or 0
            time_min = int(round(seconds / 60))
            cats = "|".join(lab.get("categories") or [])
            slug = lab.get("slug") or ""
            desc = (lab.get("learning_objective") or "").replace("\r\n", " ").replace("\n", " ").strip()
            retired = "retired" if lab.get("is_retired") else "active"
            writer.writerow([lab.get("name"), tier, retired, diff, time_min, cats, slug, desc])
    print(f"Written CSV: {output_path}")


def write_learning_paths_catalog(labs: list, output_path: Path):
    free_labs = [lab for lab in labs if not lab.get("is_pro")]
    premium_labs = [lab for lab in labs if lab.get("is_pro")]

    total_count = len(labs)
    free_count = len(free_labs)
    premium_count = len(premium_labs)

    lines = [
        "# 🛡️ CyberDefenders 全題目索引與 Free / Premium 分類手冊",
        "",
        f"版本：2026 全量版 ｜ 題目總數：**{total_count} 題**（🟢 **{free_count} 題完全免費** ｜ 🔒 **{premium_count} 題需 Premium 訂閱**）",
        "",
        "與 `cylab_all_challenges_2026-08-08.csv` 對齊，本目錄已產出同構的 CSV 檔案：[`cyberdefenders_all_challenges_2026.csv`](cyberdefenders_all_challenges_2026.csv)。",
        "",
        "---",
        "",
        f"## 🟢 {free_count} 題完全免費題庫清單 (100% 可直接練習，免信用卡)",
        "",
        "| 序號 | 挑戰名稱 (Lab Title) | 難度 | 時長 | 領域分類 (Category) | 實戰情境概要 (Scenario) |",
        "| :---: | :--- | :---: | :---: | :--- | :--- |",
    ]

    for idx, lab in enumerate(free_labs, 1):
        name = lab.get("name", "")
        slug = lab.get("slug", "")
        url = f"https://cyberdefenders.org/blueteam-ctf-challenges/{slug}/"
        diff = f"`{(lab.get('difficulty') or 'Unknown').capitalize()}`"
        time_str = format_duration(lab.get("estimated_time_in_seconds") or 0)
        cats = ", ".join(lab.get("categories") or [])
        desc = (lab.get("learning_objective") or "").replace("\r\n", " ").replace("\n", " ").strip()
        lines.append(f"| {idx} | **[{name}]({url})** | {diff} | {time_str} | {cats} | {desc} |")

    lines.extend([
        "",
        "---",
        "",
        f"## 🔒 {premium_count} 題需 Premium 訂閱之挑戰 (進階研究與付費題庫清單)",
        "",
        "| 序號 | 挑戰名稱 (Lab Title) | 難度 | 時長 | 領域分類 (Category) | 實戰情境概要 (Scenario) |",
        "| :---: | :--- | :---: | :---: | :--- | :--- |",
    ])

    for idx, lab in enumerate(premium_labs, 1):
        name = lab.get("name", "")
        slug = lab.get("slug", "")
        url = f"https://cyberdefenders.org/blueteam-ctf-challenges/{slug}/"
        diff = f"`{(lab.get('difficulty') or 'Unknown').capitalize()}`"
        time_str = format_duration(lab.get("estimated_time_in_seconds") or 0)
        cats = ", ".join(lab.get("categories") or [])
        desc = (lab.get("learning_objective") or "").replace("\r\n", " ").replace("\n", " ").strip()
        lines.append(f"| {idx} | [{name}]({url}) | {diff} | {time_str} | {cats} | {desc} |")

    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written Catalog: {output_path}")


def write_all_challenges_catalog(labs: list, output_path: Path):
    free_labs = [lab for lab in labs if not lab.get("is_pro")]
    total_count = len(labs)
    free_count = len(free_labs)
    premium_count = total_count - free_count

    lines = [
        "# 🛡️ CyberDefenders 官方全量 256 題總目錄與 Free/Premium 分類表",
        "",
        f"> 來源依據：CyberDefenders 官方即時 API 提取 ｜ 統計：共 {total_count} 題，其中 **{free_count} 題完全免費 (Non-Premium)**，{premium_count} 題需 Premium 訂閱。",
        "",
        "| 序號 | 挑戰名稱 (Lab Title) | 存取權限 (Tier) | 難度 (Difficulty) | 預估時長 | 領域分類 (Category) | 核心情境與技術概要 (Scenario) |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |",
    ]

    for idx, lab in enumerate(free_labs, 1):
        name = lab.get("name", "")
        slug = lab.get("slug", "")
        url = f"https://cyberdefenders.org/blueteam-ctf-challenges/{slug}/"
        diff = f"`{(lab.get('difficulty') or 'Unknown').capitalize()}`"
        time_str = format_duration(lab.get("estimated_time_in_seconds") or 0)
        cats = ", ".join(lab.get("categories") or [])
        desc = (lab.get("learning_objective") or "").replace("\r\n", " ").replace("\n", " ").strip()
        lines.append(f"| {idx} | **[{name}]({url})** | 🟢 **FREE** | {diff} | {time_str} | {cats} | {desc} |")

    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written Free Catalog: {output_path}")


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    challenges_dir = repo_root / "security" / "challenges"
    challenges_dir.mkdir(parents=True, exist_ok=True)

    csv_path = challenges_dir / "cyberdefenders_all_challenges_2026.csv"
    learning_paths_path = challenges_dir / "cyberdefenders_learning_paths_catalog.md"
    all_challenges_path = challenges_dir / "cyberdefenders_all_challenges_catalog.md"

    labs = fetch_all_labs()
    write_csv(labs, csv_path)
    write_learning_paths_catalog(labs, learning_paths_path)
    write_all_challenges_catalog(labs, all_challenges_path)

    print("Sync completed successfully!")


if __name__ == "__main__":
    main()
