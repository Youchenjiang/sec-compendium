# Phase 5: 深度數位鑑識與記憶體/磁碟溯源手冊 (Deep DFIR & Forensics Playbooks)

> **定位**：本階段手冊聚焦硬核數位鑑識（DFIR），包含 Volatility 3 記憶體鏡像逆推、NTFS $MFT 與 USN Journal 磁碟鐵證、Linux 內核 Rootkit 深度分析、以及 RFC 3227 / ISO 27037 證據監管鏈。

### 相關學習指引與規範
- 記憶體鑑識路徑：[block_6_dfir_memory_disk/23_memory_forensics.md](../../learning_paths/block_6_dfir_memory_disk/23_memory_forensics.md)
- 磁碟鑑識路徑：[block_6_dfir_memory_disk/24_disk_filesystem_forensics.md](../../learning_paths/block_6_dfir_memory_disk/24_disk_filesystem_forensics.md)
- 撰寫標準規範：[PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md](../PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md)

---

### 📑 實戰手冊分流目錄

#### 💾 Track A: 記憶體與磁碟數位鑑識專精 (8 項)
- [23.1_volatility_hidden_process_dkom.md](track_a_memory_disk/23.1_volatility_hidden_process_dkom.md)：隱藏進程與 DKOM 斷鏈破譯 (Volatility 3 / EPROCESS ActiveProcessLinks)
- [23.2_vad_tree_code_injection_malfind.md](track_a_memory_disk/23.2_vad_tree_code_injection_malfind.md)：VAD 樹與記憶體程式碼注入分析 (Virtual Address Descriptors & Code Injection)
- [23.3_memory_netscan_binary_dump.md](track_a_memory_disk/23.3_memory_netscan_binary_dump.md)：核心網路連線還原與二進位導出 (Memory Netscan & Binary Dump)
- [23.4_lsass_memory_credential_extraction.md](track_a_memory_disk/23.4_lsass_memory_credential_extraction.md)：記憶體憑證抓取與暫存區取證 (LSASS Memory Credential Extraction & Clipboard Forensics)
- [24.1_ntfs_mft_timestomping_analysis.md](track_a_memory_disk/24.1_ntfs_mft_timestomping_analysis.md)：NTFS 主檔案表與時間戳偽造 ($MFT & Timestomping Analysis)
- [24.2_windows_execution_prefetch_amcache.md](track_a_memory_disk/24.2_windows_execution_prefetch_amcache.md)：程式執行三大鐵證深度鑑識 (Prefetch, ShimCache & Amcache)
- [24.3_userassist_shellbags_registry_forensics.md](track_a_memory_disk/24.3_userassist_shellbags_registry_forensics.md)：使用者活動軌跡與登錄檔鑑識 (UserAssist, ShellBags & Registry Forensics)
- [24.4_vss_volume_shadow_copy_forensics.md](track_a_memory_disk/24.4_vss_volume_shadow_copy_forensics.md)：系統更新日誌與陰影複製取證 (Volume Shadow Copy Forensics & Event Log Recovery)

#### 🏰 Track B: AD 網域攻防與身分治理專精 (8 項)
- [12.1_kerberos_preauth_asrep_roasting.md](track_b_active_directory/12.1_kerberos_preauth_asrep_roasting.md)：Kerberos 預驗證弱點與 AS-REP Roasting 攻防 (Kerberos Pre-Auth & AS-REP Roasting)
- [12.2_spn_kerberoasting_detection.md](track_b_active_directory/12.2_spn_kerberoasting_detection.md)：SPN 服務票據請求與 Kerberoasting 偵測 (SPN Tickets & Kerberoasting Detection)
- [12.3_golden_silver_ticket_forgery.md](track_b_active_directory/12.3_golden_silver_ticket_forgery.md)：偽造票據攻擊與全域特權維持 (Golden & Silver Ticket Forgery Detection)
- [12.4_dcsync_ntds_credential_dumping.md](track_b_active_directory/12.4_dcsync_ntds_credential_dumping.md)：目錄複寫服務特權與 DCSync 憑證傾印偵測 (DCSync & NTDS.dit Credential Extraction)
- [12.5_bloodhound_acl_attack_paths.md](track_b_active_directory/12.5_bloodhound_acl_attack_paths.md)：AD 物件權限濫用與 BloodHound 攻擊路徑阻斷 (BloodHound ACL Attack Paths & Remediation)
- [13.1_oauth2_saml_token_abuse.md](track_b_active_directory/13.1_oauth2_saml_token_abuse.md)：雲端與現代身分驗證協定濫用 (OAuth 2.0 & SAML Token Abuse)
- [13.2_mfa_fatigue_bypass_defense.md](track_b_active_directory/13.2_mfa_fatigue_bypass_defense.md)：多因素驗證疲勞轟炸與即時中間人釣魚防禦 (MFA Fatigue & AiTM Phishing Defense)
- [13.3_service_account_prt_abuse.md](track_b_active_directory/13.3_service_account_prt_abuse.md)：服務帳號權限濫用與 Azure AD PRT 權杖劫持防護 (Service Account & Primary Refresh Token Abuse)

