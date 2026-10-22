#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate diagrams for the paper-reading-note README and WeChat article.

Usage: python docs/make_figures.py
Outputs: docs/images/{workflow,architecture,formula-chain,quality-gate,bad-vs-good,cover}-{zh,en}.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#F7F4EE"
INK = "#1D2B2A"
MUTED = "#637674"
TEAL = "#2A9D8F"
TEAL_L = "#DCEFE9"
ORANGE = "#E76F51"
ORANGE_L = "#FBE3DB"
YELLOW = "#E9C46A"
YELLOW_L = "#FBF1D4"
LINE = "#C8D6D2"
WHITE = "#FFFFFF"
RED = "#C44536"
RED_L = "#F8E1DC"
GREEN = "#2F7D5A"
GREEN_L = "#DFF0E7"


def canvas(w: float, h: float):
    fig = plt.figure(figsize=(w / 12, h / 12), dpi=200, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def rounded(ax, x, y, w, h, fill=WHITE, edge=LINE, lw=1.2, radius=2.0, alpha=1.0):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill, alpha=alpha,
        zorder=2,
    )
    ax.add_patch(patch)
    return patch


def text(ax, x, y, s, size=10, color=INK, weight="normal", ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=5, **kw)


def wrap_display(s: str, width: int) -> str:
    """Wrap mixed CJK/Latin text: width is counted in CJK-character units."""
    lines, cur, used = [], "", 0
    for ch in s:
        if ch == "\n":
            lines.append(cur)
            cur, used = "", 0
            continue
        w = 2 if ord(ch) > 127 else 1
        if used + w > width * 2 and cur:
            lines.append(cur)
            cur, used = "", 0
        cur += ch
        used += w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def arrow(ax, x1, y1, x2, y2, color=TEAL, lw=1.4, rad=0.0, ms=11):
    p = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle="-|>", mutation_scale=ms,
                        linewidth=lw, color=color, zorder=3,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(p)


def circle_num(ax, x, y, n, fill=TEAL, r=2.5):
    ax.add_patch(Circle((x, y), r, facecolor=fill, edgecolor="none", zorder=4))
    text(ax, x, y, str(n), size=9, color=WHITE, weight="bold")


# ---------------------------------------------------------------- workflow

WF = {
    "zh": {
        "title": "八步工作流：从论文到可复核的笔记",
        "sub": "每一步都有产出与通过条件；任何一步不过 → 降级并说明缺口，不编造",
        "steps": [
            ("立卡", "ID / 来源 / 版本\n阅读目的只用于内部"),
            ("结构扫描", "标题 / 摘要 / 图表\n产出主线三句"),
            ("元数据", "YAML frontmatter\n书目 / 代码 / 类型"),
            ("四张抽取表", "问题 / 方法\n证据 / 结论"),
            ("批判评估", "7.1 作者局限\n7.2 进一步局限"),
            ("定位", "最近 2–4 篇工作\n问题 / 方法 / 结论"),
            ("连接与空白", "可迁移方法\n下一步实验与 gap"),
            ("组装自检", "模板 + 质量门\ncheck_note.py"),
        ],
        "foot": "7 步阅读 + 1 步自检；L3 另有第 11/12 节（Python 复现 + 公式核查）",
    },
    "en": {
        "title": "An eight-step workflow: from paper to a checkable note",
        "sub": "Every step has an output and a pass condition; if a gate fails, downgrade and state the gap",
        "steps": [
            ("Intake", "ID / source / version\npurpose stays internal"),
            ("Skim", "title / abstract / figures\nthree-sentence spine"),
            ("Metadata", "YAML frontmatter\nbibliography / code"),
            ("Extraction", "problem / method\nevidence / results"),
            ("Appraisal", "7.1 author limits\n7.2 further limits"),
            ("Positioning", "2–4 nearest works\nproblem / method"),
            ("Connect & gap", "transferable method\nnext experiment"),
            ("Assemble", "template + quality gates\ncheck_note.py"),
        ],
        "foot": "Seven reading steps plus a self-check; L3 adds §§11–12 (Python reproduction + formula verification)",
    },
}


