# ⚔️ 紅隊原子實戰手冊庫 (Red Team Atomic Playbooks)

> 🎯 **本目錄宗旨**：  
> 告別死板教科書與零散筆記！本目錄**嚴格依照 Phase 1 ➔ Phase 6 作戰階段**，收錄 **110 篇標準化原子實戰手冊（Runbooks / Playbooks）**。  
> 每一篇手冊皆嚴格遵循「特戰速查規範」，提供：**案發現場破題 ➔ 實戰操作（第一動至第五動）➔ 靶場實戰 ➔ 過關驗收閉環**。

---

## 📜 撰寫規範與品質準則

所有手冊的編寫與審查，**必須且唯一依循以下標準文件**：  
👉 **[PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md](PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md)**

### 核心不可逾越鐵律：
1. **五動敘事流**：每篇手冊必備「🚨 案發現場破題 ➔ 🧩 第一動：核心機制 ➔ 🧭 第二動：目標辨識 ➔ 💻 第三動：現場攻堅 ➔ ⚖️ 第四動：防守特徵 ➔ 🛡️ 第五動：處置加固 ➔ 🎯 靶場實戰 ➔ 📋 三題過關驗收」。
2. **三欄式語意速查表**：攻擊步驟 / 執行目標 | 作戰指令 / 構造載荷 | 預期現象 / 成功特徵。
3. **特戰速查精準篇幅**：控制在 160 ~ 190 行高密度精煉篇幅，拒絕多餘空話，提供立即可執行的生產級指令。

---

## 📂 Phase 階段手冊目錄與索引

### [phase_1_recon_surface/](phase_1_recon_surface/) —— 外部情報與資產暴露面 (19 篇)
- **[R01_organization_public_identity/](phase_1_recon_surface/R01_organization_public_identity/)** (2 篇)
  - R01.1_organization_structure_business_relationship_mapping.md：R01.1 組織實體架構與商業關係拓撲對齊
  - R01.2_public_person_role_email_identity_enumeration.md：R01.2 公開人員角色、職能與電子郵件身分列舉
- **[R02_public_digital_footprint/](phase_1_recon_surface/R02_public_digital_footprint/)** (2 篇)
  - R02.1_open_web_search_engine_reconnaissance.md：R02.1 開放網路搜尋引擎偵察與進階 Dorking 語法
  - R02.2_public_code_repository_reconnaissance.md：R02.2 公開程式碼儲存庫機密情報探勘
- **[R03_domain_namespace_naming/](phase_1_recon_surface/R03_domain_namespace_naming/)** (5 篇)
  - R03.1_whois_rdap_domain_registry_intelligence.md：R03.1 網域名稱註冊資訊與 RDAP/WHOIS 實體情報關聯
  - R03.2_authoritative_dns_record_enumeration.md：R03.2 權威 DNS 資源記錄列舉與區域傳送驗證
  - R03.3_passive_historical_dns_intelligence.md：R03.3 被動與歷史 DNS 解析情資反查
  - R03.4_certificate_transparency_certificate_reconnaissance.md：R03.4 憑證透明度日誌與 TLS 憑證情資檢索
  - R03.5_dns_candidate_hostname_discovery.md：R03.5 DNS 候選主機名暴力列舉與規律推導
- **[R04_external_infrastructure_ownership/](phase_1_recon_surface/R04_external_infrastructure_ownership/)** (2 篇)
  - R04.1_ip_asn_netblock_attribution_external_relationship_mapping.md：R04.1 網際網路 IP、ASN 與網段歸屬關係對齊
  - R04.2_cdn_edge_ownership_scope_disambiguation.md：R04.2 CDN 邊緣節點歸屬與真實源站界限釐清
