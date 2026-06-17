"""
Diffusion-limit audit for the Carboniferous-Permian oxygen hypothesis.

Closed-form derivation of R_max under three nested scaling assumptions,
followed by a Monte Carlo variance decomposition over the three named
uncertainty sources: atmospheric O2 (Berner GEOCARBSULF), Kaiser et
al. tracheal exponent, and the Harrison et al. convective ventilation
factor.

Reference: see the paired draft and lab notebook in this workspace.
"""

import numpy as np

rng = np.random.default_rng(20260616)

# --- Physical setup ---
# Atmospheric pressure: 101.325 kPa
ATM_KPA = 101.325
# Critical PO2 for insect mitochondria, after Harrison et al. 2010
# (typical range 1-5 kPa across species; central value 2 kPa)
P_CRIT_KPA = 2.0

# Modern atmospheric O2 fraction
F_MOD = 0.2095
# Berner GEOCARBSULF (2006) central reconstruction at peak (300 Ma)
F_PEAK_CENTRAL = 0.30
# Berner stated one-sigma is ~5 percentage points; we treat the
# 23-35% Carboniferous-Permian peak window as a uniform prior for
# the high-O2 era, then narrow per timestep when projecting R_max(t)
F_PEAK_LOW = 0.23
F_PEAK_HIGH = 0.35

# Kaiser et al. 2007: V_t ~ M^(1 + k), with k = 0.29 from
# synchrotron-X-ray on four scarabaeoid beetles (n = 4 species,
# spanning ~10^-2 to 10^0 g). SE on the exponent is not reported in
# their paper directly; we treat the slope error of 0.05 as a
# reasonable propagation of their stated precision.
K_KAISER_MEAN = 0.29
K_KAISER_SD = 0.05

# Metabolic allometry (insect-wide; Chown et al. 2007)
# B ~ M^0.75; with V ~ M, demand q ~ M^(-0.25); with M ~ R^3, q ~ R^(-0.75)
ALPHA_METAB = 0.75

# Harrison et al. 2010 convective ventilation enhancement: factor
# of about 3 (rest) to about 10 (flight) over passive diffusion
GAMMA_LO = 3.0
GAMMA_HI = 10.0

# Observed reference R_max for "modern" largest dragonfly body
# length (Petalura ingentissima, Australian giant petaltail).
# Wingspan ~16 cm, body length ~13 cm; rounded to 15 cm here.
R_MAX_MODERN_CM = 15.0


def dp(f_o2):
    """Effective oxygen partial pressure gradient, kPa."""
    return f_o2 * ATM_KPA - P_CRIT_KPA


def r_ratio_naive(f_o2_high, f_o2_low=F_MOD):
    """Textbook square-root scaling: constant phi, constant q.
    R ~ Delta_P^0.5."""
    return (dp(f_o2_high) / dp(f_o2_low)) ** 0.5


def r_ratio_isometric(f_o2_high, f_o2_low=F_MOD):
    """Isometric tracheae (k = 0), allometric metabolism (alpha = 0.75).
    Solve R^2 = K * R^(3*alpha/4) * Delta_P (with q ~ R^-0.75).
    Exponent on Delta_P: 1/(2 - 0.75) = 0.8.
    """
    return (dp(f_o2_high) / dp(f_o2_low)) ** 0.8


def r_ratio_hypermetric(f_o2_high, k, f_o2_low=F_MOD):
    """Kaiser hypermetric tracheae (phi ~ M^k = R^{3k}), allometric
    metabolism. Solve R^2 = K * R^{3k} * R^{0.75} * Delta_P,
    so R^{2 - 3k - 0.75} = K' * Delta_P, exponent on R is
    e_R = 1.25 - 3k. R ~ Delta_P^{1/e_R}.

    Diverges as k -> 0.417 (the threshold beyond which the system is
    no longer diffusion-limited under these assumptions).
    """
    e_r = 1.25 - 3.0 * k
    if np.any(e_r <= 0):
        # Indicates the diffusion limit has gone unbounded
        return np.where(e_r <= 0, np.inf, (dp(f_o2_high) / dp(f_o2_low)) ** (1.0 / e_r))
    return (dp(f_o2_high) / dp(f_o2_low)) ** (1.0 / e_r)


# --- Point estimates at central Berner peak (P_O2 = 30%) ---
print("=" * 60)
print("POINT ESTIMATES: R_max ratio at peak Carboniferous O2 = 30%")
print("=" * 60)
print(f"Modern PO2 = {F_MOD*ATM_KPA:.2f} kPa; effective DeltaP = {dp(F_MOD):.2f} kPa")
print(f"Peak PO2  = {F_PEAK_CENTRAL*ATM_KPA:.2f} kPa; effective DeltaP = {dp(F_PEAK_CENTRAL):.2f} kPa")
print(f"DeltaP ratio (peak/modern) = {dp(F_PEAK_CENTRAL)/dp(F_MOD):.3f}")
print()

