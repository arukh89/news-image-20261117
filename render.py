#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261117.

Build-time only: run locally with Pillow to produce entry.png, the file the
graded program (main.ts) copies to /output/entry.png. The drawing is fully
original flat vector-style art made with Pillow shapes and system fonts; no
photograph, stock art, logo or copied artwork is used anywhere.

Content: only events that happened, or were first reported, on Tuesday
17 November 2026, each cross-checked against several news reports that day:
  1. U.S. strikes on a missile launch site on Iran's Qeshm Island, in the
     Strait of Hormuz, as commercial shipping came under attack.
  2. A road span of the Crimean (Kerch) Bridge collapsed after a Ukrainian
     strike; Kyiv's Northern and Southern bridges were closed after Russian
     missile strikes.
  3. Japan scrambled fighter jets after two suspected Russian aircraft
     entered its airspace near Okinoshima, Fukuoka; Tokyo lodged a protest.
  4. The U.S. lost its measles elimination status: PAHO declared measles
     endemic again after 26 years, with 5,412 cases in 2026.
  Briefs: Quad leaders met in Manila for the first time since 2024; the
  first Xi-Trump-Putin meeting was set for Thursday in Shenzhen.

Deterministic: fixed geometry, fixed fonts, fixed palette, no clock, no
randomness, no network. Re-running produces byte-identical output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
NAVY = (31, 58, 95)
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def centre(draw, y, s, f, fill, cx=W // 2):
    draw.text((cx - text_w(draw, s, f) // 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, s, name, start, max_w):
    size = start
    while size > 10 and text_w(draw, s, font(name, size)) > max_w:
        size -= 2
    return font(name, size)


def jet(draw, x, y, scale, fill, flip=False):
    """Simple fighter-jet silhouette, drawn from polygons. Original art.
    Side view, nose pointing right: fuselage, swept wing, tail fin."""
    body = [(0, 8), (34, 4), (58, 8), (34, 12), (8, 13)]
    wing = [(22, 10), (36, 10), (28, 26), (16, 26)]
    tail = [(4, 8), (12, 8), (6, 0), (0, 0)]
    parts = [body, wing, tail]
    if flip:
        parts = [[(-px, py) for px, py in part] for part in parts]
    for part in parts:
        draw.polygon([(x + px * scale, y + py * scale) for px, py in part], fill=fill)


def waves(draw, x0, y, x1, colour, amp=5, step=26):
    for x in range(x0, x1 - step, step):
        draw.arc([x, y, x + step, y + amp * 2], 200, 340, fill=colour, width=3)


def draw_qeshm(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(223, 150, 90))
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=NAVY)
    # Low coastal strip with small buildings and a tower.
    draw.rectangle([x + 24, y + h - 84, x + 250, y + h - 52], fill=(64, 48, 36))
    draw.rectangle([x + 52, y + h - 108, x + 84, y + h - 84], fill=(64, 48, 36))
    draw.rectangle([x + 120, y + h - 100, x + 146, y + h - 84], fill=(64, 48, 36))
    draw.rectangle([x + 196, y + h - 116, x + 206, y + h - 84], fill=(64, 48, 36))
    draw.polygon([(x + 192, y + h - 116), (x + 210, y + h - 116), (x + 201, y + h - 130)],
                 fill=(64, 48, 36))
    # Smoke plumes rising from the shore.
    for cx, cy, r in [(x + 100, y + 30, 21), (x + 128, y + 16, 15), (x + 152, y + 34, 18)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    # Jet overhead.
    jet(draw, x + 330, y + 24, 1.1, INK)
    # Tanker on the water.
    draw.polygon([(x + 300, y + h - 30), (x + 452, y + h - 30), (x + 438, y + h - 10),
                  (x + 314, y + h - 10)], fill=(40, 40, 40))
    draw.rectangle([x + 330, y + h - 46, x + 356, y + h - 30], fill=RED)
    draw.rectangle([x + 362, y + h - 46, x + 388, y + h - 30], fill=(240, 200, 80))
    waves(draw, x + 16, y + h - 40, x + 280, (255, 255, 255))


def draw_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(217, 230, 242))
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(46, 109, 164))
    # Bridge deck in two segments with a broken gap in the middle.
    deck_y = y + 62
    draw.rectangle([x + 16, deck_y, x + 200, deck_y + 14], fill=INK)
    draw.rectangle([x + 274, deck_y, x + 458, deck_y + 14], fill=INK)
    # Jagged broken ends facing the gap.
    draw.polygon([(x + 200, deck_y), (x + 214, deck_y + 7), (x + 200, deck_y + 14)],
                 fill=INK)
    draw.polygon([(x + 274, deck_y), (x + 260, deck_y + 7), (x + 274, deck_y + 14)],
                 fill=INK)
    # Piers holding each segment.
    for px in (x + 60, x + 140, x + 320, x + 400):
        draw.rectangle([px, deck_y + 14, px + 12, y + h - 52], fill=INK)
    # The fallen span, tilted into the water below the gap, with a splash.
    draw.polygon([(x + 208, deck_y + 34), (x + 266, deck_y + 58),
                  (x + 260, deck_y + 70), (x + 202, deck_y + 46)], fill=(90, 90, 90))
    draw.arc([x + 216, y + h - 66, x + 258, y + h - 34], 180, 360, fill=WHITE, width=4)
    waves(draw, x + 16, y + h - 40, x + 458, (255, 255, 255))


def draw_japan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(253, 246, 227))
    # Red sun disc, fully inside the sky.
    draw.ellipse([x + 300, y + 14, x + 420, y + 134], fill=(200, 40, 40))
    # Two jets flying in formation.
    jet(draw, x + 196, y + 66, 1.25, INK)
    jet(draw, x + 104, y + 38, 1.05, (70, 70, 70))
    # Sea and island at the bottom.
    draw.rectangle([x, y + h - 36, x + w, y + h], fill=(46, 109, 164))
    draw.polygon([(x + 30, y + h - 36), (x + 90, y + h - 64), (x + 150, y + h - 36)],
                 fill=(64, 90, 60))
    waves(draw, x + 180, y + h - 28, x + 458, (255, 255, 255))


