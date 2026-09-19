"""
Root-Me Platform Adapter

Dynamically fetches and synchronizes challenges from Root-Me's official
live XML sitemap (https://www.root-me.org/sitemap.xml).
Zero hardcoded challenge lists.
"""

import re
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import format_markdown_table, write_csv, write_markdown_file


class RootMeAdapter(BaseChallengeAdapter):
    platform_id = "rootme"
    display_name = "Root-Me"

    SITEMAP_URL = "https://www.root-me.org/sitemap.xml"

    CATEGORY_MAP = {
        "Web-Server": "Web - Server",
        "Web-Serveur": "Web - Server",
        "Web-Client": "Web - Client",
        "Cryptanalysis": "Cryptanalysis",
        "Cryptanalyse": "Cryptanalysis",
        "Forensic": "Forensics",
        "Network": "Network",
        "Reseau": "Network",
        "App-System": "App - System",
        "App-Systeme": "App - System",
        "App-Script": "App - Script",
        "Cracking": "Cracking",
        "Steganography": "Steganography",
        "Steganographie": "Steganography",
        "Programming": "Programming",
        "Programmation": "Programming",
        "Realist": "Realist",
        "Realiste": "Realist",
    }

    def fetch_challenges(self) -> List[ChallengeItem]:
        print(f"  [Root-Me] Fetching live challenges from official sitemap: {self.SITEMAP_URL}...")
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        req = urllib.request.Request(self.SITEMAP_URL, headers={"User-Agent": user_agent})

        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw_xml = resp.read().decode("utf-8", "ignore")
        except Exception as e:
            print(f"  [Error] Failed to fetch Root-Me sitemap: {e}")
            return []

        # Find all challenge URLs in sitemap across English and French paths
        url_matches = re.findall(
            r"<loc>(https://www\.root-me\.org/(?:en|fr)/Challenges/([^/]+)/([^<]+))</loc>",
            raw_xml,
        )

        seen_slugs = set()
        items: List[ChallengeItem] = []

        for full_url, raw_cat, slug in url_matches:
            # Avoid duplicate bilingual URLs pointing to the same challenge
            slug_key = slug.lower()
            if slug_key in seen_slugs:
                continue
            seen_slugs.add(slug_key)

            normalized_cat = self.CATEGORY_MAP.get(raw_cat, raw_cat.replace("-", " "))
            title = slug.replace("-", " ").strip()
            # Canonical link to English page
            canonical_url = f"https://www.root-me.org/en/Challenges/{raw_cat}/{slug}"

            items.append(
                ChallengeItem(
                    id=f"rootme-{slug_key}",
                    title=title,
                    platform=self.platform_id,
                    tier="🟢 FREE",
                    difficulty="Practitioner",
                    category=normalized_cat,
                    url=canonical_url,
                    description=f"Root-Me official wargame challenge in {normalized_cat}.",
                    extra={"slug": slug, "raw_category": raw_cat},
                )
            )

        print(f"  [Root-Me] Successfully parsed {len(items)} unique challenges dynamically from live sitemap.")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "rootme_all_challenges_2026.csv"
        md_path = self.target_dir / "rootme_all_challenges_catalog.md"

        # 1. Output CSV
        csv_headers = ["Category", "Title", "Tier", "Difficulty", "URL", "Slug"]
        csv_rows = [
            [
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
            "> 本目錄由通用同步框架動態連線 [Root-Me 官方 Sitemap](https://www.root-me.org/sitemap.xml) 解析生成，**零寫死資料**，實時追蹤官方最新題目發布。",
            "> 涵蓋 Web 滲透、現代密碼分析、數位鑑識、網路封包分析、系統二進位安全、逆向工程與擬真滲透等全領域關卡。",
            "",
            f"**同步題數統計**: 共動態抓取 `{len(challenges)}` 道官方實戰關卡（🟢 全部 100% 免費開放）。",
            "",
            "---",
            "",
            "## 📊 一、 分類與題數分佈概覽",
            "",
        ]

        cat_stats: Dict[str, List[ChallengeItem]] = {}
        for c in challenges:
            cat_stats.setdefault(c.category, []).append(c)

        summary_headers = ["領域分類 (Category)", "官方即時收錄題數", "代表關卡 Slug", "官方傳送門"]
        summary_rows = []
        for cat in sorted(cat_stats.keys()):
            ch_list = cat_stats[cat]
            sample_slugs = ", ".join(c.extra.get("slug", "") for c in ch_list[:3])
            summary_rows.append([
                f"**{cat}**",
                str(len(ch_list)),
                f"`{sample_slugs}`...",
                f"[瀏覽分類](https://www.root-me.org/en/Challenges/{cat.replace(' ', '')}/)",
            ])

        lines.append(format_markdown_table(summary_headers, summary_rows))
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📚 二、 各領域官方題目詳細清單")
        lines.append("")

        for cat in sorted(cat_stats.keys()):
            ch_list = cat_stats[cat]
            lines.append(f"### 📌 {cat}（{len(ch_list)} Challenges）")
            lines.append("")

            table_headers = ["挑戰名稱 (Title)", "關卡代碼 (Slug)", "官方直連傳送門"]
            table_rows = [
                [
                    f"**{c.title}**",
                    f"`{c.extra.get('slug', '')}`",
                    f"[前往挑戰]({c.url})",
                ]
                for c in ch_list
            ]
            lines.append(format_markdown_table(table_headers, table_rows))
            lines.append("")

        return "\n".join(lines)
