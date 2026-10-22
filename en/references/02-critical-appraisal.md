# 02 Critical Appraisal: Author Limitations, Further Limitations and Threats to Validity

> Goal: first restate accurately the limitations the authors themselves acknowledge, then add further limitations the authors did not mention.
> This skill does not score a paper on 8 dimensions and gives no confidence grades; write only specific, checkable judgments.

## 1. Two Kinds of Limitations: Separate Them First

| Type | Definition | Source | How to write |
|------|------------|--------|--------------|
| **Limitations acknowledged by the authors** | shortcomings, boundaries, failure conditions or future work that the authors explicitly acknowledge | Discussion / Conclusion / Limitation / assumptions paragraph / appendix footnote | restate item by item, preserving the authors' meaning, with locators |
| **Further limitations** | problems the authors did not acknowledge but that can be pointed out from evidence/design/assumptions/external validity/reproducibility | my analysis | each with evidence, impact and verification method |

**The order cannot be reversed**: restate the authors first, then write your additions. Paraphrasing the limitations the authors already wrote is not a critique.

**Three principles**
1. Every limitation carries a locator (`[§4]`, `[p.24]`, `[Table 3]`); adjectives alone are not enough.
2. Distinguish a "defect" from a "reasonable trade-off": simplifications forced by the data/compute available at the time are not necessarily defects.
3. Do not treat "did not do X" as a limitation unless X is standard practice in the field or necessary for the conclusion.

## 2. Find the Limitations the Authors Acknowledge

Scan the following locations item by item:

- **Discussion / Conclusion**: `limitation`, `future work`, `we do not`, `cannot`, `remains`.
- **Assumptions paragraph**: when authors state assumptions they often also state what happens if they fail.
- **Experimental setup**: notes such as "verified only under setting X", "Y not tested".
- **Appendix / footnotes**: biases and failure cases acknowledged in supplementary experiments.
- **Abstract / end of introduction**: sometimes qualified with phrases such as "in this setting".

Record them as a table:

| # | Limitation acknowledged by the authors (paraphrase) | Locator | How the authors qualify/explain it |
|---|-----------------------------------------------------|---------|------------------------------------|
| 1 | | `[§x]` | |

**Notes**
- Restate only; do not evaluate. Anything the authors did not write does not belong in this section.
- When the authors say "future work will do X", the absence of X counts as a boundary the authors acknowledge, but do not exaggerate it into "the authors admit failure".

## 3. Generate Further Limitations (Six Categories)

### 3.1 Evidence
- Are variance, random seeds, confidence intervals and significance tests reported?
- Are only means/best values reported? Only successful cases?
- Do the metrics actually measure the conclusions (metric validity)? Were more suitable metrics avoided?

### 3.2 Experimental design
- Are baselines strong, tuned under the same budget, and official implementations?
- Is there leakage risk in data splits/preprocessing?
- Does the ablation cover the key design, or does it remove only one module?

### 3.3 Assumptions
- Which key assumption is not independently verified? How much of the conclusion survives when it fails?
- Is the error magnitude of approximation/linearization/mean-field/stationarity assumptions estimated?

### 3.4 External validity
- Verified on a single dataset/domain/scale/task only?
- Are the conclusions extrapolated to untested scenarios?
- Are real-system/deployment constraints (cost, latency, noise) considered?

### 3.5 Reproducibility
- Are code, data, splits, all hyperparameters, seeds and compute provided?
- Does key preprocessing exist only in code or in an oral description?

### 3.6 Presentation
- Are key concepts ambiguous or defined inconsistently?
- Is the wording stronger than the evidence ("prove" vs "observe")?
- Are terms/symbols invented without definition?

**Write each further limitation as**: `phenomenon (what the authors did not say) + evidence (which section/table) + impact (how the conclusion changes) + how to verify`.

Example:
> The numerical evidence lacks a convergence test: the 40 updates per cycle were compared with "more frequent" only once, and the threshold shift after halving the step size is not reported [p.30]; near the threshold the result is most sensitive to discretization, which affects the accuracy of `SI=1`. How to verify: run 10 seeds each with the step size halved and doubled, and compare the threshold shift.

## 4. Writing Template (Section 7)

```text
### 7.1 Limitations Acknowledged by the Authors (restatement)
| # | Limitation acknowledged by the authors | Locator |
(only what the authors wrote)

### 7.2 Further Limitations (My Additions)
1. <limitation>: <evidence>; impact: <...>; verification: <...>
2. ...

### 7.3 Strengths and Scope of Applicability
- Specific strengths (≥2, saying which design solves which problem)
- Scope of applicability (under what conditions the conclusions hold)

### 7.4 Threats to Validity and Reproducibility
- Internal validity:
- External validity:
- Reproducibility:

### 7.5 Information Gaps
- Content not reported/not verified/could not be read
```

