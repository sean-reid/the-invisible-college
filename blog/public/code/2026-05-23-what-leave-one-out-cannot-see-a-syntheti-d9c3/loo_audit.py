"""LOO audit: a battery of synthetic cases probing what observation-level
leave-one-out can and cannot see in OLS coefficient estimation.

Each case below has a known data-generating process, a known "true" beta
for the coefficient of interest, and a contamination structure designed
to probe one failure mode. For each we run:

  - OLS on the contaminated data, record beta-hat
  - Observation-level LOO: max |DFBETAS_i| and the range of LOO beta-hats
  - Leave-pair-out (over the top-K candidate pairs by absolute residual,
    cheaper than O(n^2) but catches Lawrance/Hadi-style masked pairs)
  - Leave-cluster-out where a grouping variable is meaningful

The "verdict" reported for each method is whether the diagnostic moves
beta-hat outside the OLS confidence interval *and* across the true beta.
For LOO that is equivalent to asking: does the standard "results robust
to LOO deletion" claim survive when the underlying estimate is biased?
"""

import numpy as np
from itertools import combinations

RNG = np.random.default_rng(20260523)

# ----- OLS / influence primitives ---------------------------------------

def ols(X, y):
    """Return (beta_hat, residuals, sigma_hat, var_beta, hat_diag)."""
    n, p = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    resid = y - yhat
    sigma2 = (resid @ resid) / (n - p)
    var_beta = sigma2 * XtX_inv
    H = X @ XtX_inv @ X.T
    h = np.diag(H)
    return beta, resid, np.sqrt(sigma2), var_beta, h, XtX_inv

def dfbetas(X, y, coef_idx):
    """DFBETAS_i for the coefficient at coef_idx, all i in one pass via
    the closed-form deletion formula."""
    n, p = X.shape
    beta, resid, sigma, var_beta, h, XtX_inv = ols(X, y)
    # closed-form: beta_(i) = beta - (XtX_inv @ x_i) * resid_i / (1 - h_i)
    XtX_inv_x = X @ XtX_inv.T  # n x p; row i is x_i^T XtX_inv
    delta = (XtX_inv_x.T * (resid / (1 - h))).T  # n x p
    # studentized: divide by sqrt( s_(i)^2 * (XtX^-1)_kk )
    # Belsley-Kuh-Welsch uses sigma_(i), the leave-one-out residual std.
    # Closed form: sigma_(i)^2 = ((n-p) sigma^2 - resid_i^2/(1-h_i)) / (n-p-1)
    s2 = ((n - p) * sigma**2 - resid**2 / (1 - h)) / (n - p - 1)
    s2 = np.clip(s2, 1e-30, None)
    denom = np.sqrt(s2 * XtX_inv[coef_idx, coef_idx])
    db = delta[:, coef_idx] / denom
    # Also return the LOO beta-hat sequence for the coefficient
    loo_beta = beta[coef_idx] - delta[:, coef_idx]
    return db, loo_beta, beta[coef_idx], np.sqrt(var_beta[coef_idx, coef_idx])

def cooks_pair(X, y, top_k_resid=40, coef_idx=1):
    """Joint Cook's distance for pairs. To keep this O(K^2) rather than
    O(n^2), restrict to the K observations with largest |resid_i| / (1-h_i),
    which is what makes a pair influential in the LOO-residual sense.
    Returns (best_pair, max_joint_dfbeta_in_SE_units_for_coef, pair_loo_beta,
    base_beta, se)."""
    n, p = X.shape
    beta, resid, sigma, var_beta, h, XtX_inv = ols(X, y)
    score = np.abs(resid) / (1 - h)
    cand = np.argsort(-score)[:min(top_k_resid, n)]
    best_pair = None
    best_dbeta = 0.0
    best_loo_beta = beta[coef_idx]
    for i, j in combinations(cand, 2):
        idx = np.array([k for k in range(n) if k != i and k != j])
        Xij = X[idx]; yij = y[idx]
        try:
            b_ij = np.linalg.solve(Xij.T @ Xij, Xij.T @ yij)
        except np.linalg.LinAlgError:
            continue
        d = b_ij[coef_idx] - beta[coef_idx]
        if abs(d) > abs(best_dbeta):
            best_dbeta = d
            best_pair = (int(i), int(j))
            best_loo_beta = b_ij[coef_idx]
    se = np.sqrt(var_beta[coef_idx, coef_idx])
    return best_pair, best_dbeta / se if se > 0 else 0.0, best_loo_beta, beta[coef_idx], se

def leave_cluster_out(X, y, cluster, coef_idx=0):
    """For each unique cluster id, fit OLS without that cluster, return
    array of beta-hats."""
    cs = np.unique(cluster)
    betas = []
    for c in cs:
        m = cluster != c
        Xc = X[m]; yc = y[m]
        try:
            b = np.linalg.solve(Xc.T @ Xc, Xc.T @ yc)
            betas.append(b[coef_idx])
        except np.linalg.LinAlgError:
            betas.append(np.nan)
    return np.array(betas)

