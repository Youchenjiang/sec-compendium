# 🛠️ 資安作戰與自動化工具庫 (Security Tools)

本目錄收錄專案通用之資安作戰工具、白箱原始碼審計引擎與自動化檢驗腳本。

---

## 🧰 工具清單

### 1. [Code Auditor](code_auditor/README.md) (自動化白箱原始碼審計與 PoC 驗證引擎)
- **路徑**：`security/tools/code_auditor/`
- **定位**：全功能 PHP / 開源供應鏈安全審計與動態驗證引擎。
- **能力**：
  - 🔍 **SAST 靜態分析**：AST 語法樹追蹤與 38 條核心危險 Sink 偵測（RCE, SQLi, SSTI, Unserialize, 任意讀寫）。
  - ⚡ **PoC 產生器**：自動根據 Sinks 與資料流合成漏洞利用代碼。
  - 🐳 **Docker 沙箱驗證**：在乾淨的隔離容器中即時動態驗證 Exploit 是否有效。
  - 🔌 **模組化平台介面**：支援本機離線審計與 CTF/Wargame 遠端競賽自動化。
  - 📐 **方法論指導**：👉 [全方位安全審計與攻防方法論 (audit_methodology.md)](code_auditor/audit_methodology.md)

### 2. [Playbook Validator](validate_playbooks.py) (原子手冊結構規範檢驗工具)
- **路徑**：`security/tools/validate_playbooks.py`
- **定位**：自動化檢查 `blue_team/playbooks` 107 本實戰手冊的結構規範、YAML metadata 與必備章節。

---

## 🚀 常用指令速查

```bash
# 1. 執行本地白箱代碼審計 (純靜態掃描)
python -m security.tools.code_auditor.main --local-dir /path/to/target --scan-only

# 2. 執行本地審計並生成 Exploit
python -m security.tools.code_auditor.main --local-dir /path/to/target

# 3. 執行 Playbook 規範檢查
python security/tools/validate_playbooks.py
```
