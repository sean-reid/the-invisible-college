#!/usr/bin/env python3
"""
CI Coverage Simulation - Pre-registered Analysis Plan
Date: 2026-05-27

Tests four confidence interval methods across six distributions and eight
sample sizes. Coverage = fraction of N_TRIALS trials where true mean falls
inside the interval.

Methods:
  1. Student-t (scipy.stats.t.interval)
  2. Basic bootstrap (reflected percentile: 2*x_bar - pct)
  3. Percentile bootstrap (direct percentiles of bootstrap means)
  4. BCa bootstrap (bias-corrected and accelerated)

Distributions:
  Normal(0,1), t(3), Lognormal(0,1), Exponential(1), Pareto(2.5), Beta(0.5,0.5)

Sample sizes: n in {5, 10, 15, 20, 30, 50, 100, 200}

Pre-registered thresholds:
  Failure:      coverage < 0.90  (flagged as 'F' in tables)
  Undercoverage: coverage < 0.93  (flagged as 'U')
  Well-calibrated: 0.93 <= coverage <= 0.97
  Overcoverage:  coverage > 0.97  (flagged as 'O')
  Degenerate:   > 2% of trials produce degenerate intervals (flagged separately)

Reproducibility: MASTER_SEED = 20260527
  Per-cell seed: MASTER_SEED + dist_idx * len(SAMPLE_SIZES) + n_idx
  Bootstrap resamples shared across bootstrap methods within each trial.

True means (pre-computed, not estimated):
  Normal(0,1):    0.0
  t(3):           0.0
  Lognormal(0,1): exp(0.5) ≈ 1.64872
  Exponential(1): 1.0
  Pareto(2.5):    alpha/(alpha-1) = 2.5/1.5 ≈ 1.66667
  Beta(0.5,0.5):  0.5

BCa acceleration for the mean: closed-form via jackknife.
  L_i = x_i - x_bar  (influence function of the sample mean)
  a = sum(L_i^3) / (6 * sum(L_i^2)^1.5)
"""

import numpy as np
from scipy import stats
import json
import sys
import time

# ============================================================
# PRE-REGISTERED CONSTANTS
# ============================================================
MASTER_SEED = 20260527
B_BOOTSTRAP = 999
N_TRIALS = 10_000
ALPHA = 0.05

DIST_NAMES = [
    'Normal(0,1)',
    't(3)',
    'Lognormal(0,1)',
    'Exponential(1)',
    'Pareto(2.5)',
    'Beta(0.5,0.5)',
]

DIST_TRUE_MEANS = {
    'Normal(0,1)':    0.0,
    't(3)':           0.0,
    'Lognormal(0,1)': float(np.exp(0.5)),   # exp(mu + sigma^2/2), mu=0, sigma=1
    'Exponential(1)': 1.0,
    'Pareto(2.5)':    5.0 / 3.0,            # alpha/(alpha-1) with alpha=2.5
    'Beta(0.5,0.5)':  0.5,
}

SAMPLE_SIZES = [5, 10, 15, 20, 30, 50, 100, 200]

METHOD_NAMES = [
    'Student-t',
    'Basic Bootstrap',
    'Percentile Bootstrap',
    'BCa Bootstrap',
]


# ============================================================
# DISTRIBUTION SAMPLER
# ============================================================
def sample_dist(dist_name: str, n: int, rng: np.random.Generator) -> np.ndarray:
    """Draw n IID samples from the named distribution."""
    if dist_name == 'Normal(0,1)':
        return rng.normal(0.0, 1.0, n)
    elif dist_name == 't(3)':
        return rng.standard_t(3, n)
    elif dist_name == 'Lognormal(0,1)':
        return rng.lognormal(0.0, 1.0, n)
    elif dist_name == 'Exponential(1)':
        return rng.exponential(1.0, n)
    elif dist_name == 'Pareto(2.5)':
        # numpy.random.pareto generates Pareto II (Lomax) with support [0, inf).
        # Adding 1 gives Pareto I with support [1, inf) and mean = alpha/(alpha-1).
        return rng.pareto(2.5, n) + 1.0
    elif dist_name == 'Beta(0.5,0.5)':
        return rng.beta(0.5, 0.5, n)
    else:
        raise ValueError(f'Unknown distribution: {dist_name}')


