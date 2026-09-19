# HITCON 2026 Wargame — PHP Composer Security Challenge

> 📦 **知識庫整併說明**：本專案原為獨立倉庫 wargame-bot，已完整保留所有 16 個 Git 提交歷史與攻防框架合併入 sec-compendium，作為核心實戰題庫、自動化漏洞挖掘框架與賽後技術覆盤資產。  
> 🛠️ **通用引擎提升說明**：本賽事實戰中所提煉之通用靜態代碼分析、Exploit 自動合成與 Docker 沙箱驗證引擎，已正式解耦並提升為獨立通用武器庫：[**Code Auditor (`security/tools/code_auditor`)**](../../tools/code_auditor/README.md)。本目錄保留作為 HITCON 2026 實戰案例庫、提交腳本與覆盤戰報。

Automated vulnerability auditing, exploit development, and verification workspace for the HITCON 2026 Wargame PHP Composer Security Challenge.

**Result**: 4 AC (Full Solve) — owasp/phprbac x2, internations/http-mock x2

## Project Structure

```
├── bot/                    # Core bot framework
│   ├── main.py             #   Main orchestrator
│   ├── client.py           #   Wargame API client
│   ├── generator.py        #   Exploit auto-generation
│   ├── tester.py           #   Docker testing
│   ├── storage.py          #   Persistent storage
│   ├── config.py           #   Configuration
│   └── submit/             #   Submitted exploit scripts (4 AC + 2 failed)
│
├── lib/                    # Shared modules
│   ├── scanner.py          #   Unified scanner (consolidated from 3 versions)
│   ├── scanner_rules.py    #   Scanner rules
│   ├── scanner_utils.py    #   Scanner utilities
│   ├── paths.py            #   Centralized path resolution
│   ├── types.py            #   Type definitions
│   └── output.py           #   Output formatting
│
├── scripts/                # Consolidated tools
│   ├── scan.py             #   --scope local|deep|global|docker
│   ├── compile.py          #   --format vectors|catalog
│   ├── find.py             #   --type web|core|entrypoint|procedural
│   ├── triage.py           #   --mode triage|categorize
│   ├── audit.py            #   --mode depth|batch
│   ├── analyze/            #   2 remaining analysis scripts
│   ├── exploit/            #   1 exploit script (uses lib/scanner)
│   └── tools/              #   4 utility scripts
│
└── docs/                   # Documentation
    ├── writeup.md          #   Complete wargame writeup
    ├── methodology.md      #   Technical methodology
    └── post_mortem_wargame_retrospective.md  # Post-mortem
```

## Key Documents

- **[docs/writeup.md](docs/writeup.md)** — Competition results, exploits (with PoC), false positive analysis, container specs, key technical discoveries
- **[docs/methodology.md](docs/methodology.md)** — AI collaboration framework, SAST methodology, patch triage approach
- **[docs/post_mortem_wargame_retrospective.md](docs/post_mortem_wargame_retrospective.md)** — Full post-mortem and retrospective

## Successful Exploits

| Package | PHP | Vulnerability | Score |
|---------|-----|---------------|-------|
| owasp/phprbac 2.0.0 | 7.4.33 | install.php -> file_put_contents -> RCE | 445 AC |
| owasp/phprbac 2.0.0 | 8.4 | Same as above | 445 AC |
| internations/http-mock 0.14.0 | 7.4.33 | @unserialize($_COOKIE) -> SuperClosure eval() -> RCE | 395 AC |
| internations/http-mock 0.12.0 | 8.4 | Same as above | 395 AC |

## Environment

- PHP 7.4.33 and 8.4
- Apache with AllowOverride All
- Composer install: `--no-dev --prefer-dist`
- Exploit constraints: 60s timeout, 128 MiB memory, /tmp writable only

