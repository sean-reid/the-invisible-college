"""Extended grid: more covariates, order-level subset fits, asymmetry models.

Pre-registered grid (locked before any inspection of extended-model output):
  Responses:        {ellipticity, asymmetry}
  Models:           {OLS, MixedLM-Order, MixedLM-Family, OrderBoot-OLS}
  Covariate adds:   {none, +log_wing, +log_tarsus, +log_wing+log_tarsus+Kipps}
  Order-level subset fits restricted to orders with n >= 30.

Rejection rule (locked):
  "The HWI coefficient is 'fragile' if the sign flips, or if at least one cell
  in the locked grid yields a 95% CI containing zero, while at least one other
  cell yields a 95% CI excluding zero by a margin >= 2 standard errors."
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM

os.makedirs("results", exist_ok=True)
df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["Mass", "Hand.Wing.Index", "asymmetry", "ellipticity"]).copy()
df["log_mass"]  = np.log10(df["Mass"])
df["HWI"]       = df["Hand.Wing.Index"]
df["log_wing"]  = np.log10(df["Wing.Length"])
df["log_tarsus"]= np.log10(df["Tarsus.Length"])
df["log_kipps"] = np.log10(df["Kipps.Distance"].replace(0, np.nan))

cov_sets = {
    "base":   ["log_mass", "HWI"],
    "+wing":  ["log_mass", "HWI", "log_wing"],
    "+tarsus":["log_mass", "HWI", "log_tarsus"],
    "+all":   ["log_mass", "HWI", "log_wing", "log_tarsus", "log_kipps"],
}

def fit_block(response, cov_label, covs, dfx):
    rec = {"response": response, "covariates": cov_label, "n": int(dfx[[response] + covs].dropna().shape[0])}
    sub = dfx.dropna(subset=[response] + covs).copy()
    formula = response + " ~ " + " + ".join(covs)
    # OLS
    try:
        m = smf.ols(formula, data=sub).fit()
        rec["OLS_HWI"]    = m.params["HWI"]
        rec["OLS_HWI_se"] = m.bse["HWI"]
        ci = m.conf_int().loc["HWI"].values
        rec["OLS_HWI_lo"] = ci[0]; rec["OLS_HWI_hi"] = ci[1]
        rec["OLS_mass"]   = m.params["log_mass"]; rec["OLS_mass_se"] = m.bse["log_mass"]
        rec["OLS_R2"]     = m.rsquared
    except Exception as e:
        rec["OLS_HWI"] = np.nan
    # MixedLM Order
    try:
        mlm = MixedLM.from_formula(formula, data=sub, groups=sub["order"]).fit(method="lbfgs", maxiter=400)
        rec["MLM_O_HWI"] = mlm.params["HWI"]; rec["MLM_O_HWI_se"] = mlm.bse["HWI"]
        ci = mlm.conf_int().loc["HWI"].values
        rec["MLM_O_HWI_lo"] = ci[0]; rec["MLM_O_HWI_hi"] = ci[1]
        rec["MLM_O_mass"]   = mlm.params["log_mass"]; rec["MLM_O_mass_se"] = mlm.bse["log_mass"]
    except Exception as e:
        rec["MLM_O_HWI"] = np.nan
    # MixedLM Family
    try:
        mlmf = MixedLM.from_formula(formula, data=sub, groups=sub["family"]).fit(method="lbfgs", maxiter=400)
        rec["MLM_F_HWI"] = mlmf.params["HWI"]; rec["MLM_F_HWI_se"] = mlmf.bse["HWI"]
        ci = mlmf.conf_int().loc["HWI"].values
        rec["MLM_F_HWI_lo"] = ci[0]; rec["MLM_F_HWI_hi"] = ci[1]
        rec["MLM_F_mass"]   = mlmf.params["log_mass"]; rec["MLM_F_mass_se"] = mlmf.bse["log_mass"]
    except Exception as e:
        rec["MLM_F_HWI"] = np.nan
    return rec

records = []
for resp in ["ellipticity", "asymmetry"]:
    for cov_label, covs in cov_sets.items():
        rec = fit_block(resp, cov_label, covs, df)
        records.append(rec)

R = pd.DataFrame(records)
out_cols = ["response","covariates","n",
            "OLS_HWI","OLS_HWI_lo","OLS_HWI_hi","OLS_R2",
            "MLM_O_HWI","MLM_O_HWI_lo","MLM_O_HWI_hi",
            "MLM_F_HWI","MLM_F_HWI_lo","MLM_F_HWI_hi",
            "OLS_mass","MLM_O_mass","MLM_F_mass"]
R = R[out_cols]
print(R.to_string(float_format="%.5f"))
R.to_csv("results/02_extended_grid.csv", index=False)

# Order-level subset fits.
print("\n## Order-level subset fits (orders with n >= 30): ellipticity ~ log_mass + HWI")
subset_records = []
for o, sub in df.groupby("order"):
    if len(sub) < 30: continue
    try:
        m = smf.ols("ellipticity ~ log_mass + HWI", data=sub).fit()
        rec = {"order": o, "n": len(sub),
               "HWI": m.params["HWI"], "HWI_se": m.bse["HWI"],
               "HWI_p": m.pvalues["HWI"],
               "mass": m.params["log_mass"], "mass_se": m.bse["log_mass"],
               "mass_p": m.pvalues["log_mass"], "R2": m.rsquared}
        subset_records.append(rec)
    except Exception as e:
        print(f"  {o}: {e}")
SubR = pd.DataFrame(subset_records).sort_values("n", ascending=False)
print(SubR.to_string(float_format="%.5f"))
SubR.to_csv("results/03_order_subset.csv", index=False)

# Are the within-order HWI coefficients consistently positive?
n_pos = (SubR["HWI"] > 0).sum()
n_total = len(SubR)
print(f"\nWithin-order HWI coefficient sign: {n_pos}/{n_total} orders positive")
# Sign test against null of 50/50
from scipy.stats import binomtest
bt = binomtest(int(n_pos), int(n_total), p=0.5, alternative="two-sided")
print(f"Sign-test p (two-sided binomial vs 0.5): {bt.pvalue:.4f}")
print(f"Mean within-order HWI coefficient: {SubR['HWI'].mean():.5f}")
print(f"Median within-order HWI coefficient: {SubR['HWI'].median():.5f}")