#### ☁️ Track C: 雲原生、供應鏈與無檔案專精
- [02.2_internal_network_microsegmentation.md](track_c_cloud_supplychain/02.2_internal_network_microsegmentation.md)：內部網路微隔離與 VLAN 存取控制 (Internal Network Microsegmentation)
- [04.1_supply_chain_dependency_confusion.md](track_c_cloud_supplychain/04.1_supply_chain_dependency_confusion.md)：開源依賴投毒與相依性混淆防護 (Supply Chain Dependency Confusion)
- [04.2_sbom_vulnerability_management.md](track_c_cloud_supplychain/04.2_sbom_vulnerability_management.md)：軟體物料清單 (SBOM) 審查與自動化弱點追蹤 (SBOM Analysis & Vulnerability Tracking)
- [04.3_cicd_pipeline_secret_protection.md](track_c_cloud_supplychain/04.3_cicd_pipeline_secret_protection.md)：CI/CD 自動化管道審計與密鑰外洩防範 (CI/CD Pipeline Security & Secret Protection)
- [05.1_cloud_shared_responsibility_matrix.md](track_c_cloud_supplychain/05.1_cloud_shared_responsibility_matrix.md)：雲端運算共同責任模型實務與邊界劃分 (Cloud Security Shared Responsibility Matrix)
- [05.2_cloud_iam_privilege_escalation.md](track_c_cloud_supplychain/05.2_cloud_iam_privilege_escalation.md)：雲端多租戶 IAM 提權與 CloudTrail 審計日誌研判 (Cloud IAM Privilege Escalation)
- [05.3_container_escape_k8s_runtime_defense.md](track_c_cloud_supplychain/05.3_container_escape_k8s_runtime_defense.md)：容器逃逸機制與 Kubernetes 運行時威脅防禦 (Container Escape & K8s Runtime Security)
- [05.4_s3_bucket_leak_imds_ssrf_defense.md](track_c_cloud_supplychain/05.4_s3_bucket_leak_imds_ssrf_defense.md)：雲端儲存桶外洩與中繼資料 (IMDS) 劫持防護 (S3 Bucket Leaks & IMDSv2 SSRF Defense)
- [16.4_http_request_smuggling_defense.md](track_c_cloud_supplychain/16.4_http_request_smuggling_defense.md)：協定走私與反向代理混淆鑑識 (HTTP Request Smuggling & Reverse Proxy Desync)
- [20.1_java_memshell_filter_servlet_forensics.md](track_c_cloud_supplychain/20.1_java_memshell_filter_servlet_forensics.md)：Java 內存馬清剿與 Filter/Servlet 運行時取證 (Java Memory Shell Forensics)
- [20.3_dotnet_php_fileless_memshell.md](track_c_cloud_supplychain/20.3_dotnet_php_fileless_memshell.md)：.NET 與 PHP 內存馬與無檔案後門排查 (DotNet & PHP Fileless Memory Shell Defense)

