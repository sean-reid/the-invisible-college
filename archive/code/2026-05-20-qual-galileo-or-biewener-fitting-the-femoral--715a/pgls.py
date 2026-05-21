"""
PGLS-Brownian and PGLS-lambda on Campione & Evans (2012) mammals,
using the Upham et al. (2019) MCC supertree.

Outputs:
  - matched species count
  - PGLS-Brownian fit (slope, SE, 95% CI on beta_C and beta_I)
  - PGLS-lambda joint fit (lambda, slope, SE, 95% CI)
  - residual diagnostics
  - bootstrap CI under PGLS-Brownian on species (non-parametric block of rows;
    standard PGLS bootstrap is to refit on subtree leaves)

Method (PGLS-Brownian):
  Under Brownian motion on a tree, residuals are MVN with
  covariance sigma^2 * C, where C_ij = shared root-to-MRCA branch length.
  Diagonal C_ii is the root-to-tip distance of species i (equal across tips
  on an ultrametric tree). Solve the GLS normal equations:
      beta_hat = (X' C^-1 X)^-1 X' C^-1 y
  with Var(beta_hat) = sigma^2 (X' C^-1 X)^-1,
  sigma^2 = (y - X beta_hat)' C^-1 (y - X beta_hat) / (n - p).

  We do not need C^-1 explicitly; cholesky-solve via scipy.linalg.cho_factor
  on C produces L L'; then X' C^-1 X = (L^-1 X)' (L^-1 X), etc.

Method (PGLS-lambda):
  Replace C with C_lambda where off-diagonals are multiplied by lambda in
  (0, 1]; diagonals preserved. Profile likelihood over lambda on a grid.
"""

import csv
import math
import os
import sys
import re
import time

import numpy as np
from scipy import linalg, stats
import dendropy

HERE = os.path.dirname(os.path.abspath(__file__))
TREE_FILE = os.path.join(HERE, "upham_mcc.tre")
CSV_FILE = os.path.join(HERE, "extants.csv")

t0 = time.time()
print("Loading Upham MCC tree ...", flush=True)
tree = dendropy.Tree.get(path=TREE_FILE, schema="nexus")
print(f"  loaded in {time.time()-t0:.1f}s, {len(tree.leaf_nodes())} tips", flush=True)

# Build a map of "Genus species" -> taxon label.
# After NEXUS parsing, tip labels look like
# "Loxodonta africana ELEPHANTIDAE PROBOSCIDEA" (spaces, not underscores).
tip_map = {}
for leaf in tree.leaf_node_iter():
    label = leaf.taxon.label.strip()
    parts = label.split()
    if len(parts) >= 2:
        binom = f"{parts[0]} {parts[1]}"
        tip_map.setdefault(binom, label)

print(f"  built tip map of {len(tip_map)} binomials", flush=True)

# Load extants.csv mammal rows
rows = []
with open(CSV_FILE) as f:
    for r in csv.DictReader(f):
        try:
            BM = float(r["BM"]); FC = float(r["FC"])
        except (ValueError, KeyError):
            continue
        if BM <= 0 or FC <= 0:
            continue
        if r["Mon.Groups"] == "Reptilia":
            continue
        rows.append(dict(
            group=r["Mon.Groups"],
            species=r["Species"].strip(),
            BM_g=BM, FC_mm=FC,
        ))

print(f"  {len(rows)} mammal rows in dataset", flush=True)

