#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news dashboard, 1024x1024 PNG.

Every story was verified as having happened, or first been reported, on
Tuesday 24 November 2026. Sources are listed in notes.md next to the build.
Drawn entirely in code with PIL; no AI-generated imagery.
Deterministic: same input, same bytes on every run.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 22  # outer margin

# --- palette ---
PAPER = (246, 241, 227)
PAPER_DARK = (238, 231, 210)
INK = (26, 26, 26)
RED = (185, 28, 28)
RED_DARK = (140, 20, 20)
NAVY = (30, 58, 95)
NAVY_DARK = (18, 38, 66)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 205, 110)
GREEN = (27, 94, 60)
AMBER = (166, 110, 10)
PANEL = (253, 251, 245)
PANEL_LINE = (190, 180, 158)
SEA = (214, 230, 240)
LAND = (217, 201, 163)
LAND_DARK = (198, 178, 132)
WHITE = (255, 255, 255)
GREY = (105, 100, 88)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
MONO_B = "DejaVuSansMono-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, cx=512):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def tag_chip(draw, x, y, text, fill, outline=None):
    """Small tag, e.g. CONFIRMED / OFFICIAL / REPORTED / CLAIM."""
    fnt = font(MONO_B, 10)
    tw = draw.textlength(text, font=fnt)
    pad = 5
    box = [x, y, x + tw + pad * 2, y + 16]
    if outline:
        draw.rounded_rectangle(box, radius=3, outline=outline, width=1,
                               fill=WHITE)
        draw.text((x + pad, y + 2), text, font=fnt, fill=outline)
    else:
        draw.rounded_rectangle(box, radius=3, fill=fill)
        draw.text((x + pad, y + 2), text, font=fnt, fill=WHITE)
    return box[2]


