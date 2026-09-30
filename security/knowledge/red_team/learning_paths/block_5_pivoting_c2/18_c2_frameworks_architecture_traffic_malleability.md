# 📡 現代 C2 架構體系、流量可塑性偽裝與記憶體隱蔽深度學習路徑 (C2 Infrastructure & Malleable Traffic)
> 對應紅隊作戰矩陣：**Phase 5 (R21)** (R21.1 ~ R21.4)  
> 預計總投入時間：**30 ~ 35 小時**（視 分散式 C2 拓撲、HTTP 標頭語意、CDN 反向代理與記憶體防護基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會直連 C2 IP 容易被藍隊抓  ──►     精通現代分散式 Redirector、CDN 偽裝與前置轉發拓撲
不懂 C2 流量特徵為何被攔截   ──►     透徹理解 Malleable C2 Profile、HTTP 標頭置換與 Jitter 抖動
以為常駐 Beacon 只有定時連線 ──►     精通 Sleep Mask 記憶體休眠動態加密與堆疊偽造 (Stack Spoofing)
分不清 Sliver 與 Havoc 差異  ──►     掌握 Golang/C 跨平台現代 C2 引擎架構與 Demon Agent 指揮機制
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| 分散式命令與控制架構 | 理解 Operator、Team Server、Listener 與 Implant/Beacon 分工權責 | [Red Team Infrastructure Wiki](https://github.com/bluscreenofjeff/Red-Team-Infrastructure-Wiki) |
| HTTP/HTTPS 協議進階特徵 | 理解 Host 標頭、CDN 反向代理路由、SNI 與 TLS 憑證協商 | [Cloudflare: How CDNs Work](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) |
| 記憶體安全與特徵掃描 | 理解 YARA 規則特徵碼比對、記憶體屬性 (PAGE_EXECUTE_READWRITE) 偵測指標 | [YARA Documentation](https://yara.readthedocs.io/) |
| 行程執行緒呼叫堆疊 (Call Stack) | 理解 Return Address, Stack Frame 佈局與 EDR 執行緒堆疊回溯分析 | [Microsoft Learn: Stack Frame Layout](https://learn.microsoft.com/cpp/build/stack-allocation) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (8h) ──────► 階段二 (10h) ─────► 階段三 (8h) ──────► 階段四 (6h)
現代開源 C2 架構     CDN 與重定向器      Malleable 流量塑形  Sleep Mask 記憶體
(Sliver / Havoc)    隱蔽基礎設施佈建     與 Jitter 抖動機制   動態加密防禦逃逸
```

---

## 🏛️ 階段一：現代開源 C2 核心架構解析——Sliver 與 Havoc（約 8 小時）

### 1.1 分散式 Team Server 架構模型
現代 C2 系統嚴格分離「操作人員 (Operator)」與「後端伺服器 (Team Server)」：
- 多名紅隊隊員使用客戶端透過 mTLS 加密連線登入 Team Server，確保協同作戰指令審計。
- Team Server 管理各種 Listener（HTTP/HTTPS/DNS/mTLS/WireGuard），並產生客製化 Implant。

### 1.2 Sliver 與 Havoc 技術對決
- **Sliver (BishopFox)**：以 Go 語言編寫，具備強大原生跨平台特性（Windows/Linux/macOS），通訊協議支援 WireGuard、mTLS 與 HTTP(S)，具備反除錯、動態符號混淆能力。
- **Havoc (C2 Framework)**：以 C/ASM 原生撰寫其核心 Demon Agent，具備極致低底層特徵、原生 Indirect Syscalls、動態 API 雜湊解析與 Sleep Obfuscation，專門對抗現代進階 EDR。

---

## 🥩 階段二：C2 基礎設施隱蔽設計——重定向器 (Redirectors) 與 CDN 反向代理（約 10 小時）

### 2.1 為什麼不能直接暴露 C2 Team Server？
一旦威脅獵捕人員（藍隊或威脅情資廠商）將 C2 的真實 IP 或網域加入黑名單，整個攻擊基礎設施便全數報銷。

### 2.2 多層重定向器 (Redirectors) 架構
```text
[受害者主機 (Implant)]
        │
        ├── 透過 HTTPS 請求合法 CDN 域名 (如 cdn.example.com)
        ▼
[Cloudflare / AWS CloudFront] ──(CDN 邊緣快取與反向代理)
        │
        ▼
[Apache / Nginx 重定向器 (Redirector)]
        │
        ├── 條件 1：User-Agent 符合自訂密碼且路徑正確 ──► 轉發至 [C2 Team Server]
        │
        └── 條件 2：常規掃描器 / 藍隊探針 / 異常請求 ──► 轉發至合法官方網站 (200 OK)
```
- **Domain Fronting (網域前端化)**：利用 CDN 節點在 SNI（外部可見）與 HTTP Host 標頭（內部加密）的路由差異，使監控人員僅看到知名合法網站流量，而真實流量被送入紅隊 C2。

---

## 🔬 階段三：流量可塑性偽裝 (Malleable C2) 與 Jitter 抖動控制（約 8 小時）

### 3.1 流量特徵消除：自訂 Malleable Profile
傳統惡意程式易被 IDS/IPS 依據固定 URI 或常規長度封鎖。Malleable C2 Profile 允許紅隊重構傳輸語意：
- **偽裝為合法應用**：將傳輸 Payload 經過 Base64 編碼後注入至 Cookie、ETag、URI 查詢參數或自訂 HTTP Header（如 `X-Requested-With`）。
- **偽裝伺服器回應**：將 C2 下發之任務封裝在合法的 jQuery、CSS 或 PNG 圖像資料流尾端。

### 3.2 Jitter（時間抖動）與 Beacon 心跳隱蔽
- **週期性問題**：若固定每 60 秒發送一次心跳包，藍隊 SIEM 透過週期性演算法（Fast Fourier Transform / 自相關分析）可輕易辨識。
- **隨機抖動 (Jitter)**：設定基準休眠時間 60 秒，配合 `jitter 30%`，使實際發包間隔在 42 秒至 78 秒間完全隨機分佈，破壞統計學特徵。

---

## 🛡️ 階段四：記憶體隱蔽——Sleep Mask 動態加密防護（約 6 小時）

### 4.1 記憶體常駐狀態下的靜態 YARA 掃描
EDR（如 CrowdStrike, Defender for Endpoint）會在背景對工作站行程記憶體進行週期性記憶體掃描（Memory Inspection）。
- 當 C2 Implant 處於休眠（Sleep）期間，若其 Shellcode 或 Payload 在記憶體中以明文且具備可執行權限 (`RX` 或 `RWX`) 存在，將直接觸發簽章警報。

### 4.2 Sleep Mask (Ekko / Foliage 技術原理)
```text
[Implant 正常執行任務 (RX)] ──► 任務結束準備休眠
                                       │
                                呼叫 Sleep Mask (如利用 ROP 鏈或異步計時器)
                                       │
                                       ├── 1. 將自身記憶體區塊屬性降級為 PAGE_READWRITE (RW)
                                       ├── 2. 使用隨機密鑰對自身記憶體進行 XOR / RC4 快速加密
                                       ├── 3. 進入定時睡眠 (如透過 WaitForSingleObjectEx)
                                       │   (此時 EDR 記憶體掃描只能看到混亂的高熵無意義資料！)
                                       │
                                休眠時間結束喚醒
                                       │
                                       ├── 4. 自身解密還原程式碼
                                       └── 5. 恢復記憶體屬性為 PAGE_EXECUTE_READ (RX) 繼續執行
```

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚說明 C2 Team Server、Operator 與 Listener 的權責與網路拓撲關係。
- [ ] 能獨立配置 Nginx 重定向器，根據特定 URI 正則與 User-Agent 實現精確流量過濾分流。
- [ ] 能撰寫 Malleable C2 設定檔，將敏感資料隱蔽在 HTTP Header 與 Base64 中。
- [ ] 能解釋為什麼固定間隔的 Beacon 連線會被 SIEM / NDR 系統輕易關聯識別。
- [ ] 能詳細繪製 Sleep Mask 技術在記憶體屬性切換與加密休眠時的執行序列。

---

## 🏆 推薦實戰靶場與題庫直達
1. **BishopFox/Sliver 官方練習環境**：實地部署開源 Sliver C2，練習產生各類混淆 Implant 與 mTLS 監聽。[Sliver GitHub](https://github.com/BishopFox/sliver)
2. **HackTheBox: Sherlocks (C2 Hunting 系列)**：扮演藍隊從真實封包與記憶體日誌中逆向 C2 流量特徵。[HTB Sherlocks](https://app.hackthebox.com/sherlocks)
3. **Red Team Infrastructure Wiki**：研讀業界一線紅隊團隊在雲端與邊緣節點部署隱蔽 C2 的實戰規範。