- **[R05_external_technical_exposure/](phase_1_recon_surface/R05_external_technical_exposure/)** (8 篇)
  - R05.1_internet_scan_database_exposure_intelligence.md：R05.1 網際網路掃描資料庫曝險情報檢索
  - R05.2_authorized_host_reachability_validation.md：R05.2 授權目標主機可達性驗證與存活探測
  - R05.3_port_state_enumeration.md：R05.3 傳輸層通訊埠狀態列舉與邊界過濾分析
  - R05.4_service_protocol_fingerprint_validation.md：R05.4 服務協定與版本指紋精確識別
  - R05.5_web_virtual_host_discovery.md：R05.5 Web 虛擬主機與主機標頭路由探測
  - R05.6_web_content_path_discovery.md：R05.6 Web 目錄路徑與敏感端點發現
  - R05.7_version_configuration_vulnerability_correlation.md：R05.7 軟體版本與組態缺陷漏洞關聯分析
  - R05.8_safe_remote_vulnerability_condition_checking.md：R05.8 遠端弱點條件安全驗證與非破壞性探針

---

### [phase_2_perimeter_web/](phase_2_perimeter_web/) —— 邊界打點與 Web/API 突破 (30 篇)
- **[R06_credential_secret_recovery_guessing_reuse/](phase_2_perimeter_web/R06_credential_secret_recovery_guessing_reuse/)** (4 篇)
  - R06.1_offline_password_hash_cracking.md：R06.1 離線密碼雜湊破解與運算資源最佳化
  - R06.2_online_password_guessing.md：R06.2 線上服務密碼定向猜測與通道探測
  - R06.3_password_spraying.md：R06.3 橫向密碼噴灑與低頻率帳號鎖定規避
  - R06.4_known_credential_reuse_credential_stuffing.md：R06.4 外洩憑證撞庫與已知憑證跨域重用
- **[R09_application_authentication_session_authorization_state/](phase_2_perimeter_web/R09_application_authentication_session_authorization_state/)** (5 篇)
  - R09.1_application_session_state_forgery_validation_bypass.md：R09.1 應用程式會話狀態偽造與校驗繞過
  - R09.2_session_fixation.md：R09.2 應用程式會話固定與預先綁定劫持
  - R09.3_object_level_authorization_bypass.md：R09.3 物件層級存取控制失效與水平越權
  - R09.4_function_level_authorization_bypass.md：R09.4 功能層級存取控制失效與垂直越權
  - R09.5_application_session_replay_control_bypass.md：R09.5 應用程式會話重放控制繞過
- **[R10_interpreter_query_expression_injection/](phase_2_perimeter_web/R10_interpreter_query_expression_injection/)** (3 篇)
  - R10.1_sql_query_injection.md：R10.1 SQL 查詢表達式結構注入
  - R10.2_os_command_shell_injection.md：R10.2 作業系統命令與 Shell 解譯器語法注入
  - R10.3_server_side_template_injection.md：R10.3 伺服器端範本解譯引擎注入
- **[R11_server_side_resource_backend_trust/](phase_2_perimeter_web/R11_server_side_resource_backend_trust/)** (4 篇)
  - R11.1_server_side_request_forgery.md：R11.1 伺服器端請求偽造
  - R11.2_file_path_traversal.md：R11.2 路徑遍歷與檔案讀取機制解析
  - R11.3_local_file_inclusion.md：R11.3 本地檔案包含機制與安全防禦分析
  - R11.4_remote_file_inclusion.md：R11.4 遠端檔案包含與跨網路資源信任機制分析
- **[R12_serialization_object_binding_state_reconstruction/](phase_2_perimeter_web/R12_serialization_object_binding_state_reconstruction/)** (3 篇)
  - R12.1_unsafe_deserialization_object_injection.md：R12.1 不安全反序列化與物件注入機制分析
  - R12.2_xml_external_entity_processing_abuse.md：R12.2 XML 外部實體注入與處理機制分析
  - R12.3_mass_assignment_unsafe_object_binding.md：R12.3 批量賦值與不安全物件綁定機制分析
- **[R13_application_message_framing_routing_intermediary_semantics/](phase_2_perimeter_web/R13_application_message_framing_routing_intermediary_semantics/)** (3 篇)
  - R13.1_http_request_smuggling_desynchronization.md：R13.1 HTTP 請求走私與反向代理去同步化機制分析
  - R13.2_web_cache_poisoning_cache_key_normalization_confusion.md：R13.2 網頁快取投毒與快取鍵正規化混淆機制分析
  - R13.3_host_forwarded_header_routing_origin_selection_trust_abuse.md：R13.3 主機與轉發標頭路由與源站選擇信任濫用分析
