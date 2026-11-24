import type { ReactNode } from 'react';
import type { DesignSystem, Page } from '@open-slide/core';
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

const fontMono = 'Consolas, ui-monospace, SFMono-Regular, Menlo, monospace';

const Title = ({ children }: { children: ReactNode }) => (
  <h1
    style={{
      margin: 0,
      fontFamily: 'var(--osd-font-display)',
      fontSize: 68,
      fontWeight: 900,
      lineHeight: 1.13,
      letterSpacing: '-0.035em',
      color: 'var(--osd-text)',
    }}
  >
    {children}
  </h1>
);

const Footer = () => {
  const { current, total } = useSlidePageNumber();
  return (
    <div
      style={{
        position: 'absolute',
        left: 118,
        right: 118,
        bottom: 45,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontSize: 18,
        color: '#737572',
      }}
    >
      <span>CDX Lab 教學</span>
      <span style={{ fontFamily: 'Consolas, ui-monospace, monospace' }}>
        {current}/{total}
      </span>
    </div>
  );
};

const Eyebrow = ({ children }: { children: ReactNode }) => (
  <div style={{ fontSize: 25, fontWeight: 900, color: '#e24227', letterSpacing: '0.03em' }}>
    {children}
  </div>
);

const AccentBar = ({ width = 720 }: { width?: number }) => (
  <div style={{ width, height: 26, borderRadius: 999, background: '#e24227' }} />
);

const root = {
  position: 'relative' as const,
  width: '100%',
  height: '100%',
  overflow: 'hidden',
  background: 'var(--osd-bg)',
  color: 'var(--osd-text)',
  fontFamily: 'var(--osd-font-body)',
};

const Card = ({ children, border = '#d9d2c7' }: { children: ReactNode; border?: string }) => (
  <div
    style={{
      border: `2px solid ${border}`,
      background: '#fffdf8',
      borderRadius: 24,
      padding: 34,
      boxSizing: 'border-box',
    }}
  >
    {children}
  </div>
);

const Cover: Page = () => (
  <div style={root}>
    <div style={{ position: 'absolute', left: 240, top: 248, fontSize: 28, fontWeight: 900, color: '#3d798c' }}>
      CDX 實戰教材
    </div>
    <h1
      style={{
        position: 'absolute',
        left: 240,
        top: 315,
        width: 1320,
        margin: 0,
        fontSize: 88,
        lineHeight: 1.12,
        fontWeight: 900,
        letterSpacing: '-0.045em',
      }}
    >
      CDX Lab Theme
    </h1>
    <h2
      style={{
        position: 'absolute',
        left: 240,
        top: 430,
        width: 1320,
        margin: 0,
        fontSize: 58,
        lineHeight: 1.18,
        fontWeight: 900,
        color: '#e24227',
      }}
    >
      白底、大字、紅線，讓教學脈絡站在最前面
    </h2>
    <div style={{ position: 'absolute', left: 245, top: 550 }}>
      <AccentBar width={1265} />
    </div>
    <p style={{ position: 'absolute', left: 245, top: 620, width: 1000, margin: 0, fontSize: 32, lineHeight: 1.55, color: '#737572' }}>
      從 CDX 介紹與實戰簡報抽出的可重用 Open Slide 視覺語言。
    </p>
    <div style={{ position: 'absolute', right: 210, bottom: 150, width: 280, height: 280, borderRadius: '50%', background: '#c4d6dc' }} />
    <div style={{ position: 'absolute', right: 255, bottom: 195, width: 190, height: 190, borderRadius: '50%', background: '#e24227' }} />
    <Footer />
  </div>
);

const Content: Page = () => (
  <div style={root}>
    <div style={{ position: 'absolute', left: 118, top: 74 }}>
      <Eyebrow>01 / 教學內容</Eyebrow>
    </div>
    <div style={{ position: 'absolute', left: 118, top: 118, width: 1500 }}>
      <Title>一頁只回答一個問題</Title>
    </div>
    <div style={{ position: 'absolute', left: 118, top: 226 }}>
      <AccentBar />
    </div>
    <p style={{ position: 'absolute', left: 118, top: 282, width: 1450, margin: 0, fontSize: 31, lineHeight: 1.48, color: '#737572' }}>
      文字負責建立脈絡；卡片與流程圖負責讓關係一眼可見。
    </p>
    <div style={{ position: 'absolute', left: 118, right: 118, top: 410, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 46 }}>
      <Card border="#e24227">
        <div style={{ fontSize: 24, fontWeight: 900, color: '#e24227' }}>練習者視角</div>
        <div style={{ marginTop: 38, fontSize: 42, fontWeight: 900, lineHeight: 1.25 }}>已知題目條件<br />逐步驗證機制</div>
        <div style={{ marginTop: 38, fontSize: 28, lineHeight: 1.5, color: '#737572' }}>用暖紅色標記課堂主線與關鍵步驟。</div>
      </Card>
      <Card border="#3d798c">
        <div style={{ fontSize: 24, fontWeight: 900, color: '#3d798c' }}>對照視角</div>
        <div style={{ marginTop: 38, fontSize: 42, fontWeight: 900, lineHeight: 1.25 }}>保留比較線索<br />避免概念混在一起</div>
        <div style={{ marginTop: 38, fontSize: 28, lineHeight: 1.5, color: '#737572' }}>用 teal 做第二層資訊，不搶主色焦點。</div>
      </Card>
    </div>
    <Footer />
  </div>
);

const Section: Page = () => (
  <div style={root}>
    <div style={{ position: 'absolute', left: 255, top: 318, fontSize: 88, fontWeight: 900, color: '#e24227' }}>二</div>
    <div style={{ position: 'absolute', left: 365, top: 347, fontSize: 48, fontWeight: 900 }}>.</div>
    <h1 style={{ position: 'absolute', left: 430, top: 305, width: 1180, margin: 0, fontSize: 98, lineHeight: 1.12, letterSpacing: '-0.04em', fontWeight: 900 }}>
      章節頁保留呼吸感
    </h1>
    <div style={{ position: 'absolute', left: 296, top: 504 }}>
      <AccentBar width={1328} />
    </div>
    <div style={{ position: 'absolute', left: 430, top: 580, width: 1050, fontSize: 35, lineHeight: 1.45, color: '#737572' }}>
      用大編號、句點、長紅線把課程切成清楚段落。
      <div style={{ marginTop: 46, fontFamily: fontMono, fontSize: 24, color: '#3d798c' }}>CDX / CVE / LAB</div>
    </div>
    <Footer />
  </div>
);

export default [Cover, Content, Section] satisfies Page[];
