English | [中文](../zh/)

# Paper Reading Note Skill (paper-reading-note)

A complete skill package that turns "reading a paper" into "writing a note that is verifiable, comparable, and actionable":
fixed templates + per-section question lists + per-equation walkthroughs + limitations analysis + multi-paper
matrices + research gap analysis + a self-check script; the L3 reproduction plan comes with runnable Python code.

This folder is the concrete implementation of the introduction article "Skills for Writing Good Reading Notes"
(Chinese original: 《写出好的阅读笔记的skills介绍》): the article lists 12 capabilities, recommends a combination
of 5 core skills, and sketches an Agent workflow. This skill compresses them into **one callable skill + three
reading depths + one quality gate**, and provides executable checking tools in `scripts/`.

This is the English edition; the Chinese edition is in [`../zh/`](../zh/).

## Directory Structure

```text
en/
├── SKILL.md                         # main file: when to use, four iron rules, 7-step workflow, output contract, quality gate
├── README.md                        # this file: install and usage
├── references/
│   ├── 01-extraction-prompts.md     # per-section questions, four extraction tables, prompt library for the 12 capabilities
│   ├── 02-critical-appraisal.md     # restating authors' limitations, further limitations, threats to validity, red-flag checklist
│   ├── 03-comparison-synthesis-gap.md  # comparison matrix, five-part synthesis, four gap categories, concept maps, citation chains
│   ├── 04-evidence-and-style.md     # locators, four tag types, number discipline, wording ladder, citation format
│   ├── 05-reproduction-code.md      # two Python reproduction skeletons: numerical simulation / training
│   └── 06-cover-style.md            # WeChat cover: deep navy + gold phase circle, 900×383 / 600×600
├── templates/
│   ├── speed-card-L1.md             # quick-read card
│   ├── note-L2.md                   # standard note (with 4.3 Equation Walkthrough)
│   ├── reproduction-plan.md         # L3 §11 reproduction plan (with Python code)
│   ├── matrix.md                    # comparison matrix
│   └── synthesis.md                 # synthesis note
├── scripts/
│   ├── check_note.py                # note self-check (structure / locators / numbers / equation walkthrough / reproduction code / placeholders)
│   └── build_matrix.py              # batch notes → matrix (Markdown + CSV)
└── examples/
    └── vaswani2017-attention.md     # completed L2 example (with equation walkthrough, limitations analysis, research connections)
```

## Installation

Any tool that supports `SKILL.md` can use it directly; pick one option:

1. **Claude Code (personal skill)**: copy the whole `en/` directory into `~/.claude/skills/` (for example as `~/.claude/skills/paper-reading-note`).
2. **Claude Code (project skill)**: copy `en/` into the project's `.claude/skills/` as `paper-reading-note`.
3. **DSH / Codex / OpenCode, etc.**: place `en/` in the tool's skill directory; or hand the path of `SKILL.md`
   to the Agent and have it read the skill before reading the paper.
4. **No installation**: in the conversation, say "read this paper following the workflow in `<skill-dir>/SKILL.md`".

## How to Use

### 1. Read a paper (most common)

```text
Read <paper.pdf> and write a reading note following the paper-reading-note L2 workflow, output to notes/xxx.md.
When done, check the notes/ directory with its check_note.py.
```

### 2. Quickly decide whether a paper is worth reading

```text
Make an L1 quick-read card for <paper.pdf>; answer only: problem, approach, key result, whether it is worth a deep read.
```

### 3. L3 deep note (equation walkthrough + Python reproduction)

```text
Read <paper.pdf> and write it as L3: §4.3 explains the meaning and intellectual origin of each equation,
§7 restates the authors' limitations before adding further limitations, §11 gives runnable Python reproduction
code, and §12 verifies the derivations.
```

### 4. Multi-paper comparison + synthesis

```text
Turn these 6 papers on X in notes/ into a matrix, then write a synthesis:
problem lineage, method families and consensus, disagreements and their causes, trends, research gaps.
Tag every judgement with the papers it comes from.
```

### 5. Update an old note

```text
Read notes/xxx.md and add §5 failure cases and §9 research gaps; keep my existing judgements and dates.
```

### 6. Self-check / build a matrix

```powershell
# run from any working directory; set $skill to the actual paper-reading-note path
$skill = '<skill-dir>'
python "$skill/scripts/check_note.py" notes/                    # check every note in the directory
python "$skill/scripts/check_note.py" notes/ --strict            # warnings also count as failures
python "$skill/scripts/check_note.py" notes/ --abstract          # abstract-only card mode
python "$skill/scripts/build_matrix.py" notes/ -o notes/matrix.md --csv notes/matrix.csv
```

PowerShell does not expand `notes/*.md`, so pass the directory directly; the script searches recursively and
skips `index.md`, `matrix.md`, `README.md`, and template files.

