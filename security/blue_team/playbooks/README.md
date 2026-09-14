# 📘 藍隊原子實戰手冊庫 (Blue Team Atomic Playbooks)

> 🛡️ **本目錄宗旨**：  
> 徹底告別冷冰冰的教科書與概念骨架！本目錄**嚴格依照 Phase 0 ➔ Phase 6 職涯學習階段**，收錄 **107 個細分技術點的專屬實戰手冊（Runbooks / Playbooks）**。  
> 每一篇手冊皆嚴格採用「破案情境敘事流」，帶領分析師從案發現場的第一秒開始，順著專業調查員的思考脈絡，完成底層解剖、異常解碼、指令追兇、誤報研判與圍堵處置。

---

## 📜 撰寫規範與品質準則

所有手冊的編寫與審查，**必須且唯一依循以下標準文件**：
👉 **[PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md](PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md)**

### 核心不可逾越鐵律：
1. **五動敘事流**：每篇手冊必備「🚨 案發現場破題 ➔ 🧩 第一動：底層機制 ➔ 🧭 第二動：解碼意圖 ➔ 💻 第三動：現場追兇 ➔ ⚖️ 第四動：研判分水嶺 ➔ 🛡️ 第五動：處置加固 ➔ 🎯 靶場闖關 ➔ 📋 五題檢核點」。
2. **嚴格 3 欄式速查表**：`封包與日誌特徵現象（看到什麼）` | `底層成因與攻擊手法（是什麼攻擊）` | `威脅影響與處置優先級（怎麼應對）`。
3. **嚴格 2 欄式研判表**：`核心提問（研判維度）` | `本技術點實戰檢核標準`。
4. **真實生產級作戰代碼**：拒絕概念偽代碼，所有 PowerShell（XML 解析）、Wireshark 過濾器、Linux 核心命令、Splunk SPL 皆須可在真實系統中運行。

---

## 📂 Phase 階段手冊目錄與索引

### 🟢 [phase_0_foundation/](phase_0_foundation/) —— IT 底層與運作原語 (打底與基本功)
- [01.1_linux_auth_pam_sudoers.md](phase_0_foundation/01.1_linux_auth_pam_sudoers.md)：Linux 帳號安全、PAM 模組與 Sudoers 權限配置
- [01.2_linux_systemd_cron_process.md](phase_0_foundation/01.2_linux_systemd_cron_process.md)：Linux 系統服務管理 (systemd)、排程安全 (crontab) 與進程異常分析
- [06.1_wireshark_tcp_handshake.md](phase_0_foundation/06.1_wireshark_tcp_handshake.md)：Wireshark 封包解構與 TCP 三向交握異常 (SYN Flood / RST 異常中斷)
- [06.2_dns_tunneling_dga.md](phase_0_foundation/06.2_dns_tunneling_dga.md)：DNS 協定鑑識與惡意通道分析 (DNS Tunneling / DGA 網域名稱演算法)
- [06.3_http_tls_ja3_fingerprint.md](phase_0_foundation/06.3_http_tls_ja3_fingerprint.md)：HTTP/HTTPS 流量特徵分析與 TLS 握手解構 (JA3/JA4 指紋鑑識)
- [11.1_windows_auth_ntlm_kerberos.md](phase_0_foundation/11.1_windows_auth_ntlm_kerberos.md)：Windows 身分驗證核心原理 (NTLM 挑戰-回應 vs Kerberos 票證架構)
- [11.2_ad_architecture_dc_ldap_gc.md](phase_0_foundation/11.2_ad_architecture_dc_ldap_gc.md)：Active Directory 核心架構 (網域控制站 DC、LDAP、全局編錄 GC 與信任關係)
- [11.3_gpo_deployment_baseline.md](phase_0_foundation/11.3_gpo_deployment_baseline.md)：網域群組原則 (GPO) 部署與資安基線管理

