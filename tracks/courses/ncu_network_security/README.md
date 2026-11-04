# 《電腦網路安全》課程教材（中央資管・114・陳奕明）

這門課的**所有交付教材**都收在這裡,課程專案當家。排課總表見上一層的 [`../ncu_network_security_schedule.md`](../ncu_network_security_schedule.md)。

## 結構

| 位置 | 內容 |
|---|---|
| `deck-studio/` | **可編譯的簡報工作區**(Open Slide = Vite + React)。本課所有 deck 的源碼。`node_modules`/`dist` 不進 git,`npm install` 還原。 |
| `sessions/` | **各堂文字教材**:教案、跟課手冊、作業、answer-key、腳本、離線 pptx。 |
| `alt-materials/` | 未排入堂次的備選教材(Nessus + Suricata)。 |

## 編輯／預覽簡報

deck 是 React 源碼(`.tsx`),靠 Open Slide 引擎渲染。第一次要先裝依賴:

```bash
cd deck-studio
npm install
```

之後即時預覽(改檔即時反映):

```bash
npm run dev
```

產出靜態站 / 交付檔:

```bash
npm run build
```

目前收錄的 deck 路由:`workshop-202610-cdx-cve-2021-41773`、`workshop-202610-net-wireshark-fundamentals`、`workshop-202610-net-wireshark-v2`。

> `@open-slide/core` 是公開的 MIT npm 套件;git 只收 `.tsx` 源碼、assets 與設定,不收 `node_modules`。
