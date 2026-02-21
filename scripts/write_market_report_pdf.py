#!/usr/bin/env python3
"""Create a simple professional PDF from a markdown/text report without external deps."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import List, Tuple

PAGE_WIDTH = 595.0
PAGE_HEIGHT = 842.0
MARGIN = 44.0
BODY_SIZE = 10.5
BODY_LINE = 15.8
PARA_GAP = 24.0
SPACE_GAP_MEDIUM = 18.0
SPACE_GAP_TIGHT = 13.0
SUBSECTION_PRE_GAP = 12.0
LABEL_POST_GAP = 6.0
SECTION_POST_GAP = 8.0
MAPPING_POST_GAP = 8.0

ASCII_REPLACEMENTS = str.maketrans(
    {
        "‘": "'",
        "’": "'",
        "‚": "'",
        "“": '"',
        "”": '"',
        "„": '"',
        "–": "-",
        "—": "-",
        "―": "-",
        "−": "-",
        "…": "...",
        "→": "->",
        " ": " ",
    }
)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a markdown/text market report to PDF.")
    parser.add_argument("--input", required=True, help="Input markdown or text file")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--title", default="Trading Advisory Report", help="PDF header title")
    parser.add_argument(
        "--cleanup-input",
        action="store_true",
        help="Delete input markdown file after successful PDF write.",
    )
    return parser.parse_args()


def normalize(text: str) -> str:
    text = text.translate(ASCII_REPLACEMENTS)
    text = text.replace("\t", "    ").strip()
    return text.encode("latin-1", "replace").decode("latin-1")


def classify_line(raw: str) -> Tuple[str, float, str]:
    line = raw.rstrip("\n")
    if not line.strip():
        return ("", PARA_GAP, "space")

    stripped = line.lstrip()
    if stripped.startswith("#### "):
        return (normalize(stripped[5:]), 14.0, "h4")
    if stripped.startswith("### "):
        return (normalize(stripped[4:]), 14.0, "h3")
    if stripped.startswith("## "):
        return (normalize(stripped[3:]), 18.0, "h2")
    if stripped.startswith("# "):
        return (normalize(stripped[2:]), 22.0, "h1")
    if re.match(r"^(news|opportunity)\s+\d+\s*:", stripped, flags=re.IGNORECASE):
        return (normalize(stripped), 18.0, "section")
    if stripped.endswith(":") and "://" not in stripped and len(stripped) <= 80:
        return (normalize(stripped), BODY_LINE, "label")
    inline_label = re.match(r"^([A-Za-z][A-Za-z0-9/&()'., %+.-]{1,80}):\s+(.+)$", stripped)
    if inline_label and "://" not in inline_label.group(1):
        return (normalize(stripped), BODY_LINE, "inline_label")
    if stripped in {"Mapping:", "- Mapping:", "* Mapping:"}:
        return (normalize("Mapping:"), BODY_LINE, "mapsec")
    if stripped.startswith(("- ", "* ")):
        return (normalize("- " + stripped[2:]), BODY_LINE, "bullet")
    if stripped.startswith("|") and stripped.endswith("|"):
        return (normalize(stripped), BODY_LINE, "table")
    return (normalize(stripped), BODY_LINE, "body")


def max_chars(font_size: float) -> int:
    usable = PAGE_WIDTH - (2 * MARGIN)
    avg_char_width = max(5.0, font_size * 0.52)
    return max(20, int(usable / avg_char_width))


def break_token(token: str, width: int) -> List[str]:
    if len(token) <= width:
        return [token]
    out: List[str] = []
    remaining = token
    while len(remaining) > width:
        split_points = [
            remaining.rfind("/", 1, width),
            remaining.rfind("-", 1, width),
            remaining.rfind("_", 1, width),
            remaining.rfind("?", 1, width),
            remaining.rfind("&", 1, width),
            remaining.rfind("=", 1, width),
            remaining.rfind(".", 1, width),
        ]
        cut = max(split_points)
        if cut == -1 or cut < (width // 3):
            out.append(remaining[:width])
            remaining = remaining[width:]
            continue
        out.append(remaining[: cut + 1])
        remaining = remaining[cut + 1 :]
    if remaining:
        out.append(remaining)
    return out


def wrap_text(text: str, width: int) -> List[str]:
    if len(text) <= width:
        return [text]

    words: List[str] = []
    for word in text.split():
        words.extend(break_token(word, width))
    if not words:
        return [""]

    out: List[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
            continue
        out.append(current)
        current = word
    out.append(current)
    return out


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def expand_inline_labels(lines: List[Tuple[str, float, str]]) -> List[Tuple[str, float, str]]:
    expanded: List[Tuple[str, float, str]] = []
    for text, lh, kind in lines:
        if kind != "inline_label":
            expanded.append((text, lh, kind))
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9/&()'., %+.-]{1,80}):\s+(.+)$", text)
        if not match:
            expanded.append((text, lh, "body"))
            continue
        label = f"{match.group(1).strip()}:"
        value = match.group(2).strip()
        expanded.append((normalize(label), BODY_LINE, "label"))
        expanded.append((normalize(value), BODY_LINE, "body"))
    return expanded


def style_for_kind(kind: str, lh: float) -> Tuple[str, float, float, float]:
    font = "F1"
    size = BODY_SIZE
    line_gap = lh
    post_gap = 0.0

    if kind == "h1":
        font = "F2"
        size = 14
        line_gap = 20
    elif kind == "h2":
        font = "F2"
        size = 12
        line_gap = 19
    elif kind == "h3":
        font = "F2"
        size = 11.5
        line_gap = 16
    elif kind == "h4":
        font = "F2"
        size = 11
        line_gap = 17
    elif kind == "section":
        font = "F2"
        size = 12
        line_gap = 19
        post_gap = SECTION_POST_GAP
    elif kind == "label":
        font = "F2"
        size = 10.5
        line_gap = 15
        post_gap = LABEL_POST_GAP
    elif kind == "mapsec":
        font = "F2"
        size = 10.5
        line_gap = 15
        post_gap = MAPPING_POST_GAP
    elif kind == "table":
        font = "F1"
        size = 10
        line_gap = 14

    return font, size, line_gap, post_gap


def estimate_line_height(text: str, kind: str, lh: float) -> float:
    _, size, line_gap, post_gap = style_for_kind(kind, lh)
    wrapped = wrap_text(text, max_chars(size))
    return (len(wrapped) * line_gap) + post_gap


def estimate_following_height(
    lines: List[Tuple[str, float, str]],
    start_idx: int,
    max_non_space: int = 1,
) -> float:
    total = 0.0
    seen = 0
    for next_idx in range(start_idx, len(lines)):
        n_text, n_lh, n_kind = lines[next_idx]
        if n_kind == "space":
            continue
        total += estimate_line_height(n_text, n_kind, n_lh)
        seen += 1
        if seen >= max_non_space:
            break
    return total


def next_non_space_kind(lines: List[Tuple[str, float, str]], start_idx: int) -> str | None:
    for idx in range(start_idx, len(lines)):
        _text, _lh, kind = lines[idx]
        if kind != "space":
            return kind
    return None


def space_gap_for_context(prev_kind: str | None, next_kind: str | None) -> float:
    if not prev_kind or not next_kind:
        return PARA_GAP

    if prev_kind in {"label", "mapsec"} and next_kind in {"body", "bullet", "label", "mapsec"}:
        return SPACE_GAP_TIGHT
    if prev_kind in {"body", "bullet", "table"} and next_kind in {"label", "mapsec"}:
        return SPACE_GAP_TIGHT

    if prev_kind in {"section", "h2", "h3", "h4", "mapsec"} or next_kind in {
        "section",
        "h2",
        "h3",
        "h4",
        "mapsec",
    }:
        return SPACE_GAP_MEDIUM

    return PARA_GAP


def build_pages(lines: List[Tuple[str, float, str]], title: str) -> List[str]:
    pages: List[List[str]] = []
    commands: List[str] = []
    y = PAGE_HEIGHT - MARGIN

    def flush_page() -> None:
        nonlocal commands, y
        if not commands:
            return
        pages.append(commands)
        commands = []
        y = PAGE_HEIGHT - MARGIN

    def ensure_space(required_height: float) -> None:
        nonlocal y
        if y - required_height < MARGIN:
            flush_page()

    # Header on first page
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    commands.append(f"BT /F2 14 Tf {MARGIN:.2f} {y:.2f} Td ({escape_pdf_text(normalize(title))}) Tj ET")
    y -= 24
    commands.append(f"BT /F1 9 Tf {MARGIN:.2f} {y:.2f} Td (Generated: {escape_pdf_text(timestamp)}) Tj ET")
    y -= 20

    last_was_space = False
    prev_non_space_kind: str | None = None
    for idx, (text, lh, kind) in enumerate(lines):
        if kind == "space":
            if last_was_space:
                continue
            next_kind = next_non_space_kind(lines, idx + 1)
            gap = space_gap_for_context(prev_non_space_kind, next_kind)
            ensure_space(gap)
            y -= gap
            last_was_space = True
            continue
        last_was_space = False

        font, size, line_gap, post_gap = style_for_kind(kind, lh)

        wrapped = wrap_text(text, max_chars(size))

        # Keep labels/headings with at least one following non-space line to
        # avoid awkward splits across pages (e.g. "Gold Direction:" orphaned).
        keep_next_height = 0.0
        if kind in {"label", "h2", "h3", "h4", "section"}:
            keep_next_height = estimate_following_height(lines, idx + 1, max_non_space=1)

        # Keep "Mapping:" subsection header with at least the next 2 non-space lines.
        if kind == "mapsec":
            keep_next_height = max(keep_next_height, estimate_following_height(lines, idx + 1, max_non_space=2))

        pre_gap = 0.0
        # Render Mapping as a proper subsection break.
        if kind == "mapsec":
            pre_gap = SPACE_GAP_MEDIUM * 1.15
        elif kind in {"h2", "h3", "h4"}:
            pre_gap = SPACE_GAP_MEDIUM * 0.85
        elif kind == "section":
            pre_gap = SPACE_GAP_MEDIUM * 1.1
        elif kind == "label" and prev_non_space_kind in {"body", "bullet", "table"}:
            pre_gap = SUBSECTION_PRE_GAP

        required = pre_gap + (len(wrapped) * line_gap) + post_gap + keep_next_height
        ensure_space(required)

        if pre_gap > 0:
            y -= pre_gap

        for seg in wrapped:
            ensure_space(line_gap)
            safe = escape_pdf_text(seg)
            commands.append(f"BT /{font} {size:.2f} Tf {MARGIN:.2f} {y:.2f} Td ({safe}) Tj ET")
            y -= line_gap
        y -= post_gap
        prev_non_space_kind = kind

    flush_page()
    return ["\n".join(page) + "\n" for page in pages]


def build_pdf(content_streams: List[str]) -> bytes:
    # Object layout:
    # 1 Catalog, 2 Pages, 3 Helvetica, 4 Helvetica-Bold,
    # then pairs of (Page, Content) objects.
    objects: List[bytes] = []

    page_count = len(content_streams)
    first_page_obj = 5

    kids_refs = " ".join(f"{first_page_obj + i * 2} 0 R" for i in range(page_count))
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Count {page_count} /Kids [{kids_refs}] >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    for i, stream in enumerate(content_streams):
        page_obj_id = first_page_obj + (i * 2)
        content_obj_id = page_obj_id + 1
        page_obj = (
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {PAGE_WIDTH:.0f} {PAGE_HEIGHT:.0f}] "
            "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_obj_id} 0 R >>"
        )
        stream_bytes = stream.encode("latin-1", "replace")
        content_obj = b"<< /Length " + str(len(stream_bytes)).encode() + b" >>\nstream\n" + stream_bytes + b"endstream"
        objects.append(page_obj.encode())
        objects.append(content_obj)

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    offsets = [0]
    for obj_index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{obj_index} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())

    pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode())
    pdf.extend(f"startxref\n{xref_start}\n%%EOF\n".encode())
    return bytes(pdf)


def main() -> None:
    args = parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    raw_lines = input_path.read_text(encoding="utf-8").splitlines()

    # Avoid duplicate heading if document first heading matches PDF title.
    content_lines = raw_lines
    for idx, line in enumerate(raw_lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            h1 = stripped[2:].strip()
            if h1.casefold() == args.title.strip().casefold():
                content_lines = raw_lines[idx + 1 :]
        break

    classified = [classify_line(line) for line in content_lines]
    classified = expand_inline_labels(classified)
    pages = build_pages(classified, title=args.title)
    pdf_bytes = build_pdf(pages if pages else [""])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf_bytes)

    if args.cleanup_input:
        try:
            input_path.unlink()
        except FileNotFoundError:
            pass

    print(f"PDF written: {output_path}")


if __name__ == "__main__":
    main()