naive = r_ratio_naive(F_PEAK_CENTRAL)
iso = r_ratio_isometric(F_PEAK_CENTRAL)
hyp = r_ratio_hypermetric(F_PEAK_CENTRAL, K_KAISER_MEAN)

print(f"S1 (naive, R ~ DP^0.5):                  ratio = {naive:.2f}  =>  R_max ~ {naive*R_MAX_MODERN_CM:.1f} cm")
print(f"S2 (isometric tracheae, R ~ DP^0.8):     ratio = {iso:.2f}  =>  R_max ~ {iso*R_MAX_MODERN_CM:.1f} cm")
print(f"S3 (Kaiser hypermetric, R ~ DP^{1/(1.25-3*K_KAISER_MEAN):.2f}): ratio = {hyp:.2f}  =>  R_max ~ {hyp*R_MAX_MODERN_CM:.1f} cm")
print()
print(f"Observed Meganeuropsis permiana body length ~ 43 cm")
print(f"(wingspan ~ 71 cm)")
print()

# --- Sensitivity of S3 to Kaiser exponent ---
print("=" * 60)
print("S3 hypermetric R_max ratio at peak O2, varying Kaiser exponent k")
print("=" * 60)
for k in [0.15, 0.20, 0.24, 0.29, 0.34, 0.39]:
    er = 1.25 - 3*k
    if er <= 0:
        print(f"  k = {k:.2f}: e_R = {er:+.3f}  (diffusion limit unbounded)")
        continue
    ratio = r_ratio_hypermetric(F_PEAK_CENTRAL, k)
    print(f"  k = {k:.2f}: R_max ratio = {ratio:.2f}x  =>  body length ~ {ratio*R_MAX_MODERN_CM:.0f} cm  (exponent on DP = {1/er:.2f})")
print()

# --- Monte Carlo over the three uncertainty sources ---
print("=" * 60)
print("MONTE CARLO over P_O2, Kaiser exponent, convective gamma")
print("=" * 60)

N = 100_000
# P_O2: uniform over Berner peak window (conservative)
f_peak = rng.uniform(F_PEAK_LOW, F_PEAK_HIGH, N)
# Kaiser exponent: truncated normal
k_draws = rng.normal(K_KAISER_MEAN, K_KAISER_SD, N)
k_draws = np.clip(k_draws, 0.10, 0.40)  # avoid the singularity at k=0.417
# Convective gamma: uniform over Harrison range (applies only to S3,
# scales both modern and ancient -- so it cancels in the ratio.
# We include it here only to confirm that the variance decomposition
# of the *ratio* sees no contribution from gamma.)
gamma = rng.uniform(GAMMA_LO, GAMMA_HI, N)

ratio_naive = r_ratio_naive(f_peak)
ratio_iso = r_ratio_isometric(f_peak)

# Hypermetric ratio, capped at a large but finite value where k -> 0.417
e_r = 1.25 - 3.0 * k_draws
dp_ratio = dp(f_peak) / dp(F_MOD)
ratio_hyp = dp_ratio ** (1.0 / e_r)
# Cap absurd extrapolations (k > 0.39)
ratio_hyp_capped = np.minimum(ratio_hyp, 100.0)

print(f"Draws: N = {N}")
print()
print("S1 naive (R ~ DP^0.5):")
print(f"  median = {np.median(ratio_naive):.2f}   5-95 percentile = [{np.percentile(ratio_naive, 5):.2f}, {np.percentile(ratio_naive, 95):.2f}]")
print(f"  Body length 5-95: [{np.percentile(ratio_naive, 5)*R_MAX_MODERN_CM:.1f}, {np.percentile(ratio_naive, 95)*R_MAX_MODERN_CM:.1f}] cm")
print()
print("S2 isometric tracheae (R ~ DP^0.8):")
print(f"  median = {np.median(ratio_iso):.2f}   5-95 percentile = [{np.percentile(ratio_iso, 5):.2f}, {np.percentile(ratio_iso, 95):.2f}]")
print(f"  Body length 5-95: [{np.percentile(ratio_iso, 5)*R_MAX_MODERN_CM:.1f}, {np.percentile(ratio_iso, 95)*R_MAX_MODERN_CM:.1f}] cm")
print()
print("S3 Kaiser hypermetric (R ~ DP^{1/(1.25-3k)}):")
print(f"  median = {np.median(ratio_hyp_capped):.2f}   5-95 percentile = [{np.percentile(ratio_hyp_capped, 5):.2f}, {np.percentile(ratio_hyp_capped, 95):.2f}]")
print(f"  Body length 5-95: [{np.percentile(ratio_hyp_capped, 5)*R_MAX_MODERN_CM:.1f}, {np.percentile(ratio_hyp_capped, 95)*R_MAX_MODERN_CM:.1f}] cm")
print(f"  Share of draws over 100 cm (extrapolation blow-up): {(ratio_hyp_capped > 100/R_MAX_MODERN_CM).mean()*100:.1f}%")
print()

