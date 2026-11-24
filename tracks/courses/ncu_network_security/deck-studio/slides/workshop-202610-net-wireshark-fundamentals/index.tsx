import type { CSSProperties, ReactNode } from 'react';
import type { DesignSystem, Page, SlideMeta, SlideTransition } from '@open-slide/core';
import { useSlidePageNumber } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#f8f5ee', text: '#191f28', accent: '#0969da' },
  fonts: {
    display: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
    body: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
  },
  typeScale: { hero: 118, body: 36 },
  radius: 28,
};

export const meta: SlideMeta = {
  title: 'WORKSHOP_202610_NET_Wireshark-Fundamentals：20 分鐘掌握 Wireshark 封包分析基礎',
  createdAt: '2026-10-03T13:00:00.000Z',
};

export const transition: SlideTransition = {
  duration: 200,
  enter: {
    duration: 200,
    easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
    keyframes: [
      { opacity: 0, transform: 'translateY(6px)' },
      { opacity: 1, transform: 'translateY(0)' },
    ],
  },
  exit: { duration: 150, easing: 'ease-out', keyframes: [{ opacity: 1 }, { opacity: 0 }] },
};

const c = {
  bg: '#f8f5ee',
  text: '#191f28',
  blue: '#0969da',
  blueDark: '#054da8',
  blueSoft: '#eaf2ff',
  teal: '#0e7490',
  tealSoft: '#e0f2fe',
  cream: '#ffffff',
  gray: '#5a626a',
  line: '#dfdbd2',
  green: '#15803d',
  greenSoft: '#ecfdf5',
  amber: '#b45309',
  amberSoft: '#fef3c7',
  purple: '#7e22ce',
  purpleSoft: '#f5f3ff',
  red: '#d9381e',
  redSoft: '#fef2f2',
  termBg: '#131924',
  termText: '#f0f6fc',
};

const font = {
  body: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
  display: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
  mono: 'Consolas, ui-monospace, SFMono-Regular, Menlo, monospace',
};

const fill: CSSProperties = {
  position: 'relative',
  width: '100%',
  height: '100%',
  overflow: 'hidden',
  background: c.bg,
  color: c.text,
  fontFamily: font.body,
};

const Styles = () => (
  <style>{`
    .rise { animation: rise .3s cubic-bezier(.22,1,.36,1) both }
    @keyframes rise { from { opacity: 0; transform: translateY(8px) } to { opacity: 1; transform: translateY(0) } }
    @media (prefers-reduced-motion: reduce) { .rise { animation: none !important } }
  `}</style>
);

const Footer = () => {
  const { current, total } = useSlidePageNumber();
  return (
    <div
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        bottom: 30,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        // slide-audit-ignore: typography_floor
        fontSize: 30,
        color: c.gray,
      }}
    >
      <span>Wireshark 封包分析基礎 ｜ 20 分鐘實務引導</span>
      <span style={{ fontFamily: font.mono, fontWeight: 700 }}>
        NET-Wireshark · {current} / {total}
      </span>
    </div>
  );
};


const Frame = ({
  eyebrow,
  title,
  accentColor = c.blue,
  children,
}: {
  eyebrow: string;
  title: ReactNode;
  accentColor?: string;
  children: ReactNode;
}) => (
  <div style={fill}>
    <Styles />
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 36,
        display: 'flex',
        alignItems: 'center',
      }}
    >
      <span
        style={{
          background: accentColor,
          color: '#fff',
          fontSize: 22,
          fontWeight: 800,
          padding: '6px 18px',
          borderRadius: 8,
          letterSpacing: '0.04em',
        }}
      >
        {eyebrow}
      </span>
    </div>
    <h1
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 106,
        width: 1560,
        margin: 0,
        fontFamily: font.display,
        fontSize: 52,
        fontWeight: 900,
        lineHeight: 1.15,
        letterSpacing: '-0.03em',
      }}
    >
      {title}
    </h1>
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 200,
        bottom: 110,
      }}
    >
      {children}
    </div>
    <Footer />
  </div>
);

const Card = ({
  children,
  border = c.line,
  background = c.cream,
  style,
}: {
  children: ReactNode;
  border?: string;
  background?: string;
  style?: CSSProperties;
}) => (
  <div
    style={{
      border: `3px solid ${border}`,
      background,
      borderRadius: 24,
      padding: '30px 32px',
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
      ...style,
    }}
  >
    {children}
  </div>
);

const Badge = ({
  children,
  color = c.blue,
  bg = c.blueSoft,
}: {
  children: ReactNode;
  color?: string;
  bg?: string;
}) => (
  <span
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '6px 20px',
      borderRadius: 999,
      background: bg,
      color,
      fontSize: 30,
      fontWeight: 900,
      alignSelf: 'flex-start',
    }}
  >
    {children}
  </span>
);

