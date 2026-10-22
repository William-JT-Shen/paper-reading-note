# {{topic}} — Literature Comparison Matrix

> Scope: {{topic/problem}} | Papers: {{N}} | Time window: {{YYYY–YYYY}} | Updated: {{YYYY-MM-DD}}
> Generated with `python <skill-dir>/scripts/build_matrix.py notes/ -o notes/matrix.md --csv notes/matrix.csv`, then fill in Delta / Evidence quality / Reproducibility / Relevance by hand.

## 1. Main Matrix

| Paper | Year | Venue | Problem | Method | Key result | Delta | Evidence quality | Reproducibility | Relevance (1–5) | Note |
|-------|------|-------|---------|--------|------------|-------|------------------|-----------------|-----------------|------|
| [{{paper_id}}]({{paper_id}}.md) | {{}} | {{}} | {{}} | {{}} | {{}} | {{relative/absolute + metric + dataset}} | {{strong/moderate/weak + reason}} | {{code/data/seed}} | {{}} | {{}} |
| | | | | | | | | | | |

## 2. Comparability Notes

- **Are the metrics consistent**: {{...}}
- **Are the data/splits consistent**: {{...}}
- **Are the training budgets comparable**: {{...}}
- **Non-comparable items**: {{list and explain; mark them with "—" in the matrix}}

## 3. Grouping and Observations

- **Method family A**: {{representative work, common ground, common weakness}}
- **Method family B**: {{...}}
- **Outliers**: {{notably high/low results + possible causes}}
- **Same question, different answers**: {{conflicting conclusions + possible causes}}

## 4. Method Family × Evidence Strength

| Method family | Representative work | Strongest evidence | Evidence gap | Relevance |
|---------------|---------------------|--------------------|--------------|-----------|
| {{...}} | {{...}} | {{...}} | {{...}} | {{}} |

## 5. Initial Conclusions

- **Consensus** (≥2 independent papers): {{...}}
- **Disagreements**: {{...}}
- **Evidence gaps**: {{...}}
- **Implications for topic selection**: {{...}}

## 6. Literature to Add

| Paper | Why it is needed | Status |
|-------|------------------|--------|
| {{...}} | {{...}} | {{unread / reading / read}} |
