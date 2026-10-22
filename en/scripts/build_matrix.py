#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_matrix.py — Build a comparison matrix from existing reading notes (Markdown / CSV)

Usage:
    python scripts/build_matrix.py notes/
    python scripts/build_matrix.py notes/ -o notes/matrix.md
    python scripts/build_matrix.py notes/ -o notes/matrix.md --csv notes/matrix.csv

Notes:
  - Reads the YAML frontmatter and the section 0 "At a Glance" bullets of each note;
  - Generates automatic columns and leaves manual columns empty
    (Delta / Evidence quality / Reproducibility / Relevance);
  - Links are relative to the output file's directory, so writing the matrix elsewhere does not
    break them;
  - Skips index.md, matrix.md, README.md, synthesis-*.md and template files.
Exit codes: 0 success; 1 no usable notes found; 2 path or argument error.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from datetime import date
from pathlib import Path

HEADING_RE = re.compile(r"^##\s+(\d+)\.\s*(.+?)\s*$", re.MULTILINE)
BULLET_RE = re.compile(
    r"^\s*[-*]\s*\*\*(Problem|Approach|Result|Why it matters)\*\*\s*[：:]\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

MANUAL_COLUMNS = [
    ("delta", "Delta"),
    ("evidence_quality", "Evidence quality"),
    ("reproducibility", "Reproducibility"),
    ("relevance", "Relevance (1–5)"),
]

MARKDOWN_COLUMNS = [
    ("paper_id", "Paper"),
    ("title", "Title"),
    ("year", "Year"),
    ("venue", "Venue"),
    ("problem", "Problem"),
    ("method", "Method"),
    ("result", "Key result"),
    ("reading_level", "Level"),
    ("tags", "Tags"),
    ("file", "Note link"),
] + MANUAL_COLUMNS

CSV_COLUMNS = [
    "paper_id", "title", "year", "venue", "problem", "method",
    "result", "reading_level", "tags", "file",
] + [key for key, _ in MANUAL_COLUMNS]

SKIP_NAMES = {"index.md", "matrix.md", "readme.md", "synthesis.md"}
SKIP_PREFIXES = ("synthesis-", "note-", "speed-card-", "template-")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm: dict[str, str] = {}
    for raw in lines[1:end]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if m:
            val = m.group(2).strip()
            if val in ("|", ">"):
                val = ""
            fm[m.group(1)] = val.strip().strip('"').strip("'")
    return fm, "\n".join(lines[end + 1:])


def section_zero(body: str) -> str:
    matches = list(HEADING_RE.finditer(body))
    for idx, m in enumerate(matches):
        if int(m.group(1)) == 0:
            start = m.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
            return body[start:end]
    return ""


def cleanup(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s*(\[[^\]]*\]\s*)+$", "", text)  # strip trailing locators/tags
    return text.replace("\n", " ").strip()


def parse_note(path: Path) -> dict[str, str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    fm, body = split_frontmatter(text)
    if not fm.get("paper_id") or "{{" in fm.get("paper_id", ""):
        return None
    row: dict[str, str] = {k: fm.get(k, "") for k in
                           ("paper_id", "title", "year", "venue", "reading_level", "tags")}
    bullets = {m.group(1).lower(): cleanup(m.group(2))
               for m in BULLET_RE.finditer(section_zero(body))}
    row["problem"] = bullets.get("problem", "")
    row["method"] = bullets.get("approach", "")
    row["result"] = bullets.get("result", "")
    row["_path"] = str(path.resolve())
    return row


def collect(paths: list[str]) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    missing: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
        else:
            missing.append(path)
    result = []
    for f in files:
        if f.name.lower() in SKIP_NAMES or f.name.startswith(SKIP_PREFIXES):
            continue
        result.append(f)
    return result, missing


def escape_cell(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def sort_key(row: dict[str, str]) -> tuple[int, str]:
    try:
        year = int(re.search(r"\d{4}", row.get("year", "")).group(0))
    except (AttributeError, ValueError):
        year = 9999
    return year, row.get("paper_id", "")


def rel_link(note_path: str, base: Path) -> str:
    try:
        rel = os.path.relpath(note_path, base)
    except ValueError:
        rel = note_path
    return rel.replace("\\", "/")


def render_markdown(rows: list[dict[str, str]], source_dir: Path, base: Path) -> str:
    lines = [
        "# Comparison Matrix (auto-generated)",
        "",
        f"> Generated: {date.today().isoformat()} | Notes: {len(rows)} | Source: `{source_dir}`",
        "> Auto columns: Paper / Title / Year / Venue / Problem / Method / Key result / Level / Tags / Note link.",
        "> Manual columns: Delta (vs. strongest baseline) / Evidence quality / Reproducibility / Relevance — left empty; fill in as needed.",
        "",
        "| " + " | ".join(label for _, label in MARKDOWN_COLUMNS) + " |",
        "|" + "|".join("------" for _ in MARKDOWN_COLUMNS) + "|",
    ]
    for row in rows:
        link = rel_link(row["_path"], base)
        cells = []
        for key, _ in MARKDOWN_COLUMNS:
            if key == "paper_id":
                cells.append(f"[{row['paper_id']}]({link})")
            elif key == "file":
                cells.append(f"[Open]({link})")
            elif key in {k for k, _ in MANUAL_COLUMNS}:
                cells.append("")
            else:
                cells.append(escape_cell(row.get(key, "")) or "—")
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        "## Comparability Notes",
        "",
        "- [ ] Are the metric definitions consistent?",
        "- [ ] Are the datasets/splits consistent?",
        "- [ ] Are the training budgets comparable?",
        "- Non-comparable items:",
        "",
        "## Remarks",
        "",
        "- ",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Build a comparison matrix from reading notes")
    parser.add_argument("paths", nargs="+", help="note directories or files")
    parser.add_argument("-o", "--output", help="Markdown output path (default: print to stdout)")
    parser.add_argument("--csv", help="also write a CSV file to this path")
    args = parser.parse_args(argv)

    files, missing = collect(args.paths)
    if missing:
        print("Path error: the following paths do not exist:", file=sys.stderr)
        for p in missing:
            print(f"  - {p}", file=sys.stderr)
        return 2

    rows = [row for row in (parse_note(f) for f in files) if row]
    if not rows:
        print("Error: no notes with valid frontmatter (paper_id) found.", file=sys.stderr)
        return 1

    rows.sort(key=sort_key)
    first = Path(args.paths[0]).resolve()
    source_dir = first if first.is_dir() else first.parent
    out = Path(args.output) if args.output else None
    base = out.parent.resolve() if out else Path.cwd().resolve()
    markdown = render_markdown(rows, source_dir, base)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"Markdown written: {out} ({len(rows)} notes)")
    else:
        print(markdown)

    if args.csv:
        csv_path = Path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                record = {k: row.get(k, "") for k in CSV_COLUMNS}
                record["file"] = rel_link(row["_path"], base)
                writer.writerow(record)
        print(f"CSV written: {csv_path} ({len(rows)} notes)")

    no_result = [row["paper_id"] for row in rows if not row.get("result")]
    if no_result:
        print(f"Hint: section 0 is missing “Result” in these notes, so the matrix shows —: {', '.join(no_result)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
