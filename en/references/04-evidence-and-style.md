# 04 Evidence, Numbers and Writing Conventions

> This file defines "on what basis every sentence in a note stands". Read it when writing or self-checking; it maps one-to-one to the checks in `scripts/check_note.py`.

## 1. Locators (proving "where this sentence comes from")

| Type | Format | When to use |
|------|--------|-------------|
| Subsection | `[§4.2]` | the paper has numbered sections |
| Printed page | `[p.7]` | book/journal page numbers |
| Physical page | `[PDF p.12]` | PDF reader page (list alongside the printed page when they differ) |
| Table | `[Table 2]` | results tables, ablation tables |
| Figure | `[Fig. 3]` | architecture diagrams, curves, visualizations |
| Equation | `[Eq. (1)]` | key equations |
| Line numbers | `[L120–135]` | LaTeX source or plain text |
| Version | `[arXiv v7, §3.1]` | preprints must carry the version |
| Note | `[note:paper_id §5]` | referencing your own note in a synthesis |

**Rules**
- Locate to the smallest checkable unit: use §4.2 rather than §4.
- When one sentence has several sources, tag each: `[p1 §3][p2 Table 1]`.
- For figures/tables state which part: `[Table 2 bottom left]`, `[Fig. 4 right]`.
- Content that cannot be located does not go into the body; if it must be mentioned, put it in "information gaps".
- **Equation-number closure**: when citing `[Eq. (x)]`, if the equation has not yet appeared in the note, write it out at the point of citation. For range citations (e.g. `Eq. (A4)–(A12)`), keep only the numbers already shown in the note.

## 2. The Four Source Tags (distinguishing knowledge sources)

| Tag | Meaning | Example |
|-----|---------|---------|
| `[Original]` | the paper explicitly says it (paraphrase or quotation) | `28.4 BLEU [Original][Table 2]` |
| `[Inference]` | my reasoning from the evidence, not stated directly in the paper | `this shows the authors value parallelism more [Inference][§1]` |
| `[External: source]` | knowledge outside the paper; a source is mandatory | `later BERT/GPT reused this architecture [External: Devlin et al. 2019]` |
| `[Question]` | not understood / to be verified | `were the baselines tuned under the same budget? [Question]` |

- Tags combine with locators in the order: `content [tag][locator]`.
- When unsure whether something is original or inferred, treat it as `[Inference]`.
- External knowledge without a source: delete it or turn it into `[Question]`.

## 3. Quotation Rules

1. **Verbatim**: do not reword and do not drop words inside quotation marks; use `……` for omissions, and make sure the meaning is unchanged.
2. **Short**: at most 2 sentences per quotation; from long paragraphs quote only the key sentence.
3. **Located**: every quotation gets a page/section.
4. **Translation label**: when quoting a non-English paper, put the English translation after the quotation and mark it "(trans.)"; keep technical terms in their original language.
5. **Do not pass a paraphrase off as a quotation**: paraphrases use `[Original]` but no quotation marks.

## 4. Number Discipline

| Rule | Bad example | Good example |
|------|-------------|--------------|
| Copy verbatim | "about 47% improvement" (computed by force from 28.4 and 41.8, two different tasks) | `EN-DE 28.4 BLEU [Table 2]` |
| Separate relative/absolute | "2× improvement" (denominator unstated) | `12.5% relative improvement (absolute +4.6)` |
| Do not compare across settings | "A's 90.1 > B's 88.0" (different datasets/metrics) | `same dataset and metric: A 90.1 vs B 88.0` |
| Keep precision | "about 28" (original 28.4) | `28.4` |
| Do not derive unreported values | "about 3 days" (not given in the paper) | `training time not reported` |
| "Significant" needs a test | "significantly better" (no test) | `improves by 2.0 BLEU (no significance test reported)` |
| State units/metrics in full | "accuracy 95" | `top-1 accuracy 95.0% (ImageNet)` |
| Distinguish mean from best | "reaches 90" (actually best-of-5) | `best-of-5 90.2; mean 88.7±0.6` |

**Three questions for every number**: which dataset/metric/setting does it correspond to? Is it a mean or a best value? Is there variance/a test?

## 5. Wording Ladder (choose words by strength of evidence)