def summarize(name, true_beta, X, y, cluster=None, coef_idx=1, dfb_thresh=None):
    n, p = X.shape
    if dfb_thresh is None:
        dfb_thresh = 2.0 / np.sqrt(n)
    beta_hat = ols(X, y)[0][coef_idx]
    db, loo_beta, _, se = dfbetas(X, y, coef_idx)
    max_db = np.max(np.abs(db))
    loo_range = (loo_beta.min(), loo_beta.max())
    # LOO flag: any DFBETAS exceeds threshold
    loo_flag = max_db > dfb_thresh
    # LOO "result robust" claim survives iff conclusion (sign+significance) is unchanged
    # operationalize: does the LOO range of beta_hat exclude the true beta?
    loo_misses_truth = (loo_range[0] - 1e-9 > true_beta) or (loo_range[1] + 1e-9 < true_beta)
    # bias of point estimate (in SE units)
    bias_se = (beta_hat - true_beta) / se if se > 0 else np.nan
    out = {
        "name": name,
        "n": n, "p": p,
        "true_beta": true_beta,
        "beta_hat": beta_hat,
        "se": se,
        "bias_se": bias_se,
        "max_dfbetas": max_db,
        "dfb_thresh": dfb_thresh,
        "loo_flag": loo_flag,
        "loo_min": loo_range[0], "loo_max": loo_range[1],
        "loo_misses_truth": loo_misses_truth,
    }
    # Leave-pair-out
    pair, pair_db, pair_loo_beta, _, _ = cooks_pair(X, y, coef_idx=coef_idx)
    out["pair"] = pair
    out["pair_dfbeta_se"] = pair_db
    out["pair_loo_beta"] = pair_loo_beta
    out["pair_loo_misses_truth"] = (
        (pair_loo_beta < true_beta and beta_hat < true_beta) or
        (pair_loo_beta > true_beta and beta_hat > true_beta)
    )
    # Leave-cluster-out
    if cluster is not None:
        lco = leave_cluster_out(X, y, cluster, coef_idx)
        out["lco_min"] = float(np.nanmin(lco))
        out["lco_max"] = float(np.nanmax(lco))
        out["lco_misses_truth"] = (
            out["lco_min"] - 1e-9 > true_beta or out["lco_max"] + 1e-9 < true_beta
        )
    return out

# ----- synthetic cases --------------------------------------------------

def case_single_leverage(n=200, true_beta=1.0):
    """Single high-leverage point, contaminated to bias beta-hat."""
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + eps
    # one extreme x, with y consistent with a steeper slope
    x[0] = 8.0
    y[0] = 2.0 + 4.0 * x[0] + RNG.normal(0, 1)
    X = np.column_stack([np.ones(n), x])
    return X, y

def case_high_residual(n=200, true_beta=1.0):
    """Single high-residual non-leverage point."""
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + eps
    y[0] = y[0] + 30.0  # huge residual, but x[0] is in the middle
    X = np.column_stack([np.ones(n), x])
    return X, y

def case_masked_pair(n=200, true_beta=1.0):
    """Two opposing-leverage points whose individual deletions almost
    cancel (no single-point DFBETAS spike) but whose joint deletion
    materially shifts beta-hat. Classic Lawrance/Hadi masking."""
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + eps
    # Place a balanced pair on opposite ends, biased the same direction:
    # both anomalies push beta upward, but the leverage of each is paired
    # with the leverage of the other so that single deletion barely moves
    # beta. Setting the contaminated y on each so that the residual is
    # small but the slope-contribution is large.
    x[0], x[1] = -6.0, 6.0
    y[0] = 2.0 + 1.7 * x[0]  # implies beta ~ 1.7 from this point alone
    y[1] = 2.0 + 1.7 * x[1]
    X = np.column_stack([np.ones(n), x])
    return X, y

def case_clustered_leverage(n=200, true_beta=1.0, K=8):
    """K mutually similar leverage points sharing a common contamination.
    Each alone has DFBETAS below threshold; together they shift the slope."""
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + eps
    # cluster of K points clustered around x=3, all with y biased upward by ~3
    for k in range(K):
        x[k] = 3.0 + RNG.normal(0, 0.05)
        y[k] = 2.0 + true_beta * x[k] + 4.0 + RNG.normal(0, 0.3)
    X = np.column_stack([np.ones(n), x])
    # The "natural" cluster label for the contaminated batch:
    cluster = np.array(["A"] * K + ["B"] * (n - K))
    return X, y, cluster

def case_group_mean_shift(n=240, true_beta=1.0, n_groups=12):
    """G groups; one group's y is offset by a fixed amount. Each member's
    individual contribution to beta is tiny (<1/n leverage). LOO sees
    nothing; LCO with the true group structure sees it."""
    per = n // n_groups
    group = np.repeat(np.arange(n_groups), per)
    n = per * n_groups
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 0.5, n)
    y = 2.0 + true_beta * x + eps
    # group 0 has its x systematically shifted upward, biasing slope down
    # via classic Simpson-like geometry: within-group slope is 1.0 but
    # between-group means run perpendicular to it.
    mask = group == 0
    x[mask] += 4.0
    y[mask] -= 3.0  # group mean lies off the joint line
    X = np.column_stack([np.ones(n), x])
    return X, y, group

