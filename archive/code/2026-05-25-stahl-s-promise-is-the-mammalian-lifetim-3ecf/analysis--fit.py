"""Lifetime heartbeat analysis.

Pre-registered:
- Primary fit: OLS log10(H) ~ log10(M) where H = f_H (bpm) * L_max (yr) * 60*24*365.25
- Bootstrap CIs (5000 replicates) over species
- Order-cluster bootstrap as phylogeny stand-in
- Restricted-range fits (small <= 1 kg; large >= 1 kg)
- Leave-one-out for each species
- Companion fits: log10(f_H) ~ log10(M) and log10(L_max) ~ log10(M)
- Consistency check: slope(H) should equal slope(f_H) + slope(L_max) on the same sample
"""

import csv
import math
import json
import random
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
DATA = HERE / "species_data.csv"
OUT = HERE / "results.json"

MIN_PER_YEAR = 60 * 24 * 365.25


def load_data():
    rows = []
    with DATA.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "species": row["species"],
                "common": row["common_name"],
                "order": row["order"],
                "mass_g": float(row["mass_g"]),
                "hr_bpm": float(row["hr_bpm"]),
                "Lmax_yr": float(row["Lmax_yr"]),
                "notes": row["measurement_notes"],
            })
    return rows


def ols(x, y):
    """Plain OLS; returns slope, intercept, R^2, residuals."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    xbar = x.mean()
    ybar = y.mean()
    Sxx = np.sum((x - xbar) ** 2)
    Sxy = np.sum((x - xbar) * (y - ybar))
    beta = Sxy / Sxx
    alpha = ybar - beta * xbar
    yhat = alpha + beta * x
    resid = y - yhat
    ss_res = np.sum(resid ** 2)
    ss_tot = np.sum((y - ybar) ** 2)
    r2 = 1 - ss_res / ss_tot
    sigma = math.sqrt(ss_res / (n - 2))
    se_beta = sigma / math.sqrt(Sxx)
    return {
        "n": n,
        "slope": beta,
        "intercept": alpha,
        "se_slope": se_beta,
        "r2": r2,
        "resid": resid.tolist(),
        "yhat": yhat.tolist(),
        "sigma": sigma,
    }


def bootstrap_ci(x, y, n_iter=5000, seed=20260525):
    rng = random.Random(seed)
    x = list(x)
    y = list(y)
    n = len(x)
    slopes = []
    intercepts = []
    for _ in range(n_iter):
        idx = [rng.randrange(n) for _ in range(n)]
        xb = [x[i] for i in idx]
        yb = [y[i] for i in idx]
        # Guard against degenerate samples (all same x)
        if len(set(xb)) < 2:
            continue
        f = ols(xb, yb)
        slopes.append(f["slope"])
        intercepts.append(f["intercept"])
    slopes = np.array(slopes)
    intercepts = np.array(intercepts)
    return {
        "slope_mean": float(slopes.mean()),
        "slope_ci": [float(np.percentile(slopes, 2.5)), float(np.percentile(slopes, 97.5))],
        "intercept_mean": float(intercepts.mean()),
        "intercept_ci": [float(np.percentile(intercepts, 2.5)), float(np.percentile(intercepts, 97.5))],
        "n_replicates": len(slopes),
    }


def cluster_bootstrap_ci(x, y, clusters, n_iter=5000, seed=20260525):
    """Bootstrap whole orders as clusters (phylogeny stand-in)."""
    rng = random.Random(seed)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    clusters = np.asarray(clusters)
    cluster_ids = sorted(set(clusters.tolist()))
    cluster_idx = {c: np.where(clusters == c)[0].tolist() for c in cluster_ids}
    slopes = []
    for _ in range(n_iter):
        sampled_clusters = [rng.choice(cluster_ids) for _ in cluster_ids]
        idx = []
        for c in sampled_clusters:
            idx.extend(cluster_idx[c])
        xb = x[idx]
        yb = y[idx]
        if len(set(xb.tolist())) < 2:
            continue
        f = ols(xb, yb)
        slopes.append(f["slope"])
    slopes = np.array(slopes)
    return {
        "slope_mean": float(slopes.mean()),
        "slope_ci": [float(np.percentile(slopes, 2.5)), float(np.percentile(slopes, 97.5))],
        "n_replicates": len(slopes),
    }


def loo(x, y, species):
    """Leave-one-out: returns slope, intercept for each species dropped."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    out = []
    for i, sp in enumerate(species):
        mask = np.ones(len(x), dtype=bool)
        mask[i] = False
        f = ols(x[mask], y[mask])
        out.append({"dropped": sp, "slope": f["slope"], "intercept": f["intercept"]})
    return out


