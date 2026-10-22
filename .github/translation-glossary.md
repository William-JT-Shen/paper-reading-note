# Translation Glossary — English Skill (`en/`)

This file documents the terminology and formatting conventions used to keep the English skill aligned with the Chinese source. It is useful when updating either language.

## Voice and register

- Use concise technical English, imperative mood for instructions ("Read the paper…", "Write…").
- Do not translate code, file names, YAML keys, CLI flags, or equation symbols.
- Keep the original structure, tables, checklists, and numbering. Translate meaning, not word-for-word syntax.
- Use "paper" (not "article") for the academic object; "note" for the reading note; "skill" for this package.
- Avoid marketing language. The Chinese source is deliberately plain; keep it plain.

## Core terms

| Chinese | English |
|---|---|
| 文献阅读笔记 | paper reading note |
| 精读 / 速读卡 | deep read / quick-read card |
| 标准笔记 / 深度笔记 | standard note / deep note |
| 阅读级别 L1/L2/L3 | reading level L1/L2/L3 |
| 定位符 | locator |
| 标签 | source tag |
| 原文 / 推断 / 外部 / 疑问 | `[Original]` / `[Inference]` / `[External: source]` / `[Question]` |
| 抽取表 | extraction table |
| 批判性评估 | critical appraisal |
| 作者承认的局限 | limitations acknowledged by the authors |
| 进一步的局限 / 我补充 | further limitations / my additions |
| 威胁有效性 | threats to validity |
| 可复现性 | reproducibility |
| 信息缺口 | information gaps |
| 研究空白 | research gap |
| 可追问问题 | open questions |
| 综述笔记 | synthesis note |
| 对比矩阵 | comparison matrix |
| 概念图 | concept map |
| 引用链 | citation chain |
| 领域导读 | field guide (section `Guide: What This Field Is About`) |
| 附录 1：术语解释 | Appendix 1: Terminology |
| 公式详解 | Equation Walkthrough |
| 推导主线 | derivation chain |
| 表外推导 | derivation outside the table |
| 推导动机 | derivation motive |
| 思想来源 | intellectual origin |
| 与相邻公式的关系 | relation to adjacent equations |
| 起始式 | starting expression |
| 关键判断 | key claim |
| 最小机制 | minimal mechanism |
| 语病检查 | proofreading pass |
| 复现计划 | reproduction plan |
| 公式与推导核查 | Formula and Derivation Verification |
| 质量门 | quality gate |
| 自检 | self-check |
| 占位符 | placeholder |
| 摘录 | quotation |
| 多篇模式 | multi-paper mode |

## Fixed section headings (must match exactly)

```
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

## Keyword strings the English checker will expect

- §0 bullets: `**Problem**`, `**Approach**`, `**Result**`, `**Why it matters**`.
- §5: must contain `baseline`; must contain one of `ablation`, `control`, `robust`, `failure`.
- §4.3 must contain `### 4.3 Equation Walkthrough`, `#### 4.3.0`, one of `derivation chain` / `formula chain`, at least two `Derivation motive`, at least two `Relation to adjacent`, and `Derivation process`.
- §7 must contain `### 7.1`, `### 7.2`, `author`, `limitation`, one of `further` / `addition`, `Strength` (or `strength`), and one of `threat`, `validity`, `reproducib`.
- §8 must contain `transferable` and `next step`.
- §9 must contain `gap`.
- Tags used in the body: `[Original]` and at least one of `[Inference]`, `[External`, `[Question]`.
- L3 §11: must contain a ```` ```python ```` fence, `import` or `def`, no `NotImplementedError`, and `run` / `acceptance` / `falsification` (warnings for the last three).

## Field labels inside the 4.3 table

| Chinese | English |
|---|---|
| 公式 | Equation |
| 含义 | Meaning |
| 符号 | Symbols |
| 推导动机 | Derivation motive |
| 思想来源 | Intellectual origin |
| 在方法中的作用 | Role in the method |
| 假设/近似 | Assumptions / approximations |
| 与相邻公式的关系 | Relation to adjacent equations |

Below each table, the derivation block begins with `**Derivation process (...)**` and follows the Chinese rules: sources of the starting expression, no skipped steps, paper-style prose, key claims with minimal mechanism, and a proofreading pass.

## Commands and paths

- Replace local Windows paths with portable placeholders: `<skill-dir>` and `<notes-dir>`.
- Use POSIX-style relative paths in examples where possible.
- Keep CLI flags unchanged (`--strict`, `--abstract`, `--json`).

## Tone examples

- Chinese: "先定位再抽取" → English: "Locate before extracting."
- Chinese: "不允许跳过第 3 张表直接写结论" → English: "Do not skip the evidence table and jump to conclusions."
- Chinese: "把作者 limitation 抄一遍当批判" → English: "Paraphrasing the authors' limitations is not a critique."
