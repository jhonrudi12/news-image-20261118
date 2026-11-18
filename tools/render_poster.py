#!/usr/bin/env python3
"""Render the 18 November 2026 world-news poster (1024x1024, deterministic).

Run:  python3 tools/render_poster.py   (writes assets/poster.png)
No network, no randomness, no timestamps in the output: re-running produces
byte-identical PNG bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (176, 42, 30)
GOLD = (184, 134, 48)
GREY = (90, 86, 76)
LIGHT_LINE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype"
F_SERIF_BLACK = os.path.join(FONT_DIR, "noto/NotoSerifDisplay-Black.ttf")
F_SERIF_BOLD = os.path.join(FONT_DIR, "noto/NotoSerif-Bold.ttf")
F_SERIF = os.path.join(FONT_DIR, "noto/NotoSerif-Regular.ttf")
F_SERIF_IT = os.path.join(FONT_DIR, "noto/NotoSerif-Italic.ttf")
F_SANS_BOLD = os.path.join(FONT_DIR, "noto/NotoSans-Bold.ttf")
F_SANS = os.path.join(FONT_DIR, "noto/NotoSans-Regular.ttf")
F_SANS_BLACK = os.path.join(FONT_DIR, "noto/NotoSans-Black.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label):
    f = font(F_SANS_BLACK, 19)
    draw.text((x, y), label, font=f, fill=RED)
    return y + 26


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations
def ill_gulf(draw, x, y, w, h):
    """Dusk sky over the Gulf: radar dome, drone, interception bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 42, 68))
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(16, 66, 92))
    # stars
    for sx, sy, r in [(0.12, 0.14, 2), (0.3, 0.08, 2), (0.55, 0.16, 2),
                      (0.78, 0.1, 2), (0.9, 0.22, 2), (0.42, 0.24, 2)]:
        draw.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r, y + sy * h + r],
                     fill=(240, 230, 190))
    # moon
    draw.ellipse([x + 0.80 * w, y + 0.10 * h, x + 0.93 * w, y + 0.32 * h],
                 fill=(240, 230, 190))
    # radar dome + mast on a base
    bx, by = x + 0.10 * w, y + 0.62 * h
    draw.rectangle([bx, by, bx + 0.34 * w, by + 0.16 * h], fill=(52, 74, 102))
    draw.line([bx + 0.17 * w, by, bx + 0.17 * w, by - 0.22 * h], fill=(180, 190, 200), width=4)
    draw.pieslice([bx + 0.06 * w, by - 0.40 * h, bx + 0.28 * w, by - 0.04 * h],
                  180, 360, fill=(215, 222, 230))
    # radar sweep lines
    draw.line([bx + 0.17 * w, by - 0.22 * h, bx + 0.34 * w, by - 0.42 * h],
              fill=(240, 200, 90), width=3)
    # drone silhouette (quadcopter: body + 4 rotors + legs)
    dx, dy = x + 0.62 * w, y + 0.30 * h
    draw.ellipse([dx - 44, dy - 16, dx - 26, dy - 10], fill=(12, 12, 14))
    draw.ellipse([dx + 26, dy - 16, dx + 44, dy - 10], fill=(12, 12, 14))
    draw.line([dx - 36, dy - 4, dx - 16, dy + 2], fill=(12, 12, 14), width=4)
    draw.line([dx + 16, dy + 2, dx + 36, dy - 4], fill=(12, 12, 14), width=4)
    draw.rounded_rectangle([dx - 18, dy - 4, dx + 18, dy + 10], radius=6, fill=(12, 12, 14))
    draw.line([dx - 10, dy + 10, dx - 14, dy + 22], fill=(12, 12, 14), width=3)
    draw.line([dx + 10, dy + 10, dx + 14, dy + 22], fill=(12, 12, 14), width=3)
    # interception bursts (orange starbursts)
    for cx, cy, r in [(0.52, 0.52, 16), (0.86, 0.46, 12)]:
        px, py = x + cx * w, y + cy * h
        for ang in range(0, 360, 45):
            import math
            ex = px + r * math.cos(math.radians(ang))
            ey = py + r * math.sin(math.radians(ang))
            draw.line([px, py, ex, ey], fill=(245, 150, 40), width=4)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 210, 90))
    # sea glints
    for gx in (0.45, 0.6, 0.75, 0.9):
        draw.line([x + gx * w, y + 0.80 * h, x + (gx + 0.06) * w, y + 0.80 * h],
                  fill=(120, 180, 210), width=3)


