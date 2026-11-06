import io, sys

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
a('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>')
a('html,body{margin:0;background:#fff} body{width:%dpx;height:%dpx;overflow:hidden} svg{display:block}' % (W, H))
a('text{font-family:"Microsoft JhengHei","Noto Sans TC",sans-serif;font-size:18px;fill:#1f2328}')
a('.mono{font-family:Consolas,"Cascadia Mono",monospace;font-size:16px} .title{font-size:20px;font-weight:700} .small{font-size:15px;fill:#57606a}')
a('.png{fill:#dbeafe;stroke:#1d4ed8;stroke-width:2} .zip{fill:#fef3c7;stroke:#b45309;stroke-width:2}')
a('.unk{fill:#f3f4f6;stroke:#6b7280;stroke-width:2;stroke-dasharray:8 6} .flag{fill:#dcfce7;stroke:#15803d;stroke-width:2}')
a('.iend{stroke:#1d4ed8;stroke-width:3} .guide{stroke:#b45309;stroke-width:1.5;stroke-dasharray:4 5;fill:none}')
a('.arrow{stroke:#57606a;stroke-width:2;fill:none} .ah{fill:#57606a}')
a('</style></head><body>')
a('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H))
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
        a('<text x="%d" y="%d" class="title">%s</text>' % (x, y - 12, name))
        a('<text x="%d" y="%d" class="mono small">%d bytes</text>' % (x + 100, y - 12, size))
    else:
        a('<text x="%d" y="%d" class="title" text-anchor="end">%s</text>' % (x - 14, y + 24, name))
        if size:
            a('<text x="%d" y="%d" class="mono small" text-anchor="end">%d bytes</text>' % (x - 14, y + 46, size))
    a('<rect x="%d" y="%d" width="%d" height="%d" class="png"/>' % (x, y, pw, BAR))
    a('<rect x="%d" y="%d" width="%d" height="%d" class="%s"/>' % (zx, y, zw, BAR, 'zip' if known else 'unk'))
    a('<line x1="%d" y1="%d" x2="%d" y2="%d" class="iend"/>' % (zx, y - 6, zx, y + BAR + 6))
    a('<text x="%d" y="%d" class="mono">0  %s</text>' % (x + 12, y + 33, png))
    a('<text x="%d" y="%d" class="mono">%s  zip</text>' % (zx + 12, y + 23, off if known else '?'))
    a('<text x="%d" y="%d" class="mono">%s</text>' % (zx + 12, y + 45, child))
    # guides from this zip down to the next row, and the arrow
    ny = ROWS_Y[i + 1] if i + 1 < len(layers) else y + 140
    a('<path d="M %d %d L %d %d" class="guide"/>' % (zx, y + BAR, zx, ny))
    a('<path d="M %d %d L %d %d" class="guide"/>' % (zx + zw, y + BAR, zx + zw, ny))
    mx = zx + zw // 2
    a('<path d="M %d %d L %d %d" class="arrow" marker-end="url(#ah)"/>' % (mx, y + BAR + 6, mx, ny - 8))
    if i == 0:
        a('<text x="%d" y="%d" class="small">拆出來，回到步驟 1</text>' % (mx + 12, (y + BAR + ny) // 2 + 5))
    x, w = zx, zw

# flag box under the last zip
fy = ROWS_Y[-1] + 140
fw = max(w, 150)
fx = min(x + w // 2 - fw // 2, X0 + FULL - fw)
a('<rect x="%d" y="%d" width="%d" height="34" class="flag"/>' % (fx, fy, fw))
a('<text x="%d" y="%d" class="mono" text-anchor="middle">flag.txt</text>' % (fx + fw // 2, fy + 23))
a('<text x="%d" y="%d" class="small" text-anchor="end">最裡面的娃娃</text>' % (fx - 14, fy + 23))
a('</svg></body></html>')

io.open(sys.argv[1], 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('wrote', sys.argv[1])
