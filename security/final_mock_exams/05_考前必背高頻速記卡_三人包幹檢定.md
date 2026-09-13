# 考前必背高頻速記卡：三人包幹口測檢定手冊 (Day 30 衝刺專用)

> **使用方法**：  
> 本手冊為考前最後一天（Day 30）三人團隊「面對面互抽口測」專用！  
> 採取**三人分工包幹制**，每位隊員專精其攻防模組。抽考時，一名隊員拿手冊提問，另一名隊員在 **3 秒內**脫口而出正解。若出現卡頓或猶豫，立即標註並加強背誦！

---

## 隊員 A 專屬卡：組長 / 總體架構、資安法規與 IR 事件應變

### 【一、高頻口測快問快答 (15 題)】

1. **問：台灣《資通安全管理法》規定的中央主管機關是誰？**  
   **答**：數位發展部（數發部）。
2. **問：資通安全事件通報期限為何？**  
   **答**：知悉後 **1 小時內**必須完成通報！
3. **問：三級與四級重大資安事件的復原（損害控制）期限是多久？**  
   **答**：知悉後 **36 小時內**（一、二級事件為 72 小時）。
4. **問：台灣《個人資料保護法》第 6 條規定的特種（敏感）個資有哪六類？**  
   **答**：病歷、醫療、基因、性生活、健康檢查、犯罪前科。
5. **問：歐盟 GDPR 第 17 條賦予當事人要求刪除個人資料的權利稱為什麼？**  
   **答**：被遺忘權（Right to be Forgotten / Right to Erasure）。
6. **問：ISO/IEC 27001:2022 附錄 A 將控制措施整合為哪四大主題？**  
   **答**：組織（37項）、人員（8項）、實體（14項）、技術（34項）。
7. **問：NIST CSF 2.0 在原有五大功能之外，全新新增的第六大功能為何？**  
   **答**：治理（Govern, GV）。
8. **問：零信任架構（ZTA）的核心哲學八個字是什麼？**  
   **答**：永不信任，始終驗證（Never Trust, Always Verify）。
9. **問：RFC 3227 證據揮發性順序中，最優先收集的是什麼？**  
   **答**：CPU 暫存器（Registers）與實體記憶體（RAM）。
10. **問：Windows 安全日誌中，Event ID 4624 代表什麼？**  
    **答**：帳戶成功登入。
11. **問：Event ID 4624 中 Logon Type 10 代表什麼登入方式？**  
    **答**：遠端桌面連線（RDP / RemoteInteractive）。Logon Type 3 代表網路連線（SMB）。
12. **問：Windows 新增系統服務時會產生哪一個關鍵 Event ID？**  
    **答**：Event ID 7045。
13. **問：在 NTFS 檔案系統中，用來識破 Timestomping 時間偽造的關鍵比對屬性是什麼？**  
    **答**：比對 `$STANDARD_INFORMATION` 與 `$FILE_NAME` 的時間戳差異（後者由核心維護，攻擊者常漏改）。
14. **問：NIST SP 800-61 事件應變生命週期包含哪幾大階段？**  
    **答**：準備 -> 偵測與分析 -> 圍堵、根除與復原 -> 事後活動。
15. **問：在 Volatility 3 中，查看所有處理序及其父處理序 PID 的插件是什麼？**  
    **答**：`windows.pslist`（搜尋斷鏈隱藏行程用 `windows.psscan`）。

### 【二、隊員 A 必背核心指令清單】
- **查看網路連線進程**：`vol -f mem.dmp windows.netscan`
- **轉儲記憶體中的 SAM 密碼雜湊**：`vol -f mem.dmp windows.hashdump`
- **匯出指定進程記憶體**：`vol -f mem.dmp windows.memmap --pid <PID> --dump`
- **Linux 查看目前登入與失敗記錄**：`last` 與 `lastb`
- **Linux 即時追蹤認證日誌**：`tail -f /var/log/auth.log` (Debian/Ubuntu) 或 `/var/log/secure` (CentOS/RHEL)

---

## 隊員 B 專屬卡：Web 應用安全、密碼學應用與 CTF 攻防

