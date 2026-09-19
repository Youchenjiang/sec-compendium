#!/usr/bin/env python3
"""
Malware-Traffic-Analysis (MTA) Training Exercises Sync Tool

Fetches all traffic analysis training exercises directly from:
https://www.malware-traffic-analysis.net/training-exercises.html

Generates:
1. security/challenges/mta_all_exercises_2026.csv
2. security/challenges/mta_all_exercises_catalog.md
"""

import csv
import os
import re
import sys
from pathlib import Path
import urllib.request
import urllib.error

BASE_URL = "https://www.malware-traffic-analysis.net/"
INDEX_URL = BASE_URL + "training-exercises.html"

def fetch_mta_exercises():
    print(f"Fetching MTA exercises index from {INDEX_URL}...")
    req = urllib.request.Request(
        INDEX_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    lines = html.splitlines()
    exercises = []
    seen_urls = set()

    for line in lines:
        m = re.findall(r'<a\s+[^>]*href=[\'"]([0-9]{4}/[0-9]{2}/[0-9]{2}/index\.html)[\'"][^>]*>(.*?)</a>', line)
        if not m:
            continue
        
        rel_url = m[0][0]
        full_url = BASE_URL + rel_url
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        if len(m) >= 2:
            date_str = re.sub(r'<.*?>', '', m[0][1]).strip()
            title_str = re.sub(r'<.*?>', '', m[1][1]).strip()
        else:
            raw_text = re.sub(r'<.*?>', '', m[0][1]).strip()
            # Extract date if present
            date_match = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2})', raw_text)
            date_str = date_match.group(1) if date_match else ""
            title_str = raw_text

        # Clean title prefix
        title_clean = title_str
        if "Traffic analysis exercise:" in title_clean:
            title_clean = title_clean.split("Traffic analysis exercise:", 1)[1].strip()

        exercises.append({
            "date": date_str,
            "title": title_clean,
            "full_title": title_str,
            "url": full_url,
            "relative_url": rel_url
        })

    print(f"Parsed {len(exercises)} distinct exercises.")
    return exercises

def save_csv(exercises, output_path: Path):
    fieldnames = ["date", "title", "full_title", "url", "relative_url"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(exercises)
    print(f"Saved CSV: {output_path} ({len(exercises)} rows)")

def save_markdown(exercises, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📡 Malware-Traffic-Analysis.net (MTA) 惡意流量真實演練題庫清單\n\n")
        f.write(f"> 📌 **收錄題數**：{len(exercises)} 篇真實惡意流量分析演練（2014 ～ 2026 最新）  \n")
        f.write("> 📌 **平台特點**：100% 免登入、免訂閱、公開直接下載 pcap 封包（壓縮檔解壓密碼固定為 `infected`）  \n")
        f.write("> 📌 **官方首頁**：[Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/)\n\n")
        f.write("---\n\n")
        f.write("| 發布日期 | 演練題目名稱 (Exercise Title) | 線上題目與封包載點 (Pcap & Clues) |\n")
        f.write("| :---: | :--- | :--- |\n")
        for ex in exercises:
            f.write(f"| `{ex['date']}` | **{ex['title']}** | [👉 前往題目頁面]({ex['url']}) |\n")
    print(f"Saved Markdown catalog: {output_path}")

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    challenges_dir = repo_root / "security" / "challenges"
    challenges_dir.mkdir(parents=True, exist_ok=True)

    exercises = fetch_mta_exercises()
    if not exercises:
        print("Error: No exercises fetched.")
        sys.exit(1)

    csv_path = challenges_dir / "mta_all_exercises_2026.csv"
    md_path = challenges_dir / "mta_all_exercises_catalog.md"

    save_csv(exercises, csv_path)
    save_markdown(exercises, md_path)
    print("MTA sync completed successfully!")

if __name__ == "__main__":
    main()