| Evidence strength | Allowed wording | Forbidden wording |
|-------------------|-----------------|-------------------|
| Multiple datasets + multiple seeds + test | proves, establishes | — |
| Multiple datasets, no test | indicates, shows | proves |
| Single dataset, with control | reports, outperforms on X | generally outperforms |
| Single run/no control | reported one result | significantly improves |
| Author's claim only, no evidence | the authors claim | the fact is |
| My reasoning | I think, may, suspect | obviously |

**Downgrading examples**
- Original: `Our method significantly outperforms all baselines.`
- Bad: `The method significantly outperforms all baselines.` (copies the strength)
- Good: `The authors report 2.0+ BLEU above the previous best (including ensembles) on WMT14 EN-DE [Original][Table 2]; no significance test is reported [Question].`

## 6. Banned Expressions and Replacements

| Banned (unsupported boilerplate) | Replacement |
|----------------------------------|-------------|
| works very well / excellent performance | give the metric, dataset and comparison object |
| very innovative / disruptive | say which work it is relative to and which assumption it changed |
| of great significance | say whom it affects and which decision it affects |
| extensive experiments | say how many datasets and how many ablation groups |
| the authors did an in-depth analysis | say what exactly was analyzed and what was concluded |
| well known / obviously | cite it or delete it |
| this paper aims to / the author believes (paper-speak) | state it directly |

## 7. Note Writing Style

- **Conclusion first**: the first sentence of each paragraph is the judgment; evidence and qualifications follow.
- **One claim per paragraph**: split long paragraphs; use lists for parallel facts, not for argumentation.
- **Consistent terminology**: use one term for one concept throughout; on first use give the full form plus abbreviation, then use one form only.
- **No connective padding**: avoid chains of "moreover/furthermore/at the same time"; use logical connectives (because/but/therefore).
- **Numbers and units**: put a space between a number and a word unit; keep the percent sign tight against the number; use `–` for ranges.
- **Equations**: LaTeX; define symbols on first occurrence; for key equations write "meaning, symbols, derivation motive, intellectual origin, role, assumptions", never just copy the equation; when citing the paper's number, if the equation has not yet appeared in the note, write it out at the citation; below each equation table (outside the table) write the "derivation process" (from motive/origin step by step to the target expression); once the derivation is written out, the motive/origin in the table can be condensed.
- **Formula chain**: in 4.3 write the 4.3.0 derivation chain first (where it starts, why each step is introduced, what the next equation picks up), then expand equation by equation; do not just give a list of formulas.
- **Formula rendering**: no CJK inside math mode (`\text{}` must not contain CJK; put natural-language text outside the formula); use multi-line `$$` for display equations (`$$` on its own line); use `\lvert...\rvert` instead of a bare `|` inside tables; if rendering fails the viewer falls back to raw source, so check.
- **Derivation register**: write 4.3 derivations as paper-style statements ("Let / Set / From … we obtain / hence / therefore / only if"), without pedagogical step numbering and without meta-commentary such as "the necessity of this step" or "this does not constitute circular reasoning"; key equations get their own paragraph and keep the paper's number.
- **No skipped steps in derivations**: give the source equation each step relies on and state the operation performed (substitution/expansion/averaging/integration by parts/limit); basic algebra such as moving terms, combining like terms and multiplying both sides need not be expanded; "from Eq. X we get Eq. Y" without stating the basis is forbidden. Show an appendix equation before citing it. Other sections may summarize; derivation blocks may not.
- **Label the source of the starting expression**: state whether it is a definition, an accepted fact/conservation law, a previous conclusion (Eq. x), or a paper assumption; label once per equation, no need to repeat later. For composite expressions write the simplest case first, then explain why the added term is introduced.
- **Key claims get a mechanism**: for judgments such as "only if …", "necessarily", "equivalent to", "only … is stable", write "judgment → minimal mechanism in 1–3 equations (linearization/sign analysis/conservation/limit) → one intuition → boundary". Do not write a full proof, and do not only state the conclusion. For linearization, write the Taylor expansion (first-order term + remainder); do not write only "linearizing gives".
- **Reader markers and Appendix 1**: when readers mark unfamiliar terms as `<u>term</u>$^{[n]}$`, keep the marks and numbering, and explain them at the end under `## Appendix 1: Terminology` (definition + role in this paper + distinction from adjacent concepts), 2–4 sentences each; the appendix does not count toward body length.
- **Proofreading pass**: after writing a derivation, read it sentence by sentence for missing subjects, wrong collocation, redundancy, logical repetition (e.g. splitting one assumption into "both … and …") and unclear references; fix on the spot.
- **Field guide**: for L2/L3 write 2–3 paragraphs before §0 on "what the field is doing": the research object and typical phenomena, the three layers of problems (single-oscillator PRC / pairwise locking / population threshold and frequency), and which layer this paper fills. Background only, no conclusions from this paper; a hand-drawn schematic is optional, captioned "drawn by the note author, not from the paper".
- **Embedding figures**: crop original figures from the PDF (preferably with the caption, keeping axes and labels complete), save to `notes/figures/`, use relative paths; one figure per line, centered (`<p align="center"><img …></p>`), do not squeeze several figures onto one line; captions give figure number + page + one sentence; mark self-drawn figures separately from original ones.
- **Do not write "the paper says"**: state the content; the locator carries attribution.