def ill_bridge(draw, x, y, w, h):
    """Kerch bridge: deck with a gap, a broken span falling into the strait."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    draw.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(64, 110, 138))
    # deck, two halves with a gap in the middle
    dy = y + 0.52 * h
    draw.rectangle([x, dy, x + 0.38 * w, dy + 10], fill=(70, 70, 78))
    draw.rectangle([x + 0.62 * w, dy, x + w, dy + 10], fill=(70, 70, 78))
    # pylons under each half
    for px in (0.10, 0.30, 0.70, 0.90):
        draw.line([x + px * w, dy + 10, x + px * w, y + 0.68 * h], fill=(70, 70, 78), width=5)
    # broken span, tilted down into the water (dark deck, red underside)
    draw.polygon([(x + 0.40 * w, dy + 2), (x + 0.60 * w, dy + 2),
                  (x + 0.54 * w, dy + 40), (x + 0.46 * w, dy + 40)],
                 fill=(70, 70, 78))
    draw.polygon([(x + 0.40 * w, dy + 2), (x + 0.60 * w, dy + 2),
                  (x + 0.58 * w, dy + 12), (x + 0.42 * w, dy + 12)],
                 fill=(176, 42, 30))
    # splash + smoke
    draw.ellipse([x + 0.38 * w, y + 0.60 * h, x + 0.54 * w, y + 0.76 * h], fill=(240, 244, 246))
    draw.ellipse([x + 0.44 * w, y + 0.54 * h, x + 0.52 * w, y + 0.64 * h], fill=(240, 244, 246))
    draw.ellipse([x + 0.30 * w, y + 0.28 * h, x + 0.40 * w, y + 0.38 * h], fill=(120, 120, 118))
    draw.ellipse([x + 0.36 * w, y + 0.22 * h, x + 0.44 * w, y + 0.30 * h], fill=(150, 150, 148))
    # water lines
    for wy in (0.78, 0.88):
        draw.line([x + 0.05 * w, y + wy * h, x + 0.95 * w, y + wy * h],
                  fill=(140, 180, 200), width=2)


def ill_manila(draw, x, y, w, h):
    """Manila skyline at dusk with four Quad flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(252, 214, 130))
    # skyline
    base = y + h
    for bx, bw, bh in [(0.02, 0.16, 0.42), (0.20, 0.12, 0.58), (0.34, 0.18, 0.36),
                       (0.54, 0.12, 0.52), (0.68, 0.14, 0.40), (0.84, 0.14, 0.62)]:
        draw.rectangle([x + bx * w, base - bh * h, x + (bx + bw) * w, base], fill=(31, 58, 95))
    # windows
    for wx in (0.06, 0.24, 0.38, 0.58, 0.72, 0.88):
        for wy in (0.62, 0.72, 0.82):
            draw.rectangle([x + wx * w, y + wy * h, x + wx * w + 4, y + wy * h + 4],
                           fill=(252, 214, 130))
    # four flags on poles (simplified but recognisable)
    fx_list = [0.08, 0.30, 0.52, 0.74]
    for i, fx in enumerate(fx_list):
        px = x + fx * w
        fy = y + 0.06 * h
        fw, fh = 34, 22
        draw.line([px + 12, fy, px + 12, fy + fh + 14], fill=INK, width=2)
        if i == 0:  # United States: red/white stripes + blue canton
            draw.rectangle([px + 12, fy, px + 12 + fw, fy + fh], fill=(255, 255, 255))
            for s in range(4):
                draw.rectangle([px + 12, fy + s * 6, px + 12 + fw, fy + s * 6 + 3],
                               fill=(178, 34, 52))
            draw.rectangle([px + 12, fy, px + 12 + 15, fy + 11], fill=(60, 59, 110))
        elif i == 1:  # India: saffron / white / green + wheel
            draw.rectangle([px + 12, fy, px + 12 + fw, fy + 7], fill=(255, 153, 51))
            draw.rectangle([px + 12, fy + 7, px + 12 + fw, fy + 15], fill=(255, 255, 255))
            draw.rectangle([px + 12, fy + 15, px + 12 + fw, fy + fh], fill=(19, 136, 8))
            draw.ellipse([px + 25, fy + 8, px + 33, fy + 16], outline=(0, 0, 128), width=1)
        elif i == 2:  # Japan: white + red disc
            draw.rectangle([px + 12, fy, px + 12 + fw, fy + fh], fill=(255, 255, 255))
            draw.ellipse([px + 23, fy + 5, px + 35, fy + 17], fill=(188, 0, 45))
        else:  # Australia: blue + stars
            draw.rectangle([px + 12, fy, px + 12 + fw, fy + fh], fill=(0, 0, 139))
            for sx, sy in [(16, 5), (24, 9), (20, 15), (40, 16)]:
                draw.ellipse([px + sx, fy + sy, px + sx + 3, fy + sy + 3], fill=(255, 255, 255))
        draw.rectangle([px + 12, fy, px + 12 + fw, fy + fh], outline=INK, width=1)


