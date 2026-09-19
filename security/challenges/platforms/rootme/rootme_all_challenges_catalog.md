# 🚩 Root-Me 官方全量挑戰題庫目錄 (Root-Me Live Challenge Catalog)

> 本目錄直接連線 [Root-Me 官方 REST API](https://api.www.root-me.org/) 動態同步生成，**零寫死資料**，實時追蹤官方全部 11 大安全領域官方題庫。
> 涵蓋 Web 伺服端、Web 客戶端、密碼分析、數位鑑識、網路安全、系統漏洞利用、腳本分析、逆向破解、擬真滲透、演算法設計與隱寫術等全領域關卡。

**同步題數統計**: 共動態收錄 `608` 道官方全量實戰關卡（🟢 全部 100% 免費開放）。

---

## 📊 一、 分類與題數分佈概覽

| 領域分類 (Category) | 官方收錄題數 | 代表關卡 Slug | 官方傳送門 |
| :--- | :--- | :--- | :--- |
| **App - Script** | 33 | `sudo-weak-configuration, Bash-cron, Bash-System-1`... | [瀏覽分類](https://www.root-me.org/en/Challenges/App-Script/) |
| **App - System** | 93 | `ELF-x86-Hardened-binary-1, ELF-x86-Remote-Format-String-bug, ELF-x86-Remote-BSS-buffer-overflow`... | [瀏覽分類](https://www.root-me.org/en/Challenges/App-System/) |
| **Cracking** | 70 | `ELF-x86-0-protection, ELF-x86-Basic, ELF-x86-Ptrace`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Cracking/) |
| **Cryptanalysis** | 75 | `Encoding-UU, Hash-Message-Digest-5, Known-plaintext-XOR`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Cryptanalysis/) |
| **Forensic** | 48 | `Command-and-Control-level-2, Command-and-Control-level-3, Command-and-Control-level-4`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Forensic/) |
| **Network** | 35 | `Global-System-Traffic-for-Mobile-communication, FTP-authentication, TELNET-authentication`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Network/) |
| **Programming** | 29 | `Mathematic-progression, Quick-Response-Code, CAPTCHA-me-if-you-can`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Programming/) |
| **Realist** | 62 | `Neonazi-inside, PyRat-Auction, It-happens-sometimes`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Realist/) |
| **Steganography** | 24 | `WAV-Noise-analysis, Steganomobile, WAV-Spectral-analysis`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Steganography/) |
| **Web - Client** | 42 | `Javascript-Source, Javascript-Obfuscation-1, Javascript-Obfuscation-2`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Web-Client/) |
| **Web - Server** | 97 | `HTML-Source-code, HTTP-User-agent, Weak-password`... | [瀏覽分類](https://www.root-me.org/en/Challenges/Web-Server/) |

---

## 📚 二、 各領域官方題目詳細清單

### 📌 App - Script（33 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 8 | **sudo - weak configuration** | `sudo-weak-configuration` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/sudo-weak-configuration) |
| 12 | **Bash - cron** | `Bash-cron` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-cron) |
| 193 | **Bash - System 1** | `Bash-System-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-System-1) |
| 205 | **Bash - System 2** | `Bash-System-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-System-2) |
| 260 | **Python - pickle** | `Python-pickle` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-pickle) |
| 404 | **Python - input()** | `Python-input` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-input) |
| 451 | **Python - PyJail 1** | `Python-PyJail-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-PyJail-1) |
| 634 | **Python - PyJail 2** | `Python-PyJail-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-PyJail-2) |
| 639 | **Python - Jail - Exec** | `Python-Jail-Exec` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-Jail-Exec) |
| 931 | **Perl - Command injection** | `Perl-Command-injection` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Perl-Command-injection) |
| 1383 | **Javascript - Jail** | `Javascript-Jail` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Javascript-Jail) |
| 1420 | **Bash - Restricted shells** | `Bash-Restricted-shells` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-Restricted-shells) |
| 1626 | **Python - Jail - Garbage collector** | `Python-Jail-Garbage-collector` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-Jail-Garbage-collector) |
| 1896 | **SSH - Agent Hijacking** | `SSH-Agent-Hijacking` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/SSH-Agent-Hijacking) |
| 1988 | **PHP - Jail** | `PHP-Jail` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/PHP-Jail) |
| 2216 | **Shared Objects hijacking** | `Shared-Objects-hijacking` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Shared-Objects-hijacking) |
| 2275 | **Bash - race condition** | `Bash-race-condition` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-race-condition) |
| 2296 | **Powershell - Command Injection** | `Powershell-Command-Injection` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Powershell-Command-Injection) |
| 2297 | **Powershell - SecureString** | `Powershell-SecureString` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Powershell-SecureString) |
| 2298 | **Powershell - Basic jail** | `Powershell-Basic-jail` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Powershell-Basic-jail) |
| 2365 | **Bash - quoted expression injection** | `Bash-quoted-expression-injection` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-quoted-expression-injection) |
| 2367 | **Bash - unquoted expression injection** | `Bash-unquoted-expression-injection` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Bash-unquoted-expression-injection) |
| 2845 | **LaTeX - Input** | `LaTeX-Input` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/LaTeX-Input) |
| 2846 | **LaTeX - Command execution** | `LaTeX-Command-execution` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/LaTeX-Command-execution) |
| 2868 | **Python - format string** | `Python-format-string` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-format-string) |
| 2951 | **R: Code Execution** | `R-Code-Execution` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/R-Code-Execution) |
| 3681 | **Docker - I am groot** | `Docker-I-am-groot` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Docker-I-am-groot) |
| 3682 | **Docker - Sys-Admin’s Docker** | `Docker-Sys-Admin-s-Docker` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Docker-Sys-Admin-s-Docker) |
| 3683 | **Docker - Talk through me** | `Docker-Talk-through-me` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Docker-Talk-through-me) |
| 4227 | **AppArmor - Jail Introduction** | `AppArmor-Jail-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/AppArmor-Jail-Introduction) |
| 4418 | **Python - Eval Is Evil** | `Python-Eval-Is-Evil` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Python-Eval-Is-Evil) |
| 4419 | **AppArmor - Jail Medium** | `AppArmor-Jail-Medium` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/AppArmor-Jail-Medium) |
| 4740 | **Deep learning - Malicious model** | `Deep-learning-Malicious-model` | [前往挑戰](https://www.root-me.org/en/Challenges/App-Script/Deep-learning-Malicious-model) |

### 📌 App - System（93 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 191 | **ELF x86 - Hardened binary 1** | `ELF-x86-Hardened-binary-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-1) |
| 201 | **ELF x86 - Remote Format String bug** | `ELF-x86-Remote-Format-String-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Remote-Format-String-bug) |
| 203 | **ELF x86 - Remote BSS buffer overflow** | `ELF-x86-Remote-BSS-buffer-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Remote-BSS-buffer-overflow) |
| 211 | **ELF x86 - Format string bug basic 1** | `ELF-x86-Format-string-bug-basic-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Format-string-bug-basic-1) |
| 215 | **ELF x86 - BSS buffer overflow** | `ELF-x86-BSS-buffer-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-BSS-buffer-overflow) |
| 217 | **ELF x86 - Stack buffer overflow basic 4** | `ELF-x86-Stack-buffer-overflow-basic-4` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-4) |
| 221 | **ELF x86 - Stack buffer overflow basic 5** | `ELF-x86-Stack-buffer-overflow-basic-5` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-5) |
| 223 | **ELF x86 - Stack buffer and integer overflow** | `ELF-x86-Stack-buffer-and-integer-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-and-integer-overflow) |
| 225 | **ELF x86 - Race condition** | `ELF-x86-Race-condition` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Race-condition) |
| 227 | **ELF x86 - Hardened binary 2** | `ELF-x86-Hardened-binary-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-2) |
| 229 | **ELF x86 - Hardened binary 3** | `ELF-x86-Hardened-binary-3` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-3) |
| 231 | **ELF x86 - Hardened binary 4** | `ELF-x86-Hardened-binary-4` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-4) |
| 233 | **ELF x86 - Hardened binary 5** | `ELF-x86-Hardened-binary-5` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-5) |
| 235 | **ELF x86 - Hardened binary 6** | `ELF-x86-Hardened-binary-6` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-6) |
| 276 | **ELF x86 - Hardened binary 7** | `ELF-x86-Hardened-binary-7` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Hardened-binary-7) |
| 832 | **ELF x86 - Stack buffer overflow basic 1** | `ELF-x86-Stack-buffer-overflow-basic-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-1) |
| 843 | **ELF x86 - Format string bug basic 2** | `ELF-x86-Format-string-bug-basic-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Format-string-bug-basic-2) |
| 845 | **ELF x86 - Stack buffer overflow basic 2** | `ELF-x86-Stack-buffer-overflow-basic-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-2) |
| 848 | **ELF x86 - Stack buffer overflow basic 3** | `ELF-x86-Stack-buffer-overflow-basic-3` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-3) |
| 850 | **ELF x86 - Format String Bug Basic 3** | `ELF-x86-Format-String-Bug-Basic-3` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Format-String-Bug-Basic-3) |
| 865 | **ELF x86 - Information leakage with Stack Smashing Protector** | `ELF-x86-Information-leakage-with-Stack-Smashing-Protector` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Information-leakage-with-Stack-Smashing-Protector) |
| 871 | **ELF x64 - Stack buffer overflow - advanced** | `ELF-x64-Stack-buffer-overflow-advanced` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-advanced) |
| 875 | **ELF x64 - Stack buffer overflow - basic** | `ELF-x64-Stack-buffer-overflow-basic` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-basic) |
| 885 | **ELF x86 - Blind remote format string bug** | `ELF-x86-Blind-remote-format-string-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Blind-remote-format-string-bug) |
| 887 | **ELF x64 - Remote Heap buffer overflow 1** | `ELF-x64-Remote-Heap-buffer-overflow-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Remote-Heap-buffer-overflow-1) |
| 889 | **ELF x64 - Sigreturn Oriented Programming** | `ELF-x64-Sigreturn-Oriented-Programming` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Sigreturn-Oriented-Programming) |
| 912 | **ELF x64 - Remote Heap buffer overflow 2** | `ELF-x64-Remote-Heap-buffer-overflow-2` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Remote-Heap-buffer-overflow-2) |
| 921 | **ELF x86 - Stack buffer overflow - C++ vtables** | `ELF-x86-Stack-buffer-overflow-C-vtables` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-C-vtables) |
| 1018 | **LinKern x86 - Buffer overflow basic 1** | `LinKern-x86-Buffer-overflow-basic-1` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x86-Buffer-overflow-basic-1) |
| 1023 | **LinKern x86 - Null pointer dereference** | `LinKern-x86-Null-pointer-dereference` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x86-Null-pointer-dereference) |
| 1024 | **LinKern x64 - Race condition** | `LinKern-x64-Race-condition` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x64-Race-condition) |
| 1031 | **LinKern x64 - reentrant code** | `LinKern-x64-reentrant-code` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x64-reentrant-code) |
| 1045 | **ELF x86 - Stack buffer overflow basic 6** | `ELF-x86-Stack-buffer-overflow-basic-6` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-6) |
| 1061 | **LinKern x86 - basic ROP** | `LinKern-x86-basic-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x86-basic-ROP) |
| 1064 | **ELF x64 - Off-by-one bug** | `ELF-x64-Off-by-one-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Off-by-one-bug) |
| 1067 | **LinKern x64 - Memory exploration** | `LinKern-x64-Memory-exploration` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x64-Memory-exploration) |
| 1320 | **ELF x86 - Remote stack buffer overflow - Hardened** | `ELF-x86-Remote-stack-buffer-overflow-Hardened` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Remote-stack-buffer-overflow-Hardened) |
| 1349 | **ELF x86 - Blind ROP** | `ELF-x86-Blind-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Blind-ROP) |
| 1435 | **ELF x64 - Remote heap buffer overflow - tcache** | `ELF-x64-Remote-heap-buffer-overflow-tcache` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Remote-heap-buffer-overflow-tcache) |
| 1448 | **ELF ARM - Stack buffer overflow - basic** | `ELF-ARM-Stack-buffer-overflow-basic` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Stack-buffer-overflow-basic) |
| 1455 | **ELF ARM - Basic ROP** | `ELF-ARM-Basic-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Basic-ROP) |
| 1463 | **ELF ARM - Use After Free** | `ELF-ARM-Use-After-Free` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Use-After-Free) |
| 1464 | **ELF ARM - Heap Off-by-One** | `ELF-ARM-Heap-Off-by-One` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Heap-Off-by-One) |
| 1467 | **ELF ARM - Format String bug** | `ELF-ARM-Format-String-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Format-String-bug) |
| 1470 | **ELF ARM - Alphanumeric shellcode** | `ELF-ARM-Alphanumeric-shellcode` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Alphanumeric-shellcode) |
| 1474 | **ELF ARM - Heap buffer overflow - Wilderness** | `ELF-ARM-Heap-buffer-overflow-Wilderness` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Heap-buffer-overflow-Wilderness) |
| 1477 | **LinKern ARM - vulnerable syscall** | `LinKern-ARM-vulnerable-syscall` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-ARM-vulnerable-syscall) |
| 1486 | **LinKern ARM - Stack Overflow** | `LinKern-ARM-Stack-Overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-ARM-Stack-Overflow) |
| 1492 | **ELF ARM - Stack Spraying** | `ELF-ARM-Stack-Spraying` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Stack-Spraying) |
| 1493 | **ELF ARM - Heap Overflow** | `ELF-ARM-Heap-Overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Heap-Overflow) |
| 1528 | **ELF ARM - Race condition** | `ELF-ARM-Race-condition` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Race-condition) |
| 1529 | **ELF x64 - Seccomp Whitelist** | `ELF-x64-Seccomp-Whitelist` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Seccomp-Whitelist) |
| 1530 | **ELF ARM - Heap format string bug** | `ELF-ARM-Heap-format-string-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM-Heap-format-string-bug) |
| 1566 | **ELF x64 - Logic bug** | `ELF-x64-Logic-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Logic-bug) |
| 1587 | **ELF x64 - Heap feng-shui** | `ELF-x64-Heap-feng-shui` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Heap-feng-shui) |
| 1656 | **ELF x86 - Out of bounds attack - French Paradox** | `ELF-x86-Out-of-bounds-attack-French-Paradox` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Out-of-bounds-attack-French-Paradox) |
| 1738 | **ELF x86 - Bug Hunting - Several issues** | `ELF-x86-Bug-Hunting-Several-issues` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Bug-Hunting-Several-issues) |
| 1769 | **ELF x64 - Blind ROP** | `ELF-x64-Blind-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Blind-ROP) |
| 1899 | **ELF MIPS - Stack buffer overflow - No NX** | `ELF-MIPS-Stack-buffer-overflow-No-NX` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-MIPS-Stack-buffer-overflow-No-NX) |
| 1900 | **ELF MIPS - Basic ROP** | `ELF-MIPS-Basic-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-MIPS-Basic-ROP) |
| 1905 | **ELF MIPS - URLEncoded Format String bug** | `ELF-MIPS-URLEncoded-Format-String-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-MIPS-URLEncoded-Format-String-bug) |
| 1915 | **ELF MIPS - Format String Glitch** | `ELF-MIPS-Format-String-Glitch` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-MIPS-Format-String-Glitch) |
| 1921 | **LinKern MIPSel - Vulnerable ioctl** | `LinKern-MIPSel-Vulnerable-ioctl` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-MIPSel-Vulnerable-ioctl) |
| 1927 | **ELF x64 - Browser exploit - Intro** | `ELF-x64-Browser-exploit-Intro` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Browser-exploit-Intro) |
| 1948 | **ELF x64 - Browser exploit - BitString** | `ELF-x64-Browser-exploit-BitString` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Browser-exploit-BitString) |
| 1985 | **ELF x86 - Stack buffer overflow - ret2dl_resolve** | `ELF-x86-Stack-buffer-overflow-ret2dl-resolve` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-ret2dl-resolve) |
| 1992 | **ELF x86 - Use After Free - basic** | `ELF-x86-Use-After-Free-basic` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Use-After-Free-basic) |
| 2001 | **LinKern x64 - RowHammer** | `LinKern-x64-RowHammer` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x64-RowHammer) |
| 2019 | **LinKern x64 - SLUB off-by-one** | `LinKern-x64-SLUB-off-by-one` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/LinKern-x64-SLUB-off-by-one) |
| 2160 | **PE32 - Stack buffer overflow basic** | `PE32-Stack-buffer-overflow-basic` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/PE32-Stack-buffer-overflow-basic) |
| 2161 | **PE32 - Advanced stack buffer overflow** | `PE32-Advanced-stack-buffer-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/PE32-Advanced-stack-buffer-overflow) |
| 2162 | **PE32+ Format string bug** | `PE32-Format-string-bug` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/PE32-Format-string-bug) |
| 2163 | **PE32+ Basic ROP** | `PE32-Basic-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/PE32-Basic-ROP) |
| 2185 | **WinKern x64 - Advanced stack buffer overflow - ROP** | `WinKern-x64-Advanced-stack-buffer-overflow-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/WinKern-x64-Advanced-stack-buffer-overflow-ROP) |
| 2187 | **WinKern x64 - Use After Free** | `WinKern-x64-Use-After-Free` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/WinKern-x64-Use-After-Free) |
| 2861 | **ELF x64 - Double free** | `ELF-x64-Double-free` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Double-free) |
| 2865 | **ELF x64 - Blind SROP** | `ELF-x64-Blind-SROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Blind-SROP) |
| 2874 | **ELF x64 - Stack buffer overflow - PIE** | `ELF-x64-Stack-buffer-overflow-PIE` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-PIE) |
| 2892 | **ELF x64 - Advanced Heap Exploitation - Heap Leakless & Fortified** | `ELF-x64-Advanced-Heap-Exploitation-Heap-Leakless-and-Fortified` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Advanced-Heap-Exploitation-Heap-Leakless-and-Fortified) |
| 2904 | **ELF x64 - FILE structure hijacking** | `ELF-x64-FILE-structure-hijacking` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-FILE-structure-hijacking) |
| 2905 | **ELF x64 - ret2dl_init** | `ELF-x64-ret2dl-init` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-ret2dl-init) |
| 2906 | **ELF x64 - File Structure Hacking** | `ELF-x64-File-Structure-Hacking` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-File-Structure-Hacking) |
| 2907 | **ELF x64 - Heap Filling** | `ELF-x64-Heap-Filling` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Heap-Filling) |
| 2982 | **ELF x64 - Heap Safe-Linking Bypass** | `ELF-x64-Heap-Safe-Linking-Bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Heap-Safe-Linking-Bypass) |
| 3814 | **ELF x64 - Buggy VM** | `ELF-x64-Buggy-VM` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Buggy-VM) |
| 4088 | **ELF ARM64 - Heap Underflow** | `ELF-ARM64-Heap-Underflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM64-Heap-Underflow) |
| 4089 | **ELF ARM64 - Multithreading** | `ELF-ARM64-Multithreading` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-ARM64-Multithreading) |
| 4118 | **ELF x64 - Basic heap overflow** | `ELF-x64-Basic-heap-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Basic-heap-overflow) |
| 4128 | **ELF RISC-V - Intro - let’s do the ROP** | `ELF-RISC-V-Intro-let-s-do-the-ROP` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-RISC-V-Intro-let-s-do-the-ROP) |
| 4714 | **ELF x64 - Stack buffer overflow - Stack pivot** | `ELF-x64-Stack-buffer-overflow-Stack-pivot` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-Stack-pivot) |
| 4715 | **ELF x64 - Syscall chaining** | `ELF-x64-Syscall-chaining` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Syscall-chaining) |
| 4716 | **ELF x64 - Heap Hop** | `ELF-x64-Heap-Hop` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Heap-Hop) |
| 4717 | **ELF x64 - Advanced blind format string exploitation** | `ELF-x64-Advanced-blind-format-string-exploitation` | [前往挑戰](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Advanced-blind-format-string-exploitation) |

