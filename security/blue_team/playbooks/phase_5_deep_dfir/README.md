# Phase 5: 深度數位鑑識與記憶體/磁碟溯源手冊 (Deep DFIR & Forensics Playbooks)

> **定位**：本階段手冊聚焦硬核數位鑑識（DFIR），包含 Volatility 3 記憶體鏡像逆推、NTFS $MFT 與 USN Journal 磁碟鐵證、Linux 內核 Rootkit 深度分析、以及 RFC 3227 / ISO 27037 證據監管鏈。

### 相關學習指引與規範
- 記憶體鑑識路徑：[block_6_dfir_memory_disk/23_memory_forensics.md](../../learning_paths/block_6_dfir_memory_disk/23_memory_forensics.md)
- 磁碟鑑識路徑：[block_6_dfir_memory_disk/24_disk_filesystem_forensics.md](../../learning_paths/block_6_dfir_memory_disk/24_disk_filesystem_forensics.md)
- 撰寫標準規範：[PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md](../PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md)

---

- [23.1_volatility_hidden_process_dkom.md](23.1_volatility_hidden_process_dkom.md)：隱藏進程與 DKOM 斷鏈破譯 (Volatility 3 / EPROCESS ActiveProcessLinks)
- [23.2_vad_tree_code_injection_malfind.md](23.2_vad_tree_code_injection_malfind.md)：VAD 樹與記憶體程式碼注入分析 (Virtual Address Descriptors & Code Injection)
- [23.3_memory_netscan_binary_dump.md](23.3_memory_netscan_binary_dump.md)：核心網路連線還原與二進位導出 (Memory Netscan & Binary Dump)
- [23.4_lsass_memory_credential_extraction.md](23.4_lsass_memory_credential_extraction.md)：記憶體憑證抓取與暫存區取證 (LSASS Memory Credential Extraction & Clipboard Forensics)
- [24.1_ntfs_mft_timestomping_analysis.md](24.1_ntfs_mft_timestomping_analysis.md)：NTFS 主檔案表與時間戳偽造 ($MFT & Timestomping Analysis)

