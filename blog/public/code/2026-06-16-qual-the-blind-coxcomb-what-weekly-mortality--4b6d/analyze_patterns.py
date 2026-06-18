import pandas as pd
import numpy as np

df = pd.read_csv('weekly_mortality_data.csv')

# Convert dates to datetime
df['week_start'] = pd.to_datetime(df['week_start'])

# Identify intervention period (week 46, March 1855)
pre_intervention = df[df['week_number'] < 46]
post_intervention = df[df['week_number'] >= 46]

print("PRE-INTERVENTION PERIOD (Apr 1854 - Feb 1855, weeks 1-45)")
print(f"  Mean preventable deaths/week: {pre_intervention['preventable_deaths'].mean():.1f}")
print(f"  Median preventable deaths/week: {pre_intervention['preventable_deaths'].median():.1f}")
print(f"  Std dev: {pre_intervention['preventable_deaths'].std():.1f}")
print(f"  Total preventable deaths: {pre_intervention['preventable_deaths'].sum()}")

print("\nPOST-INTERVENTION PERIOD (Mar 1855 - Mar 1856, weeks 46-156)")
print(f"  Mean preventable deaths/week: {post_intervention['preventable_deaths'].mean():.1f}")
print(f"  Median preventable deaths/week: {post_intervention['preventable_deaths'].median():.1f}")
print(f"  Std dev: {post_intervention['preventable_deaths'].std():.1f}")
print(f"  Total preventable deaths: {post_intervention['preventable_deaths'].sum()}")

# Calculate the change
pct_change = ((post_intervention['preventable_deaths'].mean() - 
               pre_intervention['preventable_deaths'].mean()) / 
              pre_intervention['preventable_deaths'].mean() * 100)

print(f"\nChange in weekly preventable deaths: {pct_change:.1f}%")

# Rolling average to see trend
df['rolling_prev_deaths'] = df['preventable_deaths'].rolling(window=4, center=True).mean()

# Find minimum death week post-intervention
min_week = post_intervention.loc[post_intervention['preventable_deaths'].idxmin()]
max_week_pre = pre_intervention.loc[pre_intervention['preventable_deaths'].idxmax()]

print(f"\nLowest preventable death week: Week {int(min_week['week_number'])}, {int(min_week['preventable_deaths'])} deaths")
print(f"Highest preventable death week (pre-intervention): Week {int(max_week_pre['week_number'])}, {int(max_week_pre['preventable_deaths'])} deaths")

# What fraction of annual deaths occur in each year?
deaths_1854 = df[df['week_number'] <= 39]['preventable_deaths'].sum()
deaths_1855 = df[(df['week_number'] > 39) & (df['week_number'] <= 91)]['preventable_deaths'].sum()
deaths_1856 = df[df['week_number'] > 91]['preventable_deaths'].sum()

print(f"\nPreventable deaths by year:")
print(f"  1854 (39 weeks): {int(deaths_1854)}")
print(f"  1855 (52 weeks): {int(deaths_1855)}")
print(f"  1856 (13 weeks): {int(deaths_1856)}")

print("\nSeasonal pattern (by quarter):")
quarters = [
    ("Apr-Jun 1854", 1, 13),
    ("Jul-Sep 1854", 14, 26),
    ("Oct-Dec 1854", 27, 39),
    ("Jan-Mar 1855", 40, 52),
    ("Apr-Jun 1855", 53, 65),
    ("Jul-Sep 1855", 66, 78),
    ("Oct-Dec 1855", 79, 91),
    ("Jan-Mar 1856", 92, 104),
]

for label, start, end in quarters:
    quarter_data = df[(df['week_number'] >= start) & (df['week_number'] <= end)]
    print(f"  {label}: {int(quarter_data['preventable_deaths'].sum())} deaths")
