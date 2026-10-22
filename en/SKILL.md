---
name: paper-reading-note
version: 1.3.11
description: |
  Turn a paper into a paper reading note that is "verifiable, comparable, actionable". Covers single-paper
  deep reads, quick-read triage, multi-paper comparison matrices, topic synthesis, and research gap analysis;
  every conclusion requires a section/page/figure locator, and original text, inference, and external
  knowledge are kept apart. Key equations are explained one by one, including meaning and intellectual
  origin; the authors' acknowledged limitations are restated before further limitations are added; L3 also
  requires runnable Python reproduction code.
  When citing an original equation number that has not yet appeared in the note, write out the equation at
  the citation point.
  The Equation Walkthrough requires, below each equation table (outside the table), a complete derivation
  from the derivation motive / intellectual origin to the target equation; the derivation process uses
  paper-style prose (suppose / let / from ... we obtain / therefore / hence), with no teaching-style
  numbering and no self-justifying meta-discourse; proofread it sentence by sentence afterwards.
  Derivation blocks must not skip steps: each step states the original equation it relies on and the
  operation performed; do not write only "from Eq. X we obtain Eq. Y"; basic algebra such as transposition
  need not be expanded.
  When giving a starting expression, state its source: a definition, an established fact / conservation law,
  a prior result (Eq. x), or a paper assumption.
  Composite expressions are given in layers: write the simplest case first (e.g., the free-running
  $d\phi/dt=1/T$), then explain why the new term is added (e.g., the frequency increment $\Delta f$ caused by
  stimulation).
  Key claims ("only if...", "necessarily...", "equivalent to...") require a minimal mechanism and one
  intuitive sentence, not a full proof; linearization must write out the Taylor expansion.
  Readers can mark unknown terms with `<u>term</u>$^{[n]}$`, and the Agent must explain them by number in
  "Appendix 1: Terminology"; the appendix does not count toward body length.
  L2/L3 notes add a field guide before §0 (written for readers unfamiliar with the field, optionally with a
  self-drawn schematic).
  Original figures are cropped from the PDF and stored in `notes/figures/`: one figure per line, centered,
  with the figure number and page in the caption.
  No natural-language text inside math mode; display equations use multi-line $$.
  Use when the user asks to read a paper (PDF/text/abstract), write literature reading notes, compare
  multiple papers, or find research gaps.
  Not for: fabricating content from a title/abstract alone, writing a paper on the user's behalf, or
  fabricating citations or data.
license: MIT
compatibility: claude-code codex dsh opencode
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, AskUserQuestion]
---

# Paper Reading Note

> Goal: turn a paper into a note that is **verifiable, comparable, and actionable**, not a longer abstract.

Most AI-generated literature notes share four common failures: rewriting the abstract, writing conclusions without methods, praising without critiquing, and finishing with no relevance to the reader. This skill blocks each of them with four hard constraints, and ships fixed templates, an equation walkthrough framework, a limitations analysis framework, a self-check script, and copy-paste prompts.

## The Four Iron Rules

| # | Iron rule | Concrete requirement | Failure it blocks |
|---|-----------|----------------------|-------------------|
| 1 | **Evidence first** | Every key claim is followed by a locator (`[§4.2]`, `[Table 2]`, `[p.7]`); if no source can be found, write "not reported" and do not guess; when citing `Eq. (x)`, if the equation has not yet appeared in the note, write it out at the citation point | abstract rewriting |
| 2 | **Three-way judgement** | Write "what the authors claim / what the evidence supports / my judgement" separately, and tag `[Original]`, `[Inference]`, `[External: source]`, `[Question]` | praise without critique |
| 3 | **Method first** | The method section is detailed enough to reproduce: inputs/outputs, key modules and equations, per-equation walkthrough and derivation outside the table, data splits, hyperparameters, compute, code/data availability | conclusions without methods |
| 4 | **Connect to yourself** | Write at least 2 relations to the reader's research (transferable methods, reusable data/metrics, pitfalls to avoid, next experiments) | forgotten after reading |

**Cases where you should not write a note**: only a title is available; only an abstract is available (→ produce an L1 quick-read card only, clearly marked); the PDF text layer is broken and no OCR has been run; the user asks for "a review" but no paper has been read. In these cases, state the limitation first, then downgrade the output, and **do not fill in imagined content**.

**Notes do not record usage scenarios**: neither the body nor the frontmatter may mention "report out, sharing, coursework, group discussion" or similar usage-scenario wording, and no reading purpose/goals are recorded; a note only presents paper content, evidence, and research judgement.

## When to Use

