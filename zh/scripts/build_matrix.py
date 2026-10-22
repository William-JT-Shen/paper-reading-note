#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_matrix.py — 从已有阅读笔记生成对比矩阵（Markdown / CSV）

用法：
    python scripts/build_matrix.py notes/
    python scripts/build_matrix.py notes/ -o notes/matrix.md
    python scripts/build_matrix.py notes/ -o notes/matrix.md --csv notes/matrix.csv

说明：
  - 读取每篇笔记的 YAML frontmatter 与第 0 节“速览”的条目；
  - 生成自动列，并留出手动列（Delta / Evidence quality / Reproducibility / Relevance）；
  - 链接按“相对输出文件所在目录”计算，输出到别的目录也不会断链；
  - 跳过 index.md、matrix.md、README.md、synthesis-*.md 与模板文件。
退出码：0 成功；1 没有找到可用笔记；2 路径或参数错误。
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
BULLET_RE = re.compile(r"^\s*[-*]\s*\*\*(问题|做法|结果|为什么重要)\*\*\s*[：:]\s*(.+?)\s*$", re.MULTILINE)

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
    text = re.sub(r"\s*(\[[^\]]*\]\s*)+$", "", text)  # 去掉句末定位符/标签
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
    bullets = {m.group(1): cleanup(m.group(2)) for m in BULLET_RE.finditer(section_zero(body))}
    row["problem"] = bullets.get("问题", "")
    row["method"] = bullets.get("做法", "")
    row["result"] = bullets.get("结果", "")
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
        "# 文献对比矩阵（自动生成）",
        "",
        f"> 生成日期：{date.today().isoformat()}　|　笔记数：{len(rows)}　|　来源：`{source_dir}`",
        "> 自动列：Paper / Title / Year / Venue / Problem / Method / Key result / Level / Tags / Note link。",
        "> 手动列：Delta（相对最强基线）/ Evidence quality / Reproducibility / Relevance，已留空，按需填写。",
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
                cells.append(f"[打开]({link})")
            elif key in {k for k, _ in MANUAL_COLUMNS}:
                cells.append("")
            else:
                cells.append(escape_cell(row.get(key, "")) or "—")
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        "## 可比性说明",
        "",
        "- [ ] 指标定义一致？",
        "- [ ] 数据/划分一致？",
        "- [ ] 训练预算可比？",
        "- 不可比项：",
        "",
        "## 备注",
        "",
        "- ",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="从阅读笔记生成对比矩阵")
    parser.add_argument("paths", nargs="+", help="笔记目录或文件")
    parser.add_argument("-o", "--output", help="Markdown 输出路径（默认打印到 stdout）")
    parser.add_argument("--csv", help="同时输出 CSV 路径")
    args = parser.parse_args(argv)

    files, missing = collect(args.paths)
    if missing:
        print("路径错误：以下路径不存在：", file=sys.stderr)
        for p in missing:
            print(f"  - {p}", file=sys.stderr)
        return 2

    rows = [row for row in (parse_note(f) for f in files) if row]
    if not rows:
        print("错误：没有找到含有效 frontmatter（paper_id）的笔记。", file=sys.stderr)
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
        print(f"已写入 Markdown：{out}（{len(rows)} 篇）")
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
        print(f"已写入 CSV：{csv_path}（{len(rows)} 篇）")

    no_result = [row["paper_id"] for row in rows if not row.get("result")]
    if no_result:
        print(f"提示：以下笔记的第 0 节缺少“结果”，矩阵中为 —：{', '.join(no_result)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
