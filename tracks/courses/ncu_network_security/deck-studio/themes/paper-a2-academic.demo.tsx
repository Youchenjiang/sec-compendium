import { type DesignSystem, type Page, useSlidePageNumber } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#ffffff', text: '#000000', accent: '#f24300' },
  fonts: {
    display: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif',
    body: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif',
  },
  typeScale: { hero: 132, body: 48 },
  radius: 0,
};

const muted = '#c0c0c0';
const soft = '#f4f4f4';

const Title = ({ children }: { children: React.ReactNode }) => (
  <h1
    style={{
      fontFamily: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif',
      fontSize: 108,
      fontWeight: 800,
      lineHeight: 1.12,
      letterSpacing: 0,
      margin: 0,
      color: '#000000',
    }}
  >
    {children}
  </h1>
);

const Footer = ({ section = 'Paper A2 Academic' }: { section?: string }) => {
  const { current, total } = useSlidePageNumber();
  return (
    <div
      style={{
        position: 'absolute',
        left: 150,
        right: 150,
        bottom: 54,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontFamily: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif',
        fontSize: 32,
        color: '#c0c0c0',
      }}
    >
      <span>{section}</span>
      <span>{current}</span>
    </div>
  );
};

const Eyebrow = ({ children }: { children: React.ReactNode }) => (
  <div
    style={{
      fontFamily: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif',
      fontSize: 32,
      fontWeight: 700,
      lineHeight: 1.2,
      color: '#f24300',
    }}
  >
    {children}
  </div>
);

const Root = ({ children }: { children: React.ReactNode }) => (
  <div
    style={{
      width: '100%',
      height: '100%',
      position: 'relative',
      boxSizing: 'border-box',
      background: 'var(--osd-bg)',
      color: 'var(--osd-text)',
      fontFamily: 'var(--osd-font-body)',
    }}
  >
    {children}
  </div>
);

const Cover: Page = () => (
  <Root>
    <div style={{ position: 'absolute', left: 150, top: 42 }}>
      <Eyebrow>arXiv:2508.21579</Eyebrow>
    </div>
    <h1
      style={{
        position: 'absolute',
        left: 160,
        right: 160,
        top: 280,
        fontFamily: 'var(--osd-font-display)',
        fontSize: 'var(--osd-size-hero)',
        fontWeight: 800,
        lineHeight: 1.12,
        letterSpacing: 0,
        margin: 0,
        textAlign: 'center',
      }}
    >
      Agentic Discovery and Validation of Android App Vulnerabilities
    </h1>
    <p
      style={{
        position: 'absolute',
        right: 150,
        bottom: 150,
        fontSize: 40,
        lineHeight: 1.5,
        margin: 0,
        textAlign: 'right',
      }}
    >
      報告人：Your Name
      <br />
      報告日期：2026
    </p>
    <Footer section="" />
  </Root>
);

const SectionBreak: Page = () => (
  <Root>
    <div
      style={{
        position: 'absolute',
        left: 360,
        right: 360,
        top: 430,
        display: 'flex',
        alignItems: 'baseline',
        gap: 28,
      }}
    >
      <span
        style={{
          fontFamily: 'var(--osd-font-display)',
          fontSize: 170,
          fontWeight: 800,
          lineHeight: 1,
          color: 'var(--osd-accent)',
        }}
      >
        01.
      </span>
      <span
        style={{
          fontFamily: 'var(--osd-font-display)',
          fontSize: 108,
          fontWeight: 800,
          lineHeight: 1.08,
        }}
      >
        Motivation & Problem Formulation
      </span>
    </div>
    <Footer section="" />
  </Root>
);

const Content: Page = () => (
  <Root>
    <main style={{ position: 'absolute', left: 150, right: 150, top: 120, bottom: 120 }}>
      <Title>The Validation Gap</Title>
      <div style={{ width: 150, height: 10, background: 'var(--osd-accent)', marginTop: 34 }} />
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 72,
          marginTop: 72,
          fontSize: 'var(--osd-size-body)',
          lineHeight: 1.38,
        }}
      >
        <section>
          <Eyebrow>Definition:</Eyebrow>
          <p style={{ margin: '22px 0 0' }}>
            The gap between detecting potential issues and confirming exploitable vulnerabilities.
          </p>
        </section>
        <section style={{ background: soft, padding: 42 }}>
          <Eyebrow>A2's goal:</Eyebrow>
          <p style={{ margin: '22px 0 0' }}>
            Automate PoC generation and transform speculation into evidence.
          </p>
        </section>
      </div>
    </main>
    <Footer section="Motivation & Problem Formulation" />
  </Root>
);

export default [Cover, SectionBreak, Content];
