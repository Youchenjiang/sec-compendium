# 🧱 網路分段與防火牆加固深度學習路徑 (Network Segmentation & Firewall Hardening)
> 對應藍隊防衛矩陣：**領域 2** (2.1 ~ 2.3)
> 預計總投入時間：**35 ~ 45 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
知道什麼是 IP/Port       ──►    能精準規劃企業 DMZ/生產區/管理區微隔離
會用 ufw allow/deny      ──►    精通 Netfilter 表鏈結構與狀態追蹤 (conntrack)
僅看連線阻斷 log         ──►    能結合次世代防火牆 (NGFW) 與 IPS 阻斷深度攻擊
```

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 → 階段二 → 階段三 → 階段四 → 階段五
Netfilter架構 狀態追蹤  邊界阻斷  微隔離ACL  NGFW與IPS聯防
(8h)         (4h)      (8h)      (10h)     (10h)
```

---

## 🏁 階段一：Netfilter 表鏈架構與封包流向（約 8 小時）

### 1.1 Netfilter 5 表 5 鏈底層邏輯

```
網路介面進入 (Incoming Packet)
       │
       ▼
 [PREROUTING] (raw -> connection tracking -> mangle -> nat)
       │
    路由決策 (Routing Decision)
    ├──► 目的為本機 ──► [INPUT] (mangle -> filter) ──► 本機程序 (Local Process)
    └──► 目的非本機 ──► [FORWARD] (mangle -> filter) ──► 路由發送
                                                          ▲
                                                          │
 本機程序發送 ──► [OUTPUT] ──► 路由決策 ───────────────────┘
 (raw -> conntrack -> mangle -> nat -> filter)
                                                          │
                                                          ▼
                                                      [POSTROUTING]
                                               (mangle -> nat: SNAT/MASQUERADE)
                                                          │
                                                          ▼
                                                   離開網路介面 (Egress)
```

---

## 🔍 階段二：連線狀態追蹤 (Stateful Inspection)（約 4 小時）

iptables 連線追蹤機制將封包區分為四種核心狀態：
1. `NEW`：嘗試建立新連線的初始封包（如 TCP SYN）。
2. `ESTABLISHED`：雙向握手完成後的後續合法通訊流量。
3. `RELATED`：由現存連線觸發的新連線（如 FTP 資料傳輸 Port 20、ICMP 錯誤回報）。
4. `INVALID`：無法辨識或不合邏輯的異常封包（如 FIN 旗標未交握即送出，應直接 DROP）。

```bash
# 經典狀態防火牆基準規則
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
```

---

## ⚔️ 階段三：邊界策略實務與防禦性阻斷（約 8 小時）

### 3.1 預設策略與嚴格白名單原則

```bash
# 預設阻斷所有進入與轉發流量 (Default Drop)
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允許本機迴路 (Loopback)
iptables -A INPUT -i lo -j ACCEPT

# 允許特定管理子網存取 SSH (限制單一來源 IP 與速率)
iptables -A INPUT -p tcp -s 192.168.10.50 --dport 22 -m conntrack --ctstate NEW -m limit --limit 3/min -j ACCEPT
```

---

## 🏢 階段四：內部網路微隔離與 VLAN 存取控制（約 10 小時）

### 4.1 區域劃分核心原則 (DMZ vs Internal vs Management)

| 區域名稱 | 功能定位 | 存取控制原則 |
|---------|---------|-------------|
| **DMZ (隔離區)** | 對外公開服務 (Web, Mail) | 僅開放特定對外 Port；嚴禁主動發起連線至內部資料庫區 |
| **Production (生產區)** | 內部業務伺服器、資料庫 | 僅允許 DMZ 特定服務連入必要 Port；完全禁止外網直連 |
| **Management (管理平面)**| SSH、SNMP、堡壘機 | 僅限特定管理 VLAN 與固定 MAC 存取，落實頻外管理 (OOB) |

```bash
# 阻斷 DMZ 主機主動存取內部資料庫網段 (除特定回應外)
iptables -A FORWARD -s 172.16.1.0/24 -d 10.0.1.0/24 -m conntrack --ctstate NEW -j DROP
```

---

## 🛡️ 階段五：次世代防火牆 (NGFW) 與 IPS 聯防（約 10 小時）

### 5.1 NGFW 與傳統防火牆核心差異

- 傳統 L4 防火牆：依賴 IP、Port 判斷（難以阻斷 HTTP 80 埠下的 C2 流量或 SQL 注入）。
- NGFW (L7 防火牆)：具備深度封包檢測 (DPI)、SSL 解密檢視、應用程式特徵識別 (App-ID) 與使用者身分感知 (User-ID)。

### 5.2 Snort/Suricata 內聯 (Inline IPS) 阻斷模式

```bash
# Suricata NFQUEUE 內聯模式啟用配置
iptables -A FORWARD -j NFQUEUE --queue-num 0
```

---

## 📋 自我評估檢查點

- [ ] 畫出 Netfilter 封包在 PREROUTING、INPUT、FORWARD、POSTROUTING 的流向圖。
- [ ] 能解釋為什麼 `ESTABLISHED,RELATED` 規則通常放在 INPUT 鏈的最頂端。
- [ ] 能設定 iptables 規則限制特定 Port 每分鐘連線次數以防暴力破解。
- [ ] 說出 DMZ 伺服器被攻陷時，微隔離策略如何防止攻擊者橫向移動至資料庫。
