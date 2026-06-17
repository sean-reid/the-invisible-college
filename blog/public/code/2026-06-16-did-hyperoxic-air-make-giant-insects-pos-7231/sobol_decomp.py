"""
Saltelli-style first-order Sobol sensitivity for the S3 prediction.

Two inputs:
  X1 = atmospheric O2 fraction at peak (uniform 0.23 to 0.35)
  X2 = Kaiser hypermetric exponent k (truncated normal 0.29, 0.05)

Output:
  Y = log R_max ratio = log( DeltaP_ratio ) / (1.25 - 3k)

First-order indices S_i = V[E[Y|X_i]] / V[Y] estimated via pick-freeze.
"""

import numpy as np

rng = np.random.default_rng(20260616)

ATM_KPA = 101.325
P_CRIT_KPA = 2.0
F_MOD = 0.2095


def dp(f):
    return f * ATM_KPA - P_CRIT_KPA


def f_model(f_o2, k):
    e_r = 1.25 - 3.0 * k
    dp_ratio = dp(f_o2) / dp(F_MOD)
    return np.log(dp_ratio) / e_r  # log of R ratio


N = 200_000

# Sample matrices A and B (independent)
A_o2 = rng.uniform(0.23, 0.35, N)
A_k = np.clip(rng.normal(0.29, 0.05, N), 0.10, 0.40)
B_o2 = rng.uniform(0.23, 0.35, N)
B_k = np.clip(rng.normal(0.29, 0.05, N), 0.10, 0.40)

yA = f_model(A_o2, A_k)
yB = f_model(B_o2, B_k)

# C_i = A but with column i replaced by B's column
y_C_o2 = f_model(B_o2, A_k)  # k from A, O2 from B (this is "fixing k")
y_C_k = f_model(A_o2, B_k)   # O2 from A, k from B (this is "fixing O2")

# Saltelli 2010 formulae for first-order:
#   S_i = (1/N) sum [ yB * (yC_i - yA) ] / Var(y)
# (variance is estimated from yA)
varY = np.var(np.concatenate([yA, yB]))

# First-order Sobol for O2: uses yC_o2 = f(B_o2, A_k), i.e. "varying O2"
S_o2 = np.mean(yB * (y_C_o2 - yA)) / varY
# First-order Sobol for k: uses yC_k = f(A_o2, B_k), i.e. "varying k"
S_k = np.mean(yB * (y_C_k - yA)) / varY

# Total-effect indices (Jansen 1999):
#   ST_i = (1/(2N)) sum (yA - yC_i)^2 / Var(y)
ST_o2 = 0.5 * np.mean((yA - y_C_o2) ** 2) / varY
ST_k = 0.5 * np.mean((yA - y_C_k) ** 2) / varY

print("Saltelli pick-freeze, N = ", N)
print()
print(f"Total variance of log R_max ratio: {varY:.4f}")
print(f"  (median ratio = {np.exp(np.median(yA)):.2f}x)")
print()
print(f"First-order Sobol indices:")
print(f"  S_PO2 = {S_o2*100:.1f}%   (variance from atmospheric O2 reconstruction)")
print(f"  S_k   = {S_k*100:.1f}%   (variance from Kaiser hypermetric exponent)")
print(f"  sum S = {(S_o2 + S_k)*100:.1f}%")
print()
print(f"Total-effect Sobol indices:")
print(f"  ST_PO2 = {ST_o2*100:.1f}%")
print(f"  ST_k   = {ST_k*100:.1f}%")
print(f"  sum ST = {(ST_o2 + ST_k)*100:.1f}%   (>= 100% indicates interaction)")
print()
print(f"Interaction term: ST_total - S_first = {(ST_o2 + ST_k - S_o2 - S_k)*100:.1f}%")
