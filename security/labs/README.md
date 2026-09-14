# 🏰 實體靶場環境總覽 (Cyber Range & Live Labs Directory)

> [!IMPORTANT]
> **發布目標**: 本目錄提供 **Docker Compose 一鍵啟動** 之交鑰匙（Turnkey）實體資安靶場，直接對接 107 篇藍隊作戰手冊與全真模擬考試。
> **硬體相容性**: 全面配置容器資源限制（CPU / Memory Limit），確保一般 8GB ~ 16GB RAM 之筆記型電腦皆可流暢運行。

---

## 🗺️ 實體靶場架構地圖

| 靶場目錄 | 核心對接手冊 | 技術堆疊 | 佔用連接埠 | 記憶體上限 |
| :--- | :--- | :--- | :--- | :--- |
| [`01_atomic_purple_range/`](01_atomic_purple_range/README.md) | `27.1` Atomic Red Team<br>`27.2` MITRE Caldera | MITRE Caldera C2, Ubuntu 22.04, Auditd | 8888 (Web UI)<br>7010, 7012 (Agent) | 1.5 GB |
| [`02_splunk_bots_range/`](02_splunk_bots_range/README.md) | `28.2` Splunk BOTS<br>`15.1`~`15.4` SIEM 獵捕 | OpenSearch 2.11, OpenSearch Dashboards | 9200 (REST API)<br>5601 (Web UI) | 1.0 GB |
| [`03_apt_cross_domain_ctf/`](03_apt_cross_domain_ctf/README.md) | `28.1` APT 全鏈條奪旗<br>`28.3` 跨網段橫向移動 | Python Flask (RCE), Alpine Linux, 3-Tier Network | 8080 (Web 入口)<br>9999 (機密資料庫) | 512 MB |

---

## ⚡ 快速啟動指南

### 1. 選擇靶場並進入目錄
```bash
# 例如進入紫隊模擬靶場
cd labs/01_atomic_purple_range

# 或進入威脅獵捕 SIEM 靶場
cd labs/02_splunk_bots_range

# 或進入 APT 全鏈條奪旗靶場
cd labs/03_apt_cross_domain_ctf
```

### 2. 一鍵啟動容器叢集
```bash
docker compose up -d
```

### 3. 檢視運行狀態
```bash
docker compose ps
```

### 4. 演練完畢後徹底銷毀環境
```bash
docker compose down -v
```

---

## 🧪 免容器離線標本分析 (Evidence Datasets)

若您的硬體環境不便運行 Docker，可直接造訪離線鑑識標本庫：
👉 **[`../challenges/evidence/README.md`](../challenges/evidence/README.md)**  
內含：
- `pcap/dns_exfil_Topic1.pcap`（DNS 隱寫外帶分析）
- `pcap/web_attack_traffic.pcap`（Web 入侵與橫向移動分析）
- `memory/patientportal.hprof.gz`（Java JVM 記憶體傾印鑑識）
- `evtx/windows_ir_security_sample.json`（Windows 安全事件日誌）
