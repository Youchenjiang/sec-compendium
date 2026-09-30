# 🕸️ Active Directory 圖論路徑、DACL 委派濫用與 GPO 劫持深度學習路徑 (AD ACL & GPO)
> 對應紅隊作戰矩陣：**Phase 3 (R08)** (R08.1 ~ R08.5)  
> 預計總投入時間：**35 ~ 40 小時**（視 Windows 安全描述元、Active Directory DACL 與圖論演算法基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會用 net user /domain 查帳號 ──►   精通 BloodHound 圖論最短提權路徑分析與 Cypher 查詢
看不懂 Windows DACL / ACE    ──►   精通 GenericAll, WriteDacl, ForceChangePassword 鏈
拿到低權限帳號無法進展       ──►   精通 GPO 惡意排程派送與全網批次橫向感染
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| Windows 安全描述元 (Security Descriptor) | 深入理解 SID, Owner, DACL, SACL 與 ACE 結構 | [Microsoft Learn: 安全描述項與存取控制](https://learn.microsoft.com/windows/win32/secauthz/security-descriptors) |
| 圖論最短路徑 (Dijkstra / BFS) | 理解節點 (Nodes)、邊緣 (Edges) 與加權路徑遍歷 | [BloodHound GUI & Cypher Cheatsheet](https://bloodhound.specterops.io/) |
| 網域群組原則 (Group Policy) 機制 | 熟悉 SYSVOL 共享、GPO GUID、排程任務與客戶端擴展 (CSE) | [Microsoft Learn: 群組原則架構](https://learn.microsoft.com/previous-versions/windows/it-pro/) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
圖譜採集標準化 最短攻擊路徑   操作員群組濫用 DACL委派權限   GPO惡意劫持
(6h)           (8h)           (6h)           (10h)          (8h)
```

---

## 🩸 階段一：目錄物件關聯圖譜採集與標準化 (BloodHound)（約 6 小時）

### 1.1 採集工具鏈 (SharpHound / BloodHound.py)
在網域內任意已加入域的主機上，普通網域使用者預設對 LDAP 具有唯讀權限：
```bash
# 透過 Linux 平台 BloodHound.py 進行非侵入式全域採集
bloodhound-python -u user -p password -d domain.local -ns 192.168.1.10 -c All --zip
```
產出的 JSON 檔案包含：`users.json`, `groups.json`, `computers.json`, `domains.json`, `gpos.json`, `ous.json`。

---

## 🧭 階段二：目錄特權圖譜最短攻擊路徑分析（約 8 小時）

### 2.1 Neo4j Cypher 查詢高價值邊界
將資料導入 Neo4j 資料庫後，使用圖論查詢語言定位跳板：
```cypher
// 查詢當前擁有的低特權帳號至 Domain Admins 的最短攻擊路徑
MATCH (m:User {name:'LOW_USER@DOMAIN.LOCAL'}), (n:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'}), p=shortestPath((m)-[r*]->(n))
RETURN p
```

---

## 👥 階段三：目錄高特權內建操作員群組濫用（約 6 小時）

### 3.1 表面不是 Admin、實則具備破壞力的特權群組
- **Backup Operators / Server Operators**：
  具備備份檔案系統權限，可直接繞過檔案 DACL 讀取 `C:\Windows\NTDS\ntds.dit` 與 `SYSTEM` 註冊表登錄檔！
- **DnsAdmins**：
  可配置 DNS 伺服器的 `ServerLevelPluginDll`，讓 DC 上的 DNS 服務載入任意惡意 DLL 獲取 SYSTEM 權限！

---

## 🔑 階段四：目錄物件存取控制清單 (DACL) 委派濫用（約 10 小時）

### 4.1 四大天王 ACE 提權語意
| ACE 權限類型 | 攻擊者掌握此權限時的突防打擊路徑 |
| :--- | :--- |
| **GenericAll** | 對目標物件擁有完全控制權，可直接修改物件密碼、添加群組成員 |
| **WriteDacl** | 可任意修改目標物件的存取控制清單，為自己授予 `GenericAll` |
| **WriteOwner** | 可將目標物件的擁有者變更為自己，進而取得 `WriteDacl` 權限 |
| **ForceChangePassword** | 無需知曉舊密碼，直接透過 RPC/LDAP 強制重設目標使用者密碼 |

```bash
# 利用 PowerView 為受害帳號強行重設密碼
Set-DomainUserPassword -Identity "TargetAdmin" -AccountPassword "P@ssw0rd2026!"
```

---

## 📜 階段五：網域群組原則物件 (GPO) 控制權濫用與惡意部署（約 8 小時）

### 5.1 GPO 惡意策略即時注入
若攻擊者對某個鏈結至所有工作站或 DC 的 GPO 物件擁有寫入權限：
1. 透過 `SharpGPOAbuse` 向 GPO 添加一個即時啟動的排程工作 (Scheduled Task) 或本機管理員群組成員。
2. 全域電腦每 90 分鐘（DC 為 5 分鐘）會自動從 SYSVOL 同步該 GPO 並強制執行：
   ```bash
   SharpGPOAbuse.exe --AddComputerTask --TaskName "SyncTask" --Author "NT AUTHORITY\SYSTEM" --Command "powershell.exe" --Arguments "-enc <payload>" --GPOName "Default Domain Policy"
   ```

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能使用 SharpHound 或 BloodHound.py 正確收集全域物件拓撲。
- [ ] 熟練編寫 Cypher 語句定位最短提權路徑。
- [ ] 能利用 Backup Operators 權限導出網域 SAM/SYSTEM 登錄檔。
- [ ] 掌握對 GenericAll / WriteDacl 權限對象的提權利用步驟。
- [ ] 熟練使用 SharpGPOAbuse 進行惡意策略注入與全網橫向擴展。
