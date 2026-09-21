# 🔄 題庫自動同步與規格化框架 (Challenge Sync Framework)

> 本目錄收錄專案通用之多平台實戰題庫同步器、API 爬蟲與標準化輸出引擎。  
> 自動抓取各大攻防平台之即時題目、標註免費/付費狀態，並輸出為標準化 CSV 與 Markdown 目錄。

---

## 🚀 核心指令

```bash
# 1. 列出目前支援之平台適配器
python -m security.practice.challenges.sync.main --list

# 2. 同步單一平台題庫 (例如 MTA 惡意流量分析或 CyberDefenders)
python -m security.practice.challenges.sync.main --platform mta
python -m security.practice.challenges.sync.main --platform cyberdefenders

# 3. 全量同步所有支援之平台
python -m security.practice.challenges.sync.main --all
```

---

## 🏛️ 架構與模組說明

- **`main.py`**：CLI 統一命令列入口，支援 `--platform`、`--all` 與 `--list` 參數。
- **`base.py`**：定義 `ChallengeSyncAdapter` 抽象基底類別、標準化資料結構與 CSV/Markdown 匯出邏輯。
- **`platforms/`**：各攻防平台之專屬適配器（CyberDefenders, MTA, Root-Me, CyLab 等）。

---

## 🔗 相關導覽

- 平台題庫數據庫：👉 [`../platforms/README.md`](../platforms/README.md)
- 全域免費題庫大索引：👉 [`../UNIFIED_FREE_CHALLENGES_INDEX.md`](../UNIFIED_FREE_CHALLENGES_INDEX.md)