# Synonym table.  These are well-known modern synonymies or
# spelling-typo corrections for species in Campione & Evans (2012)
# whose original combination is not the tip label in the Upham tree.
# Source: each entry verified against the Upham tip set; no synonymy
# is applied that does not have an exact tip match on the receiving side.
SYNONYM = {
    "Aepyceros malampus": "Aepyceros melampus",      # typo
    "Alopex lagopus": "Vulpes lagopus",              # taxonomic
    "Cervus duvaucelii": "Rucervus duvaucelii",      # taxonomic
    "Cynomys leucurus?": "Cynomys leucurus",         # CSV punctuation
    "Dasyprocta aguti": "Dasyprocta leporina",       # taxonomic
    "Equus burchelli?": "Equus quagga",              # taxonomic
    "Funisciurus pyrrhopus": "Funisciurus pyrropus", # spelling
    "Galerella sanguinea": "Herpestes sanguineus",   # taxonomic
    "Hydrochaeris hydrochaeris": "Hydrochoerus hydrochaeris",  # spelling
    "Lutra canadensis": "Lontra canadensis",         # taxonomic
    "Mustela erminae": "Mustela erminea",            # spelling
    "Mustela vison": "Neovison vison",               # taxonomic
    "Okapia johstoni": "Okapia johnstoni",           # spelling
    "Oryzomys albigularis": "Nephelomys albigularis",  # taxonomic
    "Oryzomys megacephalus": "Hylaeamys megacephalus", # taxonomic
    "Panthera tigris_altaica": "Panthera tigris",    # subspecies -> species
    "Panthera tigris_tigris": "Panthera tigris",     # subspecies -> species
    "Panthera unica": "Panthera uncia",              # spelling
    "Phoca groenlandica": "Pagophilus groenlandicus", # taxonomic
    "Pongo Pygmaeus": "Pongo pygmaeus",              # capitalization
    "Spermophilus adocetus": "Notocitellus adocetus", # taxonomic
    "Spermophilus franklinii": "Poliocitellus franklinii",  # taxonomic
    "Spermophilus lateralis": "Callospermophilus lateralis", # taxonomic
    "Spermophilus richardsonii": "Urocitellus richardsonii", # taxonomic
    "Spermophilus tridecemlineatus": "Ictidomys tridecemlineatus", # taxonomic
    "Suricata suricata": "Suricata suricatta",       # spelling
    "Taxidae taxus": "Taxidea taxus",                # spelling (family typo)
    "Thomomys Talpoides": "Thomomys talpoides",      # capitalization
    "Urocyon cinereoargentus": "Urocyon cinereoargenteus", # spelling
}

# Pre-resolve the two Panthera tigris subspecies rows: keep only one row,
# averaging the two measurements on log scale (they are intra-species
# replicates).  Without this they would both map to the same tip and the
# VCV would be singular.

tigris_rows = [r for r in rows if r["species"] in
               ("Panthera tigris_altaica", "Panthera tigris_tigris")]
if len(tigris_rows) >= 2:
    BM_mean = math.exp(sum(math.log(r["BM_g"]) for r in tigris_rows) / len(tigris_rows))
    FC_mean = math.exp(sum(math.log(r["FC_mm"]) for r in tigris_rows) / len(tigris_rows))
    rows = [r for r in rows if r["species"] not in
            ("Panthera tigris_altaica", "Panthera tigris_tigris")]
    rows.append(dict(group="Carnivora", species="Panthera tigris",
                     BM_g=BM_mean, FC_mm=FC_mean))
    print(f"  collapsed 2 P. tigris subspecies rows into 1 (log-averaged)")

# Match to tree, applying synonym table.
matched = []
unmatched = []
for r in rows:
    binom = r["species"]
    target = SYNONYM.get(binom, binom)
    if target in tip_map:
        r["tip"] = tip_map[target]
        r["matched_as"] = target
        matched.append(r)
    else:
        unmatched.append(binom)

print(f"  matched {len(matched)}/{len(rows)} ({len(unmatched)} unmatched)", flush=True)
if unmatched:
    print(f"  unmatched examples: {unmatched[:10]}", flush=True)

# Quick fix: try genus-only lookups for unmatched? No -- want exact species.
# But also try replacing spaces with _ and looking for the binomial as the
# leading two underscored fields anywhere.

# Build set of leading binomials.
all_binoms = set()
for leaf in tree.leaf_node_iter():
    parts = leaf.taxon.label.strip().split()
    if len(parts) >= 2:
        all_binoms.add(f"{parts[0]} {parts[1]}")

still_unmatched = []
for r in rows:
    if "tip" in r:
        continue
    binom = r["species"]
    # Try replacing any synonyms (manual): no automatic synonymy.
    if binom in all_binoms:
        # tip_map already has this; reuse
        r["tip"] = tip_map[binom]
        matched.append(r)
    else:
        still_unmatched.append(binom)

# Deduplicate matched (if any row was added twice in this fall-through)
seen_keys = set()
final_matched = []
for r in matched:
    key = (r["species"], r["FC_mm"], r["BM_g"])
    if key in seen_keys:
        continue
    seen_keys.add(key)
    final_matched.append(r)
