# 🌐 網路協定與基礎封包分析深度學習路徑 (Network Protocols & Wireshark)
> 對應藍隊防衛矩陣：**領域 6** (6.1 ~ 6.4)
> 預計總投入時間：**35 ~ 45 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
打開 Wireshark 一片茫然  ──►    能精準使用 Display Filter 抓出通訊異常
分不清 TCP/UDP 差異      ──►    掌握 TCP 狀態機、三向交握旗標與 RST 阻斷
依賴外掛工具看明文       ──►    熟練執行 Follow TCP Stream 與 Export Objects
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
TCP協定狀態機  Wireshark過濾技巧  DNS/ARP異常排查  HTTP封包導出實作
(10h)         (8h)             (10h)            (8h)
```

---

## 🏁 階段一：TCP/IP 協定棧與三向交握狀態機（約 10 小時）

### 1.1 三向交握 (Three-Way Handshake) 與旗標 (Flags) 變化

```
Client (客戶端)                                  Server (伺服器)
   │                                                 │
   ├─── [SYN, Seq=x] ───────────────────────────────►│ (狀態變遷: LISTEN -> SYN_RCVD)
   │                                                 │
   │◄── [SYN, ACK, Seq=y, Ack=x+1] ──────────────────┤ (狀態變遷: SYN_SENT -> ESTABLISHED)
   │                                                 │
   ├─── [ACK, Seq=x+1, Ack=y+1] ────────────────────►│ (狀態變遷: ESTABLISHED)
```

### 1.2 四向揮手 (Four-Way Teardown) 與異常 RST 終止

- 正常關閉：`FIN -> ACK -> FIN -> ACK`
- 異常阻斷 (`RST`)：
  - 目的連接埠未開啟（Connection Refused）
  - 防火牆或 IPS 主動向雙方發送 RST 封包進行微創連線切斷
  - 惡意連線重設攻擊 (TCP Reset Attack)

---

## 🔍 階段二：Wireshark 高階 Display Filter 過濾語法（約 8 小時）

```bash
# 找出所有包含 SYN 且沒有 ACK 的封包 (SYN Flood 或連接埠掃描特徵)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# 找出連線被主動重設的封包
tcp.flags.reset == 1

# 過濾特定 DNS 查詢名稱或 NXDOMAIN 錯誤
dns.qry.name contains "malware" || dns.flags.rcode == 3

# 檢索 HTTP POST 請求且包含特定參數
http.request.method == "POST" && http contains "password"
```

---

## 📡 階段三：DNS 異常排查與 ARP/ICMP 區域網路威脅（約 10 小時）

### 3.1 DNS 隱蔽通道 (DNS Tunneling) 初探特徵

1. 異常長度的子域名查詢（如 `a1b2c3d4e5f6...evil.com`）。
2. 高頻率向同一特定名稱伺服器 (NS) 發送 `TXT` 記錄查詢。
3. 大量的 `NXDOMAIN` (不存在網域) 回應，常見於 DGA (Domain Generation Algorithm) 惡意程式。

### 3.2 ARP 欺騙與中間人攻擊 (MITM)

- 特徵：同一 IP 位址在短時間內由多個不同 MAC 位址宣告，或單一 MAC 宣稱為預設閘道 (Gateway IP)。
- Wireshark 警告：`Duplicate IP address detected` 或 `ARP poison detected`。

---

## 📋 自我評估檢查點

- [ ] 能在封包中指認 SYN、ACK、FIN、RST 旗標在 Wireshark Hex 視窗中的位元位置。
- [ ] 掌握如何在 Wireshark 中使用 `Follow -> TCP Stream` 完整提取 HTTP 明文通訊內容。
- [ ] 能寫出過濾所有 DNS 查詢且排除 mDNS/LLMNR 本地廣播的過濾語法。
