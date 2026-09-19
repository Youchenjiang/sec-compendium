"""
CyberDefenders Platform Adapter

Fetches blue team DFIR and CTF labs from CyberDefenders official API:
https://cyberdefenders.org/api/blueteam-ctf-challenges/
"""

import json
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import format_markdown_table, write_csv, write_markdown_file


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


class CyberDefendersAdapter(BaseChallengeAdapter):
    platform_id = "cyberdefenders"
    display_name = "CyberDefenders"

    API_URL_TEMPLATE = "https://cyberdefenders.org/api/blueteam-ctf-challenges/?page={page}&size={size}&sort=easiest-to-hardest"
    PAGE_SIZE = 10

    def _fetch_page(self, page: int, retries: int = 3) -> dict:
        url = self.API_URL_TEMPLATE.format(page=page, size=self.PAGE_SIZE)
        if not url.lower().startswith(("http://", "https://")):
            raise ValueError(f"Insecure URL scheme: {url}")
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
            },
        )
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:  # skipcq: BAN-B310
                    return json.loads(resp.read().decode("utf-8"))
            except Exception:
                if attempt == retries - 1:
                    raise
                time.sleep(1.0 * (attempt + 1))
        return {}

    def fetch_challenges(self) -> List[ChallengeItem]:
        first_resp = self._fetch_page(1)
        pagination = first_resp.get("data", {}).get("pagination", {})
        total_pages = pagination.get("total_pages", 1)
        total_items = pagination.get("total_items", 0)

        print(f"  [API] Total CyberDefenders Labs: {total_items} across {total_pages} pages")

        all_labs = list(first_resp.get("data", {}).get("labs", []))

        for page in range(2, total_pages + 1):
            try:
                resp = self._fetch_page(page)
                labs = resp.get("data", {}).get("labs", [])
                all_labs.extend(labs)
            except Exception as e:
                print(f"  [Warn] Page {page} failed: {e}")
            time.sleep(0.15)

        items: List[ChallengeItem] = []
        for lab in all_labs:
            name = lab.get("name", "")
            slug = lab.get("slug", "")
            is_pro = lab.get("is_pro", False)
            tier = "🔒 PREMIUM" if is_pro else "🟢 FREE"

            diff = (lab.get("difficulty") or "Unknown").capitalize()
            seconds = lab.get("estimated_time_in_seconds") or 0
            time_str = format_duration(seconds)
            time_min = int(round(seconds / 60))

            cats_list = lab.get("categories") or []
            cats = ", ".join(cats_list)
            url = f"https://cyberdefenders.org/blueteam-ctf-challenges/{slug}/"
            desc = lab.get("learning_objective") or ""
            retired = "retired" if lab.get("is_retired") else "active"

            items.append(
                ChallengeItem(
                    id=slug,
                    title=name,
                    platform=self.platform_id,
                    tier=tier,
                    difficulty=diff,
                    category=cats,
                    url=url,
                    description=desc,
                    extra={
                        "time_min": time_min,
                        "time_str": time_str,
                        "slug": slug,
                        "retired": retired,
                        "is_pro": is_pro,
                    },
                )
            )

        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "cyberdefenders_all_challenges_2026.csv"
        free_catalog_path = self.target_dir / "cyberdefenders_all_challenges_catalog.md"
        learning_paths_path = self.target_dir / "cyberdefenders_learning_paths_catalog.md"

        # 1. Output CSV (preserving schema: title, tier, is_retired, diff, time_min, categories, slug, desc)
        csv_headers = ["title", "tier", "is_retired", "diff", "time_min", "categories", "slug", "desc"]
        csv_rows = [
            [
                c.title,
                "PREMIUM" if c.extra.get("is_pro") else "FREE",
                c.extra.get("retired", "active"),
                c.difficulty,
                c.extra.get("time_min", 0),
                c.category.replace(", ", "|"),
                c.extra.get("slug", c.id),
                c.clean_description,
            ]
            for c in challenges
        ]
        write_csv(csv_path, csv_headers, csv_rows)

        # 2. Output Free Catalog Markdown
        free_items = [c for c in challenges if c.is_free]
        table_headers = [
            "序號",
            "挑戰名稱 (Lab Title)",
            "存取權限 (Tier)",
            "難度 (Difficulty)",
            "預估時長",
            "領域分類 (Category)",
            "核心情境與技術概要 (Scenario)",
        ]
        table_rows = [
            [
                str(idx),
                f"**[{c.title}]({c.url})**",
                c.tier,
                f"`{c.difficulty}`",
                c.extra.get("time_str", ""),
                c.category,
                c.clean_description,
            ]
            for idx, c in enumerate(free_items, 1)
        ]
        table_md = format_markdown_table(table_headers, table_rows)
        free_content = f"""# 🛡️ CyberDefenders 官方全量 {len(challenges)} 題總目錄與 Free/Premium 分類表

> 來源依據：CyberDefenders 官方即時 API 提取 ｜ 統計：共 {len(challenges)} 題，其中 **{len(free_items)} 題完全免費 (Non-Premium)**，{len(challenges) - len(free_items)} 題需 Premium 訂閱。

{table_md}
"""
        write_markdown_file(free_catalog_path, free_content)

        # 3. Output Learning Paths Catalog Markdown
        premium_items = [c for c in challenges if not c.is_free]
        lp_headers = [
            "序號",
            "挑戰名稱 (Lab Title)",
            "難度",
            "時長",
            "領域分類 (Category)",
            "實戰情境概要 (Scenario)",
        ]
        lp_free_rows = [
            [
                str(idx),
                f"**[{c.title}]({c.url})**",
                f"`{c.difficulty}`",
                c.extra.get("time_str", ""),
                c.category,
                c.clean_description,
            ]
            for idx, c in enumerate(free_items, 1)
        ]
        lp_prem_rows = [
            [
                str(idx),
                f"[{c.title}]({c.url})",
                f"`{c.difficulty}`",
                c.extra.get("time_str", ""),
                c.category,
                c.clean_description,
            ]
            for idx, c in enumerate(premium_items, 1)
        ]
        lp_free_table_md = format_markdown_table(lp_headers, lp_free_rows)
        lp_prem_table_md = format_markdown_table(lp_headers, lp_prem_rows)
        lp_content = f"""# 🛡️ CyberDefenders 全題目索引與 Free / Premium 分類手冊

版本：2026 全量版 ｜ 題目總數：**{len(challenges)} 題**（🟢 **{len(free_items)} 題完全免費** ｜ 🔒 **{len(premium_items)} 題需 Premium 訂閱**）

與 `cylab_all_challenges_2026-08-08.csv` 對齊，本目錄已產出同構的 CSV 檔案：[`cyberdefenders_all_challenges_2026.csv`](cyberdefenders_all_challenges_2026.csv)。

---

## 🟢 {len(free_items)} 題完全免費題庫清單 (100% 可直接練習，免信用卡)

{lp_free_table_md}

---

## 🔒 {len(premium_items)} 題需 Premium 訂閱題庫清單 (付費會員進階演練)

{lp_prem_table_md}
"""
        write_markdown_file(learning_paths_path, lp_content)

        return [csv_path, free_catalog_path, learning_paths_path]