**Prohibited**: 8-dimension score tables, confidence grades A/B/C, "what evidence would change the judgment" ratings, paraphrasing the authors' limitations as your own.

## 5. Threats to Validity

### 5.1 Internal validity
- **Data leakage**: did preprocessing use test-set statistics? Were time series shuffled? Do features contain labels?
- **Confounders**: does the improvement come from other changes (larger model, more data, longer training)?
- **Selection bias**: how were samples selected? Were failed samples removed?
- **Asymmetric tuning**: do the paper and the baselines get the same tuning budget?
- **Implementation differences**: are baselines official implementations? Were they weakened?

### 5.2 External validity
- Verified on only one dataset/domain/scale?
- Are hyperparameters sensitive to new scenarios? Do the results still hold at other scales?
- Does the task definition hide special assumptions (offline, static, abundant labels)?

### 5.3 Construct validity
- Do the metrics match the goal (accuracy ↔ calibration/fairness/robustness)?
- Can the metric be gamed (high BLEU ≠ good translation)?
- Do human evaluation/downstream tasks support the main-metric conclusions?

### 5.4 Conclusion validity
- Does the scope of the conclusions exceed the experimental coverage?
- Is correlation written as causation?
- Is "significant" supported by a statistical test?
- Are there undiscussed counterexamples/failure modes?

## 6. Reproducibility Checklist

- [ ] Code link (official/anonymous repository)
- [ ] Data source and access method
- [ ] Data splits (random seed, ratio, time split)
- [ ] Preprocessing pipeline
- [ ] All hyperparameters (including search range and selection basis)
- [ ] Random seeds and number of repetitions
- [ ] Hardware and training/simulation time
- [ ] Evaluation script and metric implementation
- [ ] Baseline implementation sources and tuning settings

Write missing items into §7.5 "Information Gaps"; do not fill them in from imagination.

## 7. Statistical Evidence Rules

| Situation | Requirement |
|-----------|-------------|
| Single run | write only "reported one result", not "stable improvement" |
| ≥3 seeds | report mean ± standard deviation; when comparing, check whether the variance overlaps |
| Significance test | record the test type, the unit of observation and the p-value; paired designs use a paired test |
| Multiple comparisons | correct when using many datasets/metrics, or state that no correction was made |
| Effect size | give the size of the difference in addition to the p-value; p-values are unreliable with small samples |
| Error bars/CI | state whether it is std / sem / CI, and the sample size n |
| Failure cases | results that report only successful cases are less credible |

## 8. Red-Flag Checklist (record on sight and try to verify)

| Red flag | Why it is dangerous | How to verify |
|----------|--------------------|---------------|
| No variance/single run | the improvement may come from randomness | look for seed count, error bars, appendix |
| Clearly weak/untuned baseline | the improvement is overestimated | check the baseline source and whether the budget is the same |
| Hyperparameters selected on the test set | optimistic bias | check whether a dev set is mentioned |
| Data leakage | results are not reproducible | check preprocessing and splits |
| Metric mismatched with the conclusion | the conclusion is invalid | check the metric definition and the task goal |
| Only means, no distribution | hides long-tail failures | look for per-task/per-domain results |
| Ablation removes only one module | no attribution possible | check variant coverage |
| All variants beat the baseline | suspicious | check the experimental design/reporting bias |
| Conclusions extrapolated to unverified scenarios | overgeneralization | compare with the experimental coverage |
| Excessive self-citation/low-quality sources | possible selective citation | spot-check the key citations |

## 9. Common Misjudgments

1. **Copying the authors' limitations as a critique** — your value is what the authors did not write.
2. **Treating "did not do X" as a defect** — unless X is standard practice in the field.
3. **Treating "simple" as "not novel"** — simple, effective designs are often harder.
4. **Treating "complex" as "good"** — stacking modules is not a contribution.
5. **Using citation counts/venue labels instead of quality judgment** — they are only external signals.
6. **Only finding faults, never merits** — good critique says "under what conditions it holds or does not hold".
7. **Rewriting boundaries the authors explicitly acknowledge as "further"** — repetition adds no information.

## 10. Pre-Delivery Check

- [ ] 7.1 contains only limitations acknowledged by the authors, with locators
- [ ] 7.2 has at least 3 further limitations, each with evidence and impact
- [ ] no 8-dimension score table, no confidence grades
- [ ] 7.4 covers internal/external validity and reproducibility
- [ ] 7.5 lists unreported/unverified information
- [ ] strengths are specific and terminology is accurate
