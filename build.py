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
