# 🏁 隊員 B（葉）金盾獎初賽考前總衝刺大卷（50 題・實戰深度版）

> **範圍**：依 [`金盾獎初賽三人分工檢核表.md`](../../金盾獎初賽三人分工檢核表.md) 隊員 B 全主責——Reverse x86/x64 ＋ Pwn ＋ Misc/網路通識 1/3 ＋ 工具總表。
> **賽制**：單選、答錯不扣分、同分比速度 → **每題必填、不確定先標記、計算用紙筆**。
> **用法**：限時 40 分鐘。先遮選項、自己說出答案與理由再對文末解析。配套速查表 [`../CHEATSHEET_1PAGE.md`](../CHEATSHEET_1PAGE.md)。
> 由隊員 A 協助出題。

---

## 🔧 Part 1 — x86/x64 組語與逆向（Q1~Q12）

#### Q1.【test 指令】
`test eax, eax` 後接 `je label`，其語意為？
* (A) 若 eax 等於 0 則跳 label
* (B) 若 eax 不等於 0 則跳 label
* (C) 把 eax 清為 0
* (D) 將 eax 與 label 相加

#### Q2.【lea vs mov】
`lea eax, [ebx+4]` 與 `mov eax, [ebx+4]` 的差別為？
* (A) 完全相同
* (B) `lea` 把「位址 ebx+4」算出來放 eax；`mov` 把「ebx+4 指向的記憶體內容」放 eax
* (C) `lea` 會解參照、`mov` 不會
* (D) 兩者都只能用於浮點數

#### Q3.【cmp 的本質】
組語中 `cmp a, b` 實際做了什麼？
* (A) 將 b 搬進 a
* (B) 計算 `a - b` 但只更新旗標暫存器、不保存結果
* (C) 將 a 與 b 相乘
* (D) 無條件跳轉

#### Q4.【call/ret 與棧】
關於 `call func` 與 `ret`，下列何者正確？
* (A) `call` 會把「返回位址」壓入堆疊再跳到 func；`ret` 把它彈出並跳回
* (B) `call` 不會動堆疊
* (C) `ret` 會清空整個堆疊
* (D) `call` 等同 `jmp`，沒有返回機制

#### Q5.【回傳值暫存器】
x86/x64 中函數的「整數回傳值」慣例上放在哪個暫存器？
* (A) esp/rsp
* (B) ebp/rbp
* (C) eax/rax
* (D) eip/rip

#### Q6.【x64 System V 傳參】
Linux x64（System V ABI）中，函數前六個整數參數依序放在？
* (A) RDI, RSI, RDX, RCX, R8, R9
* (B) RCX, RDX, R8, R9, RDI, RSI
* (C) 全部壓堆疊
* (D) RAX, RBX, RCX, RDX, RSI, RDI

#### Q7.【x64 Windows 傳參】
Windows x64 呼叫慣例中，前四個整數參數依序放在？
* (A) RDI, RSI, RDX, RCX
* (B) RCX, RDX, R8, R9
* (C) RAX, RBX, RCX, RDX
* (D) 全部壓堆疊

#### Q8.【cdecl vs stdcall】
關於 cdecl 與 stdcall（x86）的差別，下列何者正確？
* (A) cdecl 由「呼叫方」清理堆疊參數；stdcall 由「被呼叫方」清理（`ret n`）
* (B) 兩者清棧方完全相同
* (C) cdecl 是 Windows API 專用
* (D) stdcall 把參數放暫存器、不用堆疊

#### Q9.【IDA 圖形視圖箭頭】
IDA 圖形視圖中，條件跳轉分出的「綠色」箭頭代表？
* (A) 條件成立（taken）
* (B) 條件不成立（not taken）
* (C) 無條件跳轉
* (D) 函數返回

#### Q10.【PE 名詞】
下列關於 PE 結構名詞，何者**錯誤**？
* (A) RVA 是相對於 ImageBase 的偏移，VA = ImageBase + RVA
* (B) IAT（匯入位址表）記錄匯入函數的實際位址
* (C) OEP 是脫殼後要尋找的「原始進入點」
* (D) MZ 是 ELF 檔案的魔術位元組