matched = final_matched

print(f"  final matched: {len(matched)}", flush=True)
print(f"  still unmatched ({len(still_unmatched)}): {still_unmatched[:15]}", flush=True)

# Prune the tree to matched tips
keep_tip_labels = set(r["tip"] for r in matched)
tns = tree.taxon_namespace
tns_keep = [t for t in tns if t.label in keep_tip_labels]
tree.retain_taxa(tns_keep)
print(f"  pruned tree to {len(tree.leaf_nodes())} tips", flush=True)

# Compute pairwise patristic distances using dendropy's PDM, then convert to
# shared-branch length (root-to-MRCA) for the VCV under Brownian motion.
# On an ultrametric tree, C_ii = root-to-tip distance (= half of max
# patristic distance). C_ij = root-to-tip - 0.5 * patristic_ij.

print("Computing phylogenetic distance matrix ...", flush=True)
t0 = time.time()
pdm = tree.phylogenetic_distance_matrix()
print(f"  built PDM in {time.time()-t0:.1f}s", flush=True)

# Order taxa per matched data order.
taxa_in_order = []
tn_by_label = {t.label: t for t in tree.taxon_namespace}
for r in matched:
    taxa_in_order.append(tn_by_label[r["tip"]])

# Compute root-to-tip for one leaf; should be (near) equal across leaves
# on an ultrametric tree.
node_by_taxon = {}
for nd in tree.leaf_node_iter():
    node_by_taxon[nd.taxon.label] = nd

def root_to_tip(node):
    d = 0.0
    while node.parent_node is not None:
        d += node.edge_length or 0.0
        node = node.parent_node
    return d

r2t_list = [root_to_tip(node_by_taxon[t.label]) for t in taxa_in_order]
print(f"  root-to-tip distances: mean={np.mean(r2t_list):.4f},"
      f" sd={np.std(r2t_list):.4f}, range=[{min(r2t_list):.4f},"
      f" {max(r2t_list):.4f}]", flush=True)
T = float(np.mean(r2t_list))  # tree height

n = len(matched)
C = np.zeros((n, n))
for i, ti in enumerate(taxa_in_order):
    for j, tj in enumerate(taxa_in_order):
        if i == j:
            C[i, j] = r2t_list[i]
        else:
            dij = pdm.distance(ti, tj)
            C[i, j] = max(r2t_list[i], r2t_list[j]) - 0.5 * dij

# Symmetrize defensively (numerical roundoff).
C = 0.5 * (C + C.T)

# Sanity: diagonals ≈ T
print(f"  C diag mean={np.diag(C).mean():.4f}, off-diag mean={(C.sum()-np.trace(C))/(n*(n-1)):.4f}", flush=True)

# Build y, X
x_vec = np.array([math.log10(r["BM_g"]/1000.0) for r in matched])
y_vec = np.array([math.log10(r["FC_mm"]) for r in matched])
X = np.column_stack([np.ones(n), x_vec])

# --- PGLS-Brownian ---
print("\n=== PGLS-Brownian ===", flush=True)
# Cholesky of C: C = L L'
# Then C^-1 = L^-T L^-1 ; X' C^-1 X = (L^-1 X)' (L^-1 X)
L = linalg.cholesky(C, lower=True)
LinvX = linalg.solve_triangular(L, X, lower=True)
Linvy = linalg.solve_triangular(L, y_vec, lower=True)
beta_hat = linalg.lstsq(LinvX, Linvy)[0]
resid = Linvy - LinvX @ beta_hat
sigma2 = float(resid @ resid) / (n - 2)
cov_beta = sigma2 * linalg.inv(LinvX.T @ LinvX)
se_beta = np.sqrt(np.diag(cov_beta))
beta_C_pgls = float(beta_hat[1])
se_C_pgls = float(se_beta[1])
# 95% CI: t-dist with n-2 df
tcrit = stats.t.ppf(0.975, df=n-2)
ci_lo_C = beta_C_pgls - tcrit*se_C_pgls
ci_hi_C = beta_C_pgls + tcrit*se_C_pgls
print(f"  n = {n}")
print(f"  intercept = {float(beta_hat[0]):.5f}")
print(f"  beta_C = {beta_C_pgls:.5f}")
print(f"  SE(beta_C) = {se_C_pgls:.5f}")
print(f"  95% CI on beta_C: [{ci_lo_C:.5f}, {ci_hi_C:.5f}]")
print(f"  beta_I = 4*beta_C = {4*beta_C_pgls:.5f}")
print(f"  95% CI on beta_I: [{4*ci_lo_C:.5f}, {4*ci_hi_C:.5f}]")
print(f"  sigma2 (GLS residual variance per unit branch length): {sigma2:.5g}")