def workflow(lang: str):
    L = WF[lang]
    W, H = 170, 64
    fig, ax = canvas(W, H)
    text(ax, 4, 58, L["title"], size=19, weight="bold", ha="left")
    text(ax, 4, 52, L["sub"], size=9.5, color=MUTED, ha="left")

    w, h, gap = 16.8, 23, 4.2
    x0, y0 = 2.2, 21
    for i, (head, desc) in enumerate(L["steps"]):
        x = x0 + i * (w + gap)
        fill = TEAL_L if i % 2 == 0 else YELLOW_L
        rounded(ax, x, y0, w, h, fill=fill, edge=TEAL if i % 2 == 0 else YELLOW)
        circle_num(ax, x + 3.2, y0 + h - 3.4, i + 1,
                   fill=TEAL if i % 2 == 0 else "#B58B2A", r=2.2)
        text(ax, x + w / 2 + 1.5, y0 + h - 6.6, head, size=10.5, weight="bold")
        text(ax, x + w / 2, y0 + 8, desc, size=8.2, color=MUTED, linespacing=1.5)
        if i < 7:
            arrow(ax, x + w + 0.4, y0 + h / 2, x + w + gap - 0.4, y0 + h / 2,
                  color=TEAL, lw=1.1)

    text(ax, W / 2, 8.5, L["foot"], size=9.5, color=MUTED)
    fig.savefig(OUT / f"workflow-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- architecture

AR = {
    "zh": {
        "title": "四层设计：证据 → 结构 → 质量",
        "layers": [
            ("输入层", "PDF（文本/扫描）· 摘要 · LaTeX/HTML · 多篇论文", TEAL_L, TEAL),
            ("证据层", "定位符 [§4.2] [Table 2] · 四类来源标签 · 数值纪律 · 公式引用闭环", YELLOW_L, "#B58B2A"),
            ("结构层", "L1 速读卡 · L2 标准笔记 · L3 深度笔记 · 4.3 公式链 · 7.1/7.2 局限 · 11/12 复现", ORANGE_L, ORANGE),
            ("质量层", "check_note.py 自检 · build_matrix.py 矩阵 · 质量门清单 · 交付或降级", TEAL_L, TEAL),
        ],
    },
    "en": {
        "title": "A four-layer design: evidence → structure → quality",
        "layers": [
            ("Input", "PDF (text/scanned) · abstract · LaTeX/HTML · multiple papers", TEAL_L, TEAL),
            ("Evidence", "locators [§4.2] [Table 2] · four source tags · number discipline · formula closure", YELLOW_L, "#B58B2A"),
            ("Structure", "L1 quick card · L2 standard note · L3 deep note · 4.3 chain · 7.1/7.2 · 11/12", ORANGE_L, ORANGE),
            ("Quality", "check_note.py · build_matrix.py · quality gates · ship or downgrade", TEAL_L, TEAL),
        ],
    },
}


def architecture(lang: str):
    L = AR[lang]
    W, H = 150, 86
    fig, ax = canvas(W, H)
    text(ax, 6, 80, L["title"], size=19, weight="bold", ha="left")

    y_positions = [56, 39, 22, 5]
    h = 15
    for i, ((title, desc, fill, edge), y) in enumerate(zip(L["layers"], y_positions)):
        rounded(ax, 8, y, 134, h, fill=fill, edge=edge, lw=1.4)
        circle_num(ax, 13, y + h / 2, i + 1, fill=edge, r=2.8)
        text(ax, 19, y + h / 2 + 2.2, title, size=13, weight="bold", ha="left")
        text(ax, 19, y + h / 2 - 3.8, desc, size=9.8, color=MUTED, ha="left")
        if i < 3:
            arrow(ax, 75, y - 0.5, 75, y_positions[i + 1] + h + 0.5, color=TEAL, lw=1.2)

    text(ax, 75, 1.2, "paper → note", size=7.5, color=MUTED, style="italic")
    fig.savefig(OUT / f"architecture-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- formula chain

FC = {
    "zh": {
        "title": "4.3.0 推导主线：公式不是清单，是一条链",
        "nodes": [
            ("起点", "token 表示\n+ 全局交互假设"),
            ("Eq. (1)", "缩放点积注意力\n按相关性聚合"),
            ("多头", "多个子空间\n并行聚合"),
            ("Eq. (2)", "逐位置 FFN\n加非线性"),
            ("位置编码", "注入顺序\n打破置换不变"),
            ("Transformer", "6 层 block\n可堆叠"),
        ],
        "arrows": ["需要聚合", "单头会平均", "只有线性", "对顺序不敏感", "堆叠"],
        "foot": "写 4.3 时先画这条链：上一式留下什么问题，下一式就解决什么。",
    },
    "en": {
        "title": "4.3.0 derivation chain: equations are a story, not a list",
        "nodes": [
            ("Start", "token representations\n+ global interaction"),
            ("Eq. (1)", "scaled dot-product\nattention"),
            ("Multi-head", "parallel subspaces\nfor different relations"),
            ("Eq. (2)", "position-wise FFN\nadds nonlinearity"),
            ("Position", "inject order\nbreak permutation"),
            ("Transformer", "6-layer block\nstackable"),
        ],
        "arrows": ["aggregate", "single head averages", "linear only", "order-blind", "stack"],
        "foot": "Write the chain first: what the previous equation leaves unsolved is what the next one fixes.",
    },
}


def formula_chain(lang: str):
    L = FC[lang]
    W, H = 170, 62
    fig, ax = canvas(W, H)
    text(ax, 4, 56, L["title"], size=19, weight="bold", ha="left")

    n = 6
    w, gap = 20, 7.2
    x0, y0, h = 6, 21, 21
    colors = [(TEAL_L, TEAL), (YELLOW_L, "#B58B2A"), (ORANGE_L, ORANGE),
              (TEAL_L, TEAL), (YELLOW_L, "#B58B2A"), (ORANGE_L, ORANGE)]
    for i, ((head, desc), (fill, edge)) in enumerate(zip(L["nodes"], colors)):
        x = x0 + i * (w + gap)
        rounded(ax, x, y0, w, h, fill=fill, edge=edge, lw=1.3)
        text(ax, x + w / 2, y0 + h - 4.2, head, size=10, weight="bold")
        text(ax, x + w / 2, y0 + 7.6, desc, size=8.4, color=MUTED, linespacing=1.5)
        if i < n - 1:
            arrow(ax, x + w + 0.6, y0 + h / 2, x + w + gap - 0.8, y0 + h / 2,
                  color=TEAL, lw=1.2)
            text(ax, x + w + gap / 2, y0 + h + 4.2, L["arrows"][i], size=7.8,
                 color=MUTED)

    text(ax, W / 2, 8, L["foot"], size=9.5, color=MUTED)
    fig.savefig(OUT / f"formula-chain-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- quality gate

QG = {
    "zh": {
        "title": "交付前的质量门",
        "sub": "check_note.py 把“写得好不好”变成可自动验证的清单",
        "items": [
            "主线三句完整，结果有数字",
            "定位符达标（L2 ≥ 8，去重）",
            "第 5 节有基线、消融与结果数值",
            "4.3.0 推导主线 + 表外推导",
            "每个公式有推导动机与相邻关系",
            "7.1 作者局限 + 7.2 进一步局限",
            "没有占位符、未标注的未核实项",
            "L3：复现计划含可运行 Python 代码",
        ],
        "foot": "0 errors / 0 warnings → 交付；否则先降级（L2→L1）并说明缺口，不编造",
    },
    "en": {
        "title": "Quality gates before delivery",
        "sub": "check_note.py turns “is this note good?” into a checkable list",
        "items": [
            "Three-sentence spine; result has a number",
            "Locators meet the threshold (L2 ≥ 8, deduped)",
            "§5 has baselines, ablations, result numbers",
            "4.3.0 derivation chain + derivation outside tables",
            "Every equation has a motive and adjacent relation",
            "7.1 author limitations + 7.2 further limitations",
            "No placeholders or unlabeled unverified claims",
            "L3: reproduction plan with runnable Python",
        ],
        "foot": "0 errors / 0 warnings → ship; otherwise downgrade (L2→L1) and state the gap",
    },
}


def quality_gate(lang: str):
    L = QG[lang]
    W, H = 150, 80
    fig, ax = canvas(W, H)
    text(ax, 5, 73, L["title"], size=19, weight="bold", ha="left")
    text(ax, 5, 67, L["sub"], size=10.2, color=MUTED, ha="left")

    w, h = 64, 12.2
    xs = [7, 79]
    ys = [49, 34.5, 20, 5.5]
    for i, item in enumerate(L["items"]):
        col, row = i % 2, i // 2
        x, y = xs[col], ys[row]
        rounded(ax, x, y, w, h, fill=WHITE, edge=LINE)
        cx, cy = x + 5, y + h / 2
        ax.add_patch(Circle((cx, cy), 2.6, facecolor=TEAL, edgecolor="none", zorder=3))
        ax.plot([cx - 1.2, cx - 0.3, cx + 1.5], [cy + 0.1, cy - 1.2, cy + 1.3],
                color=WHITE, lw=1.9, solid_capstyle="round", zorder=6)
        text(ax, x + 9.5, y + h / 2 + 0.2, item, size=9.0, ha="left", linespacing=1.35)

    text(ax, 75, 1.2, L["foot"], size=8.8, color=MUTED)
    fig.savefig(OUT / f"quality-gate-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- bad vs good

BG_DATA = {
    "zh": {
        "title": "同一条文献，两种笔记",
        "bad": "普通 AI 笔记",
        "good": "Paper Reading Note",
        "rows": [
            ("作者提出了新方法，\n效果很好。", "WMT14 EN-DE 28.4 BLEU，\n比此前最佳（含集成）高 2.0+ [Table 2]。"),
            ("作者做了大量实验。", "2 个翻译任务 + 1 个句法分析；\nTable 3 覆盖头数、d_k、d_model、\nd_ff、dropout、位置编码。"),
            ("局限是数据集不够多。", "作者承认长序列成本、多模态未验证；\n我补充：无方差/种子、多头可解释性\n只有定性证据。"),
            ("读完之后很有启发。", "可迁移：自注意力 = 全连接图消息传递；\n下一步：Kuramoto 数据上测 N=64/256/1024。"),
        ],
        "foot": "差别不在文采，而在每条判断能不能被复核、被比较、被行动。",
    },
    "en": {
        "title": "Same paper, two kinds of notes",
        "bad": "A generic AI summary",
        "good": "Paper Reading Note",
        "rows": [
            ("The authors propose a new\nmethod with great results.",
             "WMT14 EN-DE 28.4 BLEU,\n2.0+ over the prior best\n(ensembles) [Table 2]."),
            ("The authors did extensive\nexperiments.",
             "2 translation tasks + 1 parsing task;\nTable 3 covers heads, d_k, d_model,\nd_ff, dropout, positional encoding."),
            ("The limitation is that more\ndatasets are needed.",
             "Authors acknowledge long-sequence cost\nand missing modalities; I add: no\nvariance/seeds, only qualitative\nhead interpretability."),
            ("This paper is very inspiring.",
             "Transferable: self-attention as message passing;\nnext: test N=64/256/1024 on Kuramoto data."),
        ],
        "foot": "The difference is not style; it is whether each claim can be checked, compared, and acted on.",
    },
}


def bad_good(lang: str):
    L = BG_DATA[lang]
    W, H = 160, 82
    fig, ax = canvas(W, H)
    text(ax, 5, 76, L["title"], size=19, weight="bold", ha="left")

    panels = [(5, RED_L, RED, L["bad"], 72), (83, GREEN_L, GREEN, L["good"], 72)]
    for x, fill, edge, header, w in panels:
        rounded(ax, x, 8, w, 61, fill=fill, edge=edge, lw=1.4)
        text(ax, x + w / 2, 63, header, size=12, weight="bold")

    ys = [52, 39, 26, 13]
    for i, ((bad, good), y) in enumerate(zip(L["rows"], ys)):
        ax.add_patch(Circle((10, y - 1.4), 0.9, facecolor=RED, edgecolor="none", zorder=4))
        text(ax, 13, y, bad, size=9.8, color=RED,
             ha="left", va="top", linespacing=1.65)
        ax.add_patch(Circle((88, y - 1.4), 0.9, facecolor=GREEN, edgecolor="none", zorder=4))
        text(ax, 91, y, good, size=9.8, color=GREEN,
             ha="left", va="top", linespacing=1.65)

    text(ax, 80, 3.0, L["foot"], size=9.0, color=MUTED)
    fig.savefig(OUT / f"bad-vs-good-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- cover

COVER = {
    "zh": {
        "kicker": "OPEN-SOURCE SKILL · MIT",
        "title": "把论文读成\n可复核、可比较、可行动的笔记",
        "sub": "一个面向 AI Agent 的文献阅读 Skill：证据定位 · 公式推导链 · 局限分析 · Python 复现",
        "chips": ["L1 / L2 / L3", "4.3 公式详解", "质量门自检", "中英双语"],
        "flow": ["论文", "证据", "公式链", "笔记"],
    },
    "en": {
        "kicker": "OPEN-SOURCE SKILL · MIT",
        "title": "Turn a paper into\na note you can check, compare, and act on",
        "sub": "A reading skill for AI agents: evidence locators · derivation chains · limitation analysis · Python reproduction",
        "chips": ["L1 / L2 / L3", "4.3 walkthrough", "quality gates", "EN / 中文"],
        "flow": ["Paper", "Evidence", "Chain", "Note"],
    },
}


def cover(lang: str):
    L = COVER[lang]
    W, H = 170, 72
    fig, ax = canvas(W, H)

    # decorative note card on the right
    rounded(ax, 112, 10, 52, 52, fill=WHITE, edge=LINE, lw=1.2)
    text(ax, 138, 55, "NOTE", size=7, color=MUTED)
    for i, s in enumerate(L["flow"]):
        y = 45 - i * 10
        rounded(ax, 118, y, 40, 7, fill=TEAL_L if i % 2 == 0 else YELLOW_L,
                edge=TEAL if i % 2 == 0 else "#B58B2A", radius=1.4)
        text(ax, 138, y + 3.5, s, size=9.2, weight="bold")
        if i < 3:
            arrow(ax, 138, y - 0.4, 138, y - 2.6, color=TEAL, lw=1.0, ms=8)

    text(ax, 9, 60, L["kicker"], size=8, color=TEAL, weight="bold", ha="left")
    text(ax, 9, 46, L["title"], size=24, weight="bold", ha="left", va="center", linespacing=1.45)
    text(ax, 9, 27, L["sub"], size=9.6, color=MUTED, ha="left", linespacing=1.5)

    x = 9
    for chip in L["chips"]:
        w = 4.2 + len(chip) * 1.55
        rounded(ax, x, 10, w, 7, fill=WHITE, edge=LINE, radius=1.3)
        text(ax, x + w / 2, 13.5, chip, size=8.0, color=INK)
        x += w + 3

    fig.savefig(OUT / f"cover-{lang}.png", dpi=200, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    for lang in ("zh", "en"):
        workflow(lang)
        architecture(lang)
        formula_chain(lang)
        quality_gate(lang)
        bad_good(lang)
        cover(lang)
    print(f"Wrote figures to {OUT}")
