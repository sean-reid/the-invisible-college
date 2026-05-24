"""
Adam Epsilon Stage 3: Narrow sweep around the transition zone (1e-3 to 1e-2),
100 seeds to estimate the probability of basin change.
"""

import torch
import torch.nn as nn
import numpy as np
import json
import math
import time

# Narrow the sweep: 8 epsilon values between 1e-3 and 1e-2 (log-spaced)
# plus 1e-2 and 1e-1 to bracket the regime
EPSILONS_NARROW = [
    1e-3,
    2e-3,
    3e-3,
    5e-3,
    7e-3,
    1e-2,
    2e-2,
    5e-2,
    1e-1,
]
N_SEEDS = 100


def make_two_spirals(n_points, seed):
    torch.manual_seed(seed)
    n = n_points // 2
    ix = torch.arange(n).float()

    def spiral(ix, offset_deg):
        angle = (ix / n * 570 + offset_deg) * (math.pi / 180.0)
        r = (ix + 1) / n * 5
        x = r * torch.cos(angle) + torch.randn(n) * 0.1
        y = r * torch.sin(angle) + torch.randn(n) * 0.1
        return torch.stack([x, y], dim=1)

    X0 = spiral(ix, 0)
    X1 = spiral(ix, 180)
    X = torch.cat([X0, X1], dim=0)
    y = torch.cat([torch.zeros(n), torch.ones(n)]).long()
    perm = torch.randperm(2 * n)
    return X[perm], y[perm]


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

    def reset(self, seed):
        torch.manual_seed(seed)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)


def run():
    print("=== Stage 3: Narrow epsilon sweep around transition, 100 seeds ===")
    N_TRAIN = 400
    MAX_STEPS = 3000
    LR = 1e-3

    results = {}
    for eps in EPSILONS_NARROW:
        test_accs = []
        train_losses = []
        weight_norms = []

        for seed in range(N_SEEDS):
            X_train, y_train = make_two_spirals(N_TRAIN, seed=seed)
            X_test, y_test = make_two_spirals(200, seed=seed + 1000)
            model = MLP()
            model.reset(seed=seed + 2000)
            opt = torch.optim.Adam(model.parameters(), lr=LR, eps=eps)
            loss_fn = nn.CrossEntropyLoss()

            for _ in range(MAX_STEPS):
                opt.zero_grad()
                loss_fn(model(X_train), y_train).backward()
                opt.step()

            with torch.no_grad():
                tl = loss_fn(model(X_train), y_train).item()
                acc = (model(X_test).argmax(1) == y_test).float().mean().item()
                wn = sum(p.norm().item() ** 2 for p in model.parameters()) ** 0.5

            train_losses.append(tl)
            test_accs.append(acc)
            weight_norms.append(wn)

        results[eps] = {
            "test_acc_median": float(np.median(test_accs)),
            "test_acc_q25": float(np.percentile(test_accs, 25)),
            "test_acc_q75": float(np.percentile(test_accs, 75)),
            "test_acc_mean": float(np.mean(test_accs)),
            "test_acc_std": float(np.std(test_accs)),
            "test_acc_raw": test_accs,
            "train_loss_median": float(np.median(train_losses)),
            "train_loss_q25": float(np.percentile(train_losses, 25)),
            "train_loss_q75": float(np.percentile(train_losses, 75)),
            "weight_norm_median": float(np.median(weight_norms)),
            # fraction of runs achieving >96% accuracy (the high-basin threshold)
            "frac_high_basin": float(np.mean([a >= 0.96 for a in test_accs])),
        }
        print(f"  eps={eps:.0e}: "
              f"acc={results[eps]['test_acc_median']:.3f}±{results[eps]['test_acc_std']:.3f} "
              f"[{results[eps]['test_acc_q25']:.3f},{results[eps]['test_acc_q75']:.3f}] "
              f"p(high)={results[eps]['frac_high_basin']:.2f} "
              f"loss={results[eps]['train_loss_median']:.4f}")

    return results


if __name__ == "__main__":
    t0 = time.time()
    results = run()
    elapsed = time.time() - t0
    print(f"\nElapsed: {elapsed/60:.1f} min")

    def jsonify(d):
        if isinstance(d, dict):
            return {str(k): jsonify(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [jsonify(i) for i in d]
        elif isinstance(d, float):
            return round(d, 8)
        else:
            return d

    with open("stage3_results.json", "w") as f:
        json.dump({"stage3_narrow": jsonify(results), "elapsed_seconds": round(elapsed, 1)}, f, indent=2)
    print("Written to stage3_results.json")
