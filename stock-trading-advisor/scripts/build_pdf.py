#!/usr/bin/env python3
"""Build a plain but reliable PDF report from markdown/text.

This script avoids external dependencies and creates a readable multi-page PDF
using core PDF objects and Helvetica fonts.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN_LEFT = 42
MARGIN_RIGHT = 42
TOP_Y = 754
BOTTOM_Y = 50
BODY_FONT_SIZE = 10
BODY_LEADING = 15
PARA_GAP_LEADING = 18
LABEL_GAP_LEADING = 14
SECTION_GAP_LEADING = 24

TYPO_REPLACEMENTS = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2212": "-",
    }
)


def _escape_pdf_text(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\t", "    ")
    )


def _normalize_text(line: str) -> str:
    line = line.translate(TYPO_REPLACEMENTS)
    # Convert markdown links to plain readable text.
    line = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", line)
    # Strip basic inline markdown formatting markers.
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
    line = re.sub(r"\*(.*?)\*", r"\1", line)
    line = re.sub(r"`([^`]+)`", r"\1", line)
    return line.strip()


def _wrap_for_width(text: str, font_size: int) -> list[str]:
    usable_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    max_chars = max(24, int(usable_width / (font_size * 0.53)))
    return textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def _append_prefixed(
    specs: list[tuple[str, str, int, int]],
    text: str,
    font: str,
    size: int,
    leading: int,
    first_prefix: str,
    next_prefix: str,
) -> None:
    wrapped = _wrap_for_width(text, size)
    for idx, chunk in enumerate(wrapped):
        prefix = first_prefix if idx == 0 else next_prefix
        specs.append((f"{prefix}{chunk}".rstrip(), font, size, leading))


def _line_specs(text: str, title: str | None) -> list[tuple[str, str, int, int]]:
    """Return tuples of (text, font_key, font_size, leading)."""
    specs: list[tuple[str, str, int, int]] = []
    last_was_blank = False
    indicator_counter = 0

    def add_blank(leading: int = PARA_GAP_LEADING) -> None:
        nonlocal last_was_blank
        if not specs:
            return
        if last_was_blank:
            return
        specs.append(("", "F1", BODY_FONT_SIZE, leading))
        last_was_blank = True

    def add_line(line_text: str, font: str, size: int, leading: int) -> None:
        nonlocal last_was_blank
        specs.append((line_text, font, size, leading))
        last_was_blank = False

    if title:
        specs.append((title.strip(), "F2", 18, 24))
        add_blank(SECTION_GAP_LEADING)

    lines = [ln.rstrip() for ln in text.splitlines()]
    idx = 0
    first_h1_skipped = False

    while idx < len(lines):
        raw = lines[idx]
        line = _normalize_text(raw)

        if not line:
            add_blank(PARA_GAP_LEADING)
            idx += 1
            continue

        if line.startswith("# "):
            content = line[2:].strip()
            # If title already exists and first H1 matches, avoid duplicate title line.
            if title and not first_h1_skipped and content.lower() == title.lower():
                first_h1_skipped = True
                idx += 1
                continue
            first_h1_skipped = True
            add_blank(SECTION_GAP_LEADING)
            for wrapped in _wrap_for_width(content, 16):
                add_line(wrapped, "F2", 16, 22)
            add_blank(PARA_GAP_LEADING)
            idx += 1
            continue

        if line.startswith("## "):
            content = line[3:].strip()
            add_blank(SECTION_GAP_LEADING)
            for wrapped in _wrap_for_width(content, 14):
                add_line(wrapped, "F2", 14, 19)
            add_blank(PARA_GAP_LEADING)
            idx += 1
            continue

        if line.startswith("### "):
            content = line[4:].strip()
            add_blank(LABEL_GAP_LEADING)
            for wrapped in _wrap_for_width(content, 12):
                add_line(wrapped, "F2", 12, 16)
            add_blank(PARA_GAP_LEADING)
            idx += 1
            continue

        # Normalize repeated "Indicator:" labels into numbered cards.
        if line.casefold() == "indicator:":
            indicator_counter += 1
            add_blank(SECTION_GAP_LEADING)

            idx += 1
            while idx < len(lines) and not _normalize_text(lines[idx]):
                idx += 1

            if idx < len(lines):
                candidate = _normalize_text(lines[idx])
                is_label = bool(re.match(r"^[A-Za-z][A-Za-z0-9/&()'., -]{1,80}:\s*$", candidate))
                if candidate and not is_label:
                    for wrapped in _wrap_for_width(f"Indicator {indicator_counter}: {candidate}", 12):
                        add_line(wrapped, "F2", 12, 16)
                    idx += 1
                else:
                    add_line(f"Indicator {indicator_counter}:", "F2", 12, 16)
            else:
                add_line(f"Indicator {indicator_counter}:", "F2", 12, 16)

            add_blank(PARA_GAP_LEADING)
            continue

        # Convert markdown pipe tables into readable indicator-card blocks.
        if line.startswith("|") and line.endswith("|"):
            table_rows: list[list[str]] = []
            while idx < len(lines):
                row_raw = lines[idx].rstrip()
                row_line = _normalize_text(row_raw)
                if not (row_line.startswith("|") and row_line.endswith("|")):
                    break
                cells = [c.strip() for c in row_line.strip("|").split("|")]
                table_rows.append(cells)
                idx += 1

            def is_separator(cells: list[str]) -> bool:
                return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells)

            rows = [r for r in table_rows if r and not is_separator(r)]
            if not rows:
                continue

            headers = rows[0]
            data_rows = rows[1:] if len(rows) > 1 else []

            # If the first row looks like headers, render row cards using header labels.
            header_like = any(h.lower() in {"indicator", "current", "prior", "baseline", "source"} for h in headers)
            if header_like and data_rows:
                for row in data_rows:
                    title = row[0].strip() if row else "Item"
                    indicator_counter += 1
                    add_blank(SECTION_GAP_LEADING)
                    for wrapped in _wrap_for_width(f"Indicator {indicator_counter}: {title}", 11):
                        add_line(wrapped, "F2", 11, 16)
                    for col_idx in range(1, min(len(headers), len(row))):
                        label = headers[col_idx].strip() or f"Field {col_idx}"
                        value = row[col_idx].strip()
                        for wrapped in _wrap_for_width(f"{label}: {value}", BODY_FONT_SIZE):
                            add_line(wrapped, "F1", BODY_FONT_SIZE, BODY_LEADING)
                continue

            # Fallback for non-standard tables: render each row as a compact bullet line.
            for row in rows:
                compact = " | ".join(cell for cell in row if cell)
                if compact:
                    for wrapped in _wrap_for_width(f"- {compact}", BODY_FONT_SIZE):
                        add_line(wrapped, "F1", BODY_FONT_SIZE, BODY_LEADING)
            continue

        # Treat "News N: ..." / "Opportunity N: ..." as section titles with clear gaps.
        if re.match(r"^(news|opportunity)\s+\d+\s*:", line, flags=re.IGNORECASE):
            add_blank(SECTION_GAP_LEADING)
            for wrapped in _wrap_for_width(line, 13):
                add_line(wrapped, "F2", 13, 18)
            add_blank(PARA_GAP_LEADING)
            idx += 1
            continue

        inline_label = re.match(r"^([A-Za-z][A-Za-z0-9/&()'., -]{1,80}):\s+(.+)$", line)
        if inline_label and "://" not in inline_label.group(1):
            label = f"{inline_label.group(1).strip()}:"
            value = inline_label.group(2).strip()
            add_blank(LABEL_GAP_LEADING)
            for wrapped in _wrap_for_width(label, 11):
                add_line(wrapped, "F2", 11, 16)
            for wrapped in _wrap_for_width(value, BODY_FONT_SIZE):
                add_line(wrapped, "F1", BODY_FONT_SIZE, BODY_LEADING)
            idx += 1
            continue

        if re.match(r"^\s*[-*]\s+", raw):
            cleaned = _normalize_text(re.sub(r"^\s*[-*]\s+", "", raw))
            _append_prefixed(specs, cleaned, "F1", BODY_FONT_SIZE, BODY_LEADING, "- ", "  ")
            last_was_blank = False
            idx += 1
            continue

        if re.match(r"^\s*\d+\.\s+", raw):
            m = re.match(r"^\s*(\d+\.)\s+(.*)$", raw)
            if m:
                prefix, cleaned = m.group(1), _normalize_text(m.group(2))
                _append_prefixed(specs, cleaned, "F1", BODY_FONT_SIZE, BODY_LEADING, f"{prefix} ", "   ")
                last_was_blank = False
                idx += 1
                continue

        if re.match(r"^\s*\[\d+\]\s+", raw):
            cleaned = _normalize_text(raw)
            m = re.match(r"^\s*(\[\d+\])\s+(.*)$", cleaned)
            if m:
                ref_num, ref_text = m.group(1), m.group(2)
                _append_prefixed(specs, ref_text, "F1", BODY_FONT_SIZE, BODY_LEADING, f"{ref_num} ", "    ")
                last_was_blank = False
                idx += 1
                continue

        # Label lines get slight emphasis and breathing room.
        if line.endswith(":") and len(line) <= 80:
            add_blank(LABEL_GAP_LEADING)
            for wrapped in _wrap_for_width(line, 11):
                add_line(wrapped, "F2", 11, 16)
            idx += 1
            continue

        # Paragraph mode: merge adjacent plain lines to avoid cramped hard line breaks.
        para_parts = [line]
        idx += 1
        while idx < len(lines):
            candidate_raw = lines[idx]
            candidate = _normalize_text(candidate_raw)
            if not candidate:
                break
            if (
                candidate.startswith("# ")
                or candidate.startswith("## ")
                or candidate.startswith("### ")
                or re.match(r"^\s*[-*]\s+", candidate_raw)
                or re.match(r"^\s*\d+\.\s+", candidate_raw)
                or re.match(r"^\s*\[\d+\]\s+", candidate_raw)
                or candidate.casefold() == "indicator:"
                or (candidate.endswith(":") and len(candidate) <= 90)
                or bool(re.match(r"^[A-Za-z][A-Za-z0-9/&()'., -]{1,80}:\s+.+$", candidate))
            ):
                break
            para_parts.append(candidate)
            idx += 1

        paragraph = " ".join(para_parts).strip()
        for wrapped in _wrap_for_width(paragraph, BODY_FONT_SIZE):
            add_line(wrapped, "F1", BODY_FONT_SIZE, BODY_LEADING)

    return specs


def _paginate(specs: list[tuple[str, str, int, int]]) -> list[list[tuple[str, str, int, int, int]]]:
    """Paginate lines. Output lines per page with concrete y positions."""
    pages: list[list[tuple[str, str, int, int, int]]] = []
    page: list[tuple[str, str, int, int, int]] = []
    y = TOP_Y

    for text, font, size, leading in specs:
        if y - leading < BOTTOM_Y:
            pages.append(page)
            page = []
            y = TOP_Y

        page.append((text, font, size, leading, y))
        y -= leading

    if page:
        pages.append(page)

    if not pages:
        pages.append([(" ", "F1", 11, 14, TOP_Y)])

    return pages


def _stream_for_page(lines: list[tuple[str, str, int, int, int]], page_num: int, page_count: int) -> bytes:
    commands: list[str] = []

    for text, font, size, _leading, y in lines:
        escaped = _escape_pdf_text(text)
        commands.append(f"BT /{font} {size} Tf 1 0 0 1 {MARGIN_LEFT} {y} Tm ({escaped}) Tj ET")

    footer = f"Page {page_num} of {page_count}"
    footer_x = PAGE_WIDTH - MARGIN_RIGHT - 75
    commands.append(f"BT /F1 9 Tf 1 0 0 1 {footer_x} 30 Tm ({_escape_pdf_text(footer)}) Tj ET")
    return ("\n".join(commands) + "\n").encode("latin-1", errors="replace")


def _build_pdf(pages: list[list[tuple[str, str, int, int, int]]]) -> bytes:
    # Object IDs:
    # 1 catalog, 2 pages, 3 font regular, 4 font bold
    # then per page: page object, stream object
    objects: dict[int, bytes] = {}

    page_ids: list[int] = []
    stream_ids: list[int] = []

    next_id = 5
    for _ in pages:
        page_id = next_id
        stream_id = next_id + 1
        page_ids.append(page_id)
        stream_ids.append(stream_id)
        next_id += 2

    # Fonts
    objects[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    objects[4] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"

    # Page streams and page objects
    page_count = len(pages)
    for idx, lines in enumerate(pages):
        page_id = page_ids[idx]
        stream_id = stream_ids[idx]
        stream = _stream_for_page(lines, idx + 1, page_count)
        objects[stream_id] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"endstream"
        )
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] ".encode("ascii")
            + b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            + f"/Contents {stream_id} 0 R >>".encode("ascii")
        )

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"

    max_id = max(objects.keys())
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (max_id + 1)

    for obj_id in range(1, max_id + 1):
        body = objects[obj_id]
        offsets[obj_id] = len(out)
        out.extend(f"{obj_id} 0 obj\n".encode("ascii"))
        out.extend(body)
        out.extend(b"\nendobj\n")

    xref_start = len(out)
    out.extend(f"xref\n0 {max_id + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for obj_id in range(1, max_id + 1):
        out.extend(f"{offsets[obj_id]:010d} 00000 n \n".encode("ascii"))

    out.extend(f"trailer\n<< /Size {max_id + 1} /Root 1 0 R >>\n".encode("ascii"))
    out.extend(f"startxref\n{xref_start}\n%%EOF\n".encode("ascii"))
    return bytes(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render markdown/text into a simple PDF.")
    parser.add_argument("--input", required=True, help="Path to input markdown/text file.")
    parser.add_argument("--output", required=True, help="Path to output PDF file.")
    parser.add_argument("--title", default="", help="Optional title shown at top of PDF.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    specs = _line_specs(text, args.title.strip() or None)
    pages = _paginate(specs)
    pdf_data = _build_pdf(pages)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf_data)

    print(f"Wrote PDF: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
