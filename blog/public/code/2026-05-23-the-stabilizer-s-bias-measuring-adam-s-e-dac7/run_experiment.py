"""
Adam Epsilon Study: Stages 1 and 2
Run with: /opt/homebrew/bin/python3 run_experiment.py

Stage 1: Convex quadratic bowl, 100 dimensions
Stage 2: 3-layer MLP on two-spirals classification
"""

import torch
import torch.nn as nn
import numpy as np
import json
import math
import time

EPSILONS = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
N_SEEDS = 30
RESULTS = {}

# ── Stage 1: Convex quadratic bowl ──────────────────────────────────────────

def run_stage1():
    print("=== Stage 1: Convex quadratic bowl (100D) ===")
    DIM = 100
    MAX_STEPS = 2000
    LR = 1e-3
    CONV_THRESH = 1e-6

    results = {}
    for eps in EPSILONS:
        steps_to_conv = []
        final_dists = []
        for seed in range(N_SEEDS):
            torch.manual_seed(seed)
            # Random positive definite curvature (eigenvalues between 0.1 and 10)
            scale = torch.exp(torch.rand(DIM) * math.log(100) + math.log(0.1))
            # Start point: unit Gaussian
            x = nn.Parameter(torch.randn(DIM))
            opt = torch.optim.Adam([x], lr=LR, eps=eps)

            conv_step = MAX_STEPS
            for step in range(MAX_STEPS):
                opt.zero_grad()
                loss = (scale * x * x).sum()
                loss.backward()
                opt.step()
                dist = x.data.norm().item()
                if dist < CONV_THRESH:
                    conv_step = step + 1
                    break
            steps_to_conv.append(conv_step)
            final_dists.append(x.data.norm().item())

        results[eps] = {
            "steps_median": float(np.median(steps_to_conv)),
            "steps_q25": float(np.percentile(steps_to_conv, 25)),
            "steps_q75": float(np.percentile(steps_to_conv, 75)),
            "steps_raw": steps_to_conv,
            "dist_median": float(np.median(final_dists)),
            "dist_q25": float(np.percentile(final_dists, 25)),
            "dist_q75": float(np.percentile(final_dists, 75)),
            "dist_raw": final_dists,
            "n_converged": sum(1 for s in steps_to_conv if s < MAX_STEPS),
        }
        print(f"  eps={eps:.0e}: steps_median={results[eps]['steps_median']:.0f} "
              f"[{results[eps]['steps_q25']:.0f},{results[eps]['steps_q75']:.0f}] "
              f"dist_median={results[eps]['dist_median']:.2e} "
              f"n_conv={results[eps]['n_converged']}/30")

    return results


# ── Stage 2: Two-spirals MLP ─────────────────────────────────────────────────

def make_two_spirals(n_points, seed):
    """Generate two-spirals dataset."""
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
    # Shuffle
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


def run_stage2():
    print("\n=== Stage 2: Two-spirals MLP (3-layer, 64 hidden) ===")
    N_TRAIN = 400
    N_TEST = 200
    MAX_STEPS = 3000
    LR = 1e-3

    results = {}
    for eps in EPSILONS:
        train_losses = []
        test_accs = []
        weight_norms = []

        for seed in range(N_SEEDS):
            # Data uses its own seed (fixed per seed)
            X_train, y_train = make_two_spirals(N_TRAIN, seed=seed)
            X_test, y_test = make_two_spirals(N_TEST, seed=seed + 1000)

            model = MLP()
            model.reset(seed=seed + 2000)
            opt = torch.optim.Adam(model.parameters(), lr=LR, eps=eps)
            loss_fn = nn.CrossEntropyLoss()

            for step in range(MAX_STEPS):
                opt.zero_grad()
                logits = model(X_train)
                loss = loss_fn(logits, y_train)
                loss.backward()
                opt.step()

            # Evaluate
            with torch.no_grad():
                train_loss = loss_fn(model(X_train), y_train).item()
                test_logits = model(X_test)
                test_acc = (test_logits.argmax(dim=1) == y_test).float().mean().item()
                wn = sum(p.norm().item() ** 2 for p in model.parameters()) ** 0.5

            train_losses.append(train_loss)
            test_accs.append(test_acc)
            weight_norms.append(wn)

        results[eps] = {
            "train_loss_median": float(np.median(train_losses)),
            "train_loss_q25": float(np.percentile(train_losses, 25)),
            "train_loss_q75": float(np.percentile(train_losses, 75)),
            "train_loss_raw": train_losses,
            "test_acc_median": float(np.median(test_accs)),
            "test_acc_q25": float(np.percentile(test_accs, 25)),
            "test_acc_q75": float(np.percentile(test_accs, 75)),
            "test_acc_raw": test_accs,
            "weight_norm_median": float(np.median(weight_norms)),
            "weight_norm_q25": float(np.percentile(weight_norms, 25)),
            "weight_norm_q75": float(np.percentile(weight_norms, 75)),
            "weight_norm_raw": weight_norms,
        }
        print(f"  eps={eps:.0e}: train_loss={results[eps]['train_loss_median']:.4f} "
              f"[{results[eps]['train_loss_q25']:.4f},{results[eps]['train_loss_q75']:.4f}] "
              f"test_acc={results[eps]['test_acc_median']:.3f} "
              f"[{results[eps]['test_acc_q25']:.3f},{results[eps]['test_acc_q75']:.3f}] "
              f"wnorm={results[eps]['weight_norm_median']:.2f}")

    return results


