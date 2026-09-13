# 🎯 雙北極星目標與考綱分析 (targets_and_certifications.md)

> 本文件收錄 **DEVCORE 實習門檻** 與 **全國賽考綱**，作為衡量學習成效的權威指標。

---

## 🏢 一、 DEVCORE 戴夫寇爾實習門檻 (Hard Requirements)

### 1. Red Team 組（第九、十屆必要條件）
- [ ] **PortSwigger Web Security Academy**：理解並做完**所有 Lab**。
- [ ] **OWASP Web Top 10**：熟悉漏洞原理、攻擊 Payload 與修補建議。
- [ ] **網頁獨立開發**：熟悉 PHP / ASP.NET / JSP 任一語言，能獨立建置完整 Web 服務。
- [ ] **Scripting 語言**：熟悉 Shell Script / Python / Ruby，能寫自動化工具。
- [ ] **伺服器建置**：能獨立設定 Nginx, Apache, Tomcat, IIS, Active Directory。
- [ ] **除錯能力**：會使用 Debugger 追蹤程式流程與重現 Bug。

### 2. Research 組（第九屆）
- [ ] **Open Source 分析**：能獨立分析大型開放原始碼專案（C/C++ 或 Java/Python）。
- [ ] **漏洞成因深度理解**：OWASP Top 10, Memory Corruption, Race Condition。
- [ ] **加分項**：pwnable.tw 成績、精通 IDA Pro/Ghidra、獨立挖掘 0-day / 1-day。

### 3. Binary 組（第四屆）
- [ ] **底層彙編**：看懂 x86/x64 組合語言、熟悉 Debugger。
- [ ] **利用技巧**：Stack Overflow, ROP, Use-After-Free, Race Condition。
- [ ] **OS 底層**：理解 Virtual Address / Physical Address 記憶體分頁概念。

---

## 🏆 二、 全國賽考綱與科目要求 (National Cybersecurity Competition)

### 1. Day1 AM：數位鑑識 (Digital Forensics)
- **流量鑑識**：DNS/HTTP 封包分析、SQL Injection 滲透痕跡、RCE 攻擊軌跡還原。
- **系統與記憶體**：
  - Linux/Windows 記憶體 Image 分析 (`target.mem`)，用 Volatility 重建事件時間軸 (Timeline)。
  - 磁碟 Image 分析 (`ext4.img`)、SSH/cron 持久化痕跡搜尋。
- **進階鑑識**：
  - JVM Live Heap Dump (`hprof`) 分析（使用 `jcmd` / VisualVM 提取記憶體中密鑰）。
  - JWT Key 破解與 Token 偽造分析。

### 2. Day1 PM：安全加固 (Security Hardening)
- **Active Directory 加固**：
  - dMSA (Group Managed Service Accounts) 遷移與配置。
  - AD CS ESC1 / ESC15 漏洞防禦、LDAP Signing & Channel Binding。
  - SMB Signing 密碼學簽章強制、Print Spooler 服務關閉與限制。
  - PowerShell Script Block Logging & Constrained Language Mode 啟用。
- **Linux 系統加固**：
  - Suricata IDS/IPS 部署與 TLS 指紋 (JA3/JA4) 偵測配置。
  - rsyslog 透過 TLS 安全轉發日誌至中央監控主機。
  - SSSD + LDAPS 整合 Windows Active Directory 認證。

### 3. Day2 AM：CTF I (Jeopardy 競賽)
- **Web**：Golang 語言特性、WAF Bypass 技巧。
- **Binary**：Netcat 連線 Shellcode Pwn。
- **Reverse**：GBA 遊戲機 ROM 逆向工程（使用 mGBA 模擬器與除錯器）。
- **Profiling**：Java / JVM 效能分析與記憶體洩漏檢測。

### 4. Day2 PM：CTF II (Attack-Defense & AD 內網攻防)
- **DMZ 橫向移動**：從 DMZ Web 主機拿 Shell 後建立 Tunnel/Pivot (如 Chisel/SSH) 深入內網。
- **提權與憑證竊取**：SQL Server 提權至 SYSTEM、DPAPI 憑證提取。
- **AD 票據攻擊**：
  - Kerberoasting 攻擊 SPN 服務帳戶提取 HASH。
  - Golden Ticket 偷取 krbtgt Key 打造萬能票據控制 Domain Admin。