### 📌 Cracking（70 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 42 | **ELF x86 - 0 protection** | `ELF-x86-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-0-protection) |
| 44 | **ELF x86 - Basic** | `ELF-x86-Basic` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Basic) |
| 69 | **ELF x86 - Ptrace** | `ELF-x86-Ptrace` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Ptrace) |
| 73 | **ELF x86 - Fake Instructions** | `ELF-x86-Fake-Instructions` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Fake-Instructions) |
| 75 | **ELF x86 - Random Crackme** | `ELF-x86-Random-Crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Random-Crackme) |
| 79 | **ELF x86 - ExploitMe** | `ELF-x86-ExploitMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-ExploitMe) |
| 113 | **APK - Root My Droid** | `APK-Root-My-Droid` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/APK-Root-My-Droid) |
| 119 | **ELF x86 - CrackPass** | `ELF-x86-CrackPass` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-CrackPass) |
| 123 | **ELF ARM - crackme 1337** | `ELF-ARM-crackme-1337` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-ARM-crackme-1337) |
| 157 | **ELF x86 - KeygenMe** | `ELF-x86-KeygenMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-KeygenMe) |
| 159 | **PE x86 - AutoPE** | `PE-x86-AutoPE` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x86-AutoPE) |
| 175 | **ELF x86 - Packed** | `ELF-x86-Packed` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Packed) |
| 237 | **PDF - Javascript** | `PDF-Javascript` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PDF-Javascript) |
| 243 | **APK - Insomni’Droid** | `APK-Insomni-Droid` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/APK-Insomni-Droid) |
| 253 | **ELF x86 - Anti-debug** | `ELF-x86-Anti-debug` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Anti-debug) |
| 258 | **ELF ARM - Crypted** | `ELF-ARM-Crypted` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-ARM-Crypted) |
| 272 | **PE x86 - 0 protection** | `PE-x86-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x86-0-protection) |
| 279 | **APK - Anti-debug** | `APK-Anti-debug` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/APK-Anti-debug) |
| 323 | **PE x86 - SEHVEH** | `PE-x86-SEHVEH` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x86-SEHVEH) |
| 352 | **ELF x86 - VM** | `ELF-x86-VM` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-VM) |
| 358 | **PYC - ByteCode** | `PYC-ByteCode` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PYC-ByteCode) |
| 376 | **ELF x86 - No software breakpoints** | `ELF-x86-No-software-breakpoints` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-No-software-breakpoints) |
| 385 | **PE x86 - RunPE** | `PE-x86-RunPE` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x86-RunPE) |
| 422 | **PE DotNet - 0 protection** | `PE-DotNet-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-0-protection) |
| 1303 | **ELF x64 - Anti-debug and equations** | `ELF-x64-Anti-debug-and-equations` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Anti-debug-and-equations) |
| 1304 | **ELF ARM - Basic Crackme** | `ELF-ARM-Basic-Crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-ARM-Basic-Crackme) |
| 1305 | **ELF C++ - 0 protection** | `ELF-C-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-C-0-protection) |
| 1358 | **MachO x64 - keygenme or not** | `MachO-x64-keygenme-or-not` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/MachO-x64-keygenme-or-not) |
| 1762 | **ELF x64 - Nanomites - Introduction** | `ELF-x64-Nanomites-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Nanomites-Introduction) |
| 1763 | **ELF x64 - Nanomites** | `ELF-x64-Nanomites` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Nanomites) |
| 1811 | **ELF MIPS - Basic Crackme** | `ELF-MIPS-Basic-Crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-MIPS-Basic-Crackme) |
| 1831 | **ELF x64 - Crackme automating** | `ELF-x64-Crackme-automating` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Crackme-automating) |
| 1867 | **GB - Basic GameBoy crackme** | `GB-Basic-GameBoy-crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/GB-Basic-GameBoy-crackme) |
| 1932 | **ELF x64 - Golang basic** | `ELF-x64-Golang-basic` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Golang-basic) |
| 2059 | **PE x86 - Xor Madness** | `PE-x86-Xor-Madness` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x86-Xor-Madness) |
| 2060 | **White-Box Cryptography #2** | `White-Box-Cryptography-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/White-Box-Cryptography-2) |
| 2108 | **Ringgit** | `Ringgit` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Ringgit) |
| 2293 | **ELF x64 - Basic KeygenMe** | `ELF-x64-Basic-KeygenMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Basic-KeygenMe) |
| 2294 | **ELF x64 - KeyGenMe** | `ELF-x64-KeyGenMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-KeyGenMe) |
| 2295 | **ELF x64 - Hidden Control Flow** | `ELF-x64-Hidden-Control-Flow` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Hidden-Control-Flow) |
| 2862 | **PE DotNet - Basic Anti-Debug** | `PE-DotNet-Basic-Anti-Debug` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-Basic-Anti-Debug) |
| 2866 | **WASM - Find the NPC** | `WASM-Find-the-NPC` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/WASM-Find-the-NPC) |
| 2867 | **WASM - Introduction** | `WASM-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/WASM-Introduction) |
| 2869 | **Bash - VM** | `Bash-VM` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Bash-VM) |
| 2870 | **Powershell DeObfuscation** | `Powershell-DeObfuscation` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Powershell-DeObfuscation) |
| 2871 | **Lua - Bytecode** | `Lua-Bytecode` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Lua-Bytecode) |
| 2880 | **PE DotNet - KeygenMe** | `PE-DotNet-KeygenMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-KeygenMe) |
| 2881 | **PE DotNet - Basic Crackme** | `PE-DotNet-Basic-Crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-Basic-Crackme) |
| 3647 | **APK - Flutter Debug** | `APK-Flutter-Debug` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/APK-Flutter-Debug) |
| 3707 | **Godot - 0 protection** | `Godot-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Godot-0-protection) |
| 3708 | **Godot - Bytecode** | `Godot-Bytecode` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Godot-Bytecode) |
| 3709 | **Godot - Mono** | `Godot-Mono` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Godot-Mono) |
| 3710 | **Godot - 3D model** | `Godot-3D-model` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Godot-3D-model) |
| 3861 | **ELF x64 - Rust Crackme** | `ELF-x64-Rust-Crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Rust-Crackme) |
| 3877 | **Unity - IL2CPP - Basic Game Hacking** | `Unity-IL2CPP-Basic-Game-Hacking` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Unity-IL2CPP-Basic-Game-Hacking) |
| 3881 | **PYC - Snakeygen** | `PYC-Snakeygen` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PYC-Snakeygen) |
| 3887 | **Unity - Mono - Basic Game Hacking** | `Unity-Mono-Basic-Game-Hacking` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Unity-Mono-Basic-Game-Hacking) |
| 3893 | **APK - Introduction** | `APK-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/APK-Introduction) |
| 3923 | **EVM - Bytecode** | `EVM-Bytecode` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/EVM-Bytecode) |
| 3924 | **ELF x64 - Rust backdoor** | `ELF-x64-Rust-backdoor` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/ELF-x64-Rust-backdoor) |
| 3925 | **NRO ARM - Switch homebrew** | `NRO-ARM-Switch-homebrew` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/NRO-ARM-Switch-homebrew) |
| 4018 | **Voracious Nanomites** | `Voracious-Nanomites` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Voracious-Nanomites) |
| 4205 | **PE x64 - UEFI Secure Boot** | `PE-x64-UEFI-Secure-Boot` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x64-UEFI-Secure-Boot) |
| 4206 | **HackerMan** | `HackerMan` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/HackerMan) |
| 4285 | **Unity3D Save handling** | `Unity3D-Save-handling` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Unity3D-Save-handling) |
| 4469 | **PYC - Self Modifying (Byte)Code** | `PYC-Self-Modifying-Byte-Code` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PYC-Self-Modifying-Byte-Code) |
| 4470 | **PE x64 - Tables in shambles** | `PE-x64-Tables-in-shambles` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-x64-Tables-in-shambles) |
| 4863 | **Basic ? crackme** | `Basic-crackme` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/Basic-crackme) |
| 4864 | **PE DotNet - Memory Protect** | `PE-DotNet-Memory-Protect` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-Memory-Protect) |
| 4866 | **PE32+ - KeygenMe** | `PE32-KeygenMe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cracking/PE32-KeygenMe) |

### 📌 Cryptanalysis（75 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 16 | **Encoding - UU** | `Encoding-UU` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Encoding-UU) |
| 71 | **Hash - Message Digest 5** | `Hash-Message-Digest-5` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-Message-Digest-5) |
| 77 | **Known plaintext - XOR** | `Known-plaintext-XOR` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Known-plaintext-XOR) |
| 86 | **Pixel Madness** | `Pixel-Madness` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Pixel-Madness) |
| 95 | **File - PKZIP** | `File-PKZIP` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/File-PKZIP) |
| 111 | **RSA - Factorisation** | `RSA-Factorisation` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Factorisation) |
| 131 | **Shift cipher** | `Shift-cipher` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Shift-cipher) |
| 141 | **Encoding - ASCII** | `Encoding-ASCII` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Encoding-ASCII) |
| 167 | **Polyalphabetic substitution - Vigenère** | `Polyalphabetic-substitution-Vigen-re` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Polyalphabetic-substitution-Vigen-re) |
| 179 | **Monoalphabetic substitution - Caesar** | `Monoalphabetic-substitution-Caesar` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Monoalphabetic-substitution-Caesar) |
| 181 | **Monoalphabetic substitution - Polybe** | `Monoalphabetic-substitution-Polybe` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Monoalphabetic-substitution-Polybe) |
| 199 | **File - Insecure storage 1** | `File-Insecure-storage-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/File-Insecure-storage-1) |
| 209 | **ELF64 - PID encryption** | `ELF64-PID-encryption` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/ELF64-PID-encryption) |
| 239 | **Hash - SHA-2** | `Hash-SHA-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-SHA-2) |
| 268 | **Service - CBC Padding** | `Service-CBC-Padding` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Service-CBC-Padding) |
| 270 | **Service - Timing attack** | `Service-Timing-attack` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Service-Timing-attack) |
| 281 | **Code - Pseudo Random Number Generator** | `Code-Pseudo-Random-Number-Generator` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Code-Pseudo-Random-Number-Generator) |
| 287 | **System - Android lock pattern** | `System-Android-lock-pattern` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/System-Android-lock-pattern) |
| 350 | **Polyalphabetic substitution - One Time Pad** | `Polyalphabetic-substitution-One-Time-Pad` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Polyalphabetic-substitution-One-Time-Pad) |
| 402 | **Transposition - Rail Fence** | `Transposition-Rail-Fence` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Transposition-Rail-Fence) |
| 406 | **Discrete logarithm problem** | `Discrete-logarithm-problem` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Discrete-logarithm-problem) |
| 933 | **Service - Hash length extension attack** | `Service-Hash-length-extension-attack` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Service-Hash-length-extension-attack) |
| 939 | **Initialisation Vector** | `Initialisation-Vector` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Initialisation-Vector) |
| 942 | **AES128 - CTR** | `AES128-CTR` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES128-CTR) |
| 946 | **RSA - Continued fractions** | `RSA-Continued-fractions` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Continued-fractions) |
| 971 | **AES - ECB** | `AES-ECB` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-ECB) |
| 973 | **RSA - Multiple recipients** | `RSA-Multiple-recipients` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Multiple-recipients) |
| 1332 | **GEDEFU** | `GEDEFU` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/GEDEFU) |
| 1344 | **RSA - Padding** | `RSA-Padding` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Padding) |
| 1354 | **Enigma Machine** | `Enigma-Machine` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Enigma-Machine) |
| 1369 | **ECDHE** | `ECDHE` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/ECDHE) |
| 1386 | **Hash - SHA-3** | `Hash-SHA-3` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-SHA-3) |
| 1399 | **RSA - Common modulus** | `RSA-Common-modulus` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Common-modulus) |
| 1515 | **RSA - Decipher Oracle** | `RSA-Decipher-Oracle` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Decipher-Oracle) |
| 1692 | **LFSR - Known plaintext** | `LFSR-Known-plaintext` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/LFSR-Known-plaintext) |
| 1711 | **RSA - Corrupted key 1** | `RSA-Corrupted-key-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Corrupted-key-1) |
| 1729 | **RSA - Corrupted key 2** | `RSA-Corrupted-key-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Corrupted-key-2) |
| 1798 | **AES - CBC - Bit-Flipping Attack** | `AES-CBC-Bit-Flipping-Attack` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-CBC-Bit-Flipping-Attack) |
| 1843 | **AES - Weaker variant** | `AES-Weaker-variant` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-Weaker-variant) |
| 1860 | **AES - 4 Rounds** | `AES-4-Rounds` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-4-Rounds) |
| 1885 | **AES - Fault attack #1** | `AES-Fault-attack-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-Fault-attack-1) |
| 1887 | **AES - Fault attack #2** | `AES-Fault-attack-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-Fault-attack-2) |
| 1916 | **White-Box Cryptography** | `White-Box-Cryptography` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/White-Box-Cryptography) |
| 2033 | **AES-PMAC** | `AES-PMAC` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-PMAC) |
| 2084 | **RSA - Corrupted key 3** | `RSA-Corrupted-key-3` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Corrupted-key-3) |
| 2090 | **ECDSA - Introduction** | `ECDSA-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/ECDSA-Introduction) |
| 2101 | **ECDSA - Implementation error** | `ECDSA-Implementation-error` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/ECDSA-Implementation-error) |
| 2127 | **RSA - Lee cooper** | `RSA-Lee-cooper` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Lee-cooper) |
| 2219 | **RSA - Signature** | `RSA-Signature` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Signature) |
| 2317 | **PHP - mt_rand** | `PHP-mt-rand` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/PHP-mt-rand) |
| 2334 | **Twisted secret** | `Twisted-secret` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Twisted-secret) |
| 2858 | **OTP - Implementation error** | `OTP-Implementation-error` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/OTP-Implementation-error) |
| 2931 | **Hash - NT** | `Hash-NT` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-NT) |
| 2933 | **Hash - LM** | `Hash-LM` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-LM) |
| 2935 | **Hash - DCC** | `Hash-DCC` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-DCC) |
| 2937 | **Hash - DCC2** | `Hash-DCC2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-DCC2) |
| 2943 | **CISCO - Salted Password** | `CISCO-Salted-Password` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/CISCO-Salted-Password) |
| 3711 | **FEAL - Differential Cryptanalysis** | `FEAL-Differential-Cryptanalysis` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/FEAL-Differential-Cryptanalysis) |
| 3712 | **Side Channel - AES : CPA** | `Side-Channel-AES-CPA` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Side-Channel-AES-CPA) |
| 3713 | **Side Channel - AES : first round** | `Side-Channel-AES-first-round` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Side-Channel-AES-first-round) |
| 3890 | **Circular Bit Shift** | `Circular-Bit-Shift` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Circular-Bit-Shift) |
| 3967 | **Encoding - Codebook** | `Encoding-Codebook` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Encoding-Codebook) |
| 4153 | **Hill Cipher** | `Hill-Cipher` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Hill-Cipher) |
| 4184 | **RSA - H-rabin** | `RSA-H-rabin` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-H-rabin) |
| 4552 | **AES - ECB - Copy Paste** | `AES-ECB-Copy-Paste` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/AES-ECB-Copy-Paste) |
| 4553 | **Shamir Secret Sharing - Introduction** | `Shamir-Secret-Sharing-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Shamir-Secret-Sharing-Introduction) |
| 4554 | **Shamir Secret Sharing - Traitor** | `Shamir-Secret-Sharing-Traitor` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Shamir-Secret-Sharing-Traitor) |
| 4555 | **Shamir Secret Sharing - Reduction** | `Shamir-Secret-Sharing-Reduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Shamir-Secret-Sharing-Reduction) |
| 4556 | **Shamir Secret Sharing - Irreducible ?** | `Shamir-Secret-Sharing-Irreducible` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Shamir-Secret-Sharing-Irreducible) |
| 4663 | **File - PKZIP 2** | `File-PKZIP-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/File-PKZIP-2) |
| 4832 | **DSA - Implementation error** | `DSA-Implementation-error` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/DSA-Implementation-error) |
| 4833 | **ElGamal - Fault attack (Introduction)** | `ElGamal-Fault-attack-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/ElGamal-Fault-attack-Introduction) |
| 4834 | **Goldreich Goldwasser Halevi | Weak Parameter** | `Goldreich-Goldwasser-Halevi-Weak-Parameter` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/Goldreich-Goldwasser-Halevi-Weak-Parameter) |
| 4835 | **NTRU | Weak Parameter** | `NTRU-Weak-Parameter` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/NTRU-Weak-Parameter) |
| 4836 | **NTRU | Multiple Transmission** | `NTRU-Multiple-Transmission` | [前往挑戰](https://www.root-me.org/en/Challenges/Cryptanalysis/NTRU-Multiple-Transmission) |

### 📌 Forensic（48 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 313 | **Command & Control - level 2** | `Command-and-Control-level-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-2) |
| 314 | **Command & Control - level 3** | `Command-and-Control-level-3` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-3) |
| 315 | **Command & Control - level 4** | `Command-and-Control-level-4` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-4) |
| 316 | **Command & Control - level 5** | `Command-and-Control-level-5` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-5) |
| 317 | **Command & Control - level 6** | `Command-and-Control-level-6` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-6) |
| 365 | **Find the cat** | `Find-the-cat` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Find-the-cat) |
| 877 | **Ransomware Android** | `Ransomware-Android` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Ransomware-Android) |
| 894 | **Active Directory - GPO** | `Active-Directory-GPO` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Active-Directory-GPO) |
| 917 | **Logs analysis - web attack** | `Logs-analysis-web-attack` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Logs-analysis-web-attack) |
| 938 | **Zeus Bot** | `Zeus-Bot` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Zeus-Bot) |
| 1326 | **Job interview** | `Job-interview` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Job-interview) |
| 1329 | **Second job interview** | `Second-job-interview` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Second-job-interview) |
| 1357 | **Find me** | `Find-me` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Find-me) |
| 1507 | **Ugly Duckling** | `Ugly-Duckling` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Ugly-Duckling) |
| 1521 | **Find me again** | `Find-me-again` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Find-me-again) |
| 1531 | **Malicious Word macro** | `Malicious-Word-macro` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Malicious-Word-macro) |
| 1649 | **DNS exfiltration** | `DNS-exfiltration` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/DNS-exfiltration) |
| 1664 | **Try again** | `Try-again` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Try-again) |
| 1804 | **Multi-devices** | `Multi-devices` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Multi-devices) |
| 1861 | **Homemade keylogger** | `Homemade-keylogger` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Homemade-keylogger) |
| 1941 | **Rootkit - Cold case** | `Rootkit-Cold-case` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Rootkit-Cold-case) |
| 2028 | **Find me back** | `Find-me-back` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Find-me-back) |
| 2056 | **macOS - Keychain** | `macOS-Keychain` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/macOS-Keychain) |
| 3648 | **The Lost Case - Mobile Investigation** | `The-Lost-Case-Mobile-Investigation` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/The-Lost-Case-Mobile-Investigation) |
| 3649 | **iOS - Introduction** | `iOS-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/iOS-Introduction) |
| 3650 | **Find me on Android** | `Find-me-on-Android` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Find-me-on-Android) |
| 3799 | **Docker layers** | `Docker-layers` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Docker-layers) |
| 3879 | **The Artist** | `The-Artist` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/The-Artist) |
| 3933 | **Oh My Grub** | `Oh-My-Grub` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Oh-My-Grub) |
| 3948 | **Open My Vault** | `Open-My-Vault` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Open-My-Vault) |
| 3978 | **Windows - LDAP User ASRepRoastable** | `Windows-LDAP-User-ASRepRoastable` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Windows-LDAP-User-ASRepRoastable) |
| 3979 | **Windows - LDAP User KerbeRoastable** | `Windows-LDAP-User-KerbeRoastable` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Windows-LDAP-User-KerbeRoastable) |
| 3980 | **Windows - NTDS Secret extraction** | `Windows-NTDS-Secret-extraction` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Windows-NTDS-Secret-extraction) |
| 4014 | **Supply chain attack - Python** | `Supply-chain-attack-Python` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Supply-chain-attack-Python) |
| 4015 | **Supply chain attack - Docker** | `Supply-chain-attack-Docker` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Supply-chain-attack-Docker) |
| 4115 | **Web3 - Put on your mask - Step 1** | `Web3-Put-on-your-mask-Step-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Web3-Put-on-your-mask-Step-1) |
| 4116 | **Web3 - Put on your mask - Step 2** | `Web3-Put-on-your-mask-Step-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Web3-Put-on-your-mask-Step-2) |
| 4258 | **Deleted file** | `Deleted-file` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Deleted-file) |
| 4287 | **Air-gap exfiltration** | `Air-gap-exfiltration` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Air-gap-exfiltration) |
| 4288 | **Try again 2** | `Try-again-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Try-again-2) |
| 4289 | **Capture this** | `Capture-this` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Capture-this) |
| 4307 | **C2 Mythic** | `C2-Mythic` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/C2-Mythic) |
| 4802 | **Remote Support** | `Remote-Support` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Remote-Support) |
| 4803 | **MasterKee** | `MasterKee` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/MasterKee) |
| 4964 | **ICMP exfiltration** | `ICMP-exfiltration` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/ICMP-exfiltration) |
| 4975 | **Invocation** | `Invocation` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Invocation) |
| 4976 | **Trusted** | `Trusted` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Trusted) |
| 4977 | **Heist of the century** | `Heist-of-the-century` | [前往挑戰](https://www.root-me.org/en/Challenges/Forensic/Heist-of-the-century) |

### 📌 Network（35 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 61 | **Global System Traffic for Mobile communication** | `Global-System-Traffic-for-Mobile-communication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Global-System-Traffic-for-Mobile-communication) |
| 97 | **FTP - authentication** | `FTP-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/FTP-authentication) |
| 99 | **TELNET - authentication** | `TELNET-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/TELNET-authentication) |
| 101 | **Twitter authentication** | `Twitter-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Twitter-authentication) |
| 103 | **SIP - authentication** | `SIP-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/SIP-authentication) |
| 105 | **SSL - HTTP exchange** | `SSL-HTTP-exchange` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/SSL-HTTP-exchange) |
| 107 | **ICMP payload** | `ICMP-payload` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/ICMP-payload) |
| 109 | **IP - Time To Live** | `IP-Time-To-Live` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/IP-Time-To-Live) |
| 197 | **XMPP - authentication** | `XMPP-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/XMPP-authentication) |
| 274 | **Wired Equivalent Privacy** | `Wired-Equivalent-Privacy` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Wired-Equivalent-Privacy) |
| 338 | **ETHERNET - frame** | `ETHERNET-frame` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/ETHERNET-frame) |
| 340 | **DNS - zone transfert** | `DNS-zone-transfert` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/DNS-zone-transfert) |
| 346 | **LDAP - null bind** | `LDAP-null-bind` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/LDAP-null-bind) |
| 348 | **ETHERNET - Patched transmission** | `ETHERNET-Patched-transmission` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/ETHERNET-Patched-transmission) |
| 361 | **CISCO - password** | `CISCO-password` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/CISCO-password) |
| 424 | **SNMP - Authentification** | `SNMP-Authentification` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/SNMP-Authentification) |
| 449 | **Netfilter - common mistakes** | `Netfilter-common-mistakes` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Netfilter-common-mistakes) |
| 1991 | **Bluetooth - Unknown file** | `Bluetooth-Unknown-file` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Bluetooth-Unknown-file) |
| 2348 | **HTTP - DNS Rebinding** | `HTTP-DNS-Rebinding` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/HTTP-DNS-Rebinding) |
| 2362 | **RIPv1 - no authentication** | `RIPv1-no-authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RIPv1-no-authentication) |
| 2375 | **POP - APOP** | `POP-APOP` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/POP-APOP) |
| 2810 | **RF - Key Fixed Code** | `RF-Key-Fixed-Code` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RF-Key-Fixed-Code) |
| 2812 | **RF - AM Transmission** | `RF-AM-Transmission` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RF-AM-Transmission) |
| 2813 | **RF - FM Transmission** | `RF-FM-Transmission` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RF-FM-Transmission) |
| 2814 | **RF - Satellite transmission** | `RF-Satellite-transmission` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RF-Satellite-transmission) |
| 3702 | **RF - L Band** | `RF-L-Band` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/RF-L-Band) |
| 4259 | **OSPF - Authentication** | `OSPF-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/OSPF-Authentication) |
| 4260 | **ARP Spoofing - Active listening** | `ARP-Spoofing-Active-listening` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-Active-listening) |
| 4261 | **ARP Spoofing - The man in the middle** | `ARP-Spoofing-The-man-in-the-middle` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-The-man-in-the-middle) |
| 4594 | **Analog video** | `Analog-video` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Analog-video) |
| 4664 | **NTLM - Authentication** | `NTLM-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/NTLM-Authentication) |
| 4665 | **Kerberos - Authentication** | `Kerberos-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Kerberos-Authentication) |
| 4666 | **Data extraction** | `Data-extraction` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/Data-extraction) |
| 4667 | **WPA2 - Enterprise** | `WPA2-Enterprise` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/WPA2-Enterprise) |
| 4668 | **WPA3 - SAE** | `WPA3-SAE` | [前往挑戰](https://www.root-me.org/en/Challenges/Network/WPA3-SAE) |

### 📌 Programming（29 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 18 | **Mathematic progression** | `Mathematic-progression` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Mathematic-progression) |
| 241 | **Quick Response Code** | `Quick-Response-Code` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Quick-Response-Code) |
| 251 | **CAPTCHA me if you can** | `CAPTCHA-me-if-you-can` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/CAPTCHA-me-if-you-can) |
| 947 | **ELF x64 - Sandbox shellcoding** | `ELF-x64-Sandbox-shellcoding` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/ELF-x64-Sandbox-shellcoding) |
| 1954 | **ELF x64 - Shellcoding - Sheep warmup** | `ELF-x64-Shellcoding-Sheep-warmup` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/ELF-x64-Shellcoding-Sheep-warmup) |
| 1975 | **ELF x86 - Shellcoding - Alphanumeric** | `ELF-x86-Shellcoding-Alphanumeric` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/ELF-x86-Shellcoding-Alphanumeric) |
| 1976 | **ELF x64 - Shellcoding - Polymorphism** | `ELF-x64-Shellcoding-Polymorphism` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/ELF-x64-Shellcoding-Polymorphism) |
| 2139 | **Ethereum - Tutoreum** | `Ethereum-Tutoreum` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-Tutoreum) |
| 2140 | **Ethereum - Takeover** | `Ethereum-Takeover` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-Takeover) |
| 2141 | **Ethereum - NotSoPriv8** | `Ethereum-NotSoPriv8` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-NotSoPriv8) |
| 2142 | **Ethereum - BadStack** | `Ethereum-BadStack` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-BadStack) |
| 2182 | **WinKern x64 - shellcoding : token stealing** | `WinKern-x64-shellcoding-token-stealing` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/WinKern-x64-shellcoding-token-stealing) |
| 2253 | **ARM - Shellcoding - Egg hunter** | `ARM-Shellcoding-Egg-hunter` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/ARM-Shellcoding-Egg-hunter) |
| 2961 | **Various encodings** | `Various-encodings` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Various-encodings) |
| 3885 | **Second degree polynomial solver** | `Second-degree-polynomial-solver` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Second-degree-polynomial-solver) |
| 3906 | **Ethereum - Reentrancy** | `Ethereum-Reentrancy` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-Reentrancy) |
| 3907 | **Apprentice Scraper** | `Apprentice-Scraper` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Apprentice-Scraper) |
| 4296 | **TCP - Back to school** | `TCP-Back-to-school` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/TCP-Back-to-school) |
| 4297 | **TCP - Encoded string** | `TCP-Encoded-string` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/TCP-Encoded-string) |
| 4298 | **TCP - The Roman wheel** | `TCP-The-Roman-wheel` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/TCP-The-Roman-wheel) |
| 4299 | **TCP - Uncompress Me** | `TCP-Uncompress-Me` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/TCP-Uncompress-Me) |
| 4458 | **Ethereum - King of the EVM** | `Ethereum-King-of-the-EVM` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-King-of-the-EVM) |
| 4595 | **Ethereum - tx.origin** | `Ethereum-tx-origin` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-tx-origin) |
| 4596 | **Ethereum - Bunker** | `Ethereum-Bunker` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-Bunker) |
| 4597 | **Ethereum - Architect** | `Ethereum-Architect` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Ethereum-Architect) |
| 4737 | **Deep Learning - Introduction** | `Deep-Learning-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Deep-Learning-Introduction) |
| 4738 | **Deep Learning - Captcha** | `Deep-Learning-Captcha` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Deep-Learning-Captcha) |
| 4739 | **Adversarial Attack - GAN** | `Adversarial-Attack-GAN` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Adversarial-Attack-GAN) |
| 4741 | **Adversarial Attack - Prison Break** | `Adversarial-Attack-Prison-Break` | [前往挑戰](https://www.root-me.org/en/Challenges/Programming/Adversarial-Attack-Prison-Break) |

### 📌 Realist（62 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 52 | **Neonazi inside** | `Neonazi-inside` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Neonazi-inside) |
| 83 | **PyRat Auction** | `PyRat-Auction` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/PyRat-Auction) |
| 93 | **It happens, sometimes** | `It-happens-sometimes` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/It-happens-sometimes) |
| 135 | **Root-We** | `Root-We` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Root-We) |
| 177 | **Root them** | `Root-them` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Root-them) |
| 185 | **P0wn3d** | `P0wn3d` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/P0wn3d) |
| 187 | **The h@ckers l4b** | `The-h-ckers-l4b` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/The-h-ckers-l4b) |
| 189 | **MALab** | `MALab` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/MALab) |
| 195 | **Web TV** | `Web-TV` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Web-TV) |
| 305 | **IPBX - call me maybe** | `IPBX-call-me-maybe` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/IPBX-call-me-maybe) |
| 339 | **Red Pills** | `Red-Pills` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Red-Pills) |
| 373 | **Marabout** | `Marabout` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Marabout) |
| 431 | **Crypto Secure** | `Crypto-Secure` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Crypto-Secure) |
| 436 | **Ultra Upload** | `Ultra-Upload` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Ultra-Upload) |
| 447 | **SamBox v1** | `SamBox-v1` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SamBox-v1) |
| 645 | **SamBox v2** | `SamBox-v2` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SamBox-v2) |
| 891 | **SamCMS** | `SamCMS` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SamCMS) |
| 956 | **Bluebox - Pentest** | `Bluebox-Pentest` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bluebox-Pentest) |
| 1334 | **SAP Pentest 007** | `SAP-Pentest-007` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SAP-Pentest-007) |
| 1338 | **SAP Pentest 000** | `SAP-Pentest-000` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SAP-Pentest-000) |
| 1523 | **Bluebox 2 - Pentest** | `Bluebox-2-Pentest` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bluebox-2-Pentest) |
| 1539 | **SamBox v3** | `SamBox-v3` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SamBox-v3) |
| 1554 | **Imagick** | `Imagick` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Imagick) |
| 1642 | **Starbug Bounty** | `Starbug-Bounty` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Starbug-Bounty) |
| 1681 | **Bash/Awk - netstat parsing** | `Bash-Awk-netstat-parsing` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bash-Awk-netstat-parsing) |
| 1689 | **ARM FTP Box** | `ARM-FTP-Box` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/ARM-FTP-Box) |
| 1775 | **Highway to shell** | `Highway-to-shell` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Highway-to-shell) |
| 1785 | **Bozobe Hospital** | `Bozobe-Hospital` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bozobe-Hospital) |
| 2014 | **SamBox v4** | `SamBox-v4` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SamBox-v4) |
| 2023 | **Django unchained** | `Django-unchained` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Django-unchained) |
| 2047 | **BBQ Factory - First Flirt** | `BBQ-Factory-First-Flirt` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/BBQ-Factory-First-Flirt) |
| 2049 | **BBQ Factory - Back To The Grill** | `BBQ-Factory-Back-To-The-Grill` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/BBQ-Factory-Back-To-The-Grill) |
| 2211 | **In Your Kubernetass** | `In-Your-Kubernetass` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/In-Your-Kubernetass) |
| 2224 | **Bash - System Disaster** | `Bash-System-Disaster` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bash-System-Disaster) |
| 2262 | **Well-known** | `Well-known` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Well-known) |
| 2377 | **A bittersweet shellfony** | `A-bittersweet-shellfony` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/A-bittersweet-shellfony) |
| 2817 | **Texode** | `Texode` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Texode) |
| 2822 | **SSHocker** | `SSHocker` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/SSHocker) |
| 2823 | **Breaking Root-Me like it’s 2020** | `Breaking-Root-Me-like-it-s-2020` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Breaking-Root-Me-like-it-s-2020) |
| 2859 | **reQUACKier** | `reQUACKier` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/reQUACKier) |
| 2889 | **Texode Back** | `Texode-Back` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Texode-Back) |
| 2895 | **Nodeful** | `Nodeful` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Nodeful) |
| 2967 | **Getting root Over it!** | `Getting-root-Over-it` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Getting-root-Over-it) |
| 3004 | **DjangocatZ** | `DjangocatZ` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/DjangocatZ) |
| 3720 | **Root Me, for real** | `Root-Me-for-real` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Root-Me-for-real) |
| 3883 | **DasBox1: Rififi in the lizardmen** | `DasBox1-Rififi-in-the-lizardmen` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/DasBox1-Rififi-in-the-lizardmen) |
| 3897 | **Windows - KerbeRoast** | `Windows-KerbeRoast` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-KerbeRoast) |
| 3898 | **Windows - ASRepRoast** | `Windows-ASRepRoast` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-ASRepRoast) |
| 3899 | **Windows - Group Policy Preferences Passwords** | `Windows-Group-Policy-Preferences-Passwords` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-Group-Policy-Preferences-Passwords) |
| 3900 | **Windows - ZeroLogon** | `Windows-ZeroLogon` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-ZeroLogon) |
| 3932 | **Matrix terminal** | `Matrix-terminal` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Matrix-terminal) |
| 4013 | **I’m a Bl4ck H4t** | `I-m-a-Bl4ck-H4t` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/I-m-a-Bl4ck-H4t) |
| 4070 | **Windows - krbtgt history** | `Windows-krbtgt-history` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-krbtgt-history) |
| 4071 | **Windows - sAMAccountName spoofing** | `Windows-sAMAccountName-spoofing` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Windows-sAMAccountName-spoofing) |
| 4120 | **Bohemian RhapC2** | `Bohemian-RhapC2` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Bohemian-RhapC2) |
| 4122 | **C for C-cure** | `C-for-C-cure` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/C-for-C-cure) |
| 4278 | **End Droid** | `End-Droid` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/End-Droid) |
| 4468 | **VPN Provider** | `VPN-Provider` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/VPN-Provider) |
| 4472 | **Android - Shady VPN** | `Android-Shady-VPN` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Android-Shady-VPN) |
| 4599 | **Mersenne with 2** | `Mersenne-with-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Mersenne-with-2) |
| 4600 | **Extractor** | `Extractor` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/Extractor) |
| 4824 | **ComCyber - Challenge** | `ComCyber-Challenge` | [前往挑戰](https://www.root-me.org/en/Challenges/Realist/ComCyber-Challenge) |

### 📌 Steganography（24 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 40 | **WAV - Noise analysis** | `WAV-Noise-analysis` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/WAV-Noise-analysis) |
| 145 | **Steganomobile** | `Steganomobile` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Steganomobile) |
| 171 | **WAV - Spectral analysis** | `WAV-Spectral-analysis` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/WAV-Spectral-analysis) |
| 183 | **Crypt-art** | `Crypt-art` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Crypt-art) |
| 249 | **PNG - Least Significant Bit** | `PNG-Least-Significant-Bit` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/PNG-Least-Significant-Bit) |
| 355 | **Dot and next line** | `Dot-and-next-line` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Dot-and-next-line) |
| 445 | **TXT - George and Alfred** | `TXT-George-and-Alfred` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/TXT-George-and-Alfred) |
| 927 | **EXIF - Thumbnail** | `EXIF-Thumbnail` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/EXIF-Thumbnail) |
| 1397 | **Twitter Secret Messages** | `Twitter-Secret-Messages` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Twitter-Secret-Messages) |
| 1584 | **PDF - Embedded** | `PDF-Embedded` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/PDF-Embedded) |
| 1611 | **PNG - Pixel Indicator Technique** | `PNG-Pixel-Indicator-Technique` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/PNG-Pixel-Indicator-Technique) |
| 1621 | **PNG - Pixel Value Differencing** | `PNG-Pixel-Value-Differencing` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/PNG-Pixel-Value-Differencing) |
| 1657 | **Angecryption** | `Angecryption` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Angecryption) |
| 1759 | **Base Jumper** | `Base-Jumper` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Base-Jumper) |
| 1805 | **Kitty spy** | `Kitty-spy` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Kitty-spy) |
| 2091 | **Hide and seek** | `Hide-and-seek` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Hide-and-seek) |
| 2092 | **Yellow dots** | `Yellow-dots` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Yellow-dots) |
| 2318 | **Poem from Space** | `Poem-from-Space` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Poem-from-Space) |
| 3178 | **APNG - Just A PNG** | `APNG-Just-A-PNG` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/APNG-Just-A-PNG) |
| 3179 | **Mimic - Dummy sight** | `Mimic-Dummy-sight` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Mimic-Dummy-sight) |
| 3180 | **ELF x64 - Duality** | `ELF-x64-Duality` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/ELF-x64-Duality) |
| 3719 | **EXIF - Metadata** | `EXIF-Metadata` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/EXIF-Metadata) |
| 4185 | **Genius ID** | `Genius-ID` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/Genius-ID) |
| 4646 | **PNG - EMD** | `PNG-EMD` | [前往挑戰](https://www.root-me.org/en/Challenges/Steganography/PNG-EMD) |

### 📌 Web - Client（42 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 22 | **Javascript - Source** | `Javascript-Source` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Source) |
| 28 | **Javascript - Obfuscation 1** | `Javascript-Obfuscation-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-1) |
| 54 | **Javascript - Obfuscation 2** | `Javascript-Obfuscation-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-2) |
| 65 | **Javascript - Authentication** | `Javascript-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Authentication) |
| 91 | **Javascript - Authentication 2** | `Javascript-Authentication-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Authentication-2) |
| 117 | **Javascript - Obfuscation 3** | `Javascript-Obfuscation-3` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-3) |
| 121 | **Javascript - Obfuscation 5** | `Javascript-Obfuscation-5` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-5) |
| 143 | **Javascript - Native code** | `Javascript-Native-code` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Native-code) |
| 155 | **Javascript - Obfuscation 4** | `Javascript-Obfuscation-4` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-4) |
| 245 | **XSS - Stored 1** | `XSS-Stored-1` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-1) |
| 247 | **XSS - Stored 2** | `XSS-Stored-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-2) |
| 255 | **Flash - Authentication** | `Flash-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Flash-Authentication) |
| 381 | **HTTP Response Splitting** | `HTTP-Response-Splitting` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/HTTP-Response-Splitting) |
| 998 | **XSS - Stored - filter bypass** | `XSS-Stored-filter-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-filter-bypass) |
| 1020 | **CSRF - 0 protection** | `CSRF-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSRF-0-protection) |
| 1022 | **CSRF - token bypass** | `CSRF-token-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSRF-token-bypass) |
| 1398 | **XSS - DOM Based** | `XSS-DOM-Based` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based) |
| 1569 | **HTML - disabled buttons** | `HTML-disabled-buttons` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/HTML-disabled-buttons) |
| 1758 | **XSS - Reflected** | `XSS-Reflected` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-Reflected) |
| 2327 | **Javascript - Webpack** | `Javascript-Webpack` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Webpack) |
| 2351 | **CSP Bypass - Inline code** | `CSP-Bypass-Inline-code` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-Inline-code) |
| 2352 | **CSP Bypass - JSONP** | `CSP-Bypass-JSONP` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-JSONP) |
| 2353 | **CSP Bypass - Dangling markup** | `CSP-Bypass-Dangling-markup` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-Dangling-markup) |
| 2354 | **CSP Bypass - Dangling markup 2** | `CSP-Bypass-Dangling-markup-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-Dangling-markup-2) |
| 2948 | **XSS DOM Based - Introduction** | `XSS-DOM-Based-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based-Introduction) |
| 2949 | **XSS DOM Based - Eval** | `XSS-DOM-Based-Eval` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based-Eval) |
| 2950 | **XSS DOM Based - Filters Bypass** | `XSS-DOM-Based-Filters-Bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based-Filters-Bypass) |
| 2953 | **XSS DOM Based - AngularJS** | `XSS-DOM-Based-AngularJS` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based-AngularJS) |
| 2973 | **Web Socket - 0 protection** | `Web-Socket-0-protection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Web-Socket-0-protection) |
| 3715 | **CSP Bypass - Nonce** | `CSP-Bypass-Nonce` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-Nonce) |
| 3716 | **CSS - Exfiltration** | `CSS-Exfiltration` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSS-Exfiltration) |
| 3750 | **DOM Clobbering** | `DOM-Clobbering` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/DOM-Clobbering) |
| 3751 | **XS Leaks** | `XS-Leaks` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/XS-Leaks) |
| 3771 | **Javascript - Obfuscation 6** | `Javascript-Obfuscation-6` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-6) |
| 3891 | **CSP Bypass - Nonce 2** | `CSP-Bypass-Nonce-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSP-Bypass-Nonce-2) |
| 4268 | **AST - Deobfuscation** | `AST-Deobfuscation` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/AST-Deobfuscation) |
| 4351 | **Self XSS - DOM Secrets** | `Self-XSS-DOM-Secrets` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Self-XSS-DOM-Secrets) |
| 4352 | **Self XSS - Race Condition** | `Self-XSS-Race-Condition` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Self-XSS-Race-Condition) |
| 4353 | **Same Origin Method Execution** | `Same-Origin-Method-Execution` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Same-Origin-Method-Execution) |
| 4354 | **Browser - bfcache / disk cache** | `Browser-bfcache-disk-cache` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Browser-bfcache-disk-cache) |
| 4362 | **Relative Path Overwrite** | `Relative-Path-Overwrite` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/Relative-Path-Overwrite) |
| 4769 | **CSPT - The Ruler** | `CSPT-The-Ruler` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Client/CSPT-The-Ruler) |

### 📌 Web - Server（97 Challenges）

| ID | 挑戰名稱 (Title) | 關卡代碼 (Slug) | 官方直連傳送門 |
| :--- | :--- | :--- | :--- |
| 6 | **HTML - Source code** | `HTML-Source-code` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTML-Source-code) |
| 14 | **HTTP - User-agent** | `HTTP-User-agent` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-User-agent) |
| 20 | **Weak password** | `Weak-password` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Weak-password) |
| 30 | **HTTP - Directory indexing** | `HTTP-Directory-indexing` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Directory-indexing) |
| 36 | **HTTP - Headers** | `HTTP-Headers` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Headers) |
| 48 | **Install files** | `Install-files` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Install-files) |
| 56 | **HTTP - Cookies** | `HTTP-Cookies` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Cookies) |
| 58 | **SQL injection - Blind** | `SQL-injection-Blind` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Blind) |
| 115 | **HTTP - Verb tampering** | `HTTP-Verb-tampering` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Verb-tampering) |
| 133 | **SQL injection - Authentication** | `SQL-injection-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Authentication) |
| 137 | **Backup file** | `Backup-file` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Backup-file) |
| 139 | **PHP - Filters** | `PHP-Filters` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Filters) |
| 161 | **Directory traversal** | `Directory-traversal` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Directory-traversal) |
| 163 | **CRLF** | `CRLF` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/CRLF) |
| 169 | **Local File Inclusion** | `Local-File-Inclusion` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion) |
| 173 | **PHP - register globals** | `PHP-register-globals` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-register-globals) |
| 289 | **SQL injection - Numeric** | `SQL-injection-Numeric` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Numeric) |
| 291 | **SQL injection - String** | `SQL-injection-String` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-String) |
| 293 | **File upload - Double extensions** | `File-upload-Double-extensions` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/File-upload-Double-extensions) |
| 295 | **File upload - MIME type** | `File-upload-MIME-type` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/File-upload-MIME-type) |
| 297 | **File upload - Null byte** | `File-upload-Null-byte` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/File-upload-Null-byte) |
| 299 | **XPath injection - Authentication** | `XPath-injection-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Authentication) |
| 302 | **XPath injection - Blind** | `XPath-injection-Blind` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Blind) |
| 342 | **LDAP injection - Authentication** | `LDAP-injection-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/LDAP-injection-Authentication) |
| 344 | **XPath injection - String** | `XPath-injection-String` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-String) |
| 354 | **LDAP injection - Blind** | `LDAP-injection-Blind` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/LDAP-injection-Blind) |
| 389 | **PHP - Serialization** | `PHP-Serialization` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Serialization) |
| 411 | **XML External Entity** | `XML-External-Entity` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XML-External-Entity) |
| 415 | **SQL injection - Filter bypass** | `SQL-injection-Filter-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Filter-bypass) |
| 426 | **SQL injection - File reading** | `SQL-injection-File-reading` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-File-reading) |
| 428 | **Remote File Inclusion** | `Remote-File-Inclusion` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Remote-File-Inclusion) |
| 438 | **HTTP - Improper redirect** | `HTTP-Improper-redirect` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Improper-redirect) |
| 643 | **SQL injection - Insert** | `SQL-injection-Insert` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Insert) |
| 650 | **SQL injection - Error** | `SQL-injection-Error` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Error) |
| 834 | **PHP - Path Truncation** | `PHP-Path-Truncation` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Path-Truncation) |
| 856 | **SQL Truncation** | `SQL-Truncation` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-Truncation) |
| 879 | **NoSQL injection - Authentication** | `NoSQL-injection-Authentication` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/NoSQL-injection-Authentication) |
| 950 | **SQL injection - Time based** | `SQL-injection-Time-based` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Time-based) |
| 967 | **Java - Server-side Template Injection** | `Java-Server-side-Template-Injection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Java-Server-side-Template-Injection) |
| 976 | **SQL injection - Authentication - GBK** | `SQL-injection-Authentication-GBK` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Authentication-GBK) |
| 1033 | **PHP - preg_replace()** | `PHP-preg-replace` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-preg-replace) |
| 1036 | **Local File Inclusion - Wrappers** | `Local-File-Inclusion-Wrappers` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion-Wrappers) |
| 1043 | **PHP - type juggling** | `PHP-type-juggling` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-type-juggling) |
| 1054 | **Local File Inclusion - Double encoding** | `Local-File-Inclusion-Double-encoding` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion-Double-encoding) |
| 1371 | **PHP - assert()** | `PHP-assert` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-assert) |
| 1377 | **NoSQL injection - Blind** | `NoSQL-injection-Blind` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/NoSQL-injection-Blind) |
| 1390 | **SQL Injection - Routed** | `SQL-Injection-Routed` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-Injection-Routed) |
| 1396 | **Java - Spring Boot** | `Java-Spring-Boot` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Java-Spring-Boot) |
| 1571 | **XSLT - Code execution** | `XSLT-Code-execution` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XSLT-Code-execution) |
| 1599 | **HTTP - Open redirect** | `HTTP-Open-redirect` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Open-redirect) |
| 1603 | **File upload - ZIP** | `File-upload-ZIP` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/File-upload-ZIP) |
| 1651 | **PHP - Command injection** | `PHP-Command-injection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Command-injection) |
| 1654 | **Command injection - Filter bypass** | `Command-injection-Filter-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Command-injection-Filter-bypass) |
| 1726 | **PHP - Loose Comparison** | `PHP-Loose-Comparison` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Loose-Comparison) |
| 1783 | **Server Side Request Forgery** | `Server-Side-Request-Forgery` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Server-Side-Request-Forgery) |
| 1830 | **HTTP - POST** | `HTTP-POST` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-POST) |
| 1931 | **PHP - Eval** | `PHP-Eval` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Eval) |
| 2072 | **JWT - Introduction** | `JWT-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Introduction) |
| 2074 | **JWT - Weak secret** | `JWT-Weak-secret` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Weak-secret) |
| 2075 | **JWT - Public key** | `JWT-Public-key` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Public-key) |
| 2099 | **Insecure Code Management** | `Insecure-Code-Management` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Insecure-Code-Management) |
| 2227 | **PHP - Remote Xdebug** | `PHP-Remote-Xdebug` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Remote-Xdebug) |
| 2231 | **JWT - Revoked token** | `JWT-Revoked-token` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Revoked-token) |
| 2245 | **PHP - Unserialize overflow** | `PHP-Unserialize-overflow` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Unserialize-overflow) |
| 2357 | **GraphQL - Mutation** | `GraphQL-Mutation` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Mutation) |
| 2825 | **Node - Serialize** | `Node-Serialize` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Node-Serialize) |
| 2830 | **Node - Eval** | `Node-Eval` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Node-Eval) |
| 2863 | **HTTP - IP restriction bypass** | `HTTP-IP-restriction-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/HTTP-IP-restriction-bypass) |
| 2872 | **NodeJS - vm escape** | `NodeJS-vm-escape` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/NodeJS-vm-escape) |
| 2886 | **PHP - Eval - Advanced filters bypass** | `PHP-Eval-Advanced-filters-bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Eval-Advanced-filters-bypass) |
| 2897 | **Yaml - Deserialization** | `Yaml-Deserialization` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Yaml-Deserialization) |
| 2958 | **PHP - Apache configuration** | `PHP-Apache-configuration` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Apache-configuration) |
| 2963 | **Python - Blind SSTI Filters Bypass** | `Python-Blind-SSTI-Filters-Bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Python-Blind-SSTI-Filters-Bypass) |
| 2965 | **Python - Server-side Template Injection Introduction** | `Python-Server-side-Template-Injection-Introduction` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Python-Server-side-Template-Injection-Introduction) |
| 2974 | **NodeJS - Prototype Pollution Bypass** | `NodeJS-Prototype-Pollution-Bypass` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/NodeJS-Prototype-Pollution-Bypass) |
| 2975 | **PHP - Unserialize Pop Chain** | `PHP-Unserialize-Pop-Chain` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/PHP-Unserialize-Pop-Chain) |
| 3714 | **File upload - Polyglot** | `File-upload-Polyglot` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/File-upload-Polyglot) |
| 3888 | **Flask - Unsecure session** | `Flask-Unsecure-session` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Flask-Unsecure-session) |
| 3889 | **Flask - Development server** | `Flask-Development-server` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Flask-Development-server) |
| 4072 | **GraphQL - Backend injection** | `GraphQL-Backend-injection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Backend-injection) |
| 4073 | **GraphQL - Injection** | `GraphQL-Injection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Injection) |
| 4074 | **GraphQL - Introspection** | `GraphQL-Introspection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Introspection) |
| 4148 | **JWT - Unsecure Key Handling** | `JWT-Unsecure-Key-Handling` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Unsecure-Key-Handling) |
| 4150 | **JWT - Header Injection** | `JWT-Header-Injection` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Header-Injection) |
| 4152 | **JWT - Unsecure File Signature** | `JWT-Unsecure-File-Signature` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/JWT-Unsecure-File-Signature) |
| 4283 | **Java - Custom gadget deserialization** | `Java-Custom-gadget-deserialization` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Java-Custom-gadget-deserialization) |
| 4303 | **XSS - Server Side** | `XSS-Server-Side` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/XSS-Server-Side) |
| 4464 | **SQL Injection - Second Order** | `SQL-Injection-Second-Order` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/SQL-Injection-Second-Order) |
| 4465 | **Elixir - EEx** | `Elixir-EEx` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Elixir-EEx) |
| 4537 | **API - Broken Access** | `API-Broken-Access` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/API-Broken-Access) |
| 4538 | **API - Mass Assignment** | `API-Mass-Assignment` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/API-Mass-Assignment) |
| 4539 | **API - Broken Access 2** | `API-Broken-Access-2` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/API-Broken-Access-2) |
| 4771 | **Python - dotenv** | `Python-dotenv` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Python-dotenv) |
| 4772 | **Nginx - SSRF Misconfiguration** | `Nginx-SSRF-Misconfiguration` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Nginx-SSRF-Misconfiguration) |
| 4773 | **Nginx - Root Location Misconfiguration** | `Nginx-Root-Location-Misconfiguration` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Nginx-Root-Location-Misconfiguration) |
| 4774 | **Nginx - Alias Misconfiguration** | `Nginx-Alias-Misconfiguration` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Nginx-Alias-Misconfiguration) |
| 4889 | **Ruby on Rails - ransack** | `Ruby-on-Rails-ransack` | [前往挑戰](https://www.root-me.org/en/Challenges/Web-Server/Ruby-on-Rails-ransack) |
