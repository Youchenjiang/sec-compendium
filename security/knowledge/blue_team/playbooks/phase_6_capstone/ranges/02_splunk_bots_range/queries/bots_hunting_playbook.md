# 🔍 BOTS 威脅獵捕查詢劇本 (BOTS Threat Hunting Playbook)

> **對接手冊**: [28.2 企業級實戰資料集：Splunk BOTS (Boss of the SOC) 深度研判](../../../28.2_large_scale_enterprise_bots_dataset.md)

本劇本提供在 OpenSearch Dashboards (http://localhost:5601) 與 Splunk 中進行關聯分析之標準語法。

---

## 🎯 實戰獵捕情境演練

### 情境一：獵捕 SQL Injection 攻擊與來源 IP
- **Splunk SPL 語法**:
  ```spl
  index=bots sourcetype=access_combined uri="*UNION*SELECT*"
  | stats count by clientip, method, uri, user_agent
  ```
- **OpenSearch Lucene 查詢句**:
  ```text
  sourcetype:"access_combined" AND uri:*UNION*
  ```

---

### 情境二：獵捕 WebShell 惡意程式上傳
- **Splunk SPL 語法**:
  ```spl
  index=bots sourcetype=access_combined method=POST uri="*upload*"
  | table _time, clientip, filename, status
  ```
- **OpenSearch Lucene 查詢句**:
  ```text
  sourcetype:"access_combined" AND method:"POST" AND uri:*upload*
  ```

---

### 情境三：獵捕 LOLBAS 憑證下載工具 (Certutil)
- **Splunk SPL 語法**:
  ```spl
  index=bots sourcetype=*Sysmon* EventCode=1 Image="*certutil.exe" CommandLine="*-urlcache*"
  | table _time, host, User, CommandLine, ParentImage
  ```
- **OpenSearch Lucene 查詢句**:
  ```text
  EventCode:1 AND Image:*certutil.exe AND CommandLine:*urlcache*
  ```

---

### 情境四：獵捕勒索軟體破壞陰影複製 (Volume Shadow Copy)
- **Splunk SPL 語法**:
  ```spl
  index=bots sourcetype=*Sysmon* EventCode=1 Image="*vssadmin.exe" CommandLine="*delete*shadows*"
  | table _time, host, CommandLine, ParentImage
  ```
- **OpenSearch Lucene 查詢句**:
  ```text
  EventCode:1 AND Image:*vssadmin.exe AND CommandLine:*delete*
  ```