#### 🔌 Track D: 網路通訊設備與硬體安全專精 (8 項)
- [03.1_switch_port_security_errdisable.md](track_d_network_hardware/03.1_switch_port_security_errdisable.md)：交換機連接埠安全與 MAC 違規處置 (Switch Port-Security & Errdisable Recovery)
- [03.2_vlan_tagging_trunk_hopping_defense.md](track_d_network_hardware/03.2_vlan_tagging_trunk_hopping_defense.md)：VLAN 標記結構與 Trunk 跳躍攻擊防禦 (IEEE 802.1Q VLAN Tagging & Double-Tagging Defense)
- [03.3_stp_bpdu_guard_dhcp_snooping.md](track_d_network_hardware/03.3_stp_bpdu_guard_dhcp_snooping.md)：交換機鏈路防護與生成樹安全 (BPDU Guard, Root Guard & DHCP Snooping)
- [07.1_snmpv3_security_authpriv_hardening.md](track_d_network_hardware/07.1_snmpv3_security_authpriv_hardening.md)：SNMP 版本安全演進與 v3 authPriv 實踐 (SNMPv3 Security & authPriv Hardening)
- [07.2_vpn_ipsec_wireguard_security_showdown.md](track_d_network_hardware/07.2_vpn_ipsec_wireguard_security_showdown.md)：企業級 VPN 協定對決與 IPsec/WireGuard 防禦 (Enterprise VPN Protocols IPsec & WireGuard)
- [08.1_wifi_80211_four_way_handshake_analysis.md](track_d_network_hardware/08.1_wifi_80211_four_way_handshake_analysis.md)：802.11 四向握手鑑識與 EAPOL 重播攻擊分析 (802.11 4-Way Handshake & EAPOL Forensics)
- [08.2_wifi_wpa3_sae_dragonfly_defense.md](track_d_network_hardware/08.2_wifi_wpa3_sae_dragonfly_defense.md)：Wi-Fi WPA3 SAE 密鑰交換防禦與 KRACK 重裝攻擊獵捕 (WPA3 SAE Dragonfly & KRACK Defense)
- [11.3_crypto_ciphersuite_downgrade_pfs.md](track_d_network_hardware/11.3_crypto_ciphersuite_downgrade_pfs.md)：傳輸加密密鑰套件降級防禦與前向保密性實踐 (Cipher Suite Downgrade & Perfect Forward Secrecy)

#### 🔬 Track E: 逆向、核心與行動鑑識專精 (10 項)
- [19.1_pe_structure_entropy_packer_analysis.md](track_e_reverse_mobile/19.1_pe_structure_entropy_packer_analysis.md)：PE 結構逆推、區段屬性鑑識與資訊熵 (Shannon Entropy) 檢測 (PE Header & Shannon Entropy Analysis)
- [19.2_code_deobfuscation_string_decryption.md](track_e_reverse_mobile/19.2_code_deobfuscation_string_decryption.md)：程式碼混淆還原、動態字串解密與 FLOSS / x64dbg 實戰 (Code Deobfuscation & Dynamic String Decryption)
- [19.3_malicious_office_macro_ole_extraction.md](track_e_reverse_mobile/19.3_malicious_office_macro_ole_extraction.md)：文件型惡意巨集深度逆推、內嵌 OLE 物件與 Shellcode 萃取 (Malicious Office Macro & Embedded OLE Extraction)
- [25.1_linux_kernel_lkm_rootkit_forensics.md](track_e_reverse_mobile/25.1_linux_kernel_lkm_rootkit_forensics.md)：Linux 核心模組 (LKM) Rootkit 偵測、Syscall Hooking 與斷鏈隱蔽取證 (Linux Kernel LKM Rootkits & Syscall Hooking)
- [25.2_user_space_shared_library_preload_hijacking.md](track_e_reverse_mobile/25.2_user_space_shared_library_preload_hijacking.md)：用戶態動態庫劫持 (LD_PRELOAD) 鑑識、readdir 隱形後門與記憶體排查 (LD_PRELOAD Shared Library Hijacking)
- [25.3_cloud_native_ebpf_threat_detection_falco.md](track_e_reverse_mobile/25.3_cloud_native_ebpf_threat_detection_falco.md)：雲原生 eBPF 核心級威脅偵測、Falco 運行時防護與容器邊界防禦 (Cloud-native eBPF & Falco Runtime Defense)
- [25.4_linux_memory_acquisition_lime_volatility.md](track_e_reverse_mobile/25.4_linux_memory_acquisition_lime_volatility.md)：Linux 實體記憶體採集 (LiME)、核心符號表 (ISF) 還原與 Volatility 3 深度鑑識 (Linux Memory Acquisition & ISF Symbol Tables)
- [26.1_android_apk_malware_static_decompilation.md](track_e_reverse_mobile/26.1_android_apk_malware_static_decompilation.md)：Android APK 惡意行為逆向、靜態解包與 Manifest 權限鑑識 (Android APK Static Decompilation & Manifest Forensics)
- [26.2_android_runtime_logs_sqlite_forensics.md](track_e_reverse_mobile/26.2_android_runtime_logs_sqlite_forensics.md)：Android 系統執行時日誌 (Logcat)、ADB 取證與沙盒 SQLite 資料庫鑑識 (Android Runtime Logs & Sandbox SQLite Forensics)
- [26.3_ios_backup_forensics_keychain_extraction.md](track_e_reverse_mobile/26.3_ios_backup_forensics_keychain_extraction.md)：iOS 備份檔案深度取證、Manifest.db 索引逆推與鑰匙圈 (Keychain) 敏感憑證萃取 (iOS Backup Forensics & Keychain Extraction)
