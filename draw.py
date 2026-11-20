#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Every story below was reported on 20 November 2026 (SCMP, BBC, Dawn,
Bangkok Post, Scoop). The program draws the whole image with Pillow:
no photographs, no copied artwork, no network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (15, 42, 74)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
GREY = (90, 88, 82)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_flag(draw, x, y, w, h, kind, label):
    """Tiny schematic flag: USA, China, Russia."""
    if kind == "usa":
        for i in range(7):
            draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                           fill=(178, 34, 34) if i % 2 == 0 else PAPER)
        draw.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=NAVY)
        for r in range(3):
            for c in range(4):
                cx = x + 8 + c * 13
                cy = y + 8 + r * 11
                draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=PAPER)
    elif kind == "china":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + 8, y + 8, x + 24, y + 24], fill=(255, 222, 0))
        for sx, sy in [(34, 12), (40, 22), (36, 34), (26, 38)]:
            draw.ellipse([x + sx, y + sy, x + sx + 7, y + sy + 7],
                         fill=(255, 222, 0))
    else:  # russia
        draw.rectangle([x, y, x + w, y + h / 3], fill=PAPER)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.text((x + w / 2, y + h + 6), label, font=font(SANS_B, 15),
              fill=INK, anchor="mt")


def glyph(draw, kind, x, y, s, color):
    """Small pictogram for a story card, drawn in a s x s box."""
    if kind == "burst":  # explosion / barrage
        cx, cy = x + s // 2, y + s // 2
        for a in range(8):
            import math
            ang = a * math.pi / 4
            x2 = cx + int(math.cos(ang) * s * 0.48)
            y2 = cy + int(math.sin(ang) * s * 0.48)
            draw.line([cx, cy, x2, y2], fill=color, width=4)
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=color)
    elif kind == "tower":  # skyscraper
        draw.polygon([(x + s * 0.35, y + s), (x + s * 0.35, y + s * 0.25),
                      (x + s * 0.5, y), (x + s * 0.65, y + s * 0.25),
                      (x + s * 0.65, y + s)], fill=color)
        for r in range(4):
            for c in range(2):
                draw.rectangle([x + s * 0.40 + c * 9, y + s * 0.30 + r * 14,
                                x + s * 0.40 + c * 9 + 5,
                                y + s * 0.30 + r * 14 + 8], fill=PAPER)
    elif kind == "scales":  # justice
        draw.line([x + s // 2, y + 6, x + s // 2, y + s - 8], fill=color,
                  width=4)
        draw.line([x + 6, y + 14, x + s - 6, y + 14], fill=color, width=4)
        for px in (x + 8, x + s - 8):
            draw.line([px, y + 14, px, y + 30], fill=color, width=3)
            draw.polygon([(px - 12, y + 30), (px + 12, y + 30),
                          (px, y + 44)], outline=color, width=3)
        draw.rectangle([x + s // 2 - 14, y + s - 8, x + s // 2 + 14, y + s],
                       fill=color)
    elif kind == "leaf":  # climate
        draw.ellipse([x + 4, y + 8, x + s - 4, y + s - 6], outline=color,
                     width=4)
        draw.line([x + s // 2, y + s - 6, x + s // 2, y + 12], fill=color,
                  width=4)
        draw.line([x + s // 2, y + s // 2, x + s - 10, y + s // 2 - 8],
                  fill=color, width=3)
    elif kind == "chart":  # markets
        pts = [(x + 4, y + s - 10), (x + s * 0.35, y + s * 0.55),
               (x + s * 0.6, y + s * 0.7), (x + s - 6, y + 8)]
        draw.line(pts, fill=color, width=5, joint="curve")
        draw.polygon([(x + s - 14, y + 4), (x + s - 2, y + 4),
                      (x + s - 8, y + 16)], fill=color)
    elif kind == "palette":  # art
        draw.ellipse([x + 4, y + 6, x + s - 4, y + s - 4], outline=color,
                     width=4)
        for dx, dy in [(14, 16), (30, 10), (16, 32)]:
            draw.ellipse([x + dx, y + dy, x + dx + 8, y + dy + 8],
                         fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -----------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=PAPER, anchor="mt")
    d.line([28, 104, W - 28, 104], fill=GOLD, width=3)
    d.text((W // 2, 114), "FRIDAY  •  20 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
           font=font(SANS_B, 26), fill=GOLD, anchor="mt")

    # ---- Lead story: Shenzhen trilateral ------------------------------
    d.text((28, 168), "SHENZHEN SUMMIT",
           font=font(SANS_B, 20), fill=RED)
    head = "TRUMP, XI AND PUTIN ISSUE\nJOINT PEACE DECLARATION"
    d.multiline_text((28, 196), head, font=font(SERIF_B, 38), fill=INK,
                     spacing=6)
    deck = ("The three leaders release a peace declaration after their "
            "historic trilateral meeting in Shenzhen, China.")
    y = 296
    for line in wrap(d, deck, font(SANS, 20), 620):
        d.text((28, y), line, font=font(SANS, 20), fill=(40, 40, 40))
        y += 27
    # flags strip on the right
    d.rectangle([700, 168, 996, 372], outline=INK, width=2)
    d.text((848, 178), "AT THE TABLE", font=font(SANS_B, 17), fill=GREY,
           anchor="mt")
    fx, fy = 720, 214
    for kind, label in [("usa", "USA"), ("china", "CHINA"),
                        ("russia", "RUSSIA")]:
        draw_flag(d, fx, fy, 80, 52, kind, label)
        fx += 96
    d.text((848, 300), "Kylin Villa, Shenzhen",
           font=font(SANS, 17), fill=GREY, anchor="mt")
    d.text((848, 326), "Declaration follows",
           font=font(SANS, 17), fill=GREY, anchor="mt")

    # ---- Story grid ---------------------------------------------------
    cards = [
        ("UKRAINE", "Russian barrage hits Kyiv embassies and bridges",
         "Daytime strikes damage the Austrian and Dutch missions and a "
         "cathedral; three bridges hit in a major missile attack.",
         (178, 34, 34), "burst"),
        ("MIDDLE EAST", "Houthi missile strikes Riyadh's tallest tower",
         "Windows blown out across eight floors of the landmark \u2014 the "
         "second assault on the financial district this month.",
         (146, 90, 0), "tower"),
        ("JUSTICE", "World Court: Myanmar committed genocide",
         "Judges rule 9\u20136 that Myanmar committed genocide against the "
         "Rohingya in northern Rakhine state.",
         (15, 42, 74), "scales"),
        ("CLIMATE", "Fossil fuels cut from draft climate deal",
         "COP31 near-final text drops the fossil-fuel transition, drawing "
         "outrage from island states and campaigners.",
         (34, 120, 60), "leaf"),
        ("MARKETS", "Anthropic debuts among the world's most valuable firms",
         "The first purely AI company to list publicly, in a stock-market "
         "debut that tests the whole industry.",
         (90, 40, 140), "chart"),
        ("CULTURE", "Van Gogh sells for a record $190.4 million",
         "A Van Gogh painting fetches $190.4m at auction after a dispute "
         "over its sale \u2014 a record price.",
         (150, 60, 110), "palette"),
    ]
    x0, y0, cw, ch, gap = 28, 396, 474, 148, 20
    for i, (kick, headline, deck, color, gk) in enumerate(cards):
        cx = x0 + (i % 2) * (cw + gap)
        cy = y0 + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255),
                    outline=(200, 196, 186), width=1)
        d.rectangle([cx, cy, cx + 8, cy + ch], fill=color)
        d.text((cx + 22, cy + 12), kick, font=font(SANS_B, 17), fill=color)
        glyph(d, gk, cx + cw - 62, cy + 40, 46, color)
        y = cy + 38
        for line in wrap(d, headline, font(SANS_B, 22), cw - 92):
            d.text((cx + 22, y), line, font=font(SANS_B, 22), fill=INK)
            y += 27
        for line in wrap(d, deck, font(SANS, 16), cw - 44):
            d.text((cx + 22, y), line, font=font(SANS, 16), fill=(60, 58, 52))
            y += 21

    # ---- Ticker -------------------------------------------------------
    d.rectangle([0, 898, W, 962], fill=NAVY)
    ticker = ("ALSO TODAY:  Trump pardons Pete Rose  •  "
              "Fiona the hippo dies in Cincinnati  •  "
              "Gas blast kills 6 in Georgia  •  "
              "Malaysia to resettle 10,000 Rohingya")
    y = 910
    for line in wrap(d, ticker, font(SANS_B, 18), W - 56):
        d.text((28, y), line, font=font(SANS_B, 18), fill=PAPER)
        y += 24

    # ---- Footer -------------------------------------------------------
    d.text((W // 2, 976),
           "20 November 2026  •  Drawn by code from the day's reporting",
           font=font(SANS, 15), fill=GREY, anchor="mt")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
