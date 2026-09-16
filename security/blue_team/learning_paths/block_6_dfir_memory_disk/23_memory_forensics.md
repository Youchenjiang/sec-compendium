# 🧠 記憶體鑑識深度學習路徑 (Memory Forensics - 完整從零到精通)
> 對應藍隊防衛矩陣：**領域 23** (23.1 ~ 23.4)
> 預計總投入時間：**40 ~ 60 小時**（視基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                    這份路徑帶你到達的位置
─────────────────               ────────────────────────────
知道記憶體鑑識是什麼   ──►    能獨立分析真實事件記憶體映像
聽過 Volatility        ──►    熟練使用 10+ 個 plugin 組合推理
看過 CTF 題目          ──►    能在 CyberDefenders / HTB 獨立解題
```

---

## 🧱 第零關：先確認你有這些基礎

在開始之前，以下概念你應該有基本認識（不需精通，但不能完全陌生）：

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| Windows 進程 (Process) 是什麼 | 知道 PID、父子關係、可執行檔路徑 | [Microsoft: Processes and Threads](https://learn.microsoft.com/windows/win32/procthread/processes-and-threads) |
| 虛擬記憶體是什麼 | 知道每個進程有獨立的虛擬位址空間 | [Microsoft: Virtual Address Space](https://learn.microsoft.com/windows/win32/memory/virtual-address-space) |
| DLL 是什麼 | 知道程式會載入外部程式庫 | 了解即可 |
| 基本命令列操作 | 能執行 `volatility3` 指令、看懂輸出 | 能用命令列即可 |

> 如果以上有任何一項完全不懂，先花 2~3 小時補一下，後面的路會順很多。

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 → 階段二 → 階段三 → 階段四 → 階段五
理論基礎  工具安裝  核心技術  進階偵測  實戰綜合
(8h)     (2h)     (12h)    (10h)    (18h)
```

---

## 🏁 階段一：理論基礎（約 8 小時）

### 1.1 Windows 記憶體的三層結構

你必須理解記憶體的層次才能理解「為什麼有些東西能被隱藏」：

```
應用層 (User Mode)
  └─ 每個進程的虛擬位址空間 (0x0 ~ 0x7FFFFFFF)
       ├─ 堆疊 (Stack)
       ├─ 堆積 (Heap)
       ├─ 載入的 DLL
       └─ 進程 PEB (Process Environment Block)

核心層 (Kernel Mode)
  └─ 核心虛擬位址空間 (0x80000000 ~ 0xFFFFFFFF)
       ├─ EPROCESS 結構 (進程核心物件)
       ├─ ETHREAD 結構 (執行緒核心物件)
       ├─ 非換頁池 NonPagedPool (惡意程式最愛藏的地方)
       └─ VAD 樹 (Virtual Address Descriptor Tree)
```

