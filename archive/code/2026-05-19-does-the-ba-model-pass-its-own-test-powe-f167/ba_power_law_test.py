#!/usr/bin/env python3
"""
ba_power_law_test.py

Does the BA Model Pass Its Own Test? Power-Law Convergence in Finite
Preferential-Attachment Networks.

Full run:   python ba_power_law_test.py             (~47 min on a modern laptop)
Quick run:  python ba_power_law_test.py --quick     (~7 min, 5 replicates × 100 bootstrap)

Requirements (install once):
    pip install numpy scipy networkx powerlaw

All seeds are derived deterministically from MASTER_SEED = 42; re-running
produces bit-identical results on the same platform. Results are written
to results.json; the summary table is printed to stdout.
"""

import argparse
import json
import math
import sys

import networkx as nx
import numpy as np
from scipy.special import zeta as sp_zeta

# ── Configuration ─────────────────────────────────────────────────────────────

MASTER_SEED  = 42
SIZES        = [500, 1000, 2500, 5000, 10000, 25000, 50000]
M_VALUES     = [2, 3]
P_THRESHOLD  = 0.1   # CSN threshold: p >= 0.1 → "pass"
MIN_TAIL     = 5     # halt x_min scan when fewer than this many nodes remain

N_REP_FULL   = 50
N_REP_QUICK  = 5
N_BOOT_FULL  = 200
N_BOOT_QUICK = 100


# ── Hurwitz zeta ──────────────────────────────────────────────────────────────

def hzeta(alpha: float, x):
    """Hurwitz ζ(α, x) = Σ_{n≥0} 1/(x+n)^α  — x may be float or ndarray."""
    return sp_zeta(alpha, x)


# ── Maximum-likelihood estimator ───────────────────────────────────────────────

def mle_alpha(degrees_arr: np.ndarray, xmin: int):
    """
    CSN discrete MLE (Clauset, Shalizi & Newman 2009, eq. B.15):
        α̂ = 1 + n · [Σ ln(kᵢ / (xmin − 0.5))]⁻¹

    Returns (alpha, n_tail) or (None, 0) when the tail is too small or
    degenerate.
    """
    tail = degrees_arr[degrees_arr >= xmin]
    n = len(tail)
    if n < MIN_TAIL:
        return None, 0
    log_sum = float(np.sum(np.log(tail / (xmin - 0.5))))
    if log_sum <= 0:
        return None, 0
    return 1.0 + n / log_sum, n


# ── KS statistic ───────────────────────────────────────────────────────────────

def ks_statistic(degrees_arr: np.ndarray, alpha: float, xmin: int) -> float:
    """
    KS distance between the empirical tail CDF and the fitted discrete power law.

    Computed at each *unique degree value* after counting all ties.  The naive
    per-data-point approach inflates KS by up to 20× for degree sequences with
    many identical low-degree nodes.

    Theoretical CDF: P(X ≤ k) = 1 − ζ(α, k+1) / ζ(α, xmin)
    """
    tail = np.sort(degrees_arr[degrees_arr >= xmin])
    n = len(tail)
    if n < MIN_TAIL:
        return float('inf')

    unique_vals, counts = np.unique(tail, return_counts=True)
    empirical_cdf = np.cumsum(counts) / n

    norm = hzeta(alpha, float(xmin))
    theoretical_cdf = 1.0 - hzeta(alpha, unique_vals + 1.0) / norm

    return float(np.max(np.abs(empirical_cdf - theoretical_cdf)))


# ── x_min scan ────────────────────────────────────────────────────────────────

def fit_csn(degrees_arr: np.ndarray):
    """
    Full CSN x_min scan: evaluate every unique degree as a candidate lower
    cutoff and return the (xmin, alpha, ks, n_tail) tuple minimising KS.

    Returns None if no valid fit is found.
    """
    unique_vals = np.unique(degrees_arr).astype(int)
    best = None

    for xmin in unique_vals:
        alpha, n_tail = mle_alpha(degrees_arr, xmin)
        if alpha is None or alpha <= 1.0:
            continue
        ks = ks_statistic(degrees_arr, alpha, xmin)
        if best is None or ks < best[2]:
            best = (int(xmin), alpha, ks, n_tail)

    return best


