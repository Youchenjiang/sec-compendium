# 🧭 藍隊全領域 31 大深度學習路徑全景導航庫 (Blue Team Learning Paths Directory)

> 💡 **核心精神**：本目錄為 [`../index.md`](../index.md) 中 31 個防衛核心領域量身打造的**「全流程深度自學與實戰突破指南」**。
>
> 徹底解決「只有題目、不知道怎麼學、缺乏系統化底層架構」的信心焦慮，每個領域皆包含：**前置基準測試、底層核心機制與封包/記憶體/代碼結構、實驗環境與工具配置、高階攻防對抗排查、自我評估檢查點、時間衝刺策略**。
>
> 🚀 **實戰修課主線**：想知道按部就班的推薦學習順序？請直接參閱 [【現代藍隊實戰通關課表與作戰主線 (Phase 0 ~ Phase 6)】](../career_curriculum.md)（含 SOC 告警分流八問、Incident Response 圍堵 SOP 與 36 項 Core 核心必修）。
>
> 🛡️ **CyberDefenders 免費實戰題庫映射手冊**：所有 82 題官方認證 100% 免費挑戰與 31 大學習路徑的逐題對照與情境索引，請參閱 [【CyberDefenders 全量 82 題免費實戰靶場・31 大學習路徑深度對照手冊】](cyberdefenders_free_catalog_mapping.md)。

---

## 🏛️ 區塊一：事前架構、系統加固與基礎設施防衛 (Architecture & Hardening)
- [領域 01：Linux 系統基礎加固深度學習路徑](block_1_hardening/01_linux_hardening.md) (權限模型、SUID/SGID、SSH/PAM 硬化、Crontab/自啟項)
- [領域 02：網路分段與防火牆加固深度學習路徑](block_1_hardening/02_network_segmentation_firewall.md) (Netfilter 5表5鏈、conntrack 狀態追蹤、DMZ 微隔離、NGFW/IPS)
- [領域 03：交換機硬體安全與鏈路隔離深度學習路徑](block_1_hardening/03_switching_port_security.md) (Port-Security 違規模式、802.1Q 4-Byte Tag、BPDU Guard/Root Guard)
- [領域 04：軟體供應鏈安全 (DevSecOps) 深度學習路徑](block_1_hardening/04_devsecops_supply_chain.md) (相依性混淆、SPDX/CycloneDX SBOM 審查、Gitleaks/Trivy)
- [領域 05：雲原生防衛與雲端責任模型深度學習路徑](block_1_hardening/05_cloud_security_shared_responsibility.md) (IaaS/PaaS/SaaS 責任矩陣、IMDSv2 SSRF 防護、容器逃逸)

---

## 🌐 區塊二：應用程式、協定安全與通訊防禦 (Protocols, Cryptography & Apps)
- [領域 06：網路協定與基礎封包分析深度學習路徑](block_2_protocols_crypto_app/06_network_protocols_packet_analysis.md) (TCP 狀態機、Wireshark 高階過濾、DNS 異常、串流導出)
- [領域 07：網路管理協定 (SNMP) 與 VPN 傳輸安全深度學習路徑](block_2_protocols_crypto_app/07_snmp_vpn_security.md) (SNMPv3 authPriv、四大 VPN 對決、IPsec AH/ESP 深度剖析)
- [領域 08：無線通訊安全機制與協定演進深度學習路徑](block_2_protocols_crypto_app/08_wireless_security_wpa.md) (802.11 4-Way Handshake、KRACK 重裝攻擊、WPA3 SAE 前向保密)
- [領域 09：Web 基礎弱點識別與防衛深度學習路徑](block_2_protocols_crypto_app/09_web_vulnerability_defense.md) (參數化防 SQLi、命令注入、路徑穿越、XXE、CSP 與 Cookie 標頭)
- [領域 10：電子郵件與社交工程防衛深度學習路徑](block_2_protocols_crypto_app/10_email_phishing_defense.md) (SPF/DKIM/DMARC、EML 標頭 Received 溯源、oledump 巨集提取)
- [領域 11：密碼學基礎與證書安全深度學習路徑](block_2_protocols_crypto_app/11_cryptography_certificates.md) (AES-GCM/RSA、X.509 憑證鏈、OCSP Stapling、PFS 前向保密)

---

## 🔑 區塊三：身分驗證、特權存取與目錄服務防護 (Identity & AD)
- [領域 12：Active Directory 網域攻防與防護深度學習路徑](block_3_identity_directory/12_active_directory_defense.md) (Kerberos 交握、AS-REP/Kerberoasting、黃金/白銀票據、DCSync)
- [領域 13：身分存取管理安全 (IAM) 深度學習路徑](block_3_identity_directory/13_identity_access_management.md) (OAuth 2.0 授權碼、MFA 疲勞轟炸、FIDO2 Passkey、工作階段防禦)

---

