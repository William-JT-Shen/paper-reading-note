# L3 追加节：复现计划（含 Python 代码）

> 用法：L3 笔记在 L2 模板之后追加本节（编号 11），再加第 12 节“公式与推导核查”。
> 复现计划必须包含**可直接运行的 Python 代码**；骨架与检查项见 `references/05-reproduction-code.md`。

## 11. 复现计划

**目标**：复现 {{Fig./Table 编号与结论}}

**环境**

| 项 | 内容 |
|----|------|
| Python | {{3.11}} |
| 依赖 | {{numpy, scipy, matplotlib / torch}} |
| 硬件 | {{CPU / GPU 型号；预计时长}} |

**数据与参数**

| 参数 | 取值 | 来源 |
|------|------|------|
| {{J}} | {{100}} | 论文 [p.x] |
| {{K}} | {{2.0}} | 论文 [p.x] |
| {{种子}} | {{0}} | 自行设定 |
| {{其他自行设定项}} | {{...}} | 自行设定 |

**代码**（替换参数与公式后应可直接运行；文件建议保存为 `reproduce_<paper_id>.py`）

```python
#!/usr/bin/env python3
"""复现 {{paper_id}} 的 {{Fig./Table}}。"""
from __future__ import annotations

import argparse

import numpy as np
import matplotlib.pyplot as plt


def simulate(seed: int = 0) -> dict[str, np.ndarray]:
    """按论文公式实现；注释标注对应的 Eq./章节。"""
    rng = np.random.default_rng(seed)
    # TODO: 按论文初始化参数/状态（来自第 11 节参数表）
    raise NotImplementedError("替换为论文模型")


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

**运行命令**

```bash
python reproduce_{{paper_id}}.py --seed 0
```

**验收标准**：{{与论文哪张图/表对比；允许误差；至少重复几次}}

**证伪条件**：{{出现什么结果判定复现失败}}

**已知缺口**：{{论文未报告、必须自行设定的量；无法获取的数据/算力}}

> 代码要求：可运行、固定种子、指标可复算、与论文公式对应；不要贴伪代码或未跑通的代码。

## 12. 公式与推导核查

**符号与量纲**

| 符号 | 含义 | 量纲/取值 |
|------|------|-----------|
| {{...}} | {{...}} | {{...}} |

**逐步核对**

1. {{从哪个公式推到哪个公式；核对结果}} [Eq. ({{x}})]
2. {{稳定性/边界条件/近似条件}} [§{{x}}]

**勘误记录**：{{阅读中发现的 OCR/符号/笔误；没有则写“未发现”}}

**遗留疑点**：{{[疑问] 1–3 条}}