- **[R14_browser_cross_origin_trust/](phase_2_perimeter_web/R14_browser_cross_origin_trust/)** (5 篇)
  - R14.1_reflected_cross_site_scripting.md：R14.1 反射型跨站腳本攻擊機制與防禦分析
  - R14.2_stored_cross_site_scripting.md：R14.2 儲存型跨站腳本攻擊機制與防禦分析
  - R14.3_dom_based_cross_site_scripting.md：R14.3 DOM 型跨站腳本攻擊機制與防禦分析
  - R14.4_cross_site_request_forgery.md：R14.4 跨站請求偽造機制與防禦分析
  - R14.5_cross_origin_resource_sharing_trust_abuse.md：R14.5 跨來源資源共享
- **[R15_application_workflow_business_logic_integrity/](phase_2_perimeter_web/R15_application_workflow_business_logic_integrity/)** (3 篇)
  - R15.1_workflow_state_transition_bypass.md：R15.1 工作流與狀態機跳躍繞過分析
  - R15.2_business_action_replay_idempotency_abuse.md：R15.2 業務操作重放與等冪性控制濫用分析
  - R15.3_application_race_condition_concurrency_abuse.md：R15.3 應用層競態條件與併發控制濫用分析

---

### [phase_3_domain_dominance/](phase_3_domain_dominance/) —— 企業身分與 AD 網域統治 (21 篇)
- **[R07_enterprise_authentication_protocol_ticket_semantics/](phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/)** (7 篇)
  - R07.1_as_rep_roast_material_acquisition.md：R07.1 Kerberos AS-REP 雜湊材料收割
  - R07.2_kerberos_service_ticket_roast_material_acquisition.md：R07.2 Kerberos 服務票證雜湊收割與離線破解
  - R07.3_ntlm_pass_the_hash_authentication.md：R07.3 NTLM 雜湊傳遞認證與身分橫向移動
  - R07.4_kerberos_tgt_replay.md：R07.4 Kerberos 認證票證重放與票證傳遞
  - R07.5_kerberos_service_ticket_replay.md：R07.5 Kerberos 服務票證重放與目標資源劫持
  - R07.6_kerberos_tgt_forgery.md：R07.6 Kerberos 認證票證離線偽造與黃金票證
  - R07.7_kerberos_service_ticket_forgery.md：R07.7 Kerberos 服務票證離線偽造與白銀票證
- **[R08_directory_authorization_delegation_privilege_paths/](phase_3_domain_dominance/R08_directory_authorization_delegation_privilege_paths/)** (5 篇)
  - R08.1_directory_relationship_graph_collection_normalization.md：R08.1 目錄服務關聯圖譜採集與正規化
  - R08.2_directory_privilege_graph_path_analysis.md：R08.2 目錄特權躍遷圖譜路徑分析
  - R08.3_directory_group_membership_state_validation.md：R08.3 目錄群組成員資格狀態驗證與特權濫用
  - R08.4_directory_acl_delegated_right_state_validation.md：R08.4 目錄存取控制清單與委派權限狀態驗證
  - R08.5_group_policy_object_control_abuse.md：R08.5 群組原則物件控制權濫用與全域程式碼派發
- **[R16_directory_replication_synchronization_semantics/](phase_3_domain_dominance/R16_directory_replication_synchronization_semantics/)** (2 篇)
  - R16.1_directory_credential_replication.md：R16.1 目錄服務憑證同步複製機制分析
  - R16.2_rogue_directory_replication_state_injection.md：R16.2 偽造目錄複寫狀態注入分析
