# Phase 6: 紫隊全真演習與企業級 Cyber Range 頂石專題 (Capstone & Purple Teaming)

> **定位**：本階段手冊聚焦跨維度實網對抗、紫隊協同驗證（Atomic Red Team）、企業級網路靶場演練、以及重大國家級資安事件實體推演。

### 相關學習指引與規範
- 紫隊演習路徑：[block_7_purple_team_range/27_purple_team_breach_simulation.md](../../learning_paths/block_7_purple_team_range/27_purple_team_breach_simulation.md)
- 網路靶場路徑：[block_7_purple_team_range/28_enterprise_cyber_range.md](../../learning_paths/block_7_purple_team_range/28_enterprise_cyber_range.md)
- 實體真題庫：[security/practice/exams/](../../../../practice/exams/README.md)

---

### 📑 實戰手冊目錄 (全 7 項)

- [27.1_automated_adversary_emulation_atomic_red_team.md](27.1_automated_adversary_emulation_atomic_red_team.md)：自動化對抗測試 (Atomic Red Team)、防禦遙測評估與日誌捕獲閉環
- [27.2_automated_adversary_emulation_platform_caldera.md](27.2_automated_adversary_emulation_platform_caldera.md)：自動化對抗模擬平台 (MITRE Caldera) 拓撲部署與自主滲透演練
- [27.3_purple_teaming_practice_attack_navigator.md](27.3_purple_teaming_practice_attack_navigator.md)：紫隊協同實務 (Purple Teaming) 與 ATT&CK Navigator 防禦覆蓋熱圖閉環
- [28.1_end_to_end_apt_attack_chain_ctf.md](28.1_end_to_end_apt_attack_chain_ctf.md)：端到端 APT 攻擊鏈全局溯源、多階威脅取證與 CTF 奪旗閉環
- [28.2_large_scale_enterprise_bots_dataset.md](28.2_large_scale_enterprise_bots_dataset.md)：大規模企業級實網攻防資料集 (Splunk BOTS) 深度研判與實戰奪旗
- [28.3_multi_host_lateral_movement_attribution.md](28.3_multi_host_lateral_movement_attribution.md)：跨主機橫向移動鏈路拓撲重組、多源跡證融合與攻擊組織歸因
- [28.4_taiwan_cybersecurity_competition_exam_triage.md](28.4_taiwan_cybersecurity_competition_exam_triage.md)：台灣資安法規遵從、關鍵基礎設施通報與資安競賽實體檢定 (金盾獎)

---

### 🏰 Phase 6 專屬實體攻防靶場 (Turnkey Cyber Ranges)

本階段配套之 Docker Compose 一鍵啟動實體靶場已收納於 [`ranges/`](ranges/README.md)：
1. [`ranges/01_atomic_purple_range/`](ranges/01_atomic_purple_range/README.md)：對接 `27.1`、`27.2` 之 Caldera 紫隊對抗靶場。
2. [`ranges/02_splunk_bots_range/`](ranges/02_splunk_bots_range/README.md)：對接 `28.2` 之 OpenSearch / Splunk BOTS 企業獵捕靶場。
3. [`ranges/03_apt_cross_domain_ctf/`](ranges/03_apt_cross_domain_ctf/README.md)：對接 `28.1`、`28.3` 之 3-Tier APT 跨網段奪旗靶場。

