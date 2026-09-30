# 🪟 Windows 主機權限提升：存取權杖、UAC 繞過與服務劫持深度學習路徑 (Windows PrivEsc, Tokens & UAC)
> 對應紅隊作戰矩陣：**Phase 4 (R19)** (R19.1 ~ R19.5)  
> 預計總投入時間：**30 ~ 35 小時**（視 Windows 內部安全模型、存取控制列表 DACL 與 COM 架構基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
拿到 webshell 不知如何變 SYSTEM──►   精通 Token Impersonation 與 Potato 命名管道欺騙原理
以為 UAC 是真正的安全邊界    ──►     透徹理解 Auto-Elevate 二進位檔、Mock Folders 與 COM 繞過
不懂 Windows 服務提權機制    ──►     精通未加引號服務路徑 (Unquoted Path) 與弱 DACL 權限置換
不清楚 DLL 載入順序          ──►     掌握 SafeDllSearchMode 機制與 DLL 搜尋順序劫持
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| Windows Access Token 機制 | 理解 Primary Token、Impersonation Token 與 Security Impersonation Level | [Microsoft Learn: Access Tokens](https://learn.microsoft.com/windows/win32/secauthz/access-tokens) |
| 安全描述元 (Security Descriptor) | 理解 DACL, SACL, SID 與 ACE (Access Control Entry) 繼承規則 | [Microsoft Learn: DACLs and ACEs](https://learn.microsoft.com/windows/win32/secauthz/dacl-and-aces) |
| 使用者帳戶控制 (UAC) 架構 | 理解 Integrity Level (低/中/高/系統級) 與 filtered admin token 分流 | [Microsoft Learn: How UAC Works](https://learn.microsoft.com/windows/security/application-security/application-control/user-account-control/how-user-account-control-works) |
| 服務控制管理員 (SCM) | 熟悉 `sc.exe` 配置、Service DACL 與 `SERVICE_CHANGE_CONFIG` 權限 | [Microsoft Learn: Service Control Manager](https://learn.microsoft.com/windows/win32/services/service-control-manager) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (8h) ──────► 階段二 (10h) ─────► 階段三 (8h) ──────► 階段四 (6h)
Windows服務配置     Token特權與Potato  UAC繞過內部機制     DLL搜尋順序劫持
與弱 DACL 權限濫用  命名管道模擬欺騙    (Mock Folders/COM)  與防禦監控對齊
```

---

## 🏛️ 階段一：Windows 服務漏洞利用——未加引號路徑與弱 DACL（約 8 小時）

### 1.1 未加引號服務路徑 (Unquoted Service Paths) 語法歧義
Windows 在解析無引號包裹且路徑包含空白的二進位檔案路徑時，會按照空格分割並逐級嘗試加上 `.exe`：
- 若路徑為 `C:\Program Files\Vendor App\service.exe`：
- 系統將依序嘗試搜尋並執行：
  1. `C:\Program.exe`
  2. `C:\Program Files\Vendor.exe`
  3. `C:\Program Files\Vendor App\service.exe`
- 若低權限使用者對前置目錄具備寫入權限，即可投放惡意程式優先被 SCM (SYSTEM 權限) 啟動。

### 1.2 弱服務 DACL 權限覆寫
若服務物件本身的 DACL 賦予 Authenticated Users `SERVICE_CHANGE_CONFIG` 或 `SERVICE_ALL_ACCESS` 權限：
```cmd
sc.exe config "VulnerableService" binpath= "C:\Temp\shell.exe"
sc.exe stop "VulnerableService"
sc.exe start "VulnerableService"
```

---

## 🥩 階段二：存取權杖特權與 Potato 命名管道模擬欺騙（約 10 小時）

### 2.1 `SeImpersonatePrivilege` 與 `SeAssignPrimaryTokenPrivilege`
通常指派給特定服務帳號（如 `IIS APPPOOL\*` 或 `LOCAL SERVICE`）：
- 核心意義：允許行程模擬（Impersonate）其他使用者連線至該行程時的安全性權杖。

### 2.2 Potato 家族（GodPotato / SweetPotato）底層攻防鏈
```text
[低權限服務行程] ──(1. 誘騙 RPC 連線)──► [本地 DCOM/RPC 服務 (SYSTEM)]
       │                                         │
       ├──(2. 開設本地命名管道 \\.\pipe\x)        │
       │                                         │
       ◄──(3. SYSTEM 身分連接命名管道)───────────┘
       │
[低權限行程呼叫 ImpersonateNamedPipeClient()] ──► 取得 SYSTEM 權限 Token！
```
- 利用 DCOM 氧化劑綁定（Oxidizer binding）或 RPC 介面，強迫 SYSTEM 權限之本機服務向受控的 Named Pipe 發起 NTLM 協商。
- 透過 `ImpersonateNamedPipeClient()` 捕捉到 SYSTEM 權杖後，呼叫 `CreateProcessWithTokenW()` 衍生出 SYSTEM 權限 Shell。

---

## 🥷 階段三：UAC 繞過內部機制——自動提升、Mock Folders 與 COM 介面（約 8 小時）

### 3.1 UAC 並非安全性邊界（Not a Security Boundary）
在預設 UAC 設定下，屬於本機 Administrators 群組的使用者平時以「中完整性層級 (Medium Integrity)」權杖執行。
- **Auto-Elevate 二進位檔**：微軟簽署之二進位檔（如 `fodhelper.exe`、`computerdefaults.exe`）若在資訊清單宣告 `autoElevate = true`，啟動時不會彈出 UAC 警告對話框。
- **登錄檔劫持**：此類程式啟動時會讀取使用者登錄檔分支（如 `HKCU\Software\Classes\ms-settings\Shell\Open\command`），攻擊者注入指令即可自動以 High Integrity 執行。

### 3.2 Mock Folders (目錄偽造) 穿透技術
系統只信任來自 `C:\Windows\System32\` 的自動提升程式。攻擊者可建立具備後綴空格的目錄 `C:\Windows \System32\`，並將目標程式複製至內執行，以繞過安全路徑檢查。

---

## 🛡️ 階段四：DLL 搜尋順序劫持與全域防禦對齊（約 6 小時）

### 4.1 SafeDllSearchMode 順序與利用條件
Windows 預設搜尋順序：應用程式目錄 ➔ 系統目錄 (`System32`) ➔ 16 位元系統目錄 ➔ Windows 目錄 ➔ 目前工作目錄 ➔ PATH 環境變數。
- 若應用程式載入了不存在的 DLL，且低權限帳號對應用程式目錄有寫入權限，即可觸發 DLL 劫持。

### 4.2 藍隊遙測與防禦監控
- **Windows Event 4672 / 4673**：特權指派與敏感權限使用稽核。
- **Sysmon Event 1**：監控異常母子行程（如 `w3wp.exe` 衍生 `cmd.exe`，或 `fodhelper.exe` 衍生 PowerShell）。
- **群組原則加固**：將 UAC 設定強制調整為「一律通知 (Always Notify)」，阻斷所有 Auto-Elevate 自動提升。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚說明 Primary Token 與 Impersonation Token 的架構差異。
- [ ] 能在命令列下透過 `accesschk.exe` 或 PowerShell 正確審計 Windows 服務與資料夾 DACL。
- [ ] 能清楚畫出 Potato 家族利用命名管道竊取 SYSTEM Token 的序列圖。
- [ ] 能分析為何微軟官方宣告 UAC 並不屬於安全性防護邊界（Security Boundary）。
- [ ] 能解釋 SafeDllSearchMode 與 KnownDLLs 註冊表對 DLL 劫持路徑的限制效應。

---

## 🏆 推薦實戰靶場與題庫直達
1. **TryHackMe: Windows Privilege Escalation**：涵蓋服務路徑、Potato 系列、AlwaysInstallElevated 等完整練習環境。
2. **Hack The Box Starting Point (Tier 1~2 Windows)**：練習實戰 Windows 靶機滲透全流程。[HTB Starting Point](https://app.hackthebox.com/starting-point)
3. **Orange-Cyberdefense/GOAD**：在全擬真企業 AD 網域叢集中體驗 Windows 提權與橫向移動。[GOAD 專案](https://github.com/Orange-Cyberdefense/GOAD)