- **[R17_enterprise_certificate_identity_enrollment_trust/](phase_3_domain_dominance/R17_enterprise_certificate_identity_enrollment_trust/)** (7 篇)
  - R17.1_enrollee_supplied_identity_certificate_issuance_abuse.md：R17.1 申請者自訂主體名稱
  - R17.2_over_permissive_certificate_purpose_eku_issuance_abuse.md：R17.2 過寬憑證用途與任意用途
  - R17.3_enrollment_agent_on_behalf_of_certificate_issuance_abuse.md：R17.3 憑證註冊代理人代簽發機制濫用分析
  - R17.4_certificate_template_issuance_policy_modification.md：R17.4 憑證範本發行原則與 ACL 覆寫濫用分析
  - R17.5_ca_wide_request_attribute_san_issuance_policy_abuse.md：R17.5 全 CA 級請求屬性 SAN 簽發原則濫用分析
  - R17.6_certificate_request_approval_disposition_authority_abuse.md：R17.6 憑證簽發審批與處置管理權限濫用分析
  - R17.7_enterprise_certificate_authentication_trust_anchor_manipulation.md：R17.7 企業憑證身分信任錨點操縱與金憑證分析

---

### [phase_4_host_privesc/](phase_4_host_privesc/) —— 主機立足與本地提權 (14 篇)
- **[R18_linux_host_privilege_escalation/](phase_4_host_privesc/R18_linux_host_privilege_escalation/)** (6 篇)
  - R18.1_linux_suid_sgid_binary_abuse.md：R18.1 Linux SUID/SGID 特權二進位與 GTFOBins 濫用
  - R18.2_linux_sudoers_misconfiguration_abuse.md：R18.2 Linux Sudo 授權弱點與環境變數劫持利用
  - R18.3_linux_kernel_vulnerability_exploitation.md：R18.3 Linux 核心漏洞提權與 Dirty Pipe 實施
  - R18.4_linux_capabilities_privilege_abuse.md：R18.4 Linux Capabilities 特權原語濫用
  - R18.5_linux_crontab_systemd_timer_abuse.md：R18.5 Linux 排程任務 Crontab 與 Systemd 定時器萬用字元提權
  - R18.6_linux_nfs_no_root_squash_abuse.md：R18.6 Linux 網路檔案系統 NFS no_root_squash 特權掛載提權
- **[R19_windows_host_privilege_escalation/](phase_4_host_privesc/R19_windows_host_privilege_escalation/)** (8 篇)
  - R19.1_windows_service_configuration_abuse.md：R19.1 Windows 服務權限缺陷與未加引號路徑提權
  - R19.2_windows_token_impersonation_privilege_abuse.md：R19.2 Windows 權杖模擬與 SeImpersonatePotato 濫用
  - R19.3_windows_always_install_elevated_abuse.md：R19.3 Windows 登錄檔 AlwaysInstallElevated MSI 提權
  - R19.4_windows_uac_bypass_registry_mocking.md：R19.4 Windows UAC 繞過與無憑證提示提升
  - R19.5_windows_dll_hijacking_search_order.md：R19.5 Windows DLL 尋址順序劫持與已知 DLL 替換
  - R19.6_windows_sam_system_hive_dumping.md：R19.6 Windows SAM 與 SYSTEM 註冊表登錄檔離線雜湊提取
  - R19.7_windows_lsass_memory_credential_dumping.md：R19.7 Windows LSASS 記憶體憑證導出與防禦規避
  - R19.8_windows_dpapi_secret_extraction.md：R19.8 Windows 數據保護介面 DPAPI 憑證與瀏覽器密碼解密

---

