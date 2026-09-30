# 🥋 攻防全景聯防矩陣 (Attack-Defense Matrix & TTP Mapping)

> **導讀**：本矩陣為紫隊演練 (Purple Team Exercise) 的核心戰術對映表。它將紅隊 **110 篇特戰手冊** 與藍隊 **107 篇防禦偵測與數位取證手冊** 進行點對點映射，嚴格對齊 MITRE ATT&CK 14 大戰術矩陣，提供作戰團隊一站式查閱進攻手法、對應遙測特徵、偵測規則與應變處置手冊。

---

## 📑 ATT&CK 14 大戰術聯防總覽目錄

- [TA0043: Reconnaissance (偵察)](#ta0043-reconnaissance-偵察)
- [TA0042: Resource Development (資源開發)](#ta0042-resource-development-資源開發)
- [TA0001: Initial Access (初始存取)](#ta0001-initial-access-初始存取)
- [TA0002: Execution (執行)](#ta0002-execution-執行)
- [TA0003: Persistence (持久化)](#ta0003-persistence-持久化)
- [TA0004: Privilege Escalation (權限提升)](#ta0004-privilege-escalation-權限提升)
- [TA0005: Defense Evasion (防禦規避)](#ta0005-defense-evasion-防禦規避)
- [TA0006: Credential Access (憑證存取)](#ta0006-credential-access-憑證存取)
- [TA0007: Discovery (內網探索)](#ta0007-discovery-內網探索)
- [TA0008: Lateral Movement (橫向移動)](#ta0008-lateral-movement-橫向移動)
- [TA0009: Collection (情資收集)](#ta0009-collection-情資收集)
- [TA0011: Command and Control (指揮控制)](#ta0011-command-and-control-指揮控制)
- [TA0010: Exfiltration (資料外洩)](#ta0010-exfiltration-資料外洩)
- [TA0040: Impact (作戰破壞與影響)](#ta0040-impact-作戰破壞與影響)

---

## TA0043: Reconnaissance (偵察)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1596** | Search Open Technical Databases | [R03.4 憑證透明度 CT 探查](../red_team/playbooks/phase_1_recon_surface/R03_domain_namespace_naming/R03.4_certificate_transparency_certificate_reconnaissance.md) | [06.3 HTTP/TLS JA3 指紋檢查](../blue_team/playbooks/phase_0_foundation/06.3_http_tls_ja3_fingerprint.md) | Certificate Transparency Logs | 監控 CAA 記錄與企業憑證簽發告警，定期稽核公網暴露面。 |
| **T1595** | Active Scanning (IP/Port Sweep) | [R05.3 通訊埠狀態列舉驗證](../red_team/playbooks/phase_1_recon_surface/R05_external_technical_exposure/R05.3_port_state_enumeration.md) | [02.1 邊界防火牆精準阻斷](../blue_team/playbooks/phase_2_soc_triage/02.1_border_firewall_surgical_blocking.md) | Zeek `conn.log` / Suricata Alert | 防火牆速率限制 (Rate-limiting)、動態黑名單、封鎖未授權 SYN 探針。 |
| **T1590** | Gather Victim Network Information | [R04.1 IP 與 ASN 邊界拓撲分析](../red_team/playbooks/phase_1_recon_surface/R04_external_infrastructure_ownership/R04.1_ip_asn_netblock_attribution_external_relationship_mapping.md) | [21.2 基礎設施拓撲追蹤](../blue_team/playbooks/phase_4_hunting_ir/21.2_infrastructure_topology_tracking.md) | BGP Routeviews / WHOIS DB | 建立外部資產管理 (EASM) 與 ASN 廣播異動即時警報。 |
| **T1593** | Search Open Websites/Domains | [R02.1 開放網路搜尋引擎偵察](../red_team/playbooks/phase_1_recon_surface/R02_public_digital_footprint/R02.1_open_web_search_engine_reconnaissance.md) | [21.1 CTI 痛苦之塔與 ATT&CK 映射](../blue_team/playbooks/phase_3_detection_eng/21.1_cti_pyramid_of_pain_attck_mapping.md) | MISP / AlienVault OTX | 定期清理過期與廢棄的 API Endpoint，並於 CDN 端收緊敏感路徑存取。 |

---

## TA0042: Resource Development (資源開發)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1587** | Develop Capabilities (Malware/Tool) | [R21.3 Havoc C2 Demon 作戰運用](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.3_havoc_c2_demon_agent_operations.md) | [19.1 PE 結構熵值分析](../blue_team/playbooks/phase_5_deep_dfir/track_e_reverse_mobile/19.1_pe_structure_entropy_packer_analysis.md)<br>[17.1 YARA 惡意特徵比對](../blue_team/playbooks/phase_3_detection_eng/17.1_yara_binary_rules_webshell.md) | YARA / PEiD / ClamAV | 對可疑二進制檔案執行靜態熵值 (Entropy) 檢測與加殼標籤識別。 |
| **T1584** | Compromise Infrastructure | [R23.3 雲端儲存桶列舉與接管](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.3_cloud_storage_bucket_enumeration_takeover.md) | [05.4 S3 儲存桶洩漏防護](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/05.4_s3_bucket_leak_imds_ssrf_defense.md) | AWS CloudTrail / S3 Access Logs | 啟用 S3 Block Public Access、強制使用 KMS 加密與雲端合規監控。 |
| **T1588** | Obtain Capabilities (Exploits) | [R12.1 不安全反序列化物件注入](../red_team/playbooks/phase_2_perimeter_web/R12_serialization_object_binding_state_reconstruction/R12.1_unsafe_deserialization_object_injection.md) | [22.2 Log4Shell 與 N-Day 溯源](../blue_team/playbooks/phase_3_detection_eng/22.2_historical_cve_log4shell_deepdive.md) | WAF Logs / Nginx Access Log | 維護軟體物料清單 (SBOM)，阻絕已知 CVE 與 JNDI/反序列化威脅。 |

---

## TA0001: Initial Access (初始存取)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1190** | Exploit Public-Facing Application | [R10.1 SQL 查詢注入滲透](../red_team/playbooks/phase_2_perimeter_web/R10_interpreter_query_expression_injection/R10.1_sql_query_injection.md)<br>[R11.1 SSRF 伺服器端請求偽造](../red_team/playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/R11.1_server_side_request_forgery.md) | [09.1 Web SQLi 與命令注入防禦](../blue_team/playbooks/phase_1_visibility/09.1_web_sqli_command_injection.md)<br>[16.4 HTTP 走私攻擊防禦](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/16.4_http_request_smuggling_defense.md) | WAF 阻斷日誌 / Web Access Logs | 部署 WAF (OWASP CRS)、啟用 IMDSv2、後端程式碼全面採用參數化查詢 (Prepared Statements)。 |
| **T1566** | Phishing (Spearphishing Attachment) | [R02.2 公開程式碼倉庫情資偵察](../red_team/playbooks/phase_1_recon_surface/R02_public_digital_footprint/R02.2_public_code_repository_reconnaissance.md) | [10.1 郵件認證 SPF/DKIM/DMARC](../blue_team/playbooks/phase_2_soc_triage/10.1_email_auth_spf_dkim_dmarc.md)<br>[10.3 惡意 Office 巨集提取](../blue_team/playbooks/phase_4_hunting_ir/10.3_phishing_macro_extraction.md) | Mail Gateway Logs / OLE Tools | 嚴格落實 DMARC `p=reject`、阻絕未簽章巨集文件、附件動態沙箱引爆。 |
| **T1195** | Supply Chain Compromise | [R01.2 公開人員角色與身分列舉](../red_team/playbooks/phase_1_recon_surface/R01_organization_public_identity/R01.2_public_person_role_email_identity_enumeration.md) | [04.1 軟體供應鏈相依性混淆防禦](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/04.1_supply_chain_dependency_confusion.md)<br>[04.3 CI/CD 機密保護](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/04.3_cicd_pipeline_secret_protection.md) | CI/CD Audit Logs / Git Guardian | 私有套件庫範圍作用域 (Scoping)、CI/CD 敏感環境變數掃描與自動撤銷。 |

---

## TA0002: Execution (執行)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1059.001** | PowerShell Execution | [R21.5 WMI 與 WinRM 無檔案橫向執行](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.5_wmi_winrm_fileless_lateral_execution.md) | [14.3 Windows Event 7045/4688 服務建立](../blue_team/playbooks/phase_1_visibility/14.3_windows_events_7045_4688.md) | Windows Event ID 4104 / 4688 | 啟用 PowerShell ConstrainedLanguage 模式、全域 ScriptBlock 審計與 AMSI 保護。 |
| **T1047** | Windows Management Instrumentation | [R21.5 WMI 與 WinRM 無檔案橫向執行](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.5_wmi_winrm_fileless_lateral_execution.md) | [18.1 Sysmon 行程遙測事件](../blue_team/playbooks/phase_1_visibility/18.1_sysmon_process_telemetry_events.md) | Sysmon Event ID 1 / Event ID 5861 | 阻斷遠端 WMI 呼叫、監控 `__EventConsumer` 建立並限制 DCOM 存取權限。 |
| **T1059.004** | Unix Shell & SUID Abuse | [R18.1 Linux SUID/SGID 二進制濫用](../red_team/playbooks/phase_4_host_privesc/R18_linux_host_privilege_escalation/R18.1_linux_suid_sgid_binary_abuse.md) | [01.1 Linux 驗證 PAM 與 Sudoers](../blue_team/playbooks/phase_0_foundation/01.1_linux_auth_pam_sudoers.md) | Auditd `SYSCALL execve` / `setuid` | 掛載分區使用 `nosuid` 選項、監控 Auditd setuid 系統呼叫、定期清理不必要 Capabilities。 |

---

## TA0003: Persistence (持久化)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1505.003** | Web Shell Persistence | [R11.3 本地檔案包含 LFI 利用](../red_team/playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/R11.3_local_file_inclusion.md) | [20.2 加密 Webshell 檢測](../blue_team/playbooks/phase_4_hunting_ir/20.2_encrypted_webshell_behinder_godzilla.md)<br>[20.1 Java 內存馬溯源](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/20.1_java_memshell_filter_servlet_forensics.md) | Web 日誌 / JVM Arthas Dump | 啟用唯讀容器檔案系統 (Read-only Rootfs)、監控 JVM Class 載入與 YARA 檔案掃描。 |
| **T1053.005** | Scheduled Task Persistence | [R18.5 Linux Crontab 與 Systemd Timer 濫用](../red_team/playbooks/phase_4_host_privesc/R18_linux_host_privilege_escalation/R18.5_linux_crontab_systemd_timer_abuse.md) | [18.3 排程任務常駐追蹤](../blue_team/playbooks/phase_4_hunting_ir/18.3_system_persistence_scheduled_tasks.md)<br>[01.2 Linux Systemd 與 Cron 行程管理](../blue_team/playbooks/phase_0_foundation/01.2_linux_systemd_cron_process.md) | Windows Event ID 4698 / Auditd | 監控排程任務註冊事件 (4698)、比對啟動參數中異常的 `powershell.exe -enc` 或 LOLBAS 二進制。 |
| **T1546.015** | Component Object Model Hijacking | [R19.4 Windows 登錄檔 Mocking 與 UAC 繞過](../red_team/playbooks/phase_4_host_privesc/R19_windows_host_privilege_escalation/R19.4_windows_uac_bypass_registry_mocking.md) | [24.3 註冊表痕跡分析取證](../blue_team/playbooks/phase_5_deep_dfir/track_a_memory_disk/24.3_userassist_shellbags_registry_forensics.md) | Sysmon Event ID 12 / 13 | 監控登錄檔 `HKCU\Software\Classes\CLSID` 寫入行為，比對已知 COM 劫持鍵值。 |

---

## TA0004: Privilege Escalation (權限提升)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1068** | Exploitation for Privilege Escalation | [R18.3 Linux 核心漏洞利用](../red_team/playbooks/phase_4_host_privesc/R18_linux_host_privilege_escalation/R18.3_linux_kernel_vulnerability_exploitation.md) | [25.1 Linux 核心 Rootkit 取證](../blue_team/playbooks/phase_5_deep_dfir/track_e_reverse_mobile/25.1_linux_kernel_lkm_rootkit_forensics.md) | `/var/log/audit/audit.log` | 即時更新 Linux 核心補丁、限制非特權使用者命名空間 (Unprivileged User Namespaces)。 |
| **T1134** | Access Token Manipulation | [R19.2 Windows 權限標記模擬濫用](../red_team/playbooks/phase_4_host_privesc/R19_windows_host_privilege_escalation/R19.2_windows_token_impersonation_privilege_abuse.md) | [14.1 Windows 登入事件 4624/4625](../blue_team/playbooks/phase_1_visibility/14.1_windows_logon_4624_4625.md) | Windows Event ID 4673 / 4624 (Logon Type 9) | 移除服務帳號之 `SeImpersonatePrivilege` 與 `SeAssignPrimaryTokenPrivilege` 權限。 |
| **T1548.002** | Bypass User Account Control | [R19.4 Windows 登錄檔 Mocking 與 UAC 繞過](../red_team/playbooks/phase_4_host_privesc/R19_windows_host_privilege_escalation/R19.4_windows_uac_bypass_registry_mocking.md) | [18.2 LOLBAS 離地攻擊獵捕](../blue_team/playbooks/phase_4_hunting_ir/18.2_lolbas_living_off_the_land.md) | Sysmon Event ID 1 (High Integrity) | 將 UAC 策略設為「始終通知 (Always Notify)」、停用一般使用者的本機管理員群組權限。 |

---

## TA0005: Defense Evasion (防禦規避)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1055** | Process Injection | [R22.1 系統原生呼叫 API 脫鉤規避](../red_team/playbooks/phase_6_evasion_cloud/R22_defense_evasion_endpoint_runtime/R22.1_direct_system_calls_api_unhooking.md)<br>[R22.3 行程挖空注入技術](../red_team/playbooks/phase_6_evasion_cloud/R22_defense_evasion_endpoint_runtime/R22.3_process_injection_hollowing_techniques.md) | [18.4 遠端執行緒注入偵測](../blue_team/playbooks/phase_4_hunting_ir/18.4_process_injection_remote_thread.md)<br>[23.2 VAD 樹與代碼注入分析](../blue_team/playbooks/phase_5_deep_dfir/track_a_memory_disk/23.2_vad_tree_code_injection_malfind.md) | Sysmon Event ID 8 / Volatility `malfind` | 啟用 Windows Defender Exploit Guard (ACG/CIG)、EDR 核心 ETW-Ti 遙測監控。 |
| **T1562.001** | Impair Defenses (AMSI/ETW Patch) | [R22.2 AMSI 與 ETW 記憶體動態修補](../red_team/playbooks/phase_6_evasion_cloud/R22_defense_evasion_endpoint_runtime/R22.2_amsi_etw_in_memory_patching.md) | [14.4 Windows Defender 運作日誌](../blue_team/playbooks/phase_1_visibility/14.4_windows_defender_operational_logs.md) | Sysmon Event ID 10 (ProcessAccess) | 監控對 `amsi.dll` / `ntdll.dll` 之 `PAGE_EXECUTE_READWRITE` 記憶體屬性修改行為。 |
| **T1070.006** | Timestomp File Modifications | [R11.2 檔案路徑遍歷利用](../red_team/playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/R11.2_file_path_traversal.md) | [24.1 NTFS $MFT 時間戳反篡改取證](../blue_team/playbooks/phase_5_deep_dfir/track_a_memory_disk/24.1_ntfs_mft_timestomping_analysis.md) | NTFS `$STANDARD_INFORMATION` vs `$FILE_NAME` | 解析 MFT 雙時間戳差異，比對 USN Journal 與日誌異動記錄。 |

---

## TA0006: Credential Access (憑證存取)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1003.001** | LSASS Memory Dumping | [R19.7 Windows LSASS 記憶體憑證導出](../red_team/playbooks/phase_4_host_privesc/R19_windows_host_privilege_escalation/R19.7_windows_lsass_memory_credential_dumping.md) | [23.4 LSASS 記憶體憑證提取分析](../blue_team/playbooks/phase_5_deep_dfir/track_a_memory_disk/23.4_lsass_memory_credential_extraction.md) | Sysmon Event ID 10 (LSASS Target) | 啟用 LSA RunAsPPL、CredGuard、阻斷非授權行程對 lsass.exe 的存取句柄請求。 |
| **T1558.003** | Kerberoasting | [R07.2 Kerberos 服務票據請求攻擊](../red_team/playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/R07.2_kerberos_service_ticket_roast_material_acquisition.md) | [12.2 SPN Kerberoasting 偵測](../blue_team/playbooks/phase_5_deep_dfir/track_b_active_directory/12.2_spn_kerberoasting_detection.md) | Windows Event ID 4769 (RC4 加密 0x17) | 啟用 AES-256 加密、服務帳戶改用 gMSA (群組受管服務帳戶)、設定 25 字元以上高強度密碼。 |
| **T1558.004** | AS-REP Roasting | [R07.1 AS-REP Roast 素材取得](../red_team/playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/R07.1_as_rep_roast_material_acquisition.md) | [12.1 Kerberos 預認證攻擊偵測](../blue_team/playbooks/phase_5_deep_dfir/track_b_active_directory/12.1_kerberos_preauth_asrep_roasting.md) | Windows Event ID 4768 (無預驗證請求) | 清查並取消所有網域帳戶之「不需要 Kerberos 預先驗證 (DONT_REQ_PREAUTH)」旗標。 |
| **T1003.006** | DCSync (NTDS Dump) | [R16.1 網域目錄憑證複寫導出](../red_team/playbooks/phase_3_domain_dominance/R16_directory_replication_synchronization_semantics/R16.1_directory_credential_replication.md) | [12.4 DCSync NTDS 憑證傾印獵捕](../blue_team/playbooks/phase_5_deep_dfir/track_b_active_directory/12.4_dcsync_ntds_credential_dumping.md) | Windows Event ID 4662 (Replicating Directory Changes) | 嚴格稽核域根節點複寫權限 (DS-Replication-Get-Changes-All)，非 DC IP 呼叫立即產生 P1 警報。 |

---

## TA0007: Discovery (內網探索)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1069** | Permission Groups Discovery | [R08.1 網域關係圖譜收集與標準化](../red_team/playbooks/phase_3_domain_dominance/R08_directory_authorization_delegation_privilege_paths/R08.1_directory_relationship_graph_collection_normalization.md) | [12.5 BloodHound ACL 攻擊路徑防禦](../blue_team/playbooks/phase_5_deep_dfir/track_b_active_directory/12.5_bloodhound_acl_attack_paths.md) | AD LDAP Query Logs (Event ID 1644) | 限制非管理者帳號的大規模 LDAP 查詢速率、部署 LDAP 蜜罐帳號即時觸發告警。 |
| **T1018** | Remote System Discovery | [R05.2 授權主機連通性驗證](../red_team/playbooks/phase_1_recon_surface/R05_external_technical_exposure/R05.2_authorized_host_reachability_validation.md) | [02.2 內網微隔離策略構建](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/02.2_internal_network_microsegmentation.md) | NetFlow / VPC Flow Logs | 實施 Zero Trust 網路微隔離、封鎖橫向跨 VLAN 的任意通訊與 ICMP Ping。 |
| **T1526** | Cloud Service Discovery | [R23.1 雲端 IAM 權限提升與元數據濫用](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.1_cloud_iam_privilege_escalation_metadata_abuse.md) | [05.1 雲端共擔責任模型落地](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/05.1_cloud_shared_responsibility_matrix.md) | AWS CloudTrail (`Describe*` / `List*`) | 監控短時間內大量呼叫 `DescribeInstances` 或 `ListBuckets` 的異常 API 金鑰呼叫。 |

---

## TA0008: Lateral Movement (橫向移動)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1021.002** | SMB/Windows Admin Shares | [R21.5 WMI 與 WinRM 無檔案橫向執行](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.5_wmi_winrm_fileless_lateral_execution.md) | [28.3 多主機橫向移動歸因取證](../blue_team/playbooks/phase_6_capstone/28.3_multi_host_lateral_movement_attribution.md) | Windows Event ID 5140 / 5145 | 端點主機停用 SMBv1、開啟 Windows 防火牆阻絕 445/139 橫向存取、全面啟用 LAPS。 |
| **T1550.002** | Pass the Hash | [R07.3 NTLM Pass-the-Hash 認證攻擊](../red_team/playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/R07.3_ntlm_pass_the_hash_authentication.md)<br>[R07.6 Kerberos TGT 票據偽造](../red_team/playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/R07.6_kerberos_tgt_forgery.md) | [12.3 黃金/白銀票據偽造取證](../blue_team/playbooks/phase_5_deep_dfir/track_b_active_directory/12.3_golden_silver_ticket_forgery.md) | Windows Event ID 4624 (Logon Type 3, NTLM) | 定期（每 180 天）重設兩次 KRBTGT 帳號密碼、部署 Protected Users 群組。 |
| **T1021.006** | Windows Remote Management | [R21.5 WMI 與 WinRM 無檔案橫向執行](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.5_wmi_winrm_fileless_lateral_execution.md) | [14.1 Windows 登入事件 4624/4625](../blue_team/playbooks/phase_1_visibility/14.1_windows_logon_4624_4625.md) | Windows Event ID 4624 (Logon Type 3, Port 5985) | 限制 WinRM 僅允許專用堡壘機 IP 存取、實施多因子認證 (MFA)。 |

---

## TA0009: Collection (情資收集)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1560** | Archive Collected Data | [R19.8 Windows DPAPI 憑證秘密提取](../red_team/playbooks/phase_4_host_privesc/R19_windows_host_privilege_escalation/R19.8_windows_dpapi_secret_extraction.md) | [24.4 VSS 磁碟卷影複製取證](../blue_team/playbooks/phase_5_deep_dfir/track_a_memory_disk/24.4_vss_volume_shadow_copy_forensics.md) | Sysmon Event ID 1 (7z.exe / rar.exe) | 監控壓縮軟體或 `tar` / `gzip` 於非典型目錄下壓縮大批內部文檔之行為。 |
| **T1005** | Data from Local System | [R17.1 證書使用者提供識別資訊濫用](../red_team/playbooks/phase_3_domain_dominance/R17_enterprise_certificate_identity_enrollment_trust/R17.1_enrollee_supplied_identity_certificate_issuance_abuse.md) | [31.1 機敏個資資料外洩鑑識](../blue_team/playbooks/phase_4_hunting_ir/31.1_sensitive_personal_data_protection.md) | DLP Agent Logs / EDR File Auditing | 部署端點 DLP (資料外洩防護)、檔案標籤化管制與敏感資料存取審計。 |

---

## TA0011: Command and Control (指揮控制)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1090** | Proxy & Tunneling | [R20.1 Chisel 反向 SOCKS5 穿透](../red_team/playbooks/phase_5_pivoting_c2/R20_network_tunneling_proxy_pivoting/R20.1_chisel_reverse_socks5_tunneling.md)<br>[R20.2 Ligolo-ng TUN 虛擬穿透](../red_team/playbooks/phase_5_pivoting_c2/R20_network_tunneling_proxy_pivoting/R20.2_ligolo_ng_tun_interface_pivoting.md) | [16.1 DNS 隧道與資料滲出分析](../blue_team/playbooks/phase_2_soc_triage/16.1_dns_tunneling_exfiltration_forensics.md)<br>[07.2 VPN 隧道安全比較分析](../blue_team/playbooks/phase_5_deep_dfir/track_d_network_hardware/07.2_vpn_ipsec_wireguard_security_showdown.md) | Zeek `conn.log` (長期長連接) | 限制內部主機直連外部高埠位 (High Ports)、阻斷未知 WebSocket 與 SSH 隧道特徵。 |
| **T1071.001** | Web Protocols (C2 Beaconing) | [R21.1 Sliver C2 框架部署與作戰運用](../red_team/playbooks/phase_5_pivoting_c2/R21_command_and_control_infrastructure/R21.1_sliver_c2_framework_deployment_operation.md) | [16.2 C2 信標週期性抖動分析](../blue_team/playbooks/phase_2_soc_triage/16.2_c2_beaconing_jitter_analysis.md) | Web Proxy / Zeek `http.log` | 透過 SPL 計算時間間隔變異係數 (Coefficient of Variation)、阻絕高信標關聯 IP。 |
| **T1048** | Exfiltration Over Alternative Protocol | [R23.1 雲端 IAM 權限提升與元數據濫用](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.1_cloud_iam_privilege_escalation_metadata_abuse.md) | [05.1 雲端共擔責任模型落地](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/05.1_cloud_shared_responsibility_matrix.md) | AWS GuardDuty / VPC Flow Logs | 啟用 GuardDuty 偵測異常憑證向外呼叫行為，強制要求 VPC Endpoint 與安全群組邊界。 |

---

## TA0010: Exfiltration (資料外洩)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1048.003** | Exfiltration Over Unencrypted Non-C2 Protocol | [R20.5 DNS 與 ICMP 隱蔽隧道穿透](../red_team/playbooks/phase_5_pivoting_c2/R20_network_tunneling_proxy_pivoting/R20.5_dns_icmp_covert_tunneling.md) | [06.2 DNS 隧道與 DGA 檢測](../blue_team/playbooks/phase_0_foundation/06.2_dns_tunneling_dga.md) | Bind / Windows DNS Query Logs | 限制內網主機直連外部 Public DNS、部署 DNS 封包深度檢驗 (DPI) 阻絕異常長子網域。 |
| **T1567** | Exfiltration Over Web Service | [R23.1 雲端 IAM 權限提升與元數據濫用](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.1_cloud_iam_privilege_escalation_metadata_abuse.md) | [05.2 雲端 IAM 權限提升獵捕](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/05.2_cloud_iam_privilege_escalation.md) | CloudTrail `PutObject` / `AssumeRole` | 啟用 IAM 最小權限 (Principle of Least Privilege)、強制執行 SCP 邊界與跨帳號防護。 |

---

## TA0040: Impact (作戰破壞與影響)

| ATT&CK ID | 戰術與技術名稱 | 🔴 紅隊特戰手冊 | 🔵 藍隊防禦偵測手冊 | 關鍵遙測來源 (Telemetry) | 防禦緩解與偵測工程策略 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1499** | Endpoint Denial of Service | [R13.1 HTTP 請求走私與脫步利用](../red_team/playbooks/phase_2_perimeter_web/R13_application_message_framing_routing_intermediary_semantics/R13.1_http_request_smuggling_desynchronization.md) | [02.3 核心 NGFW 與 Suricata 聯防](../blue_team/playbooks/phase_3_detection_eng/02.3_ngfw_ips_suricata_inline.md) | Suricata Drop Logs / CPU 監控 | 部署負載平衡反向代理、啟用 Rate Limit、禁止 XML 外部實體解析 (Disallow DOCTYPE)。 |
| **T1485** | Data Destruction / Ransom | [R23.4 Docker Socket 宿主機逃逸](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.4_docker_socket_host_mount_escape.md)<br>[R23.5 K8s RBAC 提權與機密導出](../red_team/playbooks/phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/R23.5_kubernetes_rbac_privilege_escalation_secrets_dumping.md) | [05.3 容器逃逸與 K8s 執行期防禦](../blue_team/playbooks/phase_5_deep_dfir/track_c_cloud_supplychain/05.3_container_escape_k8s_runtime_defense.md)<br>[25.3 雲原生 eBPF 威脅檢測 Falco](../blue_team/playbooks/phase_5_deep_dfir/track_e_reverse_mobile/25.3_cloud_native_ebpf_threat_detection_falco.md) | Falco Alert (`docker.sock open`) | 嚴禁掛載宿主機 `/var/run/docker.sock`、開啟 AppArmor/SELinux、強制 non-root 容器執行。 |

---

## 🔄 閉環演練驗證與實踐資源

在進行實際紫隊對抗演練時，可透過以下自動化與模擬工具進行雙軌驗收：

1. ⚡ **[27.1 Atomic Red Team 自動化對抗演練](../blue_team/playbooks/phase_6_capstone/27.1_automated_adversary_emulation_atomic_red_team.md)**：單點原子測試，精準模擬各項 ATT&CK 技術。
2. 🎭 **[27.2 MITRE Caldera 自動化對抗平台](../blue_team/playbooks/phase_6_capstone/27.2_automated_adversary_emulation_platform_caldera.md)**：編排完整駭客攻擊鏈，評估端點遙測覆蓋率。
3. 🗺️ **[27.3 紫隊協同實務與 ATT&CK Navigator 熱圖閉環](../blue_team/playbooks/phase_6_capstone/27.3_purple_teaming_practice_attack_navigator.md)**：量化防禦成熟度，匯出 JSON Layer。
