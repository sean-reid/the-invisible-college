"""Test of the oviduct-geometry alternative.

Premise. Direct species-level pelvic-width data at the scale of the Stoddard
1,400 do not exist; the largest published comparative pelvic-skeletal dataset
(Anten-Houston et al. 2017, J Anat) covers 146 species in 15 orders, and its
species-level table is gated behind an anti-scraping system that I cannot pass
in this environment.

Anten-Houston et al.'s headline finding constrains what we can do without it:
they report that pelvic dimensions in birds are NOT significantly explained by
body mass once phylogeny is accounted for, but ARE significantly explained by
"locomotor style" (a categorical descriptor of how the bird primarily moves:
aerial, terrestrial, perching/insessorial, aquatic, generalist).

AVONET provides Primary.Lifestyle as exactly this categorical descriptor.
If pelvic geometry, not flight performance, is what sets egg shape:
  - Within HWI strata, lifestyle should still predict egg shape.
  - Lifestyle should explain residual variance after controlling for HWI.
If flight performance is what sets egg shape:
  - HWI should explain egg shape independently of lifestyle.
  - Lifestyle should add no incremental explanatory power.

This is not as direct a test as species-level pelvic-width-to-egg-width
ratios. It is a proxy test using a locomotor proxy of pelvic dimensions.
Its result must be qualified accordingly.
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM

df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["Mass","Hand.Wing.Index","ellipticity","asymmetry","Primary.Lifestyle"]).copy()
df["log_mass"]=np.log10(df["Mass"]); df["HWI"]=df["Hand.Wing.Index"]

print(f"## n = {len(df)} with all required fields")
print(f"Primary.Lifestyle distribution:")
print(df["Primary.Lifestyle"].value_counts().to_string())
print()

# Nested model comparison.
print("## Model 1 (flight-only): ellipticity ~ log_mass + HWI")
m1 = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit()
print(f"  R^2 = {m1.rsquared:.4f}, AIC = {m1.aic:.1f}")

print("\n## Model 2 (lifestyle-only): ellipticity ~ log_mass + C(Primary.Lifestyle)")
m2 = smf.ols("ellipticity ~ log_mass + C(Primary_Lifestyle)",
             data=df.rename(columns={"Primary.Lifestyle":"Primary_Lifestyle"})).fit()
print(f"  R^2 = {m2.rsquared:.4f}, AIC = {m2.aic:.1f}")
print(m2.summary().tables[1])

print("\n## Model 3 (both): ellipticity ~ log_mass + HWI + C(Primary.Lifestyle)")
m3 = smf.ols("ellipticity ~ log_mass + HWI + C(Primary_Lifestyle)",
             data=df.rename(columns={"Primary.Lifestyle":"Primary_Lifestyle"})).fit()
print(f"  R^2 = {m3.rsquared:.4f}, AIC = {m3.aic:.1f}")
print(m3.summary().tables[1])

# Likelihood-ratio nested tests.
def lrt(restricted, full):
    LR = -2 * (restricted.llf - full.llf)
    dof = full.df_model - restricted.df_model
    from scipy.stats import chi2
    p = chi2.sf(LR, dof)
    return LR, dof, p

# 1 vs 3 (does adding lifestyle improve over flight-only?)
LR_a, df_a, p_a = lrt(m1, m3)
print(f"\n## LRT: M1 -> M3 (adding lifestyle to flight model)")
print(f"  Chi^2 = {LR_a:.3f} on {df_a:.0f} df, p = {p_a:.3g}")

# 2 vs 3 (does adding HWI improve over lifestyle-only?)
LR_b, df_b, p_b = lrt(m2, m3)
print(f"\n## LRT: M2 -> M3 (adding HWI to lifestyle model)")
print(f"  Chi^2 = {LR_b:.3f} on {df_b:.0f} df, p = {p_b:.3g}")

# Within-lifestyle slopes of ellipticity on HWI.
print("\n## Within-lifestyle slopes: ellipticity ~ log_mass + HWI")
for ls, sub in df.groupby("Primary.Lifestyle"):
    if len(sub) < 30: continue
    m = smf.ols("ellipticity ~ log_mass + HWI", data=sub).fit()
    print(f"  {ls:<20s} n={len(sub):4d}  HWI={m.params['HWI']:+.5f} (SE {m.bse['HWI']:.5f}) p={m.pvalues['HWI']:.4f}  R^2={m.rsquared:.3f}")

# A separate, sharper test: within Passeriformes, does lifestyle still predict?
print("\n## Within Passeriformes: ellipticity ~ log_mass + HWI + C(Primary.Lifestyle)")
pass_df = df[df["order"]=="PASSERIFORMES"].copy()
pass_df = pass_df.rename(columns={"Primary.Lifestyle":"Primary_Lifestyle"})
print(f"  n = {len(pass_df)}, lifestyle counts: {pass_df['Primary_Lifestyle'].value_counts().to_dict()}")
mp_flight = smf.ols("ellipticity ~ log_mass + HWI", data=pass_df).fit()
mp_full = smf.ols("ellipticity ~ log_mass + HWI + C(Primary_Lifestyle)", data=pass_df).fit()
print(f"  flight-only R^2 = {mp_flight.rsquared:.4f}, AIC = {mp_flight.aic:.1f}")
print(f"  flight+life R^2 = {mp_full.rsquared:.4f}, AIC = {mp_full.aic:.1f}")
LR_p, df_p, p_p = lrt(mp_flight, mp_full)
print(f"  LRT chi^2 = {LR_p:.3f} on {df_p:.0f} df, p = {p_p:.3g}")
print(f"  M_full HWI coef = {mp_full.params['HWI']:+.5f} (SE {mp_full.bse['HWI']:.5f}) p={mp_full.pvalues['HWI']:.4f}")

# Save summary.
with open("results/06_oviduct_proxy.txt","w") as fh:
    fh.write(f"n = {len(df)}\n")
    fh.write(f"Model 1 (mass+HWI): R^2 = {m1.rsquared:.4f}, AIC = {m1.aic:.1f}\n")
    fh.write(f"Model 2 (mass+lifestyle): R^2 = {m2.rsquared:.4f}, AIC = {m2.aic:.1f}\n")
    fh.write(f"Model 3 (mass+HWI+lifestyle): R^2 = {m3.rsquared:.4f}, AIC = {m3.aic:.1f}\n")
    fh.write(f"LRT M1->M3: chi2 = {LR_a:.3f}, df = {df_a:.0f}, p = {p_a:.3g}\n")
    fh.write(f"LRT M2->M3: chi2 = {LR_b:.3f}, df = {df_b:.0f}, p = {p_b:.3g}\n")