`check_note.py` exit codes: `0` pass; `1` checks failed (or warnings under `--strict`); `2` path/argument error
(including no checkable notes in the directory). `build_matrix.py` exit codes: `0` success; `1` no usable notes;
`2` path error. `build_matrix.py` generates the automatic columns and leaves four blank columns — Delta,
Evidence quality, Reproducibility, Relevance — for manual filling. Links are computed relative to the directory
of the output file; if the output file and the notes are on different drives, links fall back to absolute paths
(still openable).

## What You Get After Reading

An L2 standard note contains:

| Section | Content |
|---------|---------|
| 0 At a Glance | problem / approach / result / why it matters |
| 1 Paper Information | authors, venue, version, code/data |
| 2 Problem Definition | background, pain point, formalization, assumptions, success criteria |
| 3 Related Work | the 2–4 closest works + three-dimensional positioning |
| 4 Method | architecture, key modules and equations, **4.3 Equation Walkthrough** (4.3.0 derivation chain / how the equations connect + per-equation meaning/symbols/motive/intellectual origin/role), training details, complexity, reproducibility |
| 5 Experiments and Evidence | data, baselines, main results, ablations, failure cases, statistics |
| 6 Main Findings | three columns: authors claim / evidence support / my judgement |
| 7 Critical Appraisal | 7.1 restatement of the authors' limitations, 7.2 further limitations, 7.3 strengths and scope, 7.4 threats to validity and reproducibility, 7.5 information gaps (no scoring, no confidence ratings) |
| 8 Inspirations | transferable, reusable, pitfalls to avoid, next experiments, follow-up questions |
| 9 Research Gaps | problem/method/evidence/application gaps, each with evidence and a verifiable next step |
| 10 Key Quotations | verbatim quotations with page numbers |

L3 adds:

| Section | Content |
|---------|---------|
| 11 Reproduction Plan | environment, parameter table, **runnable Python code**, run command, acceptance criteria, falsification conditions, known gaps |
| 12 Formula and Derivation Verification | symbol/dimension table, step-by-step check, errata, remaining doubts |

Example: [`examples/vaswani2017-attention.md`](examples/vaswani2017-attention.md).

### WeChat Cover (Optional)

When publishing on WeChat, an optional cover can be generated; it is not part of the body.

- main cover 900×383 (2.35:1), square cover 600×600 (1:1);
- deep navy background, gold only for kicker/formula/ring/arrow;
- left text block, right phase circle (gold = locked nucleus, gray = wild, center `SI`);
- full palette, coordinates, type sizes and self-check: [`references/06-cover-style.md`](references/06-cover-style.md).

## Design Notes

- **One skill instead of 12**: the 12 capabilities from the article are orchestrated into a 7-step workflow;
  multi-paper mode reuses the same note set, so 12 small skills do not have to know about each other.
- **Three depths**: L1 quick-read card (10–15 min), L2 standard note (45–90 min), L3 deep note (with reproduction
  plan); escalate by "is it worth reading" instead of writing a long text up front.
- **Anti-hallucination first**: every conclusion needs a locator; four tag types separate original/inference/
  external/question; abstract-only input forces L1.
- **Equation walkthrough with a through-line**: §4.3 first writes the 4.3.0 derivation chain (where it starts,
  why each step introduces the next equation, what the next equation connects to), then explains each equation's
  meaning/symbols/motive/source.
- **Formula citation closure**: when citing an original `Eq. (x)`/appendix equation number, if the equation has
  not appeared in the note, write it out at the citation point; range citations keep only the numbers already shown.
- **Derivation outside the table**: below each equation table in §4.3, write the full derivation from the
  "derivation motive / intellectual origin" to the target equation; once the derivation is written, the table's
  motive/source rows may be condensed.
- **Derivation register**: §4.3 derivations use paper-style prose (suppose / let / from ... we obtain / therefore /
  hence), with no teaching-style step numbers and no self-justifying meta-discourse.
- **Proofreading pass**: after writing the derivation, read every sentence for subject, collocation, redundancy,
  logical repetition, and reference; fix problems in place.
- **Field guide**: L2/L3 add 2–3 paragraphs before §0 introducing the field (research object, three-level problem,
  which level this paper adds); a self-drawn schematic may be added, captioned "drawn by me, not from the paper".
- **Figure embedding**: crop original figures from the PDF (with the caption, kept complete) and store them in
  `notes/figures/`; one figure per line, centered, captions with figure number and page.
- **No skipped derivation steps**: §4.3 derivations give the original equation each step relies on and the
  operation performed (substitution/expansion/averaging/integration); basic algebra such as transposition need
  not be expanded, but "from X we obtain Y" must state the basis.
- **Starting expressions labelled by source**: an initial expression in a derivation must be labelled as a
  definition, an established fact/conservation law, a prior result (Eq. x), or a paper assumption; composite
  expressions give the simplest case first, then the added term.
- **Key claims get a mechanism**: for "only if / necessarily / equivalent" claims, write "claim → 1–3 equation
  minimal mechanism → one intuition → boundaries"; not a full proof, and not a bare conclusion.
