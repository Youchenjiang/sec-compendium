"""
Malware-Traffic-Analysis (MTA) Platform Adapter

Fetches real-world malware network packet (PCAP) exercises from:
https://www.malware-traffic-analysis.net/training-exercises.html
"""

import csv
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import write_markdown_file


class MTAAdapter(BaseChallengeAdapter):
    platform_id = "mta"
    display_name = "Malware-Traffic-Analysis (MTA)"

    BASE_URL = "https://www.malware-traffic-analysis.net/"
    INDEX_URL = BASE_URL + "training-exercises.html"

    def fetch_challenges(self) -> List[ChallengeItem]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        }
        req = urllib.request.Request(self.INDEX_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        lines = html.splitlines()
        items: List[ChallengeItem] = []
        seen_urls = set()

        for line in lines:
            m = re.findall(
                r'<a\s+[^>]*href=[\'"]([0-9]{4}/[0-9]{2}/[0-9]{2}/index\.html)[\'"][^>]*>(.*?)</a>',
                line,
            )
            if not m:
                continue

            rel_url = m[0][0]
            full_url = self.BASE_URL + rel_url
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            if len(m) >= 2:
                date_str = re.sub(r"<.*?>", "", m[0][1]).strip()
                title_str = re.sub(r"<.*?>", "", m[1][1]).strip()
            else:
                raw_text = re.sub(r"<.*?>", "", m[0][1]).strip()
                date_match = re.search(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", raw_text)
                date_str = date_match.group(1) if date_match else ""
                title_str = raw_text

            title_clean = title_str
            if "Traffic analysis exercise:" in title_clean:
                title_clean = title_clean.split("Traffic analysis exercise:", 1)[1].strip()

            items.append(
                ChallengeItem(
                    id=f"mta-{date_str}",
                    title=title_clean,
                    platform=self.platform_id,
                    tier="🟢 FREE",
                    difficulty="Medium" if "202" in date_str else "Easy",
                    category="Network Forensics / PCAP Analysis",
                    url=full_url,
                    description=title_str,
                    extra={
                        "date": date_str,
                        "full_title": title_str,
                        "relative_url": rel_url,
                    },
                )
            )

        print(f"  [MTA] Parsed {len(items)} distinct exercises.")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "mta_all_exercises_2026.csv"
        md_path = self.target_dir / "mta_all_exercises_catalog.md"

        # 1. Output CSV (preserving schema: date, title, full_title, url, relative_url)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "title", "full_title", "url", "relative_url"])
            for c in challenges:
                writer.writerow(
                    [
                        c.extra.get("date", ""),
                        c.title,
                        c.extra.get("full_title", c.title),
                        c.url,
                        c.extra.get("relative_url", ""),
                    ]
                )
        print(f"  [CSV] Saved {len(challenges)} entries -> {csv_path}")

        # 2. Output Markdown Catalog
        lines = [
            "# 📡 Malware-Traffic-Analysis.net (MTA) 惡意流量真實演練題庫清單",
            "",
            f"> 📌 **收錄題數**：{len(challenges)} 篇真實惡意流量分析演練（2014 ～ 2026 最新）  ",
            "> 📌 **平台特點**：100% 免登入、免訂閱、公開直接下載 pcap 封包（壓縮檔解壓密碼固定為 `infected`）  ",
            "> 📌 **官方首頁**：[Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/)",
            "",
            "---",
            "",
            "| 發布日期 | 演練題目名稱 (Exercise Title) | 線上題目與封包載點 (Pcap & Clues) |",
            "| :---: | :--- | :--- |",
        ]
        for c in challenges:
            date_str = c.extra.get("date", "")
            lines.append(f"| `{date_str}` | **{c.title}** | [👉 前往題目頁面]({c.url}) |")

        write_markdown_file(md_path, "\n".join(lines) + "\n")

        return [csv_path, md_path]
