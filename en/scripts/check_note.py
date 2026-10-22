#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_note.py — Self-check for paper reading notes (structure and quality gates)

Usage:
    python scripts/check_note.py notes/vaswani2017-attention.md
    python scripts/check_note.py notes/                  # check every note in a directory
    python scripts/check_note.py notes/ --abstract       # abstract-only card (relaxed evidence floors)
    python scripts/check_note.py notes/ --strict --json

Checks:
  - Required YAML frontmatter fields and values (including authors / keywords)
  - Required sections for the reading level (L1/L2/L3)
  - Leftover placeholders ({{...}} / TODO / "to be filled", etc.)
  - Number of unique locators, number of result values in section 5, baseline/ablation keywords
  - 4.3 Equation Walkthrough (derivation chain + meaning/symbols/intellectual origin/derivation
    motive + derivation process outside the table)
  - 7.1 restatement of the authors' limitations + 7.2 further limitations
  - L3 section 11 reproduction plan code and section 12 formula verification
  - Key content in sections 0/8/9

Exit codes: 0 pass; 1 checks failed; 2 path or argument error (e.g. path not found).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants

REQUIRED_FM = [
    "paper_id", "title", "authors", "year", "venue", "keywords",
    "reading_level", "status", "created", "updated",
]

SECTIONS = {
    "L1": {0: "At a Glance", 1: "Paper Information", 2: "Background and Problem Definition",
           4: "Method", 5: "Experiments and Evidence", 7: "Critical Appraisal"},
    "L2": {0: "At a Glance", 1: "Paper Information", 2: "Background and Problem Definition",
           3: "Related Work and Positioning",
           4: "Method", 5: "Experiments and Evidence", 6: "Main Findings",
           7: "Critical Appraisal", 8: "Relation to My Research",
           9: "Research Gaps and Open Questions"},
    "L3": {0: "At a Glance", 1: "Paper Information", 2: "Background and Problem Definition",
           3: "Related Work and Positioning",
           4: "Method", 5: "Experiments and Evidence", 6: "Main Findings",
           7: "Critical Appraisal", 8: "Relation to My Research",
           9: "Research Gaps and Open Questions", 10: "Key Quotations",
           11: "Reproduction Plan", 12: "Formula and Derivation Verification"},
}

LOCATOR_MIN = {"L1": 3, "L2": 8, "L3": 15}
SECTION5_NUM_MIN = {"L1": 2, "L2": 4, "L3": 6}
ABSTRACT_LOCATOR_MIN = 1
ABSTRACT_SECTION5_NUM_MIN = 1

