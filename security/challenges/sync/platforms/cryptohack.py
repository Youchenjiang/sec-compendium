"""
CryptoHack Platform Adapter

Extracts and catalogs all modern cryptography challenges across 14 categories:
Introduction, General, Maths, Diffie-Hellman, Hashes, Isogenies, RSA, Web,
ZKP, ECC, Misc, CTF Archive, Post-Quantum, and AES.
All challenges on CryptoHack are 100% free to access.
"""

import re
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any, Dict, List

from security.challenges.sync.base import BaseChallengeAdapter
from security.challenges.sync.models import ChallengeItem
from security.challenges.sync.writers import format_markdown_table, write_csv, write_markdown_file


class CryptoHackAdapter(BaseChallengeAdapter):
    platform_id = "cryptohack"
    display_name = "CryptoHack"

    CATEGORIES = [
        ("introduction", "Introduction", "Beginner onboarding and flag submission basics"),
        ("general", "General", "Data formats, XOR operations, mathematics foundations"),
        ("maths", "Mathematics", "Modular arithmetic, lattices, quadratic residues"),
        ("diffie-hellman", "Diffie-Hellman", "Discrete log, MITM, parameter injection, group theory"),
        ("rsa", "RSA", "Public key crypto, factorization attacks, padding oracles, Wiener's attack"),
        ("aes", "Block Ciphers (AES)", "ECB, CBC, OFB, CTR, padding oracle, GCM vulnerabilities"),
        ("ecc", "Elliptic Curves", "ECDSA, curve parameters, invalid curve attacks, Montgomery curves"),
        ("hashes", "Hash Functions", "MD5, SHA, collision attacks, length extension, HMAC"),
        ("web", "Crypto on the Web", "JWT forgery, token manipulation, TLS/SSL weaknesses"),
        ("post-quantum", "Post-Quantum", "Lattice-based cryptography, Kyber, Dilithium fundamentals"),
        ("isogenies", "Isogenies", "Supersingular isogeny Diffie-Hellman and supersingular curves"),
        ("zkp", "Zero Knowledge", "Interactive proofs, Sigma protocols, Schnorr identification"),
        ("misc", "Miscellaneous", "Interactive algorithmic crypto, esoteric cipher systems"),
        ("ctf-archive", "CTF Archive", "Past CryptoHack CTF and wargame challenge archive"),
    ]

    @staticmethod
    def _determine_difficulty(points: int) -> str:
        """Map CryptoHack challenge point values to standard difficulty tiers."""
        if points <= 15:
            return "Easy"
        elif points <= 40:
            return "Medium"
        elif points <= 80:
            return "Hard"
        else:
            return "Insane"

    def fetch_challenges(self) -> List[ChallengeItem]:
        items: List[ChallengeItem] = []
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        for cat_slug, cat_title, _ in self.CATEGORIES:
            url = f"https://cryptohack.org/challenges/{cat_slug}/"
            print(f"  [CryptoHack] Scraping category: {cat_title} ({url})...")
            try:
                if not url.lower().startswith(("http://", "https://")):
                    raise ValueError(f"Insecure URL scheme: {url}")
                req = urllib.request.Request(url, headers={"User-Agent": user_agent})
                with urllib.request.urlopen(req, timeout=15) as resp:  # skipcq: BAN-B310
                    html = resp.read().decode("utf-8", "ignore")

                # Match each challenge block within the list
                blocks = re.findall(
                    r'<li class="challenge"[^>]*>(.*?)</li>\s*(?=<li class="challenge"|</ul>)',
                    html,
                    re.DOTALL,
                )

                cat_count = 0
                for b in blocks:
                    ch_id_m = re.search(r'data-challenge="([^"]+)"', b)
                    title_m = re.search(r'<div class="challenge-text[^>]*>(.*?)</div>', b)
                    pts_m = re.search(r"(\d+)\s*pts", b)
                    solves_m = re.search(r"(\d+)\s*Solves", b)
                    desc_m = re.search(r'<div class="challengeDescription">(.*?)</div>', b, re.DOTALL)

                    if not ch_id_m or not title_m:
                        continue

                    slug = ch_id_m.group(1).strip()
                    title = title_m.group(1).strip()
                    points = int(pts_m.group(1)) if pts_m else 10
                    solves = int(solves_m.group(1)) if solves_m else 0

                    clean_desc = ""
                    if desc_m:
                        desc_text = re.sub(r"<[^>]+>", " ", desc_m.group(1))
                        clean_desc = " ".join(unescape(desc_text).split())
                        # Remove leading marker if present
                        if clean_desc.startswith("-->"):
                            clean_desc = clean_desc[3:].strip()
                        clean_desc = clean_desc[:200]

                    difficulty = self._determine_difficulty(points)
                    item_url = f"https://cryptohack.org/challenges/{cat_slug}/"

                    items.append(
                        ChallengeItem(
                            id=f"cryptohack-{slug}",
                            title=title,
                            platform=self.platform_id,
                            tier="🟢 FREE",
                            difficulty=difficulty,
                            category=cat_title,
                            url=item_url,
                            description=clean_desc or f"CryptoHack challenge in {cat_title} ({points} pts).",
                            extra={
                                "slug": slug,
                                "points": points,
                                "solves": solves,
                                "category_slug": cat_slug,
                            },
                        )
                    )
                    cat_count += 1

                print(f"    -> Extracted {cat_count} challenges for {cat_title}")

            except Exception as e:
                print(f"  [Warn] Failed to scrape category '{cat_slug}': {e}")

        print(f"  [CryptoHack] Total extracted: {len(items)} challenges (100% Free).")
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "cryptohack_all_challenges_2026.csv"
        md_path = self.target_dir / "cryptohack_all_challenges_catalog.md"

        # 1. Output CSV
        csv_headers = ["Category", "Title", "Points", "Difficulty", "Solves", "URL", "Slug", "Description"]
        csv_rows = [
            [
                c.category,
                c.title,
                c.extra.get("points", 0),
                c.difficulty,
                c.extra.get("solves", 0),
                c.url,
                c.extra.get("slug", ""),
                c.description,
            ]
            for c in challenges
        ]
        write_csv(csv_path, csv_headers, csv_rows)

        # 2. Output Markdown Catalog
        md_content = self._generate_catalog_markdown(challenges)
        write_markdown_file(md_path, md_content)

        return [csv_path, md_path]

    def _generate_catalog_markdown(self, challenges: List[ChallengeItem]) -> str:  # skipcq: PY-R1000
        lines = [
            "# 🔐 CryptoHack 現代密碼學全挑戰題庫目錄 (CryptoHack Challenge Catalog)",
            "",
            "> 本目錄自動同步自 [CryptoHack](https://cryptohack.org/) 官方挑戰區，收錄全部 14 大核心分類、300+ 道現代密碼學關卡。",
            "> **所有題目 100% 免費開放**，涵蓋對稱加密 (AES)、公鑰密碼 (RSA/Diffie-Hellman)、橢圓曲線 (ECC)、雜湊函式與後量子密碼學。",
            "",
            f"**同步題數統計**: 共收錄 `{len(challenges)}` 道實戰關卡（🟢 全部 100% 免費）。",
            "",
            "---",
            "",
            "## 📊 一、 分類與難度分佈矩陣",
            "",
        ]

        # Category summary table
        cat_stats: Dict[str, List[ChallengeItem]] = {}
        for c in challenges:
            cat_stats.setdefault(c.category, []).append(c)

        cat_summary_headers = ["主題領域 (Category)", "題目數量", "難度分佈", "代表知識點"]
        cat_summary_rows = []
        for _cat_slug, cat_title, cat_desc in self.CATEGORIES:
            ch_list = cat_stats.get(cat_title, [])
            count = len(ch_list)
            if count == 0:
                continue
            easy_c = sum(1 for c in ch_list if c.difficulty == "Easy")
            med_c = sum(1 for c in ch_list if c.difficulty == "Medium")
            hard_c = sum(1 for c in ch_list if c.difficulty == "Hard")
            insane_c = sum(1 for c in ch_list if c.difficulty == "Insane")
            diff_str = f"Easy:{easy_c} | Med:{med_c} | Hard:{hard_c} | Ins:{insane_c}"
            cat_summary_rows.append([f"**{cat_title}**", str(count), diff_str, cat_desc])

        lines.append(format_markdown_table(cat_summary_headers, cat_summary_rows))
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📚 二、 各分類題庫詳細清單")
        lines.append("")

        for _cat_slug, cat_title, cat_desc in self.CATEGORIES:
            ch_list = cat_stats.get(cat_title, [])
            if not ch_list:
                continue

            lines.append(f"### 📌 {cat_title}（{len(ch_list)} Challenges）")
            lines.append(f"*{cat_desc}*")
            lines.append("")

            table_headers = ["關卡名稱 (Title)", "分數 (Pts)", "難度", "解題人數", "線上傳送門", "關卡簡介"]
            table_rows = [
                [
                    f"**{c.title}**",
                    str(c.extra.get("points", 0)),
                    f"`{c.difficulty}`",
                    f"{c.extra.get('solves', 0):,}",
                    f"[前往解題]({c.url})",
                    c.clean_description[:90] + ("..." if len(c.clean_description) > 90 else ""),
                ]
                for c in ch_list
            ]
            lines.append(format_markdown_table(table_headers, table_rows))
            lines.append("")

        return "\n".join(lines)
