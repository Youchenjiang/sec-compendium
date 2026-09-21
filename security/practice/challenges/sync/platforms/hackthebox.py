"""
Hack The Box Platform Adapter

Fetches Starting Point, Active Machines, Retired Machines, Sherlocks (DFIR),
and CTF Challenges directly from Hack The Box API:
https://labs.hackthebox.com/api/v4/
"""

import csv
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base import BaseChallengeAdapter
from ..models import ChallengeItem
from ..writers import format_markdown_table, write_csv, write_markdown_file


class HackTheBoxAdapter(BaseChallengeAdapter):
    platform_id = "hackthebox"
    display_name = "Hack The Box"

    def load_token(self) -> Optional[str]:
        # 1. Check environment variable
        token = os.environ.get("HTB_API_TOKEN")
        if token:
            return token.strip()

        # 2. Check local .env file
        env_file = self.repo_root / ".env"
        if env_file.exists():
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("HTB_API_TOKEN=") and not line.startswith("#"):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass
        return None

    @staticmethod
    def _fetch_json(url: str, token: Optional[str]) -> Optional[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if not url.lower().startswith(("http://", "https://")):
            raise ValueError(f"Insecure URL scheme: {url}")
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:  # skipcq: BAN-B310
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            # Silently log error or debug
            return None

    def fetch_challenges(self) -> List[ChallengeItem]:  # skipcq: PY-R1000
        token = self.load_token()
        if not token:
            print("  [Notice] HTB_API_TOKEN not set or available.")
            return self._load_cached_fallback()

        items: List[ChallengeItem] = []

        # 1. Starting Point Machines
        candidates = [
            ("Meow", "Linux", "Very Easy", "Telnet 服務探測、無密碼 root 登入直接獲取 Flag"),
            ("Fawn", "Linux", "Very Easy", "FTP 服務枚舉、匿名訪客存取 (Anonymous Login) 下載機密檔案"),
            ("Dancing", "Windows", "Very Easy", "SMB 共享資源枚舉、無密碼訪客存取與管理員備份洩漏"),
            ("Explosion", "Windows", "Very Easy", "RDP 服務枚舉 (官方標註為 VIP+)"),
            ("Appointment", "Linux", "Very Easy", "Web 登入介面 SQL 注入攻擊 (SQLi) 繞過驗證"),
            ("Crocodile", "Linux", "Easy", "FTP 服務洩漏憑證、Web 管理後台預設帳密突破"),
            ("Responder", "Windows", "Easy", "Web LFI 本地檔案包含、LLMNR/NBT-NS 毒化、NTLM 雜湊捕捉提權"),
            ("Three", "Linux", "Easy", "子域名探勘、AWS S3 儲存貯體未授權寫入與 PHP WebShell"),
            ("Bike", "Linux", "Easy", "Node.js SSTI 模板注入 (官方標註為 VIP+)"),
            ("Vaccine", "Linux", "Easy", "SQL 注入攻擊 (SQLi)、資料庫密碼雜湊破解與 Sudo 提權"),
            ("Archetype", "Windows", "Easy", "MSSQL 滲透、xp_cmdshell 遠端指令執行、Windows 登錄檔密碼提權"),
            ("Oopsie", "Linux", "Easy", "Web 權限繞過、IDOR 不安全直接物件參考、SUID 二進位提權"),
            ("Markup", "Windows", "Easy", "XXE 實體注入攻擊 (官方標註為 VIP+)"),
            ("Included", "Linux", "Easy", "TFTP 服務利用與 UDP 滲透 (官方標註為 VIP+)"),
            ("Unified", "Linux", "Medium", "Log4j (CVE-2021-44228) 漏洞利用、UniFi 平台無檔案反彈 Shell"),
        ]

        for name, os_type, diff, desc in candidates:
            data = self._fetch_json(f"https://labs.hackthebox.com/api/v4/machine/profile/{name}", token)
            info = data.get("info", {}) if data else {}
            req_sub = info.get("requiredSubscription")
            is_free = (req_sub is None or req_sub != "VIP+") and not info.get("show_go_vip") and info.get("free") is not False

            items.append(
                ChallengeItem(
                    id=f"htb-sp-{name.lower()}",
                    title=name,
                    platform=self.platform_id,
                    tier="🟢 FREE" if is_free else "🔴 VIP+",
                    difficulty=diff,
                    category="Starting Point (Machine)",
                    url=f"https://app.hackthebox.com/machines/{name.replace(' ', '%20')}",
                    description=desc,
                    extra={"os": os_type, "type": "starting_point"},
                )
            )

        # 2. Active Machines
        data = self._fetch_json("https://labs.hackthebox.com/api/v4/machine/paginated?free=1&per_page=100", token)
        machines = data.get("data", []) if data else []
        for m in machines:
            name = m.get("name", "")
            items.append(
                ChallengeItem(
                    id=f"htb-machine-{m.get('id', name)}",
                    title=name,
                    platform=self.platform_id,
                    tier="🟢 FREE",
                    difficulty=m.get("difficultyText", "Unknown"),
                    category="Machine (Active Pentest)",
                    url=f"https://app.hackthebox.com/machines/{name.replace(' ', '%20')}",
                    description=f"當期線上常規主機攻堅演練 ({m.get('points')} pts) ｜ 發布日期: {str(m.get('release', ''))[:10]}",
                    extra={"os": m.get("os", "Linux"), "type": "active_machine"},
                )
            )

        # 3. Retired Machines
        page = 1
        while True:
            data = self._fetch_json(
                f"https://labs.hackthebox.com/api/v4/machine/list/retired/paginated?per_page=100&page={page}",
                token,
            )
            if not data or not data.get("data"):
                break
            for m in data["data"]:
                name = m.get("name", "")
                items.append(
                    ChallengeItem(
                        id=f"htb-retired-{m.get('id', name)}",
                        title=name,
                        platform=self.platform_id,
                        tier="🔴 VIP+",
                        difficulty=m.get("difficultyText", "Unknown"),
                        category="Machine (Retired Archive)",
                        url=f"https://app.hackthebox.com/machines/{name.replace(' ', '%20')}",
                        description=f"歷史經典滲透主機歸檔（需 VIP+ 訂閱啟動）｜ 發布日期: {str(m.get('release', ''))[:10]}",
                        extra={"os": m.get("os", "Linux"), "type": "retired_machine"},
                    )
                )
            last_page = data.get("meta", {}).get("last_page", 1)
            if page >= last_page:
                break
            page += 1
            time.sleep(0.05)

        # 4. Sherlocks
        page = 1
        while True:
            data = self._fetch_json(f"https://labs.hackthebox.com/api/v4/sherlocks?per_page=100&page={page}", token)
            if not data or not data.get("data"):
                break
            for s in data["data"]:
                name = s.get("name", "")
                state = s.get("state")
                is_free = state in ("active", "retired_free")
                items.append(
                    ChallengeItem(
                        id=f"htb-sherlock-{s.get('id', name)}",
                        title=name,
                        platform=self.platform_id,
                        tier="🟢 FREE" if is_free else "🔴 VIP",
                        difficulty=(s.get("difficulty") or "Medium").capitalize(),
                        category=f"Sherlock ({s.get('category_name', 'DFIR')})",
                        url=f"https://app.hackthebox.com/sherlocks/{name.replace(' ', '%20')}",
                        description="藍隊事件響應與取證分析實戰（包含日誌、封包流量或記憶體映像檔分析，開放線上提交答案）",
                        extra={"os": "Multi/Forensics", "type": "sherlock"},
                    )
                )
            last_page = data.get("meta", {}).get("last_page", 1)
            if page >= last_page:
                break
            page += 1
            time.sleep(0.05)

        # 5. Challenges
        page = 1
        while True:
            data = self._fetch_json(f"https://labs.hackthebox.com/api/v4/challenges?per_page=100&page={page}", token)
            if not data or not data.get("data"):
                break
            for c in data["data"]:
                name = c.get("name", "")
                state = c.get("state")
                is_free = state in ("active", "retired_free")
                items.append(
                    ChallengeItem(
                        id=f"htb-challenge-{c.get('id', name)}",
                        title=name,
                        platform=self.platform_id,
                        tier="🟢 FREE" if is_free else "🔴 VIP",
                        difficulty=(c.get("difficulty") or "Medium").capitalize(),
                        category=f"Challenge ({c.get('category_name', 'General')})",
                        url=f"https://app.hackthebox.com/challenges/{name.replace(' ', '%20')}",
                        description=f"獨立專題 CTF 解題挑戰（{c.get('category_name')} 領域實戰）",
                        extra={"os": "CTF Challenge", "type": "challenge"},
                    )
                )
            last_page = data.get("meta", {}).get("last_page", 1)
            if page >= last_page:
                break
            page += 1
            time.sleep(0.05)

        cached_items = self._load_cached_fallback()
        if len(items) < len(cached_items):
            print(
                f"  [Notice] Live API returned {len(items)} items (partial). "
                f"Preserving complete historical dataset ({len(cached_items)} items)."
            )
            return cached_items

        return items

    def _load_cached_fallback(self) -> List[ChallengeItem]:
        csv_path = self.target_dir / "hackthebox_all_challenges_2026.csv"
        if not csv_path.exists():
            return []
        print(f"  [Cached] Preserving {csv_path.name} snapshot.")
        items: List[ChallengeItem] = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(
                    ChallengeItem(
                        id=row.get("Title", ""),
                        title=row.get("Title", ""),
                        platform=self.platform_id,
                        tier=row.get("Tier", ""),
                        difficulty=row.get("Difficulty", ""),
                        category=row.get("Category", ""),
                        url=row.get("URL", "").replace(" ", "%20"),
                        description=row.get("Scenario", ""),
                        extra={"os": row.get("OS", "N/A")},
                    )
                )
        return items

    def write_outputs(self, challenges: List[ChallengeItem]) -> List[Path]:
        csv_path = self.target_dir / "hackthebox_all_challenges_2026.csv"
        md_path = self.target_dir / "hackthebox_all_challenges_catalog.md"

        if not challenges:
            print("  [Warn] 0 challenges fetched for Hack The Box; preserving existing files.")
            return [csv_path, md_path]

        # 1. Full CSV
        csv_headers = ["Title", "Tier", "Difficulty", "OS", "Category", "URL", "Scenario"]
        csv_rows = [
            [
                c.title,
                c.tier,
                c.difficulty,
                c.extra.get("os", "N/A"),
                c.category,
                c.url.replace(" ", "%20"),
                c.clean_description,
            ]
            for c in challenges
        ]
        write_csv(csv_path, csv_headers, csv_rows)

        # 2. Free Catalog Markdown
        free_items = [c for c in challenges if c.is_free]
        table_headers = ["序號", "挑戰名稱 (Title)", "類型", "難度", "作業系統", "分類", "說明"]
        table_rows = [
            [
                str(idx),
                f"**[{c.title}]({c.url})**",
                c.tier,
                f"`{c.difficulty}`",
                c.extra.get("os", "N/A"),
                c.category,
                c.clean_description[:80] + ("..." if len(c.clean_description) > 80 else ""),
            ]
            for idx, c in enumerate(free_items, 1)
        ]
        table_md = format_markdown_table(table_headers, table_rows)

        content = f"""# 📦 Hack The Box (HTB) 官方題庫目錄與 Free 實戰清單

版本：2026 全量版 ｜ 題目總數：**{len(challenges)} 題**（🟢 **{len(free_items)} 題完全免費** ｜ 🔒 **{len(challenges) - len(free_items)} 題需 VIP/VIP+**）

與 CyberDefenders 對齊，本目錄產出同構 CSV 數據：[`hackthebox_all_challenges_2026.csv`](hackthebox_all_challenges_2026.csv)。

---

## 🟢 {len(free_items)} 題完全免費實戰題庫目錄

{table_md}
"""
        write_markdown_file(md_path, content)

        return [csv_path, md_path]
