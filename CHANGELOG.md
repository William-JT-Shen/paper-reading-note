# Changelog

## 1.4.18 — 2026-10-25

- Chinese and English editions synced to 1.4.18.
- Added the optional WeChat cover style "deep navy + gold phase circle": 900×383 main cover and 600×600 square cover; spec in `references/06-cover-style.md`.
- 1.4.17: §8 title is "Inspirations" (Chinese: 启发), not "Relation to My Research".
- 1.4.16: no bare numbered citations; important equations display, minor ones inline.
- 1.4.15: mechanism/conclusion derivations restate a cited equation even at short distance.
- 1.4.14: cross-section formula citations are restated as display math at first citation.
- 1.4.12: symbol-semantics check (definition page/type/normalization/dimension).
- 1.4.11: appendix first citations of numbered equations are expanded as display math.
- 1.4.10: necessary derivations take priority over the L3 length cap; report any overrun.
- 1.4.9: a formula's first appearance states which equations/approximation produce it.
- 1.4.8: substitution/differentiation/assignment/subtraction show intermediate results; "take X = …" states its basis.
- 1.4.7: new assumptions/ansätze are declared before the formula.
- 1.4.6: numbered equations first appear as display math with numbers.
- 1.4.5: symbol table goes after the field guide and before §0.
- 1.4.4: appendix derivations use display math.
- 1.4.3: underline only text; formulas stay outside `<u>`; appendix steps restate the target equation.
- 1.4.2: "not … but …" constructions are banned.
- 1.4.1: reader marks may point to derivation steps; Appendix 1 becomes "Terminology and Derivation Steps".
- 1.4.0: crop-check each figure edge; explain before editing files; length budget with separate counts (body / captions / appendix).

## 1.3.11 — 2026-10-22

- Reader-marked terms: `<u>term</u>$^{[n]}$` must be explained in `Appendix 1: Terminology` (definition, role, contrast); appendix does not count toward note length. The checker verifies that marks and entries match.
- 1.3.10: when a key claim uses linearization, the Taylor expansion (first-order term + remainder) must be written out.
- 1.3.9: key claims ("only if", "necessarily", "equivalent to") need a minimal mechanism (1–3 equations), one plain-language intuition, and the boundary where it fails.
- 1.3.8: composite starting expressions are layered: simplest case first (e.g. free-running `dφ/dt = 1/T`), then explain each added term (e.g. `Δf`).
- 1.3.7: every starting expression states its source: definition, established fact/conservation law, earlier result (Eq. x), or paper assumption.
- 1.3.6: clarified "no skipped steps": state the source equation and operation (substitution/expansion/averaging/integration/limit); basic algebra (moving terms, combining like terms) need not be expanded.
- 1.3.5: derivation blocks may not jump steps; appendix equations must be shown before being cited.
- 1.3.4: L2/L3 add a field guide before §0; original figures are cropped into `notes/figures/`, one figure per line, centered, captioned with figure number and page.
- 1.3.3: 4.3 derivations use paper-style prose (set/let/from…we get/therefore), no teaching-style step numbers or meta-commentary; proofreading pass for grammar.
- 1.3.2: each equation table is followed by a derivation process outside the table; formula-rendering rules (no CJK inside math, multi-line `$$`, `\lvert` in tables).
- 1.3.1: formula citation closure: if an equation is cited but not yet shown, write it at the citation site; range citations include only displayed equation numbers.

## 1.3.0 — 2026-10-21

- 4.3 gains `4.3.0 Derivation Chain`: goal, starting point, one-sentence chain, step table, optional dependency graph, alternative route.
- Each equation gains `Derivation motive` and a stronger `Relation to adjacent equations` field.

## 1.2.0 — 2026-10-21

- Section 7 restructured into `7.1 Limitations Acknowledged by the Authors` + `7.2 Further Limitations (My Additions)`; no 8-dimension scoring and no confidence rating.
- L3 sections renumbered: 11 Reproduction Plan (with runnable Python), 12 Formula and Derivation Verification.
- Removed review cards / todo section and all usage-scenario wording (meeting, report, course, etc.).
- Formula chain layer added to 4.3.

## 1.1.0 — 2026-10-21

- `authors` and `keywords` are checked; locators are deduplicated; §5 result numbers are deduplicated decimals/percentages; §5 requires baseline/ablation keywords.
- Abstract-only mode (`source_scope: abstract`, `--abstract`) with relaxed thresholds; `[Abstract]` locators.
- Matrix links are relative to the output directory; four manual columns left empty.
- Path errors return exit code 2.

## 1.0.0 — 2026-10-21

- Initial release: L1/L2/L3, evidence locators, four source tags, extraction tables, critical appraisal, comparison matrix, synthesis, research gaps, templates, self-check and matrix scripts.
