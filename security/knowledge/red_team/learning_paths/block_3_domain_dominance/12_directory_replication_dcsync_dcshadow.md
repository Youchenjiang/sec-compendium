# 🧬 DRSUAPI 目錄複製原語、DCSync 與 DCShadow 注入深度學習路徑 (DCSync & DCShadow)
> 對應紅隊作戰矩陣：**Phase 3 (R16)** (R16.1 ~ R16.2)  
> 預計總投入時間：**30 ~ 35 小時**（視 MS-DRSR 協定、MS-KILE、RPC 介面與網域底層架構基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
以為抓 Hash 一定要登入 DC 本機 ──►     精通 DRSUAPI RPC 協定遠端模擬 DC 導出全域 Hash
只知道 secretsdump 工具怎麼跑  ──►     精通 DS-Replication 特權 ACE 檢驗與修補
被藍隊 SIEM 監控所有提權日誌  ──►     精通 DCShadow 惡意暫態 DC 注入達成「零日誌」特權修改
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| MS-DRSR 目錄複製服務遠端協定 | 理解 DC 之間同步資料的 RPC 介面與 DRSUAPI 呼叫 | [Microsoft Learn: MS-DRSR Protocol](https://learn.microsoft.com/openspecs/windows_protocols/ms-drsr/) |
| 網域根目錄複寫權限 (Replication Rights) | 熟悉 `DS-Replication-Get-Changes` 與 `DS-Replication-Get-Changes-All` | [Microsoft Learn: 複寫權限說明](https://learn.microsoft.com/windows/win32/ad/granting-extended-rights) |
| Active Directory 結構化資料庫 (ntds.dit) | 理解 ESE/JET 資料庫引擎、欄位結構與 PEK 加密金鑰 | [NTDS.dit 物理結構剖析](https://adsecurity.org/) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
DRSUAPI協定本質 DCSync特權判定 DCSync實戰導出 DCShadow架構   零日誌注入防禦
(6h)           (6h)           (8h)           (8h)           (5h)
```

---

## 🏛️ 階段一：MS-DRSR 目錄複製服務協定物理原理解析（約 6 小時）

### 1.1 網域控制站資料同步機制
在多台網域控制站 (Domain Controllers) 環境中，每當有使用者修改密碼或物件變更時，DC 之間透過 DRSUAPI (RPC UUID: `e3514235-4b06-11d1-ab04-00c04fc2dcd2`) 發送 `IDL_DRSGetNCChanges` 請求進行增量同步。
- 只要具有相應的「複寫延伸特權」，任何端點都可以**「假裝自己是一台合法的網域控制站」**，向主 DC 要求將包括 `krbtgt` 在內的所有帳號雜湊完整複製過來！

---

## 🔑 階段二：DCSync 特權判斷與最小化授權（約 6 小時）

### 2.1 觸發 DCSync 必須滿足的 ACE 條件
發起端帳號必須在網域根物件（Domain Root）上擁有以下兩項特定延伸權限 (Extended Rights)：
1. `DS-Replication-Get-Changes` (GUID: `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`)
2. `DS-Replication-Get-Changes-All` (GUID: `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2`)
預設僅 Domain Admins, Enterprise Admins, Domain Controllers 與 Read-Only Domain Controllers 具備此權限。

---

## ⚡ 階段三：DCSync 實戰導出與全域憑證萃取（約 8 小時）

### 3.1 Impacket secretsdump 實戰指令
無需登入 DC、無需將任何二進位檔上傳至 DC 端點，完全基於網路 RPC 通訊完成導出：
```bash
# 遠端萃取網域 krbtgt 帳號 Hash（用於製作黃金票據）
impacket-secretsdump -just-dc-user krbtgt domain.local/admin_user:password@192.168.1.10

# 批次萃取全網域所有帳號與電腦 Hash
impacket-secretsdump domain.local/admin_user:password@192.168.1.10 -outputfile domain_hashes
```

---

## 🥷 階段四：惡意網域控制站目錄狀態注入 (DCShadow)（約 8 小時）

### 4.1 DCShadow 的物理本質：偽造暫態 DC
DCSync 是「唯讀拉取」，而 DCShadow 是**「主動寫入推送」**！
- 傳統修改 AD 屬性（如將使用者加入 Domain Admins）會產生 Windows Event ID 5136 / 4728 等稽核日誌。
- **DCShadow 的繞過邏輯**：
  1. 攻擊者在內網工作站註冊一個暫時性的 RPC 服務端，並在 Active Directory 的 Configuration 分割區中註冊為一台新 DC (SPN: `GC/`).
  2. 攻擊者命令真正的 DC：「請向我這台新 DC 同步最新的更新資料！」
  3. 真正的 DC 發起 DRSUAPI 複製請求，將攻擊者指定的惡意資料（例如直接將特定使用者 SID 加到 `primaryGroupID`）同步進資料庫！
  4. **全過程跳過本機修改審計，達成完全的「零日誌 (Zero Event Log)」注入！**

---

## ⚔️ 階段五：藍隊反制與對抗檢測（約 5 小時）

### 5.1 關鍵防護與遙測指標
- **網路流量檢測**：監控非網域控制站 IP 發起的 `DRSGetNCChanges` RPC 呼叫。
- **Configuration 分割區監控**：監控 `CN=Servers,CN=Default-First-Site-Name,CN=Sites...` 節點是否被非預期的新增電腦註冊。

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能清楚描述 DRSUAPI 協定在網域多 DC 同步中的角色與呼叫方法。
- [ ] 能使用 PowerView 或 ADSI 檢查特定使用者是否被授予了 DCSync 複製權限。
- [ ] 熟練使用 `secretsdump.py` 針對單一目標或全網域導出 NTLM 雜湊。
- [ ] 能清楚說明 DCShadow 實現「零日誌注入」的 RPC 雙向反轉機制。
- [ ] 掌握藍隊偵測非 DC 主機發起 DRS 流量的 Suricata/Zeek 規則邏輯。