# {{...}} / TODO / TBD / English "to be filled" variants / Chinese placeholders kept for
# translated notes that still mix languages.
PLACEHOLDER_RE = re.compile(
    r"\{\{[^}]*\}\}|\bTODO\b|\bTBD\b|\bXXX+\b|\?\?\?"
    r"|待补充|待填写|\bto be filled\b|\bto be completed\b|\bto be added\b|\bfill in\b",
    re.IGNORECASE,
)
# Locators: [§4.2], [Sec. 3], [Table 2], [Fig. 3], [Eq. (1)], [p. 4], [arXiv:...], [L3], ...
LOCATOR_RE = re.compile(
    r"\[[^\]\n]*(?:§\s*\d|Sec\.|Section\s*\d|Table\s*\d|Tab\.\s*\d|"
    r"Fig(?:ure)?\.?\s*\d|Eq(?:uation)?\.?\s*\(?\d|pp?\.\s*\d|arXiv[: ]|L\d)[^\]\n]*\]"
)
ABSTRACT_LOC_RE = re.compile(r"\[(?:Abstract)[^\]]*\]", re.IGNORECASE)
RESULT_NUM_RE = re.compile(r"\d+(?:\.\d+)?\s*%|\d+\.\d+")
HEADING_RE = re.compile(r"^##\s+(\d+)\.\s*(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# The field guide is a section before §0; anchoring on the heading avoids a false pass from
# the fixed §2 heading "Background and Problem Definition".
FIELD_GUIDE_RE = re.compile(
    r"^##\s*(?:Guide\b|Field Background\b|Domain Background\b)",
    re.MULTILINE | re.IGNORECASE,
)

# Meta-language/filler that should be rewritten as a paper-style statement.
BAD_META_PHRASES = (
    "this step is necessary",
    "not circular",
    "it is worth noting",
    "worth noting",
    "obviously",
    "needless to say",
    "as we all know",
)

SKIP_NAMES = {"index.md", "matrix.md", "readme.md", "synthesis.md"}
SKIP_PREFIXES = ("synthesis-", "note-", "speed-card-", "template-")


class Report:
    def __init__(self, path: Path):
        self.path = path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.meta: dict[str, str] = {}
        self.stats: dict[str, int] = {}
        self.abstract = False

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"[{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"[{code}] {msg}")


# ---------------------------------------------------------------- parsing

def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if len(lines) < 2 or lines[0].strip() != "---":
        return {}, text
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
            key, val = m.group(1), m.group(2).strip()
            if val in ("|", ">"):  # block scalar: ignore the following indented lines
                val = ""
            fm[key] = val.strip().strip('"').strip("'")
    return fm, "\n".join(lines[end + 1:])


def split_sections(body: str) -> dict[int, str]:
    matches = list(HEADING_RE.finditer(body))
    sections: dict[int, str] = {}
    for idx, m in enumerate(matches):
        num = int(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        if num not in sections:  # keep the first occurrence
            sections[num] = body[start:end]
    return sections


def count_locators(text: str, abstract: bool) -> int:
    found = set(LOCATOR_RE.findall(text))
    if abstract:
        found |= set(ABSTRACT_LOC_RE.findall(text))
    return len(found)


def count_result_numbers(text: str) -> int:
    """Count only "result-like" values with a decimal point or percent sign, deduplicated
    (so years, token counts and vocabulary sizes cannot pad the total)."""
    text = re.sub(r"^#+.*$", " ", text, flags=re.MULTILINE)   # drop headings
    text = re.sub(r"\[[^\]]*\]", " ", text)                    # drop locators/tags
    nums = {m.group(0).strip() for m in RESULT_NUM_RE.finditer(text)}
    return len(nums)


def normalize(text: str) -> str:
    # Lowercase so keyword checks are case-insensitive; normalize the full-width colon too.
    return text.replace("：", ":").lower()


def count_keywords(value: str) -> int:
    value = value.strip().strip("[]")
    return len([x for x in re.split(r"[,，;；]", value) if x.strip()])


# ---------------------------------------------------------------- checks

def check_file(path: Path, level_override: str | None, strict: bool,
               abstract_flag: bool) -> Report:
    r = Report(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        r.error("FILE", f"File not found: {path}")
        return r
    except UnicodeDecodeError:
        r.error("ENC", "File is not UTF-8; convert it before running the checker")
        return r

    fm, body = split_frontmatter(text)
    r.meta = fm
    if not fm:
        r.error("FM", "Missing YAML frontmatter (the file should start with --- and contain paper_id/title, etc.)")

    # --- "abstract only" mode
    scope = fm.get("source_scope", "").lower()
    r.abstract = abstract_flag or scope in {"abstract", "summary", "abstract-only"}

    # --- frontmatter
    for key in REQUIRED_FM:
        if not fm.get(key):
            r.error("FM", f"Missing required field: {key}")
    level = (level_override or fm.get("reading_level", "")).upper()
    if level not in SECTIONS:
        r.error("FM", f"reading_level must be L1/L2/L3, got {fm.get('reading_level')!r}")
        level = "L2"
    elif level_override and fm.get("reading_level") and fm["reading_level"].upper() != level:
        r.warn("FM", f"--level={level} differs from frontmatter {fm['reading_level']}; checking as {level}")
    if r.abstract and level != "L1":
        r.warn("SCOPE", "Abstract-only mode is normally used for L1; use a mode other than --abstract for full notes")

    for key in ("created", "updated"):
        val = fm.get(key, "")
        if val and not DATE_RE.match(val):
            r.warn("FM", f"{key} should be YYYY-MM-DD, got {val!r}")
    if fm.get("paper_id") and path.stem != fm["paper_id"]:
        r.warn("NAME", f"File name {path.stem!r} does not match paper_id {fm['paper_id']!r}")
    if fm.get("keywords"):
        n_kw = count_keywords(fm["keywords"])
        if not 3 <= n_kw <= 6:
            r.warn("FM", f"keywords should have 3–6 entries, got {n_kw}")

    # --- placeholders
    placeholders = list(PLACEHOLDER_RE.finditer(text))
    if placeholders:
        samples = []
        for m in placeholders[:5]:
            line_no = text[:m.start()].count("\n") + 1
            samples.append(f"{m.group(0)!r} (line {line_no})")
        more = f" ({len(placeholders)} total)" if len(placeholders) > 5 else ""
        r.error("PLACEHOLDER", f"Leftover placeholders: {', '.join(samples)}{more}")

    # --- sections
    sections = split_sections(body)
    required = SECTIONS[level]
    missing = [f"## {n}. {title}" for n, title in required.items() if n not in sections]
    for item in missing:
        r.error("SECTION", f"Missing required section: {item}")
    known = set(range(14))
    extra = sorted(set(sections) - set(required) - known)
    if extra:
        r.warn("SECTION", f"Unknown section(s): {extra} (make sure this is not template residue)")

    # --- section 0 at a glance
    if 0 in sections:
        s0 = normalize(sections[0])
        for token in ("problem", "approach", "result"):
            if token not in s0:
                r.error("SUMMARY", f"Section 0 is missing “{token}”")
        if "why" not in s0 and "important" not in s0:
            r.warn("SUMMARY", "Section 0 is missing a “why it matters” statement")

    # --- field guide (L2/L3)
    body_l = body.lower()
    if level in ("L2", "L3") and not FIELD_GUIDE_RE.search(body):
        r.warn("SUMMARY", "No field guide found for L2/L3: add 2–3 paragraphs before §0 "
                          "introducing the field, its three-level problems, and where this paper sits")

    # --- terminology marks and Appendix 1
    marks = re.findall(r"\$\^\{?\[(\d+)\]\}?\$", body)
    has_appendix = "appendix 1" in body_l or "terminology" in body_l
    if marks and not has_appendix:
        r.warn("STYLE", "Body has <u>term</u>$^{[n]}$ marks but no “Appendix 1: Terminology”")
    elif marks:
        tail = body_l.split("appendix 1", 1)[-1] if "appendix 1" in body_l else body_l.split("terminology", 1)[-1]
        missing = sorted({m for m in marks if f"[{m}]" not in tail})
        if missing:
            r.warn("STYLE", "Appendix 1 is missing explanations for marks " + ", ".join(f"[{m}]" for m in missing))

    # --- locators (deduplicated)
    loc = count_locators(body, r.abstract)
    r.stats["locators"] = loc
    loc_min = ABSTRACT_LOCATOR_MIN if r.abstract else LOCATOR_MIN[level]
    if loc < loc_min:
        r.error("EVIDENCE", f"Locators: {loc} (deduplicated), below the minimum {loc_min}"
                            + (" (abstract-only mode)" if r.abstract else f" ({level})"))

    # --- section 5
    if 5 in sections:
        s5 = sections[5]
        n5 = count_result_numbers(s5)
        r.stats["section5_numbers"] = n5
        num_min = ABSTRACT_SECTION5_NUM_MIN if r.abstract else SECTION5_NUM_MIN[level]
        if n5 < num_min:
            r.error("EVIDENCE", f"Section 5 result values: {n5} (decimals/percent, deduplicated), "
                                f"below the minimum {num_min}" + (" (abstract-only mode)" if r.abstract else f" ({level})"))
        if not r.abstract:
            s5n = normalize(s5)
            if "baseline" not in s5n:
                (r.error if level in ("L2", "L3") else r.warn)(
                    "EVIDENCE", "Section 5 is missing a baseline comparison (should mention “baseline” and comparative numbers)")
            if level in ("L2", "L3") and not any(
                    k in s5n for k in ("ablation", "control", "robust", "failure")):
                r.error("EVIDENCE", "Section 5 is missing ablation/control/robustness/failure cases")
    else:
        r.stats["section5_numbers"] = 0

    # --- 4.3 Equation Walkthrough (L2/L3)
    if level in ("L2", "L3") and 4 in sections:
        s4 = sections[4]
        s4_l = s4.lower()
        has_formula = any(k in s4_l for k in ("$", "eq.", "[eq", "formula", "equation"))
        m43 = re.search(r"^###\s*4\.3\s*Equation Walkthrough", s4, re.M)
        if not has_formula:
            r.warn("METHOD", "No formulas found in Section 4; if the paper has key equations, add 4.3 Equation Walkthrough")
        elif not m43:
            r.error("METHOD", "Section 4 is missing “### 4.3 Equation Walkthrough” (explain each equation's meaning and intellectual origin)")
        else:
            rest = s4[m43.end():]
            nxt = re.search(r"^###\s", rest, re.M)
            detail = rest[:nxt.start()] if nxt else rest
            detail_l = detail.lower()
            if ("meaning" not in detail_l or "symbol" not in detail_l
                    or not any(k in detail_l for k in ("origin", "motive", "rationale"))):
                r.error("METHOD", "4.3 Equation Walkthrough must include: equation meaning, symbol definitions, intellectual origin")
            if not re.search(r"^####\s*4\.3\.0", detail, re.M):
                r.error("METHOD", "4.3 is missing the “4.3.0 Derivation Chain” subsection (explain first how the equations connect)")
            elif not any(k in detail_l for k in ("derivation chain", "formula chain", "equation chain")):
                r.error("METHOD", "4.3.0 must state the “derivation chain / formula chain” (how the equations connect)")
            if not any(k in detail_l for k in ("chain", "connect", "link")):
                r.error("METHOD", "4.3 must explain how the equations connect to each other")
            if not any(k in detail_l for k in ("why", "motive", "rationale")):
                r.error("METHOD", "4.3 must explain, equation by equation, “why this equation is needed” (derivation motive)")
            if detail_l.count("derivation motive") < 2:
                r.error("METHOD", "4.3 needs a “Derivation motive” line for at least two equations")
            if detail_l.count("relation to adjacent") < 2:
                r.error("METHOD", "4.3 needs a “Relation to adjacent equations” line for at least two equations")
            if "derivation process" not in detail_l:
                r.warn("METHOD", "4.3 has no “Derivation process” block: if there is a derivation, add it below each equation table (outside the table)")
            for bad in BAD_META_PHRASES:
                if bad in detail_l:
                    r.warn("STYLE", f"4.3 contains meta-language/filler such as “{bad}”; rewrite it as a paper-style statement")
                    break

    # --- section 7 critical appraisal
    if 7 in sections:
        s7 = normalize(sections[7])
        if level in ("L2", "L3"):
            if not re.search(r"^###\s*7\.1", s7, re.M):
                r.error("CRITIQUE", "Section 7 is missing 7.1 “Limitations Acknowledged by the Authors” (restatement)")
            if not re.search(r"^###\s*7\.2", s7, re.M):
                r.error("CRITIQUE", "Section 7 is missing 7.2 “Further Limitations (My Additions)”")
            if "author" not in s7 or "limitation" not in s7:
                r.error("CRITIQUE", "Section 7 does not restate the limitations acknowledged by the authors")
            if not any(k in s7 for k in ("further", "addition")):
                r.error("CRITIQUE", "Section 7 is missing “further limitations”")
            if "strength" not in s7:
                r.warn("CRITIQUE", "Section 7 is missing strengths and scope")
            if not any(k in s7 for k in ("threat", "validity", "reproducib")):
                r.warn("CRITIQUE", "Section 7 is missing threats to validity/reproducibility")
        else:
            if not any(k in s7 for k in ("strength", "concern", "doubt")):
                r.error("CRITIQUE", "Section 7 is missing the strengths/concerns quick review")
    else:
        r.error("CRITIQUE", "Section 7 (Critical Appraisal) is missing")

    # --- sections 8/9 (L2/L3)
    if level in ("L2", "L3"):
        if 8 in sections:
            s8 = normalize(sections[8])
            if "transferable" not in s8:
                r.error("REFLECTION", "Section 8 is missing transferable/applicable content")
            if "next step" not in s8:
                r.error("REFLECTION", "Section 8 is missing next-step experiments")
        if 9 in sections:
            s9 = normalize(sections[9])
            if "gap" not in s9:
                r.error("GAP", "Section 9 is missing the research gap")
            if not any(k in s9 for k in ("next step", "verifiable", "evidence")):
                r.warn("GAP", "Section 9 gap entries should include evidence and a verifiable next step")

    # --- L3: reproduction plan and formula verification
    if level == "L3":
        s11 = sections.get(11, "")
        if s11:
            s11_l = s11.lower()
            if "```python" not in s11_l:
                r.error("REPRO", "Section 11 reproduction plan is missing a ```python code block")
            elif not re.search(r"\b(import|def)\b", s11):
                r.error("REPRO", "Section 11 Python code has no import/def; it looks like pseudocode")
            if "NotImplementedError" in s11:
                r.error("REPRO", "Section 11 code is still the template placeholder (NotImplementedError); replace it with a real implementation")
            s11n = normalize(s11)
            if "run" not in s11n:
                r.warn("REPRO", "Section 11 reproduction plan is missing run commands")
            for key in ("acceptance", "falsification"):
                if key not in s11n:
                    r.warn("REPRO", f"Section 11 reproduction plan is missing “{key}”")
        s12 = sections.get(12, "")
        if s12 and not any(k in s12.lower() for k in ("formula", "symbol", "derivation")):
            r.warn("REPRO", "Section 12 should cover formula/symbol/derivation verification")

    # --- tag usage
    if "[original]" not in body_l:
        r.warn("TAG", "No [Original] tags found; key facts should cite their source")
    if not any(tag in body_l for tag in ("[inference]", "[external", "[question]")):
        r.warn("TAG", "Tags do not distinguish [Inference]/[External]/[Question]; separate evidence from judgment")

    # --- formula rendering
    if re.search(r"\\text\{[^}]*[\u4e00-\u9fff][^}]*\}", body):
        r.warn("RENDER", "CJK text appears inside math mode (\\text{} contains CJK); KaTeX/MathJax may fail to render; move the Chinese text outside the formula")
    if re.search(r"^\$\$.+\$\$$", body, re.M):
        r.warn("RENDER", "A single-line $$...$$ display formula was found; prefer multi-line $$ (opening and closing on their own lines)")

    return r


# ---------------------------------------------------------------- paths and output

def expand_paths(paths: list[str]) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    path_errors: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.rglob("*.md")):
                if f.name.lower() in SKIP_NAMES or f.name.startswith(SKIP_PREFIXES):
                    continue
                files.append(f)
        elif path.is_file():
            files.append(path)
        else:
            path_errors.append(path)
    return files, path_errors


def render(r: Report, strict: bool) -> tuple[str, int]:
    lines = [f"== check_note: {r.path} =="]
    scope = "abstract only" if r.abstract else "full text"
    lines.append(
        f"Level {r.meta.get('reading_level', '?')} | Scope {scope}"
        f" | Locators {r.stats.get('locators', 0)}"
        f" | Section 5 numbers {r.stats.get('section5_numbers', 0)}"
    )
    for e in r.errors:
        lines.append(f"  [ERROR] {e}")
    for w in r.warnings:
        lines.append(f"  [WARN] {w}")
    failed = bool(r.errors) or (strict and bool(r.warnings))
    lines.append(
        f"Result: {'FAIL' if failed else 'PASS'}"
        f" ({len(r.errors)} errors, {len(r.warnings)} warnings)"
    )
    return "\n".join(lines), 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Self-check for paper reading notes")
    parser.add_argument("paths", nargs="+", help="note .md files or note directories")
    parser.add_argument("--level", choices=["L1", "L2", "L3"], help="override the reading level from frontmatter")
    parser.add_argument("--abstract", action="store_true", help="abstract-only card mode (relaxed locator/number floors)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    files, path_errors = expand_paths(args.paths)
    if not files:
        if path_errors:
            print("Path error: the following paths do not exist:", file=sys.stderr)
            for p in path_errors:
                print(f"  - {p}", file=sys.stderr)
        else:
            print("Error: no .md notes found to check.", file=sys.stderr)
        return 2

    reports = [check_file(f, args.level, args.strict, args.abstract) for f in files]

    if args.json:
        payload = {
            "files": [
                {
                    "file": str(r.path),
                    "meta": r.meta,
                    "abstract": r.abstract,
                    "stats": r.stats,
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "passed": not r.errors and not (args.strict and r.warnings),
                }
                for r in reports
            ],
            "path_errors": [str(p) for p in path_errors],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            text, _ = render(r, args.strict)
            print(text)
        for p in path_errors:
            print(f"[ERROR] Path does not exist: {p}")

    if path_errors:
        return 2
    return 0 if all(not (r.errors or (args.strict and r.warnings)) for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
