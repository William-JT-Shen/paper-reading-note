# 05　复现代码：写法与两个可运行骨架

> 用于 L3 第 11 节“复现计划”。要求：代码与论文公式一一对应、可直接运行、有随机种子、有验收输出。
> 不要只写伪代码或“此处省略”。

## 一、原则

1. **可运行**：拿到笔记的人复制代码、按参数表填值即可跑；依赖、版本、运行命令写全。
2. **与公式对应**：每个关键公式在代码中有对应实现，注释标 `Eq. (x)`；不要用别的模型冒充。
3. **可复现**：固定随机种子；报告重复次数；保存原始输出（CSV/NPZ/图）。
4. **可验收**：打印/保存与论文图表可直接对比的指标；写清验收阈值和证伪条件。
5. **诚实**：论文没给的参数，在“已知缺口”列出并说明你如何取值；不要假装是原文设置。

## 二、骨架 A：数值模拟 / 相位模型（NumPy + SciPy）

适合耦合振子、ODE、相位模型、数值实验类论文。把注释中的公式替换成论文公式。

```python
#!/usr/bin/env python3
"""复现 <paper_id> 的 <Fig./Table>：相位振子群体的同步阈值。

运行：python reproduce_phase_model.py --J 100 --K 2.0 --seed 0
输出：results.npz（时序）与 order_parameter.png
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Config:
    J: int = 100                 # 振子数（论文参数）
    T_mean: float = 40.0         # 平均固有周期（论文参数）
    spread: float = 0.05         # 周期相对展宽（论文参数）
    K: float = 2.0               # 耦合强度（扫描变量）
    dt: float = 0.025            # 积分步长
    steps: int = 120_000         # 总步数
    seed: int = 0


def order_parameter(theta: np.ndarray) -> float:
    """Kuramoto 序参量 r = |mean(exp(i*theta))|（替换为论文指标 |S| 等）。"""
    return float(np.abs(np.mean(np.exp(1j * theta))))


def simulate(cfg: Config) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    # 固有周期分布：按论文 N(f) 替换（如三角/矩形/Lorentzian）
    T = cfg.T_mean * (1.0 + cfg.spread * (rng.random(cfg.J) - 0.5) * 2.0)
    omega = 2.0 * np.pi / T
    theta = rng.random(cfg.J) * 2.0 * np.pi

    r_hist = np.empty(cfg.steps)
    theta_hist = np.empty((cfg.steps, cfg.J), dtype=np.float32)
    for step in range(cfg.steps):
        # 论文模型：dtheta_i/dt = omega_i + (K/J) * sum_j sin(theta_j - theta_i)
        # 若论文是 Winfree 模型，替换为 omega_i + Z(theta_i) * sum_j X(theta_j) / J
        coupling = np.sin(theta[None, :] - theta[:, None]).sum(axis=1)
        theta = (theta + cfg.dt * (omega + cfg.K / cfg.J * coupling)) % (2.0 * np.pi)
        r_hist[step] = order_parameter(theta)
        theta_hist[step] = theta
    return {"r": r_hist, "theta": theta_hist}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--J", type=int, default=100)
    parser.add_argument("--K", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    cfg = Config(J=args.J, K=args.K, seed=args.seed)
    out = simulate(cfg)
    np.savez("results.npz", r=out["r"], theta=out["theta"], cfg=vars(cfg))
    plt.plot(out["r"])
    plt.xlabel("step")
    plt.ylabel("order parameter r")
    plt.tight_layout()
    plt.savefig("order_parameter.png", dpi=150)
    print(f"final r = {out['r'][-1]:.4f}（论文报告值：<填论文值>）")


if __name__ == "__main__":
    main()
```

**替换清单**
- `N(f)`：改为论文的分布与参数；
- 耦合函数：`sin(θ_j-θ_i)` → 论文的 `Z(θ_i)X(θ_j)` 或其他形式；
- 指标：`r` → 论文的 `|S|`、同步比例等；
- 积分器：Euler → RK4（若论文用连续 ODE）；
- 初始化：随机相位 → 论文的初始条件。

## 三、骨架 B：机器学习训练/评测（PyTorch）

适合有训练集、模型、指标、基线的论文。

```python
#!/usr/bin/env python3
"""复现 <paper_id> 的 <Table>：训练与评测主结果。

运行：python reproduce_training.py --epochs 10 --seed 0
"""
from __future__ import annotations

import argparse

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class Model(nn.Module):
    """替换为论文模型；保持与论文一致的层数/维度/激活。"""

    def __init__(self, in_dim: int = 64, hidden: int = 128, out_dim: int = 10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def make_loaders(batch_size: int = 64) -> tuple[DataLoader, DataLoader]:
    # 替换为论文数据集与划分；此处用随机张量占位，保证脚本可跑
    g = torch.Generator().manual_seed(0)
    x = torch.randn(1024, 64, generator=g)
    y = torch.randint(0, 10, (1024,), generator=g)
    train = TensorDataset(x[:800], y[:800])
    test = TensorDataset(x[800:], y[800:])
    return DataLoader(train, batch_size=batch_size, shuffle=True), DataLoader(test, batch_size=batch_size)


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader) -> float:
    model.eval()
    correct = total = 0
    for x, y in loader:
        pred = model(x).argmax(dim=1)
        correct += int((pred == y).sum())
        total += int(y.numel())
    return correct / max(total, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    set_seed(args.seed)

    train_loader, test_loader = make_loaders()
    model = Model()
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(args.epochs):
        model.train()
        for x, y in train_loader:
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
        print(f"epoch {epoch + 1}: test acc = {evaluate(model, test_loader):.4f}")

    print(f"final test acc = {evaluate(model, test_loader):.4f}（论文报告值：<填论文值>）")


if __name__ == "__main__":
    main()
```

**替换清单**
- 数据集、划分、预处理、batch size；
- 模型结构与超参（层数、宽度、dropout、初始化）；
- 优化器、学习率调度、训练轮数；
- 指标与评测脚本（与论文一致）；
- 基线：至少实现/调用一个最强基线，同预算训练。

## 四、第 11 节必须包含

- **环境**：Python 版本、依赖及版本、CPU/GPU。
- **参数表**：来自论文的参数 + 自行设定的参数（分开标注来源）。
- **代码**：完整可运行，与论文公式一一对应。
- **运行命令**：一条命令能跑。
- **验收标准**：与论文哪张图/表对比、允许误差。
- **证伪条件**：什么结果说明复现失败。
- **已知缺口**：论文未报告、需自行设定的量。

## 五、代码质量检查

- [ ] 能直接运行（无未定义变量、无假数据却声称是真实数据）
- [ ] 固定随机种子，报告重复次数
- [ ] 每个关键公式在代码中有对应实现
- [ ] 输出可保存、可复算指标
- [ ] 参数与论文一致，或明确标注"自行设定"
- [ ] 不把未跑通的代码贴进笔记
