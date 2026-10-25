---
paper_id: "{{firstauthor}}{{year}}-{{slug}}"
title: "{{paper title}}"
authors: ["{{Author 1}}", "{{Author 2}}"]
affiliations: ["{{Affiliation}}"]
venue: "{{venue / arXiv:xxxx.xxxxxvN}}"
year: {{year}}
doi: ""
url: ""
keywords: ["{{kw1}}", "{{kw2}}"]
reading_level: L2
source_scope: full
status: draft
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
tags: []
---

# {{title}}

> Version: {{...}} | Reading date: {{YYYY-MM-DD}}

> **Rule reminders (1.4.x):** symbol table after the guide and before §0; numbered equations first appear as display math with numbers; state new assumptions before the formula; show intermediate results for substitution/differentiation/assignment/subtraction; at a formula's first appearance state which equations or approximation produce it; when the appendix cites a numbered equation, write it out as display math; do not leave bare "(c)"/"(A10)"; §8 is titled "Inspirations".

## Guide: What This Field Is About

> Written for readers unfamiliar with the field; background only, no conclusions from this paper.

{{The research object of the field and a few typical phenomena, 2–3 sentences.}}

{{The field's problem has three levels: how a single oscillator's phase is changed by stimulation (PRC); how two oscillators lock; whether a large population can synchronise, and what determines the threshold and the population frequency.}}

{{Which level this paper adds, and how it relates to the work before and after it.}}

<p align="center"><img src="figures/{{field-map.png}}" width="680" style="background:#fff; padding:6px; border-radius:6px;"></p>

*Figure 0 (self-drawn schematic, not from the paper): {{one sentence on which concept this figure supports.}}*

## 0. At a Glance

- **Problem**: {{...}}
- **Approach**: {{...}}
- **Result**: {{key numbers + dataset}}
- **Why it matters**: {{...}} [Inference]

## 1. Paper Information

| Item | Content |
|------|---------|
| Authors / affiliations | {{...}} |
| Venue / year | {{...}} |
| DOI / link | {{...}} |
| Code / data | {{... or not reported}} |
| Paper type | {{empirical / theoretical / survey / system}} |
| Keywords | {{...}} |

## 2. Background and Problem Definition

- **State of the field**: {{2–3 sentences, with locators}}
- **Concrete pain point**: {{why existing methods are insufficient, at the mechanism level}}
- **Problem definition**: {{inputs/outputs/supervision signal; the formal definition}}
- **Key assumptions**: {{1–3; what happens if an assumption fails}}
- **Success criteria**: {{which metric/condition the authors use to decide it is solved}}

## 3. Related Work and Positioning

| Closest work | Relation | Difference from this paper |
|--------------|----------|----------------------------|
| {{...}} | predecessor / competitor / follow-up | {{...}} |

**Three-dimensional positioning**: problem {{same/different}}, method {{same/different}}, conclusion {{same/different}}.
**Citation chain**: {{predecessors ...; follow-ups ... (note if not verified)}}

## 4. Method

### 4.1 Overall Architecture

{{Modules and data flow; figures/equations may be added; with locators}}

### 4.2 Key Modules and Equations

{{What problem each module solves; list the key equations; define the symbols first and expand the details in 4.3}}

### 4.3 Equation Walkthrough

> Write in two layers; both are required:
> ① **4.3.0 Derivation Chain**: first make clear "what the target is → which assumption/equation we start from → why each step must introduce the next equation → what we obtain → why the next step can follow";
> ② **From 4.3.1 onward, expand each equation**: meaning, symbols, derivation motive, intellectual origin, role, assumptions/approximations, relation to adjacent equations.
> When there are many equations, expand at least 2 core equations; cover the rest in the symbol table or an appendix.
> **Formula number closure**: at a `[Eq. (x)]` citation, if the equation has not appeared in the note, write it out; range citations keep only the numbers already shown.
> **Derivation outside the table**: below each equation table (outside the table), write the full derivation: from the "derivation motive / intellectual origin", step by step to the target equation; when a derivation is present, the table's "derivation motive / intellectual origin" rows may be condensed to one sentence.
> **Derivation register**: use paper-style prose (suppose / let / from ... we obtain / therefore / hence); no teaching-style step numbering, and no self-justifying meta-commentary; key equations are standalone paragraphs with their original numbers.
> **No skipped steps**: give the original equation each step relies on and state the operation performed (substitution/expansion/averaging/integration by parts/taking a limit); basic algebra such as transposition and collecting like terms need not be expanded; do not write "from Eq. (x) we obtain Eq. (y)".
> **Starting expression labelled by source**: every initial expression is labelled as a definition, an established fact/conservation law, a prior result (Eq. x), or a paper assumption; composite expressions give the simplest case first, then the added term.
> **Key claims get a mechanism**: conclusion → 1–3 equation minimal mechanism → one intuition → boundaries; not a full proof, and not a bare conclusion; linearization writes out the Taylor expansion (first-order term + remainder).
> **Proofreading pass**: after writing, read every sentence for subject, collocation, redundancy, logical repetition, and reference; fix problems in place.
> **Figures**: crop original figures from the PDF (preferably with the caption) and store them in `notes/figures/`; one figure per line, centered; captions with figure number and page; self-drawn figures labelled "drawn by me, not from the paper".
> **Formula rendering**: no CJK inside `\text{}` (write natural language outside the equation); display equations use multi-line `$$` (each `$$` on its own line); inside tables use `\lvert...\rvert` instead of bare `|`.

