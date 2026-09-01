#!/usr/bin/env python3
"""Generate placeholder isometric-diorama scene stills for the 珍丸茶室 Pearl & Co.
scroll-world demo.

These are stand-ins for the paid AI image backend (GPT Image via Higgsfield/Codex).
Each scene is themed to its section + brand accent so the full scroll-scrub flight
is real and runnable without any credits. Swap in real Higgsfield/Monid renders by
replacing assets/*.webp — the engine + config are unchanged.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

BG = (245, 237, 224)  # --sw-bg cream
W, H = 1800, 1200      # 3:2 landscape

CJK = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except OSError:
        return ImageFont.load_default()


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def iso_box(d, cx, cy, w, h, depth, base):
    """Isometric box centered at (cx, cy): diamond top + two side faces."""
    hw, hh = w / 2, h / 2
    top = shade(base, 1.25); left = shade(base, 0.70); right = shade(base, 0.50)
    d.polygon([(cx, cy - hh - depth), (cx + hw, cy - depth),
               (cx, cy + hh - depth), (cx - hw, cy - depth)], fill=top)
    d.polygon([(cx - hw, cy - depth), (cx, cy + hh - depth),
               (cx, cy + hh + depth), (cx - hw, cy + depth)], fill=left)
    d.polygon([(cx + hw, cy - depth), (cx, cy + hh - depth),
               (cx, cy + hh + depth), (cx + hw, cy + depth)], fill=right)


def ground(d, accent):
    d.ellipse([W * 0.24, H * 0.70, W * 0.76, H * 0.90], fill=shade(BG, 0.86))


def cup(d, cx, cy, accent, scale=1.0):
    """A boba cup: trapezoid body, dome lid, straw, pearls."""
    bw, th = int(150 * scale), int(300 * scale)
    top_w = int(bw * 1.25)
    tea = shade(accent, 1.15)
    body = [(cx - top_w // 2, cy - th // 2), (cx + top_w // 2, cy - th // 2),
            (cx + bw // 2, cy + th // 2), (cx - bw // 2, cy + th // 2)]
    d.polygon(body, fill=(250, 246, 240))
    # tea fill (lower ~55%)
    fill_top = cy - th // 2 + int(th * 0.45)
    tw_top = top_w - int((top_w - bw) * 0.45)
    d.polygon([(cx - tw_top // 2, fill_top), (cx + tw_top // 2, fill_top),
               (cx + bw // 2, cy + th // 2), (cx - bw // 2, cy + th // 2)], fill=tea)
    # pearls at bottom
    for (dx, dy) in [(-30, 120), (0, 130), (30, 122), (-14, 100), (16, 102)]:
        r = int(15 * scale)
        px, py = cx + int(dx * scale), cy - th // 2 + int((dy) * scale)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(60, 40, 35))
    # dome lid
    d.pieslice([cx - top_w // 2, cy - th // 2 - int(70 * scale),
                cx + top_w // 2, cy - th // 2 + int(60 * scale)], 180, 360,
               fill=shade(accent, 0.9))
    d.rectangle([cx - top_w // 2, cy - th // 2 - int(6 * scale),
                 cx + top_w // 2, cy - th // 2 + int(8 * scale)], fill=shade(accent, 0.7))
    # straw
    d.line([(cx + int(24 * scale), cy - th // 2 - int(120 * scale)),
            (cx - int(10 * scale), cy + int(60 * scale))],
           fill=shade(accent, 0.55), width=int(20 * scale))


def farm(d, a):
    # terraced tea hills: stacked green iso terraces + bushes
    cx, cy = W // 2, int(H * 0.5)
    for i, (dx, dy, w, h, dep, f) in enumerate([
            (0, 120, 720, 380, 60, 0.8), (60, 20, 560, 300, 60, 0.95),
            (120, -70, 400, 220, 55, 1.1)]):
        iso_box(d, cx + dx, cy + dy, w, h, dep, shade(a, f))
    # bushes
    for (bx, by) in [(-230, 60), (-120, 10), (10, -40), (150, -90), (280, -30)]:
        r = 34
        d.ellipse([cx + bx - r, cy + by - r, cx + bx + r, cy + by + r], fill=shade(a, 0.65))


def kitchen(d, a):
    # pearl kitchen: big pot on a stove block with brown pearls bubbling
    cx, cy = W // 2, int(H * 0.52)
    iso_box(d, cx, cy + 130, 560, 300, 70, shade(a, 0.85))          # counter
    d.ellipse([cx - 220, cy - 40, cx + 220, cy + 210], fill=shade(a, 0.55))  # pot body
    d.ellipse([cx - 220, cy - 90, cx + 220, cy + 30], fill=shade(a, 0.75))   # pot rim
    d.ellipse([cx - 190, cy - 70, cx + 190, cy + 15], fill=(70, 46, 38))     # syrup
    for (dx, dy, r) in [(-90, -40, 20), (-30, -55, 24), (40, -42, 18),
                        (95, -58, 22), (-10, -30, 16), (70, -30, 15)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(48, 32, 28))


def shop(d, a):
    # flagship tea shop: building with awning + a cup on the counter
    cx, cy = W // 2, int(H * 0.5)
    iso_box(d, cx - 60, cy + 60, 480, 300, 220, shade(a, 1.0))      # shop block
    # awning stripes
    for i in range(6):
        x0 = cx - 320 + i * 90
        col = shade(a, 1.3) if i % 2 == 0 else (250, 246, 240)
        d.polygon([(x0, cy - 150), (x0 + 90, cy - 150),
                   (x0 + 70, cy - 100), (x0 - 20, cy - 100)], fill=col)
    cup(d, cx + 250, cy + 40, a, 0.7)


def delivery(d, a):
    # delivery: an insulated box on a little cart with wheels
    cx, cy = W // 2, int(H * 0.52)
    iso_box(d, cx, cy + 40, 420, 260, 200, shade(a, 1.0))          # cooler box
    d.rectangle([cx - 70, cy - 150, cx + 70, cy - 70], fill=(250, 246, 240))  # label
    d.line([cx - 50, cy - 110, cx + 50, cy - 110], fill=shade(a, 0.5), width=10)
    for wx in (-150, 150):                                          # wheels
        d.ellipse([cx + wx - 46, cy + 180, cx + wx + 46, cy + 272], fill=(60, 52, 66))
        d.ellipse([cx + wx - 18, cy + 208, cx + wx + 18, cy + 244], fill=shade(a, 1.2))


def finale(d, a):
    cup(d, W // 2, int(H * 0.5), a, 1.35)


SCENES = {
    "farm":     ("茶園",   "01", (143, 185, 138), farm),
    "kitchen":  ("珍珠工坊", "02", (200, 138, 90),  kitchen),
    "shop":     ("旗艦茶室", "03", (155, 126, 189), shop),
    "delivery": ("外送",   "04", (126, 166, 201), delivery),
    "finale":   ("招牌",   "05", (155, 126, 189), finale),
}


def render(name, out):
    label, num, accent, draw_fn = SCENES[name]
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    ground(d, accent)
    draw_fn(d, accent)
    d.text((64, 60), label, font=font(CJK, 92), fill=(58, 46, 72))
    d.text((66, 176), f"{num} / 05 · 珍丸茶室", font=font(CJK, 40), fill=(122, 108, 133))
    d.text((66, 240), "Pearl & Co.", font=font(LATIN, 34), fill=shade(accent, 0.6))
    im.save(out)
    print("still", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for name in SCENES:
        render(name, f"{out}/{name}.png")