#### Q11.【檔案簽章】
下列「檔案 — 檔頭位元組」配對，何者**錯誤**？
* (A) Windows PE — `4D 5A`（MZ）
* (B) Linux ELF — `7F 45 4C 46`
* (C) ZIP — `50 4B 03 04`（PK）
* (D) PNG — `FF D8 FF`

#### Q12.【反編譯 .NET】
分析一個 C#／.NET 編寫的惡意程式，最適合的工具為？
* (A) dnSpy（.NET 反編譯與除錯）
* (B) gdb
* (C) steghide
* (D) Wireshark

---

## 📦 Part 2 — 脫殼與反除錯（Q13~Q18）

#### Q13.【UPX 脫殼】
關於 UPX 殼，下列何者正確？
* (A) UPX 是最常見的壓縮殼，多數情況可用 `upx -d` 直接脫殼
* (B) UPX 加殼後無法脫殼
* (C) UPX 是一種反組譯器
* (D) UPX 只能用於 Linux

#### Q14.【ESP 定律】
脫殼時使用「ESP 定律」尋找 OEP 的原理為？
* (A) 殼的解壓 stub 執行完畢後，ESP 會回到初始值，對該 ESP 下硬體斷點即可停在接近 OEP 處
* (B) ESP 永遠指向 OEP
* (C) 把 ESP 設為 0 就能脫殼
* (D) ESP 定律用於破解 RSA

#### Q15.【辨識殼】
欲判斷一個執行檔是否加殼、以及用哪種編譯器/殼，最適合的工具為？
* (A) Detect It Easy（DIE）
* (B) sqlmap
* (C) Volatility
* (D) ROPgadget

#### Q16.【INT 3 反除錯】
反除錯技巧中掃描程式碼裡的 `0xCC` 位元組，目的為？
* (A) 偵測軟體中斷點（software breakpoint 會把目標位元組改成 `0xCC`=INT 3）
* (B) 偵測硬體中斷點
* (C) 加密程式碼
* (D) 清除快取

#### Q17.【IsDebuggerPresent】
`IsDebuggerPresent` API 的運作原理為？
* (A) 讀取 PEB 結構中的 BeingDebugged 旗標判斷目前是否被除錯
* (B) 掃描整個硬碟找除錯器
* (C) 關閉所有除錯器
* (D) 對記憶體加密

#### Q18.【程序注入順序】
典型的「遠端執行緒注入」API 呼叫順序為？
* (A) OpenProcess → VirtualAllocEx → WriteProcessMemory → CreateRemoteThread
* (B) CreateRemoteThread → OpenProcess → VirtualAllocEx → WriteProcessMemory
* (C) WriteProcessMemory → OpenProcess → CreateRemoteThread → VirtualAllocEx
* (D) VirtualAllocEx → CreateRemoteThread → OpenProcess → WriteProcessMemory

---

## 🛡️ Part 3 — Pwn 保護機制（Q19~Q26）

#### Q19.【NX/DEP 與繞過】
NX（DEP）保護「防什麼、怎麼繞」？
* (A) 使棧不可執行（擋在棧上跑 shellcode）；繞過用 ROP（重用現有可執行碼）
* (B) 隨機化位址；繞過靠洩漏位址
* (C) 偵測棧溢位；繞過靠洩漏 canary
* (D) GOT 唯讀；繞過靠格式化字串

#### Q20.【ASLR 與繞過】
ASLR 保護「防什麼、怎麼繞」？
* (A) 隨機化記憶體位址（使位址不可預測）；繞過關鍵是「洩漏一個位址」以推算基底
* (B) 使棧不可執行；繞過用 ROP
* (C) 偵測棧溢位
* (D) 使 GOT 唯讀

#### Q21.【Stack Canary 位置】
Stack Canary（棧金絲雀）放在什麼位置、如何運作？
* (A) 放在「局部緩衝區」與「saved EBP/返回位址」之間；函數返回前檢查，若被改動則呼叫 `__stack_chk_fail` 中止
* (B) 放在堆積開頭
* (C) 放在 GOT 表內
* (D) 放在 IAT 內

#### Q22.【RELRO】
關於 RELRO，下列何者正確？
* (A) Full RELRO 時 GOT 唯讀，封鎖「GOT 覆寫」攻擊；Partial RELRO 則 GOT 仍可寫
* (B) RELRO 用於隨機化位址
* (C) RELRO 使棧不可執行
* (D) RELRO 是一種反組譯器