const CodeBlock = ({
  children,
  title,
  fontSize = 30,
  style,
}: {
  children: string;
  title?: string;
  fontSize?: number;
  style?: CSSProperties;
}) => (
  <div
    style={{
      borderRadius: 18,
      overflow: 'hidden',
      background: c.termBg,
      border: '2px solid rgba(255,255,255,0.12)',
      ...style,
    }}
  >
    {title && (
      <div
        style={{
          background: 'rgba(255,255,255,0.06)',
          padding: '10px 20px',
          fontSize: 30,
          fontWeight: 700,
          color: '#94a3b8',
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}
      >
        <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#ef4444' }} />
        <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#f59e0b' }} />
        <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#10b981' }} />
        <span style={{ marginLeft: 6 }}>{title}</span>
      </div>
    )}
    <pre
      style={{
        margin: 0,
        padding: '20px 24px',
        fontFamily: font.mono,
        fontSize,
        color: c.termText,
        lineHeight: 1.45,
        overflowX: 'auto',
      }}
    >
      <code>{children}</code>
    </pre>
  </div>
);

// ==========================================
// Slide 1: Cover (封面開場)
// ==========================================
const SlideCover = () => (
  <div style={fill}>
    <Styles />
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 100,
        display: 'flex',
        flexDirection: 'column',
        gap: 20,
      }}
    >
      <Badge color={c.blue} bg={c.blueSoft}>
        WORKSHOP · 202610_NET_Wireshark-Fundamentals
      </Badge>
      <h1
        style={{
          margin: 0,
          fontFamily: font.display,
          fontSize: 64,
          fontWeight: 900,
          lineHeight: 1.15,
          letterSpacing: '-0.03em',
        }}
      >
        Wireshark 基礎與封包分析實務
      </h1>
      <p
        style={{
          margin: 0,
          fontSize: 34,
          color: c.gray,
          fontWeight: 700,
          lineHeight: 1.35,
        }}
      >
        20 分鐘搞懂：封包側錄原理 · 實戰故障排查 · AI 輔助過濾
      </p>
    </div>

    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 430,
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 32,
      }}
    >
      <Card border={c.line} style={{ minHeight: 280, padding: '36px 32px' }}>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.blue, marginBottom: 12 }}>
          01 · 能拿來做什麼？
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.text, lineHeight: 1.45, fontWeight: 700 }}>
          看清網路真實傳輸
        </p>
        <p style={{ margin: '12px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          網頁卡住、API 報錯或網路變慢時，直接側錄網卡進出封包，確認到底有沒有送出與回應。
        </p>
      </Card>

      <Card border={c.line} style={{ minHeight: 280, padding: '36px 32px' }}>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.teal, marginBottom: 12 }}>
          02 · 實際排錯情境
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.text, lineHeight: 1.45, fontWeight: 700 }}>
          掌握關鍵分析手法
        </p>
        <p style={{ margin: '12px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          查看 TCP 掉包重傳、檢視 HTTP 明文傳輸風險、用 Follow TCP Stream 還原完整對話。
        </p>
      </Card>

      <Card border={c.line} style={{ minHeight: 280, padding: '36px 32px' }}>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.purple, marginBottom: 12 }}>
          03 · 語法不用死背
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.text, lineHeight: 1.45, fontWeight: 700 }}>
          讓 AI 幫忙寫過濾式
        </p>
        <p style={{ margin: '12px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          清楚描述想查的 IP、Port 或協定條件，由 AI 快速轉成正確的 Display Filter 貼上查詢。
        </p>
      </Card>
    </div>

    <div
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        bottom: 100,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '18px 32px',
        background: c.cream,
        borderRadius: 18,
        border: `2px solid ${c.line}`,
      }}
    >
      <span style={{ fontSize: 30, fontWeight: 900, color: c.text }}>
        ⏱️ 20 分鐘課程安排：3 分鐘觀念 ➔ 3 分鐘適用角色 ➔ 10 分鐘實戰情境 ➔ 4 分鐘 AI 協同與 QA
      </span>
      <span style={{ fontSize: 30, fontWeight: 700, color: c.blue }}>
        情境導向 · 實用優先
      </span>
    </div>

    <Footer />
  </div>
);