### 📡 [phase_1_visibility/](phase_1_visibility/) —— 端點與網路可見性 (藍隊真正起點)
- [14.1_windows_logon_4624_4625.md](phase_1_visibility/14.1_windows_logon_4624_4625.md)：Windows 身分驗證與暴力破解日誌 (Event ID 4624 / 4625)
- [14.2_windows_core_processes_baseline.md](phase_1_visibility/14.2_windows_core_processes_baseline.md)：Windows 正常核心進程親緣基準線 (System ➔ smss ➔ services 親緣樹與偽裝破譯)
- [14.3_windows_events_7045_4688.md](phase_1_visibility/14.3_windows_events_7045_4688.md)：基礎系統管理與服務安裝日誌 (Event ID 7045 新服務安裝與 4688 命令列參數完整記錄)
- [14.4_windows_defender_operational_logs.md](phase_1_visibility/14.4_windows_defender_operational_logs.md)：防毒與主機防護日誌鑑識 (Microsoft Defender Event ID 1116 / 1117 / 5001)
- [18.1_sysmon_process_telemetry_events.md](phase_1_visibility/18.1_sysmon_process_telemetry_events.md)：Sysmon 驅動級進程遙測與命令行 (Sysmon Event ID 1 / 3 / 7 / 8)
- [09.1_web_sqli_command_injection.md](phase_1_visibility/09.1_web_sqli_command_injection.md)：注入類漏洞流量特徵與防禦 (SQL Injection / Command Injection)
- [09.2_web_path_traversal_xxe.md](phase_1_visibility/09.2_web_path_traversal_xxe.md)：檔案路徑穿越與 XML 外部實體特徵 (Path Traversal / XXE)
- [09.3_web_xss_csrf_defense.md](phase_1_visibility/09.3_web_xss_csrf_defense.md)：跨站腳本與請求偽造防範 (XSS / CSRF)
- [09.4_web_info_leak_directory_listing.md](phase_1_visibility/09.4_web_info_leak_directory_listing.md)：敏感資訊洩漏與目錄遍歷 (Information Disclosure / Directory Listing)
- [01.3_linux_ssh_pam_fail2ban.md](phase_1_visibility/01.3_linux_ssh_pam_fail2ban.md)：帳號安全與 SSH 遠端登入硬化 (SSH Key-Only, Fail2ban, PAM Limits)
- [01.4_linux_cron_systemd_persistence.md](phase_1_visibility/01.4_linux_cron_systemd_persistence.md)：排程作業與自啟動項排查 (/etc/cron*, crontab -l, systemd timers)

### 📊 [phase_2_soc_triage/](phase_2_soc_triage/) —— SOC 告警研判與樞紐分析
- [02.1_border_firewall_surgical_blocking.md](phase_2_soc_triage/02.1_border_firewall_surgical_blocking.md)：邊界防火牆策略與微創阻斷實務 (Border Firewall Policies & Surgical Blocking)
- [10.1_email_auth_spf_dkim_dmarc.md](phase_2_soc_triage/10.1_email_auth_spf_dkim_dmarc.md)：郵件認證協定與仿冒偵測 (SPF, DKIM & DMARC Spoofing Defense)
- [10.2_phishing_header_attachment_triage.md](phase_2_soc_triage/10.2_phishing_header_attachment_triage.md)：釣魚郵件標頭與惡意附件初篩 (Phishing Header Analysis & Attachment Triage)
- [10.4_quishing_redirect_chain_analysis.md](phase_2_soc_triage/10.4_quishing_redirect_chain_analysis.md)：QR Code 釣魚與跳轉識別 (Quishing & Redirect Chain Deobfuscation)
- [15.1_splunk_spl_pipeline_optimization.md](phase_2_soc_triage/15.1_splunk_spl_pipeline_optimization.md)：Splunk SPL 管道檢索與過濾最佳化 (Splunk SPL Pipeline & Search Optimization)
- [15.2_spl_field_extraction_aggregation.md](phase_2_soc_triage/15.2_spl_field_extraction_aggregation.md)：SPL 動態欄位提取與聚合統計分析 (SPL Field Extraction & Statistical Aggregation)
- [15.3_correlation_rules_threshold_tuning.md](phase_2_soc_triage/15.3_correlation_rules_threshold_tuning.md)：關聯分析規則建立與告警門檻設計 (Correlation Rules & Threshold Tuning)
- [16.1_dns_tunneling_exfiltration_forensics.md](phase_2_soc_triage/16.1_dns_tunneling_exfiltration_forensics.md)：DNS 隧道通訊與機密外洩分析 (DNS Tunneling & Exfiltration Forensics)
- [16.2_c2_beaconing_jitter_analysis.md](phase_2_soc_triage/16.2_c2_beaconing_jitter_analysis.md)：C2 心跳模式與週期抖動分析 (C2 Beaconing & Jitter Analysis)
- [19.4_dynamic_sandbox_report_triage.md](phase_2_soc_triage/19.4_dynamic_sandbox_report_triage.md)：動態沙箱行為報告解讀 (Dynamic Sandbox Report Triage)
- [22.1_cvss_metrics_score_calculation.md](phase_2_soc_triage/22.1_cvss_metrics_score_calculation.md)：CVSS v3.1/v4.0 基本指標與評分計算 (CVSS Metrics & Score Calculation)