def ornament(draw, x, y, size, color):
    """Small diamond ornament."""
    s = size
    draw.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)],
                 fill=color)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- subtle paper texture (deterministic) ---
    rnd = random.Random(24112026)
    for _ in range(900):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        d.point((x, y), fill=(232, 224, 198))

    # --- outer double border ---
    d.rectangle([10, 10, 1013, 1013], outline=INK, width=2)
    d.rectangle([14, 14, 1009, 1009], outline=RED, width=1)

    # ================= MASTHEAD =================
    centre(d, 24, "THE WORLD IN ONE DAY", font(SERIF_B, 46), INK)
    # gold rules + diamonds flanking the date band
    d.line([(M, 78), (1002, 78)], fill=GOLD, width=2)
    ornament(d, 40, 93, 5, GOLD)
    ornament(d, 984, 93, 5, GOLD)
    # date band
    d.rectangle([M, 82, 1002, 108], fill=NAVY_DARK)
    d.text((34, 87), "31 STORIES", font=font(SANS_B, 11), fill=GOLD_LIGHT)
    centre(d, 85, "TUESDAY 24 NOVEMBER 2026", font(SERIF_B, 21), WHITE)
    rtxt = "EVERY ONE DATED TUESDAY"
    d.text((1002 - 12 - d.textlength(rtxt, font=font(SANS_B, 11)), 87),
           rtxt, font=font(SANS_B, 11), fill=GOLD_LIGHT)
    d.line([(M, 112), (1002, 112)], fill=RED, width=2)

    # ================= TIMELINE STRIP =================
    ty = 116
    d.rectangle([M, ty, 1002, ty + 46], fill=PANEL, outline=PANEL_LINE)
    d.rectangle([M, ty, 150, ty + 46], fill=RED_DARK)
    d.text((M + 8, ty + 8), "TUESDAY'S", font=font(SANS_B, 11), fill=WHITE)
    d.text((M + 8, ty + 23), "TIMELINE · UTC", font=font(SANS_B, 11),
           fill=GOLD_LIGHT)
    timeline = [
        ("01:32", "Nepal quake 5.6 strikes near Taplejung"),
        ("04:35", "Ukraine FM warns UN Council on port attacks"),
        ("08:06", "Sanofi unveils its $41bn Insmed deal"),
        ("14:00", "FIDE Game 1 begins in Geneva — draw, 38 moves"),
    ]
    col_w = (1002 - 158) // 4
    for i, (t, ev) in enumerate(timeline):
        x0 = 158 + i * col_w + 8
        if i:
            d.line([(158 + i * col_w, ty + 7), (158 + i * col_w, ty + 39)],
                   fill=PANEL_LINE, width=1)
        d.text((x0, ty + 5), t, font=font(SANS_B, 13), fill=NAVY)
        lines = wrap(d, ev, font(SANS, 10), col_w - 16)[:2]
        for j, line in enumerate(lines):
            d.text((x0, ty + 22 + j * 12), line, font=font(SANS, 10),
                   fill=INK)


    # ================= ILLUSTRATIONS (nested helpers) =================
    def ill_chart(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 34, 58))
        for gy in range(y0 + 14, y0 + h, 16):
            d.line([(x0 + 6, gy), (x0 + w - 6, gy)], fill=(38, 64, 100),
                   width=1)
        # candlesticks
        xs = [x0 + 22 + i * 52 for i in range(5)]
        bodies = [(34, 22), (48, 18), (30, 26), (52, 14), (26, 30)]
        for i, (bx, (bt, bh)) in enumerate(zip(xs, bodies)):
            col = (46, 180, 110) if i != 2 else (220, 80, 70)
            d.line([(bx + 8, y0 + bt - 8), (bx + 8, y0 + bt + bh + 8)],
                   fill=col, width=2)
            d.rectangle([bx, y0 + bt, bx + 16, y0 + bt + bh], fill=col)
        # rising gold arrow
        d.line([(x0 + 14, y0 + h - 16), (x0 + w - 40, y0 + 18)],
               fill=GOLD_LIGHT, width=3)
        d.polygon([(x0 + w - 40, y0 + 18), (x0 + w - 58, y0 + 20),
                   (x0 + w - 44, y0 + 34)], fill=GOLD_LIGHT)
        d.text((x0 + 40, y0 + 5), "TAIEX +9.0%", font=font(SANS_B, 12),
               fill=WHITE)

    def ill_quake(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(205, 224, 238))
        d.ellipse([x0 + w - 52, y0 + 8, x0 + w - 20, y0 + 40],
                  fill=(245, 222, 130))
        # mountains
        d.polygon([(x0, y0 + h), (x0 + 70, y0 + 18), (x0 + 150, y0 + h)],
                  fill=(110, 116, 122))
        d.polygon([(x0 + 70, y0 + 18), (x0 + 92, y0 + 38),
                   (x0 + 70, y0 + 32), (x0 + 52, y0 + 40)],
                  fill=WHITE)
        d.polygon([(x0 + 120, y0 + h), (x0 + 220, y0 + 8),
                   (x0 + w, y0 + h)], fill=(88, 94, 100))
        d.polygon([(x0 + 220, y0 + 8), (x0 + 244, y0 + 30),
                   (x0 + 220, y0 + 24), (x0 + 198, y0 + 32)],
                  fill=WHITE)
        # crack lines from the epicentre
        ex, ey = x0 + 150, y0 + 62
        for dx, dy in [(-38, -14), (30, -20), (-20, 16), (42, 8)]:
            d.line([(ex, ey), (ex + dx, ey + dy)], fill=RED_DARK, width=2)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)
        # seismograph strip
        d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=WHITE)
        pts = []
        import math as _math
        for i in range(0, w, 6):
            amp = 6 if 90 < i < 200 else 2
            pts.append((x0 + i,
                        y0 + h - 9 + int(_math.sin(i / 5.0) * amp)))
        d.line(pts, fill=RED, width=2)

    def ill_pharma(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 236, 228))
        # big capsule
        cx, cy = x0 + 78, y0 + 46
        d.rounded_rectangle([cx - 62, cy - 20, cx + 62, cy + 20], radius=20,
                            fill=WHITE, outline=RED, width=2)
        d.rounded_rectangle([cx - 62, cy - 20, cx, cy + 20], radius=20,
                            fill=RED)
        d.line([(cx, cy - 20), (cx, cy + 20)], fill=RED, width=2)
        # flask
        fx = x0 + w - 78
        d.polygon([(fx, y0 + 22), (fx + 26, y0 + 22), (fx + 20, y0 + 34),
                   (fx + 44, y0 + h - 14), (fx - 18, y0 + h - 14),
                   (fx + 6, y0 + 34)], fill=(120, 190, 210),
                  outline=NAVY)
        d.polygon([(fx + 38, y0 + h - 30), (fx - 12, y0 + h - 30),
                   (fx - 18, y0 + h - 14), (fx + 44, y0 + h - 14)],
                  fill=(60, 140, 190))
        d.text((x0 + 40, y0 + 6), "$41bn", font=font(SANS_B, 16),
               fill=NAVY_DARK)
        d.text((x0 + 12, y0 + h - 22), "BIGGEST BIOTECH DEAL IN ~3 YRS",
               font=font(SANS_B, 9), fill=GREEN)

    def ill_bridge(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 216, 232))
        d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(90, 140, 185))
        for wx in range(x0 + 8, x0 + w - 8, 26):
            d.line([(wx, y0 + h - 6), (wx + 14, y0 + h - 6)],
                   fill=(170, 210, 235), width=2)
        # bridge deck + towers (all inside the box)
        deck_y = y0 + h - 14
        d.rectangle([x0 + 8, deck_y, x0 + w - 8, deck_y + 5],
                    fill=(70, 74, 80))
        for tx in (x0 + 44, x0 + w - 58):
            d.rectangle([tx, y0 + 8, tx + 10, deck_y + 5],
                        fill=(70, 74, 80))
        d.line([(x0 + 49, y0 + 8), (x0 + 90, deck_y)],
               fill=(120, 124, 130), width=2)
        d.line([(x0 + w - 53, y0 + 8), (x0 + w - 94, deck_y)],
               fill=(120, 124, 130), width=2)
        # explosion starburst on the deck
        ex, ey = x0 + w // 2, deck_y - 6
        for r, col in [(15, (255, 140, 40)), (10, (255, 200, 60)),
                       (5, (255, 240, 170))]:
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
        for dx, dy in [(-18, -10), (17, -12), (-16, 6), (18, 5)]:
            d.line([(ex, ey), (ex + dx, ey + dy)], fill=(255, 140, 40),
                   width=2)
        # smoke puffs
        for sx, sy, sr in [(ex - 22, ey - 14, 6), (ex + 20, ey - 16, 7),
                           (ex + 4, ey - 20, 5)]:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                      fill=(120, 120, 120))

    def ill_talks(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 222, 196))
        # window + flags
        d.rectangle([x0 + 10, y0 + 8, x0 + w - 10, y0 + 30], fill=(190, 215,
                     235))
        # three small flags on poles
        for i, cols in enumerate([((0, 91, 172), (255, 213, 0)),
                                  ((255, 255, 255), (210, 40, 40)),
                                  ((60, 90, 160), (200, 40, 40))]):
            fx = x0 + 24 + i * 58
            d.line([(fx, y0 + 12), (fx, y0 + 44)], fill=(90, 70, 40),
                   width=2)
            d.rectangle([fx, y0 + 12, fx + 34, y0 + 22], fill=cols[0])
            d.rectangle([fx, y0 + 22, fx + 34, y0 + 32], fill=cols[1])
        # table
        d.polygon([(x0 + 20, y0 + h - 2), (x0 + w - 20, y0 + h - 2),
                   (x0 + w - 34, y0 + 34), (x0 + 34, y0 + 34)],
                  fill=(140, 100, 60))
        d.ellipse([x0 + w // 2 - 46, y0 + 30, x0 + w // 2 + 46, y0 + 38],
                  fill=(170, 125, 75))
        # NO DEAL stamp
        d.rectangle([x0 + w - 78, y0 + h - 26, x0 + w - 8, y0 + h - 8],
                    outline=RED, width=2)
        d.text((x0 + w - 72, y0 + h - 24), "NO DEAL", font=font(SANS_B, 10),
               fill=RED)

    def ill_islands(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(168, 210, 232))
        # island
        d.ellipse([x0 + 18, y0 + h - 34, x0 + 130, y0 + h - 2],
                  fill=(110, 170, 110))
        d.line([(x0 + 60, y0 + h - 30), (x0 + 66, y0 + 18)],
               fill=(110, 80, 40), width=3)
        for dx, dy in [(-18, -4), (18, -6), (-10, -14), (12, -14)]:
            d.line([(x0 + 66, y0 + 20), (x0 + 66 + dx, y0 + 20 + dy)],
                   fill=(40, 130, 60), width=3)
        # sun + birds
        d.ellipse([x0 + w - 40, y0 + 6, x0 + w - 14, y0 + 32],
                  fill=(245, 222, 130))
        # two flags: red (out) with down arrow, blue (in) with up arrow
        d.line([(x0 + w - 66, y0 + 14), (x0 + w - 66, y0 + 46)],
               fill=(90, 70, 40), width=2)
        d.rectangle([x0 + w - 66, y0 + 14, x0 + w - 34, y0 + 28],
                    fill=(200, 40, 40))
        d.text((x0 + w - 60, y0 + 30), "OUT", font=font(SANS_B, 8),
               fill=RED_DARK)
        d.line([(x0 + w - 30, y0 + 34), (x0 + w - 30, y0 + h - 2)],
               fill=(90, 70, 40), width=2)
        d.rectangle([x0 + w - 30, y0 + 34, x0 + w - 2, y0 + 48],
                    fill=(40, 80, 160))
        d.text((x0 + w - 52, y0 + 38), "IN", font=font(SANS_B, 8),
               fill=NAVY)

    def ill_rocket(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 18, 40))
        rnd2 = random.Random(99)
        for _ in range(26):
            sx = x0 + rnd2.randint(4, w - 4)
            sy = y0 + rnd2.randint(4, h - 14)
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
        # earth horizon band along the bottom of the box
        d.rectangle([x0, y0 + h - 8, x0 + w, y0 + h],
                    fill=(70, 130, 200))
        d.line([(x0, y0 + h - 8), (x0 + w, y0 + h - 8)],
               fill=(140, 190, 240), width=2)
        # rocket (scaled to the box height)
        rx, ry = x0 + 44, y0 + 8
        bh = h - 28
        d.polygon([(rx, ry), (rx + 16, ry), (rx + 16, ry + bh),
                   (rx, ry + bh)], fill=WHITE)
        d.polygon([(rx, ry), (rx + 8, ry - 8), (rx + 16, ry)],
                  fill=RED)
        d.polygon([(rx - 5, ry + bh), (rx, ry + bh - 6), (rx, ry + bh + 4)],
                  fill=RED)
        d.polygon([(rx + 21, ry + bh), (rx + 16, ry + bh - 6),
                   (rx + 16, ry + bh + 4)], fill=RED)
        d.polygon([(rx + 4, ry + bh + 4), (rx + 8, ry + bh + 10),
                   (rx + 12, ry + bh + 4)], fill=(255, 160, 40))
        # station
        sx0, sy0 = x0 + w - 84, y0 + 10
        d.rectangle([sx0, sy0 + 6, sx0 + 52, sy0 + 16], fill=(180, 190, 200))
        d.rectangle([sx0 - 14, sy0 + 3, sx0, sy0 + 19], fill=(60, 110, 190))
        d.rectangle([sx0 + 52, sy0 + 3, sx0 + 66, sy0 + 19],
                    fill=(60, 110, 190))

    def ill_jets(x0, y0, w, h):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(186, 214, 236))
        for cx, cy, cr in [(x0 + 30, y0 + 14, 12), (x0 + 120, y0 + 10, 9),
                           (x0 + 150, y0 + 30, 10)]:
            d.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2],
                      fill=WHITE)
        # sea + island
        d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=(90, 140, 185))
        d.polygon([(x0 + 20, y0 + h - 18), (x0 + 70, y0 + h - 40),
                   (x0 + 130, y0 + h - 18)], fill=(100, 160, 100))
        # jets (simple darts)
        for jx, jy in [(x0 + 40, y0 + 26), (x0 + 96, y0 + 40)]:
            d.polygon([(jx, jy), (jx + 30, jy + 6), (jx + 6, jy + 10)],
                      fill=(60, 64, 70))
            d.polygon([(jx + 8, jy + 2), (jx + 14, jy - 6), (jx + 18, jy + 4)],
                      fill=(60, 64, 70))
        # alert triangle
        ax, ay = x0 + w - 44, y0 + 8
        d.polygon([(ax, ay + 26), (ax + 28, ay + 26), (ax + 14, ay)],
                  fill=(240, 200, 40), outline=INK)
        d.text((ax + 11, ay + 10), "!", font=font(SANS_B, 12), fill=INK)

    # ================= LEADS =================
    leads = [
        (1, "ASIA'S CHIP RALLY SMASHES RECORDS",
         "Taiex +9.0% — its biggest points gain ever. Kospi +6.3%, Nikkei "
         "+3.9%. TSMC +10%, Advantest +15%.",
         "CONFIRMED", GREEN, ill_chart),
        (2, "QUAKE SHAKES NEPAL AT DAWN",
         "Magnitude 5.6 near Taplejung, 01:32 UTC. Felt in Kathmandu, "
         "Sikkim, Bhutan. No casualties.",
         "OFFICIAL", NAVY, ill_quake),
        (3, "SANOFI BUYS INSMED FOR $41bn",
         "$175 a share in cash — the biggest biotech deal in nearly three "
         "years. Sanofi +5.6%, Insmed +14%.",
         "OFFICIAL", NAVY, ill_pharma),
    ]
    ly, lh = 168, 180
    lw = 320
    for i, (num, head, body, tag, tagcol, ill) in enumerate(leads):
        x0 = M + i * (lw + 10)
        d.rectangle([x0, ly, x0 + lw, ly + lh], fill=PANEL,
                    outline=PANEL_LINE, width=1)
        ill(x0 + 1, ly + 1, lw - 2, 84)
        # number badge
        d.ellipse([x0 + 8, ly + 8, x0 + 30, ly + 30], fill=RED)
        ntxt = str(num)
        nw = d.textlength(ntxt, font=font(SANS_B, 13))
        d.text((x0 + 19 - nw / 2, ly + 10), ntxt, font=font(SANS_B, 13),
               fill=WHITE)
        hy = ly + 90
        for j, line in enumerate(wrap(d, head, font(SERIF_B, 15), lw - 16)):
            d.text((x0 + 8, hy + j * 19), line, font=font(SERIF_B, 15),
                   fill=INK)
        by = hy + 19 * len(wrap(d, head, font(SERIF_B, 15), lw - 16)) + 3
        for j, line in enumerate(wrap(d, body, font(SANS, 11), lw - 16)[:2]):
            d.text((x0 + 8, by + j * 13), line, font=font(SANS, 11),
                   fill=(50, 50, 50))
        tag_chip(d, x0 + 8, ly + lh - 20, tag, tagcol)

    # ================= TIER 2 =================
    tier2 = [
        (4, "KERCH BRIDGE HIT AGAIN",
         "Third strike this week; road and rail spans hit, traffic halted.",
         "CONFIRMED", GREEN, ill_bridge),
        (5, "ABU DHABI TALKS END, NO DEAL",
         "No breakthrough after two days; 160+ missiles hit the grid.",
         "CONFIRMED", GREEN, ill_talks),
        (6, "SOLOMONS DITCH CHINA PACT",
         "Honiara lets the 2022 deal lapse in April; Australia treaty due "
         "Wed.",
         "REPORTED", AMBER, ill_islands),
        (7, "FIRST FOREIGNER FOR TIANGONG",
         "Pakistan's Muhammad Zeeshan Ali flies Wed; launch 08:18 Beijing "
         "time.",
         "OFFICIAL", NAVY, ill_rocket),
        (8, "SEOUL SCRAMBLES JETS",
         "Russian planes enter the air zone near Ulleung; alert lifted in "
         "minutes.",
         "OFFICIAL", NAVY, ill_jets),
    ]
    ty2, th2 = 354, 130
    tw2 = 188
    for i, (num, head, body, tag, tagcol, ill) in enumerate(tier2):
        x0 = M + i * (tw2 + 8)
        d.rectangle([x0, ty2, x0 + tw2, ty2 + th2], fill=PANEL,
                    outline=PANEL_LINE, width=1)
        ill(x0 + 1, ty2 + 1, tw2 - 2, 50)
        d.ellipse([x0 + 6, ty2 + 6, x0 + 24, ty2 + 24], fill=RED)
        ntxt = str(num)
        nw = d.textlength(ntxt, font=font(SANS_B, 11))
        d.text((x0 + 15 - nw / 2, ty2 + 8), ntxt, font=font(SANS_B, 11),
               fill=WHITE)
        hy = ty2 + 55
        hlines = wrap(d, head, font(SANS_B, 11.5), tw2 - 12)[:2]
        for j, line in enumerate(hlines):
            d.text((x0 + 6, hy + j * 14), line, font=font(SANS_B, 11.5),
                   fill=INK)
        by = hy + 14 * len(hlines) + 2
        for j, line in enumerate(wrap(d, body, font(SANS, 9.5),
                                      tw2 - 12)[:2]):
            d.text((x0 + 6, by + j * 11), line, font=font(SANS, 9.5),
                   fill=(50, 50, 50))
        tag_chip(d, x0 + 6, ty2 + th2 - 20, tag, tagcol)

    # ================= MAP + REGION KEY =================
    my, mh = 490, 120
    # --- map panel ---
    d.rectangle([M, my, 668, my + mh], fill=PANEL, outline=PANEL_LINE)
    d.text((M + 8, my + 5), "WHERE THE DAY HAPPENED — NUMBERED PINS MATCH "
           "THE STORIES", font=font(SANS_B, 10), fill=NAVY_DARK)
    mx0, my0, mw, mh2 = M + 6, my + 22, 634, 92
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh2], fill=SEA)
    # graticule
    for gx in range(mx0 + 60, mx0 + mw, 60):
        d.line([(gx, my0), (gx, my0 + mh2)], fill=(190, 210, 225), width=1)
    for gy in range(my0 + 23, my0 + mh2, 23):
        d.line([(mx0, gy), (mx0 + mw, gy)], fill=(190, 210, 225), width=1)
    # continents (schematic blobs, map-local coords)
    continents = [
        [(8, 18), (60, 8), (120, 12), (150, 26), (140, 44), (100, 52),
         (70, 48), (40, 44), (12, 36)],  # N America
        [(140, 44), (160, 52), (155, 60), (138, 54)],  # C America
        [(155, 58), (185, 52), (205, 62), (200, 88), (175, 92), (160, 78)],
        [(150, 6), (175, 4), (180, 12), (158, 14)],  # Greenland
        [(292, 14), (300, 12), (302, 20), (294, 22)],  # UK
        [(300, 10), (330, 6), (350, 14), (345, 30), (320, 34), (300, 26)],
        [(300, 38), (340, 36), (360, 52), (350, 80), (320, 88), (300, 70)],
        [(350, 8), (480, 6), (560, 14), (600, 30), (580, 52), (520, 60),
         (470, 58), (420, 52), (380, 44), (355, 30)],  # Asia
        [(540, 68), (590, 66), (600, 80), (580, 88), (545, 86)],
    ]
    for poly in continents:
        pts = [(mx0 + x, my0 + y) for x, y in poly]
        d.polygon(pts, fill=LAND, outline=LAND_DARK)
    # island dots: SE Asia, Japan, Indonesia
    for ix, iy in [(520, 66), (545, 70), (595, 30), (600, 38), (612, 82),
                   (505, 72)]:
        d.ellipse([mx0 + ix - 3, my0 + iy - 2, mx0 + ix + 3, my0 + iy + 2],
                  fill=LAND, outline=LAND_DARK)
    # compass rose
    cx0, cy0 = mx0 + 26, my0 + 74
    d.polygon([(cx0, cy0 - 10), (cx0 + 3, cy0), (cx0, cy0 + 10),
               (cx0 - 3, cy0)], fill=NAVY)
    d.text((cx0 - 3, cy0 - 20), "N", font=font(SANS_B, 9), fill=NAVY)
    # numbered pins for the 8 illustrated stories
    pins = {1: (548, 44), 2: (470, 42), 3: (305, 24), 4: (362, 28),
            5: (412, 48), 6: (612, 82), 7: (520, 30), 8: (580, 32)}
    for num, (px, py) in pins.items():
        ax, ay = mx0 + px, my0 + py
        d.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=RED,
                  outline=WHITE, width=1)
        ntxt = str(num)
        nw = d.textlength(ntxt, font=font(SANS_B, 9))
        d.text((ax - nw / 2, ay - 6), ntxt, font=font(SANS_B, 9),
               fill=WHITE)
    # dots for list stories
    dots = [(312, 28), (322, 20), (498, 68), (408, 52), (338, 62),
            (398, 44), (378, 46), (110, 34), (342, 14), (340, 76),
            (512, 56), (114, 38), (180, 78), (418, 52), (312, 70)]
    for px, py in dots:
        ax, ay = mx0 + px, my0 + py
        d.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=NAVY)
    # Ukraine cluster callout
    d.ellipse([mx0 + 326, my0 + 14, mx0 + 370, my0 + 40], outline=RED,
              width=2)
    d.text((mx0 + 372, my0 + 10), "UKRAINE x9", font=font(SANS_B, 9),
           fill=RED_DARK)
    d.text((mx0 + 372, my0 + 20), "war stories", font=font(SANS, 8),
           fill=RED_DARK)
    # --- region key panel ---
    kx0, kw = 676, 326
    d.rectangle([kx0, my, kx0 + kw, my + mh], fill=PANEL,
                outline=PANEL_LINE)
    d.text((kx0 + 10, my + 5), "THE DAY BY REGION", font=font(SANS_B, 11),
           fill=NAVY_DARK)
    regions = [("EUROPE", 14, (30, 58, 95)), ("ASIA", 6, (185, 28, 28)),
               ("MIDDLE EAST", 5, (27, 94, 60)),
               ("AFRICA", 3, (166, 110, 10)),
               ("AMERICAS", 2, (110, 70, 140)),
               ("OCEANIA", 1, (40, 130, 160))]
    for i, (name, count, col) in enumerate(regions):
        ry = my + 24 + i * 13
        d.rectangle([kx0 + 10, ry + 1, kx0 + 22, ry + 10], fill=col)
        d.text((kx0 + 28, ry), name, font=font(SANS_B, 10), fill=INK)
        ctxt = str(count)
        d.text((kx0 + kw - 12 - d.textlength(ctxt, font=font(SANS_B, 10)),
                ry), ctxt, font=font(SANS_B, 10), fill=INK)
    d.line([(kx0 + 10, my + 104), (kx0 + kw - 10, my + 104)],
           fill=PANEL_LINE, width=1)
    d.text((kx0 + 10, my + 107), "31 stories · 11 on the Ukraine war",
           font=font(SANS, 9), fill=GREY)

    # ================= NUMBERED LIST =================
    list_items = [
        (9, "Chess: Gukesh–Sindarov Game 1 drawn",
         "World title match opens in Geneva; 38-move Berlin ends in "
         "threefold repetition. 0.5–0.5."),
        (10, "German strike wave widens",
         "40,000 more metalworkers walk out Tue; Airbus plants hit. IG "
         "Metall wants 5%."),
        (11, "Malaysia sends 6,803 home to Myanmar",
         "Anwar defends returns despite the ICJ genocide ruling; 1,500 by "
         "ship in Dec, 5,303 by air."),
        (12, "Kyiv: 432,519 Russian troops lost in 2026",
         "General Staff figure, published Tue, already beats the 2024 "
         "annual record."),
        (13, "Zaporizhzhia bombed: 2 killed, 11 hurt",
         "Russian guided bombs hit flats in the early hours; a five-storey "
         "block partly collapses."),
        (14, "Korosten station drone kills 1",
         "Russian drone hits the railway station in Zhytomyr region; two "
         "more wounded."),
        (15, "Vinnytsia drones wound 4",
         "Early-morning strikes damage energy sites, a trolleybus and cars."),
        (16, "Hungary's PM visits Ukraine",
         "Péter Magyar meets Zelenskyy in Uzhhorod, Zakarpattia."),
        (17, "UAE bus crash kills 13",
         "Bus with 41 aboard hits a broken-down truck in Ras Al Khaimah at "
         "dawn; 14 injured."),
        (18, "Sudan: drone cuts power for millions",
         "RSF drone hits al-Markhiyat transformer Tue; Khartoum and Gezira "
         "blacked out."),
        (19, "Baghdad moves on Kurdish oilfields",
         "PM Zaidi orders federal control of fields and crossings; Barzani "
         "rejects it."),
        (20, "Gaza: Hamas security chief killed",
         "Israeli strike kills Naeem Abu Nahel in Gaza City; six others "
         "also dead."),
        (21, "Rescue worker killed in Kramatorsk",
         "Ukrainian emergency service employee, 37, dies in a Russian "
         "attack Tue."),
        (22, "Kyiv: port strikes threaten food",
         "FM Sybiha tells the UN Council that attacks on ports and export "
         "routes risk global supplies."),
        (23, "Zelenskyy confirms Sparta II strike",
         "Kyiv says the Gulf of Finland hit was lawful; FM defends the "
         "Libya raid as self-defence."),
        (24, "Poland: drone 'assumed deliberate'",
         "Deputy minister speaks Tue after a Russian jet drone looped over "
         "Dorohusk; Poland held fire."),
        (25, "Congo rebels claim downed plane found",
         "FRN says the wreckage lies near Minembwe; a S. African pilot is "
         "held. Unverified."),
        (26, "Hanoi restaurant blast kills 6",
         "Suspected gas explosion wrecks a hot-pot restaurant Tue morning."),
        (27, "Russia advances in Zaporizhzhia",
         "DeepState reports gains near Vozdvizhivka and Bilohirya."),
        (28, "Wall Street splits at the close",
         "Dow +0.9% to 50,019, over 50,000; S&P −0.5%, Nasdaq −1.5% as "
         "Nvidia gives back 5.9%."),
        (29, "Lula snubs Milei",
         "No invite to the Jan 5 inauguration after Argentina's FM cast "
         "doubt on Brazil's vote."),
        (30, "Iran claims 4th tanker hit a mine",
         "Tehran says another tanker caught fire Tue in Hormuz; claims "
         "unverified. Brent −0.45%."),
        (31, "Bayelsa boat toll rises to 32",
         "Crane lifts the wreck of Friday's capsized boat; it carried 500+ "
         "for a 200 capacity."),
    ]
    lh_y = 616
    d.text((M, lh_y), "ALSO TODAY — 23 MORE VERIFIED STORIES",
           font=font(SERIF_B, 15), fill=INK)
    d.line([(M, lh_y + 21), (1002, lh_y + 21)], fill=RED, width=2)
    row_h = 26
    for idx, (num, head, detail) in enumerate(list_items):
        col = 0 if idx < 12 else 1
        row = idx if idx < 12 else idx - 12
        x0 = M if col == 0 else 522
        y0 = 642 + row * row_h
        if row % 2 == 0:
            d.rectangle([x0 - 4, y0 - 2, x0 + 476, y0 + row_h - 4],
                        fill=(240, 234, 216))
        # number chip
        d.rectangle([x0, y0 + 1, x0 + 19, y0 + 16], fill=NAVY)
        ntxt = str(num)
        nw = d.textlength(ntxt, font=font(SANS_B, 9))
        d.text((x0 + (19 - nw) / 2, y0 + 3), ntxt, font=font(SANS_B, 9),
               fill=WHITE)
        d.text((x0 + 24, y0), head, font=font(SANS_B, 11), fill=INK)
        d.text((x0 + 24, y0 + 13), detail, font=font(SANS, 9.5),
               fill=(70, 66, 58))

    # ================= FOOTER =================
    fy = 962
    d.line([(M, fy - 4), (1002, fy - 4)], fill=INK, width=1)
    foot = [
        ("DATE CHECK — NOT TUESDAY (all MONDAY 23 NOV): ",
         "NATO space vow · Estonia warning · Megaspeed blacklist · "
         "Puigdemont amnesty · EU 22nd sanctions · Trump hush-money ruling "
         "· Nepal PM India visit · Delta deal"),
        ("", "El Chapo trial · Ma spy sentence · Pentagon–Canada rebuke · "
         "Fiji closure order · 700,000 dead report · COP31 collapse · "
         "Merkury sinking · Cikande fire · Huang +31% Nvidia · Democrats "
         "258"),
        ("OLDER: ", "ICJ Myanmar ruling (Thu 19 Nov) · Lagarde resigns "
         "(29 Oct) · Kiros elected (3 Nov) · S. Africa polls (4 Nov) · "
         "Tajikistan ICC exit (20 Nov) · El Salvador troops (Fri 20 Nov)"),
        ("NOT YET KNOWN: ", "whether Iran's Hormuz mine claims check out. "
         "Drawn entirely in code — no AI images. Sources: Reuters · AP · "
         "Yonhap · CNA · Nikkei · Sanofi · CMSA · JCS · BBC · Al Jazeera. "
         "Entry by @herza-afril."),
    ]
    for i, (bold, rest) in enumerate(foot):
        yy = fy + i * 12
        xx = M
        if bold:
            d.text((xx, yy), bold, font=font(SANS_B, 9), fill=RED_DARK)
            xx += d.textlength(bold, font=font(SANS_B, 9))
        d.text((xx, yy), rest, font=font(SANS, 9), fill=(60, 56, 48))

    return img


if __name__ == "__main__":
    image = build()
    image.save("entry.png", optimize=True)
    print("saved entry.png", image.size)
