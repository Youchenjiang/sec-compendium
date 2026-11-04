---
name: CDX Lab
description: Warm off-white cyber-range teaching slides with bold black headings, orange-red bars, chapter dividers, and restrained teal support accents.
mode: light
---

# CDX Lab

## Palette

| Role | Value | Notes |
| --- | --- | --- |
| bg | `#f8f4ed` | warm off-white page background |
| text | `#202020` | primary headings and body copy |
| accent | `#e24227` | main orange-red emphasis, bars, chapter numbers |
| accent-dark | `#bc2f20` | deeper red for secondary emphasis |
| teal | `#3d798c` | supporting contrast for alternate paths / concepts |
| muted | `#737572` | secondary copy and footer text |
| line | `#d9d2c7` | card outlines and dividers |
| cream | `#fffdf8` | card fill |
| teal-soft | `#d9e8ec` | teal callout background |
| blue-soft | `#c4d6dc` | circular decoration and cool support fill |
| green | `#5f8e69` | success / completed state |
| green-soft | `#d9ead3` | success card background |

## Typography

- Display font: `jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif` — weight 900 for titles and chapter pages.
- Body font: `jf open 粉圓 1.1, Microsoft JhengHei, Noto Sans CJK TC, system-ui, sans-serif` — weight 400–500 for explanation copy, 900 for callout labels.
- Monospace: `Consolas, ui-monospace, SFMono-Regular, Menlo, monospace` for URLs, commands, CVEs, page counters, and filesystem paths.
- Type-scale overrides:
  - Cover title: 88 px
  - Section title: 98 px
  - Page heading: 68 px
  - Lead text: 31–35 px
  - Body text: 29–36 px
  - Label / caption: 18–25 px

## Layout

- Canvas: 1920 × 1080.
- Content padding: 118 px on normal content pages; cover content starts around 240 px for the quieter opening composition.
- Alignment: predominantly left-aligned.
- Normal page rhythm: eyebrow at y≈74, title at y≈118, orange-red bar at y≈226, lead at y≈282, main content from y≈400.
- Chapter divider rhythm: large Chinese numeral at x≈255, dot separator, chapter title beginning around x≈430, long orange-red bar beneath.
- Content pages favor two-column comparisons, horizontal process flows, or 2–4 bordered cards. Use generous negative space instead of filling every area.
- Decorative geometry is restrained: one or two flat circles or rounded bars, never gradients.

## Fixed components

These are paste-ready. Copy them verbatim into a slide that uses this theme.

### Title

```tsx
import type { ReactNode } from 'react';

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
```

### Footer

Pull the page number from `useSlidePageNumber()` — never hardcode page totals.

```tsx
import { useSlidePageNumber } from '@open-slide/core';

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
```

### Eyebrow / accents

```tsx
import type { ReactNode } from 'react';

const Eyebrow = ({ children }: { children: ReactNode }) => (
  <div style={{ fontSize: 25, fontWeight: 900, color: '#e24227', letterSpacing: '0.03em' }}>
    {children}
  </div>
);

const AccentBar = ({ width = 720 }: { width?: number }) => (
  <div style={{ width, height: 26, borderRadius: 999, background: '#e24227' }} />
);
```

## Motion

- Philosophy: subtle — content rises a few pixels and fades in, preserving the reference deck's static classroom feel.
- Keep transitions around 220 ms and movement under 14 px.

```css
@keyframes rise {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## Aesthetic

Warm classroom handout meets clean cyber-range instruction. The composition should feel close to the original `CDX 介紹與實戰.pptx`: large black Chinese headings, a strong orange-red line as the recurring visual anchor, chapter pages with oversized numerals, and diagrams made from simple bordered boxes. Keep the deck bright, flat, and legible on a projector. Avoid gradients, dark neon cyberpunk styling, dense dashboards, excessive icons, and decorative effects that compete with the teaching sequence.

## Example usage

```tsx
const Content: Page = () => (
  <div style={{ width: '100%', height: '100%', background: 'var(--osd-bg)', color: 'var(--osd-text)', position: 'relative' }}>
    <div style={{ position: 'absolute', left: 118, top: 74 }}>
      <Eyebrow>01 / 核心概念</Eyebrow>
    </div>
    <div style={{ position: 'absolute', left: 118, top: 118, width: 1500 }}>
      <Title>先理解路徑，再看漏洞</Title>
    </div>
    <div style={{ position: 'absolute', left: 118, top: 226 }}>
      <AccentBar />
    </div>
    <p style={{ position: 'absolute', left: 118, top: 282, width: 1450, margin: 0, fontSize: 31, lineHeight: 1.48, color: '#737572' }}>
      把必要背景放在剛好用到的地方，讓每一張投影片只回答一個問題。
    </p>
    <Footer />
  </div>
);
```
