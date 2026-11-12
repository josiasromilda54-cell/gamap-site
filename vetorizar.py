# Vetoriza o logo GAMAP: rastreia os cortes exatos da imagem e gera SVG flat
import colorsys
import numpy as np
import potrace
from PIL import Image

IMG = r"C:\Users\romil\projetos\gamap-site\assets\obras\logo.jpg"
OUT = r"C:\Users\romil\projetos\gamap-site\assets\logo-flat.svg"
SCALE = 4  # trabalhar 4x maior (600px) para traço mais limpo

img = Image.open(IMG).convert("RGB")
w, h = img.size
img = img.resize((w * SCALE, h * SCALE), Image.LANCZOS)
W, H = img.size
px = img.load()

blue = np.zeros((H, W), dtype=bool)
silver = np.zeros((H, W), dtype=bool)

for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if v < 0.28 and s < 0.5:
            continue  # fundo escuro
        if s >= 0.38 and 0.5 <= hh <= 0.72:
            blue[y, x] = True
        elif v > 0.38:
            silver[y, x] = True

def trace(mask, turd=6):
    bmp = potrace.Bitmap(mask)
    plist = bmp.trace(turdsize=turd, alphamax=1.0, opttolerance=0.2)
    d = []
    for curve in plist.curves:
        sp = curve.start_point
        d.append(f"M{sp.x:.1f},{sp.y:.1f}")
        for seg in curve.segments:
            if seg.is_corner:
                c, e = seg.c, seg.end_point
                d.append(f"L{c.x:.1f},{c.y:.1f}L{e.x:.1f},{e.y:.1f}")
            else:
                c1, c2, e = seg.c1, seg.c2, seg.end_point
                d.append(f"C{c1.x:.1f},{c1.y:.1f} {c2.x:.1f},{c2.y:.1f} {e.x:.1f},{e.y:.1f}")
        d.append("Z")
    return " ".join(d)

d_blue = trace(blue)
d_silver = trace(silver)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
  <!-- azul: tudo que era azul no original (anel, prédios) -->
  <path d="{d_blue}" fill="#1e78d0" fill-rule="evenodd"/>
  <!-- ex-prateado: tons azuis claros no lugar do metal -->
  <path d="{d_silver}" fill="#3fb0ff" fill-rule="evenodd"/>
</svg>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"OK: {W}x{H}px -> {OUT}")
print(f"azul: {len(d_blue)//1000}k chars | ex-prata: {len(d_silver)//1000}k chars")
