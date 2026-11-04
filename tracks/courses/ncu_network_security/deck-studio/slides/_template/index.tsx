import type { CSSProperties, ReactNode } from 'react';
import type { DesignSystem, Page, SlideMeta, SlideTransition } from '@open-slide/core';
import { useSlidePageNumber } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#f8f4ed', text: '#202020', accent: '#e24227' },
  fonts: {
    display: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
    body: 'jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif',
  },
  typeScale: { hero: 118, body: 36 },
  radius: 28,
};

export const meta: SlideMeta = {
  title: 'TEMPLATE_Base-Deck：技術簡報標準範本',
  createdAt: '2026-10-02T22:30:00.000Z',
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

/* =========================================================================
   資安與工程語意色彩系統
   ========================================================================= */
export const c = {
  bg: '#f8f4ed',
  text: '#1a1a1a',
  cream: '#fffdf9',
  gray: '#555855',
  line: '#ded6cb',

  // 語意色彩
  accent: '#e24227',      // 🔴 漏洞根因、攻擊行為、越界危害
  accentDark: '#b82a16',
  redSoft: '#fdebe6',

  green: '#1e7532',       // 🟢 安全防禦、版本修復、驗證成功 (200 OK)
  greenSoft: '#e4f5e7',

  amber: '#b8721d',       // 🟡 機制分流、協定陷阱 (500 錯誤)、警示
  amberSoft: '#faeedb',

  teal: '#2b6e82',        // 🔵 基礎工具、架構導覽、客觀機制
  tealSoft: '#e5f0f3',

  purple: '#603d94',      // 🟣 權限提權 (LPE)、互動式反向連線
  purpleSoft: '#f0e9fa',

  termBg: '#1b2127',
  termText: '#f0f6fc',
};

export const font = {
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

const Footer = ({ moduleName = '技術教學 ｜ 工程化標準' }: { moduleName?: string }) => {
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
        fontSize: 22,
        color: c.gray,
      }}
    >
      <span>{moduleName}</span>
      <span style={{ fontFamily: font.mono, fontWeight: 700 }}>
        Page · {current} / {total}
      </span>
    </div>
  );
};

const AccentBar = ({ width = 680, color = c.accent }: { width?: number; color?: string }) => (
  <div style={{ width, height: 18, borderRadius: 999, background: color }} />
);

export const Frame = ({
  eyebrow,
  title,
  accentColor = c.teal,
  phaseTag,
  children,
}: {
  eyebrow: string;
  title: ReactNode;
  accentColor?: string;
  phaseTag?: string;
  children: ReactNode;
}) => (
  <div style={fill}>
    <Styles />
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 45,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
      }}
    >
      {phaseTag && (
        <span
          style={{
            background: accentColor,
            color: '#fff',
            fontSize: 22,
            fontWeight: 900,
            padding: '4px 16px',
            borderRadius: 8,
          }}
        >
          {phaseTag}
        </span>
      )}
      <span style={{ fontSize: 28, fontWeight: 900, color: accentColor }}>
        {eyebrow}
      </span>
    </div>
    <h1
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 95,
        width: 1560,
        margin: 0,
        fontFamily: font.display,
        fontSize: 56,
        fontWeight: 900,
        lineHeight: 1.15,
        letterSpacing: '-0.03em',
      }}
    >
      {title}
    </h1>
    <div style={{ position: 'absolute', left: 110, top: 182 }}>
      <AccentBar width={680} color={accentColor} />
    </div>
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 225,
        bottom: 75,
      }}
    >
      {children}
    </div>
    <Footer />
  </div>
);

/**
 * 預設隨內容自動收縮的 Card 元件（防範死空間問題）
 */
export const Card = ({
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
      padding: '32px 36px',
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
      ...style,
    }}
  >
    {children}
  </div>
);

export const Badge = ({
  children,
  color = c.accent,
  bg = c.redSoft,
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
      padding: '8px 24px',
      borderRadius: 999,
      background: bg,
      color,
      fontSize: 26,
      fontWeight: 900,
      alignSelf: 'flex-start',
    }}
  >
    {children}
  </span>
);

