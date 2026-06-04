"""Merge Stoddard egg-shape data with AVONET body mass and hand-wing index.

Inputs:
  data/eggs.RData              - 1,400 species, asymmetry, ellipticity, ave.length.com
  data/avonet/data/traitdata.rda - 11,009 species, Mass, Hand.Wing.Index, Family, Order

Outputs:
  data/merged.csv              - merged species-level table
"""
import pyreadr
import pandas as pd
import numpy as np
import re
import os

os.makedirs("data", exist_ok=True)

eggs = pyreadr.read_r("data/eggs.RData")["eggs"]
avo  = pyreadr.read_r("data/avonet/data/traitdata.rda")["traitdata"]

eggs = eggs.rename(columns={"spp": "species", "ave.length.com": "egg_length_cm"})
eggs["species"] = eggs["species"].astype(str).str.strip()
eggs["order"] = eggs["order"].astype(str).str.upper()
eggs["family"] = eggs["family"].astype(str)

avo_keep = avo[["Species1", "Family1", "Order1", "Mass", "Hand.Wing.Index",
                "Wing.Length", "Kipps.Distance", "Tail.Length",
                "Tarsus.Length", "Beak.Length_Culmen", "Migration",
                "Primary.Lifestyle"]].copy()
avo_keep["Species1"] = avo_keep["Species1"].astype(str).str.strip()

# Try direct name merge
merged = eggs.merge(avo_keep, left_on="species", right_on="Species1", how="left", indicator=True)
n_matched = (merged["_merge"] == "both").sum()
n_eggs = len(eggs)
print(f"Direct-name merge: {n_matched}/{n_eggs} species matched")

unmatched = [s for s in merged.loc[merged["_merge"] == "left_only", "species"].tolist()
             if isinstance(s, str) and s.strip() and s != 'nan']
print(f"Unmatched count: {len(unmatched)}")
if unmatched:
    print("First 12 unmatched:", unmatched[:12])

# Common avian taxonomic discrepancies: genus splits, lump/split.
# Build a {first_two_words} index for AVONET to attempt fuzzy match on bare binomial.
avo_bin = {}
for _, row in avo_keep.iterrows():
    s = row["Species1"]
    parts = s.split()
    if len(parts) >= 2:
        key = parts[0] + " " + parts[1]
        avo_bin[key] = row

n_recovered = 0
fuzzy_rows = []
for sp in unmatched:
    parts = sp.split()
    if len(parts) >= 2:
        key = parts[0] + " " + parts[1]
        if key in avo_bin:
            n_recovered += 1
            r = avo_bin[key]
            fuzzy_rows.append((sp, dict(r)))
print(f"Recovered by binomial: {n_recovered}")

# Note this gives no new info since the merge is already by exact full-name.
# Try lowercasing
avo_keep["sp_lc"] = avo_keep["Species1"].str.lower()
eggs["sp_lc"] = eggs["species"].str.lower()
merged2 = eggs.merge(avo_keep, on="sp_lc", how="left", indicator=True, suffixes=("", "_avo"))
n_matched2 = (merged2["_merge"] == "both").sum()
print(f"Lowercase merge: {n_matched2}/{n_eggs} species matched")

# Save merged with lowercase-match (since case may differ).
merged2 = merged2.drop(columns=["sp_lc"])
merged2.to_csv("data/merged.csv", index=False)
print(f"Saved data/merged.csv: {merged2.shape}")

# Profile data completeness on Mass and HWI:
ok = merged2.dropna(subset=["Mass", "Hand.Wing.Index"]).copy()
print(f"Rows with complete Mass + HWI: {len(ok)}")
print(f"Number of orders represented: {ok['order'].nunique()}")
print(f"Number of families: {ok['family'].nunique()}")
print(ok[["asymmetry","ellipticity","Mass","Hand.Wing.Index"]].describe().to_string())