### 【一、高頻口測快問快答 (15 題)】

1. **問：SQL UNION 注入成立的兩個必要語法條件為何？**  
   **答**：前後 SELECT 查詢的欄位數量必須相同，且對應欄位資料型態相容。
2. **問：MySQL 時間盲注最常用的條件延遲函數組合是什麼？**  
   **答**：`IF(condition, sleep(5), 0)`。
3. **問：寬字節注入是利用什麼編碼特性吃掉反斜線 `\`？**  
   **答**：GBK 雙字節編碼，輸入 `%df` 與反斜線 `0x5C` 組合成漢字「運」（`0xDF5C`），釋放單引號 `'`。
4. **問：Cookie 的 SameSite 屬性設為 Lax 時，什麼時候會帶 Cookie？**  
   **答**：僅在「安全且為頂層導覽」的跨站 GET 請求（如點擊 `<a>` 連結）時會攜帶；POST 或 iframe 不會攜帶。
5. **問：SSRF 攻擊中，用來向 Redis 寫入 WebShell 最強大的協議是什麼？**  
   **答**：`gopher://` 協議（支援多行 RESP 指令傳輸）。
6. **問：SSRF 防禦中，攻擊者利用 DNS 極短 TTL 繞過 IP 黑名單的技術叫什麼？**  
   **答**：DNS Rebinding（DNS 重綁定）。
7. **問：PHP 反序列化時，物件被銷毀或腳本結束時自動觸發的魔術方法是什麼？**  
   **答**：`__destruct()`。
8. **問：Python pickle 反序列化攻擊的核心利用方法是什麼？**  
   **答**：自訂類別中的 `__reduce__()` 方法。
9. **問：JWT 的「None 演算法攻擊」原理是什麼？**  
   **答**：將 Header 中 `"alg"` 改為 `"none"`，且將簽章（Signature）完全留空。
10. **問：AES 哪種分組加密模式不具備語意安全、易洩漏明文圖形輪廓？**  
    **答**：ECB 模式（Electronic Codebook）。
11. **問：TLS 1.3 強制採用的現代加密類型是什麼？**  
    **答**：AEAD 認證加密（如 AES-GCM、ChaCha20-Poly1305）。
12. **問：RSA 歐拉函數 $\phi(n)$ 在已知兩質數 $p, q$ 時怎麼算？**  
    **答**：$\phi(n) = (p - 1)(q - 1)$。
13. **問：RSA 共模攻擊（Common Modulus Attack）的先決條件是什麼？**  
    **答**：同一個明文 $m$、相同的模數 $n$、兩個互質的公鑰指數 $e_1, e_2$（$\gcd(e_1, e_2) = 1$）。
14. **問：Kerberos 網域滲透中，「黃金票據」（Golden Ticket）是偽造什麼票據？必須偷到誰的金鑰？**  
    **答**：偽造 TGT 票據；必須獲取 `krbtgt` 帳號的 NTLM Hash 或 AES 金鑰。
15. **問：TOTP（如 Google Authenticator）計算 6 位動態密碼依賴哪兩項輸入？**  
    **答**：共享私密金鑰（Secret）與當前 Unix 時間戳（以 30 秒為步長）。

### 【二、隊員 B 必背核心語法清單】
- **SQLi 查當前庫的所有表**：`' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema=database()--+`
- **SQLi 查指定表的所有欄位**：`' UNION SELECT 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='users'--+`
- **XSS 屬性自動觸發最短 Payload**：`" onfocus="alert(1)" autofocus="`
- **Flask Jinja2 SSTI 探測**：`{{7*7}}` 或 `{{config}}`
- **Jinja2 RCE 標準調用鏈**：`{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}`

---

## 隊員 C 專屬卡：系統加固、二進位逆向與網路封包鑑識

### 【一、高頻口測快問快答 (15 題)】

1. **問：Linux 檔案具有 SUID 權限時，使用者執行時會以誰的權限運行？**  
   **答**：以該檔案**擁有者（Owner，通常是 root）**的權限運行。
2. **問：Linux 搜尋系統中所有 SUID 檔案的命令是什麼？**  
   **答**：`find / -perm -4000 -type f 2>/dev/null`。