## 8. Good vs. Bad Sentences

| Bad | Good |
|-----|------|
| The authors propose a new framework that achieves good results. | Replacing recurrence with stacked pure attention reaches 28.4 BLEU on WMT14 EN-DE, 2.0+ above the previous best (including ensembles) [Original][Table 2]. |
| The experiments are very thorough. | 2 translation tasks + 1 parsing task; Table 3 covers variants of head count, d_k, d_model, d_ff, dropout and positional encoding. |
| The attention formula is given. | Scaled dot-product attention uses $\mathrm{softmax}(QK^\top/\sqrt{d_k})V$ to normalize query-key similarities into weights and then takes a weighted sum of the values; dividing by $\sqrt{d_k}$ is needed because the dot-product variance grows with $d_k$, so softmax saturates [§3.2.1]. |
| Five equations are listed, each explained separately. | Starting from assumption A we obtain Eq. (1); it solves X but leaves Y; hence Eq. (2) is introduced to handle Y; combining the two gives Eq. (3), and finally conclusion Z. This chain shows why no intermediate step can be skipped. |
| The limitation of the method is that it does not consider more scenarios. | External validity is limited: only EN-DE/EN-FR + WSJ; the O(n²) cost on long sequences was not measured — the authors acknowledge this in §4 but do not test it. |
| This is very inspiring for our research. | Self-attention can be seen as message passing on a fully connected graph, and can be transferred to modeling interactions in coupled-oscillator networks (see section 8). |
| This work solves the problem for the first time. | The authors claim "the first sequence transduction model based entirely on attention" [Original][§2]; the claim gives no search scope [Question]. |

## 9. Citation Format

In-text: `Author (year)` or `[Author, year]`; several at one point: `[Vaswani et al., 2017; Devlin et al., 2019]`.

Reference entry (choose one and use it consistently):

```text
Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention Is All You Need.
  Advances in Neural Information Processing Systems, 30. arXiv:1706.03762v7.
  https://arxiv.org/abs/1706.03762
```

Rules:
- Preprints: give the version and access date; prefer the formal version once it is published.
- Give the DOI when available; for web pages give the URL + access date.
- Do not cite literature you have not read; mark second-hand citations as "cited in".

## 10. Pre-Delivery Quick Check

- [ ] every key claim has a locator
- [ ] the four tags (original/inference/external/question) are used correctly
- [ ] no unlabelled "significant/proves/first"
- [ ] numeric precision, units, datasets and metrics are complete
- [ ] no direct comparison across settings
- [ ] quotations are verbatim, with page numbers, in a consistent format
- [ ] every equation table has a derivation outside the table (motive/origin → steps → target expression)
- [ ] 4.3 derivations are paper-style statements (no pedagogical numbering or meta-commentary)
- [ ] 4.3 derivations have no skipped steps (each step has the source equation + the operation; basic algebra is not expanded mechanically)
- [ ] starting expressions in derivations are labelled by source (definition/accepted fact/previous conclusion/paper assumption); composite expressions give the simplest case first
- [ ] "only/necessarily/equivalent" judgments have a minimal mechanism + one intuition + boundary
- [ ] every `<u>term</u>$^{[n]}$` marker in the body has a matching entry in Appendix 1 with the same number
- [ ] derivations and body have been proofread (subject/collocation/redundancy/logical repetition/reference)
- [ ] L2/L3 have a field guide (before §0, 2–3 paragraphs, three layers of problems and this paper's position)
- [ ] original figures are complete (with axes/captions), one figure per line centered, captions have figure number and page; self-drawn figures are labelled
- [ ] no CJK inside math mode; display equations use multi-line `$$`; no bare `|` in tables
- [ ] no empty phrases like "good results/strong novelty"