- **Reader marks and Appendix 1**: readers mark unfamiliar terms with `<u>term</u>$^{[n]}$`, and the Agent explains
  each by number in "Appendix 1: Terminology" at the end; the appendix does not count toward body length.
- **Formula rendering rules**: no natural-language text inside math mode; display equations use multi-line `$$`;
  use `\lvert`/`\rvert` in tables.
- **No usage-scenario wording**: the note body and frontmatter must not mention reporting, sharing, coursework,
  group discussion, or similar scenarios, and do not record the reading purpose.
- **Critical appraisal without scoring**: no 8-dimension scores, no confidence ratings; restate the authors'
  acknowledged limitations first, then add further limitations.
- **Executable quality gate**: `check_note.py` checks the required sections, deduplicated locators, the result
  numbers and baseline/ablation keywords in §5, the §4.3 equation walkthrough and derivation outside the table,
  the 7.1/7.2 limitation structure, L3 reproduction code, and leftover authors/keywords and placeholders —
  turning "is this note good" into an automatically verifiable checklist.

## Mapping to the 5 Core Skills in the Article

| Skill in the article | Where this skill covers it |
|----------------------|----------------------------|
| Metadata Extractor | Step 2 + frontmatter field table |
| Methodology Extractor | Step 3 method table + §4 |
| Critical Appraisal | Step 4 + `02-critical-appraisal.md` |
| Comparison Matrix Builder | multi-paper mode + `build_matrix.py` + `03` |
| Reading Note Generator | `templates/` + Step 7 + `check_note.py` |

## Maintenance

- Version: 1.3.11 (2026-10-22)
- Since 1.3.11: readers can mark unknown terms with `<u>term</u>$^{[n]}$`, and the Agent explains each by number
  in "Appendix 1: Terminology" (definition/role/difference); the appendix does not count toward body length;
  check_note.py verifies that marks and appendix entries correspond.
- Since 1.3.10: if the minimal mechanism of a key claim uses linearization, write out the Taylor expansion
  (first-order term + remainder); "linearizing gives" is not enough.
- Since 1.3.9: "only if / necessarily / equivalent" key claims must give a minimal mechanism (1–3 equations, e.g.
  linearization), one colloquial intuition, and the applicable boundaries; not a full proof, and not only a
  conclusion.
- Since 1.3.8: a composite starting expression must be given in layers: write the simplest case first (e.g. the
  free-running $d\phi/dt=1/T$), then explain why the new $\Delta f$ term appears after stimulation is added; do
  not drop the final expression with a parenthetical.
- Since 1.3.7: initial expressions in derivations must state their source (definition / established fact or
  conservation law / prior result / paper assumption); do not write only "from Eq. (x)".
- Since 1.3.6: the boundary of "no skipped steps" is clarified — state the original equation and the operation
  (substitution/expansion/averaging/integration/limit), but basic algebra such as transposition and collecting
  like terms need not be expanded; the old requirement of an intermediate equation at every step was too strict
  and has been changed.
- Since 1.3.5: the §4.3 "Derivation process" must not skip steps: each step gives the basis and the intermediate
  equation; "from Eq. X we obtain Eq. Y" is forbidden; appendix equations are shown before citation; other
  sections may still summarize.
- Since 1.3.4: L2/L3 require a field guide before §0 (written for readers unfamiliar with the field, with the
  three-level problem and this paper's position, optionally a self-drawn schematic); original figures are cropped
  from the PDF and stored in `notes/figures/`, one per line, centered, captions with figure number and page;
  check_note.py adds a warning for a missing field guide.
- Since 1.3.3: §4.3 derivations use paper-style prose (suppose / let / from ... we obtain / therefore / hence;
  no teaching-style numbering or meta-discourse), and after writing, read every sentence for language problems
  (subjects, collocations, redundancy, logical repetition, reference); check_note.py adds a meta-discourse warning.
- Since 1.3.2: each equation table in §4.3 requires a "Derivation process" below it (outside the table, step by
  step from motive/source to the target equation); formula rendering rules specified (no natural-language text in
  math mode, multi-line `$$` display equations, `\lvert` in tables).
- Since 1.3.1: when citing original equation numbers, if the equation has not appeared in the note, give the
  equation at the citation point; range citations list only shown numbers (an incremental requirement that does
  not change the structure of old notes).
- Backward compatibility: since 1.2.0 §7 is "7.1 restate authors' limitations + 7.2 further limitations", the L3
  reproduction plan is §11 and formula verification is §12; since 1.3.0 §4.3 requires the 4.3.0 derivation chain
  first. Old notes are not rewritten automatically; add at least the 4.3.0 derivation chain and a "Derivation
  motive" per equation, then run the self-check.
- Adapting to a new discipline: add fields to the method/experiment tables in `templates/note-L2.md`, or copy it
  as `note-L2-<field>.md`.
- Adjusting check strictness: `LOCATOR_MIN`, `SECTION5_NUM_MIN`, and `SECTIONS` at the top of
  `scripts/check_note.py`.
- License: MIT.
