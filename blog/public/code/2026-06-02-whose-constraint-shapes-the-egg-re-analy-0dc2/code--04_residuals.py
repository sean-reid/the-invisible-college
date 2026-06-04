"""Examine residual structure for the best-supported model.

Tests:
  (a) Order-level residual departures (after MLM-Family base fit).
  (b) Mass-conditioned heteroscedasticity in residuals (Breusch-Pagan-like).
  (c) Add Migration status (categorical) as additional covariate.
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM
from scipy import stats

df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["Mass","Hand.Wing.Index","asymmetry","ellipticity"]).copy()
df["log_mass"]=np.log10(df["Mass"]); df["HWI"]=df["Hand.Wing.Index"]
df["log_wing"]=np.log10(df["Wing.Length"]); df["log_tarsus"]=np.log10(df["Tarsus.Length"])

print("## Residuals from OLS ellipticity ~ log_mass + HWI")
m = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit()
df["resid"] = m.resid

# Order-level mean residuals (only orders with n >= 10).
order_resid = df.groupby("order")["resid"].agg(["mean","std","count"]).reset_index()
order_resid = order_resid[order_resid["count"] >= 10].sort_values("mean")
print("\nOrder-level mean residuals (n >= 10), most negative first:")
print(order_resid.to_string(float_format="%.5f"))

# Sign and size of clade-level departures: anything > 2 SE?
order_resid["se_mean"] = order_resid["std"] / np.sqrt(order_resid["count"])
order_resid["z"] = order_resid["mean"] / order_resid["se_mean"]
big = order_resid[np.abs(order_resid["z"]) > 2]
print(f"\nOrders with |z(mean residual)| > 2: {len(big)} of {len(order_resid)}")
print(big.to_string(float_format="%.4f"))

# Save.
order_resid.to_csv("results/04_order_residuals.csv", index=False)

# Heteroscedasticity: is |resid| systematic in log_mass?
from statsmodels.stats.diagnostic import het_breuschpagan
bp = het_breuschpagan(m.resid, m.model.exog)
print(f"\nBreusch-Pagan test (mass + HWI vs |resid|^2):")
print(f"  LM stat = {bp[0]:.3f}, p = {bp[1]:.4g}")

# Migration status as covariate.
print("\n## Adding Migration (categorical: 1=sedentary, 2=partial, 3=full) as covariate")
df2 = df.dropna(subset=["Migration"]).copy()
df2["Migration"] = df2["Migration"].astype("category")
m_mig = smf.ols("ellipticity ~ log_mass + HWI + C(Migration)", data=df2).fit()
print(m_mig.summary().tables[1])

# Conditional on Migration = sedentary subset.
for mig_val, label in [(1.0,"Sedentary"),(2.0,"Partial migrant"),(3.0,"Full migrant")]:
    sub = df2[df2["Migration"]==mig_val]
    if len(sub) < 30: continue
    ms = smf.ols("ellipticity ~ log_mass + HWI", data=sub).fit()
    print(f"\n{label} only (n={len(sub)})")
    print(f"  log_mass = {ms.params['log_mass']:+.5f} (SE {ms.bse['log_mass']:.5f})")
    print(f"  HWI      = {ms.params['HWI']:+.5f}     (SE {ms.bse['HWI']:.5f})")
    print(f"  R^2      = {ms.rsquared:.3f}")

# Save full residual table for later examination
df[["species","order","family","log_mass","HWI","ellipticity","asymmetry","resid"]].to_csv(
    "results/05_full_residuals.csv", index=False)
print("\nWrote results/04_order_residuals.csv, results/05_full_residuals.csv")
