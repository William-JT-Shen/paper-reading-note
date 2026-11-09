#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""draw_schematic.py — 自绘示意图的版式工具与几何自检

配合《references/07-self-drawn-figure.md》的版式硬规则使用：把"方框/箭头/文字"
交给本模块生成，端点会自动吸附到边框外侧，保存前再用几何断言拦住四类排版问题——

  1. 箭头穿框：端点落在方框内部或压住框内文字；
  2. 悬空箭头：声明了起点或终点却没有接到目标元素；
  3. 文字压线：图注/小标题与方框、箭头或彼此重叠；
  4. 留白失衡、同组框不齐：四边留白不等、同组方框宽高或间距不一致。

用法一（作为库，推荐）：

    from draw_schematic import Canvas

    c = Canvas()
    c.title(0, 35.5, "领域的三层问题")
    b1 = c.box(0, 23.5, 26, 8.5, "第一层：正问题", "模型已知，数值求解并观测")
    b2 = c.box(0, 12.0, 26, 8.5, "第二层：反问题", "模型类已知，从数据定参数或定结构")
    b3 = c.box(0,  0.5, 26, 8.5, "第三层：开放探索", "模型类未知，自主设计实验", ec=GOLD, lw=2.0)
    c.group([b1, b2, b3], axis="v")
    c.arrow(b1, b2, "bottom", "top")
    c.arrow(b2, b3, "bottom", "top")
    c.check()                 # 有问题抛 AssertionError，通过则静默
    c.save("fig00-field-map.png")

用法二（命令行，检查已有 PNG 的留白与画幅；需要 Pillow）：

    python draw_schematic.py --check fig00-field-map.png