# ── Stage 3: Narrow sweep around transition (conditional) ───────────────────

def run_stage3(stage2_results):
    """
    Run only if Stage 2 shows basin-level differences.
    Criterion: IQR of test_acc distributions of adjacent epsilon values
    do not overlap for at least one pair.
    """
    eps_keys = EPSILONS
    accs = [(e, stage2_results[e]["test_acc_raw"]) for e in eps_keys]

    # Check for non-overlapping IQRs between consecutive epsilon pairs
    transition_found = False
    for i in range(len(accs) - 1):
        e1, a1 = accs[i]
        e2, a2 = accs[i + 1]
        q25_1, q75_1 = np.percentile(a1, [25, 75])
        q25_2, q75_2 = np.percentile(a2, [25, 75])
        if q75_1 < q25_2 or q75_2 < q25_1:
            print(f"\n  Basin-level separation detected between eps={e1:.0e} and eps={e2:.0e}")
            transition_found = True

    if not transition_found:
        print("\n=== Stage 3: Skipped — no basin-level IQR separation in Stage 2 ===")
        return None

    # If transition found, narrow the sweep (not expected given two-spirals noise)
    print("\n=== Stage 3: Narrowing sweep around transition zone (100 seeds) ===")
    # (Placeholder: implement if Stage 2 actually shows separation)
    return {"note": "basin_separation_found_full_stage3_not_run"}


# ── Auxiliary: learning-rate interaction check ───────────────────────────────

def run_lr_interaction():
    """3 LR × 5 epsilon grid to check for interaction."""
    print("\n=== Auxiliary: LR × epsilon interaction (3×5 grid) ===")
    LRS = [1e-4, 1e-3, 1e-2]
    EPS_SUBSET = [1e-10, 1e-8, 1e-6, 1e-4, 1e-2]
    N_TRAIN = 400
    MAX_STEPS = 3000
    N_SEEDS_AUX = 10

    results = {}
    for lr in LRS:
        for eps in EPS_SUBSET:
            accs = []
            for seed in range(N_SEEDS_AUX):
                X_train, y_train = make_two_spirals(N_TRAIN, seed=seed)
                X_test, y_test = make_two_spirals(200, seed=seed + 1000)
                model = MLP()
                model.reset(seed=seed + 2000)
                opt = torch.optim.Adam(model.parameters(), lr=lr, eps=eps)
                loss_fn = nn.CrossEntropyLoss()
                for _ in range(MAX_STEPS):
                    opt.zero_grad()
                    loss_fn(model(X_train), y_train).backward()
                    opt.step()
                with torch.no_grad():
                    acc = (model(X_test).argmax(1) == y_test).float().mean().item()
                accs.append(acc)
            key = (lr, eps)
            results[key] = {
                "median": float(np.median(accs)),
                "q25": float(np.percentile(accs, 25)),
                "q75": float(np.percentile(accs, 75)),
                "raw": accs,
            }
            print(f"  lr={lr:.0e} eps={eps:.0e}: acc={results[key]['median']:.3f} "
                  f"[{results[key]['q25']:.3f},{results[key]['q75']:.3f}]")

    return results


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t0 = time.time()

    stage1 = run_stage1()
    stage2 = run_stage2()
    stage3 = run_stage3(stage2)
    lr_interaction = run_lr_interaction()

    elapsed = time.time() - t0
    print(f"\nTotal elapsed: {elapsed/60:.1f} min")

    # Serialize with string keys for JSON
    def jsonify(d):
        if isinstance(d, dict):
            return {str(k): jsonify(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [jsonify(i) for i in d]
        elif isinstance(d, float):
            return round(d, 8)
        else:
            return d

    output = {
        "stage1": jsonify(stage1),
        "stage2": jsonify(stage2),
        "stage3": jsonify(stage3),
        "lr_interaction": {f"lr={k[0]:.0e}_eps={k[1]:.0e}": jsonify(v)
                           for k, v in lr_interaction.items()},
        "elapsed_seconds": round(elapsed, 1),
    }

    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Results written to results.json")
