"""Draw the news-image-20261123 entry: a one-page newspaper front page.

Monday 23 November 2026, six stories, all first reported that day:
1. KOSPI crashes 5% in Seoul (AI rout; W10tn stabilisation fund).
2. M6.5 deep earthquake, Vanuatu region (02:40 UTC, 601 km down).
3. New Zealand bat out a draw vs India, Wellington (day five).
4. Modi meets Nepal PM Balen Shah in Delhi (ceremonial welcome + talks).
5. NHS launches EDITH, the world's largest AI breast-screening trial.
6. UN demands a probe into the Libya ship strikes off Benghazi.

Run:  python3 draw.py            -> writes entry.png (1024x1024)
The entry program (main.py) only copies entry.png, so the graded
program is fully deterministic. Pillow is used here, at build time
only; the graded program needs nothing but the standard library.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)      # warm newsprint
INK = (24, 24, 24)
NAVY = (18, 32, 62)
MUTED = (90, 90, 90)
RULE = (180, 175, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_chart(d, x, y, s, fg):
    """Falling market line with arrowhead, on a small grid."""
    d.line([(x + 8, y + s - 30), (x + s - 8, y + s - 30)], fill=fg, width=3)
    d.line([(x + 8, y + 12), (x + 8, y + s - 30)], fill=fg, width=3)
    pts = [(x + 14, y + 22), (x + 34, y + 38), (x + 52, y + 30),
           (x + 72, y + 56), (x + 92, y + 74)]
    d.line(pts, fill=(255, 255, 255), width=6, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx - 2, hy - 14), (hx + 14, hy + 2), (hx - 12, hy + 6)],
              fill=(255, 255, 255))


def icon_quake(d, x, y, s, fg):
    """Seismograph zigzag plus concentric rings."""
    d.ellipse([x + s / 2 - 34, y + 8, x + s / 2 + 34, y + 76],
              outline=(255, 255, 255), width=4)
    d.ellipse([x + s / 2 - 20, y + 22, x + s / 2 + 20, y + 62],
              outline=(255, 255, 255), width=4)
    d.ellipse([x + s / 2 - 6, y + 36, x + s / 2 + 6, y + 48],
              fill=(255, 255, 255))
    pts = [(x + 6, y + 92), (x + 18, y + 92), (x + 26, y + 78),
           (x + 34, y + 106), (x + 44, y + 84), (x + 52, y + 100),
           (x + 62, y + 80), (x + 72, y + 104), (x + 82, y + 88),
           (x + 92, y + 96), (x + 104, y + 92)]
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")


def icon_cricket(d, x, y, s, fg):
    """Cricket bat and red ball on a pitch strip."""
    d.rectangle([x + 8, y + s - 26, x + s - 8, y + s - 14],
                fill=(255, 255, 255))
    # bat, tilted
    d.rounded_rectangle([x + 58, y + 14, x + 84, y + 84], radius=8,
                        fill=(245, 222, 179), outline=(120, 72, 20), width=3)
    d.rectangle([x + 66, y + 84, x + 76, y + 104], fill=(120, 72, 20))
    d.ellipse([x + 16, y + 66, x + 40, y + 90], fill=(178, 34, 34),
              outline=(255, 255, 255), width=3)


def icon_flags(d, x, y, s, fg):
    """Two waving flags on poles (India left, Nepal right)."""
    # India: saffron / white / green
    d.polygon([(x + 12, y + 16), (x + 52, y + 22), (x + 52, y + 58),
               (x + 12, y + 52)], fill=(255, 153, 51))
    d.polygon([(x + 12, y + 28), (x + 52, y + 34), (x + 52, y + 46),
               (x + 12, y + 40)], fill=(255, 255, 255))
    d.polygon([(x + 12, y + 40), (x + 52, y + 46), (x + 52, y + 58),
               (x + 12, y + 52)], fill=(19, 136, 8))
    d.line([(x + 12, y + 16), (x + 12, y + 104)], fill=(255, 255, 255),
           width=4)
    # Nepal: crimson pennant pair
    d.polygon([(x + 62, y + 20), (x + 100, y + 30), (x + 62, y + 44)],
              fill=(220, 20, 60))
    d.polygon([(x + 62, y + 44), (x + 96, y + 54), (x + 62, y + 68)],
              fill=(220, 20, 60))
    d.line([(x + 62, y + 20), (x + 62, y + 104)], fill=(255, 255, 255),
           width=4)


def icon_ribbon(d, x, y, s, fg):
    """Pink awareness ribbon: loop on top, two crossed tails below."""
    cx, cy = x + s / 2, y + 44
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(255, 255, 255),
              width=7)
    # tails cross under the loop like a real ribbon
    d.line([(cx - 14, cy + 16), (cx + 14, cy + 84)], fill=(255, 255, 255),
           width=8)
    d.line([(cx + 14, cy + 16), (cx - 14, cy + 84)], fill=(255, 255, 255),
           width=8)
    # small heart in the loop
    d.ellipse([cx - 7, cy - 8, cx + 7, cy + 6], fill=(255, 255, 255))


def icon_ship(d, x, y, s, fg):
    """Ship hull with a small drone above it."""
    # drone: body + 4 rotors
    dx, dy = x + s / 2, y + 22
    d.ellipse([dx - 10, dy - 7, dx + 10, dy + 7], fill=(255, 255, 255))
    for rx, ry in [(-18, -12), (18, -12), (-18, 12), (18, 12)]:
        d.ellipse([dx + rx - 6, dy + ry - 3, dx + rx + 6, dy + ry + 3],
                  outline=(255, 255, 255), width=3)
        d.line([(dx, dy), (dx + rx, dy + ry)], fill=(255, 255, 255), width=2)
    d.line([(dx, dy + 8), (dx, dy + 26)], fill=(255, 255, 255), width=2,
           )
    # hull
    d.polygon([(x + 12, y + 66), (x + s - 12, y + 66), (x + s - 26, y + 92),
               (x + 26, y + 92)], fill=(255, 255, 255))
    d.rectangle([x + 44, y + 44, x + 68, y + 66], fill=(255, 255, 255))
    d.line([(x + 56, y + 44), (x + 56, y + 28)], fill=(255, 255, 255),
           width=4)
    # waves
    d.arc([x + 8, y + 92, x + 40, y + 108], 0, 180, fill=(255, 255, 255),
          width=4)
    d.arc([x + 44, y + 92, x + 76, y + 108], 0, 180, fill=(255, 255, 255),
          width=4)
    d.arc([x + 80, y + 92, x + 112, y + 108], 0, 180, fill=(255, 255, 255),
          width=4)


CARDS = [
    dict(kicker="MARKETS  ·  SEOUL", color=(185, 28, 28), stat="−5%",
         icon=icon_chart,
         headline="KOSPI CRASHES 5%",
         sub="AI sell-off slams Seoul shares; Korea readies a 10-trillion-won "
             "rescue fund as trading halts for a 2nd day."),
    dict(kicker="QUAKE  ·  PACIFIC", color=(14, 116, 144), stat="M6.5",
         icon=icon_quake,
         headline="DEEP QUAKE HITS VANUATU",
         sub="Tremor strikes 601 km down at 02:40 UTC; no damage reported, "
             "no tsunami threat."),
    dict(kicker="CRICKET  ·  WELLINGTON", color=(21, 128, 61), stat="DRAW",
         icon=icon_cricket,
         headline="NZ BAT OUT A DRAW",
         sub="Mitchell & Phillips defy India on day five; record 720/9 "
             "cannot force a win."),
    dict(kicker="DIPLOMACY  ·  DELHI", color=(180, 83, 9), stat="DELHI",
         icon=icon_flags,
         headline="MODI MEETS NEPAL'S BALEN SHAH",
         sub="Ceremonial welcome at Rashtrapati Bhavan; first bilateral "
             "talks on energy & trade."),
    dict(kicker="HEALTH  ·  UK", color=(190, 24, 93), stat="700K",
         icon=icon_ribbon,
         headline="NHS LAUNCHES AI CANCER TRIAL",
         sub="World's largest AI breast-screening trial: 700,000 women at "
             "30 sites over 3 years."),
    dict(kicker="LIBYA  ·  UNITED NATIONS", color=(29, 78, 216), stat="UN",
         icon=icon_ship,
         headline="UN DEMANDS PROBE INTO SHIP STRIKES",
         sub="After sea drones sank a Russian warship off Benghazi; 10 hurt, "
             "no one claims it."),
]


def draw_card(d, x, y, w, h, card):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=(255, 255, 255), outline=RULE, width=2)
    # icon panel on the left
    pw = 150
    d.rounded_rectangle([x, y, x + pw, y + h], radius=10, fill=card["color"])
    d.rectangle([x + pw - 10, y, x + pw, y + h], fill=card["color"])
    d.rectangle([x, y + h - 10, x + pw, y + h], fill=card["color"])
    # big stat centred near the top of the panel (shrink long stats)
    stat_size = 40 if len(card["stat"]) <= 3 else 34 if len(card["stat"]) == 4 else 30
    stat_f = font(SANS_B, stat_size)
    sw = d.textlength(card["stat"], font=stat_f)
    d.text((x + (pw - sw) / 2, y + 16), card["stat"], font=stat_f,
           fill=(255, 255, 255))
    card["icon"](d, x + 15, y + 78, 120, card["color"])
    # text on the right
    tx = x + pw + 16
    tw = w - pw - 32
    kick_f = font(SANS_B, 15)
    d.text((tx, y + 16), card["kicker"], font=kick_f, fill=card["color"])
    head_f = font(SANS_B, 27)
    lines = wrap(d, card["headline"], head_f, tw)
    yy = y + 42
    for ln in lines:
        d.text((tx, yy), ln, font=head_f, fill=INK)
        yy += 32
    sub_f = font(SANS, 17)
    slines = wrap(d, card["sub"], sub_f, tw)
    yy += 6
    for ln in slines:
        d.text((tx, yy), ln, font=sub_f, fill=(60, 60, 60))
        yy += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=(212, 175, 55))
    small_f = font(SANS_B, 22)
    label = "T H E   W O R L D   I N   O N E   D A Y"
    lw = d.textlength(label, font=small_f)
    d.text(((W - lw) / 2, 18), label, font=small_f, fill=(212, 175, 55))
    title_f = font(SERIF_B, 58)
    title = "MONDAY, 23 NOVEMBER 2026"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 52), title, font=title_f, fill=(255, 255, 255))
    strip_f = font(SANS_B, 16)
    strip = "SIX STORIES THAT DEFINED THE DAY"
    sw = d.textlength(strip, font=strip_f)
    d.text(((W - sw) / 2, 118), strip, font=strip_f, fill=(255, 255, 255))
    # ---- grid of six cards ----
    margin, gap = 16, 12
    cw = (W - 2 * margin - gap) // 2
    top = 168
    ch = (H - top - 48 - 2 * gap) // 3
    for i, card in enumerate(CARDS):
        cx = margin + (i % 2) * (cw + gap)
        cy = top + (i // 2) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, card)
    # ---- footer ----
    foot_f = font(SANS, 14)
    foot = ("Sources: Reuters · BBC · USGS · ESPNcricinfo · IANS · Sky News  —  "
            "All six stories first reported Monday 23 November 2026")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, H - 34), foot, font=foot_f, fill=MUTED)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