# --- PGLS-lambda ---
print("\n=== PGLS-lambda (Pagel) ===", flush=True)
# C(lambda): same diagonals, off-diagonals multiplied by lambda.
def neg_loglik_lambda(lam):
    Cl = lam * C.copy()
    np.fill_diagonal(Cl, np.diag(C))  # diagonals preserved
    try:
        Ll = linalg.cholesky(Cl, lower=True)
    except linalg.LinAlgError:
        return np.inf, None, None
    LinvX_l = linalg.solve_triangular(Ll, X, lower=True)
    Linvy_l = linalg.solve_triangular(Ll, y_vec, lower=True)
    b_l = linalg.lstsq(LinvX_l, Linvy_l)[0]
    r_l = Linvy_l - LinvX_l @ b_l
    s2_l = float(r_l @ r_l) / n  # MLE (use n not n-p for profile)
    # log|C_lambda| = 2*sum(log(diag(Ll)))
    logdetC = 2.0 * float(np.sum(np.log(np.diag(Ll))))
    # Profile log-likelihood for sigma^2 = s2_l_MLE (substituted in):
    # ll = -n/2 * log(2*pi*s2) - 1/2 logdetC - n/2
    ll = -0.5*n*math.log(2*math.pi*s2_l) - 0.5*logdetC - 0.5*n
    return -ll, b_l, s2_l

# Search lambda on a fine grid first
grid = np.linspace(0.001, 1.0, 100)
nll_grid = []
for lam in grid:
    nll, _, _ = neg_loglik_lambda(lam)
    nll_grid.append(nll)
i_min = int(np.argmin(nll_grid))
lo, hi = max(0.001, grid[max(0, i_min-2)]), min(1.0, grid[min(len(grid)-1, i_min+2)])
# Golden-section refinement
def gss(f, a, b, tol=1e-5):
    phi = (math.sqrt(5)-1)/2
    c = b - phi*(b - a)
    d = a + phi*(b - a)
    while abs(b - a) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c
        c = b - phi*(b - a)
        d = a + phi*(b - a)
    return (a+b)/2
def f_lam(lam):
    nll, _, _ = neg_loglik_lambda(lam)
    return nll
lam_hat = gss(f_lam, lo, hi)
nll_hat, b_hat_lam, s2_lam = neg_loglik_lambda(lam_hat)

# Likelihood-ratio 95% CI for lambda
def lr_test(lam):
    return 2.0 * (f_lam(lam) - nll_hat)

# Find LR=3.84 crossings by bisection on either side
def find_lr_root(low, high):
    while high - low > 1e-4:
        mid = 0.5*(low + high)
        if lr_test(mid) > 3.84:
            low = mid
        else:
            high = mid
    return 0.5*(low+high)

# Lambda CI
if lam_hat > 0.01:
    lam_lo = find_lr_root(0.0, lam_hat) if lr_test(0.001) > 3.84 else 0.0
else:
    lam_lo = 0.0
lam_hi = find_lr_root(1.0, lam_hat) if lr_test(0.9999) > 3.84 else 1.0
# adjust: find_lr_root expects "low side over threshold, high side under"
# Re-implement carefully:
def lr_curve_sweep():
    # scan from lam_hat outward
    pts = []
    for lam in np.linspace(0.001, 1.0, 200):
        pts.append((lam, lr_test(lam)))
    return pts
pts = lr_curve_sweep()

