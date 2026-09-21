"""
PortSwigger Web Security Academy Platform Adapter

Extracts and catalogs all official hands-on vulnerability labs across 30+ topics:
SQLi, XSS, CSRF, SSRF, XXE, Deserialization, HTTP Request Smuggling, etc.
"""

import re
from pathlib import Path
from typing import Any, Dict, List

from ..base import BaseChallengeAdapter
from ..models import ChallengeItem
from ..writers import format_markdown_table, write_csv, write_markdown_file


class PortSwiggerAdapter(BaseChallengeAdapter):
    platform_id = "portswigger"
    display_name = "PortSwigger Web Security Academy"

    def fetch_challenges(self) -> List[ChallengeItem]:
        checklist_path = (
            self.repo_root
            / "tracks"
            / "lab"
            / "90_runs"
            / "checklists"
            / "portswigger_90_runs.md"
        )

        if not checklist_path.exists():
            print(f"  [Warn] Checklist file not found at {checklist_path}")
            return []

        with open(checklist_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        items: List[ChallengeItem] = []
        current_topic = "General Web Security"
        current_difficulty = "Practitioner"

        for line in lines:
            line_str = line.strip()

            # Detect topic headers like: ### 📌 SQL Injection（18 Labs）
            topic_match = re.match(r"^###\s+📌?\s*([^（\(]+)", line_str)
            if topic_match:
                current_topic = topic_match.group(1).strip()
                current_difficulty = "Practitioner"  # default
                continue

            # Detect difficulty section headers like: #### Apprentice（先做）
            diff_match = re.match(r"^####\s*([A-Za-z]+)", line_str)
            if diff_match:
                current_difficulty = diff_match.group(1).strip()
                continue

            # Detect lab entries like: - [ ] [SQL injection vulnerability...](https://portswigger.net/...) `Apprentice`
            lab_match = re.search(
                r"-\s*\[[ xX/]\]\s*\[(.*?)\]\((https://portswigger\.net/[^\)]+)\)(.*)",
                line_str,
            )
            if lab_match:
                title = lab_match.group(1).strip()
                url = lab_match.group(2).strip()
                trailing = lab_match.group(3).strip()

                difficulty = current_difficulty
                # Check if difficulty is explicitly tagged in trailing text like `Apprentice` or `Expert`
                tag_match = re.search(r"`(Apprentice|Practitioner|Expert)`", trailing)
                if tag_match:
                    difficulty = tag_match.group(1)

                slug = url.rstrip("/").split("/")[-1]

                items.append(
                    ChallengeItem(
                        id=f"portswigger-{slug}",
                        title=title,
                        platform=self.platform_id,
                        tier="🟢 FREE",
                        difficulty=difficulty,
                        category=current_topic,
                        url=url,
                        description=f"PortSwigger Web Security Academy lab on {current_topic} ({difficulty} tier).",
                        extra={"slug": slug, "topic": current_topic},
                    )
                )

        print(f"  [PortSwigger] Extracted {len(items)} official labs across topics.")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "portswigger_all_labs_2026.csv"
        md_path = self.target_dir / "portswigger_all_labs_catalog.md"

        # 1. Output CSV
        csv_headers = ["Topic", "Title", "Tier", "Difficulty", "URL", "Slug"]
        csv_rows = [
            [
                c.category,
                c.title,
                c.tier,
                c.difficulty,
                c.url,
                c.extra.get("slug", c.id),
            ]
            for c in challenges
        ]
        write_csv(csv_path, csv_headers, csv_rows)

        # 2. Output Markdown Catalog
        table_headers = ["序號", "實驗名稱 (Lab Title)", "領域主題", "難度等級", "存取權限"]
        table_rows = [
            [
                str(idx),
                f"**[{c.title}]({c.url})**",
                c.category,
                f"`{c.difficulty}`",
                c.tier,
            ]
            for idx, c in enumerate(challenges, 1)
        ]
        table_md = format_markdown_table(table_headers, table_rows)

        content = f"""# 🌐 PortSwigger Web Security Academy 官方題庫目錄

> 來源依據：[PortSwigger Web Security Academy](https://portswigger.net/web-security) 官方題庫  
> 統計：收錄共 **{len(challenges)} 個** 經典 Web 漏洞實戰靶場實驗，**100% 完全免費公開**。

與專案題庫對齊，本目錄已產出標準化之 CSV 檔案：[`portswigger_all_labs_2026.csv`](portswigger_all_labs_2026.csv)。

---

## 🟢 {len(challenges)} 個完全免費實戰靶場實驗清單

{table_md}
"""
        write_markdown_file(md_path, content)

        return [csv_path, md_path]