**Use for**: reading a single paper / preprint / lecture notes; writing or updating a reading note; comparing multiple papers; writing a literature synthesis note; finding research gaps; quickly deciding whether a paper deserves a deep read; reviewing the credibility of a paper's conclusions.

**Trigger phrases**:
- Chinese: 精读这篇论文、写文献笔记、读一下这篇、做个速读卡、对比这几篇、文献综述、找研究空白、这篇可信吗
- English: read this paper, literature note, paper summary, compare these papers, literature review, research gap, critical appraisal

**Do not use for**: ghost-writing a paper or a review report; fabricating citations, data, or experimental results; ordinary summarization requests unrelated to literature.

## Quick Start

Hand the prompts below directly to the Agent (replace the paths with actual files):

```text
# Single-paper deep read (L2 by default)
Read <paper.pdf> and write a complete paper reading note following the paper-reading-note standard
workflow; output to notes/<paper_id>.md and check the notes/ directory with this skill's check_note.py.

# Quick-read card only (L1, 10 minutes)
Make an L1 quick-read card for <paper.pdf> and decide whether it deserves a deep read.

# L3 deep note (equation walkthrough + Python reproduction)
Read <paper.pdf> and write it as L3: §4.3 explains the meaning and intellectual origin of each equation,
§7 restates the authors' limitations before adding further limitations, §11 gives runnable Python
reproduction code, and §12 verifies the derivations.

# Multi-paper comparison + synthesis
Turn these 6 papers on X in notes/ into a comparison matrix, then write a synthesis note:
common ground, disagreements, trends, research gaps; tag every conclusion with the papers it comes from.

# Update an existing note
Read notes/xxx.md and add §5 "failure cases" and §9 "research gaps", keeping my existing judgements and
dates.
```

## Input Capability Boundaries (Important)

| Input | What you can produce | How to handle it |
|-------|----------------------|------------------|
| PDF (with text layer) | L1 / L2 / L3 | prefer the text layer; read two-column PDFs column by column; keep equation numbers; cite figures/tables by Table/Fig number |
| PDF (scanned) | OCR first, then L1/L2 | if OCR quality is poor, produce L1 only and list the pages that "could not be read" |
| Abstract / web summary only | **L1 only** (`source_scope: abstract`), title marked "abstract only" | do not write method details, training setup, or numeric comparisons; run the self-check with `--abstract`, use `[Abstract]` locators |
| LaTeX / HTML full text | L1 / L2 / L3 | keep `\section` numbering, equation numbers, and table labels |
| Non-English paper | L1 / L2 / L3 | the note still uses English; keep key definitions/terms in the original language with a translation |
| Multiple papers | batch L1/L2 + comparison matrix + synthesis | create `notes/index.md` first, then the notes, then the matrix/synthesis |
| Existing note | incremental update | keep the original judgements and dates; mark new content "updated YYYY-MM-DD" |

**Version rule**: a preprint must record its version (e.g., v1/v7) and access date; methods/numbers may differ across versions, so do not overwrite old conclusions when updating — note "differences between v7 and v1".

## Reading Depth: L1 / L2 / L3

| Level | Name | Suggested time | Output length | Required sections | Evidence floor |
|-------|------|----------------|---------------|-------------------|----------------|
| L1 | quick-read card | 10–15 minutes | 300–600 words | 0,1,2,4,5,7 | ≥3 locators, ≥2 numbers in §5 |
| L2 | standard note (default) | 45–90 minutes | 1200–3500 words | 0–9 | ≥8 locators, ≥4 numbers in §5 |
| L3 | deep note | 2–4 hours | 3000–6000 words | 0–12 (plus reproduction plan and formula verification) | ≥15 locators, ≥6 numbers in §5 |

> **Abstract only**: L1 exception — ≥1 locator (`[Abstract]`), ≥1 number in §5, ablation/cost rows may be omitted; run the self-check with `--abstract`.
> Numbers are counted as decimals or percentages, deduplicated; repeating the same locator does not count.
> **Equation Walkthrough**: §4 of L2/L3 must contain `### 4.3 Equation Walkthrough`: first write `4.3.0 Derivation Chain` (how the equations connect and why each step introduces the next equation), then explain each equation's meaning, symbols, derivation motive, intellectual origin, role, and assumptions. Below each equation table (outside the table), write the "Derivation process": start from the derivation motive / intellectual origin and proceed step by step to the target equation; key equations stand alone with their original numbers. When a derivation is present, the table's "Derivation motive"/"Intellectual origin" rows may be condensed to one sentence.
> **L3 reproduction**: §11 "Reproduction Plan" must contain runnable Python code; §12 is "Formula and Derivation Verification".