#### Q23.【checksec 用途】
`checksec` 工具的用途為？
* (A) 檢視執行檔開啟了哪些保護（NX、Canary、PIE、RELRO）
* (B) 自動化 SQL 注入
* (C) 記憶體轉儲分析
* (D) 封包擷取

#### Q24.【ret2libc】
ret2libc 攻擊的核心概念為？
* (A) 將返回位址導向 libc 中的既有函數（如 `system("/bin/sh")`），以繞過 NX
* (B) 在棧上直接執行 shellcode
* (C) 覆寫 canary
* (D) 污染 DNS 快取

#### Q25.【格式化字串】
格式化字串漏洞中，`%n` 的作用為？
* (A) 將「目前已輸出的位元組數」寫入某個指標指向的位址（達成任意寫）
* (B) 洩漏棧上的值
* (C) 讀取指標指向的字串
* (D) 讓程式睡眠

#### Q26.【Heap 漏洞】
下列關於 Heap 漏洞的敘述，何者**錯誤**？
* (A) UAF 是「釋放後仍使用」該記憶體
* (B) Double Free 是重複釋放同一塊記憶體
* (C) tcache 是 glibc 的執行緒快取，可被毒化（tcache poisoning）
* (D) 整數溢位與 NULL pointer dereference 是完全相同的漏洞

---

## 💥 Part 4 — ROP / 工具 / 提權（Q27~Q32）

#### Q27.【ROP gadget】
ROP（Return-Oriented Programming）的「gadget」通常指？
* (A) 以 `ret` 結尾的短碼片段，串接多個即可拼出任意邏輯、繞過 NX
* (B) 一種加密演算法
* (C) 封包分析工具
* (D) 檔案格式

#### Q28.【one_gadget】
`one_gadget` 工具的用途為？
* (A) 在 libc 中尋找「單一跳轉即可 execve("/bin/sh")」的 gadget
* (B) 掃描開放埠
* (C) 反編譯 APK
* (D) 製作磁碟映像

#### Q29.【ret2text】
ret2text 與 ret2libc 的差別為？
* (A) ret2text 跳到「程式自身」已有的碼；ret2libc 跳到「libc」中的函數
* (B) 兩者完全相同
* (C) ret2text 需要 libc 位址
* (D) ret2libc 只在 Windows 有效

#### Q30.【Dirty COW】
Dirty COW（CVE-2016-5195）的成因為？
* (A) Linux 核心 copy-on-write 機制的競態條件，可寫入唯讀檔案達成提權
* (B) 一種 SQL 注入
* (C) DNS 放大攻擊
* (D) 緩衝區溢位

#### Q31.【pyinstxtractor】
`pyinstxtractor` 的用途為？
* (A) 解開 PyInstaller 打包的執行檔，取出 `.pyc` 再反編譯
* (B) 反組譯 ARM 二進位
* (C) 分析記憶體
* (D) 破解 WiFi

#### Q32.【符號執行】
`angr` / `z3` 常被用於 CTF 逆向的哪種情境？
* (A) 以符號執行/約束求解自動找出「能通過驗證」的輸入（如序號、flag）
* (B) 封包重送
* (C) 圖片隱寫
* (D) ARP 欺騙

---

## 🌐 Part 5 — 網路通識（Q33~Q44）

#### Q33.【IPsec AH vs ESP】
IPsec 中 AH 與 ESP 的核心差別為？
* (A) AH 提供完整性與來源認證但**不加密**；ESP 提供加密（可含完整性與認證）
* (B) AH 加密、ESP 不加密
* (C) 兩者完全相同
* (D) AH 用於無線、ESP 用於有線

#### Q34.【IPsec 模式】
IPsec 的 Transport 模式與 Tunnel 模式差別為？
* (A) Transport 只保護 payload（主機對主機）；Tunnel 將整個原始封包封裝加密（閘道對閘道/站對站 VPN）
* (B) Transport 加密整包、Tunnel 只加密標頭
* (C) 兩者相同
* (D) Tunnel 不加密

#### Q35.【VPN 類型】
site-to-site VPN 與 client-to-site VPN 的差別為？
* (A) site-to-site 連接兩個網路（閘道對閘道）；client-to-site 讓個別遠端使用者連進內網
* (B) 兩者完全相同
* (C) site-to-site 只能用於無線
* (D) client-to-site 不需認證

