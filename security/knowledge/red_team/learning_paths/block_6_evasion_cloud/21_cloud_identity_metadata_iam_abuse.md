# ☁️ 雲端環境滲透、實例元數據與 IAM 特權提升深度學習路徑 (Cloud Infrastructure, IMDS & IAM Abuse)
> 對應紅隊作戰矩陣：**Phase 6 (R23)** (R23.1, R23.3)  
> 預計總投入時間：**25 ~ 30 小時**（視 公有雲基礎設施架構、IAM 策略評估邏輯與雲端 API 呼叫基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
拿到雲端主機 Shell 後不知所措 ──►   精通 IMDSv1 與 IMDSv2 元數據服務安全差異與臨時憑證竊取
不懂雲端 IAM 權限如何橫向    ──►     透徹理解 AssumeRole、PassRole 與 21 種 IAM 權限提升利用鏈
以為 S3 只能枚舉公開檔案     ──►     掌握 Bucket ACL 覆寫、未授權寫入與物件生命週期投毒
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補充資源 |
| :--- | :--- | :--- |
| 雲端責任共擔模型 (Shared Responsibility) | 理解 IaaS, PaaS, SaaS 架構下雲端平台與租戶的安全界線 | [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) |
| 實例元數據服務 (IMDS) 架構 | 理解 Link-Local IP `169.254.169.254` 角色與安全憑證派發機制 | [AWS IMDS Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) |
| 雲端身分與存取管理 (IAM) | 理解 Principal, Action, Resource, Condition 與 Policy Evaluation 邏輯 | [AWS IAM Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) |
| 物件儲存權限架構 (S3 / GCS) | 理解 Bucket Policy、Bucket ACL 與存取點 (Access Points) 權限邊界 | [AWS S3 Security](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (6h) ──────► 階段二 (8h) ──────► 階段三 (10h) ─────► 階段四 (6h)
雲端實例元數據      IMDSv1 vs IMDSv2    IAM 策略漏洞與      S3/GCS 儲存桶枚舉
服務 (IMDS) 機制    防護與 SSRF 結合    21 種特權提升鏈     接管與持久化控制
```

---

## 🏛️ 階段一：雲端實例元數據服務 (IMDS) 本質解析（約 6 小時）

### 1.1 什麼是 `169.254.169.254`？
公有雲平台（AWS EC2、GCP Compute Engine、Azure VM）為虛擬機提供了一個僅限內部存取的 Link-Local IP 位址，用以查詢該實例的運作元數據：
- 當虛擬機被綁定了 IAM Role 時，AWS 會自動向該主機定期下發臨時安全金鑰（AccessKeyId, SecretAccessKey, Token）。
- **竊取端點**：
  ```bash
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<ROLE_NAME>
  ```

---

## 🥩 階段二：IMDSv1 vs IMDSv2 安全機制與 SSRF 穿透對抗（約 8 小時）

### 2.1 為什麼 IMDSv1 容易受到 SSRF 攻擊？
- **IMDSv1**：採用純 HTTP GET 請求，無任何身分驗證。若 Web 應用存在 SSRF 漏洞，攻擊者只需讓伺服器請求 `http://169.254.169.254/...` 即可秒取雲端憑證。
- **IMDSv2 防禦突破**：
  微軟與亞馬遜引入 Session Token 防護（需先透過 `PUT` 請求取得 Token，並於後續請求夾帶 `X-aws-ec2-metadata-token` 標頭）：
  ```bash
  TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
  ```
- **紅隊應對**：若 SSRF 僅支援 GET 且無法自訂標頭，IMDSv2 能有效阻斷竊取；紅隊需轉向尋找命令注入或具備自訂標頭之高階轉發漏洞。

---

## 🔬 階段三：雲端 IAM 特權提升實務——21 種利用鏈精華（約 10 小時）

### 3.1 經典權限提升場景分析
1. **`iam:CreatePolicyVersion` 提權**：
   使用者如果擁有建立新策略版本的權限，可以直接將自身擁有的現有 Policy 建立一個新的 Version，在內宣告 `"Action": "*", "Resource": "*"`，並設定為預設版本，瞬間躍升為管理員。
2. **`iam:PassRole` + `ec2:RunInstances` 提權**：
   使用者本身不是 Admin，但被允許將高特權 Role 指派給 EC2 實例。攻擊者可啟動一台帶有高特權 Role 的新 EC2，並在 UserData 中寫入反向 Shell，等待伺服器啟動時以該高權限身分連回 C2！
3. **`sts:AssumeRole` 跨帳號/跨角色跳板**：
   利用信任關係 (Trust Policy) 呼叫 `AssumeRole` 切換至目標高權限角色。

---

## 🪣 階段四：雲端儲存桶安全配置與接管對抗（約 6 小時）

### 4.1 S3 Bucket 權限錯配與枚舉
- **AllUsers / AuthenticatedUsers 授權盲區**：管理員誤以為 `AuthenticatedUsers` 代表公司內部員工，實際上代表「全世界任何擁有 AWS 帳號的人」！
- **儲存桶寫入劫持 (Bucket Overwrite)**：若 S3 託管了 Web 前端靜態 JS 檔案，攻擊者可覆寫該 JS 植入惡意 XSS 腳本或後門，實現供應鏈投毒。

### 4.2 雲端藍隊防護與稽核
- **啟用 AWS CloudTrail**：完整記錄所有 API 調用事件。
- **AWS GuardDuty 威脅偵測**：即時分析 VPC 流量日誌與 CloudTrail，自動標記異常 IP 調用 STS 憑據的行為。
- **IMDSv2 強制啟用**：在全組織 EC2 啟用 `HttpTokens=required`，並將 `HttpPutResponseHopLimit` 設為 1（防止容器逃逸呼叫主機元數據）。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚說明 IMDSv1 與 IMDSv2 在協定交握上的安全本質差異。
- [ ] 能說明 Web 應用程式 SSRF 漏洞如何被串接利用於窃取雲端執行個體憑據。
- [ ] 能解析 `iam:PassRole` 權限為何必須搭配特定服務（如 EC2/Lambda）才能形成提權鏈。
- [ ] 能指出 AWS S3 權限中 `AuthenticatedUsers` 的官方真實安全定義。
- [ ] 能說明 CloudTrail 與 GuardDuty 在偵測失竊 STS 憑據時的關聯分析依據。

---

## 🏆 推薦實戰靶場與題庫直達
1. **RhinoSecurityLabs/CloudGoat**：業界最經典之開源 AWS 脆弱架構滲透演練靶場。[CloudGoat GitHub](https://github.com/RhinoSecurityLabs/cloudgoat)
2. **Flaws.cloud / Flaws2.cloud**：由知名白帽駭客打造的免費線上 AWS 實戰滲透關卡。[flaws.cloud](http://flaws.cloud/)
3. **Pwned Labs (Free Cloud Labs)**：專注於真實公有雲環境滲透與橫向移動之挑戰平台。[Pwned Labs](https://pwnedlabs.io/)
