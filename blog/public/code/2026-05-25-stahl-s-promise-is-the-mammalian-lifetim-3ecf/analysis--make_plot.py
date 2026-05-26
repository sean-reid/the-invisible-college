"""Plot lifetime heartbeats vs body mass."""
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
DATA = HERE / "species_data.csv"
OUT = HERE / "lifetime_heartbeats.png"

MIN_PER_YEAR = 60 * 24 * 365.25

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

log_M = np.array([math.log10(r["mass_g"]) for r in rows])
log_H = np.array([math.log10(r["hr_bpm"] * r["Lmax_yr"] * MIN_PER_YEAR) for r in rows])

# OLS fit
xbar, ybar = log_M.mean(), log_H.mean()
beta = np.sum((log_M - xbar) * (log_H - ybar)) / np.sum((log_M - xbar) ** 2)
alpha = ybar - beta * xbar
fitline_x = np.linspace(log_M.min() - 0.3, log_M.max() + 0.3, 50)
fitline_y = alpha + beta * fitline_x

# Group by order, distinct markers
order_styles = {
    "Rodentia":     ("o", "#1f77b4"),
    "Lagomorpha":   ("s", "#1f77b4"),
    "Carnivora":    ("^", "#d62728"),
    "Artiodactyla": ("D", "#2ca02c"),
    "Perissodactyla": ("v", "#2ca02c"),
    "Proboscidea":  ("P", "#8c564b"),
    "Cetacea":      ("*", "#17becf"),
    "Primates":     ("X", "#9467bd"),
    "Chiroptera":   ("h", "#e377c2"),
    "Eulipotyphla": ("p", "#7f7f7f"),
}

fig, ax = plt.subplots(figsize=(9, 6))

# Horizontal "invariant" reference at mean log H
mean_logH = log_H.mean()
ax.axhline(mean_logH, color="grey", linestyle=":", alpha=0.6,
           label=f"geometric mean H = {10**mean_logH:.2e}")

# OLS fit line
ax.plot(fitline_x, fitline_y, color="black", linewidth=1,
        label=f"OLS: log H = {alpha:.3f} + ({beta:+.3f}) log M")

# Reference: 10^9
ax.axhline(9.0, color="red", linestyle="--", alpha=0.4, label="10^9 heartbeats (folklore)")

# Points by order
plotted_orders = set()
for r, x, y in zip(rows, log_M, log_H):
    style = order_styles.get(r["order"], ("o", "black"))
    label = r["order"] if r["order"] not in plotted_orders else None
    ax.scatter(x, y, marker=style[0], s=90, color=style[1],
               edgecolors="black", linewidths=0.5, label=label, zorder=3)
    plotted_orders.add(r["order"])

# Label outliers
outlier_names = {"Myotis lucifugus", "Heterocephalus glaber", "Homo sapiens",
                 "Rattus norvegicus", "Bos taurus", "Mesocricetus auratus"}
for r, x, y in zip(rows, log_M, log_H):
    if r["species"] in outlier_names:
        dx, dy = 0.15, 0.04
        if r["common"] == "brown rat":
            dy = -0.10
        if r["common"] == "cow":
            dy = 0.04
            dx = -0.65
        if r["common"] == "golden hamster":
            dy = -0.14
            dx = -0.6
        ax.annotate(r["common"], (x, y), xytext=(x + dx, y + dy),
                    fontsize=8.5, alpha=0.85)

ax.set_xlabel("log10 body mass (g)")
ax.set_ylabel("log10 lifetime heartbeats (= f_H · L_max · 525,960)")
ax.set_title("Stahl's promise: lifetime heartbeat count vs body mass\n22 mammals, canonical published sample")
ax.legend(loc="lower left", fontsize=8, ncol=2)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT, dpi=140)
print("Wrote", OUT)
