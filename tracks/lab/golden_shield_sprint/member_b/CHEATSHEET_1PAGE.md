# 🛡️ 隊員 B（葉）一頁紙秒選速查表（Pwn ✕ Reverse ✕ 網路通識）

> **用途**：最後掃讀 ＋ 考場「看特徵 → 秒選」對照。單選不扣分、靠辨識特徵拿分。
> **範圍**：Pwn（主責）＋ Reverse x86/x64（主責）＋ Misc/網路通識 1/3（IPsec/VPN/SNMP/VLAN/TCP/DNS）＋ 工具總表。
> **配套**：模擬卷 [`exams/FINAL_SPRINT_MASTER.md`](exams/FINAL_SPRINT_MASTER.md)
> 由隊員 A 協助整理。

---

## 🔧 單元一：x86/x64 組語與暫存器

| 指令 | 作用（秒記） |
| :--- | :--- |
| `mov a, b` | b → a（搬移）|
| `lea a, [b]` | 把「位址」算出來放 a（**不解參照**，常用於算指標/乘法）|
| `cmp a, b` | 算 `a-b` 只設旗標（比較）|
| `test a, a` | `a AND a` 設旗標；`test eax,eax` = 判斷 eax 是否為 0 |
| `jmp` | 無條件跳 |
| `je/jz` | 相等/為零跳；`jne/jnz` 不等/非零跳 |
| `jg/jl`（有號）`ja/jb`（無號）| 大於/小於跳 |
| `call` | push 返回位址 + 跳（呼叫）|
| `ret` | pop 返回位址回去 |
| `push/pop` | 壓/彈堆疊 |
| `int3`(`0xCC`) | 軟體中斷點 |

| 暫存器 | 用途 |
| :-- | :-- |
| `eax`/`rax` | **回傳值** |
| `esp`/`rsp` | 堆疊指標（棧頂）|
| `ebp`/`rbp` | 堆疊框基底 |
| `eip`/`rip` | 下一條指令位址（Pwn 終極目標：控制它）|
| ZF/SF/CF/OF | 零/負/進位/溢位旗標 |

> **棧由高位址往低位址長**；`call` 會把返回位址壓進棧 → buffer overflow 蓋掉它就能劫持流程。

---

## 📞 單元二：呼叫慣例（Calling Convention）

| 慣例 | 參數傳遞 | 誰清棧 | 回傳 | 出沒 |
| :--- | :--- | :--- | :--- | :--- |
| **cdecl**（x86） | 棧，右→左 | **呼叫方**(caller) | eax | C 預設 |
| **stdcall**（x86） | 棧，右→左 | **被呼叫方**(callee，`ret n`) | eax | Win32 API |
| **fastcall**（x86） | 前幾個走 ecx/edx | callee | eax | |
| **x64 Windows** | **RCX, RDX, R8, R9** + 棧 | caller | rax | +32B shadow space |
| **x64 System V**（Linux）| **RDI, RSI, RDX, RCX, R8, R9** + 棧 | caller | rax | Linux/macOS |

> 🔑 **x64 傳參秒記**：Windows=`RCX RDX R8 R9`；Linux=`RDI RSI RDX RCX R8 R9`。差別常考。

---

## 🧩 單元三：PE 結構與脫殼

| 名詞 | 意義 |
| :--- | :--- |
| **MZ** | PE/EXE 檔頭（DOS header，`4D 5A`）|
| **PE header** | 真正的檔頭，含節區表 |
| 常見節區 | `.text`(碼) `.data`(資料) `.rdata`(唯讀) `.idata`(匯入) |
| **RVA** | 相對虛擬位址（相對 ImageBase 的偏移）|
| **VA** | `VA = ImageBase + RVA` |
| **IAT** | 匯入位址表（記匯入函數的實際位址）|
| **OEP** | 原始進入點（**脫殼後要找的真正入口**）|
| **UPX** | 最常見殼，`upx -d` 可解 |
| **ESP 定律** | 殼的 stub 跑完後 ESP 回到原值 → 對 ESP 下硬體斷點 → 停在 OEP 附近 |
| **DIE** | Detect It Easy，辨識殼/編譯器/檔案類型 |

