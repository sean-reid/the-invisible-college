#!/usr/bin/env python3
"""
The Calculator's Share: floating-point error in BCa acceleration vs sampling noise.
Protocol: Ada Lovelace, Invisible College, 2026-06-21.

Pre-committed thresholds (from proposal):
  meaningful: relative error in a > 1e-6 for > 5% of samples in a cell
  dominant:   |BCa-double coverage - BCa-mpmath coverage| > 0.5 percentage points
"""

import json
import time
import numpy as np
from scipy import stats
from mpmath import mp, mpf

# ===================================================================
# Core computation functions
# ===================================================================

def acc_double(x):
    """BCa acceleration via jackknife, IEEE 754 double precision.
    Formula: a = sum(d^3) / (6 * sum(d^2)^1.5)
    where d_i = (x_i - mean(x)) / (n-1).
    """
    n = len(x)
    mu = np.mean(x)
    d = (x - mu) / (n - 1)
    num = np.sum(d**3)
    den = np.sum(d**2)
    if den == 0.0:
        return 0.0
    return float(num / (6.0 * den**1.5))


def acc_mp(x, prec=256):
    """BCa acceleration via jackknife, mpmath at `prec` bits. Returns float."""
    mp.prec = prec
    n = len(x)
    xm = [mpf(str(xi)) for xi in x]    # str() avoids implicit double rounding
    mu = sum(xm) / n
    d = [(xi - mu) / (n - 1) for xi in xm]
    num = sum(di**3 for di in d)
    den = sum(di**2 for di in d)
    if den == 0:
        return 0.0
    return float(num / (6 * den**mpf('1.5')))


def bca_from_boot(theta_hat, theta_boot, a, alpha=0.05):
    """BCa 95% CI given pre-computed bootstrap replications and acceleration a."""
    B = len(theta_boot)
    p0 = float(np.mean(theta_boot < theta_hat))
    p0 = float(np.clip(p0, 0.5/B, 1.0 - 0.5/B))
    z0 = float(stats.norm.ppf(p0))
    z_lo = float(stats.norm.ppf(alpha / 2))
    z_hi = float(stats.norm.ppf(1 - alpha / 2))
    a = float(a)

    def adj(z):
        den = 1.0 - a * (z0 + z)
        if abs(den) < 1e-12:
            return 0.001 if z < 0 else 0.999
        return float(stats.norm.cdf(z0 + (z0 + z) / den))

    p1 = float(np.clip(adj(z_lo), 0.001, 0.999))
    p2 = float(np.clip(adj(z_hi), 0.001, 0.999))
    lo = float(np.quantile(theta_boot, p1))
    hi = float(np.quantile(theta_boot, p2))
    return lo, hi


# ===================================================================
# Pre-flight check
# ===================================================================

print("=" * 68)
print("PRE-FLIGHT CHECK: t(df=3), n=50, convergence at 128/256/512 bits")
print("=" * 68)
rng_pf = np.random.default_rng(20260621)
n_conv = 0
max_disc = 0.0
N_TRIALS = 30

t0 = time.time()
for i in range(N_TRIALS):
    x = rng_pf.standard_t(df=3, size=50)
    a128 = acc_mp(x, 128)
    a256 = acc_mp(x, 256)
    a512 = acc_mp(x, 512)
    adbl = acc_double(x)
    ref = a512
    disc = abs(a256 - a512) / max(abs(ref), 1e-20)
    max_disc = max(max_disc, disc)
    if disc < 1e-10:
        n_conv += 1
    if i < 5:
        print(f"  sample {i:02d}:  a_dbl={adbl:+.6e}  a_128={a128:+.6e}  "
              f"a_256={a256:+.6e}  a_512={a512:+.6e}  disc={disc:.1e}")

elapsed_pf = time.time() - t0
print(f"\nPre-flight: {N_TRIALS} samples in {elapsed_pf:.1f}s "
      f"({elapsed_pf/N_TRIALS*1000:.1f}ms/sample at 3 precision levels)")
print(f"Converged (256 vs 512 < 1e-10): {n_conv}/{N_TRIALS}")
print(f"Max discrepancy 256 vs 512: {max_disc:.2e}")

if n_conv >= int(0.9 * N_TRIALS):
    REF_PREC = 256
    print("=> Reference precision: 256 bits\n")
else:
    REF_PREC = 512
    print("=> Escalating to 512-bit reference\n")

# ===================================================================
# Timing calibration: estimate per-cell time
# ===================================================================

print("TIMING CALIBRATION: 20 mpmath calls per n value")
for n_test in [50, 100, 200, 500]:
    rng_t = np.random.default_rng(999)
    x_test = rng_t.standard_t(df=3, size=n_test)
    t0 = time.time()
    for _ in range(20):
        acc_mp(x_test, REF_PREC)
    elapsed = (time.time() - t0) / 20 * 1000
    print(f"  n={n_test:3d}: {elapsed:.2f}ms per mpmath call")

# ===================================================================
# Main experiment
# ===================================================================

CELLS = [
    ('t_2.5',   't',     2.5,  0.0),
    ('t_3.0',   't',     3.0,  0.0),
    ('t_3.5',   't',     3.5,  0.0),
    ('t_4.0',   't',     4.0,  0.0),
    ('t_5.0',   't',     5.0,  0.0),
    ('t_10.0',  't',    10.0,  0.0),
    ('par_2.0', 'pareto', 2.0,  2.0),
    ('par_2.5', 'pareto', 2.5,  5.0/3.0),
    ('par_3.0', 'pareto', 3.0,  1.5),
    ('par_4.0', 'pareto', 4.0,  4.0/3.0),
]
NS = [50, 100, 200, 500]
N_SAM = 2000    # samples per cell
B_BOOT = 500    # bootstrap resamples per sample

