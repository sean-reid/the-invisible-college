"""Sensitivity analyses extending fit.py.

Pre-registered (specified in proposal-review response, before fitting):

Sensitivity A: drop each ORDER one at a time. Detect whether a single clade
drives the slope.

Sensitivity B: max-statistic bias correction.
  - Categorize each species as "well-monitored" (lab, domestic, zoo standard)
    or "less-monitored" (wild-only or sparsely captive).
  - Fit the H slope on each subset separately.
  - If the well-monitored subset has H slope >= 0.04 less negative than the
    less-monitored subset, treat the difference as the upper-bound effect of
    upward sample-size bias in L_max on the headline slope.

Sensitivity C: drop the three named outliers (bat, naked mole rat, primates)
to see how much of the (small) negative slope is theirs vs the central body.
"""

import csv
import json
import math
import random
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
DATA = HERE / "species_data.csv"
OUT = HERE / "sensitivities.json"

MIN_PER_YEAR = 60 * 24 * 365.25

# Pre-committed annotations: "well-monitored" species have large captive
# populations or are domestic/lab and so their Lmax records draw on many
# individuals. "Less-monitored" Lmax records are more likely undercounts.
# (One could equally argue captive Lmax is INFLATED relative to wild; both
# directions are possible. The pre-registered question is whether the
# slope DIFFERS between the two subsets, not which direction.)
WELL_MONITORED = {
    "Mus musculus", "Rattus norvegicus", "Mesocricetus auratus",
    "Cavia porcellus", "Oryctolagus cuniculus", "Felis catus",
    "Canis familiaris", "Mustela putorius furo", "Ovis aries",
    "Sus scrofa domesticus", "Bos taurus", "Equus caballus",
    "Homo sapiens", "Pan troglodytes", "Macaca mulatta",
}


