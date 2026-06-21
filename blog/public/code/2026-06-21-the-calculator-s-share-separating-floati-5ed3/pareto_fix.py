#!/usr/bin/env python3
"""
Corrected Pareto cells only.
Bug: was using numpy.pareto(a=param-1) + 1 = Pareto(alpha=param-1)
Fix: use numpy.pareto(a=param) + 1 = Pareto(alpha=param)
This script re-runs just the 4 Pareto distributions.
"""

import json, time
import numpy as np
from scipy import stats
from mpmath import mp, mpf

REF_PREC = 256

def acc_double(x):
    n = len(x)
    mu = np.mean(x)
    d = (x - mu) / (n - 1)
    num = np.sum(d**3)
    den = np.sum(d**2)
    if den == 0.0:
        return 0.0
    return float(num / (6.0 * den**1.5))

def acc_mp(x, prec=256):
    mp.prec = prec
    n = len(x)
    xm = [mpf(str(xi)) for xi in x]
    mu = sum(xm) / n
    d = [(xi - mu) / (n - 1) for xi in xm]
    num = sum(di**3 for di in d)
    den = sum(di**2 for di in d)
    if den == 0:
        return 0.0
    return float(num / (6 * den**mpf('1.5')))

def bca_from_boot(theta_hat, theta_boot, a, alpha=0.05):
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
    return float(np.quantile(theta_boot, p1)), float(np.quantile(theta_boot, p2))

# Verify parameterization: numpy.pareto(a) + 1 = Pareto(alpha=a), mean = a/(a-1) for a>1
print("PARAMETERIZATION VERIFICATION")
for alpha in [2.0, 2.5, 3.0, 4.0]:
    rng_v = np.random.default_rng(12345)
    x_v = rng_v.pareto(a=alpha, size=1_000_000) + 1.0
    theo_mean = alpha / (alpha - 1)
    emp_mean = x_v.mean()
    print(f"  Pareto(alpha={alpha}): theoretical mean={theo_mean:.4f}, empirical mean={emp_mean:.4f}")

CELLS = [
    ('par_2.0', 2.0,  2.0),
    ('par_2.5', 2.5,  5.0/3.0),
    ('par_3.0', 3.0,  1.5),
    ('par_4.0', 4.0,  4.0/3.0),
]
NS = [50, 100, 200, 500]
N_SAM = 2000
B_BOOT = 500

print(f"\nRE-RUNNING PARETO CELLS  N_SAM={N_SAM}  B_BOOT={B_BOOT}")
hdr = (f"{'Cell':<22} {'med_rerr':>10} {'p95_rerr':>10} {'frac>1e-6':>10}"
       f" {'cov_dbl':>8} {'cov_mp':>8} {'cov_pct':>8} {'gap_pp':>8}")
print(hdr)

pareto_results = []
t_start = time.time()

for (dname, alpha, pop_mu) in CELLS:
    for n in NS:
        key = f"{dname}_n{n}_fixed"
        seed = int(abs(hash(key))) % (2**31 - 1)
        rng_s = np.random.default_rng(seed)
        rng_b = np.random.default_rng(seed ^ 0xDEADBEEF)

        # CORRECTED: numpy.pareto(a=alpha) + 1 = Pareto(alpha)
        data = rng_s.pareto(a=alpha, size=(N_SAM, n)) + 1.0

        rel_errs = np.empty(N_SAM)
        abs_errs = np.empty(N_SAM)
        cov_dbl  = np.empty(N_SAM, dtype=bool)
        cov_mp   = np.empty(N_SAM, dtype=bool)
        cov_pct  = np.empty(N_SAM, dtype=bool)

        for i in range(N_SAM):
            x = data[i]
            a_d = acc_double(x)
            a_m = acc_mp(x, REF_PREC)

            abs_errs[i] = abs(a_d - a_m)
            rel_errs[i] = abs_errs[i] / max(abs(a_m), 1e-15)

            theta_hat  = float(np.mean(x))
            boot_idx   = rng_b.integers(0, n, size=(B_BOOT, n))
            theta_boot = data[i][boot_idx].mean(axis=1)

            lo_d, hi_d = bca_from_boot(theta_hat, theta_boot, a_d)
            cov_dbl[i] = lo_d <= pop_mu <= hi_d

            lo_m, hi_m = bca_from_boot(theta_hat, theta_boot, a_m)
            cov_mp[i]  = lo_m <= pop_mu <= hi_m

            lo_p = float(np.percentile(theta_boot, 2.5))
            hi_p = float(np.percentile(theta_boot, 97.5))
            cov_pct[i] = lo_p <= pop_mu <= hi_p

        row = dict(
            cell=f"{dname}_n{n}", dist=dname, n=n,
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
        pareto_results.append(row)

        elapsed = time.time() - t_start
        print(f"{row['cell']:<22} {row['med_rerr']:>10.2e} {row['p95_rerr']:>10.2e}"
              f" {row['frac_meaningful']:>10.4f}"
              f" {row['cov_dbl']:>8.4f} {row['cov_mp']:>8.4f}"
              f" {row['cov_pct']:>8.4f} {row['gap_pp']:>+8.3f}"
              f"  [{elapsed:.0f}s]")

with open('pareto_results_fixed.json', 'w') as f:
    json.dump(pareto_results, f, indent=2)
print(f"\nDone in {time.time() - t_start:.1f}s. Saved to pareto_results_fixed.json")
