#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261117 (v2 front page).

Build-time only: run locally with Pillow to produce entry.png, the file the
graded program (main.ts) copies to /output/entry.png. Fully original flat
vector-style art made with Pillow shapes and system fonts; no photograph,
stock art, logo or copied artwork is used anywhere.

Content: 34 stories, every one of which happened, or was first announced,
on Tuesday 17 November 2026, each checked against dated news reports:
  8 lead stories (numbered, illustrated) + 26 numbered briefs.
  Lead: US strikes Qeshm Island (Reuters); Crimea Bridge road arch falls
  (Ukraine General Staff / Reuters); Japan scrambles jets (Defence Min.);
  US loses measles elimination status (PAHO); Nvidia record $115.8bn
  quarter (company); DRC Ebola passes 11,000 cases (WHO); NSA Net outage
  (DNI: patching, not a cyberattack); Quad meets in Manila.
  Briefs cover the Gulf, Lebanon, Gaza, markets, chips, Australia, Japan,
  Europe, India, Thailand, ASEAN, Dubai, COP31, Pakistan, US weather,
  tech, courts, sport, culture, South America and science. Items first
  reported on other days (EU-Rwanda hub, Zaporizhzhia toll, U19 Asia Cup
  final, Rio Tinto Panguna, Gaza joint statement, Depardieu, COP31 draft,
  China copper smelting) were checked and excluded.

Deterministic: fixed geometry, fixed fonts, fixed palette, no clock, no
randomness, no network. Re-running produces byte-identical output.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
NAVY = (31, 58, 95)
GREY = (90, 90, 90)
DARK = (50, 50, 50)

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
    """Simple fighter-jet silhouette, drawn from polygons. Original art."""
    body = [(0, 8), (34, 4), (58, 8), (34, 12), (8, 13)]
    wing = [(22, 10), (36, 10), (28, 26), (16, 26)]
    tail = [(4, 8), (12, 8), (6, 0), (0, 0)]
    parts = [body, wing, tail]
    if flip:
        parts = [[(-px, py) for px, py in part] for part in parts]
    for part in parts:
        draw.polygon([(x + px * scale, y + py * scale) for px, py in part], fill=fill)


def waves(draw, x0, y, x1, colour, amp=4, step=24):
    for x in range(x0, x1 - step, step):
        draw.arc([x, y, x + step, y + amp * 2], 200, 340, fill=colour, width=2)


def art_qeshm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 150, 90))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=NAVY)
    d.rectangle([x + w * 0.05, y + h * 0.42, x + w * 0.52, y + h * 0.68], fill=(64, 48, 36))
    d.rectangle([x + w * 0.11, y + h * 0.28, x + w * 0.18, y + h * 0.42], fill=(64, 48, 36))
    d.rectangle([x + w * 0.25, y + h * 0.32, x + w * 0.31, y + h * 0.42], fill=(64, 48, 36))
    d.rectangle([x + w * 0.41, y + h * 0.22, x + w * 0.44, y + h * 0.42], fill=(64, 48, 36))
    d.polygon([(x + w * 0.40, y + h * 0.22), (x + w * 0.45, y + h * 0.22),
               (x + w * 0.425, y + h * 0.10)], fill=(64, 48, 36))
    for cx, cy, r in [(0.21, 0.30, 0.14), (0.27, 0.22, 0.11), (0.32, 0.32, 0.12)]:
        d.ellipse([x + w * cx - h * r, y + h * cy - h * r,
                   x + w * cx + h * r, y + h * cy + h * r], fill=(120, 118, 112))
    jet(d, x + w * 0.68, y + h * 0.14, w / 430.0, INK)
    d.polygon([(x + w * 0.63, y + h * 0.82), (x + w * 0.95, y + h * 0.82),
               (x + w * 0.92, y + h * 0.95), (x + w * 0.66, y + h * 0.95)], fill=(40, 40, 40))
    d.rectangle([x + w * 0.70, y + h * 0.70, x + w * 0.75, y + h * 0.82], fill=RED)
    d.rectangle([x + w * 0.76, y + h * 0.70, x + w * 0.81, y + h * 0.82], fill=(240, 200, 80))
    waves(d, int(x + w * 0.03), int(y + h * 0.78), int(x + w * 0.58), WHITE)


