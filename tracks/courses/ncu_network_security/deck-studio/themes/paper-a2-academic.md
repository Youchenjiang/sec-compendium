---
name: Paper A2 Academic
description: A clean academic-report theme with white canvas, black typography, and sharp orange section accents.
---

# Paper A2 Academic

## Palette

| Role   | Value     | Notes                                   |
| ------ | --------- | --------------------------------------- |
| bg     | `#ffffff` | plain slide background                  |
| text   | `#000000` | titles and primary body copy            |
| accent | `#f24300` | section numbers, rules, key labels      |
| muted  | `#c0c0c0` | page markers and quiet secondary chrome |
| soft   | `#f4f4f4` | light blocks for diagrams or callouts   |

## Typography

- Display font: `"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif` — weight 700-800 for titles.
- Body font: `"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif` — weight 400-500.
- Type-scale overrides:
  - Hero title: 132 px
  - Section number/title: 170 px
  - Page heading: 108 px
  - Body text: 48 px
  - Detail text: 27 px
  - Footer: 32 px

## Layout

- Content padding: 150 px from canvas edges on content pages.
- Cover alignment: centered title block, small source label at top left, presenter/date block at bottom right.
- Content alignment: left-aligned title, two-column body area when comparing concepts, otherwise one strong column.
- Section dividers: giant orange number followed by black section title, centered vertically.
- Footer: left section label plus right page count; keep it quiet and gray.

## Fixed components

These are paste-ready. Copy them verbatim into a slide that uses this theme.

### Title

```tsx
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
```

### Footer

Pull the page number from `useSlidePageNumber()` — never hardcode `pageNum` / `total` props.

```tsx
import { useSlidePageNumber } from '@open-slide/core';

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
```

### Eyebrow / accents

```tsx
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
```

## Motion

- Philosophy: static — this theme should feel like a clear conference or paper-reading deck, not a product demo.

## Aesthetic

White academic canvas, assertive black typography, and sparse orange markers. It draws from paper-presentation decks: section-number dividers, high-contrast headings, minimal decoration, and diagram-friendly whitespace. Avoid gradients, rounded UI cards, decorative imagery, and playful iconography; use rules, labels, and deliberate spacing instead.

## Example usage

```tsx
const Cover: Page = () => (
  <div style={{ width: '100%', height: '100%', background: '#ffffff', color: '#000000', padding: 150, position: 'relative', fontFamily: '"Microsoft JhengHei", "微軟正黑體", Arial, sans-serif' }}>
    <Eyebrow>arXiv:2508.21579</Eyebrow>
    <h1 style={{ fontSize: 132, fontWeight: 800, lineHeight: 1.12, maxWidth: 1500, margin: '210px auto 0', textAlign: 'center' }}>
      Agentic Discovery and Validation
    </h1>
    <p style={{ position: 'absolute', right: 150, bottom: 150, fontSize: 40, lineHeight: 1.5, margin: 0, textAlign: 'right' }}>
      報告人：Your Name<br />報告日期：2026
    </p>
    <Footer section="" />
  </div>
);
```