// ==========================================
// Slide 2: 幹嘛？為什麼需要 Wireshark (00:00 - 03:00)
// ==========================================
const SlideMentalModel = () => (
  <Frame
    eyebrow="OVERVIEW · 工具定位"
    accentColor={c.blue}
    title="為什麼需要 Wireshark？看見「網路到底發生了什麼事」"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <Card border={c.red} background={c.redSoft} style={{ padding: '32px 34px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <span style={{ fontSize: 36 }}>❓</span>
          <span style={{ fontSize: 36, fontWeight: 900, color: c.red }}>
            平常遇到的排錯困境：看不見傳輸過程
          </span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.line}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.red }}>網頁卡住轉圈圈</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
              伺服器 CPU 很低，不知是網路連線慢、交換機掉包、還是後端沒處理。
            </p>
          </div>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.line}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.red }}>前後端 API 呼叫失敗</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
              前端說「已發送」，後端說「Log 沒收到」，雙方只能憑推測爭執。
            </p>
          </div>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.line}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.red }}>電腦網路燈一直閃</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
              沒有開瀏覽器，但網卡持續有流量進出，不知道是哪個程式在連外。
            </p>
          </div>
        </div>
      </Card>

      <Card border={c.blue} background={c.blueSoft} style={{ padding: '32px 34px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <span style={{ fontSize: 36 }}>🔍</span>
          <span style={{ fontSize: 36, fontWeight: 900, color: c.blueDark }}>
            Wireshark 做的事：直接錄下網卡流過的封包
          </span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.line}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.blueDark }}>側錄真實網路訊號</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
              藉由底層抓包驅動把經過網卡的封包完整存下來，記錄時間與內容。
            </p>
          </div>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.line}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.blueDark }}>自動解析各層協定格式</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
              將二進位資料解讀為 Ethernet、IP、TCP/UDP、HTTP、DNS 等欄位。
            </p>
          </div>
          <div style={{ background: '#fff', borderRadius: 16, padding: '18px 22px', border: `2px solid ${c.blue}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.blue }}>結論：拿封包紀錄來確認事實</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.45 }}>
              有沒有發送？發了什麼參數？有沒有回傳 ACK？打開抓包檔一看便知。
            </p>
          </div>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 3: 誰在用？四大角色實務應用 (03:00 - 06:00)
// ==========================================
const SlideRoleSpectrum = () => (
  <Frame
    eyebrow="AUDIENCE · 角色應用"
    accentColor={c.teal}
    title="不同崗位的人，平常用 Wireshark 做什麼？"
  >
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24, height: '100%' }}>
      <Card border={c.line} style={{ padding: '32px 24px', background: '#fff', display: 'flex', flexDirection: 'column', height: '100%', boxSizing: 'border-box' }}>
        <Badge color={c.blue} bg={c.blueSoft}>網路管理人員</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25, marginTop: 14 }}>
          排查塞車與掉包
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1, marginTop: 20 }}>
          <div style={{ flex: 1, background: '#f8fafc', borderRadius: 18, padding: '20px', border: `2px solid ${c.line}`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, lineHeight: 1.45 }}>
              會議室突然爆延遲、交換機異常掉包，難以即時定位問題節點。
            </div>
          </div>

          <div style={{ flex: 1, background: c.blueSoft, borderRadius: 18, padding: '20px', border: `2px solid ${c.blue}30`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.45 }}>
              側錄重傳與零視窗，依時間序秒定硬體設備故障。
            </div>
          </div>
        </div>
      </Card>

      <Card border={c.line} style={{ padding: '32px 24px', background: '#fff', display: 'flex', flexDirection: 'column', height: '100%', boxSizing: 'border-box' }}>
        <Badge color={c.teal} bg={c.tealSoft}>軟體開發工程師</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25, marginTop: 14 }}>
          API 與通訊除錯
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1, marginTop: 20 }}>
          <div style={{ flex: 1, background: '#f8fafc', borderRadius: 18, padding: '20px', border: `2px solid ${c.line}`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, lineHeight: 1.45 }}>
              前後端爭論「有發沒收到」，或外部 Webhook 發生不明逾時。
            </div>
          </div>

          <div style={{ flex: 1, background: c.tealSoft, borderRadius: 18, padding: '20px', border: `2px solid ${c.teal}30`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.45 }}>
              直視網卡真實進出 Payload，終結日誌對帳爭論。
            </div>
          </div>
        </div>
      </Card>

      <Card border={c.line} style={{ padding: '32px 24px', background: '#fff', display: 'flex', flexDirection: 'column', height: '100%', boxSizing: 'border-box' }}>
        <Badge color={c.purple} bg={c.purpleSoft}>資安防守人員</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25, marginTop: 14 }}>
          異常外連與鑑識
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1, marginTop: 20 }}>
          <div style={{ flex: 1, background: '#f8fafc', borderRadius: 18, padding: '20px', border: `2px solid ${c.line}`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, lineHeight: 1.45 }}>
              主機防毒完全沒告警，但端點疑似存在隱蔽的心跳信標外連。
            </div>
          </div>

          <div style={{ flex: 1, background: c.purpleSoft, borderRadius: 18, padding: '20px', border: `2px solid ${c.purple}30`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.45 }}>
              檔名與程序能偽裝，但連網封包握手特徵無法隱形。
            </div>
          </div>
        </div>
      </Card>

      <Card border={c.line} style={{ padding: '32px 24px', background: '#fff', display: 'flex', flexDirection: 'column', height: '100%', boxSizing: 'border-box' }}>
        <Badge color={c.amber} bg={c.amberSoft}>滲透測試人員</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25, marginTop: 14 }}>
          檢驗未加密風險
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1, marginTop: 20 }}>
          <div style={{ flex: 1, background: '#f8fafc', borderRadius: 18, padding: '20px', border: `2px solid ${c.line}`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, lineHeight: 1.45 }}>
              系統號稱全站 HTTPS，內部微服務卻可能私下裸奔傳明文。
            </div>
          </div>

          <div style={{ flex: 1, background: c.amberSoft, borderRadius: 18, padding: '20px', border: `2px solid ${c.amber}30`, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.45 }}>
              截取並還原通訊內容，提出無可辯駁的加密加固證據。
            </div>
          </div>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 4: 介面三段視野 (03:00 - 06:00)
// ==========================================
const SlideUiDissection = () => (
  <Frame
    eyebrow="UI · 介面結構"
    accentColor={c.teal}
    title="Wireshark 介面結構：三塊核心顯示區域"
  >
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, height: '100%' }}>
      <Card border={c.blue} background={c.cream} style={{ flex: 1, padding: '28px 32px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span style={{ background: c.blue, color: '#fff', padding: '6px 16px', borderRadius: 10, fontSize: 30, fontWeight: 900 }}>
              上方
            </span>
            <span style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
              封包清單 (Packet List)：檢視整體傳輸流向
            </span>
          </div>
          <span style={{ fontSize: 30, color: c.gray, fontFamily: font.mono }}>
            Time ｜ Source ➔ Destination ｜ Protocol ｜ Length ｜ Info
          </span>
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          每一列代表一個收送的封包。利用顏色標記（如綠色 HTTP、黑色重傳）快速找出關鍵封包。
        </p>
      </Card>

      <Card border={c.teal} background={c.cream} style={{ flex: 1, padding: '28px 32px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span style={{ background: c.teal, color: '#fff', padding: '6px 16px', borderRadius: 10, fontSize: 30, fontWeight: 900 }}>
              中間
            </span>
            <span style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
              協定細節 (Packet Details)：點選展開各層欄位
            </span>
          </div>
          <span style={{ fontSize: 30, color: c.teal, fontWeight: 900 }}>
            ★ 最常查看的排錯區域
          </span>
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          點開查看具體內容：Frame (實體網卡) ➔ Ethernet (MAC) ➔ IP (IP 位址) ➔ TCP (Port 與序號) ➔ <strong>HTTP/DNS (文字與參數)</strong>。
        </p>
      </Card>

      <Card border={c.gray} background={c.cream} style={{ flex: 1, padding: '28px 32px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span style={{ background: c.gray, color: '#fff', padding: '6px 16px', borderRadius: 10, fontSize: 30, fontWeight: 900 }}>
              下方
            </span>
            <span style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
              原始位元組 (Packet Bytes)：十六進位與 ASCII 碼
            </span>
          </div>
          <span style={{ fontSize: 30, color: c.gray, fontFamily: font.mono }}>
            Hex Dump + ASCII Raw Data
          </span>
        </div>
        <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          在中間點選任何欄位，下方會同步高亮對應的 Byte。初學者不用看 Hex，平常用上方與中間就足夠。
        </p>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 5: 情境 1 · 效能維運 (06:00 - 16:00)
// ==========================================
const SlideScenarioPerformance = () => (
  <Frame
    eyebrow="CASE 1 · 掉包排查"
    accentColor={c.amber}
    title="情境一：連線卡住或極慢？排查 TCP 重傳 (Retransmission)"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, height: '100%' }}>
        <Card border={c.amber} background={c.amberSoft} style={{ padding: '30px 32px' }}>
          <Badge color={c.amber} bg="#fff">實際現象</Badge>
          <div style={{ fontSize: 36, fontWeight: 900, color: '#78350f', margin: '14px 0 8px' }}>
            網頁卡住 5 到 10 秒才能打開
          </div>
          <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
            使用者反映系統很慢，但後端伺服器 CPU 使用率不到 20%，記憶體也完全夠用。
          </p>
        </Card>

        <CodeBlock title="在上方過濾列輸入過濾條件" fontSize={30}>
          tcp.analysis.flags
        </CodeBlock>

        <Card border={c.line} style={{ padding: '24px 28px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.gray }}>畫面上的特徵：</span>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.red, marginTop: 8 }}>
            出現大量黑底紅字：[TCP Retransmission] 或 [TCP Dup ACK]
          </div>
        </Card>
      </div>

      <Card border={c.blue} style={{ padding: '32px 34px', background: c.cream, height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 18 }}>
        <Badge color={c.blue} bg={c.blueSoft}>原因分析與結論</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          發送端送出後等不到回應，正在重複發送
        </div>

        <p style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, margin: 0 }}>
          TCP 提供可靠保證。若封包在線路上遺失，發送端逾時未收確認就會啟動計時器 (RTO) 重送。
        </p>

        <div style={{ background: c.amberSoft, border: `2px solid ${c.amber}`, borderRadius: 16, padding: '18px 22px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#92400e' }}>⚙️ 重傳特徵與問題定位：</span>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: '#78350f', lineHeight: 1.45 }}>
            重傳以指數退避遞增等待（1s ➔ 2s ➔ 4s），判定為實體網路線路、WiFi 弱訊號干擾或交換機溢位，非後端程式當機。
          </p>
        </div>

        <div style={{ background: c.greenSoft, borderRadius: 16, padding: '18px 22px', borderLeft: `6px solid ${c.green}` }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.green }}>🛠️ 實務處置步驟：</span>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            匯出包含重傳時間點的 PCAP 封包檔與統計圖，直接提交網管或機房工程師檢修硬體線路。
          </p>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 6: 情境 2 · 資安風險 (06:00 - 16:00)
// ==========================================
const SlideScenarioSecurity = () => (
  <Frame
    eyebrow="CASE 2 · 傳輸安全"
    accentColor={c.amber}
    title="情境二：為什麼不能用未加密協定？HTTP 明文帳密側錄"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, height: '100%' }}>
        <Card border={c.red} background={c.redSoft} style={{ padding: '30px 32px' }}>
          <Badge color={c.red} bg="#fff">實際現象</Badge>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.red, margin: '14px 0 8px' }}>
            在區域網路內登入未加密的 HTTP 網站
          </div>
          <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
            同網段的人只要開啟 Wireshark，輸入過濾條件鎖定送出的表單。
          </p>
        </Card>

        <CodeBlock title="過濾 HTTP POST 請求" fontSize={30}>
          http.request.method == "POST"
        </CodeBlock>

        <Card border={c.line} style={{ padding: '24px 28px', background: c.termBg, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#94a3b8' }}>Packet Details 展開 HTML 表單內容：</span>
          <pre style={{ margin: '10px 0 0', color: '#38bdf8', fontFamily: font.mono, fontSize: 30, lineHeight: 1.45 }}>
            Form item: "username" = "admin"<br />
            Form item: "password" = "SuperSecret2026!"
          </pre>
        </Card>
      </div>

      <Card border={c.line} style={{ padding: '32px 34px', background: c.cream, height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 18 }}>
        <Badge color={c.red} bg={c.redSoft}>為什麼會這樣？</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          HTTP 通訊完全無加密：明文裸奔傳輸
        </div>

        <p style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, margin: 0 }}>
          HTTP 採用純文字 ASCII 編碼傳輸，途經任何節點（區域網路 Hub、ARP 欺騙、公共 WiFi）皆可被無感還原。
        </p>

        <div style={{ background: c.redSoft, border: `2px solid ${c.red}`, borderRadius: 16, padding: '18px 22px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.red }}>⚠️ 側錄現場暴露的機敏內容：</span>
          <ul style={{ margin: '6px 0 0', paddingLeft: 22, fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            <li>登入表單輸入的明文密碼與個人資料</li>
            <li>Cookie、Session Token 與 API Authorization 標頭</li>
          </ul>
        </div>

        <div style={{ background: c.greenSoft, borderRadius: 16, padding: '18px 22px', borderLeft: `6px solid ${c.green}` }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.green }}>🔒 正確處置與防護：</span>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            全面導入 HTTPS (TLS 1.3) 並設定 HSTS 強制轉向，使側錄者只能取得無法破解的密文。
          </p>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 7: 實用功能 Follow Stream (06:00 - 16:00)
// ==========================================
const SlideFollowStream = () => (
  <Frame
    eyebrow="FEATURE · 封包還原"
    accentColor={c.amber}
    title="實用功能：Follow TCP Stream 重組完整對話"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <Card border={c.blue} background={c.cream} style={{ padding: '32px 34px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 18 }}>
        <Badge color={c.blue} bg={c.blueSoft}>解決核心痛點</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          封包切碎分散，如何看完整對話？
        </div>
        <p style={{ fontSize: 30, color: c.gray, lineHeight: 1.4, margin: 0 }}>
          傳送較大 Payload 時底層受限 MTU 會切成多個封包，逐一檢視極為耗時。
        </p>

        <div style={{ background: c.blueSoft, padding: '18px 22px', borderRadius: 16, borderLeft: `6px solid ${c.blue}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.blue }}>🖱️ 快捷操作與重組機制：</div>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            任何連線封包按右鍵 ➔ Follow ➔ TCP Stream。系統依 TCP Sequence 序號自動重組去重，還原完整通訊。
          </p>
        </div>

        <div style={{ background: c.greenSoft, padding: '18px 22px', borderRadius: 16, borderLeft: `6px solid ${c.green}` }}>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.green }}>💡 實用價值：</div>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45, fontWeight: 700 }}>
            免組裝碎片，像讀即時通訊紀錄般直觀查閱完整 API 參數。
          </p>
        </div>
      </Card>

      <Card border={c.line} background={c.termBg} style={{ padding: '28px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#94a3b8' }}>Follow TCP Stream 重組視窗</span>
          <span style={{ fontSize: 30, color: '#64748b' }}>TCP Stream #12</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14, fontFamily: font.mono, fontSize: 30, lineHeight: 1.45, flex: 1, justifyContent: 'center' }}>
          <div style={{ color: '#f87171', background: 'rgba(239,68,68,0.12)', padding: '14px 16px', borderRadius: 10, border: '1px solid rgba(239,68,68,0.25)' }}>
            <span style={{ fontWeight: 900 }}>[紅色] Client 請求 (Request)：</span><br />
            POST /api/v1/user/auth HTTP/1.1<br />
            Authorization: Bearer jwt_preview_987xyz<br />
            {`{"username": "admin", "scope": "write"}`}
          </div>
          <div style={{ color: '#60a5fa', background: 'rgba(96,165,250,0.12)', padding: '14px 16px', borderRadius: 10, border: '1px solid rgba(96,165,250,0.25)' }}>
            <span style={{ fontWeight: 900 }}>[藍色] Server 回應 (Response)：</span><br />
            HTTP/1.1 200 OK<br />
            Content-Type: application/json<br />
            {`{"status": "success", "user": "admin"}`}
          </div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, padding: '14px 18px', color: '#94a3b8', fontSize: 30, lineHeight: 1.4 }}>
          <strong style={{ color: '#38bdf8' }}>🎨 色彩識別：</strong> 紅色為 Client 送出，藍色為 Server 回應。
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 8: 加密後還能看什麼 (06:00 - 16:00)
// ==========================================
const SlideEncryptionBoundary = () => (
  <Frame
    eyebrow="SECURITY · 協定對比"
    accentColor={c.amber}
    title="加密之後還能看到什麼？HTTP vs. HTTPS 側錄對比"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <Card border={c.red} background={c.cream} style={{ padding: '28px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 14 }}>
        <Badge color={c.red} bg={c.redSoft}>HTTP 連線（未加密）</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.red, lineHeight: 1.25 }}>
          所有傳輸內容皆為純文字
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>⚠️</span>
            <div><strong>網址路徑與 Query</strong>：全部一覽無遺</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>⚠️</span>
            <div><strong>Cookie 與 Token</strong>：直接遭側錄劫持</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>⚠️</span>
            <div><strong>表單帳號與密碼</strong>：純文字未經保護</div>
          </div>
        </div>

        <div style={{ background: c.termBg, borderRadius: 14, padding: '14px 18px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#f87171' }}>[Wireshark 側錄明文內容]</span>
          <pre style={{ margin: '6px 0 0', color: '#fca5a5', fontFamily: font.mono, fontSize: 30, lineHeight: 1.4 }}>
            POST /api/login HTTP/1.1<br />
            Host: internal.corp.net<br />
            Authorization: Basic YWRtaW46MTIz<br />
            {`{"username": "admin", "password": "123"}`}
          </pre>
        </div>

        <div style={{ background: c.redSoft, border: `1.5px solid ${c.red}`, borderRadius: 12, padding: '12px 16px' }}>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.red }}>🚨 竊聽風險：中途節點可無感側錄，禁止傳送憑證。</div>
        </div>
      </Card>

      <Card border={c.green} background={c.cream} style={{ padding: '28px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 14 }}>
        <Badge color={c.green} bg={c.greenSoft}>HTTPS 連線（TLS 加密）</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.green, lineHeight: 1.25 }}>
          內容加密，但外部特徵依然可見
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>🔒</span>
            <div><strong>傳輸內容 (Payload)</strong>：高強度加密不可讀</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>👁️</span>
            <div><strong>目標 IP 與 Port</strong>：清楚識別通訊實體位址</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 30 }}>
            <span>👁️</span>
            <div><strong>目標網域名稱 (SNI)</strong>：交握階段仍為明文可見</div>
          </div>
        </div>

        <div style={{ background: c.termBg, borderRadius: 14, padding: '14px 18px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#4ade80' }}>[Wireshark 側錄密文內容]</span>
          <pre style={{ margin: '6px 0 0', color: '#86efac', fontFamily: font.mono, fontSize: 30, lineHeight: 1.4 }}>
            TLSv1.3 Client Hello (SNI: api.corp.net)<br />
            Protocol: http-over-tls<br />
            Encrypted Data: 640 bytes (密文亂碼)<br />
            [Payload 完全雜湊加密，無法直接讀取]
          </pre>
        </div>

        <div style={{ background: c.greenSoft, border: `1.5px solid ${c.green}`, borderRadius: 12, padding: '12px 16px' }}>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.green }}>🔍 排查價值：中繼特徵足以排查握手失敗與異常外連。</div>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 9: 情境 3 · 異常外連 (06:00 - 16:00)
