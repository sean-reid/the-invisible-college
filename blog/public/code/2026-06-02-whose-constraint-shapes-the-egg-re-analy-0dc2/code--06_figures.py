"""Figures for the egg-shape re-analysis."""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.formula.api as smf

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "figure.dpi": 110,
})

os.makedirs("figures", exist_ok=True)
df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["Mass","Hand.Wing.Index","ellipticity","asymmetry","Primary.Lifestyle"]).copy()
df["log_mass"]=np.log10(df["Mass"]); df["HWI"]=df["Hand.Wing.Index"]

# -----------------------------------------------------------
# Figure 1: HWI vs ellipticity, colored by Primary.Lifestyle.
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))
palette = {
    "Aerial":      "#1f77b4",
    "Aquatic":     "#17becf",
    "Generalist":  "#bcbd22",
    "Insessorial": "#d62728",
    "Terrestrial": "#8c564b",
}
order = ["Aerial","Aquatic","Terrestrial","Generalist","Insessorial"]
for ls in order:
    sub = df[df["Primary.Lifestyle"]==ls]
    ax.scatter(sub["HWI"], sub["ellipticity"], s=10, alpha=0.55,
               color=palette[ls], label=f"{ls} (n={len(sub)})", linewidth=0)
    if len(sub) >= 30:
        m = smf.ols("ellipticity ~ HWI", data=sub).fit()
        xs = np.linspace(sub["HWI"].min(), sub["HWI"].max(), 50)
        ax.plot(xs, m.params["Intercept"] + m.params["HWI"]*xs,
                color=palette[ls], lw=1.5)
ax.set_xlabel("Hand-wing index (Sheard et al. / AVONET)")
ax.set_ylabel("Egg ellipticity (Stoddard et al. 2017)")
ax.set_title("Hand-wing index vs. egg ellipticity, by primary lifestyle (n=1,145 species)")
ax.legend(frameon=False, fontsize=9, loc="upper left")
plt.tight_layout()
plt.savefig("figures/fig1_hwi_ellipticity_by_lifestyle.png", dpi=180)
plt.close()

# -----------------------------------------------------------
# Figure 2: forest plot of HWI coefficients across specifications.
# -----------------------------------------------------------
cells = []
# Whole-sample specifications.
from statsmodels.regression.mixed_linear_model import MixedLM
def add_cell(label, coef, lo, hi):
    cells.append({"label":label,"coef":coef,"lo":lo,"hi":hi})

# OLS base
m = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit()
ci = m.conf_int().loc["HWI"]
add_cell("OLS, base (n=1145)", m.params["HWI"], ci[0], ci[1])

# OLS + body shape covariates
df["log_wing"]=np.log10(df["Wing.Length"]); df["log_tarsus"]=np.log10(df["Tarsus.Length"])
m = smf.ols("ellipticity ~ log_mass + HWI + log_wing + log_tarsus", data=df).fit()
ci = m.conf_int().loc["HWI"]
add_cell("OLS, + wing + tarsus", m.params["HWI"], ci[0], ci[1])

# Cluster-robust SE (order)
m = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["order"]})
ci = m.conf_int().loc["HWI"]
add_cell("OLS, cluster-robust (Order)", m.params["HWI"], ci[0], ci[1])

# MLM-Order
mlm = MixedLM.from_formula("ellipticity ~ log_mass + HWI", data=df, groups=df["order"]).fit(method="lbfgs", maxiter=400)
ci = mlm.conf_int().loc["HWI"]
add_cell("MLM, random intercept Order", mlm.params["HWI"], ci[0], ci[1])

# MLM-Order + body shape
mlm2 = MixedLM.from_formula("ellipticity ~ log_mass + HWI + log_wing + log_tarsus", data=df, groups=df["order"]).fit(method="lbfgs", maxiter=400)
ci = mlm2.conf_int().loc["HWI"]
add_cell("MLM Order + wing + tarsus", mlm2.params["HWI"], ci[0], ci[1])

# MLM-Family
mlmf = MixedLM.from_formula("ellipticity ~ log_mass + HWI", data=df, groups=df["family"]).fit(method="lbfgs", maxiter=400)
ci = mlmf.conf_int().loc["HWI"]
add_cell("MLM, random intercept Family", mlmf.params["HWI"], ci[0], ci[1])

# MLM-Family + body shape
mlmf2 = MixedLM.from_formula("ellipticity ~ log_mass + HWI + log_wing + log_tarsus", data=df, groups=df["family"]).fit(method="lbfgs", maxiter=400)
ci = mlmf2.conf_int().loc["HWI"]
add_cell("MLM Family + wing + tarsus", mlmf2.params["HWI"], ci[0], ci[1])

# Order-level subsets with n >= 30
for o in ["PASSERIFORMES","CHARADRIIFORMES","ANSERIFORMES","GALLIFORMES","ACCIPITRIFORMES","COLUMBIFORMES"]:
    sub = df[df["order"]==o]
    if len(sub) < 30: continue
    m = smf.ols("ellipticity ~ log_mass + HWI", data=sub).fit()
    ci = m.conf_int().loc["HWI"]
    add_cell(f"{o.title()} only (n={len(sub)})", m.params["HWI"], ci[0], ci[1])

