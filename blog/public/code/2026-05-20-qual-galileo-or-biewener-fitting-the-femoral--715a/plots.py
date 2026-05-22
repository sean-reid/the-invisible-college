"""
Produce the two diagnostic plots committed in the proposal:
  1. log-log scatter of log10(FC) vs log10(M), with fitted OLS line and the
     two reference slopes (Galileo: beta_C = 1/3; Biewener: beta_C = 1/4).
  2. residual-versus-mass plot, keyed by Mon.Group (mammalian superorder).
"""

import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

rows = []
with open(os.path.join(HERE, "extants.csv")) as f:
    for r in csv.DictReader(f):
        try:
            BM = float(r["BM"]); FC = float(r["FC"])
        except (ValueError, KeyError):
            continue
        if BM <= 0 or FC <= 0:
            continue
        if r["Mon.Groups"] == "Reptilia":
            continue
        rows.append(dict(group=r["Mon.Groups"], species=r["Species"],
                         BM_kg=BM/1000.0, FC=FC))

x = np.array([math.log10(r["BM_kg"]) for r in rows])
y = np.array([math.log10(r["FC"]) for r in rows])

A = np.column_stack([np.ones(len(x)), x])
b_ols, *_ = np.linalg.lstsq(A, y, rcond=None)
intercept, slope = float(b_ols[0]), float(b_ols[1])
yhat = intercept + slope * x
resid = y - yhat
print(f"OLS: intercept={intercept:.4f}, slope (beta_C)={slope:.4f}")

# Group palette
groups = sorted(set(r["group"] for r in rows))
cmap = plt.get_cmap("tab10")
colors = {g: cmap(i % 10) for i, g in enumerate(groups)}

# --- Figure 1: log-log scatter with fit and reference slopes ---
fig, ax = plt.subplots(figsize=(8, 6))
for g in groups:
    mask = np.array([r["group"] == g for r in rows])
    ax.scatter(x[mask], y[mask], s=18, alpha=0.7, label=g, color=colors[g])

xline = np.linspace(x.min(), x.max(), 100)
yfit = intercept + slope * xline
# Reference slopes pass through the centroid (xbar, ybar)
xbar, ybar = x.mean(), y.mean()
y_galileo = ybar + (1.0/3.0) * (xline - xbar)        # beta_C = 1/3
y_biewener = ybar + (1.0/4.0) * (xline - xbar)       # beta_C = 1/4

ax.plot(xline, yfit, "k-", lw=2,
        label=f"OLS fit (β_C = {slope:.3f})")
ax.plot(xline, y_galileo, "b--", lw=1.5,
        label="Galileo (β_C = 1/3 → β_I = 4/3)")
ax.plot(xline, y_biewener, "r--", lw=1.5,
        label="Biewener (β_C = 1/4 → β_I = 1)")

ax.set_xlabel("log₁₀ body mass (kg)")
ax.set_ylabel("log₁₀ femoral circumference (mm)")
ax.set_title("Femoral circumference vs body mass, n=198 mammals\n"
             "(Campione & Evans 2012)")
ax.legend(loc="upper left", fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "fig_scatter.png"), dpi=160)
plt.close()
print("saved fig_scatter.png")

# --- Figure 2: residual vs mass, keyed by group ---
fig, ax = plt.subplots(figsize=(8, 5))
for g in groups:
    mask = np.array([r["group"] == g for r in rows])
    ax.scatter(x[mask], resid[mask], s=22, alpha=0.75,
               label=g, color=colors[g])
ax.axhline(0, color="k", lw=1)
# Mark the +/- 2 sd band
sd = float(resid.std())
ax.axhline(2*sd, color="grey", ls=":", lw=1)
ax.axhline(-2*sd, color="grey", ls=":", lw=1)

# Label the four largest-magnitude residuals
order = np.argsort(np.abs(resid))[::-1][:4]
for i in order:
    ax.annotate(rows[i]["species"], (x[i], resid[i]),
                xytext=(4, 4), textcoords="offset points",
                fontsize=7, alpha=0.85)

ax.set_xlabel("log₁₀ body mass (kg)")
ax.set_ylabel("residual on log₁₀ FC (mm)")
ax.set_title(f"OLS residuals vs body mass, n={len(rows)} (sd={sd:.3f})")
ax.legend(loc="best", fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "fig_residuals.png"), dpi=160)
plt.close()
print("saved fig_residuals.png")
