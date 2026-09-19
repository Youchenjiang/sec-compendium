"""
Challenge Sync Exporters & Writers

Provides utility functions for writing normalized challenge datasets to standard
CSV and formatted Markdown catalog files.
"""

import csv
from pathlib import Path
from typing import Any, List, Optional


def write_csv(
    output_path: Path,
    headers: List[str],
    rows: List[List[Any]],
    utf8_sig: bool = True,
) -> None:
    """Write tabular rows to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if utf8_sig else "utf-8"
    with open(output_path, "w", encoding=encoding, newline="") as f:  # skipcq: PTC-W6004
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  [CSV] Saved {len(rows)} entries -> {output_path}")


def write_markdown_file(output_path: Path, content: str) -> None:
    """Write text content to a Markdown file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:  # skipcq: PTC-W6004
        f.write(content)
    print(f"  [Markdown] Saved catalog -> {output_path}")


def format_markdown_table(
    headers: List[str],
    rows: List[List[str]],
    alignments: Optional[List[str]] = None,
) -> str:
    """Format headers and rows as a clean GitHub-flavored Markdown table."""
    if not alignments:
        alignments = [":---" for _ in headers]

    header_line = "| " + " | ".join(headers) + " |"
    align_line = "| " + " | ".join(alignments) + " |"
    row_lines = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]

    return "\n".join([header_line, align_line] + row_lines)
