#!/usr/bin/env python3
"""One-day newspaper front page for Sunday 22 November 2026.

Everything is drawn from fixed values: the same palette, the same
fonts, no clock, no dice, no network. Run the script twice and the
PNG bytes come out identical.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 36
FAR = 988

PAPER_RGB = (248, 243, 232)
INK_RGB = (24, 24, 24)
FLAG_RGB = (168, 24, 34)
NAVY_RGB = (30, 56, 94)
FAINT_RGB = (92, 88, 80)
DIVIDER_RGB = (200, 192, 175)

DAWN_HIGH = (46, 64, 112)
DAWN_MID = (198, 112, 68)
DAWN_LOW = (240, 180, 106)
SEA_RGB = (38, 84, 110)
SEA_LINE = (24, 60, 84)
HILL_RGB = (58, 66, 52)
SUN_RGB = (255, 226, 150)
BUILDING_RGB = (240, 236, 224)

DEJAVU = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = DEJAVU + "/DejaVuSerif-Bold.ttf"
SERIF_PLAIN = DEJAVU + "/DejaVuSerif.ttf"
SANS_PLAIN = DEJAVU + "/DejaVuSans.ttf"
SANS_BOLD = DEJAVU + "/DejaVuSans-Bold.ttf"


def font_at(path, size):
    return ImageFont.truetype(path, size)


def shrink_to(draw, path, text, limit, start):
    """Biggest size at or below `start` that fits `text` inside `limit`."""
    size = start
    while size > 10:
        candidate = font_at(path, size)
        if draw.textlength(text, font=candidate) <= limit:
            return candidate
        size -= 1
    return font_at(path, 10)


def wrap_text(draw, text, face, limit):
    """Split `text` into lines no wider than `limit` pixels."""
    out = []
    current = ""
    for word in text.split():
        joined = (current + " " + word).strip()
        if draw.textlength(joined, font=face) <= limit:
            current = joined
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def bar(draw, left, right, y, colour=INK_RGB, thick=2):
    draw.line([(left, y), (right, y)], fill=colour, width=thick)


def draw_nameplate(draw):
    name = font_at(SERIF_BOLD, 76)
    draw.text((PAGE // 2, 28), "THE WORLD TODAY", font=name, fill=INK_RGB,
              anchor="ma")
    bar(draw, EDGE, FAR, 126, INK_RGB, 4)
    bar(draw, EDGE, FAR, 132, INK_RGB, 1)
    dateline = font_at(SANS_BOLD, 21)
    draw.text((PAGE // 2, 142),
              "SUNDAY, 22 NOVEMBER 2026  |  ONE DAY, ONE IMAGE",
              font=dateline, fill=FLAG_RGB, anchor="ma")


LEAD = {
    "kicker": "CLIMATE",
    "head": "COP31 CLOSES IN ON A DEAL",
    "deck": "Antalya talks near a final pact after running past their Friday deadline",
    "body": ("COP31 presidents Australia and Turkey put forward a text they "
             "say every side can accept. Nearly 200 delegations have until "
             "03:00 GMT to object, with approval set for Sunday morning."),
}


def draw_dawn_panel(draw, left, top, right, bottom):
    """Sunrise over the Antalya shore: banded sky, sun, sea, hills."""
    draw.rectangle([left, top, right, bottom], fill=DAWN_HIGH)
    sky_h = int((bottom - top) * 0.58)
    steps = 28
    for step in range(steps):
        frac = step / (steps - 1)
        if frac < 0.5:
            lo, hi, u = DAWN_HIGH, DAWN_MID, frac * 2
        else:
            lo, hi, u = DAWN_MID, DAWN_LOW, (frac - 0.5) * 2
        shade = tuple(int(lo[i] + (hi[i] - lo[i]) * u) for i in range(3))
        y = top + sky_h * step // steps
        draw.rectangle([left, y, right, y + sky_h // steps + 1], fill=shade)
    sea_line = top + sky_h
    sun_x, sun_y, sun_r = left + 190, sea_line - 42, 34
    draw.ellipse([sun_x - sun_r - 8, sun_y - sun_r - 8,
                  sun_x + sun_r + 8, sun_y + sun_r + 8],
                 outline=SUN_RGB, width=2)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r,
                  sun_x + sun_r, sun_y + sun_r], fill=SUN_RGB)
    for k in range(5):
        y = sea_line + 8 + k * 14
        half = 26 + k * 10
        draw.line([(sun_x - half, y), (sun_x + half, y)],
                  fill=(255, 214, 130), width=3)
    draw.rectangle([left, sea_line, right, bottom], fill=SEA_RGB)
    for k in range(4):
        y = sea_line + 26 + k * 22
        draw.line([(left + 14, y), (right - 14, y)], fill=SEA_LINE, width=2)
    draw.polygon([(left, sea_line), (left + 90, sea_line - 34),
                  (left + 170, sea_line - 12), (left + 250, sea_line - 40),
                  (left + 330, sea_line - 8), (right, sea_line - 18),
                  (right, sea_line)], fill=HILL_RGB)
    tower_x = left + 30
    draw.rectangle([tower_x, sea_line - 46, tower_x + 8, sea_line],
                   fill=BUILDING_RGB)
    draw.polygon([(tower_x - 3, sea_line - 46),
                  (tower_x + 4, sea_line - 62),
                  (tower_x + 11, sea_line - 46)], fill=BUILDING_RGB)
    draw.rectangle([tower_x + 16, sea_line - 18, tower_x + 64, sea_line],
                   fill=(232, 226, 210))
    caption = font_at(SANS_BOLD, 17)
    draw.text((left + 12, bottom - 30), "ANTALYA, TURKIYE",
              font=caption, fill=(255, 255, 255))


def draw_lead_story(draw):
    top = 176
    kicker_face = font_at(SANS_BOLD, 22)
    draw.text((EDGE, top), LEAD["kicker"], font=kicker_face, fill=FLAG_RGB)
    head_face = shrink_to(draw, SERIF_BOLD, LEAD["head"], 570, 38)
    draw.text((EDGE, top + 30), LEAD["head"], font=head_face, fill=INK_RGB)
    deck_face = font_at(SERIF_PLAIN, 24)
    deck_lines = wrap_text(draw, LEAD["deck"], deck_face, 560)
    y = top + 84
    for line in deck_lines:
        draw.text((EDGE, y), line, font=deck_face, fill=NAVY_RGB)
        y += 30
    body_face = font_at(SANS_PLAIN, 19)
    y += 14
    for line in wrap_text(draw, LEAD["body"], body_face, 560):
        draw.text((EDGE, y), line, font=body_face, fill=INK_RGB)
        y += 25
    draw_dawn_panel(draw, 620, top, FAR, top + 300)
    bar(draw, EDGE, FAR, top + 318, INK_RGB, 2)


STORIES = [
    {"kicker": "BALTIC SEA",
     "head": "DRONES SET RUSSIAN SHIP ABLAZE",
     "body": ("Sparta II, bound for Kaliningrad, is hit in the Gulf of "
              "Finland and drifts into Finnish waters, still burning. "
              "Helsinki says Ukraine is likely behind it.")},
    {"kicker": "NATO",
     "head": "RUTTE: EVERY INCH DEFENDED",
     "body": ("A day after Russian missiles landed in Poland, the NATO "
              "chief vows in Warsaw to defend all Polish territory. Its "
              "council meets on Monday.")},
    {"kicker": "MEXICO",
     "head": "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
     "body": ("FBI Ten Most Wanted boss Fausto Isidro Meza-Flores is "
              "seized in Guasave; 11 die \u2014 four soldiers, seven "
              "gunmen \u2014 as Sinaloa erupts.")},
    {"kicker": "BRAZIL",
     "head": "BOLSONARO IN INTENSIVE CARE",
     "body": ("The jailed ex-president, 71, is admitted in Brasilia with "
              "an acute bowel obstruction; doctors say he is stable and "
              "conscious.")},
    {"kicker": "NIGERIA",
     "head": "BOAT CAPSIZES; AT LEAST 24 DEAD",
     "body": ("A boat carrying mourners to a funeral sinks in Bayelsa "
              "state; emergency services put the toll at 24 as the "
              "search goes on.")},
    {"kicker": "UKRAINE",
     "head": "MISSILE HITS ZELENSKY\u2019S HOME CITY",
     "body": ("A ballistic missile strike on Kryvyi Rih kills two and "
              "wounds 60, as Russia\u2019s war keeps spilling across "
              "borders.")},
]

FOOTER = [
    "India 486 for 4 at stumps on day three in Wellington, lead by 118 \u2014 Rahul 136",
    "France asks the UN Security Council to act after Myanmar rejects the ICJ genocide ruling",
]


def draw_story_card(draw, left, top, width, item):
    kicker_face = font_at(SANS_BOLD, 17)
    draw.text((left, top), item["kicker"], font=kicker_face, fill=FLAG_RGB)
    head_face = shrink_to(draw, SERIF_BOLD, item["head"], width, 21)
    draw.text((left, top + 24), item["head"], font=head_face, fill=INK_RGB)
    body_face = font_at(SANS_PLAIN, 16)
    y = top + 58
    for line in wrap_text(draw, item["body"], body_face, width)[:3]:
        draw.text((left, y), line, font=body_face, fill=INK_RGB)
        y += 21


def draw_footer(draw):
    y = 944
    bar(draw, EDGE, FAR, y, INK_RGB, 2)
    face = font_at(SANS_PLAIN, 15)
    for line in FOOTER:
        draw.text((PAGE // 2, y + 12), line, font=face, fill=FAINT_RGB,
                  anchor="ma")
        y += 22


def render_front_page(path):
    page = Image.new("RGB", (PAGE, PAGE), PAPER_RGB)
    draw = ImageDraw.Draw(page)
    draw_nameplate(draw)
    draw_lead_story(draw)
    grid_x, grid_y = EDGE, 522
    cell_w, cell_h = 466, 126
    for pos, item in enumerate(STORIES):
        col, row = pos % 2, pos // 2
        x = grid_x + col * (cell_w + 20)
        y = grid_y + row * (cell_h + 14)
        draw_story_card(draw, x, y, cell_w, item)
        if col == 0:
            draw.line([(x + cell_w + 10, y + 4),
                       (x + cell_w + 10, y + cell_h - 4)],
                      fill=DIVIDER_RGB, width=1)
    draw_footer(draw)
    page.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    render_front_page(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
