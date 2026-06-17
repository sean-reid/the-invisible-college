#!/usr/bin/env python3
"""
Render the weekly-resolution coxcomb visualization.

This script creates a polar-area diagram (coxcomb) where:
- Each wedge represents one week (chronological order)
- Wedge width is constant (one week ≈ 2.3 degrees)
- Wedge area is proportional to preventable deaths in that week
- Color represents the cause category (disease, wounds, other)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('weekly_mortality_data.csv')
interventions = pd.read_csv('interventions.csv')

n_weeks = len(df)
week_numbers = df['week_number'].values
preventable = df['preventable_deaths'].values
wounds = df['wound_deaths'].values
other = df['other_deaths'].values

print(f"Creating coxcomb for {n_weeks} weeks")

# ============================================================================
# Create the coxcomb visualization
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(projection='polar'))

# Each week gets constant angular width
degrees_per_week = 360.0 / n_weeks  # ≈ 2.31 degrees per week
theta_start = 0

# Color scheme: disease (red), wounds (blue), other (gray)
colors = {
    'preventable': '#d62728',    # Red
    'wounds': '#1f77b4',          # Blue
    'other': '#7f7f7f'            # Gray
}

# Maximum radius will be scaled to the largest preventable death count
max_preventable = preventable.max()
# Add some margin
max_radius = max_preventable * 1.15

# Find intervention weeks for marking on the plot
intervention_weeks = interventions['week_number'].values

print(f"Intervention weeks: {intervention_weeks}")

# Build the coxcomb: each death type gets a concentric ring
# Ring 1 (outermost): preventable deaths
# Ring 2: wounds
# Ring 3 (innermost): other

for week_idx in range(n_weeks):
    theta_start_rad = np.radians(theta_start)
    theta_end_rad = np.radians(theta_start + degrees_per_week)

    # Radius for this week's data (proportional to death count)
    r_preventable = preventable[week_idx]
    r_wounds = wounds[week_idx]
    r_other = other[week_idx]

    # Wedge 1: Preventable deaths (outermost)
    wedge1 = Wedge((0, 0), r_preventable, theta_start, theta_start + degrees_per_week,
                   facecolor=colors['preventable'], edgecolor='none', alpha=0.8, zorder=1)
    ax.add_patch(wedge1)

    # Wedge 2: Wounds (middle)
    wedge2 = Wedge((0, 0), r_wounds, theta_start, theta_start + degrees_per_week,
                   facecolor=colors['wounds'], edgecolor='none', alpha=0.8, zorder=2)
    ax.add_patch(wedge2)

    # Wedge 3: Other (innermost)
    wedge3 = Wedge((0, 0), r_other, theta_start, theta_start + degrees_per_week,
                   facecolor=colors['other'], edgecolor='none', alpha=0.8, zorder=3)
    ax.add_patch(wedge3)

    # Mark interventions with thin radial lines
    if (week_idx + 1) in intervention_weeks:
        theta_mid = np.radians(theta_start + degrees_per_week / 2)
        ax.plot([theta_mid, theta_mid], [0, max_radius * 1.1],
                'k-', linewidth=0.8, alpha=0.5, zorder=0)

    theta_start += degrees_per_week

# Set radial limits
ax.set_ylim(0, max_radius * 1.15)

# Set angle labels (show month markers at 13-week intervals, approximate to months)
# 13 weeks ≈ 3 months
month_weeks = [4, 17, 30, 43, 56, 69, 82, 95, 108, 121, 134, 147, 156]
month_labels = [
    'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',  # 1854
    'Jan', 'Feb', 'Mar', 'Apr'  # 1855-1856 sample
]

angle_ticks = [(w - 1) * degrees_per_week for w in month_weeks]
ax.set_xticks([np.radians(a) for a in angle_ticks])
ax.set_xticklabels(month_labels, fontsize=10)

# Clean up radial axis
ax.set_yticks([100, 200, 300, 400])
ax.set_yticklabels(['100', '200', '300', '400'], fontsize=9)
ax.set_rlabel_position(0)

# Remove grid for clarity
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

# Title
plt.title('Weekly Mortality at Scutari Hospital, April 1854 - March 1856\n' +
          'Wedge area proportional to preventable deaths\n' +
          '(Weekly-resolution reconstruction from published Nightingale aggregates)',
          fontsize=14, fontweight='bold', pad=20)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=colors['preventable'], label='Preventable (disease)', alpha=0.8),
    mpatches.Patch(facecolor=colors['wounds'], label='Wounds/injuries', alpha=0.8),
    mpatches.Patch(facecolor=colors['other'], label='Other causes', alpha=0.8),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11, framealpha=0.95)

plt.tight_layout()
plt.savefig('coxcomb_weekly.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: coxcomb_weekly.png")
plt.close()

# ============================================================================
# Create a comparison: annual aggregates
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Annual data from Nightingale's 1858 report
annual_data = [
    {'year': 1854, 'weeks': 39, 'preventable': 5080, 'wounds': 732, 'other': 514},
    {'year': 1855, 'weeks': 52, 'preventable': 2761, 'wounds': 2618, 'other': 1369},
    {'year': 1856, 'weeks': 13, 'preventable': 594, 'wounds': 267, 'other': 142},
]

degrees_per_year = 360.0 / 3
theta_start = 0

for annual in annual_data:
    theta_start_rad = np.radians(theta_start)
    theta_end_rad = np.radians(theta_start + degrees_per_year)

    # Annual totals as radius
    r_preventable = annual['preventable']
    r_wounds = annual['wounds']
    r_other = annual['other']

    # Wedges
    wedge1 = Wedge((0, 0), r_preventable, theta_start, theta_start + degrees_per_year,
                   facecolor=colors['preventable'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(wedge1)

    wedge2 = Wedge((0, 0), r_wounds, theta_start, theta_start + degrees_per_year,
                   facecolor=colors['wounds'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(wedge2)

    wedge3 = Wedge((0, 0), r_other, theta_start, theta_start + degrees_per_year,
                   facecolor=colors['other'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(wedge3)

    # Label year in center of wedge
    theta_mid = np.radians(theta_start + degrees_per_year / 2)
    r_mid = annual['preventable'] / 2
    ax.text(theta_mid, r_mid, str(annual['year']), fontsize=12, fontweight='bold',
            ha='center', va='center', color='white')

    theta_start += degrees_per_year

# Set limits
max_annual = max(a['preventable'] for a in annual_data) * 1.15
ax.set_ylim(0, max_annual)

# Labels
ax.set_xticks([np.radians(a) for a in [60, 180, 300]])
ax.set_xticklabels(['1854\n(Apr-Dec)', '1855\n(Full year)', '1856\n(Jan-Mar)'], fontsize=11)

ax.set_yticks([1000, 2000, 3000, 4000, 5000])
ax.set_yticklabels(['1000', '2000', '3000', '4000', '5000'], fontsize=9)
ax.set_rlabel_position(0)

ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

plt.title("Nightingale's 1858 Report: Annual Mortality\n(Original rendering)",
          fontsize=14, fontweight='bold', pad=20)

legend_elements = [
    mpatches.Patch(facecolor=colors['preventable'], label='Preventable (disease)', alpha=0.8),
    mpatches.Patch(facecolor=colors['wounds'], label='Wounds/injuries', alpha=0.8),
    mpatches.Patch(facecolor=colors['other'], label='Other causes', alpha=0.8),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11, framealpha=0.95)

plt.tight_layout()
plt.savefig('coxcomb_annual.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: coxcomb_annual.png")
plt.close()

print("\nCoxcomb visualizations complete.")
