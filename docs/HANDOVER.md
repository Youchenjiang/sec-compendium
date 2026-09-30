# 📋 紅隊作戰體系建置工程：跨對話交接文件 (Project Handover Document)

> **交接地點**：`docs/HANDOVER.md`  
> **建立時間**：2026-09-30  
> **交接對象**：接手本專案的下一任 AI 助理 / 開發工程師  
> **核心任務**：接續執行紅隊進攻體系（Red Team Offensive Knowledge Base）的三大缺口補齊任務。

---

## 🧭 一、 當前專案狀態與 Git 基準線

* **工作目錄**：`c:\Users\LabStrix\Documents\GitHub\Youchen\Security\red-team-curriculum`
* **當前分支**：`feature/red-team-curriculum`（Working Tree 100% Clean）
* **遠端追蹤**：未推送到 `origin`（本機歷史包含 46 個完整 Commits）
* **最近 4 個原子化提交（已嚴格解耦，遵循 SRP 單一責任原則）**：
  * `70c65ef test(tools): introduce automated validation test suite for red team playbooks`
  * `5647e6a docs(index): update red team catalog and READMEs with Phase structure`
  * `c55038b docs(curriculum): establish Red Team operational curriculum roadmap`
  * `225d237 refactor(taxonomy): migrate playbooks into Phase 1 to Phase 3 operational directories`

---

## 🏛️ 二、 已完成之架構與成果盤點

### 1. 70 篇原子實戰手冊（100% 撰寫完畢並完成 Phase 階層重構）
全量 70 篇手冊已全數重寫為「特戰速查版」（篇幅 160 ~ 190 行，總計 12,223 行，平均 174 行/篇），並歸入三大作戰階段：
* **`security/knowledge/red_team/playbooks/phase_1_recon_surface/`（19 篇）**：
  * R01 (組織架構與人員情報 - 2 篇)
  * R02 (公開數位足跡 - 2 篇)
  * R03 (域名與 DNS 命名空間 - 5 篇)
  * R04 (外部網路基礎設施歸屬 - 2 篇)
  * R05 (外部技術暴露驗證 - 8 篇)
* **`security/knowledge/red_team/playbooks/phase_2_perimeter_web/`（30 篇）**：
  * R06 (憑證秘密恢復、噴灑與撞庫 - 4 篇)
  * R09 (身分驗證與 Session 狀態 - 5 篇)
  * R10 (直譯器與語法注入 SQLi/Cmdi/SSTI - 3 篇)
  * R11 (伺服端資源信任 SSRF/LFI/RFI - 4 篇)
  * R12 (物件反序列化與 XXE - 3 篇)
  * R13 (訊息封裝與走私 Smuggling - 3 篇)
  * R14 (瀏覽器同源策略信任 XSS/CSRF/CORS - 5 篇)
  * R15 (業務工作流與併發競態 - 3 篇)
* **`security/knowledge/red_team/playbooks/phase_3_domain_dominance/`（21 篇）**：
  * R07 (企業身分協定與票據 Kerberos/NTLM/Golden/Silver - 7 篇)
  * R08 (目錄授權與 ACL 提權路徑 BloodHound/GPO - 5 篇)
  * R16 (目錄複製與同步原語 DCSync/DCShadow - 2 篇)
  * R17 (企業憑證服務 AD CS / ESC1~ESC8 - 7 篇)

> 💡 **註：彻底解決了先前的「AD 夾心」歷史包袱**。原 R07/R08 與 R16/R17 已在 `phase_3` 完美合體，形成完整 21 篇 Active Directory 網域攻防專案。

### 2. 配套核心導覽文件
* **`career_curriculum.md`**：現代紅隊通關主線課表（Phase 1 ~ Phase 6 全景作戰鏈、Core 25 篇 / Specialization 32 篇 / Advanced 13 篇能力分流）。
* **`RED_TEAM_TECHNIQUES_CATALOG.md`**：17 領域、70 項技術點的標準命名與檔案對照表。
* **`README.md`**：紅隊知識庫頂層入口，與藍隊（`security/knowledge/blue_team/`）達到 1:1 對稱。
* **`security/tools/validate_red_team_playbooks.py`**：自動化品質稽核腳本。執行指令 `python security/tools/validate_red_team_playbooks.py`，當前測試結果：**100% 通過（70/70 合規）**。