def ill_chip(draw, x, y, w, h):
    """Green AI chip with a rising chart arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 244, 230))
    cx, cy = x + 0.38 * w, y + 0.52 * h
    s = int(0.42 * w)
    # pins
    for i in range(4):
        off = -s // 2 + i * (s // 3)
        draw.line([cx + off, cy - s // 2 - 14, cx + off, cy - s // 2], fill=(60, 60, 60), width=4)
        draw.line([cx + off, cy + s // 2, cx + off, cy + s // 2 + 14], fill=(60, 60, 60), width=4)
        draw.line([cx - s // 2 - 14, cy + off, cx - s // 2, cy + off], fill=(60, 60, 60), width=4)
        draw.line([cx + s // 2, cy + off, cx + s // 2 + 14, cy + off], fill=(60, 60, 60), width=4)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2], fill=(22, 110, 60))
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4], fill=(16, 80, 44))
    draw.text((cx, cy), "AI", font=font(F_SANS_BLACK, 22), fill=(255, 255, 255), anchor="mm")
    # rising arrow
    ax0, ay0 = x + 0.62 * w, y + 0.78 * h
    draw.line([ax0, ay0, x + 0.74 * w, y + 0.55 * h, x + 0.86 * w, y + 0.62 * h,
               x + 0.97 * w, y + 0.28 * h], fill=(176, 42, 30), width=6, joint="curve")
    draw.polygon([(x + 0.97 * w, y + 0.28 * h), (x + 0.90 * w, y + 0.26 * h),
                  (x + 0.95 * w, y + 0.38 * h)], fill=(176, 42, 30))


def ill_cyclone(draw, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal coast."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=(206, 224, 234))
    # sea
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(64, 110, 138))
    # land (right side coast)
    draw.polygon([(x + 0.62 * w, y), (x + w, y), (x + w, y + h),
                  (x + 0.58 * w, y + h), (x + 0.66 * w, y + 0.55 * h),
                  (x + 0.58 * w, y + 0.30 * h)], fill=(214, 196, 150))
    # spiral
    cx, cy = x + 0.38 * w, y + 0.42 * h
    for turns in range(3):
        pts = []
        for a in range(0, 360, 6):
            t = math.radians(a + turns * 360)
            r = 8 + (turns * 360 + a) / 1080 * 46
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 0.85))
        draw.line(pts, fill=(31, 58, 95), width=5)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(248, 244, 233))
    # rain streaks
    for rx in (0.15, 0.28, 0.55, 0.7, 0.85):
        draw.line([x + rx * w, y + 0.78 * h, x + (rx - 0.03) * w, y + 0.92 * h],
                  fill=(240, 244, 246), width=3)


def ill_gaza(draw, x, y, w, h):
    """Warning triangle over tents: a ceasefire under strain."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # tents
    for tx, tw in [(0.06, 0.26), (0.36, 0.26), (0.66, 0.26)]:
        px = x + tx * w
        draw.polygon([(px, y + 0.88 * h), (px + tw * w / 2, y + 0.55 * h),
                      (px + tw * w, y + 0.88 * h)], fill=(196, 168, 120))
        draw.polygon([(px + tw * w * 0.42, y + 0.88 * h), (px + tw * w / 2, y + 0.68 * h),
                      (px + tw * w * 0.58, y + 0.88 * h)], fill=(90, 70, 50))
    # warning triangle
    tx0, ty0 = x + 0.30 * w, y + 0.08 * h
    draw.polygon([(tx0, ty0), (tx0 + 0.40 * w, ty0), (tx0 + 0.20 * w, ty0 + 0.42 * h)],
                 fill=(245, 180, 40), outline=INK)
    draw.text((tx0 + 0.20 * w, ty0 + 0.20 * h), "!", font=font(F_SANS_BLACK, 44),
              fill=INK, anchor="mm")


