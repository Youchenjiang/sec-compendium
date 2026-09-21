# 💻 端點核心日誌與排查深度學習路徑 (Windows Endpoint Log Triage)
> 對應藍隊防衛矩陣：**領域 14** (14.1 ~ 14.4)
> 預計總投入時間：**35 ~ 45 小時**（SOC 藍隊基石）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
在事件檢視器中茫然捲動   ──►    秒記 4624/4625/4688/7045 等核心 Event ID
分不清登入類型 2 與 3    ──►    精通 Logon Type 2/3/10/7 的攻防研判意義
只看有報警的防毒日誌     ──►    能結合命令列參數與進程樹挖掘未知隱蔽威脅
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
Windows登入日誌  進程建立4688  服務與持續性7045  EDR與Defender日誌
(10h)           (10h)         (8h)             (8h)
```

---

## 🔐 階段一：Windows 登入事件 (4624 / 4625) 與登入類型（約 10 小時）

### 1.1 核心 Logon Types 對照表（藍隊必背標準）

| 登入類型 (Logon Type) | 名稱 | 實務場景與排查意義 |
| :---: | :--- | :--- |
| **2** | **Interactive (互動式登入)** | 使用者坐在本機螢幕鍵盤前手動輸入帳密登入 |
| **3** | **Network (網路登入)** | 透過網路共享連線 (SMB, IPC$, Net Share)、PsExec 存取 |
| **4** | **Batch (批次排程)** | 系統排程作業 (Task Scheduler) 以該帳戶權限啟動 |
| **5** | **Service (服務登入)** | 系統後台常駐服務以此帳戶啟動 |
| **7** | **Unlock (解除鎖定)** | 使用者解除螢幕鎖定畫面 |
| **10** | **RemoteInteractive (遠端桌面)** | 透過 RDP (Remote Desktop) 遠端連入 |

---

## ⚙️ 階段二：進程建立審計 (Event ID 4688)（約 10 小時）

### 2.1 啟用命令列參數記錄 (Include Command Line)
- 預設 4688 僅記錄程式路徑，透過群組原則 (GPO) 啟用 `Include command line in process creation events`。
- 排查高危 LOLBAS 指令：
  - `certutil.exe -urlcache -split -f http://...`
  - `powershell.exe -enc ...` (Base64 編碼執行)
  - `vssadmin delete shadows /all /quiet` (勒索軟體刪除備份特徵)

---

## 📋 自我評估檢查點

- [ ] 熟練說出 Logon Type 2、3、10 分別代表的真實登入行為。
- [ ] 說出勒索軟體在執行加密前最常下的指令與對應 Event ID。
- [ ] 說明 Event ID 7045 (新服務安裝) 在橫向移動 (如 PsExec) 排查中的關鍵價值。