数据坐标约定：1 个坐标单位 = scale 英寸（默认 0.1 in），x 向右、y 向上。
字号按 point 给定，换算成坐标单位后参与排版检查。
"""

from __future__ import annotations

import argparse
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ---------------------------------------------------------------- 配色与字体

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

DARK = "#0B1F33"
GOLD = "#C8922A"
MIST = "#9FB3C8"
INK = "#3A4A5C"

_FONT_CANDIDATES = [
    "Microsoft YaHei", "SimHei", "DengXian", "Source Han Sans SC",
    "Noto Sans CJK SC", "DejaVu Sans",
]


def _pick_font() -> str:
    import matplotlib.font_manager as fm

    names = {f.name for f in fm.fontManager.ttflist}
    for name in _FONT_CANDIDATES:
        if name in names:
            return name
    return "DejaVu Sans"


# ---------------------------------------------------------------- 几何小工具

def _rect_intersect(a, b, tol=0.0):
    """两矩形是否相交（tol>0 表示先各自外扩 tol/2 再判）。"""
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 + tol / 2 <= bx0 or bx1 + tol / 2 <= ax0
                or ay1 + tol / 2 <= by0 or by1 + tol / 2 <= ay0)


def _rect_union(rects):
    xs0 = min(r[0] for r in rects)
    ys0 = min(r[1] for r in rects)
    xs1 = max(r[2] for r in rects)
    ys1 = max(r[3] for r in rects)
    return (xs0, ys0, xs1, ys1)


def _rect_contains(outer, inner, pad=0.0):
    return (inner[0] >= outer[0] + pad and inner[1] >= outer[1] + pad
            and inner[2] <= outer[2] - pad and inner[3] <= outer[3] - pad)


_SIDE_NORMAL = {
    "left": (-1.0, 0.0), "right": (1.0, 0.0),
    "bottom": (0.0, -1.0), "top": (0.0, 1.0),
}


# ---------------------------------------------------------------- 元件

class Box:
    def __init__(self, canvas, x, y, w, h, title, sub, patch, title_art, sub_arts):
        self.canvas = canvas
        self.x, self.y, self.w, self.h = x, y, w, h
        self.title = title
        self.sub = sub
        self.patch = patch
        self.title_art = title_art
        self.sub_arts = sub_arts

    @property
    def rect(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def edge_point(self, side):
        x0, y0, x1, y1 = self.rect
        if side == "left":
            return (x0, (y0 + y1) / 2)
        if side == "right":
            return (x1, (y0 + y1) / 2)
        if side == "bottom":
            return ((x0 + x1) / 2, y0)
        if side == "top":
            return ((x0 + x1) / 2, y1)
        raise ValueError(f"side 必须是 left/right/bottom/top，收到 {side!r}")


class Arrow:
    def __init__(self, canvas, p0, p1, patch, src, dst, from_side, to_side, label, label_art):
        self.canvas = canvas
        self.p0, self.p1 = p0, p1
        self.patch = patch
        self.src, self.dst = src, dst
        self.from_side, self.to_side = from_side, to_side
        self.label = label
        self.label_art = label_art


# ---------------------------------------------------------------- 画布

class Canvas:
    """坐标单位 = scale 英寸；所有元素放进来后 check() → save()。"""

    def __init__(self, scale=0.1, dpi=200):
        self.scale = float(scale)
        self.dpi = int(dpi)
        self.font = _pick_font()
        plt.rcParams["font.family"] = self.font
        plt.rcParams["axes.unicode_minus"] = False
        self.fig = plt.figure(figsize=(10, 6), dpi=self.dpi)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_axis_off()
        self.boxes: list[Box] = []
        self.arrows: list[Arrow] = []
        self.texts = []          # (artist, kind)
        self.groups = []         # (boxes, axis, name)
        self._set_view(0, 100, 0, 60)

    # ---- 视图：始终保证 1 单位 = scale 英寸
    def _set_view(self, x0, x1, y0, y1):
        self.ax.set_xlim(x0, x1)
        self.ax.set_ylim(y0, y1)
        self.fig.set_size_inches((x1 - x0) * self.scale, (y1 - y0) * self.scale)
        self.ax.set_position([0, 0, 1, 1])

    # ---- 元件添加
    def title(self, x, y, text, size=11.0, color=DARK, ha="left", va="center", bold=True):
        art = self.ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color,
                           fontweight="bold" if bold else "normal")
        self.texts.append((art, "title"))
        return art

    def note(self, x, y, text, size=8.0, color=GOLD, ha="left", va="center", bold=True):
        art = self.ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color,
                           fontweight="bold" if bold else "normal")
        self.texts.append((art, "note"))
        return art

    def box(self, x, y, w, h, title, sub=None, fc="white", ec=DARK, lw=1.2,
            title_size=9.5, sub_size=7.6, title_color=DARK, sub_color=INK):
        patch = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.30,rounding_size=1.0",
                               linewidth=lw, edgecolor=ec, facecolor=fc)
        self.ax.add_patch(patch)
        title_art = self.ax.text(x + w / 2, y + h * (0.66 if sub else 0.50), title,
                                 ha="center", va="center", fontsize=title_size,
                                 color=title_color, fontweight="bold")
        sub_arts = []
        if sub:
            lines = sub.split("\n")
            line_h = sub_size / 72.0 / self.scale * 1.45
            y0 = y + h * 0.32 + (len(lines) - 1) * line_h / 2
            for i, line in enumerate(lines):
                art = self.ax.text(x + w / 2, y0 - i * line_h, line, ha="center",
                                   va="center", fontsize=sub_size, color=sub_color)
                sub_arts.append(art)
        b = Box(self, x, y, w, h, title, sub, patch, title_art, sub_arts)
        self.boxes.append(b)
        return b

    def check(self, strict=True, gap_min=1.0, pad_min=0.30, attach_tol=0.6):
        """几何自检；strict=True 时有问题抛 AssertionError，否则返回问题清单。"""
        problems = self._run_checks(gap_min, pad_min, attach_tol)
        if strict and problems:
            raise AssertionError("示意图版式自检未通过（%d 项）：\n- %s"
                                 % (len(problems), "\n- ".join(problems)))
        return problems

    def _run_checks(self, gap_min, pad_min, attach_tol):
        self._draw()
        p = []

        # 1) 文字不出框
        for b in self.boxes:
            for art in [b.title_art] + b.sub_arts:
                tb = self._artist_bbox(art)
                if not _rect_contains(b.rect, tb, pad=pad_min):
                    p.append(f"方框「{b.title}」内文字超出边界或贴边（pad<{pad_min}）：{art.get_text()!r}")

        # 2) 方框不重叠且留出最小间隙
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                a, b = self.boxes[i], self.boxes[j]
                if _rect_intersect(a.rect, b.rect, tol=gap_min):
                    p.append(f"方框重叠或间距 < {gap_min}：{a.title!r} / {b.title!r}")

        # 3) 独立文字（标题/图注）不与方框、彼此重叠
        for art, kind in self.texts:
            tb = self._artist_bbox(art)
            for b in self.boxes:
                if _rect_intersect(tb, b.rect, tol=0.2):
                    p.append(f"{kind} 文字压到方框「{b.title}」：{art.get_text()!r}")
            for art2, _ in self.texts:
                if art2 is art:
                    continue
                if _rect_intersect(tb, self._artist_bbox(art2), tol=0.2):
                    p.append(f"两段文字重叠：{art.get_text()!r} / {art2.get_text()!r}")

        # 4) 箭头：必须两端有目标、吸附正确、不穿框、不压文字
        for a in self.arrows:
            if a.src is None or a.dst is None:
                p.append(f"悬空箭头：{a.p0} → {a.p1}（起点或终点没有接到任何元素）")
                continue
            exp0 = self._attach_point(a.src, a.from_side, a.canvas_pad)
            exp1 = self._attach_point(a.dst, a.to_side, a.canvas_pad)
            if math.dist(a.p0, exp0) > attach_tol:
                p.append(f"箭头起点没有吸附在「{a.src.title}」的 {a.from_side} 边外侧"
                         f"（偏差 {math.dist(a.p0, exp0):.2f}）")
            if math.dist(a.p1, exp1) > attach_tol:
                p.append(f"箭头终点没有吸附在「{a.dst.title}」的 {a.to_side} 边外侧"
                         f"（偏差 {math.dist(a.p1, exp1):.2f}）")
            if a.from_side in ("left", "right") and a.to_side in ("left", "right"):
                if abs(a.p0[1] - a.p1[1]) > 0.8:
                    p.append(f"水平箭头两端不在同一高度（相差 {abs(a.p0[1]-a.p1[1]):.2f}）："
                             f"{a.src.title} → {a.dst.title}")
            if a.from_side in ("top", "bottom") and a.to_side in ("top", "bottom"):
                if abs(a.p0[0] - a.p1[0]) > 0.8:
                    p.append(f"竖直箭头两端不在同一竖线（相差 {abs(a.p0[0]-a.p1[0]):.2f}）："
                             f"{a.src.title} → {a.dst.title}")
            if math.dist(a.p0, a.p1) < 1.5:
                p.append(f"箭头过短（{math.dist(a.p0, a.p1):.2f} 单位）："
                         f"{a.src.title} → {a.dst.title}")
            for t in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95):
                pt = (a.p0[0] + (a.p1[0] - a.p0[0]) * t, a.p0[1] + (a.p1[1] - a.p0[1]) * t)
                for b in self.boxes:
                    if _rect_contains(b.rect, (pt[0], pt[1], pt[0], pt[1])):
                        p.append(f"箭头穿过方框「{b.title}」：{a.src.title} → {a.dst.title}")
                        break
            if a.label_art is not None:
                lb = self._artist_bbox(a.label_art)
                for b in self.boxes:
                    if _rect_intersect(lb, b.rect, tol=0.2):
                        p.append(f"箭头标签压到方框「{b.title}」：{a.label!r}")
                for t in (0.2, 0.4, 0.6, 0.8):
                    pt = (a.p0[0] + (a.p1[0] - a.p0[0]) * t, a.p0[1] + (a.p1[1] - a.p0[1]) * t)
                    if _rect_intersect(lb, (pt[0], pt[1], pt[0], pt[1]), tol=0.2):
                        p.append(f"箭头标签压住箭头线：{a.label!r}")

        # 5) 同组方框等大、等距
        for boxes, axis, name in self.groups:
            if len(boxes) < 2:
                continue
            ws = {round(b.w, 2) for b in boxes}
            hs = {round(b.h, 2) for b in boxes}
            if len(ws) > 1 or len(hs) > 1:
                p.append(f"组「{name}」方框宽高不一致：w={sorted(ws)} h={sorted(hs)}")
            if axis == "v":
                ordered = sorted(boxes, key=lambda b: b.y)
                gaps = [round(ordered[i + 1].y - (ordered[i].y + ordered[i].h), 2)
                        for i in range(len(ordered) - 1)]
            else:
                ordered = sorted(boxes, key=lambda b: b.x)
                gaps = [round(ordered[i + 1].x - (ordered[i].x + ordered[i].w), 2)
                        for i in range(len(ordered) - 1)]
            if len(gaps) > 1 and (max(gaps) - min(gaps)) > 0.5:
                p.append(f"组「{name}」间距不等：{gaps}")

        return p

    def group(self, boxes, axis="v", name=""):
        self.groups.append((list(boxes), axis, name or "未命名组"))

    # ---- 箭头
    def arrow(self, src, dst, from_side, to_side, pad=0.9, color=DARK, lw=1.3,
              mutation=11, label=None, label_off=(0.0, 0.0), label_size=7.6, label_color=INK):
        p0 = self._attach_point(src, from_side, pad)
        p1 = self._attach_point(dst, to_side, pad)
        patch = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=mutation,
                                linewidth=lw, color=color, shrinkA=0, shrinkB=0)
        self.ax.add_patch(patch)
        art = None
        if label:
            mx, my = (p0[0] + p1[0]) / 2 + label_off[0], (p0[1] + p1[1]) / 2 + label_off[1]
            art = self.ax.text(mx, my, label, ha="center", va="center",
                               fontsize=label_size, color=label_color)
        a = Arrow(self, p0, p1, patch, src, dst, from_side, to_side, label, art)
        a.canvas_pad = pad
        self.arrows.append(a)
        return a

    def arrow_raw(self, p0, p1, color=DARK, lw=1.3, mutation=11):
        """不接目标的箭头：check() 会报"悬空箭头"，只用于确实需要自由箭头的场合。"""
        patch = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=mutation,
                                linewidth=lw, color=color, shrinkA=0, shrinkB=0)
        self.ax.add_patch(patch)
        a = Arrow(self, p0, p1, patch, None, None, None, None, None, None)
        a.canvas_pad = 0.0
        self.arrows.append(a)
        return a

    @staticmethod
    def _attach_point(box, side, pad):
        ex, ey = box.edge_point(side)
        nx, ny = _SIDE_NORMAL[side]
        return (ex + nx * pad, ey + ny * pad)

    # ---- 度量
    def _draw(self):
        self.fig.canvas.draw()

    def _artist_bbox(self, art):
        r = self.fig.canvas.get_renderer()
        bb = art.get_window_extent(renderer=r)
        inv = self.ax.transData.inverted()
        x0, y0 = inv.transform((bb.x0, bb.y0))
        x1, y1 = inv.transform((bb.x1, bb.y1))
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    def content_bbox(self):
        self._draw()
        rects = [b.rect for b in self.boxes]
        for a in self.arrows:
            rects.append((a.p0[0], a.p0[1], a.p1[0], a.p1[1]))
        for art, _ in self.texts:
            rects.append(self._artist_bbox(art))
        for a in self.arrows:
            if a.label_art is not None:
                rects.append(self._artist_bbox(a.label_art))
        return _rect_union(rects)

    # ---- 收尾：按内容包围盒重设画布，四边留白相等
    def finalize(self, margin=2.5):
        x0, y0, x1, y1 = self.content_bbox()
        self._set_view(x0 - margin, x1 + margin, y0 - margin, y1 + margin)
        self._draw()
        return self.fig.get_size_inches()

    def save(self, path, margin=2.5):
        self.finalize(margin=margin)
        problems = self._run_checks(1.0, 0.30, 0.6)
        if problems:
            raise AssertionError("示意图版式自检未通过（%d 项）：\n- %s"
                                 % (len(problems), "\n- ".join(problems)))
        self.fig.savefig(path, dpi=self.dpi, facecolor="white")
        return path


# ---------------------------------------------------------------- 已有 PNG 的留白检查

def check_image(path, min_margin_pct=2.0, max_ratio=2.5):
    """检查已生成 PNG 的四边留白与画幅比例；返回问题清单（空表示通过）。"""
    try:
        from PIL import Image
        import numpy as np
    except Exception as exc:  # pragma: no cover
        return [f"未安装 Pillow/numpy，跳过像素级检查：{exc}"]
    problems = []
    im = Image.open(path).convert("L")
    a = np.asarray(im)
    mask = a < 245
    if not mask.any():
        return [f"{os.path.basename(path)}：整张图是空白"]
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    h, w = a.shape
    margins = {"左": cols[0], "上": rows[0], "右": w - 1 - cols[-1], "下": h - 1 - rows[-1]}
    mmin = min(w, h)
    pct = {k: 100.0 * v / mmin for k, v in margins.items()}
    for k, v in pct.items():
        if v < min_margin_pct:
            problems.append(f"{os.path.basename(path)}：{k}边留白仅 {v:.1f}%（< {min_margin_pct}%）")
    lo, hi = min(pct.values()), max(pct.values())
    if hi > max_ratio * lo:
        problems.append(f"{os.path.basename(path)}：四边留白失衡，最小 {lo:.1f}% / 最大 {hi:.1f}%"
                        f"（> {max_ratio} 倍）")
    # 画幅与内容比例：内容太长或太高都会留下大片空白
    cw, ch = cols[-1] - cols[0] + 1, rows[-1] - rows[0] + 1
    if w / h > 1.25 * (cw / ch) or h / w > 1.25 * (ch / cw):
        problems.append(f"{os.path.basename(path)}：画幅 {w}x{h} 与内容 {cw}x{ch} 比例不匹配，"
                        f"存在大片空白")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="示意图版式检查 / 自检")
    ap.add_argument("--check", metavar="PNG", nargs="+", help="检查已有 PNG 的留白与画幅")
    args = ap.parse_args(argv)
    if not args.check:
        ap.print_help()
        return 0
    bad = 0
    for path in args.check:
        probs = check_image(path)
        if probs:
            bad += 1
            print(f"== {path} ==")
            for p in probs:
                print("  [问题]", p)
        else:
            print(f"== {path} == 通过")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
