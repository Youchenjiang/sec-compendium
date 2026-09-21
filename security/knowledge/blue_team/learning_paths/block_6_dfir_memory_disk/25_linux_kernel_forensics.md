# 🐧 Linux 核心與 Rootkit 鑑識深度學習路徑 (Linux Kernel & eBPF Forensics)
> 對應藍隊防衛矩陣：**領域 25** (25.1 ~ 25.4)
> 預計總投入時間：**35 ~ 45 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
ps 指令看不到就當作沒進程 ──►    能突破 LKM 核心級 Rootkit 與 DKOM 隱蔽技術
不知動態庫可被惡意劫持   ──►    掌握 /etc/ld.so.preload 與 LD_PRELOAD 攔截機制
對核心監控毫無概念       ──►    能運用現代 eBPF 技術實作核心級無感異常追蹤
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
LKM核心模組與Rootkit  動態庫劫持排查  eBPF核心遙測追蹤  Linux記憶體採集(LiME)
(10h)                (8h)            (10h)             (8h)
```

---

## 🧩 階段一：LKM (Loadable Kernel Module) 與 Rootkit 原理（約 10 小時）

- **Rootkit 隱匿手法**：
  - 核心模組卸載自身於 `/proc/modules` 的鏈結（斷鏈隱蔽）。
  - Hook 系統呼叫表 (Syscall Table Hooking)，例如修改 `sys_getdents64` 以過濾特定前綴的後門檔案。
- **用戶態動態庫劫持**：
  - 攻擊者在 `/etc/ld.so.preload` 寫入惡意 `.so`，所有執行檔啟動時皆優先載入惡意庫並替換 `readdir()`。

---

## 📋 自我評估檢查點

- [ ] 說出 Linux 用戶態 Rootkit (LD_PRELOAD) 與核心態 Rootkit (LKM) 的架構差異。
- [ ] 能使用 `lsmod` 與 `/sys/module/` 進行模組一致性比對。
- [ ] 說明 LiME (Linux Memory Extractor) 核心模組採集實體記憶體映像的步驟。