def main():
    rows = load_data()
    species = [r["species"] for r in rows]
    common = [r["common"] for r in rows]
    orders = [r["order"] for r in rows]

    log_M = [math.log10(r["mass_g"]) for r in rows]
    log_fH = [math.log10(r["hr_bpm"]) for r in rows]
    log_Lmax = [math.log10(r["Lmax_yr"]) for r in rows]
    H = [r["hr_bpm"] * r["Lmax_yr"] * MIN_PER_YEAR for r in rows]
    log_H = [math.log10(h) for h in H]

    results = {}

    # --- Companion fits ---
    fH_fit = ols(log_M, log_fH)
    Lmax_fit = ols(log_M, log_Lmax)
    H_fit = ols(log_M, log_H)

    results["fit_fH"] = {
        "slope": fH_fit["slope"], "se_slope": fH_fit["se_slope"],
        "intercept": fH_fit["intercept"], "r2": fH_fit["r2"], "n": fH_fit["n"],
        "boot": bootstrap_ci(log_M, log_fH),
    }
    results["fit_Lmax"] = {
        "slope": Lmax_fit["slope"], "se_slope": Lmax_fit["se_slope"],
        "intercept": Lmax_fit["intercept"], "r2": Lmax_fit["r2"], "n": Lmax_fit["n"],
        "boot": bootstrap_ci(log_M, log_Lmax),
    }
    results["fit_H"] = {
        "slope": H_fit["slope"], "se_slope": H_fit["se_slope"],
        "intercept": H_fit["intercept"], "r2": H_fit["r2"], "n": H_fit["n"],
        "boot": bootstrap_ci(log_M, log_H),
    }

    # Consistency check
    results["consistency"] = {
        "slope_H_observed": H_fit["slope"],
        "slope_fH_plus_Lmax": fH_fit["slope"] + Lmax_fit["slope"],
        "difference": H_fit["slope"] - (fH_fit["slope"] + Lmax_fit["slope"]),
    }

    # --- Order-cluster bootstrap ---
    results["cluster_boot_H"] = cluster_bootstrap_ci(log_M, log_H, orders)

    # --- Restricted-range fits ---
    small_idx = [i for i, r in enumerate(rows) if r["mass_g"] <= 1000]
    large_idx = [i for i, r in enumerate(rows) if r["mass_g"] > 1000]
    if len(small_idx) >= 3:
        s_lM = [log_M[i] for i in small_idx]
        s_lH = [log_H[i] for i in small_idx]
        s_fit = ols(s_lM, s_lH)
        results["fit_H_small"] = {
            "slope": s_fit["slope"], "se_slope": s_fit["se_slope"],
            "intercept": s_fit["intercept"], "r2": s_fit["r2"], "n": s_fit["n"],
            "species_included": [species[i] for i in small_idx],
        }
    if len(large_idx) >= 3:
        l_lM = [log_M[i] for i in large_idx]
        l_lH = [log_H[i] for i in large_idx]
        l_fit = ols(l_lM, l_lH)
        results["fit_H_large"] = {
            "slope": l_fit["slope"], "se_slope": l_fit["se_slope"],
            "intercept": l_fit["intercept"], "r2": l_fit["r2"], "n": l_fit["n"],
            "species_included": [species[i] for i in large_idx],
        }

    # --- Central H value and its bootstrap ---
    median_H = float(np.median(H))
    boot_seed = random.Random(20260526)
    boot_medians = []
    for _ in range(5000):
        idx = [boot_seed.randrange(len(H)) for _ in range(len(H))]
        boot_medians.append(float(np.median([H[i] for i in idx])))
    boot_medians = np.array(boot_medians)
    results["central_H"] = {
        "median_H": median_H,
        "median_H_ci": [float(np.percentile(boot_medians, 2.5)), float(np.percentile(boot_medians, 97.5))],
        "geomean_H": float(10 ** np.mean(np.log10(H))),
        "log10_H_mean": float(np.mean(np.log10(H))),
        "log10_H_sd": float(np.std(np.log10(H), ddof=1)),
        "log10_H_range": [float(np.min(np.log10(H))), float(np.max(np.log10(H)))],
    }

    # --- Per-species table ---
    results["per_species"] = []
    yhat_H = H_fit["yhat"]
    for i, r in enumerate(rows):
        results["per_species"].append({
            "species": r["species"],
            "common": r["common"],
            "order": r["order"],
            "mass_g": r["mass_g"],
            "hr_bpm": r["hr_bpm"],
            "Lmax_yr": r["Lmax_yr"],
            "H": H[i],
            "log10_H": math.log10(H[i]),
            "log10_H_predicted_under_zero_slope": float(np.mean(np.log10(H))),
            "log10_H_predicted_under_H_fit": yhat_H[i],
            "residual_under_H_fit": math.log10(H[i]) - yhat_H[i],
        })

    # --- Leave-one-out ---
    results["loo_H"] = loo(log_M, log_H, species)

    # --- Pre-registered tripwire: measurement heterogeneity ---
    # Decision rule: if residual SD on log10(H) exceeds 0.45 (i.e. 2.8x spread),
    # OR if any single species drives the slope by more than 0.05 in LOO,
    # the joint analysis is downgraded to a methodological note.
    resid_sd = float(np.std(H_fit["resid"], ddof=1))
    slopes_loo = [d["slope"] for d in results["loo_H"]]
    max_loo_shift = max(abs(s - H_fit["slope"]) for s in slopes_loo)
    results["heterogeneity_check"] = {
        "resid_sd_log10H": resid_sd,
        "threshold_resid_sd": 0.45,
        "resid_sd_pass": bool(resid_sd <= 0.45),
        "max_loo_slope_shift": float(max_loo_shift),
        "threshold_loo_shift": 0.05,
        "loo_pass": bool(max_loo_shift <= 0.05),
    }

    OUT.write_text(json.dumps(results, indent=2))
    print("Wrote", OUT)
    print()
    print("Headline results:")
    print(f"  N species: {H_fit['n']}")
    print(f"  Slope log10(f_H) ~ log10(M): {fH_fit['slope']:+.4f}  boot CI {results['fit_fH']['boot']['slope_ci']}")
    print(f"  Slope log10(L_max) ~ log10(M): {Lmax_fit['slope']:+.4f}  boot CI {results['fit_Lmax']['boot']['slope_ci']}")
    print(f"  Slope log10(H) ~ log10(M): {H_fit['slope']:+.4f}  boot CI {results['fit_H']['boot']['slope_ci']}")
    print(f"  Consistency residual: {results['consistency']['difference']:+.6f}")
    print(f"  Cluster (order) boot CI on H slope: {results['cluster_boot_H']['slope_ci']}")
    if "fit_H_small" in results:
        print(f"  Small (<=1 kg) H slope: {results['fit_H_small']['slope']:+.4f}  n={results['fit_H_small']['n']}")
    if "fit_H_large" in results:
        print(f"  Large (>1 kg) H slope:  {results['fit_H_large']['slope']:+.4f}  n={results['fit_H_large']['n']}")
    print(f"  Median H: {results['central_H']['median_H']:.3e}  boot CI {[f'{x:.2e}' for x in results['central_H']['median_H_ci']]}")
    print(f"  log10(H) mean: {results['central_H']['log10_H_mean']:.3f}  SD: {results['central_H']['log10_H_sd']:.3f}")
    print(f"  log10(H) range: {results['central_H']['log10_H_range']}")
    print(f"  Resid SD pass: {results['heterogeneity_check']['resid_sd_pass']}  (sd={resid_sd:.3f})")
    print(f"  LOO pass: {results['heterogeneity_check']['loo_pass']}  (max shift={max_loo_shift:.4f})")
    print()
    print("Largest residuals under H fit (log10 units):")
    spp = results["per_species"]
    spp_sorted = sorted(spp, key=lambda d: abs(d["residual_under_H_fit"]), reverse=True)
    for d in spp_sorted[:6]:
        print(f"  {d['common']:25s} {d['residual_under_H_fit']:+.3f}  H={d['H']:.2e}")


if __name__ == "__main__":
    main()
