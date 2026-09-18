# HITCON 2026 Wargame - 提交用 Exploit 目錄

## 檔名命名規則

```
[v/x]_[序號]_[套件名]_[PHP版本].py
```

| 前綴 | 意義 |
|------|------|
| `v_` | **Verified** — 本地 Docker 驗證通過 + 平台已提交成功 |
| `x_` | **Failed** — 本地測試失敗或平台提交被拒 |
| (無前綴) | **Pending** — 寫好了但還沒測試 |

## 當前狀態

| 檔案 | 套件 | PHP | 版本 | 本地 | 平台 |
|------|------|-----|------|------|------|
| `v_01_owasp_phprbac_7.4.33.py` | owasp/phprbac | 7.4.33 | 2.0.0 | ✅ PASS | ✅ AC |
| `v_02_owasp_phprbac_8.4.py` | owasp/phprbac | 8.4 | 2.0.0 | ✅ PASS | ✅ AC |
| `v_03_internations_http-mock_7.4.33.py` | internations/http-mock | 7.4.33 | 0.8.3 | ✅ PASS | ✅ AC |
| `v_04_internations_http-mock_8.4.py` | internations/http-mock | 8.4 | 0.8.3 | ✅ PASS | ✅ AC |
| `v_05_interconnectit_7.4.33.py` | interconnectit/search-replace-db | 7.4.33 | 4.1.2 | ✅ PASS | ✅ AC |
| `v_06_vrana_adminer_8.4.py` | vrana/adminer | 8.4 | 4.8.1 | ✅ PASS | ✅ AC |
| `x_04_luracast_restler_7.4.33.py` | luracast/restler | 7.4.33 | 3.0.0 | ❌ FAIL | ❌ REJ |
| `x_04_potsky_pimp-my-log_1.7.10.py` | potsky/pimp-my-log | 7.4.33 | 1.7.10 | ❌ FAIL | ❌ REJ |

## 上傳步驟

1. 到 `${WARGAME_BASE_URL}/submit`
2. 選套件 + PHP 版本
3. 上傳對應的 `v_*.py` 檔案
4. 通過 → 檔名保持 `v_`；失敗 → 改為 `x_`

## 本地測試

```bash
cd dist
./run.sh 7.4.33 owasp/phprbac 2.0.0 ../bot/submit/v_01_owasp_phprbac_7.4.33.py
./run.sh 8.4 owasp/phprbac 2.0.0 ../bot/submit/v_02_owasp_phprbac_8.4.py
```