def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(217, 230, 242))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(46, 109, 164))
    dy = y + h * 0.40
    d.rectangle([x + w * 0.03, dy, x + w * 0.42, dy + h * 0.09], fill=INK)
    d.rectangle([x + w * 0.58, dy, x + w * 0.97, dy + h * 0.09], fill=INK)
    d.polygon([(x + w * 0.42, dy), (x + w * 0.45, dy + h * 0.045), (x + w * 0.42, dy + h * 0.09)],
              fill=INK)
    d.polygon([(x + w * 0.58, dy), (x + w * 0.55, dy + h * 0.045), (x + w * 0.58, dy + h * 0.09)],
              fill=INK)
    for px in (0.13, 0.30, 0.67, 0.84):
        d.rectangle([x + w * px, dy + h * 0.09, x + w * px + w * 0.025, y + h * 0.68], fill=INK)
    d.polygon([(x + w * 0.44, dy + h * 0.22), (x + w * 0.56, dy + h * 0.36),
               (x + w * 0.55, dy + h * 0.44), (x + w * 0.43, dy + h * 0.30)], fill=(90, 90, 90))
    d.arc([x + w * 0.45, y + h * 0.60, x + w * 0.55, y + h * 0.80], 180, 360, fill=WHITE, width=3)
    waves(d, int(x + w * 0.03), int(y + h * 0.78), int(x + w * 0.97), WHITE)


def art_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(253, 246, 227))
    d.ellipse([x + w * 0.60, y + h * 0.08, x + w * 0.60 + h * 0.42, y + h * 0.50],
              fill=(200, 40, 40))
    jet(d, x + w * 0.36, y + h * 0.42, w / 300.0, INK)
    jet(d, x + w * 0.16, y + h * 0.22, w / 360.0, (70, 70, 70))
    d.rectangle([x, y + h * 0.76, x + w, y + h], fill=(46, 109, 164))
    d.polygon([(x + w * 0.06, y + h * 0.76), (x + w * 0.19, y + h * 0.56),
               (x + w * 0.32, y + h * 0.76)], fill=(64, 90, 60))
    waves(d, int(x + w * 0.38), int(y + h * 0.84), int(x + w * 0.97), WHITE)