// ==========================================
const SlideScenarioThreat = () => (
  <Frame
    eyebrow="CASE 3 · 異常外連"
    accentColor={c.amber}
    title="情境三：電腦沒在用卻有流量？排查異常外連與 DNS 查詢"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 18, height: '100%' }}>
        <Card border={c.purple} background={c.purpleSoft} style={{ padding: '24px 28px' }}>
          <Badge color={c.purple} bg="#fff">實際現象</Badge>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.purple, margin: '12px 0 6px' }}>
            下班電腦待機，網卡卻每隔幾秒閃一下
          </div>
          <p style={{ margin: 0, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
            使用者未開啟任何瀏覽器或通訊軟體，但網卡持續有規律的小封包向未知公網 IP 傳輸。
          </p>
        </Card>

        <CodeBlock title="過濾 DNS 域名查詢" fontSize={30}>
          dns
        </CodeBlock>

        <Card border={c.line} style={{ padding: '22px 26px', background: c.termBg, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#94a3b8' }}>發現定期查詢奇怪的網域名稱：</span>
          <pre style={{ margin: '10px 0 0', color: '#c084fc', fontFamily: font.mono, fontSize: 30, lineHeight: 1.45 }}>
            Standard query A x89k-cmd.suspicious-host.net<br />
            Standard query response ➔ 198.51.100.77 (TTL=60)
          </pre>
        </Card>
      </div>

      <Card border={c.line} style={{ padding: '32px 34px', background: c.cream, height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 18 }}>
        <Badge color={c.purple} bg={c.purpleSoft}>為什麼要這樣查？</Badge>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          惡意程式常會定期連回控制主機 (C2)
        </div>
        <p style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, margin: 0 }}>
          木馬透過 Beaconing（心跳信標）每隔固定時間連外確認指令，連線必留痕跡。
        </p>

        <div style={{ background: c.purpleSoft, border: `2px solid ${c.purple}`, borderRadius: 16, padding: '18px 22px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.purple }}>🔍 封包無法隱形與 DGA 特徵：</span>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            處理程序可在系統工作管理員偽裝，但連網封包必經網卡。雜湊字串動態域名具有固定查詢頻率且存活極短。
          </p>
        </div>

        <div style={{ background: c.greenSoft, borderRadius: 16, padding: '18px 22px', borderLeft: `6px solid ${c.green}` }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.green }}>🛡️ 資安應變處置 SOP：</span>
          <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, lineHeight: 1.45 }}>
            1. 拔除網路線隔離 ➔ 2. 防火牆阻絕 C2 IP ➔ 3. 以 <code>netstat -ano</code> 查出 PID 掃毒清除。
          </p>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// ==========================================
// Slide 10: AI 協同工作流 (16:00 - 20:00)
// ==========================================
const SlideAiWorkflow = () => (
  <Frame
    eyebrow="AI · 提示詞生成"
    accentColor={c.purple}
    title="不用死背過濾語法：用 AI 快速生成 Wireshark Filter"
  >
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 28, height: '100%' }}>
      <Card border={c.blue} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.blue} bg={c.blueSoft}>情境 1 · API 排錯</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.blue }}>鎖定主機</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          篩選特定 IP 與 POST 請求
        </div>

        <div>
          <div style={{ fontSize: 30, fontWeight: 900, color: c.blueDark }}>💬 提示詞 (Prompt)：</div>
          <p style={{ margin: '8px 0 0', fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.4 }}>
            「鎖定目的地 192.168.1.1 且為 POST 的 HTTP 請求」
          </p>
        </div>

        <div style={{ background: c.termBg, borderRadius: 16, padding: '22px 24px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ fontSize: 30, color: '#94a3b8', fontWeight: 700 }}>AI 生成 Filter：</div>
          <div style={{ color: '#38bdf8', fontFamily: font.mono, fontSize: 30, marginTop: 8, fontWeight: 700, lineHeight: 1.45 }}>
            ip.dst == 192.168.1.1 &&<br />
            http.request.method == "POST"
          </div>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          👉 <strong>實戰：</strong>過濾列貼上變綠，右鍵 Follow TCP Stream 還原 JSON。
        </div>
      </Card>

      <Card border={c.amber} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.amber} bg={c.amberSoft}>情境 2 · 效能維運</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.amber }}>診斷掉包</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          一鍵抓出 TCP 異常標籤
        </div>

        <div>
          <div style={{ fontSize: 30, fontWeight: 900, color: '#92400e' }}>💬 提示詞 (Prompt)：</div>
          <p style={{ margin: '8px 0 0', fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.4 }}>
            「抓出所有 TCP 重傳 (Retransmission) 異常標籤」
          </p>
        </div>

        <div style={{ background: c.termBg, borderRadius: 16, padding: '22px 24px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ fontSize: 30, color: '#94a3b8', fontWeight: 700 }}>AI 生成 Filter：</div>
          <div style={{ color: '#fbbf24', fontFamily: font.mono, fontSize: 30, marginTop: 8, fontWeight: 700, lineHeight: 1.45 }}>
            tcp.analysis.flags
          </div>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          👉 <strong>實戰：</strong>若出現大量黑底紅字，代表實體線路異常，直接報修。
        </div>
      </Card>

      <Card border={c.purple} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.purple} bg={c.purpleSoft}>情境 3 · 威脅偵測</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.purple }}>排查外連</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          過濾 DNS 並排除內網
        </div>

        <div>
          <div style={{ fontSize: 30, fontWeight: 900, color: '#581c87' }}>💬 提示詞 (Prompt)：</div>
          <p style={{ margin: '8px 0 0', fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.4 }}>
            「過濾所有 DNS 查詢請求，但排除內網 192.168.0.0/16」
          </p>
        </div>

        <div style={{ background: c.termBg, borderRadius: 16, padding: '22px 24px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ fontSize: 30, color: '#94a3b8', fontWeight: 700 }}>AI 生成 Filter：</div>
          <div style={{ color: '#c084fc', fontFamily: font.mono, fontSize: 30, marginTop: 8, fontWeight: 700, lineHeight: 1.45 }}>
            dns &&<br />
            !(ip.addr == 192.168.0.0/16)
          </div>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
          👉 <strong>實戰：</strong>展開查詢字串抓出外部可疑域名，提交防火牆阻斷。
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 11: 課後複習 (16:00 - 20:00)
// ==========================================
const SlideCheckpoints = () => (
  <Frame
    eyebrow="REVIEW · 課後思考"
    accentColor={c.purple}
    title="課後複習：常見問題與情境對照"
  >
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 32, height: '100%' }}>
      <Card border={c.blue} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.blue} bg={c.blueSoft}>Q1 · API 爭執</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.blue }}>通訊真偽判定</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          前端說有送，後端說沒收到？
        </div>

        <div style={{ background: c.blueSoft, padding: '22px 24px', borderRadius: 16, borderLeft: `6px solid ${c.blue}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.blueDark }}>🔍 Wireshark 判斷法：</span>
          <ul style={{ margin: '10px 0 0', paddingLeft: 24, fontSize: 30, color: c.text, lineHeight: 1.5 }}>
            <li><strong>有發出且收到 ACK</strong> ➔ 前端確實送達</li>
            <li><strong>收到 4xx / 5xx</strong> ➔ 後端有收到但程式報錯</li>
          </ul>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          💡 <strong>一句話結論：</strong>不要各開 Console 猜測，側錄封包 10 秒結束爭執。
        </div>
      </Card>

      <Card border={c.green} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.green} bg={c.greenSoft}>Q2 · HTTPS 加密</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.green }}>加密邊界掌握</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          內容加密了，還能看什麼？
        </div>

        <div style={{ background: c.greenSoft, padding: '22px 24px', borderRadius: 16, borderLeft: `6px solid ${c.green}`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#166534' }}>🔍 Wireshark 判斷法：</span>
          <ul style={{ margin: '10px 0 0', paddingLeft: 24, fontSize: 30, color: c.text, lineHeight: 1.5 }}>
            <li><strong>看 Client Hello SNI</strong> ➔ 明文暴露連線域名</li>
            <li><strong>看 IP、Port 與時序</strong> ➔ 診斷握手失敗與異常</li>
          </ul>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          💡 <strong>一句話結論：</strong>內容雖保密，外部中繼資料足以定位 80% 網路障礙。
        </div>
      </Card>

      <Card border={c.amber} background={c.cream} style={{ padding: '36px 30px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Badge color={c.amber} bg={c.amberSoft}>Q3 · 網路卡頓</Badge>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.amber }}>效能瓶頸歸因</span>
        </div>

        <div style={{ fontSize: 36, fontWeight: 900, color: c.text, lineHeight: 1.25 }}>
          大量 TCP Retransmission 代表什麼？
        </div>

        <div style={{ background: c.amberSoft, padding: '22px 24px', borderRadius: 16, borderLeft: `6px solid #d97706`, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: '#92400e' }}>🔍 Wireshark 判斷法：</span>
          <ul style={{ margin: '10px 0 0', paddingLeft: 24, fontSize: 30, color: c.text, lineHeight: 1.5 }}>
            <li><strong>逾時未收到 ACK</strong> ➔ 實體線路、交換機或 WiFi 掉包</li>
            <li><strong>Dup ACK 快速重傳</strong> ➔ 網路佇列擁塞而非 CPU 不足</li>
          </ul>
        </div>

        <div style={{ paddingTop: 16, borderTop: `2px solid ${c.line}`, fontSize: 30, color: c.gray, lineHeight: 1.45 }}>
          💡 <strong>一句話結論：</strong>問題在傳輸層，請聯絡網管團隊，不用盲目改 SQL。
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Slide 12: 總結與資源 (16:00 - 20:00)
// ==========================================
const SlideSummary = () => (
  <Frame
    eyebrow="SUMMARY · 總結交流"
    accentColor={c.purple}
    title="重點總結與實務練習資源"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      <Card border={c.blue} background={c.cream} style={{ padding: '32px 34px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div>
          <Badge color={c.blue} bg={c.blueSoft}>課堂核心收穫</Badge>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
          <div style={{ background: c.blueSoft, padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.blueDark }}>01 · 網路問題以真實封包為準</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
              不用憑空猜測，透過側錄封包確認請求到底有沒有發出、對方有沒有回應。
            </p>
          </div>
          <div style={{ background: c.tealSoft, padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.teal }}>02 · 語法交給 AI 輔助生成</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
              把精力放在「定義想排查的症狀」，讓 AI 寫出精準的過濾條件。
            </p>
          </div>
          <div style={{ background: c.purpleSoft, padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.purple }}>03 · 善用 Follow TCP Stream</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
              遇到切碎的封包不要一個個看，右鍵 Follow Stream 快速重組完整通訊。
            </p>
          </div>
        </div>
      </Card>

      <Card border={c.line} background={c.cream} style={{ padding: '32px 34px', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div>
          <Badge color={c.green} bg={c.greenSoft}>自主練習推薦</Badge>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
          <div style={{ border: `2px solid ${c.line}`, background: '#fff', padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.text }}>Wireshark 官方範例庫 (Sample Captures)</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
              官方收集了數百個真實協定與故障 PCAP 檔案，免自己抓包即可下載練習。
            </p>
          </div>
          <div style={{ border: `2px solid ${c.line}`, background: '#fff', padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.text }}>Malware Traffic Analysis 實戰題庫</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.gray, lineHeight: 1.4 }}>
              提供各種惡意程式連線的實戰抓包題庫，適合資安分析人員練習分析。
            </p>
          </div>
          <div style={{ background: c.greenSoft, padding: '18px 24px', borderRadius: 16, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.green }}>💬 現場 Q&A 時間</span>
            <p style={{ margin: '6px 0 0', fontSize: 30, color: c.text, fontWeight: 700, lineHeight: 1.4 }}>
              大家在網路排錯或封包分析上有任何問題，歡迎隨時提問交流！
            </p>
          </div>
        </div>
      </Card>
    </div>
  </Frame>
);

// ==========================================
// Speaker Notes & Default Export
// ==========================================
export const notes: string[] = [
  '【0:00-0:45】開場問候。以平常開發或維運常碰到的問題開場：網頁卡住、前後端吵 API 有沒有送、或網路卡一直閃。今天用 20 分鐘帶大家了解 Wireshark 的基本原理、實務用途，以及如何用 AI 幫忙過濾封包。',
  '【0:45-3:00】幹嘛？說明平常排錯的盲點是看不到傳輸過程，只能猜測。Wireshark 的本質就是把網卡進出的封包完整錄下來並解析格式。有沒有送出、送了什麼、對方回什麼，全部看封包確認，不用靠猜。',
  '【3:00-4:30】誰在用？不同角色在實務上的用法：網管查網路塞車與掉包；軟體工程師查 API 傳輸內容與回傳錯誤；資安藍隊查異常外連 IP 與惡意程式連線；滲透測試人員檢驗傳輸是否有未加密風險。',
  '【4:30-6:00】介面結構介紹：上方是封包清單，看整體流向；中間是協定詳細欄位，點開可以看 IP、TCP、HTTP 等具體內容；下方是 Hex/ASCII 原始資料。強調平常 90% 的除錯只要看上方清單與中間協定即可。',
  '【6:00-8:30】情境一·效能排查：網頁卡住但主機 CPU 很低。輸入 tcp.analysis.flags，看到大量黑底紅字的 TCP Retransmission。說明這是封包在中途掉包導致發送端超時重傳，是實體網路或 WiFi 訊號問題，不是程式碼當機。',
  '【8:30-11:00】情境二·傳輸安全：在區網連 HTTP 網站。過濾 http.request.method == "POST"，點開看表單欄位，帳號與密碼都是純文字。透過實際抓包讓大家看到未加密通訊的風險，說明為什麼現在網站都必須改用 HTTPS。',
  '【11:00-12:30】實用功能·Follow TCP Stream：解決封包被切成幾十個碎片難以連續看的問題。右鍵點選 Follow TCP Stream，紅色是 Client 送的、藍色是 Server 回的，像聊天紀錄一樣一目了然，查 API 參數非常方便。',
  '【12:30-14:00】加密對比：HTTPS 下 Wireshark 還能看到什麼。雖然內容加密看不到完整網址和 Payload，但依然看得到連線的 IP、Port、域名 (SNI)、連線時間與流量大小，對判斷連線對象依然很有用。',
  '【14:00-16:00】情境三·異常外連：電腦待機沒人在用，網卡卻持續有小流量。過濾 dns 查出可疑的網域名稱查詢。說明惡意程式常會定期發送心跳連線 (C2)，只要有上網就一定要過網卡，可以從封包抓出連線目標並阻斷。',
  '【16:00-17:30】AI 協同：不用死背一堆過濾標籤。實務上只要把想要查的條件（IP、Port、方法）告訴 AI，讓 AI 轉成 Display Filter。示範三組常見 Prompt，複製貼上即可開始排查。',
  '【17:30-19:00】課後思考互動：帶三個常見問題與台下互動。Q1 前後端確認用 Follow TCP Stream；Q2 HTTPS 看中繼資料 (IP/SNI)；Q3 大量 TCP 重傳代表網路掉包而非主機算力不足。',
  '【19:00-20:00】總結與 Q&A：以封包事實為準、語法交給 AI、善用 Follow Stream。推薦 Wireshark 官方 Sample Captures 抓包庫，進入問答交流環節。',
];

export default [
  SlideCover,
  SlideMentalModel,
  SlideRoleSpectrum,
  SlideUiDissection,
  SlideScenarioPerformance,
  SlideScenarioSecurity,
  SlideFollowStream,
  SlideEncryptionBoundary,
  SlideScenarioThreat,
  SlideAiWorkflow,
  SlideCheckpoints,
  SlideSummary,
] satisfies Page[];