# 🔴 紅隊 17 領域與 70 個核心實戰技術索引 (Red Team Tactical Catalog)

> 本清單匯整自標準架構，完整保留 17 個作戰領域與 70 項攻擊技術點，並依照「紅隊三大作戰階段 (Phase 1 ~ Phase 3)」進行分層導覽，作為實戰操作之標準索引。

---

## 🌐 Phase 1: 外部情報與資產暴露面 (Recon & Attack Surface)

### 📁 R01_organization_public_identity
- **路徑**：`playbooks/phase_1_recon_surface/R01_organization_public_identity/`
- **R01.1_organization_structure_business_relationship_mapping.md**：組織架構與商業關係測繪
- **R01.2_public_person_role_email_identity_enumeration.md**：公開人員職能與公務電子郵件枚舉

### 📁 R02_public_digital_footprint
- **路徑**：`playbooks/phase_1_recon_surface/R02_public_digital_footprint/`
- **R02.1_open_web_search_engine_reconnaissance.md**：開放網路與搜尋引擎情資偵察
- **R02.2_public_code_repository_reconnaissance.md**：公開程式碼倉庫與敏感資訊洩漏偵察

### 📁 R03_domain_namespace_naming
- **路徑**：`playbooks/phase_1_recon_surface/R03_domain_namespace_naming/`
- **R03.1_whois_rdap_domain_registry_intelligence.md**：WHOIS 與 RDAP 網域名稱註冊情資
- **R03.2_authoritative_dns_record_enumeration.md**：權威 DNS 資源紀錄枚舉
- **R03.3_passive_historical_dns_intelligence.md**：被動與歷史 DNS 解析情資偵察
- **R03.4_certificate_transparency_certificate_reconnaissance.md**：憑證透明度日誌與 TLS 憑證情資偵察
- **R03.5_dns_candidate_hostname_discovery.md**：DNS 候選主機名稱字典枚舉

### 📁 R04_external_infrastructure_ownership
- **路徑**：`playbooks/phase_1_recon_surface/R04_external_infrastructure_ownership/`
- **R04.1_ip_asn_netblock_attribution_external_relationship_mapping.md**：IP、ASN 與網段歸屬測繪
- **R04.2_cdn_edge_ownership_scope_disambiguation.md**：CDN 與邊緣節點歸屬與真實 IP 辨析

### 📁 R05_external_technical_exposure
- **路徑**：`playbooks/phase_1_recon_surface/R05_external_technical_exposure/`
- **R05.1_internet_scan_database_exposure_intelligence.md**：網際網路掃描資料庫暴露情資
- **R05.2_authorized_host_reachability_validation.md**：授權目標主機存活性驗證
- **R05.3_port_state_enumeration.md**：通訊埠開放狀態枚舉
- **R05.4_service_protocol_fingerprint_validation.md**：服務與應用層通訊協定指紋識別
- **R05.5_web_virtual_host_discovery.md**：Web 虛擬主機 (Virtual Host) 發現
- **R05.6_web_content_path_discovery.md**：Web 目錄與路徑模糊測試
- **R05.7_version_configuration_vulnerability_correlation.md**：軟體版本與配置弱點關聯分析
- **R05.8_safe_remote_vulnerability_condition_checking.md**：遠端弱點存在條件無害驗證

---

## 🎯 Phase 2: 邊界打點與 Web/API 突破 (Perimeter & Web Exploitation)

### 📁 R06_credential_secret_recovery_guessing_reuse
- **路徑**：`playbooks/phase_2_perimeter_web/R06_credential_secret_recovery_guessing_reuse/`
- **R06.1_offline_password_hash_cracking.md**：離線密碼雜湊破解與規則攻擊
- **R06.2_online_password_guessing.md**：線上服務密碼猜解與鎖定機制探測
- **R06.3_password_spraying.md**：外網低頻密碼噴灑攻擊實施
- **R06.4_known_credential_reuse_credential_stuffing.md**：已知洩漏憑證重用與撞庫攻擊