def art_measles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(234, 243, 236))
    cx, cy, r = x + w * 0.30, y + h * 0.52, min(w, h) * 0.26
    for k in range(12):
        a = math.pi * 2 * k / 12
        x1, y1 = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        x2, y2 = cx + int((r + h * 0.12) * math.cos(a)), cy + int((r + h * 0.12) * math.sin(a))
        d.line([x1, y1, x2, y2], fill=(192, 57, 43), width=4)
        d.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=(192, 57, 43))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 110, 100))
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx - r * 0.1, cy - r * 0.1], fill=(192, 57, 43))
    d.ellipse([cx + r * 0.1, cy + r * 0.1, cx + r * 0.5, cy + r * 0.5], fill=(192, 57, 43))
    bx, by, br = x + w * 0.74, y + h * 0.52, min(w, h) * 0.36
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=NAVY)
    d.ellipse([bx - br, by - br, bx + br, by + br], outline=WHITE, width=2)
    f_big = font(SANS_B, int(br * 0.75))
    f_small = font(SANS_B, int(br * 0.32))
    centre(d, int(by - br * 0.62), "26", f_big, WHITE, cx=int(bx))
    centre(d, int(by + br * 0.18), "YEARS", f_small, WHITE, cx=int(bx))


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 32, 48))
    s = min(w, h) * 0.52
    cx, cy = x + w * 0.30, y + h * 0.52
    for i in range(4):
        off = -s * 0.33 + i * s * 0.22
        d.rectangle([cx - s / 2 - w * 0.06, cy + off - 2, cx - s / 2, cy + off + 2], fill=(120, 160, 200))
        d.rectangle([cx + s / 2, cy + off - 2, cx + s / 2 + w * 0.06, cy + off + 2], fill=(120, 160, 200))
        d.rectangle([cx + off - 2, cy - s / 2 - h * 0.10, cx + off + 2, cy - s / 2], fill=(120, 160, 200))
        d.rectangle([cx + off - 2, cy + s / 2, cx + off + 2, cy + s / 2 + h * 0.10], fill=(120, 160, 200))
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=(40, 110, 70),
                outline=(140, 220, 170), width=3)
    f_ai = font(SANS_B, int(s * 0.42))
    centre(d, int(cy - s * 0.22), "AI", f_ai, WHITE, cx=int(cx))
    bars = [0.30, 0.45, 0.62, 0.85]
    bw = w * 0.055
    for i, bh in enumerate(bars):
        bx = x + w * 0.62 + i * w * 0.085
        d.rectangle([bx, y + h * 0.88 - h * 0.70 * bh, bx + bw, y + h * 0.88],
                    fill=(240, 200, 80) if i == 3 else (90, 140, 190))


def art_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 24, 24))
    for r in range(5):
        for c in range(9):
            cx = x + w * 0.06 + c * w * 0.055
            cy = y + h * 0.14 + r * h * 0.18
            col = (235, 120, 110) if (r + c) % 3 == 0 else (170, 70, 60)
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
    f_big = font(SANS_B, int(h * 0.42))
    centre(d, int(y + h * 0.24), "11,000+", f_big, WHITE, cx=int(x + w * 0.74))
    f_small = font(SANS_B, int(h * 0.17))
    centre(d, int(y + h * 0.68), "CASES", f_small, (240, 200, 80), cx=int(x + w * 0.74))


def art_nsa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 30, 38))
    rx, rw = x + w * 0.10, w * 0.44
    for i in range(3):
        ry = y + h * 0.14 + i * h * 0.28
        d.rectangle([rx, ry, rx + rw, ry + h * 0.20], fill=(60, 64, 74), outline=(140, 140, 150), width=2)
        for j in range(3):
            d.ellipse([rx + rw * 0.14 + j * rw * 0.18 - 3, ry + h * 0.10 - 3,
                       rx + rw * 0.14 + j * rw * 0.18 + 3, ry + h * 0.10 + 3],
                      fill=(90, 220, 120) if not (i == 1 and j == 1) else (230, 60, 50))
    tx, ty = x + w * 0.74, y + h * 0.50
    s = min(w, h) * 0.30
    d.polygon([(tx, ty - s), (tx + s * 0.9, ty + s * 0.7), (tx - s * 0.9, ty + s * 0.7)],
              fill=(240, 200, 80))
    f_bang = font(SANS_B, int(s * 0.9))
    centre(d, int(ty - s * 0.45), "!", f_bang, INK, cx=int(tx))


def art_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 240))
    for i, bh in enumerate([0.42, 0.58, 0.36, 0.50, 0.30]):
        bx = x + w * (0.06 + i * 0.19)
        d.rectangle([bx, y + h * 0.86 - h * bh, bx + w * 0.13, y + h * 0.86], fill=(90, 110, 135))
    d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(70, 90, 110))
    cols = [(31, 58, 95), (220, 120, 40), (200, 40, 40), (40, 120, 80)]
    for i, col in enumerate(cols):
        px = x + w * (0.16 + i * 0.23)
        d.line([px, y + h * 0.12, px, y + h * 0.86], fill=INK, width=3)
        d.polygon([(px, y + h * 0.12), (px + w * 0.15, y + h * 0.20), (px, y + h * 0.28)], fill=col)