3. **問：Linux `/etc/shadow` 中密碼欄位以 `$6$` 開頭代表什麼雜湊算法？**  
   **答**：SHA-512。
4. **問：Linux 檔案只允許追加（append-only）、禁止刪除和覆寫的命令是什麼？**  
   **答**：`chattr +a <檔名>`。
5. **問：SELinux 切換為僅警告不阻擋的寬容模式命令是什麼？**  
   **答**：`setenforce 0`。
6. **問：Windows 防禦 Mimikatz 提取記憶體憑證的虛擬化隔離技術叫什麼？**  
   **答**：Windows Defender Credential Guard（基於 VBS / VSM）。
7. **問：Active Directory GPO 群組原則的覆蓋優先順序（LSDOU）為何？**  
   **答**：Local -> Site -> Domain -> OU（後者覆蓋前者，OU 優先權最高）。
8. **問：DEP / NX（資料執行防止）的核心硬體機制是什麼？**  
   **答**：頁表 NX 位元，將堆疊與堆積分頁標記為「不可執行」（W^X）。
9. **問：在 DEP/NX 開啟的情況下，攻擊者控制執行流的主要技術是什麼？**  
   **答**：ROP（返回導向編程，Return-Oriented Programming）。
10. **問：x86/x64 中除錯器軟體中斷點（INT 3）的單字節機器碼是什麼？**  
    **答**：`0xCC`。
11. **問：Windows 惡意程式檢測自身是否被除錯的最經典 API 是什麼？**  
    **答**：`IsDebuggerPresent()`（檢查 PEB 偏移 0x02 的 BeingDebugged 標誌）。
12. **問：PE 執行檔開頭前兩個位元組的魔術數字（ASCII）是什麼？**  
    **答**：`MZ`（十六進位 `4D 5A`）。
13. **問：Wireshark 過濾所有 DNS 查詢請求（非回應）的表達式是什麼？**  
    **答**：`dns.flags.response == 0`。
14. **問：DNS 隱寫外洩時，子域名資料僅包含 A-Z 與 2-7 代表什麼編碼？**  
    **答**：Base32 編碼。
15. **問：TCP 三次握手第二步伺服器回應的確認號（Ack）與客戶端序號 $x$ 的關係為何？**  
    **答**：$Ack = x + 1$。

### 【二、隊員 C 必背核心指令清單】
- **Wireshark 過濾指定 IP 與 HTTP POST**：`ip.addr == 192.168.1.100 and http.request.method == "POST"`
- **Wireshark 檢索封包內包含特定字串**：`tcp contains "flag{"`
- **Linux 升級為完整互動式 TTY Shell**：`python3 -c 'import pty; pty.spawn("/bin/bash")'`
- **iptables 封鎖惡意 IP 連線 22 端口**：`iptables -A INPUT -p tcp -s <Bad_IP> --dport 22 -j DROP`
- **Windows PowerShell 徹底停用 SMBv1**：`Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol`

---

## 考前 30 分鐘救命覆盤清單 (三人同看)

- [ ] **通報時限牢記**：資安事件 **1 小時內通報**，三/四級事件 **36 小時內完成復原**！
- [ ] **常規端口反射**：21(FTP), 22(SSH), 23(Telnet), 25(SMTP), 53(DNS), 88(Kerberos), 389(LDAP), 445(SMB), 1433(MSSQL), 1521(Oracle), 3306(MySQL), 3389(RDP), 5985/5986(WinRM), 6379(Redis)。
- [ ] **Event ID 核心四碼**：4624(成功登入), 4625(登入失敗), 4720(新增使用者), 7045(安裝新服務)。
- [ ] **Logon Type 重點兩碼**：Type 3(網路連線/SMB/共用), Type 10(遠端桌面/RDP)。
- [ ] **封包隱寫解碼必備**：子域名 Base32 解碼 -> 拼出 CSV -> 留意 `name` 首字垂直拼寫 Flag！
- [ ] **穩住心態**：先做確定拿分的客觀題與日誌推演題，封包題先過濾關鍵協議，遇到卡題 10 分鐘立即換下一題！

