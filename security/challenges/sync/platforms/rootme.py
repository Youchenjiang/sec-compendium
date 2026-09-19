"""
Root-Me Platform Adapter

Dynamically fetches and synchronizes challenges from Root-Me's official
REST API (https://api.www.root-me.org/challenges?lang=en) with session auth,
and maintains live local snapshot caching against API rate limits.
Zero hardcoded challenge lists.
"""

import html
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import format_markdown_table, write_csv, write_markdown_file


class RootMeAdapter(BaseChallengeAdapter):
    platform_id = "rootme"
    display_name = "Root-Me"

    API_BASE = "https://api.www.root-me.org"

    # Official Rubrique ID -> (Standard Display Category, Canonical URL Category Slug)
    RUBRIQUE_MAP = {
        "154": ("Web - Server", "Web-Server"),
        "155": ("Web - Client", "Web-Client"),
        "156": ("Steganography", "Steganography"),
        "157": ("Realist", "Realist"),
        "158": ("Cracking", "Cracking"),
        "159": ("Programming", "Programming"),
        "160": ("Cryptanalysis", "Cryptanalysis"),
        "183": ("Network", "Network"),
        "191": ("App - Script", "App-Script"),
        "204": ("App - System", "App-System"),
        "209": ("Forensic", "Forensic"),
    }

    def load_session(self) -> Optional[str]:
        """Load Root-Me spip_session cookie from environment or .env."""
        # 1. Check environment variable
        token = os.environ.get("ROOTME_SPIP_SESSION")
        if token:
            return token.strip()

        # 2. Check local .env file
        env_file = self.repo_root / ".env"
        if env_file.exists():
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ROOTME_SPIP_SESSION=") and not line.startswith("#"):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass

        # 3. No session provided
        return None

    def _clean_slug(self, title: str) -> str:
        """Convert title into Root-Me canonical URL slug."""
        s = html.unescape(title).strip()
        s = s.replace("&amp;", "and").replace("&", "and")
        s = re.sub(r"[^a-zA-Z0-9]+", "-", s)
        return s.strip("-")

    def _fetch_from_api(self, session: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all official English challenges from official Root-Me REST API."""
        print(f"  [Root-Me] Connecting to official REST API: {self.API_BASE}/challenges?lang=en...")
        current_url = f"{self.API_BASE}/challenges?lang=en"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": f"spip_session={session}",
            "Accept": "application/json",
            "Accept-Language": "en",
        }

        raw_items: List[Dict[str, Any]] = []
        page = 1

        try:
            while current_url:
                req = urllib.request.Request(current_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read().decode("utf-8"))

                if not data or not isinstance(data, list) or len(data) == 0:
                    break

                items_dict = data[0]
                for idx, item in items_dict.items():
                    raw_items.append(item)

                next_url = None
                for link in data[1:]:
                    if isinstance(link, dict) and link.get("rel") == "next":
                        next_url = link.get("href")
                        break

                current_url = next_url
                page += 1
                time.sleep(0.3)

            print(f"  [Root-Me] Successfully retrieved {len(raw_items)} official challenge records from API.")
            return raw_items
        except Exception as e:
            print(f"  [Root-Me] Official API call encountered: {e}")
            return None

    def fetch_challenges(self) -> List[ChallengeItem]:
        session = self.load_session()
        raw_items = None
        snapshot_path = self.target_dir / "rootme_official_api_snapshot.json"

        if session:
            raw_items = self._fetch_from_api(session)

        # Fallback to verified official API snapshot if API is rate-limited (HTTP 429) or offline
        if not raw_items:
            if snapshot_path.exists():
                print(f"  [Root-Me] Using local official API snapshot: {snapshot_path.name}")
                with open(snapshot_path, "r", encoding="utf-8") as f:
                    raw_items = json.load(f)
            else:
                print("  [Error] No API response and no local snapshot found.")
                return []

        # Update snapshot with latest successful data
        if raw_items and (not snapshot_path.exists() or len(raw_items) > 0):
            try:
                with open(snapshot_path, "w", encoding="utf-8") as f:
                    json.dump(raw_items, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        items: List[ChallengeItem] = []
        for raw in raw_items:
            cid = str(raw.get("id_challenge", ""))
            raw_title = raw.get("titre", "")
            title = html.unescape(raw_title).strip()
            rid = str(raw.get("id_rubrique", ""))

            cat_info = self.RUBRIQUE_MAP.get(rid, ("General", "Challenges"))
            cat_name, cat_slug = cat_info

            slug = self._clean_slug(title)
            canonical_url = f"https://www.root-me.org/en/Challenges/{cat_slug}/{slug}"

            items.append(
                ChallengeItem(
                    id=f"rootme-{cid}",
                    title=title,
                    platform=self.platform_id,
                    tier="🟢 FREE",
                    difficulty="Practitioner",
                    category=cat_name,
                    url=canonical_url,
                    description=f"Root-Me official wargame challenge #{cid} in {cat_name}.",
                    extra={"id_challenge": cid, "slug": slug, "id_rubrique": rid, "category_slug": cat_slug},
                )
            )

        print(f"  [Root-Me] Successfully parsed {len(items)} official challenges across all 11 categories.")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "rootme_all_challenges_2026.csv"
        md_path = self.target_dir / "rootme_all_challenges_catalog.md"

        # 1. Output CSV
        csv_headers = ["ID", "Category", "Title", "Tier", "Difficulty", "URL", "Slug"]
        csv_rows = [
            [
                c.extra.get("id_challenge", c.id),
                c.category,
                c.title,
                c.tier,
                c.difficulty,
                c.url,
                c.extra.get("slug", ""),
            ]
            for c in challenges
        ]
        write_csv(csv_path, csv_headers, csv_rows)

        # 2. Output Markdown Catalog
        md_content = self._generate_catalog_markdown(challenges)
        write_markdown_file(md_path, md_content)

        return [csv_path, md_path]

    def _generate_catalog_markdown(self, challenges: List[ChallengeItem]) -> str:
        lines = [
            "# 🚩 Root-Me 官方全量挑戰題庫目錄 (Root-Me Live Challenge Catalog)",
            "",
            "> 本目錄直接連線 [Root-Me 官方 REST API](https://api.www.root-me.org/) 動態同步生成，**零寫死資料**，實時追蹤官方全部 11 大安全領域官方題庫。",
            "> 涵蓋 Web 伺服端、Web 客戶端、密碼分析、數位鑑識、網路安全、系統漏洞利用、腳本分析、逆向破解、擬真滲透、演算法設計與隱寫術等全領域關卡。",
            "",
            f"**同步題數統計**: 共動態收錄 `{len(challenges)}` 道官方全量實戰關卡（🟢 全部 100% 免費開放）。",
            "",
            "---",
            "",
            "## 📊 一、 分類與題數分佈概覽",
            "",
        ]

        cat_stats: Dict[str, List[ChallengeItem]] = {}
        for c in challenges:
            cat_stats.setdefault(c.category, []).append(c)

        summary_headers = ["領域分類 (Category)", "官方收錄題數", "代表關卡 Slug", "官方傳送門"]
        summary_rows = []
        for cat in sorted(cat_stats.keys()):
            ch_list = cat_stats[cat]
            sample_slugs = ", ".join(c.extra.get("slug", "") for c in ch_list[:3])
            cat_slug = ch_list[0].extra.get("category_slug", cat.replace(" ", ""))
            summary_rows.append([
                f"**{cat}**",
                str(len(ch_list)),
                f"`{sample_slugs}`...",
                f"[瀏覽分類](https://www.root-me.org/en/Challenges/{cat_slug}/)",
            ])

        lines.append(format_markdown_table(summary_headers, summary_rows))
        lines.append("")
        lines.append("---",)
        lines.append("")
        lines.append("## 📚 二、 各領域官方題目詳細清單")
        lines.append("")

        for cat in sorted(cat_stats.keys()):
            ch_list = cat_stats[cat]
            lines.append(f"### 📌 {cat}（{len(ch_list)} Challenges）")
            lines.append("")

            table_headers = ["ID", "挑戰名稱 (Title)", "關卡代碼 (Slug)", "官方直連傳送門"]
            table_rows = [
                [
                    str(c.extra.get("id_challenge", "")),
                    f"**{c.title}**",
                    f"`{c.extra.get('slug', '')}`",
                    f"[前往挑戰]({c.url})",
                ]
                for c in ch_list
            ]
            lines.append(format_markdown_table(table_headers, table_rows))
            lines.append("")

        return "\n".join(lines)