# --- Schematic world map (lon/lat polygons, equirectangular) ---

CONTINENTS = [
    [(-165, 60), (-150, 65), (-135, 68), (-120, 70), (-105, 68), (-95, 69), (-85, 66),
     (-80, 62), (-70, 58), (-60, 52), (-55, 47), (-65, 44), (-70, 41), (-74, 39),
     (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-94, 29), (-97, 26),
     (-97, 21), (-94, 18), (-90, 15), (-86, 13), (-83, 9), (-79, 9), (-81, 13),
     (-86, 16), (-92, 15), (-96, 16), (-100, 19), (-105, 22), (-110, 25), (-114, 29),
     (-118, 33), (-122, 37), (-124, 42), (-124, 48), (-128, 52), (-133, 56), (-145, 60),
     (-155, 59), (-162, 58)],
    [(-79, 9), (-75, 11), (-71, 12), (-64, 10), (-60, 8), (-55, 6), (-51, 4), (-50, 0),
     (-48, -2), (-44, -3), (-38, -5), (-35, -8), (-37, -12), (-40, -17), (-46, -23),
     (-52, -28), (-57, -33), (-62, -38), (-65, -42), (-68, -48), (-70, -52), (-73, -53),
     (-73, -46), (-72, -40), (-71, -33), (-70, -25), (-70, -19), (-74, -15), (-77, -11),
     (-80, -6), (-81, -1), (-80, 4)],
    [(-10, 37), (-9, 43), (-2, 48), (-1, 50), (3, 52), (7, 54), (8, 57), (10, 59),
     (13, 56), (18, 55), (21, 56), (24, 58), (28, 60), (30, 65), (35, 66), (42, 68),
     (48, 68), (40, 64), (35, 60), (30, 58), (26, 54), (22, 52), (19, 50), (15, 48),
     (12, 46), (8, 44), (4, 43), (0, 40), (-3, 37), (-6, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)],
    [(-17, 15), (-16, 20), (-13, 26), (-9, 31), (-5, 35), (0, 36), (10, 37), (19, 33),
     (30, 31), (34, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 10), (46, 4),
     (42, -2), (40, -8), (39, -14), (36, -20), (33, -26), (28, -32), (20, -35),
     (17, -33), (14, -27), (13, -20), (12, -13), (9, -3), (9, 4), (4, 6), (-4, 5),
     (-10, 6), (-14, 9)],
    [(30, 68), (45, 68), (60, 69), (75, 72), (90, 75), (105, 76), (120, 73), (135, 71),
     (150, 70), (162, 68), (172, 66), (178, 65), (170, 60), (162, 58), (158, 52),
     (152, 47), (145, 44), (140, 40), (135, 35), (130, 33), (124, 30), (121, 27),
     (118, 24), (113, 22), (108, 19), (105, 10), (103, 7), (100, 6), (98, 10), (96, 15),
     (94, 18), (91, 22), (88, 22), (86, 20), (82, 16), (80, 13), (77, 8), (75, 12),
     (73, 18), (70, 22), (66, 25), (61, 25), (57, 26), (54, 26), (52, 28), (49, 30),
     (45, 29), (42, 30), (39, 32), (36, 36), (33, 36), (30, 36), (27, 38), (26, 40),
     (28, 44), (30, 47), (33, 52), (38, 55), (40, 60), (35, 64)],
    [(130, 31), (133, 34), (137, 35), (140, 37), (142, 42), (144, 44), (141, 45),
     (138, 39), (134, 34), (131, 32)],
    [(95, 5), (100, 2), (104, -2), (106, -5), (102, -6), (98, -1), (95, 2)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -10), (141, -8),
     (136, -7), (131, -4)],
    [(113, -22), (114, -28), (117, -32), (122, -34), (128, -32), (133, -32), (136, -35),
     (140, -38), (145, -38), (149, -37), (153, -33), (153, -27), (150, -23), (147, -19),
     (143, -14), (141, -12), (136, -12), (132, -11), (128, -14), (124, -16), (120, -19),
     (116, -21)],
    [(167, -45), (172, -41), (175, -38), (178, -37), (175, -41), (171, -44)],
]

