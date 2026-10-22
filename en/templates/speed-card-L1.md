---
paper_id: "{{firstauthor}}{{year}}-{{slug}}"
title: "{{paper title}}"
authors: ["{{Author 1}}", "{{Author 2}}"]
year: {{year}}
venue: "{{venue / arXiv:xxxx.xxxxxvN}}"
doi: ""
url: ""
keywords: ["{{kw1}}", "{{kw2}}"]
reading_level: L1
source_scope: full
status: draft
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
tags: []
---

# {{title}} — Quick-read Card

> Goal: decide within 10–15 minutes whether the paper deserves a deep read. Do not write method or experiment details; the conclusion stops at "continue reading or not".

## 0. At a Glance

- **Problem**: {{what it solves, under what setting, ≤40 words}}
- **Approach**: {{the core mechanism, not the model name, ≤40 words}}
- **Result**: {{key numbers + dataset; write "not reported" if there are none, ≤40 words}}
- **Why it matters**: {{whom it affects / which decision it informs, ≤40 words}} [Inference]

## 1. Paper Information

| Item | Content |
|------|---------|
| Authors / affiliations | {{...}} |
| Venue / year | {{...}} |
| Version / access date | {{...}} |
| Code / data | {{link or not reported}} |
| Paper type | {{empirical / theoretical / survey / system}} |

## 2. Background and Problem Definition

- Background: {{one sentence on the state of the field}}
- Pain point: {{what existing methods specifically lack}}
- Problem definition: {{input → output; key assumptions}}
- Success criteria: {{how the authors count it as solved}}

## 4. Method

- Core mechanism: {{one sentence that makes "how it is done" clear}}
- Key modules: {{1–3 items}}
- Difference from the closest method: {{1–2 items, with locators}}

## 5. Experiments and Evidence

> Abstract only (`source_scope: abstract`): keep only the "main result" row and drop the ablation and cost rows; use `[Abstract]` locators and run the self-check with `--abstract`.

| Evidence | Value / conclusion | Locator |
|----------|--------------------|---------|
| {{main result (vs. strongest baseline)}} | {{...}} | {{[Table 2]}} |
| {{ablation / control}} | {{...}} | {{[Table 3]}} |
| {{cost / scale}} | {{...}} | {{[§5]}} |

## 7. Critical Appraisal

- **Main strengths**: {{1–2 items, specific}}
- **Main doubts**: {{1–2 items, specific}}
- **Worth a deep read**: {{yes/no}}. Reason: {{...}}
- **If deep reading, focus on**: {{sections/figures}}

## 9. Next Steps

- To be confirmed: {{[Question] ...}}
- Literature to add: {{...}}
