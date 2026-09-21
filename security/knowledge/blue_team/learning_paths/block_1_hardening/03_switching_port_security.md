# 🔌 交換機硬體安全與鏈路隔離深度學習路徑 (Switching Security & Port-Security)
> 對應藍隊防衛矩陣：**領域 3** (3.1 ~ 3.3)
> 預計總投入時間：**25 ~ 35 小時**（金盾獎初賽高頻考點）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
知道交換機轉發 MAC 封包   ──►    精通 CAM 溢位攻擊原理與 Port-Security 硬防護
分不清 Trunk 與 Access   ──►    掌握 802.1Q 4-Byte Tag 結構與 Native VLAN 跳躍防禦
聽過 STP 廣播風暴        ──►    能配置 BPDU Guard、Root Guard 與 DHCP Snooping
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
CAM原理與Port-Security  802.1Q與VLAN隔離  STP防護與鏈路安全  真題演練
(8h)                   (8h)              (8h)              (6h)
```

---

## 🏁 階段一：交換機轉發機制與 Port-Security 違規模式（約 8 小時）

### 1.1 CAM 表（MAC 位址表）耗盡攻擊 (MAC Flooding) 原理

交換機維護 CAM (Content Addressable Memory) 表以將 MAC 位址映射至實體 Port。當攻擊者偽造百萬個隨機 MAC 封包塞爆 CAM 表時，交換機會退化為**集線器 (Hub)** 模式，向所有連接埠廣播所有流量（Fail-open），攻擊者即可監聽全網通訊。

### 1.2 Cisco Port-Security 三大違規處理模式（金盾獎必考對比）

```
switchport port-security violation { protect | restrict | shutdown }
```

| 違規處理模式 | 是否丟棄違規封包？ | 是否記錄日誌並發送 SNMP Trap？ | 增加違規計數器？ | 介面狀態變化 |
| :--- | :---: | :---: | :---: | :--- |
| **Protect** | ✅ 是 | ❌ 否 | ❌ 否 | 維持 `up` 運作 |
| **Restrict** | ✅ 是 | ✅ 是 (Syslog / Trap) | ✅ 是 | 維持 `up` 運作 |
| **Shutdown** (預設) | ✅ 是 | ✅ 是 | ✅ 是 | 立即關閉介面進入 **`err-disable`** |

> 💡 **考點提示**：若介面進入 `err-disable`，管理員必須先下達 `shutdown` 再下達 `no shutdown`，或配置 `errdisable recovery cause psecure-violation` 自動恢復。

---

## 🌐 階段二：IEEE 802.1Q VLAN Tag 結構與跨交換機 Trunk（約 8 小時）

### 2.1 802.1Q 幀結構深度剖析 (4 Bytes / 32 Bits)

```
標準乙太網路幀: [DMAC (6B)] [SMAC (6B)] ──► [ 802.1Q Tag (4B) ] ──► [Type (2B)] [Data]
                                            │
   ┌────────────────────────────────────────┴────────────────────────────────────────┐
   ▼                                                                                 ▼
[ TPID: 16 Bits ] [ Priority (PCP): 3 Bits ] [ DEI (CFI): 1 Bit ] [ VLAN ID (VID): 12 Bits ]
(固定 0x8100)      (QoS 服務品質優先權)        (丟棄資格指示)         (範圍: 0~4095)
```

- **TPID (Tag Protocol Identifier)**: 固定值 `0x8100`，表示此幀帶有 802.1Q 標籤。
- **VLAN ID (VID)**: 長度為 **12 Bits**，因此最大支援數為 $2^{12} = 4096$ 個 VLAN（其中 0 與 4095 為保留，可用範圍 1 ~ 4094）。
- **Native VLAN 跳躍攻擊 (VLAN Hopping)**：雙重標籤 (Double Tagging) 攻擊利用 Trunk 預設 Native VLAN (VLAN 1) 不打標籤的特性。**防禦措施：將 Native VLAN 變更為未使用之獨立 VLAN，並啟用 `vlan dot1q tag native`**。

---

## 🛡️ 階段三：生成樹協定 (STP) 防護與二層防衛工程（約 8 小時）

### 3.1 STP 生成樹攻擊與安全防禦矩陣

1. **BPDU Guard**：
   - 部署在邊界存取埠（啟用 PortFast 的 Access Port）。
   - **防禦效果**：若該埠意外收到任何 BPDU 封包，代表有人私接交換機，立即將該埠置入 `err-disable` 狀態。
2. **Root Guard**：
   - 部署在非根交換機的指定埠 (Designated Port)。
   - **防禦效果**：防止惡意或低優先順序交換機宣告更優的 BPDU 奪取 Root Bridge 根橋接器身分。
3. **DHCP Snooping**：
   - 將連接埠劃分為 Trusted（上聯至真實 DHCP Server）與 Untrusted（一般終端）。
   - 攔截非法的 DHCP Offer 封包，防止惡意 DHCP 欺騙與中間人攻擊。

---

## 📋 自我評估檢查點

- [ ] 精確默背 Port-Security 的 Protect、Restrict、Shutdown 三種模式在「丟棄、告警、介面狀態」上的差異。
- [ ] 說出 802.1Q Tag 的總位元組數 (4B) 以及 VLAN ID 的位元數 (12 Bits)。
- [ ] 解釋 Double Tagging 雙重標籤攻擊的運作邏輯及防禦原則。
- [ ] 能說明為何 BPDU Guard 必須與 PortFast 一起配置在 Access Port。
