# Changelog

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