### 📁 R09_application_authentication_session_authorization_state
- **路徑**：`playbooks/phase_2_perimeter_web/R09_application_authentication_session_authorization_state/`
- **R09.1_application_session_token_forgery.md**：應用程式 Session Token 偽造與簽章破壞
- **R09.2_application_session_fixation_adoption.md**：應用程式 Session Fixation 攻擊實施
- **R09.3_broken_object_level_authorization.md**：物件層級存取控制失效 (BOLA / IDOR) 利用
- **R09.4_broken_function_level_authorization.md**：功能層級存取控制失效 (BFLA) 越權利用
- **R09.5_authentication_session_replay_bypass.md**：認證工作階段重放與防護繞過

### 📁 R10_interpreter_query_expression_injection
- **路徑**：`playbooks/phase_2_perimeter_web/R10_interpreter_query_expression_injection/`
- **R10.1_sql_query_structure_injection.md**：SQL 查詢語法樹破壞與注入利用
- **R10.2_operating_system_command_interpreter_injection.md**：作業系統命令直譯器注入突破
- **R10.3_server_side_template_expression_injection.md**：伺服器端模板引擎表示式注入 (SSTI)

### 📁 R11_server_side_resource_backend_trust
- **路徑**：`playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/`
- **R11.1_server_side_request_forgery.md**：伺服器端請求偽造 (SSRF) 與內網穿透
- **R11.2_file_path_traversal_arbitrary_file_read.md**：檔案路徑穿越與任意檔案讀取
- **R11.3_local_file_inclusion.md**：本機檔案包含 (LFI) 漏洞利用
- **R11.4_remote_file_inclusion.md**：遠端檔案包含 (RFI) 漏洞利用

### 📁 R12_serialization_object_binding_state_reconstruction
- **路徑**：`playbooks/phase_2_perimeter_web/R12_serialization_object_binding_state_reconstruction/`
- **R12.1_insecure_deserialization_object_injection.md**：不安全反序列化與物件注入攻擊
- **R12.2_xml_external_entity_processing_abuse.md**：XML 外部實體 (XXE) 解析機制濫用
- **R12.3_mass_assignment_object_binding_abuse.md**：物件自動綁定濫用 (Mass Assignment)

### 📁 R13_application_message_framing_routing_intermediary_semantics
- **路徑**：`playbooks/phase_2_perimeter_web/R13_application_message_framing_routing_intermediary_semantics/`
- **R13.1_http_request_smuggling_message_framing_abuse.md**：HTTP 請求走私與訊息長度邊界混淆
- **R13.2_web_cache_poisoning_routing_manipulation.md**：Web 快取投毒與中繼節點路由操控
- **R13.3_host_forwarded_header_routing_trust_abuse.md**：Host 與 Forwarded 標頭路由信任濫用

### 📁 R14_browser_cross_origin_trust
- **路徑**：`playbooks/phase_2_perimeter_web/R14_browser_cross_origin_trust/`
- **R14.1_reflected_cross_site_scripting.md**：反射型跨站腳本 (Reflected XSS) 實施
- **R14.2_stored_cross_site_scripting.md**：儲存型跨站腳本 (Stored XSS) 與持久化劫持
- **R14.3_dom_based_cross_site_scripting.md**：DOM 型跨站腳本 (DOM XSS) 資料流污點利用
- **R14.4_cross_site_request_forgery.md**：跨站請求偽造 (CSRF) 與非預期動作強制觸發
- **R14.5_cross_origin_resource_sharing_trust_abuse.md**：跨來源資源共用 (CORS) 信任配置濫用

