# 🎯 資安檢定與必考名詞速查表 (Security Exam Terms Cheatsheet)

本速查表專為**資安認證考試 (Security+, CISSP, CEH) 與高頻易忘名詞**設計，淘汰冗長段落，全面改採用**「關鍵字對照 + 一句話考點 + 易混淆比較」**，方便快速搜尋與複習。

---

## 📋 分類快速導覽

1. [🔐 1. 身分驗證與存取控制 (IAM & Authentication)](#1-身分驗證與存取控制-iam--authentication)
2. [🌐 2. 網路與通訊安全 (Network & Communication Security)](#2-網路與通訊安全-network--communication-security)
3. [🛡️ 3. 風險、合規與營運連續性 (GRC & Business Continuity)](#3-風險合規與營運連續性-grc--business-continuity)
4. [💻 4. 應用程式與密碼學 (AppSec & Cryptography)](#4-應用程式與密碼學-appsec--cryptography)
5. [⚔️ 5. 安全評估與攻防術語 (Assessment & Operations)](#5-安全評估與攻防術語-assessment--operations)

---

## 🔐 1. 身分驗證與存取控制 (IAM & Authentication)

### 高頻協定與機制對照表

| 英文簡稱 / 名詞 | 中文名稱 | 考試核心關鍵字 (1秒記考點) | 常考情境與易混淆比較 |
| :--- | :--- | :--- | :--- |
| **SSO** | 單點登錄 | 一組憑證存取多個系統 | 提高效率，但「單點失效 (Single Point of Failure)」風險高 |
| **MFA** | 多因素認證 | 跨兩類以上 (知/持/固有) | 密碼 + 手機簡訊/OTP (知+持)；兩次密碼依然只是 2FA 不是 MFA |
| **SAML 2.0** | 安全斷言標記語言 | **XML-based**、企業級 SSO、IdP 與 SP | 跨企業/企業內部單點登錄；傳輸 XML 格式的 Assertion |
| **OAuth 2.0** | 開放授權框架 | **JSON/Token**、第三方授權 | **只負責「授權」不負責「認證」**；核發 Access Token 給第三方 |
| **OIDC (OpenID Connect)** | OpenID 連線 | **OAuth 2.0 基礎上的「認證層」** | OAuth 2.0 (授權) + OIDC (身份認證)，回傳 ID Token (JWT) |
| **RADIUS** | 遠程撥號用戶服務 | **UDP**、集中式 AAA 認證、Port 1812/1813 | 僅加密密碼，其餘封包明文；常見於企業 Wireshark / VPN 認證 |
| **TACACS+** | 終端存取控制系統 | **TCP (Port 49)**、Cisco 專利 | **全封包加密**，AAA 三者分離，安全性高於 RADIUS |
| **LDAP** | 輕量目錄存取協定 | 集中式帳號目錄查詢 (Port 389/636) | 查詢 AD / 目錄樹結構；未加密走 Port 389，LDAPS 走 636 |
| **PEAP** | 受保護可擴展認證協定 | **TLS 隧道**、只需要**伺服器端證書** | 常用於 WPA2/3 Enterprise，比起 EAP-TLS 簡化（客戶端免證書） |
| **EAP-TLS** | EAP 傳輸層安全 | **雙向證書認證** (伺服器+客戶端) | 無線網路安全性最高，但管理成本高（兩端皆需安裝證書） |
| **LEAP** | 輕量 EAP | Cisco 早期研發、容易被字典攻擊 | **已廢棄**（因加密強度不足，考題常問何者不安全） |

### 存取控制模型 (Access Control Models)

| 模型名稱 | 關鍵機制 | 適用場景 / 考試判定 |
| :--- | :--- | :--- |
| **RBAC** (Role-Based) | 依據**角色/職位**分配權限 | 企業最常見，員工離職/調職只需換角色 |
| **ABAC** (Attribute-Based) | 依據**屬性** (時間、地點、設備狀態) | 零信任的核心，最靈活 (例如：僅限上班時間從台灣存取) |
| **MAC** (Mandatory) | 依據**機密等級標籤** (Top Secret) | 軍方、政府機構採用，使用者無法自行轉讓權限 |
| **DAC** (Discretionary) | 依據**資源所有者**自由劃分 | 檔案擁有者可自行決定開給誰 (Linux `chmod` 權限) |

---

## 🌐 2. 網路與通訊安全 (Network & Communication Security)

| 英文簡稱 / 名詞 | 中文名稱 | 考試核心關鍵字 (1秒記考點) | 常考情境與易混淆比較 |
| :--- | :--- | :--- | :--- |
| **Zero Trust** | 零信任模型 | **永不信任，始終驗證** | 不再劃分「內網/外網」，每次存取皆需連續認證與最小權限 |
| **NGFW** | 下一代防火牆 | **L7 應用層識別**、IPS 整合、深層封包檢查 | 比對傳統 L3/L4 防火牆，能辨識封包內部的「應用程式行為」 |
| **WAF** | Web 應用防火牆 | **Layer 7**、防範 **OWASP Top 10** | 防範 SQLi、XSS、CSRF；WAF 護 Web 應用，NGFW 護整體網路 |
| **TLS** | 傳輸層安全 | 加密傳輸、對稱+非對稱加密 | TLS 1.3 廢棄不安全演算法並簡化握手（Handshake 降至 1-RTT） |
| **SD-WAN** | 軟體定義廣域網 | 軟體控制、動態路徑選擇、降低專線成本 | 結合加密隧道與中央控制器，靈活調配網際網路與 MPLS 流量 |
| **DMZ** | 非軍事區 | 隔離區、放置對外服務 (Web/Mail) | 夾在外部網際網路與內部私有網路中間的緩衝隔離區 |
| **Outbound DNS** | 出站 DNS 流量 | 檢測 DNS 隧道與 C2 通訊 | 惡意程式常用 53 Port 出站進行 **DNS Tunneling** 竊密 |

---

## 🛡️ 3. 風險、合規與營運連續性 (GRC & Business Continuity)

### 災害復原關鍵指標 (BCP / DRP)

| 指標 / 術語 | 英文全稱 | 考試核心概念 (一句話考點) | 記法小撇步 |
| :--- | :--- | :--- | :--- |
| **RPO** | Recovery Point Objective | **最多能承受丟失多少「資料量/時間」** | 關注「資料 (Data)」；RPO=2hr 表示最多損失2小時資料 |
| **RTO** | Recovery Time Objective | **系統受損後最多多久要「恢復服務」** | 關注「時間 (Time)」；RTO=4hr 表示4小時內系統必須上線 |
| **MTBF** | Mean Time Between Failures | 系統兩次故障之間的**平均正常運作時間** | 越高代表系統越穩定可靠 |
| **MTTR** | Mean Time to Repair | 系統故障後修復所需的**平均修復時間** | 越低代表維運團隊應變修復越快 |

### 應變計畫與合規術語

| 術語 / 名詞 | 中文名稱 | 考試核心關鍵字 (1秒記考點) |
| :--- | :--- | :--- |
| **IRP** | 事件應變計畫 | 包含 6 階段：準備 → 識別 → 抑制 → 根除 → 恢復 → 復盤總結 |
| **DRP** | 災難恢復計畫 | 聚焦於災難發生後的 **IT 設施與系統復原** (BCP 的一部份) |
| **Rules of Engagement (RoE)** | 參與規則 | 滲透測試前**必須簽署**的授權文件（明確規定測試範圍與禁止行為） |
| **Right to Audit Clause** | 審計權條款 | 載明於第三方/供應商合約中，授權我方隨時查核其資安合規性 |
| **Due Diligence** | 盡職調查 | 簽約或決策前的**事前調查與評估** (調查對方資安現況) |
| **Due Care** | 應有折衝 / 盡職防禦 | 營運過程中的**日常合規維護** (有做合理防護，避免法律責任) |
| **SLA vs SOW** | 服務級別協定 / 工作說明書 | SLA 訂定**效能指標** (如 99.9% 上線率)；SOW 訂定**工作範圍細節** |

---

## 💻 4. 應用程式與密碼學 (AppSec & Cryptography)

| 術語 / 名詞 | 英文全稱 / 概念 | 考試核心關鍵字 (1秒記考點) | 常考細節 |
| :--- | :--- | :--- | :--- |
| **SDLC** | 軟體開發生命週期 | 將安全整合進開發每階段 | **Shift Left (安全左移)**：越早發現漏洞修復成本越低 |
| **Buffer Overflow** | 緩衝區溢位 | 寫入資料超出記憶體預留區塊 | 常見於 C/C++；防禦手段：**ASLR, DEP/NX, Stack Canaries** |
| **Symmetric Enc** | 對稱式加密 | 同一把金鑰加密與解密 | 加解密速度快；常見演算法：**AES, ChaCha20, 3DES** |
| **Asymmetric Enc**| 非對稱式加密 | 公鑰加密、私鑰解密 (或反之) | 解決金鑰傳遞問題，速度較慢；常見：**RSA, ECC, Diffie-Hellman** |
| **Hashing** | 雜湊演算法 | 單向不可逆、固定長度輸出 | 驗證完整性 (Integrity)；常見：**SHA-256, SHA-3** (MD5/SHA1 已不安全) |

---

## ⚔️ 5. 安全評估與攻防術語 (Assessment & Operations)

| 術語 / 名詞 | 中文名稱 | 考試核心關鍵字 (1秒記考點) | 比較與異同 |
| :--- | :--- | :--- | :--- |
| **Vulnerability Scan** | 漏洞掃描 | **自動化工具**、掃描已知漏洞 | 廣度大、可能產生偽陽性 (False Positive)，**不進行實際入侵** |
| **Penetration Test** | 滲透測試 | **人工模擬黑客攻擊**、驗證漏洞可利用性 | 深度深，實際嘗試利用漏洞突破防線 |
| **Red Team** | 紅隊 (攻擊方) | 模擬真實 APT 駭客攻擊 | 不擇手段突破（包含社交工程、實體入侵） |
| **Blue Team** | 藍隊 (防禦方) | 負責即時監控、應變與防禦 | 操作 SIEM, WAF, EDR 進行資安事件應變 |
| **Purple Team** | 紫隊 (協調方) | 促進紅藍兩隊溝通與知識共享 | 確保攻擊測試能有效轉化為防禦規則修訂 |