### 📝 [phase_3_detection_eng/](phase_3_detection_eng/) —— 偵測工程與簽章生命週期
- [02.3_ngfw_ips_suricata_inline.md](phase_3_detection_eng/02.3_ngfw_ips_suricata_inline.md)：次世代防火牆 (NGFW) 與 IPS 聯防 (NGFW & Suricata Inline IPS Defense)
- [15.4_siem_baseline_anomaly_detection.md](phase_3_detection_eng/15.4_siem_baseline_anomaly_detection.md)：巨量資安日誌基準線與異常偏離偵測 (SIEM Baseline & Anomaly Detection)
- [16.3_nday_packet_reverse_engineering.md](phase_3_detection_eng/16.3_nday_packet_reverse_engineering.md)：知名 N-day 漏洞利用封包逆推 (N-day Exploit Packet Reverse Engineering)
- [17.1_yara_binary_rules_webshell.md](phase_3_detection_eng/17.1_yara_binary_rules_webshell.md)：YARA 檔案二進位特徵碼規則撰寫 (WebShell 與惡意 PE 實戰鑑識)
- [17.2_sigma_rules_transpilation.md](phase_3_detection_eng/17.2_sigma_rules_transpilation.md)：Sigma 通用日誌偵測規則與轉譯 (Sigma Rules & pySigma Transpilation)
- [17.3_suricata_snort_network_rules.md](phase_3_detection_eng/17.3_suricata_snort_network_rules.md)：Snort/Suricata 網路入侵特徵撰寫 (Content, Offset, Depth 與協定解析實戰)
- [17.4_detection_rule_tuning_lifecycle.md](phase_3_detection_eng/17.4_detection_rule_tuning_lifecycle.md)：偵測規則生命週期與誤判除錯 (Detection Rule Lifecycle & FP Tuning)
- [21.1_cti_pyramid_of_pain_attck_mapping.md](phase_3_detection_eng/21.1_cti_pyramid_of_pain_attck_mapping.md)：威脅指標管理與 ATT&CK 戰術映射 (CTI Pyramid of Pain & MITRE ATT&CK Mapping)
- [22.2_historical_cve_log4shell_deepdive.md](phase_3_detection_eng/22.2_historical_cve_log4shell_deepdive.md)：歷史重大 CVE 運作機制逆推 (Log4Shell CVE-2021-44228 Deep Dive)

### 🚨 [phase_4_hunting_ir/](phase_4_hunting_ir/) —— 主動威脅獵捕與應變處置 SOP
*(即將依修課時序編撰，深度指南請先參閱 [learning_paths/](../learning_paths/))*

### 🔬 [phase_5_deep_dfir/](phase_5_deep_dfir/) —— 深度取證與專精分流
#### 💾 Track A: 記憶體與磁碟數位鑑識專精
- [23.1_volatility_hidden_process_dkom.md](phase_5_deep_dfir/track_a_memory_disk/23.1_volatility_hidden_process_dkom.md)：隱藏進程與 DKOM 斷鏈破譯 (Volatility 3 / EPROCESS ActiveProcessLinks)
- [23.2_vad_tree_code_injection_malfind.md](phase_5_deep_dfir/track_a_memory_disk/23.2_vad_tree_code_injection_malfind.md)：VAD 樹與記憶體程式碼注入分析 (Virtual Address Descriptors & Code Injection)
- [23.3_memory_netscan_binary_dump.md](phase_5_deep_dfir/track_a_memory_disk/23.3_memory_netscan_binary_dump.md)：核心網路連線還原與二進位導出 (Memory Netscan & Binary Dump)
- [23.4_lsass_memory_credential_extraction.md](phase_5_deep_dfir/track_a_memory_disk/23.4_lsass_memory_credential_extraction.md)：記憶體憑證抓取與暫存區取證 (LSASS Memory Credential Extraction & Clipboard Forensics)
- [24.1_ntfs_mft_timestomping_analysis.md](phase_5_deep_dfir/track_a_memory_disk/24.1_ntfs_mft_timestomping_analysis.md)：NTFS 主檔案表與時間戳偽造 ($MFT & Timestomping Analysis)
- [24.2_windows_execution_prefetch_amcache.md](phase_5_deep_dfir/track_a_memory_disk/24.2_windows_execution_prefetch_amcache.md)：程式執行三大鐵證深度鑑識 (Prefetch, ShimCache & Amcache)
- [24.3_userassist_shellbags_registry_forensics.md](phase_5_deep_dfir/track_a_memory_disk/24.3_userassist_shellbags_registry_forensics.md)：使用者活動軌跡與登錄檔鑑識 (UserAssist, ShellBags & Registry Forensics)
- [24.4_vss_volume_shadow_copy_forensics.md](phase_5_deep_dfir/track_a_memory_disk/24.4_vss_volume_shadow_copy_forensics.md)：系統更新日誌與陰影複製取證 (Volume Shadow Copy Forensics & Event Log Recovery)

