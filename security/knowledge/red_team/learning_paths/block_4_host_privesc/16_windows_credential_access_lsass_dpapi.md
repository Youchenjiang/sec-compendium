# 🔑 Windows 憑證存取機制：SAM、LSASS 記憶體與 DPAPI 深度學習路徑 (Credential Access, LSASS & DPAPI)
> 對應紅隊作戰矩陣：**Phase 4 (R19)** (R19.6 ~ R19.8)  
> 預計總投入時間：**25 ~ 30 小時**（視 Windows 驗證架構、LSA 安全子系統與加密 API 階層基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會把 mimikatz 丟上去直接跑 ──►     透徹理解 LSASS 內部記憶體布局與 SSP (Security Support Provider) 機制
遇到 RunAsPPL 被拒絕就放棄   ──►     精通 PPL 保護模式、驅動級內核存取與離線轉儲繞過
分不清 SAM 與 LSA Secrets    ──►     精通登錄檔離線匯出、Syskey 解密與本機帳密還原
不知道瀏覽器儲存密碼如何解密 ──►     徹底掌握 DPAPI MasterKey、Domain Backup Key 與萬用解密鏈
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| 本機安全性授權 (LSA) 架構 | 理解 `lsass.exe`、SSP/AP (Kerberos, Nsun, Wdigest) 與 Kerberos 票據緩存 | [Microsoft Learn: LSA Architecture](https://learn.microsoft.com/windows-server/security/credentials-protection-and-management/authentication-and-credentials) |
| 安全帳號管理員 (SAM) | 理解 SAM 資料庫結構、BootKey (Syskey) 與 RID 帳號 Hash 派生 | [Microsoft Learn: SAM Database](https://learn.microsoft.com/troubleshoot/windows-server/identity/sam-storage-credentials-security) |
| Windows 受保護行程 (PPL) | 理解 Protected Process Light 機制、簽章驗證等級與 `PROCESS_VM_READ` 限制 | [Microsoft Learn: Protecting LSASS](https://learn.microsoft.com/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection) |
| DPAPI 資料保護架構 | 理解 DPAPI 主金鑰 (MasterKey)、Preferred 檔案與用戶密碼加密推導 | [MS-DPAPI: Data Protection Application Programming Interface](https://learn.microsoft.com/openspecs/windows_protocols/ms-dpapi/) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (6h) ──────► 階段二 (8h) ──────► 階段三 (10h) ─────► 階段四 (6h)
本機 SAM/SYSTEM     LSASS記憶體結構     LSASS PPL防護模式   DPAPI階層架構
登錄檔離線轉儲還原    與SSP憑證緩存原理   與驅動內核繞過技術    與跨應用憑證解密
```

---

## 🏛️ 階段一：本機 SAM 與 SYSTEM 登錄檔離線提取（約 6 小時）

### 1.1 鎖定機制與離線導出
在 Windows 運作期間，`C:\Windows\System32\config\SAM` 由核心排他性獨佔開啟，常規檔案讀取將回傳存取被拒。
- **Volume Shadow Copy (VSS) 或登錄檔快照**：
  ```cmd
  reg save HKLM\SAM sam.hive
  reg save HKLM\SYSTEM system.hive
  reg save HKLM\SECURITY security.hive
  ```
- **解密原理**：
  `system.hive` 保存了系統啟動金鑰（Syskey / BootKey）。透過 BootKey 解密 `sam.hive` 內的帳號金鑰後，即可還原所有本機帳號的 NTLM Hash。

---

## 🥩 階段二：LSASS 記憶體結構與憑證快取機制（約 8 小時）

### 2.1 為什麼憑證會存在於 `lsass.exe`？
Windows 登入後，使用者在網域中的 SSO（單一登入）體驗仰賴 LSA 保持認證狀態：
- **SSP 模組**：Kerberos, NTLM (Msv1_0), Wdigest (歷史明文協定), CredSSP 等。
- **儲存內容**：已解密的 Kerberos 票證 Session Keys、NTLM 密碼雜湊、明文快取等。
- **MiniDump 轉儲原語**：
  Windows 原生 API `MiniDumpWriteDump()` 可被正常調試器呼叫建立 LSASS 完整傾印檔案，但在現代 EDR 監控下，該 API 會觸發嚴格的存取攔截。

---

## 🔬 階段三：LSASS PPL (Protected Process Light) 防護與繞過對抗（約 10 小時）

### 3.1 RunAsPPL 防禦機制本質
當啟動 LSA Protection (`RunAsPPL=1`) 時：
- 核心驅動層拒絕所有未達 `PsProtectedSignerLsa` 等級之行程對 `lsass.exe` 請求 `PROCESS_VM_READ` 或 `PROCESS_ALL_ACCESS` 存取代碼。
- 即使是本機 `NT AUTHORITY\SYSTEM` 也無法直接附加除錯器或讀取記憶體！

### 3.2 攻擊者繞過與應對策略
1. **BYOVD (自帶易受攻擊驅動)**：載入具備微軟簽署之合法脆弱第三方驅動程式（如 RTCore64、ProcessHacker 驅動），利用驅動程式的任意核心記憶體讀寫權限，修改核心中 `EPROCESS` 結構體的 `Protection` 旗標以摘除 PPL。
2. **影子複製靜態提取 (Volume Shadow Copy)**：轉向提取 `ntds.dit` 或登錄檔，避開動態記憶體。

---

## 💎 階段四：DPAPI 階層架構與本機憑證寶庫解密（約 6 小時）

### 4.1 DPAPI 解密樹狀圖
```text
[使用者登入密碼 / NTLM Hash] ──► 解密 ──► [DPAPI MasterKey (位於 %APPDATA%\Microsoft\Protect)]
                                                     │
                                                     ▼
                        ┌────────────────────────────┴────────────────────────────┐
                        ▼                                                         ▼
       [Google Chrome / Edge 儲存之密碼與 Cookie]                 [Windows 認證管理員 (Credential Manager)]
```
- **Domain Backup Key (網域備份金鑰)**：在網域環境中，DPAPI MasterKey 亦可使用網域控制器 CA 的 LSA 備份私鑰解密。若紅隊已取得網域備份金鑰，可直接離線解密網域內任意工作站所有使用者的 DPAPI 密碼庫！

### 4.2 藍隊防禦與偵測遙測
- **Sysmon Event 10**：監控對 `TargetImage = C:\Windows\system32\lsass.exe` 的 `ProcessAccess` 事件，嚴密過濾非微軟系統行程發起的記憶體存取。
- **啟用 Windows Credential Guard (VBS)**：透過虛擬化安全技術將 LSA 核心金鑰隔離至 Hyper-V 容器 (LSAiso.exe) 中，使實體主機即使遭受 Rootkit 攻破亦無法讀取網域憑據。

---

## 📋 自我評估檢查點
- [ ] 能向他人詳細說明 Syskey 與 SAM 資料庫解密還原 NTLM Hash 的數學運算關聯。
- [ ] 能清楚解釋 Windows RunAsPPL 在核心層級如何攔截未受保護行程的存取控制代碼。
- [ ] 能說明 BYOVD 技術如何透過物理記憶體映射抹除行程的 Protection 位元。
- [ ] 能畫出 DPAPI 從使用者密碼、MasterKey 到瀏覽器加密資料的兩層金鑰派生圖。
- [ ] 能說明 Credential Guard 的硬體虛擬化保護邊界。

---

## 🏆 推薦實戰靶場與題庫直達
1. **Orange-Cyberdefense/GOAD**：練習在真實網域環境中擷取 DPAPI Backup Key 與憑據導出。[GOAD GitHub](https://github.com/Orange-Cyberdefense/GOAD)
2. **Hack The Box Sherlocks (GhostTrace / Brutus)**：鑑識分析惡意攻擊者轉儲 LSASS 與橫向移動痕跡。[HTB Sherlocks](https://app.hackthebox.com/sherlocks)
3. **TryHackMe: Post-Exploitation Basics**：練習 Windows 憑據枚舉與本機認證庫萃取實作。
