# NCtfU 資安社｜2026 秋季週五讀書會簡明進度表 (幹部版)

> **🎯 本學期核心進程**：
> - **9月～11月**：衝刺「金盾獎資安競賽」
> - **12月**：試行「全國技能競賽」實務題型（磁碟鑑識、防火牆配置），評估下學期培訓走向。
> - **運作原則**：社員每週從清單中「各自挑選 1 題」認領實作，不強制全刷。詳細流程規範統一見 [每週實作課表](classic_ctf_practice_table.md)。

---

| 週次與日期 | 當週推薦題目清單（每人自選 1 題認領） | 核心目標 (Why) | 題目出處／備註 |
| :---: | :--- | :--- | :--- |
| **W1 (9/18)** | • **Web**: [SSTI1 #492](https://learn.cylabacademy.org/library?search=SSTI1)<br>• **逆向**: [vault-door-3 #60](https://learn.cylabacademy.org/library?search=vault-door-3)<br>• **Pwn**: [Local Target #399](https://learn.cylabacademy.org/library?search=Local%20Target)<br>• **密碼**: [Dachshund Attacks #159](https://learn.cylabacademy.org/library?search=Dachshund%20Attacks)<br>• **流量**: [Wireshark twoo twooo... #110](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...) | **六領域摸底診斷與分工**<br>盤點社員熟悉度，確立金盾 3 人隊伍主修／副修分工。 | CyLab 題庫 (picoCTF)<br>直接點擊連結啟動練習 |
| **W2 (9/25)** | • **逆向**: [keygenme-py #121](https://learn.cylabacademy.org/library?search=keygenme-py)<br>• **Pwn**: [buffer overflow 1 #258](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) | **底層程式流程與 Stack 溢出**<br>讀懂 Python 反組譯金鑰驗證與 C 語言 Stack 記憶體覆寫。 | CyLab 題庫 (picoCTF 2021/2022) |
| **W3 (10/2)** | • **Web**: [SSTI2 #488](https://learn.cylabacademy.org/library?search=SSTI2)<br>• **密碼**: [No Padding, No Problem #154](https://learn.cylabacademy.org/library?search=No%20Padding%2C%20No%20Problem) | **Web 模板繞過與 RSA 代數特性**<br>掌握進階 SSTI 過濾繞過與 RSA 乘法同態無填充弱點。 | CyLab 題庫 (picoCTF 2025/2021) |
| **W4 (10/9)** | **初賽形式全真模擬測驗**<br>(社內自編 36 題單選題，六領域各 6 題) | **金盾初賽全真模擬**<br>適應 90 分鐘單選題答題節奏，排查觀念盲點。 | 社內自編題庫 (10/7 覆核公告)<br>涵蓋六領域官方文件與 CVE |
| **W5 (10/16)** | **不排新題**（賽前環境確認與錯題回顧） | **賽前準備與減壓**<br>檢視 10/9 錯題，確認初賽帳密與隊內通訊設備。 | 回顧 10/9 模擬卷錯題清單<br>(10/17 金盾初賽) |
| **W6 (10/23)** | • **Web**: [Crack the Gate 1 #520](https://learn.cylabacademy.org/library?search=Crack%20the%20Gate%201)<br>• **逆向**: [Flag Hunters #472](https://learn.cylabacademy.org/library?search=Flag%20Hunters)<br>• 初賽可公開題目覆盤研討 | **初賽復盤與 Web/逆向深化**<br>檢討初賽不足，攻堅黑箱認證繞過與程式特徵分析。 | CyLab 題庫 (picoMini Africa/2025) |
| **W7 (10/30)** | *段考週休息（不開會）* | **段考溫書與查看入圍名單** | 自主溫書 |
| **W8 (11/6)** | • **流量**: [Trivial Flag Transfer #103](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol)<br>• **鑑識**: [Riddle Registry #530](https://learn.cylabacademy.org/library?search=Riddle%20Registry) | **TFTP 協定還原與 Windows 註冊表**<br>從流量提取傳輸檔案，並分析註冊表敏感機碼。 | CyLab 題庫 (picoCTF 2021/picoMini Africa)<br>銜接週三 Wireshark 社課 |
| **W9 (11/13)** | • **Pwn**: [format string 1 #434](https://learn.cylabacademy.org/library?search=format%20string%201)<br>• **Pwn**: [heap 0 #438](https://learn.cylabacademy.org/library?search=heap%200)<br>*(先備不足可選: [format string 0 #433](https://learn.cylabacademy.org/library?search=format%20string%200))* | **Pwn 進階：格式化字串與 Heap 基礎**<br>掌握 Format String 記憶體讀寫與 Heap 堆積覆寫概念。 | CyLab 題庫 (picoCTF 2024) |
| **W10 (11/20)** | **金盾決賽全真模擬（全新未見過題組）**：<br>• **Web**: [Web Gauntlet #88](https://learn.cylabacademy.org/library?search=Web%20Gauntlet)<br>• **Pwn**: [PIE TIME #490](https://learn.cylabacademy.org/library?search=PIE%20TIME)<br>• **密碼**: [StegoRSA #719](https://learn.cylabacademy.org/library?search=StegoRSA)<br>• **鑑識**: [Binary Digits #698](https://learn.cylabacademy.org/library?search=Binary%20Digits) | **金盾決賽停損與團隊換題實戰**<br>90 分鐘限時無提示解題，練習卡關及時求助與換題決策。 | CyLab 題庫 (當天聚會公佈盲測)<br>四題全新題目無重複 |
| **W11 (11/27)** | *金盾決賽日（當晚讀書會暫停休息）* | **出征金盾獎決賽 (5 小時現場賽)** | [教育部/數發部 金盾獎現場](https://csc.nics.nat.gov.tw/shield.aspx) |
| **W12 (12/4)** | • **磁碟鑑識**: [Disk, disk, sleuth! II #137](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21%20II) | **技能競賽體驗 (一)：Linux 磁碟鑑識**<br>分析 ext4 映像檔，練習真實數位證據提取與時間線還原。 | CyLab 題庫 (picoCTF 2021)<br>下載硬碟映像檔實作 |
| **W13 (12/11)** | • **防火牆配置**: [SEED 防火牆實驗室 (Firewall Lab)](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) | **技能競賽體驗 (二)：防火牆配置**<br>體驗技能競賽「安全強化」，撰寫 iptables 白名單規則。 | Syracuse SEED Labs 2.0<br>官方開源 Docker 拓撲環境 |
| **W14 (12/18)** | • **防火牆排錯**: SEED 防火牆自訂排錯任務<br>• 下學期方向評估討論 | **技能競賽體驗 (三)：排錯與決策**<br>排查規則衝突；評估社團下學期是否組隊打技能競賽。 | 同 W13 之 SEED Docker 環境<br>(幹部預置規則衝突) |
| **W15 (12/25)** | *段考週休息（不開會）* | **期末總結** | 自主溫書 |