#### 4.3.0 Derivation Chain (How the Equations Connect)

**Goal**: {{the conclusion/quantity to obtain in the end}}

**Starting point**: {{which assumption, definition, or known equation we start from}}

**One-line through-line**: {{start from X; because Y is needed, introduce Eq. (1); it leaves problem Z, so introduce (2)... finally obtain (n)}}

| Step | Starting point (previous equation / assumption) | What this step solves | Resulting equation | What it provides for the next step |
|------|-------------------------------------------------|-----------------------|--------------------|------------------------------------|
| 1 | {{...}} | {{...}} | {{Eq. (1)}} | {{...}} |
| 2 | {{...}} | {{...}} | {{Eq. (2)}} | {{...}} |
| 3 | {{...}} | {{...}} | {{...}} | {{...}} |

**Dependency graph (optional)**:

```mermaid
graph LR
  A[Start: ...] --> B[Eq. (1): ...]
  B --> C[Eq. (2): ...]
  C --> D[Final conclusion: ...]
```

**What if we took another derivation route?**: {{the authors could have..., but chose..., because...; this determines the form of the equations}}

#### 4.3.1 {{equation number and form}}　[Eq. ({{x}})]

| Item | Content |
|------|---------|
| Equation | {{...}} |
| Meaning | {{what this equation computes; the physical/statistical meaning of the output}} |
| Symbols | {{definition, dimension, and range of each symbol}} |
| Derivation motive | {{what problem the previous equation/question left; why this equation must be introduced}} |
| Intellectual origin | {{why the authors write it this way; which assumption, analogy, prior work, or derivation motive it comes from}} |
| Role in the method | {{which link of the model/proof chain it is; what breaks if it is removed}} |
| Assumptions / approximations | {{conditions of validity, approximation error, consequences of failure}} |
| Relation to adjacent equations | {{which equation it is derived from / substituted into / provides input for; where the chain breaks if it is deleted}} |

**Derivation process ({{Eq. (x)}} → {{Eq. (y)}})**

{{Source of the starting expression: definition / established fact / prior result Eq. (x) / paper assumption; if it is composite, write the simplest case first (e.g. free running), then explain why the added term is present (e.g. $+\Delta f$).}}