## 📡 區塊四：即時監控、偵測工程與 SIEM 大數據分析 (SOC & SIEM)
- [領域 14：端點核心日誌與排查深度學習路徑](block_4_detection_siem_soc/14_endpoint_logs_triage.md) (Logon Types 2/3/10、4688 命令列審計、7045 服務安裝)
- [領域 15：SIEM 大數據分析與 Splunk SPL 深度學習路徑](block_4_detection_siem_soc/15_siem_splunk_big_data.md) (SPL 管道語法、rex 欄位提取、stats 聚合、動態基準線告警)
- [領域 16：惡意流量與隱蔽通訊鑑識深度學習路徑](block_4_detection_siem_soc/16_malicious_traffic_covert_comm.md) (C2 心跳與 Jitter 方差分析、DNS 隱蔽隧道、N-day 封包逆推)
- [領域 17：偵測工程與簽章撰寫深度學習路徑](block_4_detection_siem_soc/17_detection_engineering_rules.md) (YARA 檔案特徵碼、Sigma 規則跨平台轉譯、Suricata 網路簽章)

---

## 🏹 區塊五：主動威脅獵捕、惡意樣本分流與無檔案防禦 (Threat Hunting & CTI)
- [領域 18：端點威脅獵捕與 Sysmon 遙測深度學習路徑](block_5_threat_hunting_triage/18_threat_hunting_sysmon.md) (Sysmon Event 1/3/7/8、LOLBAS 合法程式白利用、CreateRemoteThread)
- [領域 19：惡意程式靜態分流深度學習路徑](block_5_threat_hunting_triage/19_malware_static_triage.md) (PE 結構區段表、Shannon 資訊熵加殼辨識、Win32 API 導入表逆推)
- [領域 20：Web 無檔案與記憶體馬防禦深度學習路徑](block_5_threat_hunting_triage/20_web_fileless_defense.md) (Tomcat Filter/Servlet 內存馬、Arthas 記憶體反編譯清剿)
- [領域 21：威脅情資 (CTI) 與 ATT&CK 映射深度學習路徑](block_5_threat_hunting_triage/21_cyber_threat_intelligence.md) (痛苦之塔 Pyramid of Pain、ATT&CK TTPs 映射、獵捕假說設計)
- [領域 22：漏洞通用評分系統 (CVSS) 與重大 CVE 深度剖析](block_5_threat_hunting_triage/22_cvss_metrics_cve_analysis.md) (CVSS v3.1 基本指標計算、Log4Shell 滿分 10.0 逆推、Heartbleed)

---

## 🔬 區塊六：深度數位鑑識、主機核心與行動取證 (DFIR)
- [領域 23：記憶體鑑識實戰深度學習路徑](block_6_dfir_memory_disk/23_memory_forensics.md) (EPROCESS 鏈表、VAD 樹、Volatility 3 核心 Plugin、DKOM 斷鏈)
- [領域 24：磁碟檔案系統鑑識深度學習路徑](block_6_dfir_memory_disk/24_disk_filesystem_forensics.md) (NTFS $MFT、$SI vs $FN 時間偽造辨析、Prefetch/ShimCache/Amcache 三大鐵證)
- [領域 25：Linux 核心與 Rootkit 鑑識深度學習路徑](block_6_dfir_memory_disk/25_linux_kernel_forensics.md) (LKM 核心模組、Syscall Hooking、/etc/ld.so.preload 劫持、eBPF 追蹤)
- [領域 26：行動裝置鑑識深度學習路徑](block_6_dfir_memory_disk/26_mobile_device_forensics.md) (APK 靜態解包、classes.dex 反編譯、SQLite 快取分析、iOS Keychain)

---

## ⚔️ 區塊七：持續防禦驗證、紫隊協同與全真對抗 (Purple Teaming & Range)
- [領域 27：防禦驗證工程與紫隊協同深度學習路徑](block_7_purple_team_range/27_purple_team_breach_simulation.md) (Atomic Red Team 自動化對抗測試、MITRE Caldera、遙測覆蓋率量化)
- [領域 28：企業級全真演練與 Cyber Range 深度學習路徑](block_7_purple_team_range/28_enterprise_cyber_range.md) (Splunk BOTSv2/v3 實網數據集、跨主機橫向移動全局溯源、金盾獎真題)

---

## 📜 區塊八：法規遵循、合規治理與數位證據監管 (GRC & Evidence)
- [領域 29：數位證據法規與監管鏈深度學習路徑](block_8_grc_standards_custody/29_digital_evidence_chain_of_custody.md) (RFC 3227 數據揮發次序、ISO/IEC 27037 標準、防寫設備與雙雜湊驗證)
- [領域 30：台灣《資通安全管理法》與責任等級制深度學習路徑](block_8_grc_standards_custody/30_cyber_security_management_act.md) (A~E 級劃分標準、專職配置與受訓時數、1~4 級事件「1 小時法定通報時限」)
- [領域 31：《個人資料保護法》與隱私安全架構深度學習路徑](block_8_grc_standards_custody/31_personal_data_protection_frameworks.md) (六大特種個資法定除外要件、外洩罰則與賠償、ISO 27001:2022、NIST CSF 2.0)