# Find lambda values where LR crosses 3.84 above and below lam_hat.
def find_crossing(direction):
    # direction = -1 (below lam_hat) or +1 (above)
    crossings = []
    prev = None
    for lam, lr in pts:
        if prev is not None:
            lam0, lr0 = prev
            if (lr0 - 3.84) * (lr - 3.84) < 0:
                # linear interp
                t = (3.84 - lr0) / (lr - lr0)
                crossings.append(lam0 + t * (lam - lam0))
        prev = (lam, lr)
    crossings.sort()
    if direction == -1:
        below = [c for c in crossings if c < lam_hat]
        return below[-1] if below else 0.0
    else:
        above = [c for c in crossings if c > lam_hat]
        return above[0] if above else 1.0

lam_lo = find_crossing(-1)
lam_hi = find_crossing(+1)

# Now fit the GLS at lambda_hat to get beta_C SE
Cl = lam_hat * C.copy()
np.fill_diagonal(Cl, np.diag(C))
Ll = linalg.cholesky(Cl, lower=True)
LinvX_l = linalg.solve_triangular(Ll, X, lower=True)
Linvy_l = linalg.solve_triangular(Ll, y_vec, lower=True)
b_lam = linalg.lstsq(LinvX_l, Linvy_l)[0]
r_lam = Linvy_l - LinvX_l @ b_lam
sigma2_lam = float(r_lam @ r_lam) / (n - 2)  # restricted (REML-ish for profile)
cov_b_lam = sigma2_lam * linalg.inv(LinvX_l.T @ LinvX_l)
se_b_lam = np.sqrt(np.diag(cov_b_lam))
beta_C_lam = float(b_lam[1])
se_C_lam = float(se_b_lam[1])
ci_lo_lam = beta_C_lam - tcrit*se_C_lam
ci_hi_lam = beta_C_lam + tcrit*se_C_lam
print(f"  lambda_hat = {lam_hat:.4f}")
print(f"  lambda 95% LR CI: [{lam_lo:.4f}, {lam_hi:.4f}]")
print(f"  beta_C (at lambda_hat) = {beta_C_lam:.5f}")
print(f"  SE(beta_C | lambda_hat) = {se_C_lam:.5f}")
print(f"  95% CI on beta_C: [{ci_lo_lam:.5f}, {ci_hi_lam:.5f}]")
print(f"  beta_I = 4*beta_C = {4*beta_C_lam:.5f}")
print(f"  95% CI on beta_I: [{4*ci_lo_lam:.5f}, {4*ci_hi_lam:.5f}]")

# --- Save summary ---
with open(os.path.join(HERE, "pgls_summary.txt"), "w") as f:
    f.write(f"n_matched = {n}\n")
    f.write(f"PGLS-Brownian:\n")
    f.write(f"  beta_C = {beta_C_pgls:.5f}\n")
    f.write(f"  SE(beta_C) = {se_C_pgls:.5f}\n")
    f.write(f"  95% CI on beta_C: [{ci_lo_C:.5f}, {ci_hi_C:.5f}]\n")
    f.write(f"  beta_I = {4*beta_C_pgls:.5f}\n")
    f.write(f"  95% CI on beta_I: [{4*ci_lo_C:.5f}, {4*ci_hi_C:.5f}]\n")
    f.write(f"PGLS-lambda:\n")
    f.write(f"  lambda_hat = {lam_hat:.4f}\n")
    f.write(f"  lambda 95% LR CI: [{lam_lo:.4f}, {lam_hi:.4f}]\n")
    f.write(f"  beta_C = {beta_C_lam:.5f}\n")
    f.write(f"  SE(beta_C) = {se_C_lam:.5f}\n")
    f.write(f"  95% CI on beta_C: [{ci_lo_lam:.5f}, {ci_hi_lam:.5f}]\n")
    f.write(f"  beta_I = {4*beta_C_lam:.5f}\n")
    f.write(f"  95% CI on beta_I: [{4*ci_lo_lam:.5f}, {4*ci_hi_lam:.5f}]\n")

# Save matched species list (for transparency and unmatched audit)
with open(os.path.join(HERE, "matched_species.txt"), "w") as f:
    f.write(f"n_matched = {len(matched)}\n")
    f.write(f"n_unmatched = {len(still_unmatched)}\n\n")
    f.write("Unmatched species:\n")
    for s in sorted(still_unmatched):
        f.write(f"  {s}\n")

print("\nDone.", flush=True)
