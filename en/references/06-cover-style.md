# WeChat Cover Style: Deep Navy + Gold Phase Circle

Optional cover style for notes published on WeChat. The cover is not part of the note body and is not checked by the L1/L2/L3 quality gate.

## When to use

- Generate a cover only when the note is published on WeChat;
- Default outputs: main cover **900×383** (2.35:1), square cover **600×600** (1:1);
- If the platform accepts only one source image, upload the 900×383 and crop the 1:1 from the phase circle on the right; do not squeeze the title out of the 1:1 crop.

## Palette

| Use | Hex | Note |
|-----|-----|------|
| Background | `#0B1F33` | deep navy, no gradient |
| Accent | `#E8B44A` | warm gold; only kicker, formula, ring, arrow |
| Body text | `#F4EFE6` | warm white; title and subtitle |
| Secondary | `#9FB3C8` | muted blue-gray; metadata, wild dots |

No shadows, glows, gradients, or stickers; dark background relies on contrast.

## Main cover (900×383)

| Element | Position / size | Note |
|---------|-----------------|------|
| Kicker | (48, 336), 11.5 pt, gold | `WINFREE 1967 · CLOSE READING`, replace with paper short id |
| Title | (48, 272), 38 pt, bold, warm white | Chinese key phrase, ≤ 8 characters |
| Subtitle | (48, 224), 16.5 pt | one line, ≤ 20 characters; core question |
| Gold rule | x=48–430, y=193, lw 1.0 | separates title from formula |
| Formula | (48, 166), 20 pt, gold | at most one core equation |
| Critical condition | (48, 128), 12.5 pt, warm white | one line |
| Metadata | (48, 92), 9.8 pt, muted | `authors | journal volume(issue), pages` |

Left-aligned text block; do not cross x≈470.

## Phase circle on the right

Center `(705, 188)`, radius `R=104`:

- three concentric rings: `R`, `0.72R`, `0.45R`, gold, `alpha=0.18`, `lw=0.7`;
- locked nucleus: 22 gold dots, angles about `−0.55…0.55 + 0.15`, radius `0.93R`;
- wild oscillators: 30 muted dots, random angles, radius `0.55R…1.12R`, `alpha=0.65`;
- thin lines from center to gold dots, `alpha=0.28` (coherent sum);
- center `SI` (34 pt, bold, warm white), below it "threshold" (13 pt, gold);
- short outward arrow at angle `0.15`, from `R+20` to `R+52`, gold, no label;
- keep every element at x≤870; ≥30 px right margin.

## Square cover (600×600)

Same palette and ring, centered:

| Element | Position / size |
|---------|-----------------|
| Kicker | (300, 556), 12 pt |
| Title | (300, 500), 46 pt, bold |
| Subtitle | (300, 438), 14.5 pt |
| Phase circle | center (300, 310), R=112 |
| Gold rule | x=150–450, y=152 |
| Formula | (300, 120), 19 pt |
| Critical condition | (300, 82), 12.5 pt |
| Metadata | (300, 42), 8.8 pt |

## Content rules

1. Title is a short Chinese key phrase, not the English paper title; put the paper title in the metadata line or the article body.
2. At most one formula; do not stack abstract, contribution list, or author photo.
3. Gold only for kicker, formula, ring, arrow; title and subtitle are warm white.
4. Metadata is one line: `authors | journal volume(issue), pages`; year optional.
5. Do not use a screenshot of the paper's first page as the default; if used, make a separate version and label it "original figure".
6. Never place text over the ring; keep ≥20 px between text and ring.
7. The title must remain readable at 26 px; keep it ≤8 Chinese characters.

## Generation

- matplotlib, `figsize=(9, 3.83)`, `dpi=100` gives exactly 900×383;
- `fig.add_axes([0, 0, 1, 1])`, `xlim(0,900)`, `ylim(0,383)`, `axis("off")`;
- write coordinates in pixels; at 100 dpi, 1 pt ≈ 1.39 px;
- save with `facecolor=bg`; do **not** use `bbox_inches="tight"` (it changes the canvas);
- square cover: `figsize=(6,6)`, `dpi=100`;
- font `Microsoft YaHei`; math `mathtext.fontset="dejavusans"`.

## Self-check

- clear gap between title and subtitle;
- metadata ≥20 px above the bottom edge, not clipped;
- all rings, dots and arrow inside the canvas;
- title still inside the central safe area after the 1:1 crop;
- title readable in a 26 px thumbnail;
- no third accent colour.

## File names

```text
cover-900x383.png
cover-600x600.png
```

## Anti-patterns

- using the paper's first page as the default cover;
- low-contrast grey text on a dark background;
- title longer than 12 characters and unreadable in a thumbnail;
- the ring covering the title or formula;
- the 1:1 crop cutting off the title;
- three accent colours at once.
