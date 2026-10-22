# L3 Addition: Reproduction Plan (with Python Code)

> Usage: an L3 note replaces the §11/§12 stubs in `templates/note-L2.md` with this section (numbered 11 and 12; keep Appendix 1 last).
> The reproduction plan must contain **directly runnable Python code**; the skeleton and checklist are in `references/05-reproduction-code.md`.

## 11. Reproduction Plan

**Goal**: reproduce {{Fig./Table number and conclusion}}

**Environment**

| Item | Content |
|------|---------|
| Python | {{3.11}} |
| Dependencies | {{numpy, scipy, matplotlib / torch}} |
| Hardware | {{CPU / GPU model; estimated duration}} |

**Data and parameters**

| Parameter | Value | Source |
|-----------|-------|--------|
| {{J}} | {{100}} | paper [p.x] |
| {{K}} | {{2.0}} | paper [p.x] |
| {{seed}} | {{0}} | set by us |
| {{other self-set item}} | {{...}} | set by us |

**Code** (should run directly after replacing the parameters and equations; save it as `reproduce_<paper_id>.py`)

```python
#!/usr/bin/env python3
"""Reproduce {{Fig./Table}} of {{paper_id}}."""
from __future__ import annotations

import argparse

import numpy as np
import matplotlib.pyplot as plt


def simulate(seed: int = 0) -> dict[str, np.ndarray]:
    """Implement the paper's equations; annotate comments with the corresponding Eq./section."""
    rng = np.random.default_rng(seed)
    # TODO: initialize parameters/state from the paper (see the parameter table in §11)
    raise NotImplementedError("replace with the paper's model")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    out = simulate(args.seed)
    np.savez("results.npz", **out)
    print("done")


if __name__ == "__main__":
    main()
```

**Run command**

```bash
python reproduce_{{paper_id}}.py --seed 0
```

**Acceptance criteria**: {{which figure/table in the paper to compare against; allowed error; how many repetitions at minimum}}

**Falsification conditions**: {{which outcome counts as a failed reproduction}}

**Known gaps**: {{quantities the paper does not report and that must be set manually; data/compute that cannot be obtained}}

> Code requirements: runnable, fixed seed, metrics recomputable, corresponding to the paper's equations; do not paste pseudocode or code that has not been run.

## 12. Formula and Derivation Verification

**Symbols and dimensions**

| Symbol | Meaning | Dimension / value |
|--------|---------|-------------------|
| {{...}} | {{...}} | {{...}} |

**Step-by-step check**

1. {{from which equation to which; check result}} [Eq. ({{x}})]
2. {{stability / boundary conditions / approximation conditions}} [§{{x}}]

**Errata**: {{OCR/symbol/typo issues found while reading; write "none found" if there are none}}

**Remaining doubts**: {{[Question] 1–3}}
