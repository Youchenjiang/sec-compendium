# 🥷 終端防禦規避、直接系統調用與進程注入深度學習路徑 (EDR Evasion, Syscalls & Injection)
> 對應紅隊作戰矩陣：**Phase 6 (R22)** (R22.1 ~ R22.8)  
> 預計總投入時間：**35 ~ 40 小時**（視 x64 組合語言、Windows 核心呼叫門、PE 檔案結構與動態注入基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
呼叫 Win32 API 總被 EDR 攔截 ──►     透徹理解 EDR 於 ntdll.dll 的 Inline Hook 機制與跳板攔截
只聽過 Syscall 不懂底層差異  ──►     精通 Direct Syscalls、Indirect Syscalls 與 Halo's Gate 動態尋址
只會用傳統 CreateRemoteThread──►     掌握 Process Hollowing、Early Bird APC 注入與 PPID 父行程偽裝
腳本總是被 AMSI 或 ETW 報警  ──►     深入掌握記憶體位元組修補 (Patching) 與從磁碟重新掛載乾淨 DLL
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| x64 組合語言與 CPU 暫存器 | 理解 RAX, RCX, RDX, R8, R9 與 `syscall` 指令的執行時序 | [Intel 64 and IA-32 Architectures Software Developer Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) |
| Windows 系統調用表 (SSN) | 理解 System Service Number、`ntdll.dll` 匯出 stub 與核心模式切換 | [Windows Syscall Database (j00ru)](https://j00ru.vexillium.org/syscalls/nt/64/) |
| PE (Portable Executable) 格式 | 理解 DOS Header, NT Header, Section Table (`.text`, `.data`) 與匯出表 EAT | [Microsoft Learn: PE Format](https://learn.microsoft.com/windows/win32/debug/pe-format) |
| 行程與執行緒生命週期 | 理解 `CreateProcess`, `OpenProcess`, `VirtualAllocEx`, 佇列化 APC 與行程狀態 | [Microsoft Learn: Processes and Threads](https://learn.microsoft.com/windows/win32/procthread/processes-and-threads) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (10h) ─────► 階段二 (10h) ─────► 階段三 (10h) ─────► 階段四 (6h)
EDR User-Mode Hook   Direct / Indirect   AMSI / ETW 動態    隱蔽行程注入技術
原理與記憶體脫鉤對抗   系統調用突破實務    記憶體修補 (Patch) (Hollowing / APC)
```

---

## 🏛️ 階段一：EDR 使用者模式 API Hooking 原理與動態脫鉤（約 10 小時）

### 1.1 EDR 是如何監控 API 呼叫的？
當行程啟動時，EDR 的核心驅動程式會向該行程的使用者空間注入監控 DLL。
- **Inline Hooking 本質**：EDR 覆寫 `ntdll.dll` 中關鍵系統調用函數（如 `NtProtectVirtualMemory`, `NtWriteVirtualMemory`）的前 5 個位元組，將原本的指令替換為 `jmp <EDR_Agent.dll>`。
- **檢測方式**：當惡意程式呼叫這些函數時，執行流程先跳入 EDR 分析記憶體參數，若特徵異常則直接中斷。

### 1.2 動態脫鉤技術——Perun's Fart 原理
既然記憶體中的 `ntdll.dll` 已經被 EDR 污染，紅隊如何取得乾淨的代碼？
1. 行程自行從磁碟讀取原生唯讀檔案 `C:\Windows\System32\ntdll.dll`。
2. 在記憶體中解析該磁碟檔案的 PE 結構，定位其 `.text` 代碼區段。
3. 呼叫 `VirtualProtect()` 暫時將記憶體中被 Hook 的 `ntdll.dll` 的 `.text` 區塊改為可寫 (`RWX`)。
4. 使用磁碟中未被污染的原始位元組覆蓋目前記憶體，將 EDR 的 `jmp` 指令全數洗掉，瞬間解除監控！

---

## 🥩 階段二：直接系統調用 (Direct Syscalls) 與間接調用 (Indirect Syscalls)（約 10 小時）

### 2.1 Direct Syscalls 的優勢與致命弱點
- **原理**：攻擊程式不呼叫 `kernel32.dll` 或 `ntdll.dll`，而是在自身二進位檔案內嵌入一小段組合語言，自行將 SSN（系統服務號碼）載入 `EAX`，並直接發出 `syscall` 指令進入核心。
- **致命弱點**：現代進階 EDR 會監控系統調用的「返回位址 (Return Address)」。如果一個系統調用發生的位址不是位於 `ntdll.dll` 的位址空間內，而是來自未簽署的未知記憶體區段，EDR 將立即觸發告警！

### 2.2 Indirect Syscalls（間接系統調用，如 Halo's Gate）
```text
[攻擊程式]
   │
   ├── 1. 自行計算或動態取得正確的 SSN 號碼 (如 0x50) 放入 EAX
   │
   └── 2. 不在自身執行 syscall 指令，而是跳轉至 ntdll.dll 內部的合法 `syscall; ret` 指令位址！
                               │
                               ▼
               [ntdll.dll 內建的合法 syscall; ret]
                               │
                               ▼ 進入核心
```
- **核心價值**：呼叫堆疊（Call Stack）的來源與返回點均完全合法地位於 `ntdll.dll` 內部，徹底化解 EDR 的呼叫堆疊回溯分析（Call Stack Spoofing）。

---

## 🔬 階段三：執行期防護修補——AMSI 與 ETW Patching（約 10 小時）

### 3.1 AMSI (Antimalware Scan Interface) 記憶體修補
PowerShell 或腳本引擎執行任何字串前，會呼叫 `amsi.dll!AmsiScanBuffer`。
- **修補原理**：
  在目前行程記憶體中定位 `AmsiScanBuffer` 函數入口，覆寫前數個位元組為：
  `mov eax, 0x80070057; ret` (即直接回傳 `E_INVALIDARG` 錯誤代碼)。
- **結果**：AMSI 以為傳入參數錯誤而終止檢查，後續所有未混淆的攻擊腳本皆可暢行無阻！

### 3.2 ETW (Event Tracing for Windows) 遙測關閉
許多防毒產品依賴 ETW 收集端點事件。修補 `ntdll.dll!EtwEventWrite` 使其在開頭直接 `ret`，即可令系統停止發送遙測事件至 EDR 感應器。

---

## 🥷 階段四：隱蔽進程注入技術——Process Hollowing 與 Early Bird APC（約 6 小時）

### 4.1 Process Hollowing (進程掏空)
1. 以掛起模式 (`CREATE_SUSPENDED`) 啟動合法的微軟簽署行程（如 `svchost.exe`）。
2. 卸載其原始代碼區段，並將惡意 Shellcode / PE 寫入其記憶體位址。
3. 修改執行緒內容 (`SetThreadContext`) 的 `RCX` (進入點) 指向惡意代碼，最後呼叫 `ResumeThread`。

### 4.2 Early Bird APC Queue 注入
在行程主執行緒初始化、尚未載入任何 EDR Hooking DLL 的極早期階段，呼叫 `QueueUserAPC()` 將惡意 Shellcode 插入執行緒的非同步程序呼叫 (APC) 佇列，使惡意代碼在 EDR 啟動防禦前率先執行完畢。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚繪製 EDR Inline Hook 在記憶體中替換前置位元組的機器碼示意圖。
- [ ] 能解釋 Direct Syscall 與 Indirect Syscall 在對抗 EDR 呼叫堆疊審查時的根本差異。
- [ ] 能說明 Perun's Fart 技術從硬碟重新映射 `ntdll.dll` 脫鉤的四個核心步驟。
- [ ] 能寫出修補 `AmsiScanBuffer` 記憶體的 64 位元組合語言機器碼序列。
- [ ] 能比較 Process Hollowing 與 Early Bird APC 注入在繞過 EDR 監控視窗上的時序優勢。

---

## 🏆 推薦實戰靶場與題庫直達
1. **MalwareTech: Introduction to Reverse Engineering**：學習組合語言、PE 結構與 API 逆向基礎。[MalwareTech](https://www.malwaretech.com/)
2. **Sektor7: Windows Evasion Course Labs**：業界公認最權威之 EDR 規避與 Syscall 深度實作指南。
3. **CyberDefenders: SpotTheDrop / Titan**：藍隊取證挑戰，從記憶體傾印中逆向分析進階行程注入技術。[CyberDefenders](https://cyberdefenders.org/)