**📖 必讀材料：**
- [Microsoft Sysinternals: Windows Internals 參考資源](https://learn.microsoft.com/sysinternals/resources/windows-internals) — 核心教材，至少讀 Process 章節
- [Windows Internals Part 1 免費章節摘要 (Scribd)](https://www.scribd.com/) — 補充理解

### 1.2 記憶體映像類型

| 類型 | 說明 | 鑑識價值 |
|------|------|---------|
| **Full Memory Dump** (`.raw`, `.mem`, `.dmp`) | 完整實體記憶體快照 | ⭐⭐⭐⭐⭐ 最完整 |
| **Crash Dump** (`MEMORY.DMP`) | 系統崩潰時自動產生 | ⭐⭐⭐⭐ 通常包含完整記憶體 |
| **Hibernation File** (`hiberfil.sys`) | 睡眠時記憶體快照 | ⭐⭐⭐ 壓縮格式，需轉換 |
| **PageFile** (`pagefile.sys`) | 虛擬記憶體延伸檔 | ⭐⭐ 可補充已換頁的資料 |

### 1.3 EPROCESS 是記憶體鑑識的心臟

```
EPROCESS (約 0x900 bytes)
├─ ActiveProcessLinks ← 雙向鏈表，pslist 就讀這個
│    ↕ (惡意程式 DKOM 攻擊會把自己從這裡斷鏈)
├─ UniqueProcessId (PID)
├─ InheritedFromUniqueProcessId (PPID)
├─ ImageFileName (前 15 字元的進程名稱)
├─ Peb → ProcessParameters → ImagePathName (完整路徑)
├─ VadRoot → VAD 二元搜尋樹 (記憶體區域分配)
└─ ObjectTable → 進程開啟的所有 Handle 表
```

**🧠 關鍵理解**：
- `pslist` 走 `ActiveProcessLinks` 鏈表 → 被 DKOM 斷鏈的進程看不到
- `psscan` 掃描 NonPagedPool 找 EPROCESS 特徵簽名 (`PROC`) → 能找到被隱藏的進程
- **這就是為什麼要兩個 plugin 交叉比對**

---

## 🔧 階段二：工具安裝與環境建置（約 2 小時）

### 2.1 安裝 Volatility 3

```bash
# 建議用 Python 虛擬環境
python -m venv vol3-env
vol3-env\Scripts\activate  # Windows

pip install volatility3

# 驗證安裝
vol -h
```

> **小提示**：符號表 (Symbol Tables) 是 Volatility 3 分析 Windows 記憶體的關鍵。
> 第一次分析會自動下載，需要網路連線。

**📖 官方文件：**
- [Volatility 3 官方文件](https://volatility3.readthedocs.io/)
- [Volatility Foundation GitHub](https://github.com/volatilityfoundation/volatility3)

### 2.2 準備練習記憶體映像

| 來源 | 格式 | 下載方式 |
|------|------|---------|
| [Digital Corpora](https://digitalcorpora.org/corpora/memory-images) | `.raw` | 直接下載，免費 |
| [DFRWS 歷年挑戰題](https://dfrws.org/forensic-challenges/) | 多種 | 免費下載 |
| [MemLabs (GitHub)](https://github.com/stuxnet999/MemLabs) | `.raw` | 免費，含解題指南 |

> **MemLabs** 是最適合初學者的練習材料——有 6 個難度遞增的記憶體映像，每個都有完整解題思路，強烈推薦從這裡開始。

---

## 🔍 階段三：核心技術精通（約 12 小時）

依序學習以下 Plugin 群組，**每個 Plugin 都要：1. 理解它在找什麼 2. 跑一遍看輸出 3. 能解釋為什麼**

### 3.1 進程分析三件組

```bash
# 1. 從 EPROCESS 雙向鏈表列出進程（被 DKOM 隱藏的找不到）
vol -f memory.raw windows.pslist

# 2. 以樹狀結構顯示父子關係（異常父子關係是重要線索）
vol -f memory.raw windows.pstree

# 3. 掃描 pool 標籤找 EPROCESS（能找到被斷鏈的隱藏進程）
vol -f memory.raw windows.psscan
```

**✅ 你該能回答：**
- pslist 和 psscan 結果不一致代表什麼？
- 哪些進程應該只有一個實例（`lsass.exe`, `csrss.exe`, `services.exe`）？
- `cmd.exe` 的父進程應該是什麼？

### 3.2 正常進程基準線（必背）

| 進程名稱 | 正常父進程 | 正常執行路徑 | 正常個數 |
|---------|-----------|-------------|---------|
| `System` | 無 (PID 4) | N/A | 1 |
| `smss.exe` | System (4) | `\Windows\System32\smss.exe` | 1 |
| `csrss.exe` | smss.exe | `\Windows\System32\csrss.exe` | 每個 Session 1 個 |
| `wininit.exe` | smss.exe | `\Windows\System32\wininit.exe` | 1 |
| `services.exe` | wininit.exe | `\Windows\System32\services.exe` | 1 |
| `lsass.exe` | wininit.exe | `\Windows\System32\lsass.exe` | **1（嚴格）** |
| `svchost.exe` | services.exe | `\Windows\System32\svchost.exe` | 多個（正常） |
| `explorer.exe` | userinit.exe | `\Windows\explorer.exe` | 每個登入用戶 1 個 |

> ⚠️ **惡意程式常偽裝**：`lsas.exe`（少一個 s）、`svch0st.exe`（數字代替字母）、在錯誤路徑執行的 `svchost.exe`。

### 3.3 DLL 與命令列分析

```bash
# 列出進程載入的所有 DLL
vol -f memory.raw windows.dlllist --pid 1234

# 查看進程啟動時的命令列參數（PowerShell 混淆常在這裡現形）
vol -f memory.raw windows.cmdline

# 查看環境變數（偵測繞過手法）
vol -f memory.raw windows.envars --pid 1234
```

### 3.4 網路連線分析

```bash
# 列出活動的 TCP/UDP 連線（包含 PID 對應）
vol -f memory.raw windows.netscan

# 顯示 TCP 連線狀態
vol -f memory.raw windows.netstat
```

**✅ 你該能回答：**
- 哪個 PID 建立了外連連線？
- 目的 IP 和 Port 是否異常？（常見 C2 Port：4444, 8080, 443, 1337）

### 3.5 登錄檔提取

```bash
# 列出記憶體中的 Hive
vol -f memory.raw windows.registry.hivelist

# 列印特定登錄鍵值
vol -f memory.raw windows.registry.printkey --key "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
```

---

## ⚔️ 階段四：進階偵測技術（約 10 小時）

### 4.1 代碼注入偵測 (malfind)

```bash
# 掃描所有進程的 VAD 節點，找可疑的可執行記憶體區域
vol -f memory.raw windows.malfind

# 針對特定進程
vol -f memory.raw windows.malfind --pid 1234
```

**malfind 的判定邏輯：**
```
可疑條件（同時滿足時高度可疑）：
1. VAD 保護屬性 = PAGE_EXECUTE_READWRITE (可執行 + 可寫入)
2. 該區域不對應任何已知 DLL（Mapped: 無）
3. 區域開頭有 MZ 標頭（4D 5A）→ 內嵌 PE 檔案
4. 有 shellcode 特徵位元組
```

> ⚠️ **注意**：malfind 誤報率高。不是所有輸出都是惡意的——需要結合其他 plugin 交叉確認。

### 4.2 DKOM 隱藏進程偵測

**方法：交叉比對 pslist 和 psscan**

```python
# 手動比對邏輯（可寫腳本）
pslist_pids = {進程PID集合，從 pslist 取得}
psscan_pids = {進程PID集合，從 psscan 取得}

# 在 psscan 有、在 pslist 沒有的 = 被隱藏的進程
hidden = psscan_pids - pslist_pids
```

### 4.3 記憶體憑證萃取

```bash
# 從 lsass.exe 記憶體提取 NTLM Hash
vol -f memory.raw windows.hashdump

# 提取 LSA 秘密
vol -f memory.raw windows.lsadump

# 導出 lsass.exe 完整記憶體段（供離線分析）
vol -f memory.raw windows.memmap --pid <lsass_pid> --dump
```

### 4.4 Rootkit 偵測

```bash
# 比對 SSDT 系統服務呼叫表是否被 Hook
vol -f memory.raw windows.ssdt

# 偵測隱藏驅動程式（交叉比對）
vol -f memory.raw windows.modules   # 走鏈表
vol -f memory.raw windows.modscan   # 掃描 pool
# modules 有但 modscan 沒有、或 modscan 有但 modules 沒有的都值得注意
```

---

## 🏆 階段五：實戰綜合練習（約 18 小時）

### 5.1 初階練習（先從這裡開始）

| 題目 | 難度 | 連結 | 練習重點 |
|------|------|------|---------|
| **MemLabs Lab 1** | ⭐ | [GitHub: MemLabs](https://github.com/stuxnet999/MemLabs) | pslist、cmdline、filescan 基礎流程 |
| **MemLabs Lab 2** | ⭐⭐ | [GitHub: MemLabs](https://github.com/stuxnet999/MemLabs) | malfind、注入偵測 |
| **MemLabs Lab 3** | ⭐⭐ | [GitHub: MemLabs](https://github.com/stuxnet999/MemLabs) | 登錄檔、隱寫術結合 |
| **MemLabs Lab 4~6** | ⭐⭐⭐ | [GitHub: MemLabs](https://github.com/stuxnet999/MemLabs) | 進階綜合場景 |

### 5.2 中階靶場（主力練習區）

| 題目 | 難度 | 連結 | 練習重點 |
|------|------|------|---------|
| **CyberDefenders: RedLine** | ⭐⭐ | [CyberDefenders](https://cyberdefenders.org/blueteam-ctf-challenges/redline/) | 綜合進程、網路、DLL 分析 |
| **CyberDefenders: Lespion** | ⭐⭐⭐ | [CyberDefenders](https://cyberdefenders.org/blueteam-ctf-challenges/lespion/) | 進程樹異常、憑證提取 |
| **CyberDefenders: BlackEnergy** | ⭐⭐⭐ | [CyberDefenders](https://cyberdefenders.org/blueteam-ctf-challenges/blackenergy/) | 真實 APT Rootkit 樣本分析 |
| **Blue Team Labs Online: Memory Analysis** | ⭐⭐ | [BTLO](https://blueteamlabs.online/) | 引導式記憶體調查 |

### 5.3 進階挑戰（考前衝刺）

| 題目 | 難度 | 連結 | 練習重點 |
|------|------|------|---------|
| **HTB Sherlocks: Brutus** | ⭐⭐⭐ | [HTB Sherlocks](https://app.hackthebox.com/sherlocks) | 混合 EVTX + 記憶體分析 |
| **DFRWS 2005 Challenge** | ⭐⭐⭐⭐ | [DFRWS](https://dfrws.org/forensic-challenges/) | 經典 rootkit 案例，業界標準 |
| **Digital Corpora: Scenario M57** | ⭐⭐⭐⭐ | [Digital Corpora](https://digitalcorpora.org/) | 企業級完整調查場景 |

---

## 📋 自我評估檢查點

**全部能回答才算通過該階段，不能蒙混。**

### 階段一通過測試
- [ ] 說明 `pslist` 和 `psscan` 為何結果可能不同？
- [ ] `EPROCESS.ActiveProcessLinks` 被 DKOM 攻擊斷鏈後會發生什麼？
- [ ] `hiberfil.sys` 和完整記憶體映像有何差異？

### 階段三通過測試
- [ ] 在 30 秒內說出 `lsass.exe` 的正常父進程、執行路徑、正常個數
- [ ] 看到 `svchost.exe` 父進程是 `explorer.exe`，你的反應是什麼？
- [ ] 一個進程開啟了 TCP 4444 埠的外連，你會接著用哪些 plugin 調查？

### 階段四通過測試
- [ ] `malfind` 輸出中，哪三個條件同時出現最危險？
- [ ] 如何區分 `malfind` 的誤報和真實注入？
- [ ] 提取 NTLM Hash 的 plugin 是什麼？需要哪個進程的記憶體？

### 最終通過測試
- [ ] 獨立完成 MemLabs Lab 1 到 Lab 3，**不看 writeup**
- [ ] 在 CyberDefenders 完成至少 2 個記憶體鑑識挑戰，得分 ≥ 80%

---

## 📚 延伸精進資源

| 類型 | 資源 | 說明 |
|------|------|------|
| 📘 書籍 | [The Art of Memory Forensics (Wiley)](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics-p-9781118825099) | 記憶體鑑識聖經，作者即 Volatility 開發者 |
| 📝 速查 | [Andrea Fortuna: Volatility Cheatsheet](https://andreafortuna.org/2017/06/25/volatility-my-own-cheatsheet-part-1-image-identification/) | Plugin 速查與實例解說 |
| 🔧 工具 | [Volatility Workbench](https://www.osforensics.com/tools/volatility-workbench.html) | Volatility 的 GUI 前端，適合初學者 |
| 🎥 影片 | [SANS: Memory Forensics YouTube 精華](https://www.youtube.com/c/SANSInstitute) | 免費公開影片 |

---

## ⏱️ 依考試距離調整策略

| 距考試還有 | 建議投入 | 重點放在 |
|-----------|---------|---------|
| **4 週以上** | 完整走完 5 個階段 | 全部按順序走 |
| **2~3 週** | 每天 2 小時，共 30 小時 | 速讀階段一、重點放階段三+五 |
| **1 週** | 每天 3 小時，共 18 小時 | 只做階段三 + MemLabs Lab 1~3 + 1 個 CyberDefenders |
| **3 天內** | 每天 4 小時 | 背進程基準線表 + 做 MemLabs Lab 1 |

---

*本路徑對應藍隊防衛矩陣領域 23：記憶體鑑識實戰 (23.1 ~ 23.4)*
*建議搭配 [`BLUE_TEAM_PRACTICE_RESOURCES_INDEX.md`](../../index.md) 中的靶場連結一起使用*
