# 📊 Splunk / Elastic BOTS 威脅獵捕靶場 (BOTS Hunting Range)

> **對接手冊**: [28.2 企業級實戰資料集：Splunk BOTS (Boss of the SOC) 深度研判](../../28.2_large_scale_enterprise_bots_dataset.md)

---

## 🎯 環境架構

本環境透過 Docker Compose 部署輕量化 SIEM 分析平台：
1. **OpenSearch 引擎 (連接埠 9200)**：單節點開源搜尋引擎，預先配置記憶體 512MB~1GB。
2. **OpenSearch Dashboards (連接埠 5601)**：圖形化 SIEM 儀表板，支援 Lucene、DQL 與 PPL 語法。

---

## 🚀 一鍵啟動與日誌匯入

```bash
# 1. 啟動 SIEM 叢集
docker compose up -d

# 2. 匯入 BOTS 實戰攻防日誌集
python scripts/import_bots_dataset.py

# 3. 進入 Web 介面進行獵捕
# 瀏覽器造訪: http://localhost:5601
# 進入 Discover 頁面建立索引模式: bots-enterprise-logs
```

---

## 🔍 演練指南

請參考 [`queries/bots_hunting_playbook.md`](queries/bots_hunting_playbook.md) 進行四大攻擊階段的獵捕實作：
1. Web Reconnaissance (SQLi 掃描)
2. Initial Access (WebShell 上傳)
3. Living Off the Land (Certutil 惡意下載)
4. Impact & Ransomware (VSSAdmin 陰影複製刪除)
