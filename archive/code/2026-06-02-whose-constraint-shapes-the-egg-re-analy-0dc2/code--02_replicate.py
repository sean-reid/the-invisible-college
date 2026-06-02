"""Replicate the Stoddard et al. headline result on the merged sample.

Stoddard et al. (2017) Table S6: across 1400 species, the two best predictors
of egg-shape PC1 (ellipticity) and PC2 (asymmetry) are body mass and a
flight-ability composite. They report PGLS-Brownian.

Here:
  - We do NOT have BirdTree phylogeny in this environment, so PGLS is not
    available. We use three substitutes:
       (a) OLS on n = 1145 (matched sample)
       (b) mixed-effects regression with Family random intercept
       (c) mixed-effects with Order random intercept
       (d) leave-one-order-out OLS sensitivity
       (e) clade-cluster bootstrap by Order
  - Hand-wing index (HWI) stands in for Stoddard's flight-ability composite.
    Stoddard used wing-loading + HWI. AVONET provides only HWI directly.
    HWI is the published primary flight-ability metric in Sheard et al. 2020.

Outputs:
  results/01_replicate.txt
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

os.makedirs("results", exist_ok=True)

df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["Mass", "Hand.Wing.Index", "asymmetry", "ellipticity"]).copy()
df["log_mass"] = np.log10(df["Mass"])
df["log_egg_len"] = np.log10(df["egg_length_cm"])
df["HWI"] = df["Hand.Wing.Index"]
df["log_wing"] = np.log10(df["Wing.Length"])
df["log_tarsus"] = np.log10(df["Tarsus.Length"])

lines = []
def out(s=""):
    lines.append(s)
    print(s)

out(f"# Replication on matched sample (n = {len(df)})")
out(f"# Species coverage: {df['family'].nunique()} families, {df['order'].nunique()} orders")
out("")

# -----------------------------------------------------------
# 1. OLS replication, both response variables.
# -----------------------------------------------------------
out("## OLS, ellipticity ~ log_mass + HWI")
m = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit()
out(m.summary().as_text())
out("")

out("## OLS, asymmetry ~ log_mass + HWI")
m_asym = smf.ols("asymmetry ~ log_mass + HWI", data=df).fit()
out(m_asym.summary().as_text())
out("")

# -----------------------------------------------------------
# 2. Egg-shape adjusted for egg size (Stoddard's claim is about shape, not size).
# -----------------------------------------------------------
out("## Sanity check: log(egg length) is a proxy for body mass.")
m_size = smf.ols("log_egg_len ~ log_mass", data=df).fit()
out(f"slope log10(egg_len) on log10(mass) = {m_size.params['log_mass']:.4f}, R^2 = {m_size.rsquared:.3f}")
out(f"   (geometric isometry predicts slope 1/3 = 0.333)")
out("")

# -----------------------------------------------------------
# 3. Mixed-effects with Order as random intercept (clade structure).
# -----------------------------------------------------------
from statsmodels.regression.mixed_linear_model import MixedLM
out("## Mixed-effects: ellipticity ~ log_mass + HWI, random intercept by Order")
try:
    mlm = MixedLM.from_formula("ellipticity ~ log_mass + HWI", data=df, groups=df["order"])
    res = mlm.fit(method="lbfgs", maxiter=200)
    out(res.summary().as_text())
    out("")
except Exception as e:
    out(f"  MixedLM (order) failed: {e}")

out("## Mixed-effects: ellipticity ~ log_mass + HWI, random intercept by Family")
try:
    mlm2 = MixedLM.from_formula("ellipticity ~ log_mass + HWI", data=df, groups=df["family"])
    res2 = mlm2.fit(method="lbfgs", maxiter=400)
    out(res2.summary().as_text())
    out("")
except Exception as e:
    out(f"  MixedLM (family) failed: {e}")

# -----------------------------------------------------------
# 4. Cluster-robust SEs by Order (treats each order as one cluster).
# -----------------------------------------------------------
out("## OLS with cluster-robust SEs by Order")
m_cl = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["order"]})
out(m_cl.summary().as_text())
out("")

# -----------------------------------------------------------
# 5. Cluster bootstrap by Order: resample 35 orders with replacement.
# -----------------------------------------------------------
out("## Cluster bootstrap by Order, ellipticity ~ log_mass + HWI")
np.random.seed(20260602)
orders = df["order"].unique().tolist()
B = 2000
boots_mass = []
boots_hwi  = []
for _ in range(B):
    sample_orders = np.random.choice(orders, size=len(orders), replace=True)
    pieces = []
    for o in sample_orders:
        pieces.append(df[df["order"] == o])
    boot = pd.concat(pieces, ignore_index=True)
    try:
        mb = smf.ols("ellipticity ~ log_mass + HWI", data=boot).fit()
        boots_mass.append(mb.params["log_mass"])
        boots_hwi.append(mb.params["HWI"])
    except Exception:
        continue

ci_mass = np.percentile(boots_mass, [2.5, 97.5])
ci_hwi  = np.percentile(boots_hwi,  [2.5, 97.5])
out(f"Cluster-bootstrap n={len(boots_mass)} (orders resampled with replacement)")
out(f"log_mass : mean = {np.mean(boots_mass):+.5f}  95% CI [{ci_mass[0]:+.5f}, {ci_mass[1]:+.5f}]")
out(f"HWI      : mean = {np.mean(boots_hwi):+.5f}  95% CI [{ci_hwi[0]:+.5f}, {ci_hwi[1]:+.5f}]")
out("")

# Save bootstrap distribution
np.savetxt("results/boot_log_mass.txt", boots_mass)
np.savetxt("results/boot_HWI.txt", boots_hwi)

with open("results/01_replicate.txt", "w") as fh:
    fh.write("\n".join(lines))
print("\nWrote results/01_replicate.txt")
