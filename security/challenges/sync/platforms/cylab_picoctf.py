"""
picoCTF / CyLab Security Academy Platform Adapter

Parses and normalizes the full picoCTF / CMU CyLab challenge dataset across
all core competition domains: Binary Exploitation, Reverse, Web, Forensics, Crypto.
"""

import csv
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import format_markdown_table, write_markdown_file


class CyLabAdapter(BaseChallengeAdapter):
    platform_id = "cylab_picoctf"
    display_name = "picoCTF / CyLab Academy"

    DIFF_MAP = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard",
        "4": "Insane",
    }

    def fetch_challenges(self) -> List[ChallengeItem]:
        csv_path = self.target_dir / "cylab_all_challenges_2026-08-08.csv"
        if not csv_path.exists():
            print(f"  [Warn] CyLab CSV snapshot not found at {csv_path}")
            return []

        items: List[ChallengeItem] = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                c_id = row.get("ID", "").strip()
                title = row.get("題目名稱", "").strip()
                category = row.get("分類", "").strip()
                raw_diff = row.get("難易度", "1").strip()
                difficulty = self.DIFF_MAP.get(raw_diff, f"Level {raw_diff}")
                points = row.get("分數", "0").strip()
                author = row.get("作者", "").strip()
                solves = row.get("全站解出人數", "0").strip()
                source = row.get("事件/出處", "").strip()

                encoded_title = urllib.parse.quote(title)
                url = f"https://learn.cylabacademy.org/library?search={encoded_title}"
                desc = f"出處：{source} ｜ 配分：{points} pts ｜ 全站通關：{solves} 人 ｜ 作者：{author}"

                items.append(
                    ChallengeItem(
                        id=f"pico-{c_id}",
                        title=title,
                        platform=self.platform_id,
                        tier="🟢 FREE",
                        difficulty=difficulty,
                        category=category,
                        url=url,
                        description=desc,
                        extra={
                            "numeric_id": c_id,
                            "points": points,
                            "solves": solves,
                            "source": source,
                            "author": author,
                        },
                    )
                )

        print(f"  [CyLab/picoCTF] Normalized {len(items)} challenges from official snapshot.")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        catalog_path = self.target_dir / "cylab_all_challenges_catalog.md"

        # Output Markdown Catalog
        table_headers = [
            "題號 ID",
            "題目名稱 (Title)",
            "領域分類 (Category)",
            "難度等級",
            "分數 (Points)",
            "賽事出處 / 活動",
        ]
        table_rows = [
            [
                f"`{c.extra.get('numeric_id', c.id)}`",
                f"**[{c.title}]({c.url})**",
                c.category,
                f"`{c.difficulty}`",
                f"{c.extra.get('points', '')} pts",
                c.extra.get("source", ""),
            ]
            for c in challenges
        ]
        table_md = format_markdown_table(table_headers, table_rows)

        content = f"""# 🚩 picoCTF / CMU CyLab Security Academy 全量題庫目錄

> 來源依據：CMU CyLab & picoCTF 官方題庫數據庫  
> 統計：收錄共 **{len(challenges)} 道** 經典 CTF 實戰題目，**100% 完全免費公開**。

對齊檔案：[`cylab_all_challenges_2026-08-08.csv`](cylab_all_challenges_2026-08-08.csv) ｜ 學習路徑：[`cylab_learning_paths_catalog.md`](cylab_learning_paths_catalog.md)

---

## 🟢 {len(challenges)} 題完全免費競賽演練題庫目錄

{table_md}
"""
        write_markdown_file(catalog_path, content)

        return [catalog_path]