### [phase_5_pivoting_c2/](phase_5_pivoting_c2/) —— 內網橫向與穿透代理 (13 篇)
- **[R20_network_tunneling_proxy_pivoting/](phase_5_pivoting_c2/R20_network_tunneling_proxy_pivoting/)** (7 篇)
  - R20.1_chisel_reverse_socks5_tunneling.md：R20.1 Chisel 反向 SOCKS5 隧道與 HTTP 穿透
  - R20.2_ligolo_ng_tun_interface_pivoting.md：R20.2 Ligolo-ng TUN 虛擬網卡多層次代理跳板
  - R20.3_ssh_dynamic_forwarding_proxychains.md：R20.3 SSH 動態轉發與 Proxychains 多級跳板
  - R20.4_frp_high_performance_reverse_proxy.md：R20.4 FRP 高性能多協議內網穿透與埠轉發
  - R20.5_dns_icmp_covert_tunneling.md：R20.5 DNS 與 ICMP 隱蔽隧道穿透受限網路
  - R20.6_socat_netsh_port_forwarding_redirection.md：R20.6 Socat 與 Netsh PortProxy 雙向流量轉發與重定向
  - R20.7_smb_named_pipe_pivoting.md：R20.7 SMB 命名管道隧道穿越完全隔離子網域
- **[R21_command_and_control_infrastructure/](phase_5_pivoting_c2/R21_command_and_control_infrastructure/)** (6 篇)
  - R21.1_sliver_c2_framework_deployment_operation.md：R21.1 Sliver C2 現代跨平台控制架構部署與操作
  - R21.2_malleable_c2_profile_traffic_obfuscation.md：R21.2 Malleable C2 流量特徵自定義與 CDN 隱蔽重定向
  - R21.3_havoc_c2_demon_agent_operations.md：R21.3 Havoc C2 現代化跨平台框架與 Demon Agent 實戰作戰
  - R21.4_c2_sleep_mask_obfuscation.md：R21.4 C2 記憶體休眠混淆與呼叫堆疊欺騙
  - R21.5_wmi_winrm_fileless_lateral_execution.md：R21.5 WMI 與 WinRM 無檔案橫向移動與遠端執行
  - R21.6_rdp_session_hijacking_shadowing.md：R21.6 RDP 會話劫持與 Shadow 隱蔽無感監控

---

### [phase_6_evasion_cloud/](phase_6_evasion_cloud/) —— 防禦規避與前沿環境攻防 (13 篇)
- **[R22_defense_evasion_endpoint_runtime/](phase_6_evasion_cloud/R22_defense_evasion_endpoint_runtime/)** (8 篇)
  - R22.1_direct_system_calls_api_unhooking.md：R22.1 直接系統調用 Direct Syscalls 與 EDR 鉤子繞過
  - R22.2_amsi_etw_in_memory_patching.md：R22.2 AMSI 與 ETW 記憶體動態修補繞過
  - R22.3_process_injection_hollowing_techniques.md：R22.3 進程鏤空 Process Hollowing 與隱蔽注入實施
  - R22.4_early_bird_apc_queue_injection.md：R22.4 Early Bird APC 佇列非同步注入技術
  - R22.5_parent_pid_spoofing_command_line_argument_mocking.md：R22.5 父進程 ID
  - R22.6_peruns_fart_disk_dll_unhooking.md：R22.6 Perun's Fart 磁碟純淨 DLL 重載與 API 脫鉤技術
  - R22.7_shellcode_encoding_uuid_mac_formatting.md：R22.7 Shellcode 格式混淆與 UUID/MAC/IPv4 位址編碼
  - R22.8_windows_defender_tampering_exclusion_abuse.md：R22.8 Windows Defender 篡改保護機制與排除路徑濫用
- **[R23_cloud_container_infrastructure_exploitation/](phase_6_evasion_cloud/R23_cloud_container_infrastructure_exploitation/)** (5 篇)
  - R23.1_cloud_iam_privilege_escalation_metadata_abuse.md：R23.1 雲端 IAM 權限提升與中繼資料憑證濫用
  - R23.2_kubernetes_container_escape_cluster_compromise.md：R23.2 Kubernetes 特權容器逃逸與叢集控制權獲取
  - R23.3_cloud_storage_bucket_enumeration_takeover.md：R23.3 雲端儲存桶枚舉、權限配置失誤與子域名接管
  - R23.4_docker_socket_host_mount_escape.md：R23.4 Docker Socket 掛載濫用與容器主機逃逸
  - R23.5_kubernetes_rbac_privilege_escalation_secrets_dumping.md：R23.5 Kubernetes RBAC 權限提升與全叢集 Secrets 轉儲

---