#### 🏰 Track B: AD 網域攻防與身分治理專精
- [12.1_kerberos_preauth_asrep_roasting.md](phase_5_deep_dfir/track_b_active_directory/12.1_kerberos_preauth_asrep_roasting.md)：Kerberos 預驗證弱點與 AS-REP Roasting 攻防 (Kerberos Pre-Auth & AS-REP Roasting)
- [12.2_spn_kerberoasting_detection.md](phase_5_deep_dfir/track_b_active_directory/12.2_spn_kerberoasting_detection.md)：SPN 服務票據請求與 Kerberoasting 偵測 (SPN Tickets & Kerberoasting Detection)
- [12.3_golden_silver_ticket_forgery.md](phase_5_deep_dfir/track_b_active_directory/12.3_golden_silver_ticket_forgery.md)：偽造票據攻擊與全域特權維持 (Golden & Silver Ticket Forgery Detection)
- [12.4_dcsync_ntds_credential_dumping.md](phase_5_deep_dfir/track_b_active_directory/12.4_dcsync_ntds_credential_dumping.md)：目錄複寫服務特權與 DCSync 憑證傾印偵測 (DCSync & NTDS.dit Credential Extraction)
- [12.5_bloodhound_acl_attack_paths.md](phase_5_deep_dfir/track_b_active_directory/12.5_bloodhound_acl_attack_paths.md)：AD 物件權限濫用與 BloodHound 攻擊路徑阻斷 (BloodHound ACL Attack Paths & Remediation)
- [13.1_oauth2_saml_token_abuse.md](phase_5_deep_dfir/track_b_active_directory/13.1_oauth2_saml_token_abuse.md)：雲端與現代身分驗證協定濫用 (OAuth 2.0 & SAML Token Abuse)
- [13.2_mfa_fatigue_bypass_defense.md](phase_5_deep_dfir/track_b_active_directory/13.2_mfa_fatigue_bypass_defense.md)：多因素驗證疲勞轟炸與即時中間人釣魚防禦 (MFA Fatigue & AiTM Phishing Defense)
- [13.3_service_account_prt_abuse.md](phase_5_deep_dfir/track_b_active_directory/13.3_service_account_prt_abuse.md)：服務帳號權限濫用與 Azure AD PRT 權杖劫持防護 (Service Account & Primary Refresh Token Abuse)

