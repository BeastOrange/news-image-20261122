#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Sunday 22 November 2026.

Deterministic: fixed palette, fixed fonts, no randomness, no timestamps,
no network. Two runs produce byte-identical PNG output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
DAWN_TOP = (44, 62, 110)
DAWN_MID = (196, 110, 66)
DAWN_LOW = (238, 178, 104)
SEA = (38, 84, 110)
SEA_DARK = (24, 60, 84)
LAND = (58, 66, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def load(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, path, text, max_w, start):
    """Largest font size at or below `start` whose text fits `max_w`."""
    size = start
    while size > 10:
        fnt = load(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return load(path, 10)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to lines fitting `width` pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def hline(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def masthead(draw):
    title = load(SERIF_B, 76)
    draw.text((W // 2, 28), "THE WORLD TODAY", font=title, fill=INK,
              anchor="ma")
    hline(draw, 36, 988, 126, INK, 4)
    hline(draw, 36, 988, 132, INK, 1)
    date_f = load(SANS_B, 21)
    draw.text((W // 2, 142), "SUNDAY, 22 NOVEMBER 2026  |  ONE DAY, ONE IMAGE",
              font=date_f, fill=RED, anchor="ma")


LEAD_KICKER = "CLIMATE"
LEAD_HEAD = "COP31 CLOSES IN ON A DEAL"
LEAD_SUB = "Antalya talks near a final pact after running past their Friday deadline"
LEAD_BODY = ("COP31 presidents Australia and Turkey put forward a text they "
             "say every side can accept. Nearly 200 delegations have until "
             "03:00 GMT to object, with approval set for Sunday morning.")


def scene(draw, x0, y0, x1, y1):
    """Dawn over the Antalya coast: sky bands, rising sun, sea, shore."""
    draw.rectangle([x0, y0, x1, y1], fill=DAWN_TOP)
    bands = 28
    span = int((y1 - y0) * 0.58)
    for i in range(bands):
        t = i / (bands - 1)
        if t < 0.5:
            a, b, u = DAWN_TOP, DAWN_MID, t * 2
        else:
            a, b, u = DAWN_MID, DAWN_LOW, (t - 0.5) * 2
        col = tuple(int(a[c] + (b[c] - a[c]) * u) for c in range(3))
        yy = y0 + span * i // bands
        draw.rectangle([x0, yy, x1, yy + span // bands + 1], fill=col)
    horizon = y0 + span
    # sun disc low over the water
    sx, sy, sr = x0 + 190, horizon - 42, 34
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 226, 150))
    draw.ellipse([sx - sr - 8, sy - sr - 8, sx + sr + 8, sy + sr + 8],
                 outline=(255, 226, 150), width=2)
    # sun path on the water
    for k in range(5):
        yy = horizon + 8 + k * 14
        ww = 26 + k * 10
        draw.line([(sx - ww, yy), (sx + ww, yy)], fill=(255, 214, 130),
                  width=3)
    # sea
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for k in range(4):
        yy = horizon + 26 + k * 22
        draw.line([(x0 + 14, yy), (x1 - 14, yy)], fill=SEA_DARK, width=2)
    # distant Taurus mountains and shore
    draw.polygon([(x0, horizon), (x0 + 90, horizon - 34),
                  (x0 + 170, horizon - 12), (x0 + 250, horizon - 40),
                  (x0 + 330, horizon - 8), (x1, horizon - 18), (x1, horizon)],
                 fill=LAND)
    # a white minaret and rooftops on the shore
    bx = x0 + 30
    draw.rectangle([bx, horizon - 46, bx + 8, horizon], fill=(240, 236, 224))
    draw.polygon([(bx - 3, horizon - 46), (bx + 4, horizon - 62),
                  (bx + 11, horizon - 46)], fill=(240, 236, 224))
    draw.rectangle([bx + 16, horizon - 18, bx + 64, horizon],
                   fill=(232, 226, 210))
    lab = load(SANS_B, 17)
    draw.text((x0 + 12, y1 - 30), "ANTALYA, TURKIYE",
              font=lab, fill=(255, 255, 255))


def lead(draw):
    x0, x1 = 36, 988
    y = 176
    kick = load(SANS_B, 22)
    draw.text((x0, y), LEAD_KICKER, font=kick, fill=RED)
    head = fit(draw, SERIF_B, LEAD_HEAD, 570, 38)
    draw.text((x0, y + 30), LEAD_HEAD, font=head, fill=INK)
    sub = load(SERIF, 24)
    sub_lines = wrap(draw, LEAD_SUB, sub, 560)
    sy = y + 84
    for i, line in enumerate(sub_lines):
        draw.text((x0, sy + i * 30), line, font=sub, fill=NAVY)
    body = load(SANS, 19)
    by = sy + 30 * len(sub_lines) + 14
    for i, line in enumerate(wrap(draw, LEAD_BODY, body, 560)):
        draw.text((x0, by + i * 25), line, font=body, fill=INK)
    scene(draw, 620, y, x1, y + 300)
    hline(draw, x0, x1, y + 318, INK, 2)


STORIES = [
    ("BALTIC SEA", "DRONES SET RUSSIAN SHIP ABLAZE",
     "Sparta II, bound for Kaliningrad, is hit in the Gulf of Finland "
     "and drifts into Finnish waters, still burning. Helsinki says "
     "Ukraine is likely behind it."),
    ("NATO", "RUTTE: EVERY INCH DEFENDED",
     "A day after Russian missiles landed in Poland, the NATO chief "
     "vows in Warsaw to defend all Polish territory. Its council "
     "meets on Monday."),
    ("MEXICO", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
     "FBI Ten Most Wanted boss Fausto Isidro Meza-Flores is seized in "
     "Guasave; 11 die \u2014 four soldiers, seven gunmen \u2014 as "
     "Sinaloa erupts."),
    ("BRAZIL", "BOLSONARO IN INTENSIVE CARE",
     "The jailed ex-president, 71, is admitted in Brasilia with an "
     "acute bowel obstruction; doctors say he is stable and conscious."),
    ("NIGERIA", "BOAT CAPSIZES; AT LEAST 24 DEAD",
     "A boat carrying mourners to a funeral sinks in Bayelsa state; "
     "emergency services put the toll at 24 as the search goes on."),
    ("UKRAINE", "MISSILE HITS ZELENSKY\u2019S HOME CITY",
     "A ballistic missile strike on Kryvyi Rih kills two and wounds "
     "60, as Russia\u2019s war keeps spilling across borders."),
]

FOOTER_LINES = [
    "India 486 for 4 at stumps on day three in Wellington, lead by 118 \u2014 Rahul 136",
    "France asks the UN Security Council to act after Myanmar rejects the ICJ genocide ruling",
]


def card(draw, x0, y0, w, kicker, headline, blurb):
    kf = load(SANS_B, 17)
    draw.text((x0, y0), kicker, font=kf, fill=RED)
    hf = fit(draw, SERIF_B, headline, w, 21)
    draw.text((x0, y0 + 24), headline, font=hf, fill=INK)
    bf = load(SANS, 16)
    for i, line in enumerate(wrap(draw, blurb, bf, w)[:3]):
        draw.text((x0, y0 + 58 + i * 21), line, font=bf, fill=INK)


def footer(draw):
    y = 944
    hline(draw, 36, 988, y, INK, 2)
    ff = load(SANS, 15)
    for i, line in enumerate(FOOTER_LINES):
        draw.text((W // 2, y + 12 + i * 22), line, font=ff, fill=GREY,
                  anchor="ma")


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead(draw)
    gx, gy = 36, 522
    cw, ch = 466, 126
    gap_x, gap_y = 20, 14
    for idx, (kicker, head, blurb) in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cw + gap_x)
        y0 = gy + row * (ch + gap_y)
        card(draw, x0, y0, cw, kicker, head, blurb)
        if col == 0:
            draw.line([(x0 + cw + 10, y0 + 4), (x0 + cw + 10, y0 + ch - 4)],
                      fill=(200, 192, 175), width=1)
    footer(draw)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
