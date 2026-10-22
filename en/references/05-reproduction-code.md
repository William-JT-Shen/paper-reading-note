# 05 Reproduction Code: How to Write It and Two Runnable Skeletons

> For L3 section 11 "Reproduction Plan". Requirements: the code corresponds one-to-one with the paper's equations, runs directly, has random seeds, and has acceptance output.
> Do not write only pseudocode or "omitted here".

## 1. Principles

1. **Runnable**: someone who receives the note can copy the code, fill in the values from the parameter table and run it; dependencies, versions and run commands are complete.
2. **Corresponds to equations**: every key equation has a corresponding implementation, with `Eq. (x)` in a comment; do not pass off a different model.
3. **Reproducible**: fix random seeds; report the number of repetitions; save the raw output (CSV/NPZ/figures).
4. **Acceptable**: print/save metrics that can be compared directly with the paper's figures/tables; state the acceptance thresholds and falsification conditions.
5. **Honest**: parameters the paper does not give go in "known gaps" together with how you chose them; do not pretend they are the paper's settings.

## 2. Skeleton A: Numerical Simulation / Phase Model (NumPy + SciPy)

Suitable for coupled oscillators, ODEs, phase models and numerical-experiment papers. Replace the formulas in the comments with the paper's formulas.

```python
#!/usr/bin/env python3
"""Reproduce the <Fig./Table> of <paper_id>: synchronization threshold of a phase-oscillator population.

Run: python reproduce_phase_model.py --J 100 --K 2.0 --seed 0
Output: results.npz (time series) and order_parameter.png
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Config:
    J: int = 100                 # number of oscillators (paper parameter)
    T_mean: float = 40.0         # mean natural period (paper parameter)
    spread: float = 0.05         # relative spread of periods (paper parameter)
    K: float = 2.0               # coupling strength (swept variable)
    dt: float = 0.025            # integration step
    steps: int = 120_000         # total number of steps
    seed: int = 0


def order_parameter(theta: np.ndarray) -> float:
    """Kuramoto order parameter r = |mean(exp(i*theta))| (replace with the paper's metric, e.g. |S|)."""
    return float(np.abs(np.mean(np.exp(1j * theta))))


def simulate(cfg: Config) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    # natural-period distribution: replace with the paper's N(f) (e.g. triangular/rectangular/Lorentzian)
    T = cfg.T_mean * (1.0 + cfg.spread * (rng.random(cfg.J) - 0.5) * 2.0)
    omega = 2.0 * np.pi / T
    theta = rng.random(cfg.J) * 2.0 * np.pi

    r_hist = np.empty(cfg.steps)
    theta_hist = np.empty((cfg.steps, cfg.J), dtype=np.float32)
    for step in range(cfg.steps):
        # paper model: dtheta_i/dt = omega_i + (K/J) * sum_j sin(theta_j - theta_i)
        # if the paper uses the Winfree model, replace with omega_i + Z(theta_i) * sum_j X(theta_j) / J
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
    print(f"final r = {out['r'][-1]:.4f} (paper value: <enter the paper's value>)")


if __name__ == "__main__":
    main()
```

**Replacement checklist**
- `N(f)`: change to the paper's distribution and parameters;
- coupling function: `sin(θ_j-θ_i)` → the paper's `Z(θ_i)X(θ_j)` or another form;
- metric: `r` → the paper's `|S|`, synchronization fraction, etc.;
- integrator: Euler → RK4 (if the paper uses a continuous ODE);
- initialization: random phases → the paper's initial conditions.

## 3. Skeleton B: Machine-Learning Training/Evaluation (PyTorch)

Suitable for papers with a training set, a model, metrics and baselines.

```python
#!/usr/bin/env python3
"""Reproduce the <Table> of <paper_id>: main training and evaluation results.

Run: python reproduce_training.py --epochs 10 --seed 0
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
    """Replace with the paper's model; keep the same depth/width/activations as the paper."""

    def __init__(self, in_dim: int = 64, hidden: int = 128, out_dim: int = 10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def make_loaders(batch_size: int = 64) -> tuple[DataLoader, DataLoader]:
    # replace with the paper's dataset and splits; random tensors are used here as placeholders so the script runs
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

    print(f"final test acc = {evaluate(model, test_loader):.4f} (paper value: <enter the paper's value>)")


if __name__ == "__main__":
    main()
```

**Replacement checklist**
- dataset, splits, preprocessing, batch size;
- model structure and hyperparameters (depth, width, dropout, initialization);
- optimizer, learning-rate schedule, number of epochs;
- metrics and evaluation script (consistent with the paper);
- baselines: implement/call at least one strongest baseline and train it under the same budget.

## 4. What Section 11 Must Contain

- **Environment**: Python version, dependencies and versions, CPU/GPU.
- **Parameter table**: parameters taken from the paper + parameters set by yourself (label the source of each separately).
- **Code**: complete and runnable, one-to-one with the paper's equations.
- **Run command**: one command runs it.
- **Acceptance criterion**: which figure/table of the paper to compare against, allowed error.
- **Falsification condition**: which result means the reproduction failed.
- **Known gaps**: quantities the paper does not report that you must set yourself.

## 5. Code Quality Check

- [ ] runs directly (no undefined variables, no fake data claimed to be real)
- [ ] fixed random seeds, reported number of repetitions
- [ ] every key equation has a corresponding implementation
- [ ] outputs can be saved and metrics recomputed
- [ ] parameters match the paper, or are explicitly marked "set by the note author"
- [ ] do not paste code that has not actually run into the note
