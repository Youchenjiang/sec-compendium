# 🚪 內網橫向移動協定、無檔案遠端執行與會話劫持深度學習路徑 (Lateral Movement & Session Hijacking)
> 對應紅隊作戰矩陣：**Phase 5 (R21)** (R21.5 ~ R21.6)  
> 預計總投入時間：**25 ~ 30 小時**（視 Windows 遠端管理協定、DCOM/RPC 呼叫機制與 RDP 會話模型基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
橫向只會上傳木馬被防毒秒殺   ──►     精通 WMI、WinRM 與 DCOM 原生無檔案 (Fileless) 遠端指令執行
以為 RDP 必須知道明文密碼    ──►     透徹掌握 RDP 會話劫持 (tscon) 與影子模式 (Shadowing) 免密存取
分不清 PsExec 與 WMIExec 差異 ──►     理解 SMB 命名管道、Windows 服務註冊與 DCE/RPC 流量差異
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| Windows DCE/RPC 協定架構 | 理解 RPC End-Point Mapper (Port 135) 與動態高位埠綁定機制 | [Microsoft Learn: RPC Architecture](https://learn.microsoft.com/windows/win32/rpc/rpc-architecture) |
| Windows 管理規範 (WMI) / DCOM | 理解 WMI 物件模型、命名空間 (`root\cimv2`) 與 `Win32_Process` 方法呼叫 | [Microsoft Learn: WMI Architecture](https://learn.microsoft.com/windows/win32/wmisdk/wmi-architecture) |
| Windows 遠端管理 (WinRM) | 理解 WS-Management 協定、HTTP 5985 / HTTPS 5986 埠與 PowerShell 遠端處理 | [Microsoft Learn: Installation and Configuration for WinRM](https://learn.microsoft.com/windows/win32/winrm/installation-and-configuration-for-windows-remote-management) |
| 終端機服務 (Terminal Services) | 理解 Windows 桌面工作階段 (Session 0 與 Interactive Session ID) 隔離機制 | [Microsoft Learn: Terminal Services Architecture](https://learn.microsoft.com/windows/win32/termserv/terminal-services-architecture) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (8h) ──────► 階段二 (8h) ──────► 階段三 (8h) ──────► 階段四 (6h)
SMB 命名管道與      WMI / DCOM 物件呼叫  WinRM 遠端存取與    RDP 會話劫持
PsExec 服務落地代價  無檔案執行 (WMIExec) 認證繞過 (Evil-WinRM) 與影子桌面監控
```

---

## 🏛️ 階段一：傳統 SMB 橫向移動——PsExec 原理與痕跡代價（約 8 小時）

### 1.1 PsExec 底層執行三部曲
1. **連線與檔案寫入**：透過 SMB (Port 445) 連線至目標機的 `ADMIN$` 共享目錄，寫入可執行檔（如 `psexesvc.exe`）。
2. **服務建立與啟動**：透過 RPC 呼叫目標主機的 SCM（服務控制管理員），註冊一個名為 `PSEXESVC` 的暫時性 Windows 服務並將其啟動為 SYSTEM。
3. **命名管道通訊**：該服務開啟特定命名管道（Named Pipe），將命令輸入、輸出與攻擊機進行重導向。
- **痕跡代價**：此操作會在磁碟留下實體二進位檔案、在登錄檔留下服務鍵值、並在系統事件日誌留下 **Event ID 7045**（已安裝新服務），極易被 SOC 偵測規則捕獲。

---

## 🥩 階段二：WMI 與 DCOM 無檔案 (Fileless) 遠端指令執行（約 8 小時）

### 2.1 WMIExec 運作本質：零二進位檔案落地
WMIExec（如 Impacket 的 `wmiexec.py`）利用 Windows 內建的 Windows Management Instrumentation 基礎設施：
- **通訊協議**：連線 Port 135 (RPC Endpoint Mapper) 取得動態介面，再透過 DCOM 存取 `root\cimv2:Win32_Process` 類別。
- **呼叫方法**：直接調用 `Create` 方法：
  `cmd.exe /Q /c whoami > \\127.0.0.1\ADMIN$\__output 2>&1`
- **優勢**：不需要在目標主機註冊任何新服務，不需編譯或上傳專用 Payload，全程使用目標原生系統行程。

---

## 🔬 階段三：WinRM 與 PowerShell 遠端處理（Evil-WinRM）（約 8 小時）

### 3.1 WinRM 協定與管理埠
WinRM 是微軟官方推薦的現代遠端管理技術，底層使用 SOAP / HTTP (Port 5985) 或 HTTPS (Port 5986)：
- **特點**：預設在所有 Windows Server 啟用。
- **配合 NTLM 雜湊 (Pass-the-Hash)**：
  攻擊者即使不知道明文密碼，只要擁有 Administrator 的 NTLM Hash，便可利用 `evil-winrm` 透過 HTTP NTLM 認證直接登入，獲取全互動式 PowerShell 終端：
  ```bash
  evil-winrm -i 192.168.1.50 -u Administrator -H <NTLM_HASH>
  ```
- **記憶體載入腳本**：支援直接在記憶體中執行 PowerShell 腳本或二進位程式，完全避開硬碟讀寫監控。

---

## 🪟 階段四：RDP 遠端桌面會話劫持與影子監控（約 6 小時）

### 4.1 RDP 會話劫持技術 (`tscon.exe`)
當攻擊者已取得本機 `NT AUTHORITY\SYSTEM` 權限時，微軟終端機服務工具 `tscon.exe` 允許直接切換桌面會話：
- **操作情境**：網域管理員在該主機曾經登入並留下斷線或鎖定的 RDP 會話（如 Session ID 2）。
- **劫持指令**：
  ```cmd
  tscon 2 /dest:console
  ```
- **結果**：攻擊者不需要輸入該網域管理員的密碼，也不需要其 NTLM Hash，直接將該管理員的桌面與所有開啟的程式（瀏覽器、內部管理工具）搶奪並投射至目前螢幕！

### 4.2 藍隊偵測與事件關聯
- **Windows Event 4624 (登入類型解析)**：
  - `Logon Type 3`：網路登入（代表 SMB, WMI 或 WinRM 連線）。
  - `Logon Type 10`：遠端互動式登入（代表 RDP 連線）。
- **Sysmon Event 3 (網路連線)**：監控不尋常的主機間相互發起之 445 (SMB)、135 (RPC) 或 5985 (WinRM) 連線。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚比較 PsExec、WMIExec 與 WinRM 在目標端留下的取證軌跡差異。
- [ ] 能說明 WMI 遠端執行指令時如何透過命名空間調用 `Win32_Process.Create` 方法。
- [ ] 能在已知 NTLM Hash 情況下，使用 `evil-winrm` 成功與目標工作站建立會話。
- [ ] 能解釋 `tscon.exe` 會話劫持在 SYSTEM 權限下運作的 Windows 作業系統機制。
- [ ] 能從 Windows 安全日誌中準確區分 Logon Type 3、Type 9 與 Type 10。

---

## 🏆 推薦實戰靶場與題庫直達
1. **Hack The Box: Unified**：練習 Log4j 漏洞突破後利用 Evil-WinRM 橫向移動通關。[HTB Unified](https://app.hackthebox.com/machines/Unified)
2. **Orange-Cyberdefense/GOAD**：在多台 Windows 伺服器間演練 WMIExec、PsExec 與 RDP 會話劫持。[GOAD 專案](https://github.com/Orange-Cyberdefense/GOAD)
3. **CyberDefenders: RedLine / GrabThePhish**：藍隊取證挑戰，練習分析攻擊者內網橫向移動痕跡。[CyberDefenders](https://cyberdefenders.org/)