# ============================================================
# BCa CI IMPLEMENTATION
# ============================================================
def bca_ci(
    data: np.ndarray,
    bootstrap_means: np.ndarray,
    alpha: float = 0.05,
) -> tuple[float | None, float | None, bool]:
    """
    Bias-corrected and accelerated (BCa) confidence interval for the mean.

    Parameters
    ----------
    data            : original sample of shape (n,)
    bootstrap_means : B bootstrap sample means of shape (B,)
    alpha           : significance level (0.05 → 95% CI)

    Returns
    -------
    (lower, upper, is_degenerate)
      is_degenerate is True when the interval cannot be computed reliably.
    """
    n = len(data)
    theta_hat = float(np.mean(data))
    B = len(bootstrap_means)

    # --- Bias correction z0 ---
    prop_less = float(np.mean(bootstrap_means < theta_hat))
    # Avoid Phi^{-1}(0) or Phi^{-1}(1); clamp to (0.5/B, 1 - 0.5/B)
    prop_less = float(np.clip(prop_less, 0.5 / B, 1.0 - 0.5 / B))
    z0 = float(stats.norm.ppf(prop_less))

    # --- Acceleration a (closed-form for the mean) ---
    # Jackknife influence function: L_i = x_i - x_bar
    L = data - theta_hat
    sum_L2 = float(np.sum(L ** 2))
    if sum_L2 < 1e-15:
        a = 0.0
    else:
        a = float(np.sum(L ** 3)) / (6.0 * sum_L2 ** 1.5)

    # --- Adjusted quantile levels ---
    z_lo = float(stats.norm.ppf(alpha / 2))        # ≈ -1.96
    z_hi = float(stats.norm.ppf(1.0 - alpha / 2))  # ≈ +1.96

    def adj_q(z_val: float) -> float:
        inner = z0 + z_val
        denom = 1.0 - a * inner
        if abs(denom) < 1e-10:
            # Avoid division by zero; fall back to percentile quantile
            return alpha / 2 if z_val < 0 else 1.0 - alpha / 2
        return float(stats.norm.cdf(z0 + inner / denom))

    a1 = float(np.clip(adj_q(z_lo), 1.0 / (B + 1), 1.0 - 1.0 / (B + 1)))
    a2 = float(np.clip(adj_q(z_hi), 1.0 / (B + 1), 1.0 - 1.0 / (B + 1)))

    if a1 >= a2:
        # Quantiles crossed: degenerate interval
        return None, None, True

    lo = float(np.quantile(bootstrap_means, a1))
    hi = float(np.quantile(bootstrap_means, a2))
    return lo, hi, False