# Within lifestyles
for ls in ["Aerial","Aquatic","Terrestrial","Generalist","Insessorial"]:
    sub = df[df["Primary.Lifestyle"]==ls]
    if len(sub) < 30: continue
    m = smf.ols("ellipticity ~ log_mass + HWI", data=sub).fit()
    ci = m.conf_int().loc["HWI"]
    add_cell(f"{ls} only (n={len(sub)})", m.params["HWI"], ci[0], ci[1])

C = pd.DataFrame(cells)
C.to_csv("results/07_forest_plot_data.csv", index=False)

fig, ax = plt.subplots(figsize=(8.5, 7.5))
ys = np.arange(len(C))[::-1]
ax.errorbar(C["coef"], ys, xerr=[C["coef"]-C["lo"], C["hi"]-C["coef"]],
            fmt="o", color="black", markersize=4.5, capsize=2.5, lw=1)
ax.axvline(0, color="grey", lw=0.8, linestyle="--")
ax.set_yticks(ys)
ax.set_yticklabels(C["label"], fontsize=9)
ax.set_xlabel(r"HWI coefficient ($\beta_{\mathrm{HWI}}$) on ellipticity, with 95% CI")
ax.set_title("Sensitivity of the HWI-ellipticity coefficient across specifications", fontsize=11)

# Add category dividers
cat_starts = [0, 7, 13]
for i in cat_starts[1:]:
    ax.axhline(ys[i]+0.5, color="lightgrey", lw=0.5)

# Add bracket labels
ax.text(ax.get_xlim()[1]*1.02, ys[3], "Whole-sample\nspecifications", va="center", fontsize=8, color="grey")
ax.text(ax.get_xlim()[1]*1.02, ys[10], "Order subsets", va="center", fontsize=8, color="grey")
ax.text(ax.get_xlim()[1]*1.02, ys[15], "Lifestyle subsets", va="center", fontsize=8, color="grey")

plt.tight_layout()
plt.savefig("figures/fig2_forest_plot.png", dpi=180)
plt.close()

# -----------------------------------------------------------
# Figure 3: residual map by order
# -----------------------------------------------------------
m = smf.ols("ellipticity ~ log_mass + HWI", data=df).fit()
df["resid"] = m.resid
order_stats = df.groupby("order")["resid"].agg(["mean","std","count"]).reset_index()
order_stats = order_stats[order_stats["count"] >= 10].sort_values("mean")
order_stats["se"] = order_stats["std"]/np.sqrt(order_stats["count"])

fig, ax = plt.subplots(figsize=(8.5, 5.0))
ys = np.arange(len(order_stats))
ax.errorbar(order_stats["mean"], ys, xerr=order_stats["se"]*1.96,
            fmt="s", color="black", markersize=4, capsize=2)
ax.axvline(0, color="grey", lw=0.8, linestyle="--")
ax.set_yticks(ys)
ax.set_yticklabels([o + f"  (n={n})" for o,n in zip(order_stats["order"], order_stats["count"])],
                   fontsize=9)
ax.set_xlabel("Mean residual ellipticity after OLS(mass + HWI)\n(95% CI around mean)")
ax.set_title("Clade-level residual structure: the fit explains \na minority of inter-order variance in egg shape", fontsize=11)
plt.tight_layout()
plt.savefig("figures/fig3_order_residuals.png", dpi=180)
plt.close()

# -----------------------------------------------------------
# Figure 4: ellipticity histograms for a few flagged orders
# -----------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(12, 3.4), sharex=True, sharey=True)
flagged = [("STRIGIFORMES", "Owls — round eggs"),
           ("APODIFORMES", "Swifts & hummingbirds — pointed eggs"),
           ("ANSERIFORMES", "Ducks & geese"),
           ("PASSERIFORMES", "Passerines (perching birds)")]
all_e = df["ellipticity"]
for ax,(o, label) in zip(axes, flagged):
    sub = df[df["order"]==o]
    ax.hist(all_e, bins=30, alpha=0.18, color="grey", density=True, label="All 1145")
    if len(sub) > 0:
        ax.hist(sub["ellipticity"], bins=18, alpha=0.65, color="C0", density=True, label=f"{o} (n={len(sub)})")
    ax.set_title(label, fontsize=9.5)
    ax.set_xlabel("ellipticity")
axes[0].set_ylabel("density")
plt.tight_layout()
plt.savefig("figures/fig4_clade_histograms.png", dpi=180)
plt.close()

print("Wrote figures/fig1_hwi_ellipticity_by_lifestyle.png")
print("Wrote figures/fig2_forest_plot.png")
print("Wrote figures/fig3_order_residuals.png")
print("Wrote figures/fig4_clade_histograms.png")