#### ☁️ Track C: 雲原生、供應鏈與無檔案專精
- [02.2_internal_network_microsegmentation.md](phase_5_deep_dfir/track_c_cloud_supplychain/02.2_internal_network_microsegmentation.md)：內部網路微隔離與 VLAN 存取控制 (Internal Network Microsegmentation)
- [04.1_supply_chain_dependency_confusion.md](phase_5_deep_dfir/track_c_cloud_supplychain/04.1_supply_chain_dependency_confusion.md)：開源依賴投毒與相依性混淆防護 (Supply Chain Dependency Confusion)
- [04.2_sbom_vulnerability_management.md](phase_5_deep_dfir/track_c_cloud_supplychain/04.2_sbom_vulnerability_management.md)：軟體物料清單 (SBOM) 審查與自動化弱點追蹤 (SBOM Analysis & Vulnerability Tracking)
- [04.3_cicd_pipeline_secret_protection.md](phase_5_deep_dfir/track_c_cloud_supplychain/04.3_cicd_pipeline_secret_protection.md)：CI/CD 自動化管道審計與密鑰外洩防範 (CI/CD Pipeline Security & Secret Protection)
- [05.1_cloud_shared_responsibility_matrix.md](phase_5_deep_dfir/track_c_cloud_supplychain/05.1_cloud_shared_responsibility_matrix.md)：雲端運算共同責任模型實務與邊界劃分 (Cloud Security Shared Responsibility Matrix)
- [05.2_cloud_iam_privilege_escalation.md](phase_5_deep_dfir/track_c_cloud_supplychain/05.2_cloud_iam_privilege_escalation.md)：雲端多租戶 IAM 提權與 CloudTrail 審計日誌研判 (Cloud IAM Privilege Escalation)
- [05.3_container_escape_k8s_runtime_defense.md](phase_5_deep_dfir/track_c_cloud_supplychain/05.3_container_escape_k8s_runtime_defense.md)：容器逃逸機制與 Kubernetes 運行時威脅防禦 (Container Escape & K8s Runtime Security)
- [05.4_s3_bucket_leak_imds_ssrf_defense.md](phase_5_deep_dfir/track_c_cloud_supplychain/05.4_s3_bucket_leak_imds_ssrf_defense.md)：雲端儲存桶外洩與中繼資料 (IMDS) 劫持防護 (S3 Bucket Leaks & IMDSv2 SSRF Defense)
- [16.4_http_request_smuggling_defense.md](phase_5_deep_dfir/track_c_cloud_supplychain/16.4_http_request_smuggling_defense.md)：協定走私與反向代理混淆鑑識 (HTTP Request Smuggling & Reverse Proxy Desync)
- [20.1_java_memshell_filter_servlet_forensics.md](phase_5_deep_dfir/track_c_cloud_supplychain/20.1_java_memshell_filter_servlet_forensics.md)：Java 內存馬清剿與 Filter/Servlet 運行時取證 (Java Memory Shell Forensics)
- [20.3_dotnet_php_fileless_memshell.md](phase_5_deep_dfir/track_c_cloud_supplychain/20.3_dotnet_php_fileless_memshell.md)：.NET 與 PHP 內存馬與無檔案後門排查 (DotNet & PHP Fileless Memory Shell Defense)

#### 🔌 Track D: 網路通訊設備與硬體安全專精 (8 項)
- [03.1_switch_port_security_errdisable.md](phase_5_deep_dfir/track_d_network_hardware/03.1_switch_port_security_errdisable.md)：交換機連接埠安全與 MAC 違規處置 (Switch Port-Security & Errdisable Recovery)
- [03.2_vlan_tagging_trunk_hopping_defense.md](phase_5_deep_dfir/track_d_network_hardware/03.2_vlan_tagging_trunk_hopping_defense.md)：VLAN 標記結構與 Trunk 跳躍攻擊防禦 (IEEE 802.1Q VLAN Tagging & Double-Tagging Defense)
- [03.3_stp_bpdu_guard_dhcp_snooping.md](phase_5_deep_dfir/track_d_network_hardware/03.3_stp_bpdu_guard_dhcp_snooping.md)：交換機鏈路防護與生成樹安全 (BPDU Guard, Root Guard & DHCP Snooping)
- [07.1_snmpv3_security_authpriv_hardening.md](phase_5_deep_dfir/track_d_network_hardware/07.1_snmpv3_security_authpriv_hardening.md)：SNMP 版本安全演進與 v3 authPriv 實踐 (SNMPv3 Security & authPriv Hardening)
- [07.2_vpn_ipsec_wireguard_security_showdown.md](phase_5_deep_dfir/track_d_network_hardware/07.2_vpn_ipsec_wireguard_security_showdown.md)：企業級 VPN 協定對決與 IPsec/WireGuard 防禦 (Enterprise VPN Protocols IPsec & WireGuard)
- [08.1_wifi_80211_four_way_handshake_analysis.md](phase_5_deep_dfir/track_d_network_hardware/08.1_wifi_80211_four_way_handshake_analysis.md)：802.11 四向握手鑑識與 EAPOL 重播攻擊分析 (802.11 4-Way Handshake & EAPOL Forensics)
- [08.2_wifi_wpa3_sae_dragonfly_defense.md](phase_5_deep_dfir/track_d_network_hardware/08.2_wifi_wpa3_sae_dragonfly_defense.md)：Wi-Fi WPA3 SAE 密鑰交換防禦與 KRACK 重裝攻擊獵捕 (WPA3 SAE Dragonfly & KRACK Defense)
- [11.3_crypto_ciphersuite_downgrade_pfs.md](phase_5_deep_dfir/track_d_network_hardware/11.3_crypto_ciphersuite_downgrade_pfs.md)：傳輸加密密鑰套件降級防禦與前向保密性實踐 (Cipher Suite Downgrade & Perfect Forward Secrecy)

### 👑 [phase_6_capstone/](phase_6_capstone/) —— 紫隊全真演練與畢業門檻
*(即將依修課時序編撰)*