print(f"\n{'='*68}")
print(f"MAIN EXPERIMENT  N_SAM={N_SAM}  B_BOOT={B_BOOT}  REF_PREC={REF_PREC}")
print(f"{'='*68}")
hdr = (f"{'Cell':<22} {'med_rerr':>10} {'p95_rerr':>10} {'frac>1e-6':>10}"
       f" {'cov_dbl':>8} {'cov_mp':>8} {'cov_pct':>8} {'gap_pp':>8}")
print(hdr)

results = []
t_start = time.time()

for (dname, dtype, param, pop_mu) in CELLS:
    for n in NS:
        key = f"{dname}_n{n}"
        seed = int(abs(hash(key))) % (2**31 - 1)
        rng_s = np.random.default_rng(seed)
        rng_b = np.random.default_rng(seed ^ 0xDEADBEEF)

        if dtype == 't':
            data = rng_s.standard_t(df=param, size=(N_SAM, n))
        else:
            # Pareto with shape param, location 1: mean = param/(param-1)
            data = rng_s.pareto(a=param - 1, size=(N_SAM, n)) + 1.0

        rel_errs  = np.empty(N_SAM)
        abs_errs  = np.empty(N_SAM)
        cov_dbl   = np.empty(N_SAM, dtype=bool)
        cov_mp    = np.empty(N_SAM, dtype=bool)
        cov_pct   = np.empty(N_SAM, dtype=bool)

        for i in range(N_SAM):
            x = data[i]
            a_d = acc_double(x)
            a_m = acc_mp(x, REF_PREC)

            abs_errs[i] = abs(a_d - a_m)
            rel_errs[i] = abs_errs[i] / max(abs(a_m), 1e-15)

            # Bootstrap — same for both BCa versions
            theta_hat = float(np.mean(x))
            boot_idx  = rng_b.integers(0, n, size=(B_BOOT, n))
            theta_boot = data[i][boot_idx].mean(axis=1)

            lo_d, hi_d = bca_from_boot(theta_hat, theta_boot, a_d)
            cov_dbl[i] = lo_d <= pop_mu <= hi_d

            lo_m, hi_m = bca_from_boot(theta_hat, theta_boot, a_m)
            cov_mp[i]  = lo_m <= pop_mu <= hi_m

            lo_p = float(np.percentile(theta_boot, 2.5))
            hi_p = float(np.percentile(theta_boot, 97.5))
            cov_pct[i] = lo_p <= pop_mu <= hi_p

        row = dict(
            cell=key, dist=dname, n=n,
            med_rerr=float(np.median(rel_errs)),
            p95_rerr=float(np.percentile(rel_errs, 95)),
            p99_rerr=float(np.percentile(rel_errs, 99)),
            med_abserr=float(np.median(abs_errs)),
            p95_abserr=float(np.percentile(abs_errs, 95)),
            p99_abserr=float(np.percentile(abs_errs, 99)),
            frac_meaningful=float(np.mean(rel_errs > 1e-6)),
            cov_dbl=float(np.mean(cov_dbl)),
            cov_mp=float(np.mean(cov_mp)),
            cov_pct=float(np.mean(cov_pct)),
            gap_pp=float((np.mean(cov_dbl) - np.mean(cov_mp)) * 100),
        )
        results.append(row)

        elapsed_total = time.time() - t_start
        print(f"{key:<22} {row['med_rerr']:>10.2e} {row['p95_rerr']:>10.2e}"
              f" {row['frac_meaningful']:>10.4f}"
              f" {row['cov_dbl']:>8.4f} {row['cov_mp']:>8.4f}"
              f" {row['cov_pct']:>8.4f} {row['gap_pp']:>+8.3f}"
              f"  [{elapsed_total:.0f}s]")

with open('results.json', 'w') as f:
    json.dump({'ref_prec': REF_PREC, 'n_sam': N_SAM, 'b_boot': B_BOOT,
               'results': results}, f, indent=2)

print(f"\nTotal elapsed: {time.time() - t_start:.1f}s")
print("Results saved to results.json")

# ===================================================================
# Threshold evaluation
# ===================================================================

print(f"\n{'='*68}")
print("THRESHOLD EVALUATION")
print(f"{'='*68}")
print("Pre-committed: 'meaningful' = frac > 5% with rel_err > 1e-6")
print("               'dominant'   = |gap| > 0.5 pp")

meaningful = [r for r in results if r['frac_meaningful'] > 0.05]
dominant   = [r for r in results if abs(r['gap_pp']) > 0.5]

print(f"\nCells with 'meaningful' numerical error: {len(meaningful)}")
for r in meaningful:
    print(f"  {r['cell']:22s}  frac={r['frac_meaningful']:.4f}"
          f"  med_abserr={r['med_abserr']:.2e}"
          f"  p95_abserr={r['p95_abserr']:.2e}")

print(f"\nCells with 'dominant' coverage gap (>0.5pp): {len(dominant)}")
for r in dominant:
    print(f"  {r['cell']:22s}  gap={r['gap_pp']:+.3f}pp"
          f"  cov_dbl={r['cov_dbl']:.4f}  cov_mp={r['cov_mp']:.4f}")

if not meaningful:
    print("\n=> No cells exceeded the 'meaningful' threshold.")
    print("   Floating-point error in a does not contribute measurably to BCa coverage failure.")
if not dominant:
    print("=> No cells exceeded the 'dominant' threshold.")
    print("   Coverage is indistinguishable between BCa-double and BCa-mpmath.")