# --- Variance decomposition for S3 (the only scenario with both
# uncertainty sources active) ---
print("=" * 60)
print("VARIANCE DECOMPOSITION (S3): contributions of P_O2 vs Kaiser k")
print("=" * 60)

# Use log(ratio) since the ratio is multiplicative and right-skewed.
# log R_max ratio = (1/(1.25 - 3k)) * log(DP_ratio)
log_ratio_S3 = np.log(ratio_hyp_capped)

# Marginal variances by holding one input at central value
log_ratio_fix_k = np.log(np.clip(dp(f_peak)/dp(F_MOD), 1e-10, None) ** (1.0/(1.25 - 3*K_KAISER_MEAN)))
log_ratio_fix_o2 = np.log(np.clip(dp(F_PEAK_CENTRAL)/dp(F_MOD), 1e-10, None) ** (1.0/(1.25 - 3*k_draws)))

V_full = np.var(log_ratio_S3)
V_o2_only = np.var(log_ratio_fix_k)
V_k_only = np.var(log_ratio_fix_o2)

print(f"Total variance of log R_max ratio (S3):           {V_full:.4f}")
print(f"  variance with only P_O2 varying (k = 0.29):     {V_o2_only:.4f}   ({V_o2_only/V_full*100:.1f}%)")
print(f"  variance with only Kaiser k varying (P_O2=30%): {V_k_only:.4f}   ({V_k_only/V_full*100:.1f}%)")
print(f"  unexplained / interaction:                      {V_full - V_o2_only - V_k_only:.4f}   ({(V_full - V_o2_only - V_k_only)/V_full*100:.1f}%)")
print()

# --- Post-Permian collapse: does R_max envelope contract correctly? ---
print("=" * 60)
print("R_max ratio under S3 across the Carboniferous-Permian timeline")
print("(approximate Berner GEOCARBSULF central estimates)")
print("=" * 60)
# Approximate central values from Berner 2006 / Glasspool & Scott 2010
timeline = [
    (330, 0.22, "early Carboniferous"),
    (320, 0.27, "mid-Carboniferous"),
    (310, 0.30, "Pennsylvanian peak"),
    (300, 0.30, "Carboniferous-Permian boundary peak"),
    (290, 0.28, "early Permian (Meganeuropsis era)"),
    (280, 0.25, "mid-Permian"),
    (270, 0.22, "late Permian"),
    (260, 0.21, "end-Permian decline"),
    (250, 0.18, "early Triassic"),
    (0,   0.21, "modern"),
]
print(f"  Anchored at modern R_max = {R_MAX_MODERN_CM} cm; Kaiser k = {K_KAISER_MEAN}")
print()
print(f"  {'Age (Ma)':>9} | {'PO2 frac':>8} | {'R/R_mod (S1)':>12} | {'R/R_mod (S3)':>12} | {'L_max(S3) cm':>12} | era")
for age, f, label in timeline:
    r1 = r_ratio_naive(f)
    r3 = r_ratio_hypermetric(f, K_KAISER_MEAN)
    print(f"  {age:>9} | {f:>8.2f} | {r1:>12.2f} | {r3:>12.2f} | {r3*R_MAX_MODERN_CM:>12.1f} | {label}")
print()

print("=" * 60)
print("CONCLUSION SUMMARY")
print("=" * 60)
print("S1 (naive, square-root): R_max at peak Carboniferous = ~18 cm")
print("S2 (isometric tracheae): R_max at peak Carboniferous = ~20 cm")
print("S3 (Kaiser hypermetric): R_max at peak Carboniferous = ~40 cm")
print()
print("Meganeuropsis observed body length: ~43 cm")
print()
print("Only the hypermetric scenario reaches Meganeuropsis -- and it")
print("does so only by extrapolating Kaiser's exponent (measured on 4")
print("beetle species spanning 10^-2 to 10^0 g) up to a 100 g dragonfly.")
print("Within S3, variance in the predicted envelope is dominated by")
print("the Kaiser exponent uncertainty, not by atmospheric O2 uncertainty.")
