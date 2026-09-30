# 🟣 紫隊協同對抗與全景聯防架構 (Purple Team Operations & Adversary Emulation)

> **「攻防並濟，方得始終。」**  
> 紫隊 (Purple Teaming) 並非獨立存在的第三個作戰陣營，而是以**透明協同 (Transparency)**、**即時反饋 (Real-time Feedback)** 與**威脅知情 (Threat-Informed Defense)** 為核心的雙軌進化引擎。它打破紅藍邊界，將紅隊 110 篇特戰攻擊技術精準轉化為藍隊 107 篇深層偵測與應變能力，實現 ATT&CK 覆蓋閉環。

---

## 🏛️ 紫隊核心協同閉環迴路 (Purple Closed-Loop Lifecycle)

紫隊協同演習的核心在於**「以測促防、即時迭代」**。每一次進攻動作皆需在防守端產生可被量化的遙測紀錄與告警規則：

```text
       ┌────────────────────────────────────────────────────────┐
       │   1. 威脅情報與劇本定義 (CTI & Adversary Profile)      │
       │   • 選擇目標威脅組織 (如 APT29, FIN7) 與核心 TTPs        │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   2. 戰術同桌對齊 (Tabletop & Hypothesis Formulation)  │
       │   • 紅藍共議注入點、預期日誌來源與檢測假說 (Hypothesis)    │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   3. 原子化攻擊注入 (Atomic Attack Emulation)          │
       │   • 執行紅隊特戰手冊 (Playbooks/Phase 1~6) 或 Caldera    │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   4. 遙測觀測與防禦差距分析 (Telemetry Gap Analysis)   │
       │   • 檢查 EDR/Sysmon/Auditd/SIEM 是否成功捕捉行為       │
       │   • 紀錄偵測延遲時間 (MTTD) 與日誌欄位完整度             │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   5. 偵測工程即時反饋調優 (Detection Engineering Loop)  │
       │   • 現場編寫/修訂 Sigma、YARA、Suricata 或 SPL 規則      │
       │   • 抑制誤報 (FP)，調優閥值與微隔離策略 (Microseg)       │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   6. ATT&CK Navigator 熱圖閉環與成熟度復評              │
       │   • 匯入 Navigator Layer 標記技術覆蓋評分 (Score 1~3)   │
       └────────────────────────────────────────────────────────┘
```

---

## 📊 紫隊防禦成熟度評級標準 (Maturity Model)

在紫隊演練中，每項 ATT&CK 技術對抗成果依據防禦深度分為五個等級：

| 等級 | 標記狀態 | 評分 (Score) | 具體定義與標準 |
| :---: | :---: | :---: | :---|
| **L0** | **Blind (防禦盲區)** | `0` | 無任何防護手段，系統既無日誌採集，亦無告警觸發。 |
| **L1** | **Offense-Only (僅知攻擊)** | `1` | 紅隊具備驗證手冊，但藍隊缺乏遙測採集，無法重構時間線。 |
| **L2** | **Telemetry (具備遙測)** | `2` | 底層有記錄 (如 Sysmon Event ID 1 / Auditd)，但 SIEM 無關聯告警。 |
| **L3** | **Detected (精準告警)** | `3` | 攻擊觸發 SIEM / EDR 即時告警，誤報率低於 5%，已形成標準 SOC 劇本。 |
| **L4** | **Mitigated (主動阻斷)** | `4` | 端點 EDR 或網路 IPS 於執行當下成功阻斷，並自動觸發隔離處置。 |

---

## 🧭 紫隊模組導航與核心資產

1. 🗺️ **[攻防全景聯防矩陣 (attack_defense_matrix.md)](attack_defense_matrix.md)**  
   收錄橫跨 MITRE ATT&CK 14 大戰術、紅隊 110 篇手冊與藍隊 107 篇防禦對抗點的完整對照表，標註核心日誌來源（Event ID / Sysmon / Auditd / Zeek）與驗收標準。

2. ⚙️ **[ATT&CK Navigator 雙軌圖層產生器 (purple_layer_generator.py)](purple_layer_generator.py)**  
   自動化將攻防矩陣解析為標準 MITRE ATT&CK Navigator v4.5 JSON 檔案，支援一鍵匯入雲端儀表板生成覆蓋熱圖。

3. 🟣 **[紫隊全景熱圖展示層 (layers/enterprise_attack_defense_layer.json)](layers/enterprise_attack_defense_layer.json)**  
   預先編譯的企業級紫隊演習覆蓋圖層，已標註雙軌驗證得分與對應技術清單。

4. 🧪 **實體對抗模擬靶場**  
   - [Atomic Purple Range](../blue_team/playbooks/phase_6_capstone/ranges/01_atomic_purple_range/README.md)：Caldera + Ubuntu 22.04 + Auditd 自動化注入對抗環境。
   - [Splunk BOTS 實戰取證分析](../blue_team/playbooks/phase_6_capstone/ranges/02_splunk_bots_range/README.md)：百萬筆真實企業攻防流量溯源環境。
   - [APT 跨域實戰演練](../blue_team/playbooks/phase_6_capstone/ranges/03_apt_cross_domain_ctf/README.md)：多主機橫向移動與域滲透混合對抗場景。

---

## 🛠️ 常用演練執行指令

```bash
# 1. 執行全專案雙軌手冊與跨模組超連結品質檢驗
python security/tools/validate_playbooks.py

# 2. 自動生成最新的 ATT&CK Navigator 紫隊演習熱圖 Layer
python security/knowledge/purple_team/purple_layer_generator.py

# 3. 啟動本機 Docker 紫隊自動化演練靶場
cd security/knowledge/blue_team/playbooks/phase_6_capstone/ranges/01_atomic_purple_range
docker compose up -d
```