---

## 🕵️ 單元四：反除錯（Anti-Debug）

| 手法 | 原理 |
| :--- | :--- |
| `IsDebuggerPresent` | 查 PEB 的 BeingDebugged 旗標 |
| `CheckRemoteDebuggerPresent` | 查遠端除錯器 |
| **NtGlobalFlag** | PEB 旗標；被除錯時 heap 旗標會變 |
| **INT 3 掃描**（`0xCC`） | 軟體斷點會在碼中插入 `0xCC`，程式掃到就知被下斷點 |
| `rdtsc` 時間差 | 單步執行會變慢 → 偵測 |

---

## 💉 單元五：程序注入與 DLL 劫持

**Process Injection 標準 API 順序**（必背順序題）：
```
OpenProcess → VirtualAllocEx → WriteProcessMemory → CreateRemoteThread
 (開目標)     (在目標配記憶體)   (寫入 shellcode/DLL路徑)  (建遠端執行緒跑它)
```
- **Process Hollowing（掉空）**：建合法程序→挖空其映像→換成惡意碼。工具 **Hollow Hunter** 偵測（2024 考過）。
- **DLL 搜尋順序劫持**：程式只用檔名(未給完整路徑)載入 DLL → 攻擊者把惡意 DLL 放進較前的搜尋路徑。

---

## 🛡️ 單元六：Pwn 保護機制（防什麼/驗證/繞過）

| 機制 | 防什麼 | 怎麼驗證 | 怎麼繞 |
| :--- | :--- | :--- | :--- |
| **NX / DEP** | 棧不可執行（擋 shellcode）| checksec 看 NX | **ROP**（重用現有碼）|
| **ASLR** | 位址隨機化 | — | **洩漏位址** |
| **PIE** | 連「碼段」基底也隨機 | checksec 看 PIE | 洩漏碼段位址 |
| **Stack Canary** | 偵測棧溢位 | checksec 看 Canary | 洩漏 canary / 精準蓋 / 爆破(fork) |
| **RELRO** | 保護 GOT | checksec：Partial/Full | Full 時 GOT 唯讀→封鎖 GOT 覆寫 |

- **Canary 位置**：放在「局部緩衝區」與「saved EBP/返回位址」之間；ret 前檢查，被改→呼叫 `__stack_chk_fail` 中止。
- **RELRO**：Partial（GOT 可寫）vs **Full（GOT 唯讀，擋 GOT hijack）**。

---

## 💥 單元七：溢位、ROP 與格式化字串

| 題型 | 要點 |
| :--- | :--- |
| Buffer Overflow | 蓋掉返回位址 → 控制 `eip/rip` |
| **ret2text** | 跳到程式**自身**已有的碼 |
| **ret2libc** | 跳到 libc 函數（如 `system("/bin/sh")`）|
| ROP | 串接 `gadget`（以 `ret` 結尾的碼片段）繞 NX |
| **格式化字串** | `%x`/`%p` **洩漏**棧、`%s` **讀**指標指向記憶體、`%n` **寫**(把已輸出位元組數寫入位址)|
| Heap：UAF | Use-After-Free（釋放後仍使用）|
| Heap：Double Free | 重複釋放 → tcache 毒化 |
| 整數溢位 vs NULL deref | 前者數值環繞、後者解參照空指標 |

> **格式化字串三連記**：`%p/%x`=洩漏、`%s`=讀、`%n`=寫。

---

## 🐧 單元八：Linux 提權常識

| 點 | 說明 |
| :--- | :--- |
| **SUID** | `-perm -4000`；以檔主(常 root)身分執行 → GTFOBins |
| **Capabilities** | 細粒度 root；`getcap -r /`；`cap_setuid` 可提權 |
| **Dirty COW**(CVE-2016-5195) | Copy-On-Write 競態 → 寫入唯讀檔案提權 |