**Automatic level selection**: L2 by default when the user does not specify; "quick look / help me triage / is it worth reading" → L1; "need to reproduce / write into a paper / dig into the equations" → L3; abstract only → force L1 and set `source_scope: abstract` in the frontmatter (run the self-check with `--abstract`).

## Workflow (Default L2)

### Step 0 — Create the Note Card (2 minutes)

1. Generate `paper_id`: `<first author surname><year>-<3–5 word topic slug>`, all lowercase; e.g. `vaswani2017-attention`.
2. Record: file path, source (journal/conference/arXiv/web page), version and access date, page count.
3. The reading purpose is only used **internally** to decide the emphasis and is not written into the note:
   - Archive → complete method and main results; limitations and discussion first;
   - Topic selection / finding gaps → related work, limitations, future work first; multi-paper comparison required;
   - Reproduction → hyperparameters, data splits, code/data links, compute first; go to L3.
4. If the purpose or output language is unclear, **ask at most once**: Chinese or English output? If there is no reply, continue with the defaults (L2, English, Markdown) without blocking.

### Step 1 — Structure Scan (5–10 minutes)

Read only six places: title, abstract, last paragraph of the introduction (contribution list), all figure/table captions, conclusion, appendix headings.

Produce a "three-sentence storyline" (each sentence ≤25 words):

- **Problem**: What does it solve, and under what setting?
- **Approach**: What is the core mechanism (not the model name)?
- **Result**: What are the key numbers (write "not reported" if there are none)?

Also list: must-read sections (method core, main results table, ablations, limitations), a figure/table inventory, and places with obvious doubts.
**For long papers**: read the abstract, the end of the introduction, the method, the main results table, and the conclusion first; related work and appendices as needed; record the sections you skipped in the note.
**If you cannot write the three-sentence storyline, you have not understood the paper yet: stop at L1 and state why.**

### Step 2 — Metadata Extraction

Extract according to the schema in `references/01-extraction-prompts.md`: title, authors, affiliations, year, venue, DOI/URL, keywords, code/data links, paper type (empirical/theoretical/survey/system). Output as YAML frontmatter (see "Output Contract").

### Step 3 — Four Extraction Tables (the core work of reading)

Fill in the four tables in order; every row except "my judgement" must have a locator:

1. **Problem table**: input/output definitions, assumptions, constraints, failure modes, differences from existing definitions.
2. **Method table**: overall architecture, key modules and equations, the connections/derivation chain between equations, per-equation meaning/symbols/motive/intellectual origin/role, loss function, training flow, hyperparameters, complexity, implementation details, reproducibility.
3. **Evidence table**: datasets (size/splits/preprocessing), baselines (strong baseline? same setting?), metrics (definition/direction), main results, ablations, significance/variance, failure cases, compute cost.
4. **Conclusion table**: three columns — what the authors claim / what the evidence supports / my judgement.

The required questions for each table, the "good enough" criteria, and the "sloppy-work signals" are in `references/01-extraction-prompts.md`.
**Do not skip the third table and jump to conclusions** — this is where the note's credibility comes from. The four tables are working drafts: condense them into an appendix, or delete them; rewrite the body according to the template rather than dumping the tables into the note.

### Step 4 — Critical Appraisal

Use the framework in `references/02-critical-appraisal.md`; **no scoring, no confidence ratings**; write in order:

- **7.1 Limitations acknowledged by the authors (restatement)**: weaknesses the authors explicitly acknowledge in limitations/discussion/assumptions/future work; paraphrase each and give a locator; do not put into this section anything the authors did not write.
- **7.2 Further limitations (my additions)**: at least 3 limitations the authors did not acknowledge; for each write "phenomenon + evidence + impact + how to verify"; do not repeat what 7.1 already restates.
- **7.3 Strengths and scope**: at least 2 specific strengths (which design solves which problem), and state the conditions under which the conclusions hold.
- **7.4 Threats to validity and reproducibility**: internal/external validity, metric validity, missing baselines/ablations, code/data/seeds.
- **7.5 Information gaps**: unreported, unverified, or unreadable content.

### Step 5 — Positioning (Comparison with the Closest Work)

Find 2–4 closest works: direct predecessors, concurrent competitors, later improvements. Prefer the paper's related work and reference list; verify citation relations online when possible; if not possible, mark "citation chain not verified" in the note, and **do not fabricate citations**. Use three-dimensional positioning: same/different problem, same/different method, same/different conclusion.

### Step 6 — Connections and Gaps

Answer 5 questions (§8): transferable methods, reusable data/metrics, pitfalls to avoid, relation to the reader's research question, the next experiment that can be run.