### 📁 R15_application_workflow_business_logic_integrity
- **路徑**：`playbooks/phase_2_perimeter_web/R15_application_workflow_business_logic_integrity/`
- **R15.1_workflow_state_transition_bypass.md**：業務工作流程狀態機躍遷驗證繞過
- **R15.2_business_action_replay_idempotency_abuse.md**：業務操作重放與冪等性機制破壞
- **R15.3_application_race_condition_concurrency_abuse.md**：應用程式併發競態條件 (Race Condition) 濫用

---

## 👑 Phase 3: 企業身分與 AD 網域統治 (Domain Dominance & Identity)

### 📁 R07_enterprise_authentication_protocol_ticket_semantics
- **路徑**：`playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/`
- **R07.1_as_rep_roast_material_acquisition.md**：Kerberos AS-REP Roasting 憑證素材獲取
- **R07.2_kerberos_service_ticket_roast_material_acquisition.md**：Kerberos 服務票證 (Kerberoasting) 獲取
- **R07.3_ntlm_pass_the_hash_authentication.md**：NTLM Pass-the-Hash 雜湊傳遞認證實施
- **R07.4_kerberos_tgt_replay.md**：Kerberos TGT 票證重放 (Pass-the-Ticket) 實施
- **R07.5_kerberos_service_ticket_replay.md**：Kerberos 服務票證 (ST) 重放攻擊實施
- **R07.6_kerberos_tgt_forgery.md**：Kerberos 黃金票據 (Golden Ticket) 偽造實施
- **R07.7_kerberos_service_ticket_forgery.md**：Kerberos 白銀票據 (Silver Ticket) 偽造實施

### 📁 R08_directory_authorization_delegation_privilege_paths
- **路徑**：`playbooks/phase_3_domain_dominance/R08_directory_authorization_delegation_privilege_paths/`
- **R08.1_directory_relationship_graph_collection_normalization.md**：目錄物件關聯圖譜採集與標準化 (BloodHound)
- **R08.2_directory_privilege_graph_path_analysis.md**：目錄特權圖譜最短攻擊路徑分析
- **R08.3_directory_group_membership_state_validation.md**：目錄高特權內建操作員群組濫用驗證
- **R08.4_directory_acl_delegated_right_state_validation.md**：目錄物件存取控制清單 (DACL) 委派權限濫用
- **R08.5_group_policy_object_control_abuse.md**：網域群組原則物件 (GPO) 控制權濫用與惡意部署

### 📁 R16_directory_replication_synchronization_semantics
- **路徑**：`playbooks/phase_3_domain_dominance/R16_directory_replication_synchronization_semantics/`
- **R16.1_directory_credential_replication.md**：目錄認證資訊複製 (DCSync) 攻擊實施
- **R16.2_rogue_directory_replication_state_injection.md**：惡意網域控制站目錄狀態注入 (DCShadow)

### 📁 R17_enterprise_certificate_identity_enrollment_trust
- **路徑**：`playbooks/phase_3_domain_dominance/R17_enterprise_certificate_identity_enrollment_trust/`
- **R17.1_enrollee_supplied_identity_certificate_issuance_abuse.md**：申請者指定主體別名憑證頒發濫用 (ESC1)
- **R17.2_over_permissive_certificate_purpose_eku_issuance_abuse.md**：過度寬鬆憑證增強金鑰用法濫用 (ESC2)
- **R17.3_enrollment_agent_on_behalf_of_certificate_issuance_abuse.md**：註冊代理憑證代表申請機制濫用 (ESC3)
- **R17.4_certificate_template_issuance_policy_modification.md**：憑證範本存取控制脆弱性修改與濫用 (ESC4)
- **R17.5_ca_wide_request_attribute_san_issuance_policy_abuse.md**：CA 全域請求屬性 SAN 頒發策略濫用 (ESC6)
- **R17.6_certificate_request_approval_disposition_authority_abuse.md**：憑證註冊審查管理權限脆弱性濫用 (ESC7)
- **R17.7_enterprise_certificate_authentication_trust_anchor_manipulation.md**：憑證信任鏈錨點操縱與惡意憑證注入