def draw_measles(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(234, 243, 236))
    # Abstract virus: spiked disc, drawn from lines and circles.
    cx, cy, r = x + 150, y + 76, 44
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12
        x1, y1 = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        x2, y2 = cx + int((r + 16) * math.cos(a)), cy + int((r + 16) * math.sin(a))
        draw.line([x1, y1, x2, y2], fill=(192, 57, 43), width=5)
        draw.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(192, 57, 43))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 110, 100))
    draw.ellipse([cx - r + 12, cy - r + 12, cx - r + 29, cy - r + 29], fill=(192, 57, 43))
    draw.ellipse([cx + 7, cy + 5, cx + 26, cy + 24], fill=(192, 57, 43))
    # Badge: 26 years.
    bx, by = x + 316, y + 76
    draw.ellipse([bx - 56, by - 56, bx + 56, by + 56], fill=NAVY)
    draw.ellipse([bx - 56, by - 56, bx + 56, by + 56], outline=WHITE, width=3)
    f_big = font(SANS_B, 40)
    f_small = font(SANS_B, 18)
    centre(draw, by - 38, "26", f_big, WHITE, cx=bx)
    centre(draw, by + 8, "YEARS", f_small, WHITE, cx=bx)


def card(draw, x, y, w, h, tag, tag_fill, headline, subhead, art):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3)
    art(draw, x + 3, y + 3, w - 6, 150)
    draw.rectangle([x + 3, y + 153, x + w - 3, y + 156], fill=INK)
    ty = y + 168
    f_tag = font(SANS_B, 19)
    tw = text_w(draw, tag, f_tag) + 24
    draw.rounded_rectangle([x + 20, ty, x + 20 + tw, ty + 30], radius=15, fill=tag_fill)
    draw.text((x + 32, ty + 4), tag, font=f_tag, fill=WHITE)
    f_head = font(SANS_B, 31)
    lines = wrap(draw, headline, f_head, w - 40)
    hy = ty + 42
    for line in lines[:2]:
        draw.text((x + 20, hy), line, font=f_head, fill=INK)
        hy += 38
    f_sub = font(SANS, 21)
    sub_lines = wrap(draw, subhead, f_sub, w - 40)
    sy = hy + 4
    for line in sub_lines[:2]:
        draw.text((x + 20, sy), line, font=f_sub, fill=(60, 60, 60))
        sy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Masthead.
    draw.rectangle([28, 24, W - 28, 26], fill=INK)
    f_kick = font(SANS_B, 22)
    centre(draw, 36, "W O R L D   N E W S   •   O N E   D A Y   •   O N E   I M A G E",
           f_kick, RED)
    f_date = fit_font(draw, "TUESDAY 17 NOVEMBER 2026", SERIF_B, 64, W - 56)
    centre(draw, 66, "TUESDAY 17 NOVEMBER 2026", f_date, INK)
    draw.rectangle([28, 142, W - 28, 146], fill=RED)
    draw.rectangle([28, 150, W - 28, 152], fill=INK)
    # Story grid.
    gx, gy, gap = 28, 164, 16
    cw = (W - 2 * gx - gap) // 2
    ch = 356
    card(draw, gx, gy, cw, ch, "MIDDLE EAST", NAVY,
         "U.S. STRIKES QESHM ISLAND",
         "Missile site hit in the Strait of Hormuz as shipping comes under attack.",
         draw_qeshm)
    card(draw, gx + cw + gap, gy, cw, ch, "UKRAINE", (70, 90, 140),
         "CRIMEA BRIDGE SPAN FALLS",
         "Road arch collapses after Ukrainian strike; Kyiv bridges shut.",
         draw_bridge)
    card(draw, gx, gy + ch + gap, cw, ch, "EAST ASIA", (160, 60, 60),
         "JAPAN SCRAMBLES FIGHTER JETS",
         "Two suspected Russian planes breach airspace; Tokyo protests.",
         draw_japan)
    card(draw, gx + cw + gap, gy + ch + gap, cw, ch, "HEALTH", (50, 110, 70),
         "U.S. LOSES MEASLES-FREE STATUS",
         "PAHO: measles endemic again after 26 years; 5,412 cases in 2026.",
         draw_measles)
    # Footer briefs.
    fy = gy + 2 * ch + gap + 16
    draw.rectangle([28, fy, W - 28, fy + 78], fill=INK)
    f_foot = font(SANS, 21)
    f_foot_b = font(SANS_B, 21)
    draw.text((48, fy + 10), "MANILA:", font=f_foot_b, fill=(240, 200, 80))
    draw.text((48 + text_w(draw, "MANILA: ", f_foot_b), fy + 10),
              "Quad leaders meet, first time since 2024; minerals, AI deals.",
              font=f_foot, fill=WHITE)
    draw.text((48, fy + 42), "AHEAD:", font=f_foot_b, fill=(240, 200, 80))
    draw.text((48 + text_w(draw, "AHEAD: ", f_foot_b), fy + 42),
              "First Xi–Trump–Putin meeting set for Thursday in Shenzhen.",
              font=f_foot, fill=WHITE)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
