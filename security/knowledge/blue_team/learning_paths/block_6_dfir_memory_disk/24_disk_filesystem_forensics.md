# 💾 磁碟檔案系統鑑識深度學習路徑 (Disk & Filesystem Forensics)
> 對應藍隊防衛矩陣：**領域 24** (24.1 ~ 24.4)
> 預計總投入時間：**40 ~ 55 小時**（DFIR 核心主力）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
以為檔案丟進垃圾桶就是刪除 ──►  能從 NTFS $MFT 與 USN Journal 完整還原痕跡
分不清檔案建立與修改時間 ──►    精通 Timestomping 時間偽造辨析 ($SI vs $FN)
找程式執行證據全靠猜     ──►    掌握 Windows 執行三大鐵證 (Prefetch, ShimCache, Amcache)
```

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 → 階段二 → 階段三 → 階段四 → 階段五
NTFS與$MFT結構  時間戳偽造辨析  程式執行三大鐵證  登錄檔與活動痕跡  VSS磁碟陰影複製
(10h)          (8h)           (12h)            (10h)            (8h)
```

---

## 📂 階段一：NTFS 檔案系統與 $MFT 主檔案表（約 10 小時）

NTFS 所有檔案皆記錄在 `$MFT` 中，每個檔案記錄長度固定為 1024 Bytes：
- `$STANDARD_INFORMATION ($SI, 0x10)`：標準時間戳（Windows API 可修改，常被 Timestomping 偽造）。
- `$FILE_NAME ($FN, 0x30)`：由 NTFS 核心自動維護的時間戳，一般使用者態 API 無法修改。
- **時間偽造辨析原則**：**當 `$SI` 的建立時間早於 `$FN` 時，有 99% 機率經過惡意時間篡改 (Timestomping)**！

---

## ⚡ 階段二：Windows 程式執行三大鐵證（約 12 小時）

| 鑑識神器 (Artifact) | 存放路徑 / 機制 | 鑑識價值與證據力 |
| :--- | :--- | :--- |
| **Prefetch 預先擷取檔** | `C:\Windows\Prefetch\*.pf` | 記錄最近 8 次執行時間戳、執行總次數、載入之 DLL 清單 |
| **ShimCache (AppCompat)**| `SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache` | 記錄系統重啟前的所有可執行檔路徑、大小、上次修改時間 |
| **Amcache.hve** | `C:\Windows\appcompat\Programs\Amcache.hve` | 記錄程式的 **SHA-1 雜湊值**、首次執行時間，無實體檔亦可溯源 |

---

## 📋 自我評估檢查點

- [ ] 說明 NTFS 中 `$SI` 與 `$FN` 屬性在鑑識時間戳防偽中的對比邏輯。
- [ ] 說出 Prefetch、ShimCache、Amcache 各自提供的關鍵資訊與互補價值。
- [ ] 掌握如何使用 FTK Imager 或 Eric Zimmerman 工具 (MFTECmd, PECmd) 解析證據。
