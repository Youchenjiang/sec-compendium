# 🏟️ HITCON 藍隊 Cyber Range 實戰攻防靶場特訓專案 (Cyber Range Track)

> 本專案為實驗室出征 HITCON Cyber Range（藍隊網路靶場 / 企業安全防禦演練 / SOC 實戰防衛戰）專用特訓藍圖。  
> 徹底摒棄片段分工，落實**【全員全能 (All-Rounder) ＋ 零分工摩擦 (Zero Division Friction)】**指導原則。

---

## 🧭 專案核心文檔

| 文檔名稱 | 檔案連結 | 核心用途與規格 |
| :--- | :--- | :--- |
| **Cyber Range 特訓指南 (v1.0)** | [`cyber_range_blue_team_roadmap.md`](cyber_range_blue_team_roadmap.md) | 企業混合架構剖析（DMZ、內網 AD、監控中樞）、四大奪分評分維度深度實戰、應變流程與實操指令集 |
| **HITCON 2026 實戰 Wargame 案例庫** | [`wargame_case_study/README.md`](wargame_case_study/README.md) | PHP Composer 供應鏈安全挑戰實戰題庫、自動化漏洞挖掘框架（4 AC 完整通關）、提交腳本與覆盤戰報 |

---

## 🏆 靶場四大奪分評分維度 (Scoring Dimensions)

1. **告警研判與溯源 (Triage & Threat Hunting)**：
   - 海量日誌快速降噪，精準還原攻擊時間線（入口 IP、時間、CVE 編號、初始 Payload SHA-256）。
2. **數位鑑識與奪旗 (DFIR & Flag Recovery)**：
   - 深入記憶體與網路封包，逆推 C2 通訊協定與金鑰，尋回被竄改的 `hitcon{...}` Flag。
3. **圍堵防禦與系統加固 (Containment & Hardening)**：
   - 快速切斷威脅、根除後門、修補漏洞並維持服務上線（滿足靶場 SLA 巡檢）。
4. **偵測工程與規則撰寫 (Detection Engineering)**：
   - 撰寫標準化 **Sigma 規則**（日誌端）、**YARA 規則**（檔案與記憶體）、**Suricata 簽章**（網路特徵）。
