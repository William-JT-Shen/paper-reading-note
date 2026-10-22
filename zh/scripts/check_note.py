#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_note.py — 文献阅读笔记自检（结构与质量门）

用法：
    python scripts/check_note.py notes/vaswani2017-attention.md
    python scripts/check_note.py notes/                  # 检查目录下所有笔记
    python scripts/check_note.py notes/ --abstract       # 仅摘要卡（放宽证据下限）
    python scripts/check_note.py notes/ --strict --json

检查项：
  - YAML frontmatter 必填字段与取值（含 authors / keywords）
  - 对应阅读级别（L1/L2/L3）的必填章节
  - 占位符残留（{{...}} / TODO / 待补充 等）
  - 去重后的定位符数量、第 5 节结果数值数量与基线/消融关键词
  - 4.3 公式详解（推导主线/串联 + 含义/符号/思想来源/推导动机 + 表外推导过程）
  - 7.1 作者局限复述 + 7.2 进一步局限
  - L3 第 11 节复现计划中的 Python 代码、第 12 节公式核查
  - 第 0/8/9 节的关键内容

退出码：0 通过；1 检查未通过；2 路径或参数错误（路径不存在等）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 常量

REQUIRED_FM = [
    "paper_id", "title", "authors", "year", "venue", "keywords",
    "reading_level", "status", "created", "updated",
]

SECTIONS = {
    "L1": {0: "速览", 1: "论文信息", 2: "研究背景与问题定义",
           4: "方法", 5: "实验与证据", 7: "批判性评估"},
    "L2": {0: "速览", 1: "论文信息", 2: "研究背景与问题定义", 3: "相关工作与定位",
           4: "方法", 5: "实验与证据", 6: "主要发现", 7: "批判性评估",
           8: "与我的研究的关系", 9: "研究空白与可追问问题"},
    "L3": {0: "速览", 1: "论文信息", 2: "研究背景与问题定义", 3: "相关工作与定位",
           4: "方法", 5: "实验与证据", 6: "主要发现", 7: "批判性评估",
           8: "与我的研究的关系", 9: "研究空白与可追问问题", 10: "关键原文摘录",
           11: "复现计划", 12: "公式与推导核查"},
}

LOCATOR_MIN = {"L1": 3, "L2": 8, "L3": 15}
SECTION5_NUM_MIN = {"L1": 2, "L2": 4, "L3": 6}
ABSTRACT_LOCATOR_MIN = 1
ABSTRACT_SECTION5_NUM_MIN = 1

PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}|\bTODO\b|\bTBD\b|待补充|待填写|\bXXX+\b|\?\?\?")
LOCATOR_RE = re.compile(
    r"\[[^\]\n]*(?:§\s*\d|Sec\.|Section\s*\d|Table\s*\d|Tab\.\s*\d|"
    r"Fig(?:ure)?\.?\s*\d|Eq(?:uation)?\.?\s*\(?\d|pp?\.\s*\d|arXiv[: ]|L\d)[^\]\n]*\]"
)
ABSTRACT_LOC_RE = re.compile(r"\[(?:Abstract|摘要)[^\]]*\]")
RESULT_NUM_RE = re.compile(r"\d+(?:\.\d+)?\s*%|\d+\.\d+")
HEADING_RE = re.compile(r"^##\s+(\d+)\.\s*(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

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


# ---------------------------------------------------------------- 解析

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
            if val in ("|", ">"):  # 块标量：忽略后续缩进行
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
        if num not in sections:  # 保留第一次出现
            sections[num] = body[start:end]
    return sections


def count_locators(text: str, abstract: bool) -> int:
    found = set(LOCATOR_RE.findall(text))
    if abstract:
        found |= set(ABSTRACT_LOC_RE.findall(text))
    return len(found)


def count_result_numbers(text: str) -> int:
    """只数带小数或百分号的“结果型”数值，并去重（避免年份/句对数/词表规模凑数）。"""
    text = re.sub(r"^#+.*$", " ", text, flags=re.MULTILINE)   # 去标题
    text = re.sub(r"\[[^\]]*\]", " ", text)                    # 去定位符/标签
    nums = {m.group(0).strip() for m in RESULT_NUM_RE.finditer(text)}
    return len(nums)


def normalize(text: str) -> str:
    return text.replace("：", ":")


def count_keywords(value: str) -> int:
    value = value.strip().strip("[]")
    return len([x for x in re.split(r"[,，;；]", value) if x.strip()])


# ---------------------------------------------------------------- 检查

def check_file(path: Path, level_override: str | None, strict: bool,
               abstract_flag: bool) -> Report:
    r = Report(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        r.error("FILE", f"文件不存在：{path}")
        return r
    except UnicodeDecodeError:
        r.error("ENC", "文件不是 UTF-8；请先转码再运行")
        return r

    fm, body = split_frontmatter(text)
    r.meta = fm
    if not fm:
        r.error("FM", "缺少 YAML frontmatter（文件应以 --- 开头，包含 paper_id/title 等字段）")

    # --- 是否“仅摘要”模式
    scope = fm.get("source_scope", "").lower()
    r.abstract = abstract_flag or scope in {"abstract", "summary", "仅摘要"}

    # --- frontmatter
    for key in REQUIRED_FM:
        if not fm.get(key):
            r.error("FM", f"缺少必填字段：{key}")
    level = (level_override or fm.get("reading_level", "")).upper()
    if level not in SECTIONS:
        r.error("FM", f"reading_level 必须是 L1/L2/L3，当前为 {fm.get('reading_level')!r}")
        level = "L2"
    elif level_override and fm.get("reading_level") and fm["reading_level"].upper() != level:
        r.warn("FM", f"--level={level} 与 frontmatter 的 {fm['reading_level']} 不一致，按 {level} 检查")
    if r.abstract and level != "L1":
        r.warn("SCOPE", "仅摘要模式通常只用于 L1；完整笔记请用 --abstract 以外的模式")

    for key in ("created", "updated"):
        val = fm.get(key, "")
        if val and not DATE_RE.match(val):
            r.warn("FM", f"{key} 建议用 YYYY-MM-DD，当前为 {val!r}")
    if fm.get("paper_id") and path.stem != fm["paper_id"]:
        r.warn("NAME", f"文件名 {path.stem!r} 与 paper_id {fm['paper_id']!r} 不一致")
    if fm.get("keywords"):
        n_kw = count_keywords(fm["keywords"])
        if not 3 <= n_kw <= 6:
            r.warn("FM", f"keywords 建议 3–6 个，当前 {n_kw} 个")

    # --- 占位符
    placeholders = list(PLACEHOLDER_RE.finditer(text))
    if placeholders:
        samples = []
        for m in placeholders[:5]:
            line_no = text[:m.start()].count("\n") + 1
            samples.append(f"{m.group(0)!r}（第 {line_no} 行）")
        more = f" 等共 {len(placeholders)} 处" if len(placeholders) > 5 else ""
        r.error("PLACEHOLDER", f"残留占位符：{'、'.join(samples)}{more}")

    # --- 章节
    sections = split_sections(body)
    required = SECTIONS[level]
    missing = [f"## {n}. {title}" for n, title in required.items() if n not in sections]
    for item in missing:
        r.error("SECTION", f"缺少必填章节：{item}")
    known = set(range(14))
    extra = sorted(set(sections) - set(required) - known)
    if extra:
        r.warn("SECTION", f"存在未知章节：{extra}（确认不是模板残留）")

    # --- 第 0 节速览
    if 0 in sections:
        s0 = normalize(sections[0])
        for token in ("问题", "做法", "结果"):
            if token not in s0:
                r.error("SUMMARY", f"第 0 节缺少 “{token}”")
        if "为" not in s0 and "重要" not in s0:
            r.warn("SUMMARY", "第 0 节缺少“为什么重要”")

    # --- 领域导读（L2/L3）
    if level in ("L2", "L3") and "导读" not in body and "领域背景" not in body:
        r.warn("SUMMARY", "L2/L3 未见“导读/领域背景”：建议在 §0 前用 2–3 段介绍领域、三层问题与本文位置")

    # --- 读者标记与附录 1
    marks = re.findall(r"\$\^\{?\[(\d+)\]\}?\$", body)
    if marks and "附录 1" not in body and "术语解释" not in body:
        r.warn("STYLE", "正文有 <u>术语</u>$^{[n]}$ 标记，但未见“附录 1：术语解释”")
    elif marks:
        tail = body.split("附录 1", 1)[-1] if "附录 1" in body else body.split("术语解释", 1)[-1]
        missing = sorted({m for m in marks if f"[{m}]" not in tail})
        if missing:
            r.warn("STYLE", "附录 1 缺少标记 " + "、".join(f"[{m}]" for m in missing) + " 的解释")

    # --- 定位符（去重）
    loc = count_locators(body, r.abstract)
    r.stats["locators"] = loc
    loc_min = ABSTRACT_LOCATOR_MIN if r.abstract else LOCATOR_MIN[level]
    if loc < loc_min:
        r.error("EVIDENCE", f"定位符 {loc} 个（去重后），低于下限 {loc_min}"
                            + ("（仅摘要模式）" if r.abstract else f"（{level}）"))

    # --- 第 5 节
    if 5 in sections:
        s5 = sections[5]
        n5 = count_result_numbers(s5)
        r.stats["section5_numbers"] = n5
        num_min = ABSTRACT_SECTION5_NUM_MIN if r.abstract else SECTION5_NUM_MIN[level]
        if n5 < num_min:
            r.error("EVIDENCE", f"第 5 节结果数值 {n5} 个（小数/百分号、去重后），"
                                f"低于下限 {num_min}" + ("（仅摘要模式）" if r.abstract else f"（{level}）"))
        if not r.abstract:
            s5n = normalize(s5)
            if "基线" not in s5n:
                (r.error if level in ("L2", "L3") else r.warn)(
                    "EVIDENCE", "第 5 节缺少基线对比（应出现“基线”及对比数值）")
            if level in ("L2", "L3") and not any(
                    k in s5n for k in ("消融", "对照", "鲁棒", "失败")):
                r.error("EVIDENCE", "第 5 节缺少消融/对照/鲁棒性/失败案例")
    else:
        r.stats["section5_numbers"] = 0

    # --- 第 4.3 节公式详解（L2/L3）
    if level in ("L2", "L3") and 4 in sections:
        s4 = sections[4]
        has_formula = any(k in s4 for k in ("$", "Eq.", "[Eq", "公式"))
        m43 = re.search(r"^###\s*4\.3\s*公式详解", s4, re.M)
        if not has_formula:
            r.warn("METHOD", "第 4 节未见公式；若论文有关键公式，请补 4.3 公式详解")
        elif not m43:
            r.error("METHOD", "第 4 节缺少“### 4.3 公式详解”（逐条解释公式含义与思想来源）")
        else:
            rest = s4[m43.end():]
            nxt = re.search(r"^###\s", rest, re.M)
            detail = rest[:nxt.start()] if nxt else rest
            if ("含义" not in detail or "符号" not in detail
                    or not any(k in detail for k in ("来源", "思想", "动机"))):
                r.error("METHOD", "4.3 公式详解需包含：公式含义、符号定义、思想来源")
            if not re.search(r"^####\s*4\.3\.0", detail, re.M):
                r.error("METHOD", "4.3 缺少“4.3.0 推导主线”小节（先说明公式如何串联）")
            elif not any(k in detail for k in ("推导主线", "公式串联", "公式链")):
                r.error("METHOD", "4.3.0 需写“推导主线/公式串联”（公式之间如何连接）")
            if not any(k in detail for k in ("串联", "链条", "主线")):
                r.error("METHOD", "4.3 推导主线需说明公式之间的串联关系")
            if not any(k in detail for k in ("为什么", "动机")):
                r.error("METHOD", "4.3 需逐式说明“为什么需要这一式”（推导动机）")
            if detail.count("推导动机") < 2:
                r.error("METHOD", "4.3 至少两个公式需写“推导动机”一行")
            if detail.count("与相邻公式") < 2:
                r.error("METHOD", "4.3 至少两个公式需要写明“与相邻公式的关系”")
            if "推导过程" not in detail:
                r.warn("METHOD", "4.3 未见“推导过程”块：若有推导，建议在每个公式表格下方（表格外）补齐")
            for bad in ("这一步的必要性", "不构成循环论证", "值得注意的是", "显而易见"):
                if bad in detail:
                    r.warn("STYLE", f"4.3 推导中出现“{bad}”一类元话语/套话，建议改为论文式陈述")
                    break

    # --- 第 7 节批判
    if 7 in sections:
        s7 = normalize(sections[7])
        if level in ("L2", "L3"):
            if not re.search(r"^###\s*7\.1", s7, re.M):
                r.error("CRITIQUE", "第 7 节缺少 7.1“作者承认的局限（复述）”")
            if not re.search(r"^###\s*7\.2", s7, re.M):
                r.error("CRITIQUE", "第 7 节缺少 7.2“进一步的局限（我补充）”")
            if "作者" not in s7 or "局限" not in s7:
                r.error("CRITIQUE", "第 7 节未复述作者承认的局限")
            if not any(k in s7 for k in ("进一步", "补充")):
                r.error("CRITIQUE", "第 7 节缺少“进一步局限”内容")
            if "优点" not in s7:
                r.warn("CRITIQUE", "第 7 节缺少优点与适用边界")
            if not any(k in s7 for k in ("威胁", "有效性", "可复现")):
                r.warn("CRITIQUE", "第 7 节缺少威胁有效性/可复现性")
        else:
            if not any(k in s7 for k in ("优点", "疑点")):
                r.error("CRITIQUE", "第 7 节缺少优点/疑点快评")
    else:
        r.error("CRITIQUE", "缺少第 7 节批判性评估")

    # --- 第 8/9 节（L2/L3）
    if level in ("L2", "L3"):
        if 8 in sections:
            s8 = normalize(sections[8])
            if not any(k in s8 for k in ("可迁移", "可借鉴")):
                r.error("REFLECTION", "第 8 节缺少“可迁移/可借鉴”内容")
            if "下一步" not in s8:
                r.error("REFLECTION", "第 8 节缺少“下一步”实验")
        if 9 in sections:
            s9 = normalize(sections[9])
            if "空白" not in s9 and "缺口" not in s9:
                r.error("GAP", "第 9 节缺少研究空白/缺口")
            if not any(k in s9 for k in ("下一步", "可验证", "证据")):
                r.warn("GAP", "第 9 节空白条目建议包含证据与可验证的下一步")

    # --- L3：复现计划与公式核查
    if level == "L3":
        s11 = sections.get(11, "")
        if s11:
            if "```python" not in s11.lower():
                r.error("REPRO", "第 11 节复现计划缺少 ```python 代码块")
            elif not re.search(r"\b(import|def)\b", s11):
                r.error("REPRO", "第 11 节 Python 代码缺少 import/def，疑似伪代码")
            if "NotImplementedError" in s11:
                r.error("REPRO", "第 11 节代码仍是模板占位（NotImplementedError），请替换为实际实现")
            if "运行" not in normalize(s11):
                r.warn("REPRO", "第 11 节复现计划缺少运行命令")
            for key in ("验收", "证伪"):
                if key not in normalize(s11):
                    r.warn("REPRO", f"第 11 节复现计划缺少“{key}”")
        s12 = sections.get(12, "")
        if s12 and not any(k in s12 for k in ("公式", "符号", "推导")):
            r.warn("REPRO", "第 12 节建议包含公式/符号/推导核查内容")

    # --- 标签使用
    if "[原文]" not in body:
        r.warn("TAG", "未使用 [原文] 标签；关键事实建议标注来源")
    if not any(tag in body for tag in ("[推断]", "[外部", "[疑问]")):
        r.warn("TAG", "未区分 [推断]/[外部]/[疑问]；请区分证据与判断")

    # --- 公式渲染
    if re.search(r"\\text\{[^}]*[\u4e00-\u9fff][^}]*\}", body):
        r.warn("RENDER", "数学模式内出现中文（\\text{} 含 CJK），KaTeX/MathJax 可能解析失败；请把中文移到公式外")
    if re.search(r"^\$\$.+\$\$$", body, re.M):
        r.warn("RENDER", "存在单行 $$...$$ 行间公式；建议改为多行 $$（$$ 单独占行）")

    return r


# ---------------------------------------------------------------- 路径与输出

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
    scope = "仅摘要" if r.abstract else "全文"
    lines.append(
        f"级别 {r.meta.get('reading_level', '?')} | 范围 {scope}"
        f" | 定位符 {r.stats.get('locators', 0)}"
        f" | 第5节数值 {r.stats.get('section5_numbers', 0)}"
    )
    for e in r.errors:
        lines.append(f"  [错误] {e}")
    for w in r.warnings:
        lines.append(f"  [警告] {w}")
    failed = bool(r.errors) or (strict and bool(r.warnings))
    lines.append(
        f"结果：{'未通过' if failed else '通过'}"
        f"（{len(r.errors)} 个错误，{len(r.warnings)} 个警告）"
    )
    return "\n".join(lines), 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="文献阅读笔记自检")
    parser.add_argument("paths", nargs="+", help="笔记 .md 文件或笔记目录")
    parser.add_argument("--level", choices=["L1", "L2", "L3"], help="覆盖 frontmatter 的阅读级别")
    parser.add_argument("--abstract", action="store_true", help="仅摘要卡模式（放宽定位符/数值下限）")
    parser.add_argument("--strict", action="store_true", help="警告也视为失败")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args(argv)

    files, path_errors = expand_paths(args.paths)
    if not files:
        if path_errors:
            print("路径错误：以下路径不存在：", file=sys.stderr)
            for p in path_errors:
                print(f"  - {p}", file=sys.stderr)
        else:
            print("错误：没有找到可检查的 .md 笔记。", file=sys.stderr)
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
            print(f"[错误] 路径不存在：{p}")

    if path_errors:
        return 2
    return 0 if all(not (r.errors or (args.strict and r.warnings)) for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
