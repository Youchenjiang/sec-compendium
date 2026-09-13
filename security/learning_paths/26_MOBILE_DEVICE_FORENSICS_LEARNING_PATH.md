# 📱 行動裝置鑑識深度學習路徑 (Android & iOS Forensics)
> 對應藍隊防衛矩陣：**領域 26** (26.1 ~ 26.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
只會裝 APK 不知底層結構  ──►    能反編譯 AndroidManifest.xml 審查惡意權限
手機被鎖死無法提取資料   ──►    掌握 ADB 邏輯萃取與物理映像 (Physical Dump) 差異
面對 iOS 封閉系統束手無策──►    能解析 iTunes 加密備份與鑰匙圈 (Keychain) 敏感資料
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
APK靜態反編譯審查  Android SQLite暫存解析  iOS備份提取與密鑰鏈  鑑識提取等級辨析
(10h)             (10h)                   (8h)                 (6h)
```

---

## 🤖 階段一：Android APK 結構與靜態解包審查（約 10 小時）

```
APK (ZIP 封裝架構)
├── AndroidManifest.xml (二進位清單: 宣告 Permission、Activity、Service、Receiver)
├── classes.dex (Dalvik/ART 虛擬機可執行字節碼)
├── lib/ (JNI 原生動態庫 .so)
└── res/ & resources.arsc (編譯後的 UI 資源與文字)
```

- 使用 `jadx-gui` 將 `classes.dex` 反編譯為可讀的 Java 原始碼。

---

## 📋 自我評估檢查點

- [ ] 說明 Android 邏輯提取 (Logical)、檔案系統提取 (File System) 與物理提取 (Physical) 的深度差異。
- [ ] 能在 `AndroidManifest.xml` 中找出高危惡意廣播接收器 (BroadcastReceiver)。
- [ ] 熟練使用 SQLite 查看通訊軟體 (Line, Telegram) 的快取資料庫與未加密媒體檔。