---

## 🎯 三、 下一任助理的核心待辦清單（三大缺口補齊任務）

用戶明確指示需依序解決以下「三大缺口」：

### 📌 缺口 1：重構 `security/knowledge/red_team/index.md`
* **問題現況**：現有 `index.md` 仍為舊版 16 領域 50 項技術點，與已完成的 70 篇手冊脫節。
* **執行任務**：
  1. 參考藍隊 [`security/knowledge/blue_team/index.md`](../security/knowledge/blue_team/index.md) 的格局。
  2. 將其升級為**「三大作戰階段、17 大領域、70 項實戰技術點」的完整終極矩陣表**。
  3. 矩陣必須包含：`難度分級 (🟢 L1 ~ 👑 L4)` | `領域與技術編號 (R01.1 ~ R17.7)` | `實戰技術點名稱` | `🎯 具體免費用線上靶場/真實環境清單`（精選 PortSwigger、HTB Starting Point / Sherlocks、picoCTF、GOAD、SadServers 等 100% 免費資源）。
  4. 同時在表末保留 **Phase 4 ~ Phase 6 的前瞻架構規劃**。
* **Git 規範**：單獨提交一個 Commit：`docs(index): update red team master skills and lab matrix to 70 techniques`。

### 📌 缺口 2：建構 `security/knowledge/red_team/learning_paths/` 深度自學體系
* **問題現況**：該目錄目前僅有 `README.md` 與 `.gitkeep`，缺乏系統性的原理概念教學。
* **執行任務**：
  1. 比照藍隊 [`security/knowledge/blue_team/learning_paths/`](../security/knowledge/blue_team/learning_paths/) 的 Block 資料夾結構，建立對應區塊：
     * `block_1_recon_surface/`（外部情報、網路空間測繪與暴露面）
     * `block_2_perimeter_web/`（Web 漏洞底層機制、直譯器與訊息語意）
     * `block_3_domain_dominance/`（Active Directory 協定、Kerberos 深入與 AD CS 信任鏈）
  2. 撰寫代表性的深入自學指南，必須包含：「你在哪裡、去哪裡」、「第零關必備基礎」、「整體學習地圖」、「各階段深入剖析」與「通過檢查表」。
* **Git 規範**：每個 Block 或模組獨立進行原子化提交。

### 📌 缺口 3：正式規劃並落地 Phase 4 ~ Phase 6 實戰擴充槽位
* **問題現況**：目前實戰手冊僅完成 Phase 1 ~ Phase 3，完整的紅隊作戰光譜尚缺後段。
* **執行任務**：
  1. 在 `playbooks/` 下建立三個新資料夾：
     * `phase_4_host_privesc/`（主機立足與本地提權：Linux SUID/Sudo、Windows Token/SeImpersonate/Service 提權）
     * `phase_5_pivoting_c2/`（內網橫向與穿透：Chisel/Ligolo-ng 隧道代理、Sliver/Havoc C2 基礎設施）
     * `phase_6_evasion_cloud/`（防禦規避與雲原生：EDR Syscall 繞過、AMSI/ETW Patching、K8s 容器逃逸）
  2. 依據 [`PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md`](../security/knowledge/red_team/playbooks/PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md) 規格，編寫高質量原子實戰手冊。
* **Git 規範**：每完成一個 Phase 或領域，進行嚴格的原子化提交。

---

## ⚠️ 四、 不可逾越之工程守則

1. **嚴格原子化提交（Atomic Commits）**：
   * **禁止巨石型打包**！絕對不可將「目錄搬移」、「文件更新」、「工具測試」混在同一個 Commit。
   * 每個 Commit 必須具備單一且明確的職責（`refactor:` / `docs:` / `test:` / `feat:`）。
2. **手冊格式鐵律**：
   * 繁體中文撰寫。
   * 特戰速查標準：控制在 160 ~ 190 行高密度精煉篇幅。
   * 必備關鍵字：`🎯 作戰任務破題`、`第一動` 至 `第五動`、`實戰`、`驗收`。
3. **驗證指令強制執行**：
   * 每次手冊更新或目錄調整後，必須執行驗證腳本：
     ```bash
     python security/tools/validate_red_team_playbooks.py
     ```
   * 必須確保 100% 通過（0 Errors），方可執行 Git Commit。
