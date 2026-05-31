"""Generate publication figures for the isotherm paper."""
import json, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

MOUNTAINS = ['Chimborazo', 'Cotopaxi', 'Misti', 'Chachani']
REGIMES = {'Chimborazo': 'wet', 'Cotopaxi': 'wet', 'Misti': 'dry', 'Chachani': 'dry'}
COLORS = {'wet': '#2166ac', 'dry': '#d6604d'}
THRESHOLD_PCT = 80

def load_records(m):
    with open(f'cache_elev_{m}.json') as f:
        return json.load(f)

def load_lapse(m):
    with open(f'cache_lapse_{m}.json') as f:
        return json.load(f)

# ── FIGURE 1: Bray-Curtis dissimilarity profiles ─────────────────────────────
with open('results.json') as f:
    results = json.load(f)

fig, axes = plt.subplots(2, 2, figsize=(10, 9), sharex=False, sharey=False)
axes = axes.flatten()

for i, m in enumerate(MOUNTAINS):
    ax = axes[i]
    data = results[m]
    bc_rows = data['bc_profile']
    if not bc_rows:
        continue

    mids = [r['mid_elev'] for r in bc_rows]
    bcs  = [r['bc'] for r in bc_rows]
    thresh = np.percentile(bcs, THRESHOLD_PCT)
    color = COLORS[REGIMES[m]]

    ax.bar(mids, bcs, width=90, color=color, alpha=0.7, label='BC dissimilarity')
    ax.axhline(thresh, color='black', linewidth=1, linestyle='--',
               label=f'80th pct ({thresh:.3f})')

    # Annotate candidate zone boundaries
    for r in bc_rows:
        if r['bc'] >= thresh:
            ax.axvline(r['mid_elev'], color='gray', linewidth=0.7, alpha=0.6)

    ax.set_title(f"{m}\n({REGIMES[m]}, ERA5 LR={load_lapse(m)['lr']:.2f}°C/km)",
                 fontsize=11)
    ax.set_xlabel('Elevation (m)', fontsize=9)
    ax.set_ylabel('Bray-Curtis dissimilarity', fontsize=9)
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)

    # Shade the 3100-3300m window
    ax.axvspan(3100, 3300, alpha=0.12, color='green', zorder=0, label='3100-3300m window')