def ols(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    xbar, ybar = x.mean(), y.mean()
    Sxx = np.sum((x - xbar) ** 2)
    Sxy = np.sum((x - xbar) * (y - ybar))
    beta = Sxy / Sxx
    alpha = ybar - beta * xbar
    yhat = alpha + beta * x
    resid = y - yhat
    ss_res = float(np.sum(resid ** 2))
    sigma = math.sqrt(ss_res / (n - 2)) if n > 2 else float("nan")
    se_beta = sigma / math.sqrt(Sxx) if Sxx > 0 else float("nan")
    return {"n": int(n), "slope": float(beta), "intercept": float(alpha), "se": float(se_beta)}


def bootstrap_slope(x, y, n_iter=3000, seed=20260525):
    rng = random.Random(seed)
    x = list(x); y = list(y)
    n = len(x)
    slopes = []
    for _ in range(n_iter):
        idx = [rng.randrange(n) for _ in range(n)]
        xb = [x[i] for i in idx]; yb = [y[i] for i in idx]
        if len(set(xb)) < 2: continue
        slopes.append(ols(xb, yb)["slope"])
    return [float(np.percentile(slopes, 2.5)), float(np.percentile(slopes, 97.5))]


def load_data():
    rows = []
    with DATA.open() as f:
        for row in csv.DictReader(f):
            rows.append({
                "species": row["species"],
                "common": row["common_name"],
                "order": row["order"],
                "mass_g": float(row["mass_g"]),
                "hr_bpm": float(row["hr_bpm"]),
                "Lmax_yr": float(row["Lmax_yr"]),
            })
    return rows


def main():
    rows = load_data()
    out = {}

    log_M = [math.log10(r["mass_g"]) for r in rows]
    log_H = [math.log10(r["hr_bpm"] * r["Lmax_yr"] * MIN_PER_YEAR) for r in rows]

    # --- Sensitivity A: drop each order ---
    orders = sorted(set(r["order"] for r in rows))
    out["drop_order"] = {}
    for o in orders:
        idx = [i for i, r in enumerate(rows) if r["order"] != o]
        if len(idx) < 4: continue
        xs = [log_M[i] for i in idx]
        ys = [log_H[i] for i in idx]
        f = ols(xs, ys)
        out["drop_order"][o] = {
            "slope": f["slope"], "n": f["n"],
            "ci": bootstrap_slope(xs, ys),
            "dropped": [r["common"] for r in rows if r["order"] == o],
        }

    # --- Sensitivity B: well vs less monitored ---
    well_idx = [i for i, r in enumerate(rows) if r["species"] in WELL_MONITORED]
    less_idx = [i for i, r in enumerate(rows) if r["species"] not in WELL_MONITORED]
    out["well_monitored"] = {
        "n": len(well_idx),
        "species": [rows[i]["common"] for i in well_idx],
        **ols([log_M[i] for i in well_idx], [log_H[i] for i in well_idx]),
        "ci": bootstrap_slope([log_M[i] for i in well_idx], [log_H[i] for i in well_idx]),
    }
    out["less_monitored"] = {
        "n": len(less_idx),
        "species": [rows[i]["common"] for i in less_idx],
        **ols([log_M[i] for i in less_idx], [log_H[i] for i in less_idx]),
        "ci": bootstrap_slope([log_M[i] for i in less_idx], [log_H[i] for i in less_idx]),
    }
    out["bias_check"] = {
        "well_slope": out["well_monitored"]["slope"],
        "less_slope": out["less_monitored"]["slope"],
        "difference": out["well_monitored"]["slope"] - out["less_monitored"]["slope"],
    }

    # --- Sensitivity C: drop named outliers ---
    drop_sets = {
        "drop_bat": {"Myotis lucifugus"},
        "drop_nakedmolerat": {"Heterocephalus glaber"},
        "drop_primates": {"Homo sapiens", "Pan troglodytes", "Macaca mulatta"},
        "drop_bat_and_mole_rat": {"Myotis lucifugus", "Heterocephalus glaber"},
        "drop_all_named_outliers": {"Myotis lucifugus", "Heterocephalus glaber",
                                     "Homo sapiens", "Pan troglodytes", "Macaca mulatta"},
    }
    out["drop_outliers"] = {}
    for name, sset in drop_sets.items():
        idx = [i for i, r in enumerate(rows) if r["species"] not in sset]
        xs = [log_M[i] for i in idx]; ys = [log_H[i] for i in idx]
        f = ols(xs, ys)
        out["drop_outliers"][name] = {
            "slope": f["slope"], "n": f["n"],
            "ci": bootstrap_slope(xs, ys),
            "dropped": sorted(sset),
        }

    # --- Per-clade summary of H values ---
    out["by_order"] = {}
    for o in orders:
        idx = [i for i, r in enumerate(rows) if r["order"] == o]
        Hs = [10 ** log_H[i] for i in idx]
        out["by_order"][o] = {
            "n": len(idx),
            "species": [rows[i]["common"] for i in idx],
            "median_H": float(np.median(Hs)),
            "geomean_H": float(10 ** np.mean(np.log10(Hs))),
        }

    OUT.write_text(json.dumps(out, indent=2))
    print("Wrote", OUT)
    print()
    print("=== Sensitivity A: drop one order ===")
    for o, d in out["drop_order"].items():
        print(f"  drop {o:14s}  n={d['n']:3d}  slope={d['slope']:+.4f}  CI {d['ci']}")
    print()
    print("=== Sensitivity B: monitoring bias ===")
    print(f"  Well-monitored (n={out['well_monitored']['n']}):  slope={out['well_monitored']['slope']:+.4f}  CI {out['well_monitored']['ci']}")
    print(f"  Less-monitored (n={out['less_monitored']['n']}):  slope={out['less_monitored']['slope']:+.4f}  CI {out['less_monitored']['ci']}")
    print(f"  Difference: {out['bias_check']['difference']:+.4f}")
    print()
    print("=== Sensitivity C: drop named outliers ===")
    for name, d in out["drop_outliers"].items():
        print(f"  {name:30s}  n={d['n']:3d}  slope={d['slope']:+.4f}  CI {d['ci']}")
    print()
    print("=== H by order ===")
    for o, d in out["by_order"].items():
        print(f"  {o:18s}  n={d['n']}  geomean H = {d['geomean_H']:.2e}")


if __name__ == "__main__":
    main()
