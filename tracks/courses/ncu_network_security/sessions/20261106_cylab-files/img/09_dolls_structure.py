import io, os

W, H = 1200, 720
X0, FULL = 40, 1120
BAR = 54
ROWS_Y = [104, 244, 384, 524]

# name, size, png label, zip offset (None = unknown), child name
layers = [
    ("dolls.jpg", 651609, "PNG 594x1104", 272492, "base_images/2_c.jpg"),
    ("2_c.jpg",   383919, "PNG 526x1106", 187707, "base_images/3_c.jpg"),
    ("3_c.jpg",   201426, "PNG",          None,   "base_images/4_c.jpg"),
    ("4_c.jpg",   None,   "PNG",          None,   "flag.txt"),
]

out = []
a = out.append
a('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>dolls.jpg 結構</title><style>')
a(f'html,body{{margin:0;background:#fff}} body{{width:{W}px;height:{H}px;overflow:hidden}} svg{{display:block}}')
a('text{font-family:"Microsoft JhengHei","Noto Sans TC",sans-serif;font-size:18px;fill:#1f2328}')
a('.mono{font-family:Consolas,"Cascadia Mono",monospace;font-size:16px} .title{font-size:20px;font-weight:700} .small{font-size:15px;fill:#57606a}')
a('.png{fill:#dbeafe;stroke:#1d4ed8;stroke-width:2} .zip{fill:#fef3c7;stroke:#b45309;stroke-width:2}')
a('.unk{fill:#f3f4f6;stroke:#6b7280;stroke-width:2;stroke-dasharray:8 6} .flag{fill:#dcfce7;stroke:#15803d;stroke-width:2}')
a('.iend{stroke:#1d4ed8;stroke-width:3} .guide{stroke:#b45309;stroke-width:1.5;stroke-dasharray:4 5;fill:none}')
a('.arrow{stroke:#57606a;stroke-width:2;fill:none} .ah{fill:#57606a}')
a('</style></head><body>')
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>')

# legend
a('<rect x="40" y="22" width="26" height="18" class="png"/><text x="74" y="37">PNG（看圖軟體只畫這一段）</text>')
a('<line x1="330" y1="22" x2="330" y2="40" class="iend"/><text x="340" y="37">IEND</text>')
a('<rect x="420" y="22" width="26" height="18" class="zip"/><text x="454" y="37">zip：裡面就是下一層。每一層都是上一層 zip 的內容，所以一層比一層小</text>')

x, w = X0, FULL
for i, (name, size, png, off, child) in enumerate(layers):
    y = ROWS_Y[i]
    known = off is not None
    frac = off / size if known else 0.5
    pw = round(w * frac)
    zx, zw = x + pw, w - pw
    # label: above the bar for the first row, to the left for the rest
    if i == 0:
        a(f'<text x="{x}" y="{y - 12}" class="title">{name}</text>')
        a(f'<text x="{x + 100}" y="{y - 12}" class="mono small">{size} bytes</text>')
    else:
        a(f'<text x="{x - 14}" y="{y + 24}" class="title" text-anchor="end">{name}</text>')
        if size:
            a(f'<text x="{x - 14}" y="{y + 46}" class="mono small" text-anchor="end">{size} bytes</text>')
    a(f'<rect x="{x}" y="{y}" width="{pw}" height="{BAR}" class="png"/>')
    a(f'<rect x="{zx}" y="{y}" width="{zw}" height="{BAR}" class="{"zip" if known else "unk"}"/>')
    a(f'<line x1="{zx}" y1="{y - 6}" x2="{zx}" y2="{y + BAR + 6}" class="iend"/>')
    a(f'<text x="{x + 12}" y="{y + 33}" class="mono">0  {png}</text>')
    a(f'<text x="{zx + 12}" y="{y + 23}" class="mono">{off if known else "?"}  zip</text>')
    a(f'<text x="{zx + 12}" y="{y + 45}" class="mono">{child}</text>')
    # guides from this zip down to the next row, and the arrow
    ny = ROWS_Y[i + 1] if i + 1 < len(layers) else y + 140
    a(f'<path d="M {zx} {y + BAR} L {zx} {ny}" class="guide"/>')
    a(f'<path d="M {zx + zw} {y + BAR} L {zx + zw} {ny}" class="guide"/>')
    mx = zx + zw // 2
    a(f'<path d="M {mx} {y + BAR + 6} L {mx} {ny - 8}" class="arrow" marker-end="url(#ah)"/>')
    if i == 0:
        a(f'<text x="{mx + 12}" y="{(y + BAR + ny) // 2 + 5}" class="small">拆出來，回到步驟 1</text>')
    x, w = zx, zw

# flag box under the last zip
fy = ROWS_Y[-1] + 140
fw = max(w, 150)
fx = min(x + w // 2 - fw // 2, X0 + FULL - fw)
a(f'<rect x="{fx}" y="{fy}" width="{fw}" height="34" class="flag"/>')
a(f'<text x="{fx + fw // 2}" y="{fy + 23}" class="mono" text-anchor="middle">flag.txt</text>')
a(f'<text x="{fx - 14}" y="{fy + 23}" class="small" text-anchor="end">最裡面的娃娃</text>')
a('</svg></body></html>')

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), '09_dolls_structure.html')
io.open(dest, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('wrote', dest)