#### Q36.【SNMP 版本】
關於 SNMP，下列何者正確？
* (A) v1/v2c 使用明文 community string；v3 才加入認證與加密
* (B) v1 就有完整加密
* (C) SNMP 使用 TCP 80
* (D) v3 移除了所有安全功能

#### Q37.【SNMP 埠號】
SNMP agent 與 trap 慣用的埠號為？
* (A) UDP 161（agent）、UDP 162（trap）
* (B) TCP 22、TCP 23
* (C) UDP 53、TCP 53
* (D) TCP 161、TCP 162

#### Q38.【ARP 欺騙防禦】
對抗 ARP 欺騙（ARP spoofing）的交換器機制為？
* (A) DAI（Dynamic ARP Inspection）
* (B) NAT
* (C) QoS
* (D) STP

#### Q39.【VLAN hopping】
VLAN hopping 常見的兩種手法為？
* (A) switch spoofing（偽裝成 trunk）與 double tagging（雙層 VLAN 標籤）
* (B) SQL 注入與 XSS
* (C) ARP 與 DNS 快取
* (D) 緩衝區溢位與格式化字串

#### Q40.【TCP 三次握手】
TCP 三次握手的正確順序為？
* (A) SYN → SYN-ACK → ACK
* (B) ACK → SYN → SYN-ACK
* (C) SYN → ACK → SYN
* (D) SYN-ACK → SYN → ACK

#### Q41.【SYN Flood】
SYN Flood 攻擊使伺服器大量連線卡在哪個狀態？常見防禦為？
* (A) 卡在 SYN_RECV（半開連線）佔滿佇列；防禦用 SYN cookies
* (B) 卡在 ESTABLISHED；防禦用 NAT
* (C) 卡在 TIME_WAIT；防禦用 VLAN
* (D) 卡在 CLOSED；無需防禦

#### Q42.【TIME_WAIT】
TCP 連線關閉後，「主動關閉方」進入 TIME_WAIT 狀態的目的為？
* (A) 等待約 2MSL，確保最後的 ACK 送達、舊封包在網路中消散，避免影響新連線
* (B) 立即釋放資源、不等待
* (C) 重新建立連線
* (D) 加密資料

#### Q43.【DNS 放大攻擊】
DNS 放大攻擊（DNS amplification）的核心手法為？
* (A) 偽造來源 IP 為受害者，送出小查詢換取大回應，使大量回應灌向受害者
* (B) 直接對 DNS 伺服器做 SQL 注入
* (C) 竄改 ARP 表
* (D) 暴力破解 DNS 密碼

#### Q44.【DNSSEC 記錄】
下列何者是 DNSSEC 引入的記錄類型？
* (A) RRSIG、DNSKEY、DS、NSEC
* (B) A、AAAA、CNAME、MX
* (C) TXT、SPF、PTR
* (D) SOA、NS 僅此兩者

---

## 🧰 Part 6 — 工具總表辨識（Q45~Q50）

#### Q45.【誘答：挑不同類】
下列工具中，唯一**不是**「反組譯/除錯」用途的是？
* (A) IDA Pro
* (B) Ghidra
* (C) x64dbg
* (D) ffuf

#### Q46.【工具配對錯誤】
下列「工具 — 用途」配對，何者**錯誤**？
* (A) Volatility 3 — 記憶體轉儲分析
* (B) ROPgadget — 尋找 ROP gadget
* (C) gflags — 目錄暴力掃描工具
* (D) pwntools — 撰寫 exploit 的 Python 套件

#### Q47.【Pwn 工具組】
下列哪一組**全部**是 Pwn 常用工具？
* (A) checksec、pwntools、gdb+pwndbg、ROPgadget、one_gadget
* (B) IDA、steghide、Wireshark、nmap
* (C) sqlmap、Burp、ffuf、dirb
* (D) Volatility、FTK Imager、dd、Autopsy

#### Q48.【Cobalt Strike 設定抽取】
`1768.py` 的用途為？
* (A) 從記憶體中抽出 Cobalt Strike 的設定檔（beacon config）
* (B) 反編譯 .NET
* (C) 掃描子網域
* (D) 製作釣魚網站