MAP_PINS = [(1, 56, 27), (2, 34, 45), (3, 139, 36), (4, -100, 40),
            (5, -122, 37), (6, 23, -3), (7, -77, 39), (8, 121, 15)]

MAP_LABELS = [("N AMERICA", -108, 60), ("S AMERICA", -55, -18), ("EUROPE", 8, 55),
              ("AFRICA", 10, 22), ("ASIA", 82, 52), ("OCEANIA", 128, -27)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240), outline=INK, width=2)
    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (72 - lat) / 122.0 * h)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(196, 205, 170),
                  outline=(110, 120, 95))
    f_lab = font(SANS_B, 10)
    for name, lon, lat in MAP_LABELS:
        px, py = proj(lon, lat)
        d.text((px - text_w(d, name, f_lab) // 2, py - 5), name, font=f_lab, fill=(90, 95, 85))
    f_pin = font(SANS_B, 10)
    for num, lon, lat in MAP_PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=2)
        s = str(num)
        d.text((px - text_w(d, s, f_pin) // 2, py - 6), s, font=f_pin, fill=WHITE)


# --- Card helpers ---

def tag_chip(d, x, y, label, fill, size=14):
    f = font(SANS_B, size)
    tw = text_w(d, label, f) + 16
    d.rounded_rectangle([x, y, x + tw, y + size + 8], radius=(size + 8) // 2, fill=fill)
    d.text((x + 8, y + 3), label, font=f, fill=WHITE)
    return size + 8


def feature(d, x, y, w, h, num, tag, tagfill, head, sub, art, art_h,
            head_size=19, sub_size=13):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    art(d, x + 2, y + 2, w - 4, art_h)
    d.rectangle([x + 2, y + 2 + art_h, x + w - 2, y + 4 + art_h], fill=INK)
    ty = y + art_h + 6
    tag_chip(d, x + 12, ty, "%d \u00b7 %s" % (num, tag), tagfill)
    f_head = font(SANS_B, head_size)
    lines = wrap(d, head, f_head, w - 24)
    hy = ty + 24
    for line in lines[:2]:
        d.text((x + 12, hy), line, font=f_head, fill=INK)
        hy += head_size + 3
    f_sub = font(SANS, sub_size)
    sub_lines = wrap(d, sub, f_sub, w - 24)
    sy = hy
    for line in sub_lines[:3]:
        d.text((x + 12, sy), line, font=f_sub, fill=DARK)
        sy += sub_size + 3


def side_card(d, x, y, w, h, num, tag, tagfill, head, sub, art, art_w,
              head_size=16, sub_size=12):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    art(d, x + 2, y + 2, art_w, h - 4)
    d.rectangle([x + 2 + art_w, y + 2, x + 4 + art_w, y + h - 2], fill=INK)
    tx = x + art_w + 12
    tw = w - art_w - 24
    ty = y + 6
    tag_chip(d, tx, ty, "%d \u00b7 %s" % (num, tag), tagfill, size=12)
    f_head = font(SANS_B, head_size)
    lines = wrap(d, head, f_head, tw)
    hy = ty + 22
    for line in lines[:2]:
        d.text((tx, hy), line, font=f_head, fill=INK)
        hy += head_size + 2
    f_sub = font(SANS, sub_size)
    sub_lines = wrap(d, sub, f_sub, tw)
    sy = hy + 1
    for line in sub_lines[:2]:
        d.text((tx, sy), line, font=f_sub, fill=DARK)
        sy += sub_size + 2


BRIEFS = [
    "Trump takes 'dirty bomb' plot report seriously; Iran denies it. (CNN)",
    "Houthis say 5 drones fired at Saudi pipeline stations.",
    "Strikes and shelling reported across south Lebanon.",
    "UN: winter rains flood Gaza shelters, deepen food crisis.",
    "Wall Street falls on AI slide; Brent crude tops $93.",
    "US requires chip export licences for five nations. (WSJ)",
    "RBA minutes: most see 4.85% rate 'not clearly sufficient'.",
    "Kuroda: BOJ rates may top neutral; Japan delays new bond.",
    "Germany backs Spain's de Cos for ECB top job.",
    "US presses FCC ban on Chinese transceivers. (Reuters)",
    "Amazon pledges $7bn for Indian renewables by 2030.",
    "Thailand, US hail progress on reciprocal trade deal.",
    "Japan, China leaders skip meeting at ASEAN+3 summit.",
    "Dubai Airports traffic down 28.1% to 50.4m in 9 months.",
    "COP31: Brazil, France launch 25-nation ocean taskforce.",
    "25 nations back Wildlife for Climate pledge at COP31.",
    "BASIC bloc presses rich nations on pre-2050 net zero.",
    "Pope Leo XIV ends 12-day South America tour, lands in Rome.",
    "Pakistan cuts petrol and diesel by Rs2 a litre.",
    "Flash flooding hits Florida; storm front reaches the West.",
    "Waymo pulls robotaxis from freeways.",
    "Irish activist charged in NY over $60m plane damage.",
    "NASA ends NICER X-ray telescope science, motor blamed.",
    "Tiger Woods confirms return at Hero World Challenge. (AP)",
    "National Geographic's Pictures of the Year published.",
    "Trump open to one-on-one meeting with Putin this week.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([20, 16, W - 20, 18], fill=INK)
    f_kick = font(SANS_B, 18)
    centre(d, 26, "W O R L D   N E W S   \u2022   O N E   D A Y   \u2022   O N E   I M A G E",
           f_kick, RED)
    f_date = fit_font(d, "TUESDAY 17 NOVEMBER 2026", SERIF_B, 54, W - 40)
    centre(d, 48, "TUESDAY 17 NOVEMBER 2026", f_date, INK)
    d.rectangle([20, 106, W - 20, 109], fill=RED)
    f_sub = font(SANS_B, 17)
    centre(d, 110, "34 STORIES FROM SIX CONTINENTS \u2014 EVERY ONE DATED THIS TUESDAY",
           f_sub, INK)
    # Hero row.
    feature(d, 20, 132, 640, 196, 1, "MIDDLE EAST \u2014 THE GULF", NAVY,
            "U.S. STRIKES QESHM ISLAND",
            "U.S. warplanes hit an Iranian missile launch site after attacks on "
            "Hormuz shipping, a U.S. official tells Reuters. "
            "Oman evacuates a burning gas tanker's crew (UKMTO).",
            art_qeshm, 76, head_size=28, sub_size=15)
    side_card(d, 672, 132, 332, 93, 2, "UKRAINE", (70, 90, 140),
              "CRIMEA BRIDGE SPAN FALLS",
              "Road arch drops into the strait; road shut, rail resumes.",
              art_bridge, 100, head_size=15, sub_size=12)
    side_card(d, 672, 235, 332, 93, 3, "EAST ASIA", (160, 60, 60),
              "JAPAN SCRAMBLES FIGHTER JETS",
              "Two suspected Russian planes breach airspace; Tokyo protests.",
              art_japan, 100, head_size=15, sub_size=12)
    # Second row: three cards.
    feature(d, 20, 336, 322, 142, 4, "HEALTH", (50, 110, 70),
            "U.S. LOSES MEASLES-FREE STATUS",
            "PAHO: endemic again after 26 years; 5,412 cases. Mexico, Bolivia too.",
            art_measles, 42, head_size=17, sub_size=12)
    feature(d, 351, 336, 322, 142, 5, "BUSINESS", (20, 60, 100),
            "NVIDIA POSTS RECORD $115.8BN",
            "Revenue +103%; Q4 guided to $130bn. No Huang return; Kress interim.",
            art_chip, 42, head_size=17, sub_size=12)
    feature(d, 682, 336, 322, 142, 6, "AFRICA \u2014 HEALTH", (140, 30, 30),
            "EBOLA PASSES 11,000 CASES IN DRC",
            "WHO: ~5,400 dead, 67 zones; children a third of deaths.",
            art_ebola, 42, head_size=17, sub_size=12)
    # Third row: two wide cards.
    side_card(d, 20, 486, 492, 86, 7, "TECHNOLOGY", (60, 60, 80),
              "NSA NETWORK GOES DOWN",
              "Classified NSA Net disrupted by patching, DNI says \u2014 'not a "
              "cyberattack'. Apple hit too.",
              art_nsa, 118, head_size=18, sub_size=13)
    side_card(d, 522, 486, 482, 86, 8, "DIPLOMACY", (120, 80, 30),
              "QUAD MEETS IN MANILA",
              "Leaders meet for the first time since 2024, warning on coercion. "
              "Xi\u2013Trump\u2013Putin Thursday.",
              art_quad, 118, head_size=18, sub_size=13)
    # Map + numbers strip.
    f_sec = font(SANS_B, 15)
    d.text((24, 580), "WHERE THE DAY HAPPENED \u2014 LEAD STORIES 1\u20138 PINNED", font=f_sec, fill=INK)
    d.text((712, 580), "THE DAY IN NUMBERS", font=f_sec, fill=INK)
    draw_map(d, 24, 598, 676, 74)
    d.rectangle([712, 598, 1004, 672], fill=WHITE, outline=INK, width=2)
    figures = [("1,441", "record drones in one night"),
               ("$115.8bn", "Nvidia revenue, +103%"),
               ("5,412", "U.S. measles cases in 2026"),
               ("11,000+", "DRC Ebola cases, WHO")]
    f_num = font(SANS_B, 16)
    f_lab = font(SANS, 12)
    for i, (num, lab) in enumerate(figures):
        fy = 600 + i * 17
        d.text((722, fy), num, font=f_num, fill=RED)
        d.text((722 + 92, fy + 2), lab, font=f_lab, fill=DARK)
    # Briefs.
    f_bhead = font(SANS_B, 17)
    d.text((20, 680), "THE DAY IN BRIEF \u2014 26 MORE STORIES, ALL DATED 17 NOVEMBER",
           font=f_bhead, fill=INK)
    d.rectangle([20, 702, W - 20, 704], fill=INK)
    f_bnum = font(SANS_B, 11)
    f_b = font(SANS, 14)
    cols = [BRIEFS[0:9], BRIEFS[9:18], BRIEFS[18:26]]
    for ci, col in enumerate(cols):
        cx = 20 + ci * 332
        for ri, text in enumerate(col):
            by = 710 + ri * 29
            num = 9 + ci * 9 + ri
            d.rectangle([cx, by, cx + 22, by + 16], fill=RED)
            s = str(num)
            d.text((cx + 11 - text_w(d, s, f_bnum) // 2, by + 2), s, font=f_bnum, fill=WHITE)
            lines = wrap(d, text, f_b, 292)
            ly = by - 1
            for line in lines[:2]:
                d.text((cx + 28, ly), line, font=f_b, fill=INK)
                ly += 15
    # Footer.
    f_foot = font(SANS, 12)
    centre(d, 994,
           "Sources: Reuters, AP, AFP, Bloomberg, WSJ, PAHO, WHO, UN News, UKMTO, "
           "Le Monde, IANS, RBA, Nvidia, NASA, Vatican News.",
           f_foot, GREY)
    centre(d, 1008,
           "Original artwork \u2014 no photographs. All 34 stories happened or were "
           "announced on Tuesday 17 November 2026.",
           f_foot, GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