def case_ovb(n=200, true_beta=1.0):
    """Omitted variable z correlated with x and with y. The full DGP has
    y = 2 + 1*x + 2*z + eps; we fit y ~ x only. The OLS beta-hat is
    biased upward; observation-level LOO cannot in principle detect this."""
    z = RNG.normal(0, 1, n)
    x = 0.7 * z + RNG.normal(0, np.sqrt(1 - 0.49), n)  # corr(x,z) ~ 0.7
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + 2.0 * z + eps
    X = np.column_stack([np.ones(n), x])
    # Synthetic "robustness check" cluster: split sample in half arbitrarily
    cluster = np.array(["A"] * (n // 2) + ["B"] * (n - n // 2))
    return X, y, cluster

def case_clean_baseline(n=200, true_beta=1.0):
    """Reference: no contamination. The maximum |DFBETAS| here is the
    'noise floor' the practitioner is reading against."""
    x = RNG.normal(0, 1, n)
    eps = RNG.normal(0, 1, n)
    y = 2.0 + true_beta * x + eps
    X = np.column_stack([np.ones(n), x])
    return X, y

def case_classical_me(n=200, true_beta=1.0):
    """Classical measurement error on the regressor: x_obs = x_true + u.
    Beta-hat is attenuated toward zero. LOO cannot see this."""
    x_true = RNG.normal(0, 1, n)
    u = RNG.normal(0, 0.8, n)  # error variance comparable to x var
    x_obs = x_true + u
    eps = RNG.normal(0, 0.5, n)
    y = 2.0 + true_beta * x_true + eps
    X = np.column_stack([np.ones(n), x_obs])
    return X, y

# ----- run battery ------------------------------------------------------

def run_all():
    results = []

    X, y = case_clean_baseline()
    results.append(summarize("0 clean baseline (no contamination)", 1.0, X, y))

    X, y = case_single_leverage()
    results.append(summarize("A single high-leverage point", 1.0, X, y))

    X, y = case_high_residual()
    results.append(summarize("B single high-residual point", 1.0, X, y))

    X, y = case_masked_pair()
    results.append(summarize("C masked pair (Lawrance/Hadi)", 1.0, X, y))

    X, y, cluster = case_clustered_leverage()
    results.append(summarize("D clustered leverage (K=8 batch) — correct LCO grouping", 1.0, X, y, cluster=cluster))
    # Same data with a *wrong* grouping (random partition into 5 groups of
    # 40, so each group has ~1.6 contaminants on average): the analyst doesn't
    # know which axis the contamination ran along, and the contamination is
    # not aligned with the grouping.
    perm = RNG.permutation(200)
    wrong = np.empty(200, dtype=int)
    for g in range(5):
        wrong[perm[g * 40:(g + 1) * 40]] = g
    results.append(summarize("D' clustered leverage — wrong LCO grouping (5 random partitions)", 1.0, X, y, cluster=wrong))

    X, y, group = case_group_mean_shift()
    results.append(summarize("E group mean shift (one of 12)", 1.0, X, y, cluster=group))

    X, y, cluster = case_ovb()
    results.append(summarize("F omitted-variable bias", 1.0, X, y, cluster=cluster))

    X, y = case_classical_me()
    results.append(summarize("G classical measurement error on x", 1.0, X, y))

    return results

def fmt(r):
    s = f"\n=== {r['name']} (n={r['n']}, p={r['p']}) ===\n"
    s += f"  true beta            = {r['true_beta']:+.3f}\n"
    s += f"  OLS beta-hat         = {r['beta_hat']:+.3f}  (SE {r['se']:.3f})\n"
    s += f"  bias                 = {r['bias_se']:+.2f} SE\n"
    s += f"  max |DFBETAS|        = {r['max_dfbetas']:.3f}  (thresh {r['dfb_thresh']:.3f})\n"
    s += f"  LOO flag             = {'YES' if r['loo_flag'] else 'no '}\n"
    s += f"  LOO beta range       = [{r['loo_min']:+.3f}, {r['loo_max']:+.3f}]"
    s += "  (excludes truth)\n" if r['loo_misses_truth'] else "  (covers truth)\n"
    if r['pair'] is not None:
        s += f"  best pair            = {r['pair']}\n"
        s += f"  pair-LOO beta-hat    = {r['pair_loo_beta']:+.3f}  (move {r['pair_dfbeta_se']:+.2f} SE)\n"
    if 'lco_min' in r:
        s += f"  LCO beta range       = [{r['lco_min']:+.3f}, {r['lco_max']:+.3f}]"
        s += "  (excludes truth)\n" if r.get('lco_misses_truth', False) else "  (covers truth)\n"
    return s

if __name__ == "__main__":
    rs = run_all()
    for r in rs:
        print(fmt(r))
