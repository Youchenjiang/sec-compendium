# 🔴 紅隊原子實戰手冊 (Red-Team Atomic Playbook) 撰寫黃金標準與模板

---

## 📌 宗旨與核心約束 (The Golden Mandate)

本規範為專案內所有紅隊攻擊與滲透技術手冊（`security/knowledge/red_team/playbooks/*/*.md`）的**唯一法定撰寫標準**。

### 核心原則：
1. **拒絕機器人八股與單元測試充數**：嚴禁通篇使用生硬英文法律條款、嚴禁塞入上千行本地 Mock HTTP Server 代碼充當手冊字數。
2. **以人與作戰為本**：每份手冊必須兼具**「身臨其境的滲透作戰心流（Tactical Narrative）」**與**「字典級實戰指令武器庫（Arsenal Cheatsheet）」**。
3. **深入底層物理真實**：講清楚記憶體佈局、TCP/HTTP/Kerberos/LDAP 封包欄位、身分驗證權限機制的真正底層缺陷，不打高空。
4. **極致的攻防對抗意識**：紅隊的價值不僅在於拿到權限，更在於**「如何繞過 EDR/WAF」**、**「留下什麼藍隊日誌特徵」**以及**「如何反制 SOC 獵捕」**。

---

## 🏛️ 紅隊實戰手冊標準 7 大區塊架構

每篇手冊嚴格由以下 7 個標準區塊依序構成：

```
🔴 手冊 [技術編號]：[技術名稱] (技術英文名稱)
├── 🎯 作戰任務破題 (Tactical Objective & Mental Workflow) & 滲透思維導圖
├── 🔬 第一動：底層協定/漏洞機制全景解剖 (Vulnerability Mechanics & Physical Structs)
├── ⚡ 第二動：武器化與突防打擊 (Weaponization & Exploitation Vector)
├── 🥷 第三動：隱匿作戰與反鑑識規避 (Evasion & Anti-Forensics Operational Cheatsheet)
├── ⚔️ 第四動：紅藍攻防對抗矩陣 (Red vs. Blue Confrontation Matrix)
├── 🚩 第五動：戰果鞏固與橫向拓展 (Post-Exploitation & Lateral Pivot)
├── 🧪 實戰演練環境導引 (Hands-on Range Lab Walkthrough)
└── 🎯 作戰驗收檢查點 (Mastery Checklist - 5 題情境實戰自我測驗)
```

---

## 📐 各區塊詳細規範與撰寫標準

### 1. 🎯 作戰任務破題 (Tactical Objective & Mental Workflow)
- **作戰背景**：設定具體的滲透情境（例如：外部暴露面突防、內網網域提權、雲端邊界穿透）。
- **作戰目標**：明確定義本技術要達成的作戰目標（取得初期存取權、竊取特定金鑰、取得未授權身分）。
- **破局思維導圖**：使用 ASCII 繪製紅隊攻擊者的心流決策圖，明確指出「在什麼條件下選擇此技術？失敗後的 Fallback 是什麼？」。

### 2. 🔬 第一動：底層協定/漏洞機制全景解剖 (Mechanics & Physical Structs)
- **拒絕空洞概念**：必須繪製底層封包結構、記憶體結構、ASN.1/BER/XML 欄位或作業系統核心結構。
- **根本原因剖析 (Root Cause)**：從 RFC 規範、原始碼邏輯或微軟內部機制出發，講透漏洞為什麼會存在（例如：Parser 差異、解序列化未校驗類別、Kerberos 缺乏 PAC 簽章校驗）。

### 3. ⚡ 第二動：武器化與突防打擊 (Weaponization & Exploitation Vector)
- **字典級 Payload 構造表**：以三欄標準表格整理：
  | 攻擊場景/變體 | 關鍵 Payload 構造與指令 | 突防原理與作用標記 |
  | :--- | :--- | :--- |
- **實戰打擊指令庫**：提供可在真實環境（Linux/Windows 終端）直接運行的具體命令（cURL、PowerShell、Impacket、Python 原生腳本）。

### 4. 🥷 第三動：隱匿作戰與反鑑識規避 (Evasion & Anti-Forensics Operational Cheatsheet)
- **規避 EDR / WAF 阻斷**：字元編碼繞過、分塊傳輸（Chunked）、記憶體加載（In-memory Execution）、Parent PID 欺騙、Token 偷渡。
- **無檔案落地 (Fileless)** 與內存駐留技巧。
- **痕跡抹除與暫存清理**：操作完成後的清理動作（日誌覆蓋、暫存檔消除、網路連線終止）。

### 5. ⚔️ 第四動：紅藍攻防對抗矩陣 (Red vs. Blue Confrontation Matrix)
- 必須讓讀者清楚知道自己的一舉一動在藍隊眼中長怎樣：
  | 紅隊攻擊行為 (Action) | 藍隊產生的遙測足跡 (Telemetry / Event ID) | SOC 告警特徵 (Sigma / Splunk) | 紅隊反制與規避手法 (Evasion TTP) |
  | :--- | :--- | :--- | :--- |
- 列出具體的 Windows Event ID（如 4624, 4688, 4768, 4769）、Sysmon Event（如 1, 3, 10, 11）或 Suricata 規則邏輯。

