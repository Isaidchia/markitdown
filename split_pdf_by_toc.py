from __future__ import annotations

import argparse
import csv
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from docling.document_converter import DocumentConverter
from pypdf import PdfReader, PdfWriter


@dataclass(frozen=True)
class TocEntry:
    """Represents a row from the CSV table of contents."""

    index: str
    title: str
    page_start: int
    page_end: int


@dataclass(frozen=True)
class UnitRange:
    """Holds the resolved page range for a top-level unit."""

    index: str
    title: str
    page_start: int
    page_end: int


def parse_top_level_entries(csv_path: Path) -> list[TocEntry]:
    """Parse the CSV and return ordered top-level TOC entries."""

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required_headers = {"index", "title", "page_start", "page_end"}
        if reader.fieldnames is None:
            raise ValueError(f"CSV file {csv_path} has no header row")
        missing = required_headers.difference({header.strip() for header in reader.fieldnames})
        if missing:
            missing_headers = ", ".join(sorted(missing))
            raise ValueError(f"CSV missing required headers: {missing_headers}")

        entries: list[TocEntry] = []
        for row in reader:
            # Normalize row keys by stripping whitespace to handle CSV headers with spaces
            normalized_row = {key.strip(): value for key, value in row.items()}
            
            raw_index = (normalized_row.get("index") or "").strip()
            if not raw_index or "." in raw_index:
                continue
            title = (normalized_row.get("title") or "").strip()
            if not title:
                title = f"Unit {raw_index}"
            try:
                page_start = int((normalized_row.get("page_start") or "").strip())
                page_end = int((normalized_row.get("page_end") or "").strip())
            except ValueError as exc:
                raise ValueError(f"Invalid page_start or page_end for index {raw_index}") from exc

            entries.append(TocEntry(index=raw_index, title=title, page_start=page_start, page_end=page_end))

    if not entries:
        raise ValueError(f"No top-level entries found in {csv_path}")

    entries.sort(key=lambda entry: entry.page_start)
    return entries


def determine_unit_ranges(entries: Sequence[TocEntry], total_pages: int) -> list[UnitRange]:
    """Calculate inclusive page ranges for each top-level unit."""

    unit_ranges: list[UnitRange] = []
    for position, entry in enumerate(entries):
        # Check if there's a next entry
        if position + 1 < len(entries):
            next_start = entries[position + 1].page_start
            # If next entry starts on same page or earlier, use CSV's page_end
            # Otherwise, use next_start - 1
            if next_start <= entry.page_start:
                end_page = min(entry.page_end, total_pages)
            else:
                end_page = min(next_start - 1, total_pages)
        else:
            # Last entry: use CSV's page_end or total_pages, whichever is smaller
            end_page = min(entry.page_end, total_pages)
        
        if entry.page_start < 1 or entry.page_start > total_pages:
            raise ValueError(
                f"Entry {entry.index} starts on page {entry.page_start}, but PDF has {total_pages} pages"
            )
        if end_page < entry.page_start:
            raise ValueError(f"Computed negative range for entry {entry.index}")
        unit_ranges.append(
            UnitRange(
                index=entry.index,
                title=entry.title,
                page_start=entry.page_start,
                page_end=end_page,
            )
        )
    return unit_ranges


def sanitize_title(title: str) -> str:
    """Return a filesystem-friendly slug for the title."""

    slug = re.sub(r"[^A-Za-z0-9]+", "_", title.strip())
    slug = slug.strip("_")
    if not slug:
        slug = "unit"
    return slug[:80]


def build_pdf_writer(reader: PdfReader, start_page: int, end_page: int) -> PdfWriter:
    """Extract a page range from the reader into a new PdfWriter."""

    writer = PdfWriter()
    start_index = start_page - 1
    end_index = end_page - 1
    if start_index < 0 or end_index >= len(reader.pages):
        raise ValueError(f"Requested pages {start_page}-{end_page} are outside PDF bounds")

    for page_number in range(start_index, end_index + 1):
        writer.add_page(reader.pages[page_number])
    return writer


def convert_writer_to_markdown(writer: PdfWriter, converter: DocumentConverter) -> str:
    """Write the PdfWriter to a temporary file and convert it to markdown."""

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        writer.write(temp_pdf)
        temp_path = Path(temp_pdf.name)

    try:
        result = converter.convert(str(temp_path))
        markdown = result.document.export_to_markdown()
    finally:
        temp_path.unlink(missing_ok=True)
    return markdown


def write_markdown_file(output_dir: Path, filename: str, content: str) -> Path:
    """Persist markdown content to disk within the output directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(content)
    return output_path


def split_pdf_to_markdown(
    pdf_path: Path,
    csv_path: Path,
    output_dir: Path,
) -> list[Path]:
    """Split a PDF by top-level units and export markdown files."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    entries = parse_top_level_entries(csv_path)
    unit_ranges = determine_unit_ranges(entries, len(reader.pages))

    converter = DocumentConverter()
    written_files: list[Path] = []

    for unit in unit_ranges:
        writer = build_pdf_writer(reader, unit.page_start, unit.page_end)
        markdown = convert_writer_to_markdown(writer, converter)
        filename = f"{unit.index}_{sanitize_title(unit.title)}.md"
        output_path = write_markdown_file(output_dir, filename, markdown)
        written_files.append(output_path)

    return written_files


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Split a PDF into markdown files using a CSV table of contents."
    )
    parser.add_argument("pdf", type=Path, help="Path to the source PDF file")
    parser.add_argument("csv", type=Path, help="Path to the CSV table of contents")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Directory to store markdown files (default: ./output)",
    )
    return parser.parse_args(args)


def main(argv: Iterable[str] | None = None) -> None:
    """Entrypoint for CLI execution."""

    arguments = parse_args(argv)
    written_paths = split_pdf_to_markdown(arguments.pdf, arguments.csv, arguments.output)
    print(f"Wrote {len(written_paths)} markdown files to {arguments.output}")


if __name__ == "__main__":
    main()

