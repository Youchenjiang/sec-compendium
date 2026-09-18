# 🛡️ Code Auditor (自動化白箱源碼審計與漏洞驗證引擎)

Code Auditor 是一套通用的開源白箱代碼審計、自動化 PoC / Exploit 鑄造、Docker 動態沙箱驗證與安全報告產出框架。

---

## 🌟 核心架構

```
code_auditor/
├── core/                # 🔍 核心靜態分析引擎 (AST 語法樹 + 污點分析 + 38 條安全 Sink 規則)
├── generator/           # ⚡ 自動化 PoC / Exploit 產生器 (SQLi, RCE, SSTI, Unserialize, 任意讀寫)
├── sandbox/             # 🐳 Docker 隔離沙箱動態驗證器 (支援 PHP 7.4 / 8.x)
├── platform/            # 🔌 模組化平台介面 (支援 本地離線審計、REST API 平台、Playwright 繞過)
├── storage/             # 📝 結果持久化、JSON 審計報告與 Markdown Writeup 自動產出
├── config.py            # ⚙️ 全域環境變數與平台設定
└── main.py              # 🚀 統一 CLI 入口
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r security/tools/code_auditor/requirements.txt

# 若需啟用 Cloudflare Turnstile 瀏覽器驗證碼繞過：
pip install playwright && playwright install chromium
```

### 2. 模式 A：本地目錄開箱審計 (Local Code Audit)

直接審計本機任一 PHP 專案、開源軟體庫或解壓後的原始碼目錄：

```bash
# 1. 靜態分析 + 輸出漏洞報告與初步 Markdown Writeup
python -m security.tools.code_auditor.main --local-dir /path/to/target --scan-only

# 2. 靜態分析 + 自動生成 PoC Exploit
python -m security.tools.code_auditor.main --local-dir /path/to/target

# 3. 靜態分析 + 自動生成 PoC + 在本機 Docker 沙箱動態驗證
python -m security.tools.code_auditor.main --local-dir /path/to/target --dist-dir /path/to/docker_env --verify
```

### 3. 模式 B：CTF / Wargame 競賽聯網攻防 (Competition Automation)

複製並配置 `.env`：

```bash
cp security/tools/code_auditor/.env.example security/tools/code_auditor/.env
```

一鍵全自動執行（登入 ➡️ 取題 ➡️ 掃描 ➡️ 生成 Exploit ➡️ 本地 Docker 測試 ➡️ 自動向平台提交 ➡️ 產出 Writeup）：

```bash
python -m security.tools.code_auditor.main --verify
```

---

## 📊 產出結果

所有審計與攻擊驗證結果自動持久化至 `results/`：
- `results/reports/`：結構化漏洞掃描報告 (`.json`)
- `results/exploits/`：針對該目標自動合成的 Python Exploit 腳本
- `results/writeups/`：自動生成的 Markdown Writeup
- `results/history.jsonl`：全域審計歷史時間軸