### 6. 🚩 第五動：戰果鞏固與橫向拓展 (Post-Exploitation & Lateral Pivot)
- 拿到漏洞或憑證後的**下一步推進**：
  - 如何將此權限轉換為互動式 Shell？
  - 如何利用取得的 Session/Ticket 向內網跳躍？
  - 如何建立持久化隱蔽通道？

### 7. 🧪 實戰演練環境導引 (Hands-on Range Lab Walkthrough)
- 說明如何在標準靶場（Docker Compose 或虛擬機環境）中搭建並親手驗證。
- 提供驗證指令與預期回顯，確保讀者可 100% 親自重現。

### 8. 🎯 作戰驗收檢查點 (Mastery Checklist)
- 提供 5 道深度實戰情境自我測驗題（含情境、分析思路與參考答案），幫助學習者檢驗是否已徹底掌握該技術。

---

## 📋 紅隊原子實戰手冊標準模板 (Template)

```markdown
# [技術編號] [技術中文名稱] ([技術英文名稱])

## 🎯 作戰任務破題 (Tactical Objective & Mental Workflow)

在企業紅隊演練或實戰滲透中，[描述目標場景與痛點]...

```
[攻擊者終端] ── 1. 探測並定位目標 ──► [目標邊界/服務]
                                      │
                                      ├── 2. 注入惡意構造 Payload
                                      ▼
                               [觸發漏洞/核心瑕疵]
                                      │
                                      └── 3. 取得未授權權限/票證
                                      ▼
[內網跳板/權限提升] ◄── 4. 建立隱蔽通道 ─────┘
```

### 作戰痛點與決策分支
- **痛點場景**：[描述傳統手段為何受阻，例如 WAF 攔截、EDR 行為阻斷]
- **決策心流**：[說明何時採用此手法]

---

## 🔬 第一動：底層協定/漏洞機制全景解剖 (Mechanics & Physical Structs)

### 物理結構與缺陷原理
[深入解剖底層協議、封包結構、記憶體或二進位細節]

```
+-----------------------------------------------------------------------------------+
| 核心協定/資料結構剖析                                                              |
|                                                                                   |
| 欄位/位移 | 欄位名稱         | 脆弱性成因與攻擊者控制點                           |
| :-------- | :--------------- | :------------------------------------------------- |
| 0x00      | Protocol Header  | 伺服器未校驗長度或來源簽章                         |
| 0x14      | Attribute Flag   | 可由攻擊者任意翻轉以偽造管理者權限                 |
+-----------------------------------------------------------------------------------+
```

---

## ⚡ 第二動：武器化與突防實戰 (Weaponization & Exploitation Vector)

### 核心 Payload 與作戰矩陣

| 攻擊手法變體 | 核心 Payload / 關鍵指令構造 | 突防原理說明 |
| :--- | :--- | :--- |
| **基礎原型利用** | `curl -X POST ...` | [原理] |
| **進階繞過變體** | `curl --path-as-is ...` | [原理] |

### 實戰打擊指令庫

#### 1. 自動化探測與定位
```bash
# 終端探測指令
```

#### 2. 武器化攻擊觸發
```bash
# 武器化觸發指令
```

---

## 🥷 第三動：隱匿作戰與反鑑識規避 (Evasion & Anti-Forensics Operational Cheatsheet)

### 1. 繞過端點偵測 (EDR/AV Evasion)
- **記憶體載入**：...
- **混淆與特徵消除**：...

### 2. 網路流量擬態與隱匿
- **流量封裝**：...

---

## ⚔️ 第四動：紅藍攻防對抗矩陣 (Red vs. Blue Confrontation Matrix)

| 紅隊攻擊階段 (Action) | 藍隊遙測足跡 (Telemetry / Event ID) | SOC 獵捕邏輯 (Detection Rule) | 紅隊反制/規避策略 (Countermeasure) |
| :--- | :--- | :--- | :--- |
| **初始觸發** | Event ID 4688 / Sysmon EID 1 | 偵測異常命令列參數 | 使用環境變數或 Base64 內存調用 |
| **權限提升** | Event ID 4672 / 4624 Type 3 | 異常用戶特權登入 | 竊取既有高權限 Token 避免登入日誌 |

---

## 🚩 第五動：戰果鞏固與橫向拓展 (Post-Exploitation & Lateral Pivot)

### 權限維持與後滲透展開
```bash
# 後滲透與橫向移動指令
```

---

## 🧪 實戰演練環境導引 (Hands-on Range Lab Walkthrough)

### 靶場架設與重現步驟
```bash
# 啟動靶場
docker-compose up -d
```

---

## 🎯 作戰驗收檢查點 (Mastery Checklist)

- [ ] **Q1. [實戰情境題 1]**  
  *分析思路*：...
- [ ] **Q2. [實戰情境題 2]**  
  *分析思路*：...
- [ ] **Q3. [實戰情境題 3]**  
  *分析思路*：...
- [ ] **Q4. [實戰情境題 4]**  
  *分析思路*：...
- [ ] **Q5. [實戰情境題 5]**  
  *分析思路*：...
```