Write research gaps with four categories (§9): **problem gap / method gap / evidence gap / application gap**. Each gap must contain three elements: evidence (which result in which papers), why it remains unsolved, and a verifiable next step. Judging criteria are in `references/03-comparison-synthesis-gap.md`.

If the reader's research direction is unknown: write "to be confirmed", give 3 possible directions, and do not invent the reader's background.

### Step 7 — Assemble, Self-check, and Save

1. Assemble with the matching template in `templates/` (L1 → `speed-card-L1.md`; L2 → `note-L2.md`; L3 fills the `## 11. Reproduction Plan` (with runnable Python code) and `## 12. Formula and Derivation Verification` sections of the L2 template with `templates/reproduction-plan.md`).
2. Go through the "Quality Gate" checklist item by item (below).
3. Run this skill's `check_note.py` self-check: from any working directory run
   `python "<skill-dir>/scripts/check_note.py" notes/`
   (replace `<skill-dir>` with your actual install location; pass the directory directly and the script will check every note in it); deliver after it passes; if it fails, fix according to the report.
4. Save naming: `notes/<paper_id>.md`; in multi-paper mode also update `notes/index.md` and `notes/matrix.md`.

## Output Contract

### Files and Naming

```text
notes/
├── index.md                     # multi-paper index (grouped by topic/year, one line per paper)
├── matrix.md                    # comparison matrix (generated by scripts/build_matrix.py, then columns filled by hand)
├── synthesis-<topic>.md         # topic synthesis note
└── <paper_id>.md                # single-paper note (same naming for L1/L2/L3)
```

- The file name matches the frontmatter `paper_id`; on conflict add `-v2`.
- Output goes to `notes/` in the current workspace by default; if the user names a directory, use it.
- Default Markdown + YAML frontmatter (Obsidian reads it directly as properties).

### YAML Frontmatter Fields

| Field | Required | Example | Rule |
|-------|----------|---------|------|
| `paper_id` | yes | `vaswani2017-attention` | first author surname + year + slug, lowercase with hyphens |
| `title` | yes | `Attention Is All You Need` | original title, not translated (a translated title may go in parentheses) |
| `authors` | yes | `[Vaswani, Shazeer, ...]` | surname first; for >6 authors, first 3 + `et al.` |
| `affiliations` | no | `[Google Brain, ...]` | first affiliation first |
| `venue` | yes | `NeurIPS 2017` / `arXiv:1706.03762v7` | distinguish formal publication from preprint |
| `year` | yes | `2017` | publication year (first public year for preprints) |
| `doi` / `url` | no | `10.48550/arXiv.1706.03762` | prefer DOI when available |
| `keywords` | yes | `[Transformer, self-attention]` | 3–6 terms, prefer the paper's own words |
| `reading_level` | yes | `L2` | `L1` / `L2` / `L3` |
| `source_scope` | no | `full` | `full` / `abstract` (required for abstract-only) |
| `status` | yes | `done` | `draft` / `done` / `revisit` |
| `created` / `updated` | yes | `2026-10-21` | ISO date; when updating change only `updated` |
| `tags` | no | `[NLP, attention]` | 2–5 tags, for retrieval |

> Do not record reading purpose, usage scenarios, or confidence levels; these do not belong in the note.

### Section Structure and Writing Requirements (L2)

| # | Section | Required content | Common mistake |
|---|---------|------------------|----------------|
| Guide | field guide | what the field works on, the three-level problem (single oscillator / pairwise locking / population threshold), which level this paper adds; 2–3 paragraphs written for someone unfamiliar with the field | rewriting the abstract; not labelling a self-drawn figure as "drawn by me, not from the paper" |
| 0 | At a Glance | problem / approach / result / why it matters, each ≤40 words | translating the abstract; "result" with no numbers |
| 1 | Paper Information | metadata table + code/data links + paper type | missing version or code link |
| 2 | Background and Problem Definition | field status, concrete pain point, formal definition, assumptions, success criteria | long paraphrase of the introduction with no formalization |
| 3 | Related Work and Positioning | 2–4 closest works + three-dimensional positioning | listing citations without stating the differences |
| 4 | Method | architecture, key modules and equations, **4.3 Equation Walkthrough** (4.3.0 derivation chain + per-equation meaning/symbols/motive/intellectual origin/role/assumptions + derivation process outside the table), training details, complexity, implementation details | writing only "proposes method X"; copying equations without explaining them or connecting them |
| 5 | Experiments and Evidence | data table, main results table, ablations, failure cases, compute cost | copying only the best number, no baseline setting |
| 6 | Main Findings | three-column table: authors claim / evidence support / my judgement | treating the authors' conclusions as facts |
| 7 | Critical Appraisal | 7.1 restate the authors' limitations, 7.2 further limitations, 7.3 strengths and scope, 7.4 threats to validity and reproducibility, 7.5 information gaps | no scoring, no confidence ratings; paraphrasing the authors' limitations is not a critique |
| 8 | Relation to My Research | transferable / reusable / pitfalls / next experiments / further questions | empty phrases such as "very inspiring" |
| 9 | Research Gaps and Open Questions | four gap categories, each with three elements | treating "nobody has done it" as a gap |
| 10 | Key Quotations | 2–4 verbatim quotations + page numbers + translation (optional) | presenting a paraphrase as a quotation |
| Appendix | Appendix 1: Terminology | explain each reader-marked `<u>term</u>$^{[n]}$`: one-sentence definition, role in this paper, difference from adjacent concepts / common misconception; 2–4 sentences each | numbering inconsistent with the marks; copying sentences from the body |

