"""
Supplementary analysis:
1. Published lapse rate comparison at the ~3200m boundary
2. Species richness per elevation band for each mountain
3. Power calculation: minimum lapse rate contrast needed to distinguish hypotheses
"""
import json, math
import numpy as np
import pandas as pd

# Published lapse rates from literature
# Ecuador wet mountains: Bendix et al. (2008) JGR, Celeri & Buytaert (2012)
# Peru dry mountains: Vuille & Bradley (2000) J Climate, Seltzer (1994)
PUB_LAPSE = {
    "Chimborazo": {"lr": 6.0, "se": 0.4, "source": "Bendix et al. 2008"},
    "Cotopaxi":   {"lr": 6.0, "se": 0.4, "source": "Bendix et al. 2008"},
    "Misti":      {"lr": 7.0, "se": 0.5, "source": "Vuille & Bradley 2000"},
    "Chachani":   {"lr": 7.0, "se": 0.5, "source": "Vuille & Bradley 2000"},
}

# Load ERA5 regression results
ERA5 = {}
for m in ['Chimborazo', 'Cotopaxi', 'Misti', 'Chachani']:
    with open(f'cache_lapse_{m}.json') as f:
        ERA5[m] = json.load(f)

print("=" * 65)
print("1. ERA5 vs Published Lapse Rates")
print("=" * 65)
print(f"\n{'Mountain':12s} {'ERA5 LR':>10s} {'Pub LR':>10s} {'ERA5 R²':>8s} {'Regime':8s}")
regimes = {"Chimborazo": "wet", "Cotopaxi": "wet", "Misti": "dry", "Chachani": "dry"}
for m in ['Chimborazo', 'Cotopaxi', 'Misti', 'Chachani']:
    e = ERA5[m]
    p = PUB_LAPSE[m]
    r = regimes[m]
    print(f"{m:12s} {e['lr']:8.2f}   {p['lr']:8.2f}   {e['r2']:7.4f}  {r}")

print("\n2. Temperature at the ~3200m assemblage boundary")
print("=" * 65)
print("(~3200m is where a consistent high-BC boundary appears across all mountains)")
print()
TARGET_ELEV = 3200

# ERA5 temperatures at 3200m
print(f"{'Mountain':12s} {'ERA5 T@3200m':>13s}  {'Pub T@3200m':>13s}  {'Regime':8s}")
era5_temps = []
pub_temps = []
for m in ['Chimborazo', 'Cotopaxi', 'Misti', 'Chachani']:
    e = ERA5[m]
    p = PUB_LAPSE[m]
    r = regimes[m]
    # ERA5: T = intercept - lr/1000 * elev
    era5_t = e['intercept'] - e['lr'] / 1000 * TARGET_ELEV
    # Published: use ERA5 intercept but with published lapse rate
    pub_t = e['intercept'] - p['lr'] / 1000 * TARGET_ELEV
    era5_temps.append(era5_t)
    pub_temps.append(pub_t)
    print(f"{m:12s}  {era5_t:12.2f}°C  {pub_t:12.2f}°C  {r}")

print(f"\nSD of ERA5 temperatures at 3200m:      {np.std(era5_temps):.2f}°C")
print(f"SD of Published temperatures at 3200m:  {np.std(pub_temps):.2f}°C")
print(f"Variance ratio (pub/era5):              {np.var(pub_temps)/np.var(era5_temps):.1f}×")

print("\n3. Power analysis: minimum lapse rate contrast for the test")
print("=" * 65)
# If wet mountains have LR_wet and dry mountains have LR_dry,
# and the same zone boundary appears at T_threshold,
# then the elevation difference is:
#   h_dry = (T_base_dry - T_threshold) / LR_dry
#   h_wet = (T_base_wet - T_threshold) / LR_wet
# For the test to be informative, |h_wet - h_dry| > precision of GBIF elevations

# Approximate base temperatures (from ERA5 intercepts)
T_base = {m: ERA5[m]['intercept'] for m in ERA5}
T_threshold = 10.0  # °C, approximately the páramo/montane forest boundary

print(f"\nAssumptions: T_threshold = {T_threshold}°C, T_base from ERA5 intercepts")
print(f"{'Wet mountain':14s}  {'Dry mountain':14s}  {'ΔLAPSE':>8s}  {'ΔElev (m)':>10s}")

for wet in ['Chimborazo', 'Cotopaxi']:
    for dry in ['Misti', 'Chachani']:
        for dlr in [0.5, 1.0, 1.5]:  # lapse rate contrasts in °C/1000m
            lr_wet = ERA5[wet]['lr']
            lr_dry = lr_wet + dlr
            h_wet = (T_base[wet] - T_threshold) / (lr_wet / 1000)
            h_dry = (T_base[dry] - T_threshold) / (lr_dry / 1000)
            delta_h = abs(h_wet - h_dry)
            print(f"{wet:14s}  {dry:14s}  {dlr:+7.1f}  {delta_h:10.0f}m")

print("\n4. Species richness and record counts per elevation band")
print("=" * 65)

def load_records(m):
    with open(f'cache_elev_{m}.json') as f:
        return json.load(f)

BAND = 100

for m in ['Chimborazo', 'Cotopaxi', 'Misti', 'Chachani']:
    records = load_records(m)
    df = pd.DataFrame(records)
    df = df.dropna(subset=['elev', 'speciesKey'])
    df['elev'] = df['elev'].astype(float)
    df['speciesKey'] = df['speciesKey'].astype(str)

    min_e = int(df['elev'].min() // BAND * BAND)
    max_e = int(df['elev'].max() // BAND * BAND) + BAND
    bands = range(min_e, max_e, BAND)

    r = regimes[m]
    era5_lr = ERA5[m]['lr']
    print(f"\n{m} ({r}, ERA5 LR={era5_lr:.2f}°C/km):")
    print(f"  {'Band (m)':10s} {'N_records':>10s} {'N_species':>10s}")
    for b in bands:
        mask = (df['elev'] >= b) & (df['elev'] < b + BAND)
        subset = df[mask]
        if len(subset) > 0:
            n_rec = len(subset)
            n_sp = subset['speciesKey'].nunique()
            print(f"  {b:4d}-{b+BAND:<4d}  {n_rec:10d}  {n_sp:10d}")

print("\n5. Bray-Curtis dissimilarity profiles (from results)")
print("=" * 65)

with open('results.json') as f:
    results = json.load(f)

for m_name, data in results.items():
    bc_profile = data.get('bc_profile', [])
    if not bc_profile:
        continue
    print(f"\n{m_name} ({data['regime']}):")
    print(f"  {'Band_lo':8s} {'Band_hi':8s} {'Mid':8s} {'BC':8s} {'N_sp_lo':8s} {'N_sp_hi':8s}")
    for row in bc_profile:
        star = " *" if row['bc'] >= np.percentile([r['bc'] for r in bc_profile], 80) else ""
        print(f"  {row['band_lower']:7.0f}  {row['band_upper']:7.0f}  {row['mid_elev']:7.0f}  "
              f"{row['bc']:7.3f}  {row['n_sp_lo']:7d}  {row['n_sp_hi']:7d}{star}")