export const CodeBlock = ({
  children,
  title,
  lang = 'bash',
  fontSize = 28,
  style,
}: {
  children: string;
  title?: string;
  lang?: string;
  fontSize?: number;
  style?: CSSProperties;
}) => (
  <div
    style={{
      borderRadius: 16,
      overflow: 'hidden',
      background: c.termBg,
      border: '2px solid #363e46',
      fontFamily: font.mono,
      fontSize,
      color: c.termText,
      boxSizing: 'border-box',
      ...style,
    }}
  >
    {title && (
      <div
        style={{
          background: '#15191d',
          padding: '10px 20px',
          borderBottom: '2px solid #363e46',
          fontSize: 22,
          fontWeight: 700,
          color: '#9ba5b0',
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <span>{title}</span>
        <span style={{ textTransform: 'uppercase' }}>{lang}</span>
      </div>
    )}
    <pre
      style={{
        margin: 0,
        padding: '20px 26px',
        lineHeight: 1.45,
        whiteSpace: 'pre-wrap',
        fontFamily: font.mono,
      }}
    >
      {children}
    </pre>
  </div>
);

/* =========================================================================
   版型 1: 封面範例
   ========================================================================= */
const Slide01_Cover: Page = () => (
  <div style={fill}>
    <Styles />
    <div
      className="rise"
      style={{ position: 'absolute', left: 200, top: 160, fontSize: 36, fontWeight: 900, color: c.teal }}
    >
      技術專題 · 實戰架構
    </div>
    <h1
      className="rise"
      style={{
        position: 'absolute',
        left: 200,
        top: 230,
        width: 1450,
        margin: 0,
        fontSize: 88,
        lineHeight: 1.15,
        fontWeight: 900,
        letterSpacing: '-0.04em',
      }}
    >
      簡報主題名稱（Base Template）
    </h1>
    <h2
      className="rise"
      style={{
        position: 'absolute',
        left: 200,
        top: 360,
        width: 1350,
        margin: 0,
        fontSize: 48,
        lineHeight: 1.25,
        fontWeight: 900,
        color: c.teal,
      }}
    >
      副標題：技術機制解析與防禦性架構設計
    </h2>
    <div style={{ position: 'absolute', left: 200, top: 495 }}>
      <AccentBar width={1300} color={c.teal} />
    </div>
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 200,
        top: 565,
        fontSize: 34,
        color: c.gray,
        fontWeight: 700,
      }}
    >
      核心目標：示範零死空間、平衡視覺天平與色彩語意標準
    </div>
    <Footer />
  </div>
);

/* =========================================================================
   版型 2: 雙欄對照版（自然收縮，絕不死留白）
   ========================================================================= */
const Slide02_Comparison: Page = () => (
  <Frame
    phaseTag="機制對照"
    eyebrow="核心概念分析"
    accentColor={c.teal}
    title="雙欄對比版型：以自然高度收縮卡片"
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, alignContent: 'start' }}>
      <Card border={c.line} background={c.cream}>
        <Badge color={c.teal} bg={c.tealSoft}>
          方案 A：預設行為
        </Badge>
        <div style={{ marginTop: 20 }}>
          <CodeBlock title="輸入指令" lang="bash">
            {`curl -i http://target/normal-path`}
          </CodeBlock>
        </div>
        <div style={{ marginTop: 24, fontSize: 32, lineHeight: 1.7, color: c.text, fontWeight: 700 }}>
          • 卡片高度由內容自然決定，不強設固定高度。
          <br />
          • 當內容文字精簡時，不會在底部產生 60% 的死空間。
        </div>
      </Card>

      <Card border={c.teal} background={c.tealSoft}>
        <Badge color={c.teal} bg={c.cream}>
          方案 B：調整後行為
        </Badge>
        <div style={{ marginTop: 20 }}>
          <CodeBlock title="正確指令" lang="bash">
            {`curl -i --path-as-is http://target/raw-path`}
          </CodeBlock>
        </div>
        <div style={{ marginTop: 24, fontSize: 32, lineHeight: 1.7, color: c.text, fontWeight: 800 }}>
          • 兩側保持水平對稱與相同的視覺密度。
          <br />
          • 確保在 1080p 螢幕投影下，學員一眼即可捕捉對照差異。
        </div>
      </Card>
    </div>
  </Frame>
);

/* =========================================================================
   版型 3: 三欄矩陣版（防禦策略 / 多階段架構）
   ========================================================================= */
const Slide03_DefenseMatrix: Page = () => (
  <Frame
    phaseTag="安全防禦"
    eyebrow="防禦矩陣"
    accentColor={c.green}
    title="三欄防禦版型：安全措施統一採用綠色語意"
  >
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 32, alignContent: 'start' }}>
      <Card border={c.green} background={c.cream}>
        <div style={{ fontSize: 38, fontWeight: 900, color: c.green }}>
          1. 程式修復
        </div>
        <div style={{ marginTop: 24, fontSize: 30, lineHeight: 1.7, color: c.text, fontWeight: 700 }}>
          • 升級至官方安全版本
          <br />
          • 徹底修正核心模組邏輯
          <br />
          • 消除未授權解析的漏洞路徑
        </div>
      </Card>

      <Card border={c.green} background={c.cream}>
        <div style={{ fontSize: 38, fontWeight: 900, color: c.green }}>
          2. 設定強化
        </div>
        <div style={{ marginTop: 20 }}>
          <CodeBlock title="設定檔" lang="apache" fontSize={24}>
            {`<Directory />\n  Require all denied\n</Directory>`}
          </CodeBlock>
        </div>
        <div style={{ marginTop: 20, fontSize: 28, lineHeight: 1.6, color: c.text, fontWeight: 800 }}>
          預設關閉所有未授權目錄的讀寫存取權限。
        </div>
      </Card>

      <Card border={c.green} background={c.cream}>
        <div style={{ fontSize: 38, fontWeight: 900, color: c.green }}>
          3. 最小權限
        </div>
        <div style={{ marginTop: 24, fontSize: 30, lineHeight: 1.7, color: c.text, fontWeight: 700 }}>
          • 關閉非必要之執行模組
          <br />
          • 限縮服務行程帳號之操作範圍
          <br />
          • 阻斷跨目錄的指令執行途徑
        </div>
      </Card>
    </div>
  </Frame>
);

export default [
  Slide01_Cover,
  Slide02_Comparison,
  Slide03_DefenseMatrix,
] satisfies Page[];