L3 additions:

| # | Section | Required content |
|---|---------|------------------|
| 11 | Reproduction Plan | environment, parameter table, **runnable Python code**, run command, acceptance criteria, falsification conditions, known gaps |
| 12 | Formula and Derivation Verification | symbol/dimension table, step-by-step check, errata, remaining doubts |

L2/L3 notes must use these headings verbatim (the checker matches them exactly):

```text
## Guide: What This Field Is About
## 0. At a Glance
## 1. Paper Information
## 2. Background and Problem Definition
## 3. Related Work and Positioning
## 4. Method
### 4.1 Overall Architecture
### 4.2 Key Modules and Equations
### 4.3 Equation Walkthrough
#### 4.3.0 Derivation Chain (How the Equations Connect)
#### 4.3.1 <equation name>　[Eq. (x)]
### 4.4 Training and Implementation Details
### 4.5 Complexity and Assumptions
## 5. Experiments and Evidence
### 5.1 Data and Setup
### 5.2 Main Results
### 5.3 Ablations and Robustness
### 5.4 Failure Cases and Statistics
## 6. Main Findings
## 7. Critical Appraisal
### 7.1 Limitations Acknowledged by the Authors
### 7.2 Further Limitations (My Additions)
### 7.3 Strengths and Scope
### 7.4 Threats to Validity and Reproducibility
### 7.5 Information Gaps
## 8. Relation to My Research
## 9. Research Gaps and Open Questions
## 10. Key Quotations
## 11. Reproduction Plan
## 12. Formula and Derivation Verification
## Appendix 1: Terminology
```

### Writing and Formatting

