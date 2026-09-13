# ⚖️ 數位證據法規與監管鏈深度學習路徑 (Digital Evidence & Chain of Custody)
> 對應藍隊防衛矩陣：**領域 29** (29.1 ~ 29.3)
> 預計總投入時間：**25 ~ 35 小時**（法遵與鑑識標準）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
查案直接在原始硬碟操作   ──►    嚴格落實 ISO/IEC 27037 鑑識標準程序
忽略證據揮發性順序       ──►    精通 RFC 3227 記憶體優先擷取原則
不知法庭如何認定證據效力 ──►    熟練防寫設備 (Write Blocker) 與雙雜湊 MD5+SHA256
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
ISO/IEC 27037標準  RFC 3227數據揮發順序  防寫設備與雜湊驗證  法庭證據能力
(8h)              (8h)                   (6h)               (6h)
```

---

## 📜 階段一：RFC 3227 數據揮發次序 (Order of Volatility)（必背核心）

在關機或中斷電源前，鑑識人員必須依據數據保存期限由短至長依序採集：
1. **暫存器與快取記憶體 (Registers & Cache)**
2. **路由表、ARP 快取、進程表與核心記憶體 (Routing table, ARP, Process table, Kernel Memory)**
3. **臨時檔案系統 (Temporary file systems)**
4. **硬碟實體資料 (Disk data)**
5. **遠端日誌與網路監控記錄 (Remote logging and network data)**
6. **實體拓撲與媒體備份 (Physical configuration and backup media)**

> ⚠️ **嚴禁行為**：面對可疑主機直接拔除電源線（會導致記憶體內之非對稱金鑰與無檔案木馬永久消失！）。

---

## 📋 自我評估檢查點

- [ ] 默背 RFC 3227 數據揮發順序前四項。
- [ ] 說明防寫設備 (Hardware/Software Write Blocker) 的必要性與原理。
- [ ] 解釋數位證據監管鏈 (Chain of Custody, CoC) 表格必須包含哪些法定欄位。