---

## 🌐 單元九：網路通識（隊員 B 分攤）

### IPsec
| 協定 | 提供 |
| :-- | :-- |
| **AH** | 完整性+來源認證，**不加密** |
| **ESP** | 加密 + 完整性 + 認證 |

| 模式 | 範圍 | 用途 |
| :-- | :-- | :-- |
| **Transport** | 只加密 payload | 主機對主機 |
| **Tunnel** | 整包加密再封裝 | 閘道對閘道（站對站 VPN）|

### VPN / SNMP
- **VPN**：site-to-site（閘道對閘道，連兩個網路）vs client-to-site（遠端使用者連進公司）。
- **SNMP**：v1/v2c 用明文 community string；**v3 加入認證與加密**。Port **UDP 161**（agent）、**162**（trap）。

### 交換/ARP
- **VLAN hopping**：switch spoofing、double tagging。防：關 DTP、改 native VLAN。
- **ARP 欺騙**：偽造 ARP 回覆做 MITM。防：**DAI（Dynamic ARP Inspection）**、靜態 ARP。

### TCP / DNS
- **三次握手**：SYN → SYN-ACK → ACK。
- **TIME_WAIT**：主動關閉方等 2MSL 確保尾封包處理完。
- **SYN Flood**：灌 SYN 塞滿半開連線佇列（卡在 **SYN_RECV**）→ DoS。防：**SYN cookies**。
- **DNS 放大攻擊**：偽造來源 IP，小查詢→大回應灌向受害者。
- **DNSSEC 記錄**：RRSIG、DNSKEY、DS、NSEC/NSEC3。

---

## 🧰 單元十：工具總表（全員必會・誘答重點）

| 工具 | 用途 | 誘答陷阱 |
| :--- | :--- | :--- |
| IDA Pro | 靜態反組譯，圖形控制流 | **箭頭：綠=條件成立、紅=不成立、藍=無條件** |
| Ghidra | NSA 開源，有反編譯器 | 免費替代 IDA |
| x64dbg/x32dbg | Windows 動態除錯 | 32/64 要分清 |
| gdb+pwndbg | Linux 動態除錯 | Pwn 必備 |
| WinDbg | Windows 核心/使用者除錯 | |
| dnSpy | .NET 反編譯+除錯 | C#/.NET |
| Detect It Easy | 辨識殼/編譯器/檔案類型 | **不是 sqlmap** |
| angr / z3 | 符號執行 / 約束求解 | 自動解題 |
| **checksec** | 看保護(NX/Canary/PIE/RELRO) | |
| **pwntools** | 寫 exploit 的 Python 庫 | |
| **ROPgadget / one_gadget** | 找 gadget / 現成 execve | |
| pyinstxtractor | 解 PyInstaller 打包 exe | |
| **gflags** | Windows 除錯旗標 | **不是掃描工具**（2024 誘答）|
| **1768.py** | 抽 Cobalt Strike 設定（2024）| |
| **Hollow Hunter** | 偵測 process hollowing（2024）| |

---

## ⚠️ 誘答紅旗（看到要警覺）
- **x64 傳參**：Windows `RCX RDX R8 R9` ↔ Linux `RDI RSI RDX RCX R8 R9`,別記反。
- **NX 擋 shellcode → 繞過是 ROP**(不是洩漏);**ASLR → 繞過才是洩漏位址**。別配錯。
- **AH 不加密、ESP 才加密**。
- **cdecl 呼叫方清棧、stdcall 被呼叫方清棧**。
- **格式化字串 `%n` 是「寫」不是讀**;`%s` 才是讀。
- **gflags 非掃描、DIE 非 sqlmap、Hollow Hunter 是偵測掉空**。
- **MZ=Windows PE、7F ELF=Linux**,別和檔案隱寫的 Magic Bytes 搞混。