- Default to English; at the first mention of a technical term give the original-language form when the paper is not in English, then use one consistent rendering; do not force-translate proper nouns.
- Conclusion first: the first sentence of each paragraph is the judgement, the evidence follows; one paragraph makes one point.
- Prefer tables and short lists; long paragraphs appear only where an argument needs them.
- Numbers and units as in the original; put a space between a number and its unit (`28.4 BLEU`, `8 P100 GPUs`), and between mixed-language tokens.
- No paper voice ("this paper aims to"), no marketing voice ("revolutionary breakthrough"), no empty evaluations ("works very well").
- Use LaTeX for equations; define symbols at first appearance; a symbol table may be added.
- **Formula citation closure**: when citing an original `Eq. (x)` / appendix equation number that has not appeared earlier in the note, write out the equation at the citation point (inline or display); for range citations (e.g., `Eq. (A4)–(A12)`) keep only the numbers already shown in the note.
- **Derivation outside the table**: below each equation table in 4.3 (outside the table), write the complete derivation — start from the "derivation motive / intellectual origin" and proceed step by step to the target equation; each step states which assumption or equation it uses, and the key step is a standalone equation with its original number. When a derivation is present, the table's "Derivation motive / Intellectual origin" may be condensed to one sentence.
- **Derivation register**: the "Derivation process" in 4.3 uses paper-style prose: advance with "suppose / let / from ... we obtain / therefore / hence / only then"; assumptions, substitutions, approximations, and conclusions each get their own sentence; key equations are standalone paragraphs with their original numbers. Do not use teaching-style step numbering, and do not write meta-discourse such as "the necessity of this step", "this is not a circular argument", or "it is worth noting that".
- **No skipped steps**: the "Derivation process" in 4.3 must give the original equation each step relies on and state the operation performed (substitution, first-order expansion, phase averaging, integration by parts, taking a limit); basic algebra such as transposition, collecting like terms, and multiplying both sides need not be expanded line by line. Do not write only "from Eq. (X) we obtain Eq. (Y)" without the basis and the operation. When citing appendix equations (e.g., (A1)(A3)(A8)), write the equation out first. Other sections may summarize; derivation blocks may not.
- **State the source of the starting expression**: when a derivation gives any initial expression, first state why it holds: a definition (the definition of phase/frequency, the definition of $M$), an established fact or conservation law (conservation of the number of oscillators), a prior result (name Eq. (x) or §x.x), or the paper's model assumption (linear response, single-population assumption). Do not make the reader guess; label the same expression only once, later citations need not repeat it.
- **Give composite expressions in layers**: when the starting expression has several terms, write the simplest case first (e.g., the free-running $d\phi/dt=1/T$), then explain why a term is added in the new setting (e.g., after stimulation is added the frequency increment is written as $\Delta f$, hence $d\phi/dt=1/T+\Delta f$). Do not drop only the final composite expression and add a one-line parenthetical explanation.
- **Give key claims a mechanism**: for claims such as "only if...", "necessarily...", "equivalent to...", "only ... is stable", do not just state the conclusion; write four steps: ① the claim itself; ② the minimal mechanism (1–3 equations: linearization, sign analysis, conservation, limiting case, keeping only the necessary steps); ③ one colloquial intuition (translate the symbols into "what happens if we push it forward"); ④ boundaries (when it fails, which term only corrects the value). Do not write a full proof and do not only state the conclusion; if the mechanism exceeds 3 equations or the intuition exceeds 2 sentences, it is usually already bloated. Definitions and transpositions are not covered. Linearization must write out the Taylor expansion (first-order term + remainder), not just "linearizing gives"; sign analysis must give the source of the inequality.
- **Reader marks and Appendix 1**: readers may mark unfamiliar technical terms in the md with `<u>term</u>$^{[n]}$`, meaning they want the Agent to explain them in Appendix 1. When such marks are present: ① keep the mark and the number; ② write `## Appendix 1: Terminology` at the end and, by number, give "one-sentence definition + role in this paper + difference from adjacent concepts / common misconception", 2–4 sentences each; ③ numbers must correspond one-to-one with the marks; a wrong number counts as an unfinished note; ④ the appendix does not count toward body length, but must not be used to smuggle body content into it.
- **Proofreading pass**: after writing the derivation, read it sentence by sentence: check for missing subjects, mismatched collocations, redundant components, logical repetition (e.g., splitting the same assumption into "both... and..."), and unclear reference; fix problems in place and do not leave them in the delivered draft.
- **Formula rendering**: no natural-language text inside math mode (no CJK inside `\text{}`; write prose outside the equation); display equations use multi-line `$$` (opening and closing `$$` on their own lines), not single-line `$$...$$`; inside tables use `\lvert...\rvert` instead of bare `|` to avoid breaking the table.
- **Field guide**: L2/L3 write `## Guide: What This Field Is About` before `## 0. At a Glance` (2–3 paragraphs): what the field studies, the three-level problem (how a single oscillator's phase is changed by stimulation / how two oscillators lock / whether a large population can synchronise, and what sets the threshold and population frequency), and which level this paper adds. Write for readers unfamiliar with the field; give background only, not the paper's conclusions; a self-drawn schematic may be added, and its caption must say "drawn by me, not from the paper".
- **Figure embedding**: crop original figures from the PDF, preferably together with the caption, making sure axes, curves, and annotations are complete; store them in `notes/figures/` and reference them with relative paths. One figure per line, centered (`<p align="center"><img src="..." width="620" style="background:#fff; padding:6px; border-radius:6px;"></p>`); do not squeeze several figures onto one line; captions give "figure number + page + one sentence". Label self-drawn figures separately from original figures, and say in the body which concept they support.

## Evidence Rules (Summary)

Full rules are in `references/04-evidence-and-style.md`; minimum requirements:

| Need | How to write | Note |
|------|--------------|------|
| subsection | `[§4.2]` | the paper's own numbering |
| page | `[p.7]` / `[PDF p.12]` | printed page and physical page kept separate |
| figure/table | `[Table 2]` / `[Fig. 3]` | use the paper's numbering |
| equation | `[Eq. (1)]` | with the number |
| line | `[L120–135]` | LaTeX source/text lines |
| version | `[arXiv v7, §3.1]` | preprints must carry a version |

Four tag types: `[Original]` the paper explicitly says it; `[Inference]` my reasoning; `[External: source]` knowledge outside the paper (a source is mandatory); `[Question]` to be verified. Tags and locators may be combined: `28.4 BLEU [Original][Table 2]`.

**Number discipline**: copy verbatim, do not re-convert; state relative/absolute improvements; different settings/metrics are not directly comparable; use "significant" only when a statistical test was actually run; write "not reported" when unreported, do not extrapolate.

## Multi-paper Mode

1. First make an L1 or L2 note for every paper (**never build a matrix from abstracts directly**).
2. Run this skill's `build_matrix.py`: `python "<skill-dir>/scripts/build_matrix.py" notes/ -o notes/matrix.md --csv notes/matrix.csv`; the script generates the automatic columns and leaves Delta / Evidence quality / Reproducibility / Relevance blank for manual filling.
3. Write the synthesis with `templates/synthesis.md`: problem lineage → method families and consensus → disagreements and their causes → trends → gaps and opportunities.
4. In the synthesis, tag every judgement with the number of source papers and the note links; distinguish "consensus (≥2 independent pieces of evidence) / controversy / single-paper finding".
5. Add citation chains (capability 11) and concept maps (capability 7) in an appendix as needed; formats are in `references/03-comparison-synthesis-gap.md`.

## Quality Gate (Tick Every Item Before Delivery)

- [ ] three-sentence storyline complete, "result" has numbers or explicitly says "not reported"
- [ ] locator count meets the bar (deduplicated; L1 ≥3 / L2 ≥8 / L3 ≥15)
- [ ] method section has at least 3 reproducible details (data splits, optimizer, hyperparameters, compute, etc.)
- [ ] **4.3 Equation Walkthrough**: `4.3.0 Derivation Chain` present first (how the equations connect, why the next equation is introduced), and every key equation has meaning, symbols, derivation motive, intellectual origin, role (L2/L3)
- [ ] **Formula citation closure**: every cited `Eq. (x)` / appendix number has a matching equation in the note; missing ones are written at the citation point; range citations (e.g., `A4–A12`) contain no numbers that are not shown
- [ ] **4.3 derivation outside the table**: a "Derivation process" below every equation table (step by step from motive/source to the target equation, key equation shown standalone); when present, the table's motive/source rows are condensed
- [ ] **Formula rendering**: no natural-language text inside math mode; display equations are multi-line `$$`; no bare `|` in tables (use `\lvert`/`\rvert`)
- [ ] **Derivation register**: the 4.3 derivation uses paper-style prose (no teaching-style numbering or meta-discourse; key equations standalone and numbered)
- [ ] **No skipped steps**: each step gives the original equation and the operation (substitution/expansion/averaging/integration/limit); "from X we obtain Y" alone is not enough; basic algebra such as transposition need not be expanded
- [ ] **Starting expression has a source**: every initial expression is labelled as one of definition / established fact / prior result / paper assumption; composite expressions are layered (simplest case first, then the added term)
- [ ] **Key claims have a mechanism**: "only if / necessarily / equivalent" conclusions each have a 1–3 equation minimal mechanism + one intuition + boundaries; not a full proof and not a bare conclusion; linearization has a Taylor expansion
- [ ] **Reader marks explained**: every `<u>term</u>$^{[n]}$` in the body has an entry in "Appendix 1: Terminology" with a matching number
- [ ] **Proofreading pass**: the 4.3 derivation and the body are read sentence by sentence; no missing subjects, mismatched collocations, redundant components, logical repetition, or unclear reference
- [ ] **Field guide**: L2/L3 have a field guide before §0 (with the three-level problem and this paper's position); self-drawn figures labelled "drawn by me, not from the paper"
- [ ] **Figures**: original figures cropped completely (axes/caption included); one figure per line, centered; captions have figure number and page
- [ ] §5 independent number count meets the bar (L1 ≥2 / L2 ≥4 / L3 ≥6) and is compared against the strongest baseline
- [ ] at least 1 ablation, robustness, or failure case discussed
- [ ] **7.1 restates the authors' acknowledged limitations + 7.2 has at least 3 further limitations** (each with evidence and impact)
- [ ] at least 2 connections to the reader's research (at least 1 actionable)
- [ ] at least 2 research gaps, each with evidence, cause, and a verifiable next step
- [ ] no `{{placeholders}}`, `TODO`, or "to be added" left behind
- [ ] unretrieved/unverified information listed in one place
- [ ] L3: §11 reproduction plan has **runnable Python code** (environment/parameters/run command/acceptance/falsification)
- [ ] `check_note.py` passes (pass the `notes/` directory)

If any item fails: **downgrade first (L2→L1) and state the gap; do not fabricate**. An L1 quick-read card only enforces the three-sentence storyline, the locator floor, the §5 number floor, a quick review of strengths/doubts, and the self-check; it is exempt from the 4.3 Equation Walkthrough, the full limitations analysis, research connections, and the gap list. Abstract-only cards relax further to ≥1 locator (`[Abstract]`) and ≥1 number in §5, with `--abstract` for the self-check.

## Anti-patterns

| Bad note | Good note |
|----------|-----------|
| "This paper proposes a new method with significantly better results." | "Replacing the recurrent structure with multi-head self-attention reaches 28.4 BLEU on WMT14 EN-DE, 2.0+ above the previous best (including ensembles) [Original][Table 2]." |
| "The authors ran many experiments." | "Main experiments: 2 translation tasks + 1 parsing task; Table 3 covers variants over head count, d_k, d_model, d_ff, dropout, positional encoding, etc." |
| "Copy the equation: $\mathrm{softmax}(QK^\top/\sqrt{d_k})V$." | "The equation uses the similarity between a query and all keys as softmax weights, then takes a weighted sum of the values; the division by $\sqrt{d_k}$ is needed because the dot-product variance grows with $d_k$ and softmax saturates; it is the common primitive of all three attention mechanisms in the paper [§3.2.1]." |
| "Each equation is explained on its own, so the reader cannot see how they connect." | "Start with the 4.3.0 derivation chain: assumption A gives Eq. (1), which solves X but leaves Y, so Eq. (2) is introduced to handle Y; combining the two gives Eq. (3), which finally yields conclusion Z." |
| "The limitation is that it was not tested on more datasets." | "External validity is limited: English-German/English-French plus WSJ parsing only; the O(n²) cost on long sequences was not tested, which the authors acknowledge in §4 but do not measure." |
| "The method is very innovative." | "It removes the constraint that sequences must be computed sequentially, and argues for the alternative with the complexity/path-length table (Table 1); this is problem-reframing-level innovation, not a module-level improvement." |
| "It is very inspiring for my research." | "Self-attention can be viewed as message passing on a complete graph, which transfers to interaction modelling in coupled-oscillator networks; the O(n²) cost and permutation symmetry must be solved first." |

## Mapping to the 12 Capabilities in the Introduction Article

| Capability in the introduction | Where this skill covers it |
|-------------------------------|----------------------------|
| 1 Metadata Extractor | Step 2 + frontmatter field table + the schema in `01` |
| 2 Abstract-to-Claim Summarizer | Step 1 three-sentence storyline + §0 At a Glance |
| 3 Methodology Extractor | Step 3 method table + §4 |
| 4 Result-and-Evidence Extractor | Step 3 evidence table + §5 |
| 5 Critical Appraisal | Step 4 + `02-critical-appraisal.md` |
| 6 Comparison Matrix | multi-paper mode + `build_matrix.py` + `03` |
| 7 Concept Mapping | the concept map spec in `03` (Mermaid) |
| 8 Research Gap Finder | Step 6 + §9 + the gap categories in `03` |
| 9 Reading Note Template | the five templates in `templates/` |
| 10 Personal Reflection | Step 6 + §8 |
| 11 Citation Graph | Step 5 + the citation chain spec in `03` |
| 12 Synthesis & Comparison | multi-paper mode + `templates/synthesis.md` |

## File Index

| File | When to read it |
|------|-----------------|
| `references/01-extraction-prompts.md` | every read; per-section question lists, the four extraction tables, copy-paste prompts for the 12 capabilities |
| `references/02-critical-appraisal.md` | when writing §7; restating the authors' limitations, classifying further limitations, threats to validity, red-flag checklist |
| `references/03-comparison-synthesis-gap.md` | multi-paper comparison, synthesis, gap analysis, concept maps, citation chains |
| `references/04-evidence-and-style.md` | while writing and self-checking; locators, tags, number discipline, wording ladder, citation format |
| `references/05-reproduction-code.md` | when writing L3 §11; numerical-simulation/training Python skeletons and the reproduction-code checklist |
| `templates/speed-card-L1.md` | L1 quick-read card |
| `templates/note-L2.md` | L2 standard note (with 4.3 Equation Walkthrough and derivation outside the table; L3 fills in §11/§12 there) |
| `templates/reproduction-plan.md` | L3 §11 reproduction plan (with Python code) |
| `templates/matrix.md` | multi-paper comparison matrix |
| `templates/synthesis.md` | synthesis note |
| `scripts/check_note.py` | pre-delivery self-check (supports directories and `--abstract`) |
| `scripts/build_matrix.py` | batch notes → comparison matrix |
| `examples/vaswani2017-attention.md` | completed L2 example (with equation walkthrough, limitations analysis, and research connections) |
