#!/usr/bin/env python3
"""
Draw images/social-card.jpg — the picture that appears when the address of the
site is texted, posted or pasted into a chat.

    python3 tools/make-social-card.py

This script is OPTIONAL. The card it produces is already committed to the
repository, and the preview can be changed without ever running this: put any
picture 1200 x 630 pixels into the images folder and point `preview_image` in
content.md at it. See "The preview card" in README.md.

Run it only to redraw the branded card — after the name changes, say, or to
build the card from a different photograph. Unlike build.py it needs three
libraries that are not otherwise required:

    pip install pillow fonttools brotli

It reads the site's own Lora and Inter fonts out of the fonts folder, and the
site's own colours, so the card looks like the website rather than like a
generic template.
"""

import io
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    from fontTools.ttLib import TTFont
except ImportError:
    sys.exit(
        "This script needs three extra libraries:\n"
        "    pip install pillow fonttools brotli\n"
        "You do not need them for ordinary editing — see the note at the top\n"
        "of this file for how to change the preview picture without them."
    )

HERE = Path(__file__).resolve().parent.parent
FONTS = HERE / "fonts"
IMAGES = HERE / "images"
OUTPUT = IMAGES / "social-card.jpg"

# --- What the card says --------------------------------------------------
# Keep these in step with the top of content.md.
SOURCE_PHOTO = IMAGES / "ocean.jpg"
NAME = "Abby Stamelman Hocky"
TAGLINE = "Leadership & Organizational Consulting  ·  Spiritual Accompaniment"

# --- Colours, taken from css/styles.css ----------------------------------
SAND = (246, 242, 234)
INK = (44, 40, 35)
INK_SOFT = (87, 80, 71)
CLAY = (154, 79, 53)

# --- Proportions ----------------------------------------------------------
# 1200 x 630 is the size every messaging app and social network expects. At
# that shape the picture is shown whole, instead of being cropped to fit.
W, H = 1200, 630
PANEL_TOP = 366          # the sand band starts here; photograph above it
PAD = 64                 # left and right margin inside the sand band
RULE = 3                 # thickness of the clay line under the photograph


def load_font(woff2_name, size):
    """Read one of the site's own web fonts and hand it to Pillow.

    The fonts are stored as .woff2, which is a compressed wrapper that Pillow
    cannot read directly, so it is unwrapped in memory first. Nothing is
    written to the fonts folder.
    """
    path = FONTS / woff2_name
    if not path.exists():
        sys.exit(f"Cannot find {path}")
    font = TTFont(path)
    font.flavor = None
    buffer = io.BytesIO()
    font.save(buffer)
    buffer.seek(0)
    return ImageFont.truetype(buffer, size)


def text_width(draw, text, font, tracking=0):
    width = draw.textlength(text, font=font)
    return width + tracking * max(len(text) - 1, 0)


def draw_tracked(draw, xy, text, font, fill, tracking):
    """Draw text with extra space between the letters, as the site's CSS does."""
    x, y = xy
    for character in text:
        draw.text((x, y), character, font=font, fill=fill)
        x += draw.textlength(character, font=font) + tracking


def panoramic_crop(photo, width, height):
    """Take a strip of the photograph, centred, at exactly the shape wanted."""
    source = Image.open(photo).convert("RGB")
    wanted = width / height
    have = source.width / source.height
    if have > wanted:                      # too wide: trim the sides
        new_width = round(source.height * wanted)
        left = (source.width - new_width) // 2
        source = source.crop((left, 0, left + new_width, source.height))
    else:                                  # too tall: trim top and bottom
        new_height = round(source.width / wanted)
        # Sit a little above centre, which keeps the horizon in the frame.
        top = round((source.height - new_height) * 0.40)
        source = source.crop((0, top, source.width, top + new_height))
    return source.resize((width, height), Image.LANCZOS)


def main():
    card = Image.new("RGB", (W, H), SAND)

    # The photograph, as a panoramic strip across the top.
    card.paste(panoramic_crop(SOURCE_PHOTO, W, PANEL_TOP), (0, 0))

    draw = ImageDraw.Draw(card)
    draw.rectangle([0, PANEL_TOP, W, PANEL_TOP + RULE], fill=CLAY)

    lora_italic = load_font("lora-latin-500-italic.woff2", 46)
    lora = load_font("lora-latin-500-normal.woff2", 62)
    inter_semibold = load_font("inter-latin-600-normal.woff2", 24)
    inter = load_font("inter-latin-400-normal.woff2", 25)

    # The wordmark: italic "Insights" then spaced-out capitals "LLC",
    # the same pairing as the header of the website.
    y = PANEL_TOP + RULE + 32
    draw.text((PAD, y), "Insights", font=lora_italic, fill=INK)
    mark_width = draw.textlength("Insights", font=lora_italic)
    draw_tracked(
        draw,
        (PAD + mark_width + 16, y + 17),
        "LLC",
        inter_semibold,
        INK_SOFT,
        tracking=3.8,
    )

    y += 76
    draw.text((PAD, y), NAME, font=lora, fill=INK)

    y += 82
    draw.text((PAD, y), TAGLINE, font=inter, fill=INK_SOFT)

    # Quality 88 keeps the file well under the size that messaging apps will
    # bother to download, without visible softening.
    card.save(OUTPUT, "JPEG", quality=88, optimize=True, progressive=True)
    size = OUTPUT.stat().st_size
    print(f"Wrote {OUTPUT.relative_to(HERE)}  ({W}x{H}, {size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
