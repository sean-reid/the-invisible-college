"""
Galileo or Biewener?  Femoral cross-section scaling.

Inputs:
  extants.csv  -- 245 living tetrapods (mammals + reptiles).
                   Columns relevant here: Mon.Groups, Species,
                   BM (body mass, grams), FC (femoral circumference, mm).
                   Source: Campione & Evans (2012) BMC Biology 10:60,
                   distributed in the MASSTIMATE R package as
                   data(extants).

Outputs (printed):
  - Step 1: pre-flight Monte Carlo power table
  - Step 2: restated rejection rule (numeric thresholds)
  - Step 3: OLS fit on mammal-only subset, with bootstrap CI
  - Step 4: order-clustered robust SE (phylo proxy)
  - Step 5: translation from beta_C to beta_I and rejection-rule call
"""

import csv
import math
import os
import random
from collections import defaultdict

random.seed(20260520)

# ---------------------------------------------------------------------------
# Step 0:  Load data.

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = []
with open(os.path.join(HERE, "extants.csv")) as f:
    for r in csv.DictReader(f):
        try:
            BM = float(r["BM"])
            FC = float(r["FC"])
        except (ValueError, KeyError):
            continue
        if BM <= 0 or FC <= 0:
            continue
        ROWS.append(
            dict(
                group=r["Mon.Groups"],
                species=r["Species"],
                BM_g=BM,
                FC_mm=FC,
            )
        )

mammals = [r for r in ROWS if r["group"] != "Reptilia"]
reptiles = [r for r in ROWS if r["group"] == "Reptilia"]

print(f"Loaded {len(ROWS)} extant tetrapods")
print(f"  mammals: {len(mammals)}    reptiles: {len(reptiles)}")
print(f"  mammalian groups: {sorted(set(r['group'] for r in mammals))}")
M_min = min(r["BM_g"] for r in mammals) / 1000.0
M_max = max(r["BM_g"] for r in mammals) / 1000.0
print(f"  mammal body-mass range (kg): {M_min:.4g}   -   {M_max:.4g}")
print(f"  log10 range: {math.log10(M_min):.2f} to {math.log10(M_max):.2f}")
print()


# ---------------------------------------------------------------------------
# Helper: simple OLS on (x, y), returns slope, intercept, residual sd, n.