# ============================================================
# CELL RUNNER
# ============================================================
def run_cell(dist_name: str, n: int, cell_seed: int) -> dict:
    """
    Run N_TRIALS trials for one (distribution, sample-size) cell.

    Bootstrap resamples are shared across the three bootstrap methods
    within each trial (reduces compute; does not bias coverage estimates).
    """
    rng = np.random.default_rng(cell_seed)
    true_mean = DIST_TRUE_MEANS[dist_name]

    covered   = {m: 0 for m in METHOD_NAMES}
    degenerate = {m: 0 for m in METHOD_NAMES}

    for _ in range(N_TRIALS):
        data  = sample_dist(dist_name, n, rng)
        x_bar = float(np.mean(data))

        # --- Student-t ---
        sem = float(stats.sem(data))
        if sem > 0.0:
            lo_t, hi_t = stats.t.interval(
                1.0 - ALPHA, df=n - 1, loc=x_bar, scale=sem
            )
            if lo_t <= true_mean <= hi_t:
                covered['Student-t'] += 1
        else:
            degenerate['Student-t'] += 1

        # --- Bootstrap resamples (shared) ---
        idx = rng.integers(0, n, size=(B_BOOTSTRAP, n))
        bs_means = data[idx].mean(axis=1)

        # --- Percentile bootstrap ---
        lo_p = float(np.quantile(bs_means, ALPHA / 2))
        hi_p = float(np.quantile(bs_means, 1.0 - ALPHA / 2))
        if lo_p <= true_mean <= hi_p:
            covered['Percentile Bootstrap'] += 1

        # --- Basic bootstrap (reflected) ---
        lo_b = 2.0 * x_bar - float(np.quantile(bs_means, 1.0 - ALPHA / 2))
        hi_b = 2.0 * x_bar - float(np.quantile(bs_means, ALPHA / 2))
        if lo_b <= true_mean <= hi_b:
            covered['Basic Bootstrap'] += 1

        # --- BCa bootstrap ---
        lo_bca, hi_bca, is_deg = bca_ci(data, bs_means, ALPHA)
        if is_deg:
            degenerate['BCa Bootstrap'] += 1
        elif lo_bca <= true_mean <= hi_bca:
            covered['BCa Bootstrap'] += 1

    return {
        m: {
            'coverage':        covered[m]    / N_TRIALS,
            'degenerate_rate': degenerate[m] / N_TRIALS,
        }
        for m in METHOD_NAMES
    }


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    print("CI Coverage Simulation")
    print(f"  Master seed : {MASTER_SEED}")
    print(f"  N trials    : {N_TRIALS:,}")
    print(f"  B bootstrap : {B_BOOTSTRAP}")
    print(f"  Alpha       : {ALPHA}")
    print()

    results: dict = {}
    total_cells = len(DIST_NAMES) * len(SAMPLE_SIZES)
    cell_idx = 0
    t0 = time.time()

    for di, dist_name in enumerate(DIST_NAMES):
        results[dist_name] = {}
        for ni, n in enumerate(SAMPLE_SIZES):
            cell_seed = MASTER_SEED + di * len(SAMPLE_SIZES) + ni
            t_cell = time.time()
            print(
                f"[{cell_idx + 1:2d}/{total_cells}] {dist_name}, n={n:3d} "
                f"(seed={cell_seed}) ...",
                end=' ', flush=True
            )
            cell_res = run_cell(dist_name, n, cell_seed)
            results[dist_name][str(n)] = cell_res
            dt = time.time() - t_cell
            print(f"done ({dt:.1f}s)")
            cell_idx += 1

    print(f"\nTotal elapsed: {time.time() - t0:.1f}s")

    # Save raw results
    with open('coverage_results.json', 'w') as fh:
        json.dump(results, fh, indent=2)
    print("Saved: coverage_results.json")

    # ---- Text report ----
    def flag(c: float) -> str:
        if c < 0.90:  return 'F'
        if c < 0.93:  return 'U'
        if c > 0.97:  return 'O'
        return ' '

    print()
    for method in METHOD_NAMES:
        print(f"\n{'='*70}")
        print(f"  {method}")
        print(f"{'='*70}")
        header = f"{'Distribution':<20s} " + "  ".join(f"n={n:<3d}" for n in SAMPLE_SIZES)
        print(header)
        print('-' * len(header))
        for dist_name in DIST_NAMES:
            row = f"{dist_name:<20s} "
            for n in SAMPLE_SIZES:
                c = results[dist_name][str(n)][method]['coverage']
                row += f" {c:.3f}{flag(c)} "
            print(row)

    # ---- Min-n summary ----
    print(f"\n{'='*70}")
    print("  Minimum n to reach and sustain coverage >= 0.930")
    print(f"{'='*70}")
    header = f"{'Distribution':<20s} " + "  ".join(f"{m[:6]:<8s}" for m in METHOD_NAMES)
    print(header)
    for dist_name in DIST_NAMES:
        row = f"{dist_name:<20s} "
        for method in METHOD_NAMES:
            min_n = None
            covs = [results[dist_name][str(n)][method]['coverage'] for n in SAMPLE_SIZES]
            # Find smallest n such that all subsequent n also >= 0.93
            for i, n in enumerate(SAMPLE_SIZES):
                if all(covs[j] >= 0.93 for j in range(i, len(SAMPLE_SIZES))):
                    min_n = n
                    break
            label = str(min_n) if min_n is not None else '>200'
            row += f" {label:<8s}"
        print(row)

    # ---- Degenerate-rate report ----
    print(f"\n{'='*70}")
    print("  Degenerate interval rates (BCa Bootstrap only)")
    print(f"{'='*70}")
    header = f"{'Distribution':<20s} " + "  ".join(f"n={n:<3d}" for n in SAMPLE_SIZES)
    print(header)
    for dist_name in DIST_NAMES:
        row = f"{dist_name:<20s} "
        has_any = False
        for n in SAMPLE_SIZES:
            dr = results[dist_name][str(n)]['BCa Bootstrap']['degenerate_rate']
            mark = '*' if dr > 0.02 else ' '
            row += f" {dr:.3f}{mark} "
            if dr > 0 : has_any = True
        if has_any:
            print(row)

    print("\nDone.")


if __name__ == '__main__':
    main()