{{Suppose ... . From Eq. (x), ..., we obtain

$$
{{key equation 1}}
$$

{{Intermediate step: cite which original equation is used and state the operation performed (substitution/expansion/averaging/integration by parts); basic algebra such as transposition need not be expanded; write the resulting equation:

$$
{{intermediate equation}}
$$

Therefore, ... . Substituting ... gives Eq. (y).}}

> After writing, read it once: first check for skipped steps (every "we obtain" must have a basis before it), then check the language (subject, collocation, redundancy, logical repetition, reference).
> For claims such as "only ... is stable / necessarily / equivalent to": write "claim → minimal mechanism (1–3 equations) → one intuition → boundaries"; do not only state the conclusion.

#### 4.3.2 {{equation number and form}}　[Eq. ({{x}})]

{{Same as 4.3.1: the field table (Equation / Meaning / Symbols / Derivation motive / Intellectual origin / Role in the method / Assumptions / approximations / Relation to adjacent equations) plus the "Derivation process" block below the table.}}

### 4.4 Training and Implementation Details

| Item | Content | Locator |
|------|---------|---------|
| Data and splits | {{...}} | {{...}} |
| Optimizer / learning rate | {{...}} | {{...}} |
| batch / steps / epoch | {{...}} | {{...}} |
| Regularization / initialization | {{...}} | {{...}} |
| Hardware / duration | {{...}} | {{...}} |
| Code / data availability | {{...}} | {{...}} |

### 4.5 Complexity and Assumptions

{{Time/space complexity; how it grows with scale; strong assumptions and failure conditions}}

## 5. Experiments and Evidence

### 5.1 Data and Setup

| Dataset | Size / splits | Preprocessing | Locator |
|---------|---------------|---------------|---------|
| {{...}} | {{...}} | {{...}} | {{...}} |

### 5.2 Main Results

| Dataset / setting | Metric | This paper | Strongest baseline | Difference (relative / absolute) | Locator |
|-------------------|--------|------------|--------------------|----------------------------------|---------|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{[Table 2]}} |

### 5.3 Ablations and Robustness

| What is removed or changed | Effect | Explanation | Locator |
|----------------------------|--------|-------------|---------|
| {{...}} | {{...}} | {{...}} | {{[Table 3]}} |

### 5.4 Failure Cases and Statistics

- **Failure cases**: {{...}}
- **Variance / seeds / confidence intervals**: {{... or not reported}}
- **Significance test**: {{... or not reported}}
- **Compute cost**: {{...}}

## 6. Main Findings

| Authors claim | Strength of evidence | My judgement |
|---------------|----------------------|--------------|
| {{...}} | strong/moderate/weak: {{reason + locator}} | {{...}} |
| {{...}} | {{...}} | {{...}} |

## 7. Critical Appraisal

### 7.1 Limitations Acknowledged by the Authors

> Only content the authors explicitly state in limitations/discussion/assumptions/future work; do not put anything they did not write here.

| # | Limitation acknowledged by the authors (paraphrased) | Locator | How the authors qualify/explain it |
|---|------------------------------------------------------|---------|------------------------------------|
| 1 | {{...}} | {{[§x]}} | {{...}} |
| 2 | {{...}} | {{[p.x]}} | {{...}} |

### 7.2 Further Limitations (My Additions)

> Problems the authors did not acknowledge but that can be pointed out from the evidence/design/assumptions/external validity/reproducibility; do not repeat 7.1.

1. **{{limitation}}**: {{phenomenon/evidence (with locator)}}; impact: {{impact on the conclusions}}; how to verify: {{checkable approach}}.
2. **{{limitation}}**: {{...}}
3. **{{limitation}}**: {{...}}

### 7.3 Strengths and Scope

- **Specific strengths**: {{≥2 items; which design solves which problem}}
- **Scope**: {{under what conditions the conclusions hold; when they no longer hold}}
- **Do not misuse**: {{situations in which it cannot be applied directly}}

### 7.4 Threats to Validity and Reproducibility

- **Internal validity**: {{data leakage/confounding/asymmetric tuning/implementation differences}}
- **External validity**: {{data/domain/scale/task boundaries}}
- **Construct validity**: {{whether the metric measures the intended target}}
- **Reproducibility**: {{code/data/seeds/preprocessing/compute}}

### 7.5 Information Gaps

- {{unreported / unverified / unreadable content}}

## 8. Inspirations

- **Transferable methods**: {{specific mechanism + conditions under which it is transferable}}
- **Reusable data / metrics / baselines**: {{...}}
- **Pitfalls to avoid**: {{...}}
- **The single most important idea**: {{...}}
- **Next step — executable experiment**: {{hypothesis + data + metric + expectation}}
- **Follow-up questions**: {{1–3}} (academic questions only, no usage scenarios)

## 9. Research Gaps and Open Questions

| Gap type | Gap description | Evidence | Why it is unsolved | Verifiable next step |
|----------|-----------------|----------|--------------------|----------------------|
| {{problem gap / method gap / evidence gap / application gap}} | {{...}} | {{[paper §x]}} | {{...}} | {{...}} |

- **To follow up**: {{[Question] 1–3}}

## 10. Key Quotations

1. > "{{verbatim quotation}}" [p.{{x}}] (translation: {{...}})
2. > "{{...}}" [§{{x}}]

## 11. Reproduction Plan

> **L3 only.** Replace this stub with the full section from `templates/reproduction-plan.md`: environment, parameter table, runnable Python code, run command, acceptance criteria, falsification conditions, known gaps. L2 notes delete §11 and §12.

## 12. Formula and Derivation Verification

> **L3 only.** Replace this stub with the full section from `templates/reproduction-plan.md`: symbol/dimension table, step-by-step check, errata, remaining doubts. L2 notes delete §11 and §12.

## Appendix 1: Terminology

> Terms in the body marked with an underline and $^{[n]}$ are explained below by number.

**[1] {{term}}**: {{one-sentence definition}}. {{role in this paper}}. {{difference from adjacent concepts or common misconception}}.

**[2] {{term}}**: {{...}}