def ols(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    b = sxy / sxx
    a = my - b * mx
    resid = [yi - (a + b * xi) for xi, yi in zip(x, y)]
    s2 = sum(r * r for r in resid) / max(n - 2, 1)
    se_b = math.sqrt(s2 / sxx)
    return dict(a=a, b=b, sd_resid=math.sqrt(s2), se_b=se_b, n=n, resid=resid)


# ---------------------------------------------------------------------------
# Step 1.  Pre-flight Monte Carlo power table.
#
# Question: at the sample sizes we can realistically afford, can the
# design distinguish the Galileo (beta_I = 4/3) and Biewener (beta_I = 1.0)
# predictions?  Simulate from log10(I) = a + beta_I * log10(M) + eps,
# eps ~ N(0, sigma).  For each true beta and each n, simulate 1000
# datasets, fit OLS, record the empirical 95% CI width and the rejection
# rates against each null.
#
# The proposal pre-committed to:
#   beta_true in {1.0, 1.10, 1.20, 4/3}
#   sigma = 0.10 on log10(I)
#   n = 90 (matching the proposal target after pruning)
#
# Real working sample after switching to the available Campione/Evans
# femoral-circumference data is ~198.  We therefore report both n=90
# (pre-committed) and n=198 (data we have).
#
# Reminder: we fit on log10(I) here, but the available variable is
# circumference C; the link is I = C^4/(64*pi^3) for a solid circle.
# Under multiplicative log-log models, the slope of log(I) on log(M)
# is 4 * slope of log(C) on log(M).  The Monte Carlo can therefore be
# stated in either coordinate; what matters is the gap between 4/3 and 1.0.

print("=" * 70)
print("Step 1: pre-flight Monte Carlo power for distinguishing beta_I.")
print("=" * 70)
print()
print("  Simulate y = a + beta * x + eps,  x ~ U(log10 mass range),")
print("  eps ~ N(0, sigma=0.10).  Fit OLS, take 95% Wald CI on beta.")
print()


def simulate_power(n, beta_true, sigma=0.10, n_sim=1000,
                   x_low=-2.0, x_high=3.7):
    """Return (median CI half-width, P(reject 1.0), P(reject 4/3))."""
    half_widths = []
    rej_biewener = 0
    rej_galileo = 0
    for _ in range(n_sim):
        x = [random.uniform(x_low, x_high) for _ in range(n)]
        y = [beta_true * xi + random.gauss(0, sigma) for xi in x]
        f = ols(x, y)
        b, se = f["b"], f["se_b"]
        # large-n Wald 95% CI
        lo, hi = b - 1.96 * se, b + 1.96 * se
        half_widths.append((hi - lo) / 2)
        if lo > 1.0 + 0.03:  # pre-registered 0.03 margin
            rej_biewener += 1
        if hi < 4.0 / 3.0 - 0.03:
            rej_galileo += 1
    half_widths.sort()
    median_hw = half_widths[len(half_widths) // 2]
    return median_hw, rej_biewener / n_sim, rej_galileo / n_sim


print("  n=90 (pre-committed in proposal):")
print(f"  {'beta_true':>10s} {'med CI ±':>10s} {'P(rej 1.0)':>12s} "
      f"{'P(rej 4/3)':>12s}")
for bt in [1.0, 1.10, 1.20, 4.0 / 3.0]:
    hw, rb, rg = simulate_power(n=90, beta_true=bt)
    print(f"  {bt:10.3f} {hw:10.3f} {rb:12.2%} {rg:12.2%}")
print()
print("  n=198 (Campione&Evans 2012 mammal subset actually available):")
print(f"  {'beta_true':>10s} {'med CI ±':>10s} {'P(rej 1.0)':>12s} "
      f"{'P(rej 4/3)':>12s}")
for bt in [1.0, 1.10, 1.20, 4.0 / 3.0]:
    hw, rb, rg = simulate_power(n=198, beta_true=bt)
    print(f"  {bt:10.3f} {hw:10.3f} {rb:12.2%} {rg:12.2%}")
print()


# ---------------------------------------------------------------------------
# Step 2:  Restate the rejection rule with numeric thresholds.
#
# Reviewer asked that "0.03 outside" be made unambiguous BEFORE the data
# fit.  Restated, in writing, before Step 3 runs:
#
#   Let beta_I be the exponent of I on M.
#
#   Reject Biewener (H0: beta_I = 1.0):
#       require   95% CI lower bound on beta_I  >  1.03.
#
#   Reject Galileo (H0: beta_I = 4/3 = 1.3333...):
#       require   95% CI upper bound on beta_I  <  1.3033.
#
#   If neither bound is satisfied: report the CI and decline to discriminate.
#
# We restate the rule in the language of beta_I (the variable Galileo and
# Biewener disagree about).  The fit below is in beta_C (slope of log(C)
# on log(M)) and is propagated by beta_I = 4 * beta_C under the geometric-
# similarity assumption beta_d = beta_C.  The propagation is multiplicative
# on logs; the CI multiplies by the same factor.

print("=" * 70)
print("Step 2: restated rejection rule (numeric, pre-data).")
print("=" * 70)
print()
print("  Reject Biewener (beta_I = 1.0):  lower 95% CI on beta_I > 1.03.")
print("  Reject Galileo (beta_I = 4/3):   upper 95% CI on beta_I < 1.3033.")
print("  CI straddling both: decline to discriminate.")
print()


# ---------------------------------------------------------------------------
# Step 3:  OLS fit on log10(BM_kg) vs log10(FC_mm), mammal-only.

print("=" * 70)
print("Step 3: OLS fit, mammals only,  log10(FC_mm) ~ log10(BM_kg).")
print("=" * 70)
print()


def fit_mammals(data):
    x = [math.log10(r["BM_g"] / 1000.0) for r in data]
    y = [math.log10(r["FC_mm"]) for r in data]
    return ols(x, y), x, y


fit, x, y = fit_mammals(mammals)
b, a = fit["b"], fit["a"]
se = fit["se_b"]
n = fit["n"]

# Bootstrap CI for beta_C, 10000 resamples (pre-committed = 10,000).
B = 10000
boots = []
for _ in range(B):
    idx = [random.randrange(n) for _ in range(n)]
    xb = [x[i] for i in idx]
    yb = [y[i] for i in idx]
    fb = ols(xb, yb)
    boots.append(fb["b"])
boots.sort()
ci_lo = boots[int(0.025 * B)]
ci_hi = boots[int(0.975 * B)]

print(f"  n = {n}")
print(f"  beta_C (slope of log(FC) on log(BM_kg)): {b:.4f}")
print(f"    Wald 95% CI: [{b - 1.96 * se:.4f}, {b + 1.96 * se:.4f}]")
print(f"    Bootstrap 95% CI (B={B:,}): [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"  intercept a (log10 FC at 1 kg): {a:.4f}")
print(f"  predicted FC at 1 kg: {10 ** a:.3f} mm")
print(f"  residual sd on log10(FC_mm): {fit['sd_resid']:.4f}")
print()


# ---------------------------------------------------------------------------
# Step 4:  Phylogenetic proxy --- clustered robust SE by Mon.Groups.
#
# I do not have a full phylogenetic tree loaded; the Upham et al. 2019
# supertree the proposal named is not in this workspace.  Mon.Groups
# (Afrotheria, Carnivora, Euarchonta, Eulipotyphla, Glires, Marsupialia,
# Ungulata, Xenarthra) groups species by their superordinal clade.  A
# cluster-robust SE under group resampling is a crude but defensible
# stand-in: it inflates the SE in proportion to within-cluster correlation
# in residuals.  The expected effect, given Capellini & Gosling (2007),
# is a 0.02-0.06 widening of the CI versus OLS, smaller than the gap
# between 1.0 and 4/3.

print("=" * 70)
print("Step 4: cluster-bootstrap SE by mammalian Mon.Group (phylo proxy).")
print("=" * 70)
print()

by_group = defaultdict(list)
for i, r in enumerate(mammals):
    by_group[r["group"]].append(i)
groups = list(by_group.keys())
print(f"  clusters: {len(groups)}")
for g in groups:
    print(f"    {g:15s} n={len(by_group[g])}")

boots_g = []
for _ in range(B):
    # Resample whole clusters with replacement.
    drawn = [random.choice(groups) for _ in range(len(groups))]
    idx = []
    for g in drawn:
        idx.extend(by_group[g])
    xb = [x[i] for i in idx]
    yb = [y[i] for i in idx]
    if len(xb) < 3:
        continue
    fb = ols(xb, yb)
    boots_g.append(fb["b"])
boots_g.sort()
cig_lo = boots_g[int(0.025 * len(boots_g))]
cig_hi = boots_g[int(0.975 * len(boots_g))]
print(f"  cluster-bootstrap 95% CI on beta_C: "
      f"[{cig_lo:.4f}, {cig_hi:.4f}]")
print()


# ---------------------------------------------------------------------------
# Step 5:  Translate to beta_I and call the rejection rule.

print("=" * 70)
print("Step 5: translation to beta_I and rejection-rule call.")
print("=" * 70)
print()

# Assumption: solid-circular-beam (equivalently, geometrically-similar
# tube with constant cortical-thickness fraction).  Under this
# assumption beta_I = 4 * beta_C exactly.  The assumption is stated
# explicitly so a reader can substitute their own preferred cortical
# scaling.
beta_I_hat = 4 * b
beta_I_lo_boot = 4 * ci_lo
beta_I_hi_boot = 4 * ci_hi
beta_I_lo_clu = 4 * cig_lo
beta_I_hi_clu = 4 * cig_hi

print(f"  Under I ∝ C^4 (solid beam / constant-k tube):")
print(f"    beta_I point estimate:   {beta_I_hat:.4f}")
print(f"    beta_I bootstrap 95% CI: [{beta_I_lo_boot:.4f}, "
      f"{beta_I_hi_boot:.4f}]")
print(f"    beta_I cluster   95% CI: [{beta_I_lo_clu:.4f}, "
      f"{beta_I_hi_clu:.4f}]")
print()

# Pre-registered call.
def call(name, lo, hi):
    rej_b = lo > 1.0 + 0.03
    rej_g = hi < 4.0 / 3.0 - 0.03
    return (
        f"  {name:18s} reject Biewener? {rej_b!s:5s}  "
        f"reject Galileo? {rej_g!s:5s}"
    )

print(call("OLS bootstrap:", beta_I_lo_boot, beta_I_hi_boot))
print(call("cluster bootstrap:", beta_I_lo_clu, beta_I_hi_clu))
print()


# ---------------------------------------------------------------------------
# Step 6:  Influential-species and residual plot data.

print("=" * 70)
print("Step 6: residual extrema (influential species).")
print("=" * 70)
print()
resid_pairs = list(zip(mammals, fit["resid"]))
resid_pairs.sort(key=lambda p: abs(p[1]), reverse=True)
print("  Top 10 residuals (|log10 FC_obs - log10 FC_pred|):")
for r, e in resid_pairs[:10]:
    print(f"    {r['group']:12s} {r['species']:32s} "
          f"BM={r['BM_g'] / 1000:8.3g} kg   FC={r['FC_mm']:7.3g} mm  "
          f"resid={e:+.3f}")
print()

# Sensitivity: drop top-3 residual species, refit.
drop_idx = [
    i for i in range(len(mammals))
    if mammals[i] in [p[0] for p in resid_pairs[:3]]
]
keep = [i for i in range(len(mammals)) if i not in drop_idx]
x2 = [x[i] for i in keep]
y2 = [y[i] for i in keep]
fit2 = ols(x2, y2)
print(f"  Sensitivity: drop top-3 residuals -> beta_C = {fit2['b']:.4f}, "
      f"intercept = {fit2['a']:.4f}, n = {fit2['n']}")
print(f"  Sensitivity beta_I = {4 * fit2['b']:.4f}")
print()


# ---------------------------------------------------------------------------
# Step 7:  Unit audit (the pre-committed sanity check).
#
# Predicted log10(FC_mm) at 1 kg = a.
# For a 1 kg mammal (e.g. rat, ~250 g body mass; or rabbit, ~2 kg),
# femur diameter is on the order of 5 mm, so femur circumference is on
# the order of pi*5 ~ 15 mm, log10(15) ~ 1.18.
#
# Then log10(I_AP_mm4) = log10(C^4 / (64*pi^3)) = 4*a - log10(64*pi^3)
# = 4*1.18 - log10(1984) = 4.72 - 3.30 = 1.42.
# The pre-committed predicted intercept band was log10 I ≈ 1.5 to 2.5 mm^4,
# which brackets this back-of-envelope estimate.

print("=" * 70)
print("Step 7: unit audit.")
print("=" * 70)
print()
intercept_logI = 4 * a - math.log10(64 * math.pi ** 3)
print(f"  Predicted log10(FC) at BM=1 kg:   {a:.3f}")
print(f"  Predicted FC at BM=1 kg:          {10 ** a:.2f} mm")
print(f"  -> predicted log10(I_AP) at 1 kg: {intercept_logI:.3f} mm^4")
print(f"  Pre-committed band: log10 I in [1.5, 2.5] mm^4")
print(f"  Audit: "
      f"{'PASS' if 1.5 <= intercept_logI <= 2.5 else 'OUT OF BAND'}")
print()


# ---------------------------------------------------------------------------
# Step 8:  Save a clean tabulation of the fit for the draft.

with open(os.path.join(HERE, "fit_summary.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"beta_C = {b:.5f}\n")
    f.write(f"beta_C bootstrap 95% CI: [{ci_lo:.5f}, {ci_hi:.5f}]\n")
    f.write(f"beta_C cluster bootstrap 95% CI: "
            f"[{cig_lo:.5f}, {cig_hi:.5f}]\n")
    f.write(f"intercept a = {a:.5f}\n")
    f.write(f"residual sd = {fit['sd_resid']:.5f}\n")
    f.write(f"beta_I = 4*beta_C = {beta_I_hat:.5f}\n")
    f.write(f"beta_I bootstrap 95% CI: "
            f"[{beta_I_lo_boot:.5f}, {beta_I_hi_boot:.5f}]\n")
    f.write(f"beta_I cluster bootstrap 95% CI: "
            f"[{beta_I_lo_clu:.5f}, {beta_I_hi_clu:.5f}]\n")

print("Saved fit_summary.txt")