#### Q49.【process hollowing 偵測】
`Hollow Hunter` 的用途為？
* (A) 偵測 process hollowing（程序掉空）等記憶體注入
* (B) 自動化 XSS
* (C) 破解雜湊
* (D) 封包重放

#### Q50.【x64dbg vs x32dbg】
關於 x64dbg / x32dbg，下列何者正確？
* (A) x64dbg 除錯 64 位元程式、x32dbg 除錯 32 位元程式，位元數要對應
* (B) 兩者可互換、無差別
* (C) 它們是 Linux 除錯器
* (D) 它們是封包分析工具

---
---

## ✅ 答案總表

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | B | B | A | C | A | B | A | A | D |

| Q11 | Q12 | Q13 | Q14 | Q15 | Q16 | Q17 | Q18 | Q19 | Q20 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| D | A | A | A | A | A | A | A | A | A |

| Q21 | Q22 | Q23 | Q24 | Q25 | Q26 | Q27 | Q28 | Q29 | Q30 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | A | A | A | A | D | A | A | A | A |

| Q31 | Q32 | Q33 | Q34 | Q35 | Q36 | Q37 | Q38 | Q39 | Q40 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | A | A | A | A | A | A | A | A | A |

| Q41 | Q42 | Q43 | Q44 | Q45 | Q46 | Q47 | Q48 | Q49 | Q50 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | A | A | A | D | C | A | A | A | A |

> ⚠️ 本卷正解集中在 A（練習用；出題刻意如此以便對照）。**考場正式題答案會打散，務必從理由判斷，不要靠位置。**

---

## 📝 重點詳解（擇關鍵題）

**Q1 A**：`test eax,eax` 做 `eax AND eax`，結果為 0（即 eax=0）時 ZF=1，`je`(=jz) 跳轉。這是判斷「eax 是否為 0/NULL」的慣用寫法。
**Q2 B**：`lea` = Load Effective Address，只算位址不解參照；`mov [..]` 才會去讀記憶體內容。`lea` 也常被編譯器拿來做乘加運算。
**Q3 B**：`cmp` 做減法但只設旗標（ZF/CF/SF/OF）不保存結果，供後面條件跳轉用。
**Q4 A**：`call` = push 返回位址 + jmp；`ret` = pop 返回位址回去。Pwn 蓋掉棧上的返回位址即可劫持 `eip/rip`。
**Q5 C**：整數回傳值在 eax/rax。
**Q6 A** / **Q7 B**：**Linux x64 = RDI,RSI,RDX,RCX,R8,R9**；**Windows x64 = RCX,RDX,R8,R9**。兩者差異必考。
**Q8 A**：cdecl 呼叫方清棧（支援可變參數如 printf）；stdcall 被呼叫方清棧（`ret n`），Win32 API 慣用。
**Q9 A**：IDA 綠=條件成立(taken)、紅=不成立、藍=無條件。
**Q10 D**：MZ 是 **PE/EXE** 的檔頭，不是 ELF（ELF 是 `7F 45 4C 46`）。
**Q11 D**：PNG 是 `89 50 4E 47`；`FF D8 FF` 是 JPG。
**Q13 A** / **Q14 A** / **Q15 A**：UPX 可 `upx -d` 脫；ESP 定律靠 stub 跑完 ESP 復原、對 ESP 下硬體斷點找 OEP；DIE 辨識殼/編譯器。
**Q16 A**：軟體斷點會把目標位元組改成 `0xCC`(INT 3)，掃 `0xCC` 可偵測被下斷點。
**Q17 A**：`IsDebuggerPresent` 讀 PEB 的 BeingDebugged 旗標。
**Q18 A**：OpenProcess → VirtualAllocEx → WriteProcessMemory → CreateRemoteThread（開→配→寫→跑）。
**Q19 A**：NX 擋棧上 shellcode → 繞過用 **ROP**。**別和 ASLR(Q20，繞過靠洩漏位址)搞混**。
**Q20 A**：ASLR 隨機化位址 → 繞過關鍵是洩漏一個位址推基底。
**Q21 A**：Canary 在「緩衝區」與「saved EBP/返回位址」之間；ret 前驗，被改→`__stack_chk_fail`。
**Q22 A**：Full RELRO → GOT 唯讀，擋 GOT 覆寫；Partial → GOT 可寫。
**Q24 A** / **Q29 A**：ret2libc 跳 libc 函數（system）；ret2text 跳程式自身的碼。皆為繞 NX 的手法。
**Q25 A**：`%n` 把「已輸出位元組數」寫入指標所指位址 → 任意寫。`%p/%x`=洩漏、`%s`=讀。
**Q26 D**：整數溢位（數值環繞）與 NULL deref（解參照空指標）是**不同**漏洞；其餘 A/B/C 正確。
**Q27 A** / **Q28 A**：gadget = 以 `ret` 結尾的碼片段；one_gadget 找 libc 中單跳即 execve 的 gadget。
**Q30 A**：Dirty COW = copy-on-write 競態，可寫入唯讀檔提權。
**Q33 A** / **Q34 A**：**AH 不加密(只認證)、ESP 加密**；Transport 保護 payload(主機對主機)、Tunnel 封裝整包(站對站 VPN)。
**Q36 A** / **Q37 A**：SNMP v1/v2c 明文 community、v3 才加認證加密；埠 UDP 161(agent)/162(trap)。
**Q38 A**：DAI 對抗 ARP 欺騙。
**Q40 A** / **Q41 A** / **Q42 A**：握手 SYN→SYN-ACK→ACK；SYN Flood 塞滿 SYN_RECV，防禦 SYN cookies；TIME_WAIT 等 2MSL。
**Q43 A**：DNS 放大 = 偽造來源 IP、小查詢換大回應灌受害者。
**Q44 A**：DNSSEC 記錄 = RRSIG/DNSKEY/DS/NSEC(NSEC3)。
**Q45 D**：ffuf 是 web fuzzing，不是反組譯/除錯。
**Q46 C**：gflags 是 Windows 除錯旗標工具，**不是**目錄掃描（2024 誘答）。
**Q47 A**：checksec/pwntools/gdb+pwndbg/ROPgadget/one_gadget 全為 Pwn 工具組。
**Q48 A** / **Q49 A**：1768.py 抽 Cobalt Strike 設定；Hollow Hunter 偵測 process hollowing（皆 2024 考過）。
**Q50 A**：x64dbg 除 64 位元、x32dbg 除 32 位元，要對應。