# ── Discrete power-law sampler ────────────────────────────────────────────────

def make_pmf(alpha: float, xmin: int, max_k: int = None):
    """
    Precompute the PMF of Discrete-PL(α, xmin) over k = xmin … max_k.

    P(k) = [ζ(α, k) − ζ(α, k+1)] / ζ(α, xmin)   (Hurwitz difference formula)
    """
    if max_k is None:
        max_k = max(xmin * 200, 3000)
    ks = np.arange(xmin, max_k + 1, dtype=float)
    norm = hzeta(alpha, float(xmin))
    pmf = (hzeta(alpha, ks) - hzeta(alpha, ks + 1)) / norm
    pmf = np.maximum(pmf, 0.0)
    pmf /= pmf.sum()   # renormalise to absorb far-tail truncation
    return ks.astype(int), pmf


# ── Bootstrap p-value ──────────────────────────────────────────────────────────

def bootstrap_pvalue(
    degrees_arr: np.ndarray,
    xmin: int,
    alpha: float,
    n_tail: int,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> float:
    """
    CSN parametric bootstrap (step 3 of the three-step CSN procedure).

    Each synthetic dataset:
      • below-xmin values: resampled with replacement from the empirical
        below-xmin distribution.
      • tail values: drawn from Discrete-PL(α, xmin).

    p-value = fraction of synthetic KS statistics ≥ observed KS statistic.
    """
    observed_ks = ks_statistic(degrees_arr, alpha, xmin)
    n = len(degrees_arr)
    n_below = n - n_tail
    below = degrees_arr[degrees_arr < xmin]

    # Precompute the tail PMF once; reuse across all bootstrap replicates.
    max_k = int(np.max(degrees_arr)) * 3 + 200
    pl_ks, pl_pmf = make_pmf(alpha, xmin, max_k)

    exceed = 0
    for _ in range(n_bootstrap):
        syn_below = (
            rng.choice(below, size=n_below, replace=True)
            if n_below > 0 and len(below) > 0
            else np.array([], dtype=int)
        )
        syn_tail = rng.choice(pl_ks, size=n_tail, p=pl_pmf, replace=True)
        syn = np.concatenate([syn_below, syn_tail]).astype(float)

        fit = fit_csn(syn)
        if fit is None:
            continue
        _, _, sks, _ = fit
        if sks >= observed_ks:
            exceed += 1

    return exceed / n_bootstrap


# ── Full CSN test ──────────────────────────────────────────────────────────────

def csn_test(degrees, n_bootstrap: int, rng: np.random.Generator) -> dict:
    """Run the full three-step CSN test on a degree sequence."""
    arr = np.array(degrees, dtype=float)
    fit = fit_csn(arr)
    if fit is None:
        return dict(passes=False, p=0.0, alpha=None, xmin=None, n_tail=0, ks=None)

    xmin, alpha, ks, n_tail = fit
    p = bootstrap_pvalue(arr, xmin, alpha, n_tail, n_bootstrap, rng)
    return dict(
        passes=p >= P_THRESHOLD,
        p=p, alpha=alpha, xmin=xmin, n_tail=n_tail, ks=ks,
    )


# ── BA network ────────────────────────────────────────────────────────────────

def ba_degrees(n: int, m: int, seed: int):
    G = nx.barabasi_albert_graph(n, m, seed=seed)
    return list(dict(G.degree()).values())


# ── Wilson confidence interval ────────────────────────────────────────────────

def wilson_ci(k: int, n: int, z: float = 1.96):
    """95% Wilson interval for a proportion k/n."""
    p = k / n
    d = 1.0 + z ** 2 / n
    centre = (p + z ** 2 / (2 * n)) / d
    margin = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / d
    return max(0.0, centre - margin), min(1.0, centre + margin)


# ── i.i.d. sanity check ───────────────────────────────────────────────────────

def run_iid_sanity():
    """
    Verify the implementation on i.i.d. discrete power-law samples with known
    α ∈ {2.0, 3.0, 4.0}, xmin=2, n=2000.  All should pass (p ≥ 0.1) and
    recover α̂ close to the true value.
    """
    print("\nSanity check — i.i.d. discrete power-law samples (n=2000, xmin=2):")
    rng = np.random.default_rng(MASTER_SEED + 9999)
    for alpha_true in [2.0, 3.0, 4.0]:
        pl_ks, pl_pmf = make_pmf(alpha_true, xmin=2, max_k=5000)
        sample = rng.choice(pl_ks, size=2000, p=pl_pmf, replace=True)
        res = csn_test(sample.tolist(), n_bootstrap=200, rng=rng)
        print(
            f"  α_true={alpha_true:.1f}  α̂={res['alpha']:.3f}  "
            f"xmin={res['xmin']}  p={res['p']:.3f}  "
            f"pass={'Y' if res['passes'] else 'N'}"
        )


# ── Main sweep ────────────────────────────────────────────────────────────────

def run_sweep(n_rep: int, n_boot: int) -> dict:
    """
    Sweep over all (N, m) conditions.  Network seeds are derived from
    MASTER_SEED in a deterministic order; bootstrap RNGs are separate
    (derived from net_seed + 10^6) to avoid interference.
    """
    rng_master = np.random.default_rng(MASTER_SEED)
    n_total = n_rep * len(SIZES) * len(M_VALUES)
    all_seeds = rng_master.integers(0, 2 ** 31 - 1, size=n_total).tolist()
    seed_idx = 0

    results = {}
    for m in M_VALUES:
        for n in SIZES:
            passes, alphas = [], []
            for rep in range(n_rep):
                net_seed = all_seeds[seed_idx]
                seed_idx += 1
                degrees = ba_degrees(n, m, net_seed)
                rng = np.random.default_rng(net_seed + 10 ** 6)
                res = csn_test(degrees, n_boot, rng)
                passes.append(int(res['passes']))
                if res['alpha'] is not None:
                    alphas.append(res['alpha'])
                sys.stdout.write(
                    f"\r  m={m} N={n:6d}  rep {rep+1:3d}/{n_rep}  "
                    f"pass={sum(passes)}/{len(passes)}"
                )
                sys.stdout.flush()
            print()

            k = sum(passes)
            lo, hi = wilson_ci(k, n_rep)
            results[f"m{m}_n{n}"] = dict(
                m=m, n=n,
                pass_rate=round(k / n_rep, 4),
                n_pass=k, n_rep=n_rep,
                wilson_lo=round(lo, 3),
                wilson_hi=round(hi, 3),
                mean_alpha=(round(float(np.mean(alphas)), 4) if alphas else None),
                sd_alpha=(round(float(np.std(alphas, ddof=0)), 4) if alphas else None),
            )
    return results


# ── Table printer ─────────────────────────────────────────────────────────────

def print_table(results: dict):
    print(
        "\nTable 1. Pass rate (p ≥ 0.1), 95% Wilson CI, "
        "mean MLE exponent (±SD)\n"
    )
    hdr = (
        "| N | m=2 pass | 95% CI | m=2 α̂ (±SD) |"
        " m=3 pass | 95% CI | m=3 α̂ (±SD) |"
    )
    sep = "|---|---|---|---|---|---|---|"
    print(hdr)
    print(sep)
    for n in SIZES:
        row = f"| {n} |"
        for m in M_VALUES:
            r = results[f"m{m}_n{n}"]
            ci = f"[{r['wilson_lo']:.2f}, {r['wilson_hi']:.2f}]"
            ae = f"{r['mean_alpha']:.2f} ± {r['sd_alpha']:.2f}"
            row += f" {r['pass_rate']:.2f} | {ci} | {ae} |"
        print(row)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="CSN power-law test sweep over BA networks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help=f"Run {N_REP_QUICK} replicates × {N_BOOT_QUICK} bootstrap (~7 min)",
    )
    args = parser.parse_args()

    n_rep  = N_REP_QUICK  if args.quick else N_REP_FULL
    n_boot = N_BOOT_QUICK if args.quick else N_BOOT_FULL

    print(
        f"BA power-law sweep | seed={MASTER_SEED} | "
        f"{n_rep} replicates × {n_boot} bootstrap"
    )
    print("=" * 65)

    run_iid_sanity()

    print(f"\nMain sweep ({n_rep} replicates × {n_boot} bootstrap):")
    results = run_sweep(n_rep, n_boot)
    print_table(results)

    out = "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results written to {out}")


if __name__ == "__main__":
    main()
