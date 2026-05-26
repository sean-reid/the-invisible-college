"""
Toy demonstration of the blind set of single-point LOO applied to OLS.

World-states differ in which cluster of a two-cluster design carries a fixed
contamination of size delta on a fixed number of observations.

Cluster-rotation symmetry of the design implies that, over data
resampling, the distribution of the LOO summary statistic
  T(data) = max_i |beta_hat_{-i} - beta_hat|
is identical between two states inside the rotation class. We verify by
simulation, and contrast with a state outside the class
(no contamination).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(20260526)

# Design: two clusters of equal size.
N_PER_CLUSTER = 50
N = 2 * N_PER_CLUSTER  # total 100 obs
X_A_CENTER = 0.0
X_B_CENTER = 10.0
X_NOISE = 1.0
BETA_TRUE = 1.0           # slope
INTERCEPT_TRUE = 0.0
SIGMA = 1.0               # residual sd

N_CONTAMINATED = 5        # observations contaminated within the chosen cluster
DELTA = 5.0               # contamination shift in Y
N_TRIALS = 4000


def simulate_one(world_state, rng):
    """
    world_state in {'A', 'B', 'clean'}
    Returns T = max_i |beta_hat_{-i} - beta_hat|.
    """
    xA = rng.normal(X_A_CENTER, X_NOISE, N_PER_CLUSTER)
    xB = rng.normal(X_B_CENTER, X_NOISE, N_PER_CLUSTER)
    x = np.concatenate([xA, xB])

    eps = rng.normal(0, SIGMA, N)
    y = INTERCEPT_TRUE + BETA_TRUE * x + eps

    # Apply contamination per world_state.
    if world_state == 'A':
        idx = rng.choice(N_PER_CLUSTER, N_CONTAMINATED, replace=False)
        y[idx] += DELTA
    elif world_state == 'B':
        idx = rng.choice(N_PER_CLUSTER, N_CONTAMINATED, replace=False) + N_PER_CLUSTER
        y[idx] += DELTA
    elif world_state == 'clean':
        pass
    else:
        raise ValueError(world_state)

    # Full-sample OLS.
    Xd = np.column_stack([np.ones(N), x])
    beta_full = np.linalg.lstsq(Xd, y, rcond=None)[0]

    # Single-point LOO.
    deltas = np.empty(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        beta_i = np.linalg.lstsq(Xd[mask], y[mask], rcond=None)[0]
        deltas[i] = beta_i[1] - beta_full[1]
    return float(np.max(np.abs(deltas)))


def run(world_state, n_trials, seed):
    sub_rng = np.random.default_rng(seed)
    return np.array([simulate_one(world_state, sub_rng) for _ in range(n_trials)])


T_A = run('A', N_TRIALS, seed=1)
T_B = run('B', N_TRIALS, seed=2)
T_clean = run('clean', N_TRIALS, seed=3)

print(f"N={N}, n_contaminated={N_CONTAMINATED}, delta={DELTA}, trials={N_TRIALS}")
print(f"T_A:       mean={T_A.mean():.5f}  median={np.median(T_A):.5f}  sd={T_A.std():.5f}")
print(f"T_B:       mean={T_B.mean():.5f}  median={np.median(T_B):.5f}  sd={T_B.std():.5f}")
print(f"T_clean:   mean={T_clean.mean():.5f}  median={np.median(T_clean):.5f}  sd={T_clean.std():.5f}")

ks_AB = stats.ks_2samp(T_A, T_B)
ks_Aclean = stats.ks_2samp(T_A, T_clean)
ks_Bclean = stats.ks_2samp(T_B, T_clean)
print(f"\nKS(A,B):     D={ks_AB.statistic:.4f}  p={ks_AB.pvalue:.4f}")
print(f"KS(A,clean): D={ks_Aclean.statistic:.4f}  p={ks_Aclean.pvalue:.4f}")
print(f"KS(B,clean): D={ks_Bclean.statistic:.4f}  p={ks_Bclean.pvalue:.4f}")

# Plot.
fig, ax = plt.subplots(figsize=(7.5, 4.5))
bins = np.linspace(0, max(T_A.max(), T_B.max(), T_clean.max()) * 1.02, 60)
ax.hist(T_A,     bins=bins, alpha=0.45, label='contamination in cluster A',
        density=True, color='C0')
ax.hist(T_B,     bins=bins, alpha=0.45, label='contamination in cluster B',
        density=True, color='C1')
ax.hist(T_clean, bins=bins, alpha=0.45, label='no contamination (outside blind set)',
        density=True, color='C2')
ax.set_xlabel(r'$T = \max_i\,|\,\hat\beta_{-i} - \hat\beta\,|$  (LOO summary)')
ax.set_ylabel('density')
ax.set_title('Single-point LOO output distribution under cluster rotation')
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig('blind_set_loo.png', dpi=140)
print("\nWrote blind_set_loo.png")