---

## 📊 成績對照
| 答對 | 評級 |
|:--|:--|
| 45~50 | 🏆 秒殺級，主責穩 |
| 40~44 | ✅ 合格，錯題精修 |
| 32~39 | ⚠️ 待加強，回速查表 |
| ≤31 | 🔴 鎖定最弱 Part 集中補 |

---

## 🧠 高頻深度考點濃縮（考前掃這段）
1. **x64 傳參**：Linux `RDI RSI RDX RCX R8 R9`／Windows `RCX RDX R8 R9`。
2. **cdecl 呼叫方清棧、stdcall 被呼叫方清棧**；回傳值 eax/rax。
3. **IDA 箭頭**：綠=成立、紅=不成立、藍=無條件。
4. **PE**：RVA/VA/IAT/OEP；**MZ=PE、7F ELF=Linux**。
5. **脫殼**：UPX `-d`、ESP 定律找 OEP、DIE 辨識殼。
6. **反除錯**：IsDebuggerPresent(PEB)、NtGlobalFlag、INT3=`0xCC`。
7. **注入順序**：OpenProcess→VirtualAllocEx→WriteProcessMemory→CreateRemoteThread。
8. **保護機制**：NX↔ROP、ASLR↔洩漏位址、Canary↔`__stack_chk_fail`、Full RELRO↔GOT 唯讀。
9. **格式化字串**：`%p/%x` 洩漏、`%s` 讀、`%n` 寫。
10. **提權**：SUID(`-perm -4000`)、Capabilities(`getcap`)、Dirty COW 競態。
11. **IPsec**：AH 不加密/ESP 加密；Transport(主機)/Tunnel(站對站)。
12. **SNMP**：v3 才加密；UDP 161/162。**TCP**：握手 SYN/SYN-ACK/ACK、SYN Flood→SYN_RECV→SYN cookies、TIME_WAIT 2MSL。
13. **DNS**：放大攻擊(偽造來源+大回應)、DNSSEC(RRSIG/DNSKEY/DS/NSEC)。
14. **工具誘答**：gflags 非掃描、DIE 非 sqlmap、ffuf 非除錯、Hollow Hunter 偵測掉空、1768 抽 CS。
