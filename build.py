#!/usr/bin/env python3
"""
Build index.html for the Insights LLC website.

    python3 build.py

Reads the words from content.md, drops them into the structure in
_template.html, and writes index.html. Nothing else is touched; the resume
page, the stylesheet and the images are all edited directly.

Needs one small library, installed once:

    pip install markdown          (or: pip3 install markdown)
"""

import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit(
        "This script needs the 'markdown' library.\n"
        "Install it once with:  pip install markdown\n"
        "(on some Macs the command is 'pip3 install markdown')"
    )

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "content.md"
TEMPLATE = HERE / "_template.html"
OUTPUT = HERE / "index.html"

GENERATED_NOTE = (
    "<!--\n"
    "  GENERATED FILE — do not edit.\n"
    "  This page is built from content.md and _template.html by build.py.\n"
    "  Edit content.md and run:  python3 build.py\n"
    "-->\n"
)


def split_front_matter(text):
    """Separate the settings block at the top from the writing below it."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        sys.exit("content.md must start with a line containing only ---")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        sys.exit("content.md is missing the second --- that closes the settings block")
    return lines[1:end], "\n".join(lines[end + 1:])


def parse_settings(lines):
    """Read 'name: value' lines, ignoring blanks and # comments."""
    settings = {}
    for number, line in enumerate(lines, start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            sys.exit(f"content.md line {number}: expected 'name: value', found {stripped!r}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        settings[key] = value
    return settings


def image_size(path):
    """Width and height of a JPEG or PNG, without needing any library.

    The sharing preview declares the size of its picture so that a messaging
    app can lay the card out before the picture has finished downloading.
    """
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        return width, height
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            # The frame headers are the ones carrying the dimensions;
            # everything else is skipped by its stated length.
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                height = int.from_bytes(data[i + 5:i + 7], "big")
                width = int.from_bytes(data[i + 7:i + 9], "big")
                return width, height
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
            else:
                i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
        sys.exit(f"{path.name} looks like a damaged JPEG — its size cannot be read")
    sys.exit(
        f"The preview picture {path.name} must be a .jpg or a .png "
        "(those are the only kinds messaging apps reliably show)."
    )


def preview_addresses(settings):
    """Turn the preview settings into the full web addresses a preview needs."""
    base = settings.get("site_url", "").strip().rstrip("/")
    if not base:
        sys.exit("content.md needs a 'site_url' setting — see README.md")
    if not base.startswith(("http://", "https://")):
        sys.exit(f"content.md: site_url should begin with https:// — found {base!r}")

    picture = settings.get("preview_image", "").strip()
    if not picture:
        sys.exit("content.md needs a 'preview_image' setting — see README.md")

    settings["page_url"] = base + "/"
    settings["preview_image_url"] = f"{base}/{picture.lstrip('/')}"

    # The picture has to be one of the site's own files, so that its size can
    # be measured and declared, and so that it cannot quietly disappear.
    on_disk = HERE / picture
    if not on_disk.exists():
        sys.exit(f"content.md: preview_image points at {picture}, which is not there")
    width, height = image_size(on_disk)
    settings["preview_image_width"] = str(width)
    settings["preview_image_height"] = str(height)
    if (width, height) != (1200, 630):
        print(
            f"note: {picture} is {width}x{height}. Previews look best at "
            "1200x630 — other shapes get cropped, and small ones are ignored."
        )


def slug(heading):
    """'Card one — front'  ->  'card_one_front'"""
    return re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")


def parse_sections(body):
    """Split the writing on its '## ' headings."""
    sections = {}
    current = None
    buffer = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = slug(line[3:])
            buffer = []
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer).strip()
    return sections


def indent(block, spaces):
    pad = " " * spaces
    return "\n".join(pad + line if line else line for line in block.splitlines())


def main():
    if not CONTENT.exists():
        sys.exit(f"Cannot find {CONTENT.name}")
    if not TEMPLATE.exists():
        sys.exit(f"Cannot find {TEMPLATE.name}")

    front_matter, body = split_front_matter(CONTENT.read_text(encoding="utf-8"))
    settings = parse_settings(front_matter)
    preview_addresses(settings)
    sections = parse_sections(body)

    # Short settings are plain text, so anything special in them is escaped.
    values = {key: html.escape(value) for key, value in settings.items()}

    # The longer passages are markdown and become real HTML.
    converter = markdown.Markdown(extensions=["smarty"])
    for key, text in sections.items():
        converter.reset()
        values[key] = converter.convert(text)

    template = TEMPLATE.read_text(encoding="utf-8")
    missing = []

    def fill(match):
        pad = len(match.group(1))
        key = match.group(2)
        if key not in values:
            missing.append(key)
            return match.group(0)
        return indent(values[key], pad) if "\n" in values[key] else " " * pad + values[key]

    page = re.sub(r"( *)\{\{ *([a-z0-9_]+) *\}\}", fill, template)

    unused = set(sections) - set(re.findall(r"\{\{ *([a-z0-9_]+) *\}\}", template))
    for key in sorted(unused):
        print(f"note: the '## {key}' section in content.md is not used by the page")

    if missing:
        sys.exit(
            "content.md is missing:  "
            + ", ".join(sorted(set(missing)))
            + "\nAdd it as a setting at the top, or as a '## ' heading below."
            + ("\n(A heading may have been renamed or mistyped.)" if unused else "")
        )

    # Strip the template's own explanatory comment, then flag the output.
    page = re.sub(r"<!--\n  This is the \*template\*.*?-->\n", "", page, flags=re.S)
    page = page.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + GENERATED_NOTE, 1)

    OUTPUT.write_text(page, encoding="utf-8")
    print(f"Built {OUTPUT.name} from {CONTENT.name} ({len(page):,} characters)")


if __name__ == "__main__":
    main()