fig.suptitle('Bray-Curtis assemblage turnover profiles\n'
             'Wet (Ecuador, blue) vs Dry (Peru, red) mountains',
             fontsize=13, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('fig1_bray_curtis.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig1_bray_curtis.png saved")

# ── FIGURE 2: Species richness per elevation band ─────────────────────────────
BAND = 100

fig, axes = plt.subplots(2, 2, figsize=(10, 9), sharex=False, sharey=True)
axes = axes.flatten()

for i, m in enumerate(MOUNTAINS):
    ax = axes[i]
    records = load_records(m)
    df = pd.DataFrame(records).dropna(subset=['elev', 'speciesKey'])
    df['elev'] = df['elev'].astype(float)
    df['speciesKey'] = df['speciesKey'].astype(str)

    min_e = int(df['elev'].min() // BAND * BAND)
    max_e = int(df['elev'].max() // BAND * BAND) + BAND
    bands = range(min_e, max_e, BAND)

    band_centers = []
    n_species = []
    for b in bands:
        mask = (df['elev'] >= b) & (df['elev'] < b + BAND)
        subset = df[mask]
        if len(subset) >= 3:
            band_centers.append(b + BAND/2)
            n_species.append(subset['speciesKey'].nunique())

    color = COLORS[REGIMES[m]]
    ax.barh(band_centers, n_species, height=BAND*0.85, color=color, alpha=0.7)
    ax.axhline(3200, color='green', linewidth=1.5, linestyle='--', label='3200m')
    ax.set_title(f"{m} ({REGIMES[m]})", fontsize=11)
    ax.set_xlabel('Species richness per 100m band', fontsize=9)
    ax.set_ylabel('Elevation (m)', fontsize=9)
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)

fig.suptitle('Species richness per 100m elevation band\n'
             'Wet (Ecuador, blue) vs Dry (Peru, red) mountains',
             fontsize=13, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('fig2_species_richness.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig2_species_richness.png saved")

# ── FIGURE 3: Cross-mountain temperature comparison ──────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))

pub_lr = {'Chimborazo': 6.0, 'Cotopaxi': 6.0, 'Misti': 7.0, 'Chachani': 7.0}
elevs = np.linspace(1000, 6000, 200)

for m in MOUNTAINS:
    lap = load_lapse(m)
    color = COLORS[REGIMES[m]]
    ls_era5 = '-'
    ls_pub = '--'

    T_era5 = lap['intercept'] - lap['lr'] / 1000 * elevs
    T_pub  = lap['intercept'] - pub_lr[m] / 1000 * elevs

    label = f"{m} (ERA5)" if m in ['Chimborazo', 'Misti'] else None
    ax.plot(T_era5, elevs, color=color, linewidth=1.5, linestyle=ls_era5, label=label)

    label2 = f"{m} (pub)" if m in ['Chimborazo', 'Misti'] else None
    ax.plot(T_pub, elevs, color=color, linewidth=1.5, linestyle=ls_pub, label=label2, alpha=0.7)

# Draw 10°C vertical line
ax.axvline(10.0, color='green', linewidth=1.5, linestyle=':', label='10°C isotherm')

# Draw the ~3200m zone boundary reference line
ax.axhline(3200, color='gray', linewidth=1, linestyle=':', label='3200m boundary')

ax.set_xlabel('Mean Annual Temperature (°C, ERA5 extrapolation)', fontsize=11)
ax.set_ylabel('Elevation (m)', fontsize=11)
ax.set_title('Temperature-elevation profiles: ERA5 (solid) vs Published (dashed)\n'
             'Wet/Ecuador (blue) vs Dry/Peru (red)', fontsize=11)
ax.legend(fontsize=9, loc='upper right')
ax.set_xlim(-15, 32)
ax.set_ylim(1000, 5500)
ax.grid(True, alpha=0.3)

# Annotate convergence vs divergence at 3200m
ax.annotate('ERA5 temperatures\nconverge at 3200m\n(~10°C for all)',
            xy=(10, 3200), xytext=(16, 3600),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=9, color='gray',
            ha='center')

plt.tight_layout()
plt.savefig('fig3_temperature_profiles.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig3_temperature_profiles.png saved")

# ── FIGURE 4: Power analysis ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

delta_lrs = np.linspace(0, 2.0, 100)  # lapse rate contrast in °C/1000m
T_threshold = 10.0

# Use ERA5 parameters for wet (Cotopaxi-like) and dry (Misti-like)
T_wet  = load_lapse('Cotopaxi')['intercept']
lr_wet = 6.0  # published
T_dry  = load_lapse('Misti')['intercept']

for lr_wet_val, label in [(5.5, 'ERA5 LR = 5.5°C/km'), (6.0, 'Pub LR wet = 6.0°C/km')]:
    delta_elevs = []
    for dlr in delta_lrs:
        lr_dry_val = lr_wet_val + dlr
        h_wet = (T_wet - T_threshold) / (lr_wet_val / 1000)
        h_dry = (T_dry - T_threshold) / (lr_dry_val / 1000)
        delta_elevs.append(abs(h_wet - h_dry))
    ax.plot(delta_lrs, delta_elevs, label=label, linewidth=2)

ax.axhline(100, color='gray', linestyle='--', linewidth=1, label='100m (1 elevation band)')
ax.axvline(1.0, color='orange', linestyle=':', linewidth=1.5,
           label='Published LR contrast (~1.0°C/km)')

ax.set_xlabel('Lapse rate contrast: dry − wet (°C per 1000m)', fontsize=11)
ax.set_ylabel('Predicted elevation difference\nat 10°C boundary (m)', fontsize=11)
ax.set_title('Power analysis: detectable lapse rate contrast\n'
             'at the 10°C isotherm boundary', fontsize=11)
ax.legend(fontsize=9)
ax.set_xlim(0, 2)
ax.set_ylim(0, 800)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig4_power_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("fig4_power_analysis.png saved")

print("\nAll figures generated.")
