#!/usr/bin/env python3
"""Make the annotated how-to images for the workshop page.

Usage: uv run --no-project --with pillow python -I scripts/make-howto.py <screenshots dir> <out dir>

The screenshots are Tim's (22 Nov 2026, his own Copilot, Excel and Litmaps) and
one Litmaps search taken without a login. They stay out of git. Each image is
cropped so no name or account shows, then gets numbered red markers, frames,
and arrows. Coordinates are in the source image's pixels.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FONT = Path(__file__).resolve().parent.parent / "assets/fonts/work-sans-latin-700-normal.woff2"
RED = (166, 58, 79)
WHITE = (255, 255, 255)


def font(size):
    return ImageFont.truetype(str(FONT), size)


def frame(d, box, w=5, r=12):
    d.rounded_rectangle(box, radius=r, outline=RED, width=w)


def ring(d, xy, r, w=5):
    x, y = xy
    d.ellipse((x - r, y - r, x + r, y + r), outline=RED, width=w)


def arrow(d, start, end, w=6, head=22):
    d.line([start, end], fill=RED, width=w)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(ang - 0.45), end[1] - head * math.sin(ang - 0.45))
    right = (end[0] - head * math.cos(ang + 0.45), end[1] - head * math.sin(ang + 0.45))
    d.polygon([end, left, right], fill=RED)


def label(d, xy, num, text, size=26):
    """A numbered red badge with a red pill of white text to its right, top-left at xy."""
    f = font(size)
    x, y = xy
    h = int(size * 1.7)
    d.ellipse((x, y, x + h, y + h), fill=RED)
    n = str(num)
    nb = d.textbbox((0, 0), n, font=f)
    d.text((x + (h - (nb[2] - nb[0])) / 2 - nb[0], y + (h - (nb[3] - nb[1])) / 2 - nb[1]), n, font=f, fill=WHITE)
    if text:
        tb = d.textbbox((0, 0), text, font=f)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        px = x + h + 8
        d.rounded_rectangle((px, y, px + tw + 2 * int(size * 0.6), y + h), radius=h // 2, fill=RED)
        d.text((px + int(size * 0.6) - tb[0], y + (h - th) / 2 - tb[1]), text, font=f, fill=WHITE)


def save(im, name, width=None):
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(OUT / name, optimize=True)
    print(name, im.size)


def pad(im, top=0, right=0, bottom=0, left=0, color=WHITE):
    out = Image.new("RGB", (im.width + left + right, im.height + top + bottom), color)
    out.paste(im, (left, top))
    return out


# Workflow 1, Copilot: new chat, paste, send. Cropped above the account line at the bottom left.
im = pad(Image.open(SRC / "1.png").convert("RGB").crop((0, 0, 1046, 700)), right=190)
d = ImageDraw.Draw(im)
frame(d, (4, 52, 244, 89))
label(d, (262, 48), 1, "New chat")
frame(d, (272, 324, 1028, 673))
label(d, (290, 262), 2, "Paste the prompt")
ring(d, (992, 636), 30)
label(d, (1040, 614), 3, "Send")
save(im, "copilot-1-paste.png")

# Workflow 1, the answer: the table of works. From Tim's full-length screenshot of the answer.
im = pad(Image.open(SRC / "3.png").convert("RGB").crop((0, 1350, 795, 2090)), top=64, bottom=64)
d = ImageDraw.Draw(im)
frame(d, (556, 64 + 58, 780, 64 + 740), w=4)
label(d, (250, 10), 1, "Search each title in Google Scholar", size=22)
arrow(d, (668, 48), (668, 64 + 66), w=5, head=16)
label(d, (420, 64 + 740 + 12), 2, "Scroll right for more", size=22)
arrow(d, (712, 64 + 740 + 31), (780, 64 + 740 + 31), w=5, head=16)
save(im, "copilot-2-answer.png")

# Workflow 2, Litmaps: search, tick your works (taken without a login; the right panel blanked).
im = pad(Image.open(SRC / "litmaps-1-search.png").convert("RGB"), right=300, color=(243, 245, 247))
d = ImageDraw.Draw(im)
frame(d, (6, 6, 514, 46), w=4)
label(d, (530, 8), 1, "Search by title", size=20)
ring(d, (365, 117), 20, w=4)
ring(d, (365, 241), 20, w=4)
label(d, (530, 160), 2, "Tick your 2 or 3 works", size=20)
arrow(d, (526, 178), (392, 128), w=5, head=16)
arrow(d, (526, 186), (392, 236), w=5, head=16)
save(im, "litmaps-1-search.png")

# Workflow 2, Litmaps: Tim's map. Dark: the works on the map. Blue ring: suggestions.
T = 70
im = pad(Image.open(SRC / "kutnaos.png").convert("RGB"), top=T)
d = ImageDraw.Draw(im)
ring(d, (636, T + 313), 34)
label(d, (360, T + 440), 1, "Your works", size=24)
arrow(d, (470, T + 440), (612, T + 340))
ring(d, (785, T + 201), 30)
label(d, (470, 14), 2, "Suggestions, in the blue ring", size=24)
arrow(d, (790, 56), (786, T + 168))
save(im, "litmaps-2-map.png")

# Workflow 2, Litmaps: click a suggestion, then Add to Litmap. The abstract is blanked.
im = Image.open(SRC / "Pasted 2026-11-22 at 9.08.25.png").convert("RGB")
d = ImageDraw.Draw(im)
d.rectangle((8, 388, 336, 899), fill=WHITE)
im = im.crop((0, 0, 1196, 640))
d = ImageDraw.Draw(im)
ring(d, (1016, 283), 34)
label(d, (760, 470), 1, "Click a suggestion", size=26)
arrow(d, (930, 462), (1000, 314))
frame(d, (84, 278, 206, 308), w=5)
label(d, (30, 430), 2, "Add it to your map", size=26)
arrow(d, (130, 428), (140, 314))
save(im, "litmaps-3-add.png")

# Workflow 4, Excel: the table pasted into A1, every column in its own column (columns A to L).
B = 130
im = pad(Image.open(SRC / "scrren 3.png").convert("RGB").crop((0, 370, 1700, 740)), bottom=B)
d = ImageDraw.Draw(im)
frame(d, (60, 45, 192, 80), w=6)
label(d, (60, 370 + 30), 1, "Click A1, then paste", size=40)
arrow(d, (110, 370 + 26), (120, 88), w=8, head=28)
label(d, (720, 370 + 30), 2, "Every column in its own column", size=40)
arrow(d, (1150, 370 + 26), (1150, 60), w=8, head=28)
save(im, "excel-1-paste.png", width=1400)