# ---------------------------------------------------------------- poster
def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=LIGHT_LINE, width=1)

    # top strip
    f_top = font(F_SANS_BOLD, 20)
    d.text((M, 30), "WORLD NEWS  •  ONE DAY, ONE PAGE", font=f_top, fill=NAVY)
    d.text((W - M, 30), "No. 322", font=f_top, fill=GREY, anchor="ra")

    # masthead
    f_mast = font(F_SERIF_BLACK, 74)
    d.text((W // 2, 56), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    rule(d, M, 142, W - M, 3)
    rule(d, M, 148, W - M, 1)

    # date line
    f_date = font(F_SANS_BLACK, 30)
    d.text((W // 2, 158), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date, fill=RED, anchor="ma")

    # ---------------- lead story: the Gulf
    ly = 208
    ill_w, ill_h = 350, 216
    ill_gulf(d, W - M - ill_w, ly + 8, ill_w, ill_h)
    d.text((W - M - ill_w, ly + 230), "Bahrain later gave the all-clear.",
           font=font(F_SERIF_IT, 16), fill=GREY)
    tx = M
    y = kicker(d, tx, ly, "THE GULF  •  IRAN–U.S. CLASH")
    f_lead = font(F_SERIF_BOLD, 38)
    headline = "Gulf on edge as Iran's drones\ntarget a U.S. radar in Bahrain"
    y = text_block(d, tx, y, headline.split("\n"), f_lead, INK, 44)
    f_body = font(F_SANS, 21)
    summary = ("Iran's Revolutionary Guards said they launched drones at the "
               "U.S.-operated radar at Sheikh Isa Air Base. U.S. jets then struck "
               "a missile site on Qeshm Island, and Kuwait's air defences "
               "intercepted drones overnight.")
    y = text_block(d, tx, y + 8, wrap(d, summary, f_body, 596), f_body, (48, 48, 48), 27)
    rule(d, M, 478, W - M, 2)

    # ---------------- 2x2 grid
    grid = [
        ("UKRAINE  •  WAR", "Crimea bridge crumbles as Kyiv's bridges are hit",
         "The road arch fell into the sea. Russia hit Kyiv's North and South "
         "bridges and damaged the metro.",
         ill_bridge),
        ("ASIA  •  DIPLOMACY", "Trump joins first Quad summit in two years",
         "Leaders agreed critical-minerals deals. Trump meets President "
         "Marcos today, then flies to Shenzhen.",
         ill_manila),
        ("TECH  •  MARKETS", "Nvidia's sales double to $115.8 billion",
         "Revenue rose 103% in its first report since CEO Jensen Huang "
         "resigned. Guidance: $130 billion next quarter.",
         ill_chip),
        ("WEATHER  •  INDIA", "Cyclone Akvan nears India's east coast",
         "The storm strengthened over the Bay of Bengal. Andhra Pradesh and "
         "Odisha are on high alert.",
         ill_cyclone),
    ]
    gx0, gy0 = M, 490
    cw, ch = 472, 158
    for i, (kick, head, summ, ill) in enumerate(grid):
        cx = gx0 + (i % 2) * (cw + 20)
        cy = gy0 + (i // 2) * (ch + 10)
        iw, ih = 120, 120
        ill(d, cx, cy + 6, iw, ih)
        tx2 = cx + iw + 12
        tw = cw - iw - 12
        y2 = kicker(d, tx2, cy, kick)
        f_h = font(F_SERIF_BOLD, 25)
        y2 = text_block(d, tx2, y2, wrap(d, head, f_h, tw), f_h, INK, 28)
        f_s = font(F_SANS, 19)
        text_block(d, tx2, y2 + 4, wrap(d, summ, f_s, tw), f_s, (48, 48, 48), 23)

    rule(d, M, 826, W - M, 2)

    # ---------------- bottom strip: Gaza
    by = 838
    ill_gaza(d, M, by, 210, 108)
    tx3 = M + 226
    y3 = kicker(d, tx3, by, "GAZA  •  CEASEFIRE")
    f_h3 = font(F_SERIF_BOLD, 29)
    y3 = text_block(d, tx3, y3, ["Board of Peace warns Gaza truce"], f_h3, INK, 32)
    y3 = text_block(d, tx3, y3, ["faces 'imminent collapse'"], f_h3, INK, 32)
    f_s3 = font(F_SANS, 20)
    text_block(d, tx3, y3 + 6,
               wrap(d, "The board said the ceasefire could fail without urgent action, "
                       "as aid groups warn families are running short of food and fuel.",
                    f_s3, W - M - tx3), f_s3, (48, 48, 48), 25)

    # footer
    rule(d, M, 984, W - M, 1)
    d.text((W // 2, 989), "Early edition  •  Sources: Reuters, Al Jazeera, AP, AFP  •  18 November 2026 (UTC)",
           font=font(F_SANS, 14), fill=GREY, anchor="ma")

    img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    out = os.path.join(root, "assets", "poster.png")
    render(out)
    print(out, os.path.getsize(out), "bytes")
