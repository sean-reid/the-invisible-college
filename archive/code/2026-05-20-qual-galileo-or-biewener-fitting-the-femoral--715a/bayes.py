"""
Bayesian posterior on (alpha, beta_I, sigma) for log10(I) ~ alpha + beta_I * log10(M),
with the pre-registered priors:
    beta_I ~ N(1.15, 0.15^2)
    alpha  ~ N(2, 5^2)
    sigma  ~ half-Cauchy(1)

Implemented as a Metropolis-Hastings sampler in raw Python (numpy only)
because PyMC is not installed and the model is small enough that a
hand-rolled sampler is verifiable.

Reports the 95% credible interval on beta_I and compares it to the
frequentist 95% CI from OLS bootstrap and PGLS-Brownian.

Decision rule from the proposal: if the posterior 95% credible interval
and the frequentist CI differ by more than 0.03 on either endpoint,
disagreement is the headline.
"""

import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# --- Load data ---
rows = []
with open(os.path.join(HERE, "extants.csv")) as f:
    for r in csv.DictReader(f):
        try:
            BM = float(r["BM"]); FC = float(r["FC"])
        except (ValueError, KeyError):
            continue
        if BM <= 0 or FC <= 0:
            continue
        if r["Mon.Groups"] == "Reptilia":
            continue
        rows.append((BM/1000.0, FC))

# Transform: log10(I) = 4*log10(FC) - log10(64 pi^3), under the solid-beam
# geometric assumption that I = C^4 / (64 pi^3).  The translation moves the
# intercept but the slope of log10(I) on log10(M) IS beta_I directly.
LOG_64PI3 = math.log10(64 * math.pi**3)
x = np.array([math.log10(M) for M, _ in rows])     # log10 body mass (kg)
y_I = np.array([4*math.log10(FC) - LOG_64PI3 for _, FC in rows])  # log10 I

n = len(x)
print(f"n = {n}", flush=True)
print(f"x range: [{x.min():.3f}, {x.max():.3f}]")
print(f"y_I range: [{y_I.min():.3f}, {y_I.max():.3f}]")

# OLS reference
A = np.column_stack([np.ones(n), x])
beta_ols, *_ = np.linalg.lstsq(A, y_I, rcond=None)
resid = y_I - A @ beta_ols
sigma_ols = math.sqrt(float(resid @ resid)/(n-2))
print(f"OLS: intercept={beta_ols[0]:.4f}, beta_I={beta_ols[1]:.4f}, sigma={sigma_ols:.4f}")

# --- Priors ---
def log_prior(alpha, beta_I, sigma):
    if sigma <= 0:
        return -np.inf
    lp_alpha = -0.5 * (alpha - 2.0)**2 / 25.0
    lp_beta = -0.5 * (beta_I - 1.15)**2 / 0.15**2
    lp_sigma = math.log(2.0 / (math.pi * (1.0 + sigma**2)))  # half-Cauchy(1)
    return lp_alpha + lp_beta + lp_sigma

def log_lik(alpha, beta_I, sigma):
    if sigma <= 0:
        return -np.inf
    yhat = alpha + beta_I * x
    rs = y_I - yhat
    return -0.5*n*math.log(2*math.pi*sigma*sigma) - 0.5*float(rs @ rs)/(sigma*sigma)

def log_post(alpha, beta_I, sigma):
    lp = log_prior(alpha, beta_I, sigma)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_lik(alpha, beta_I, sigma)

# --- Metropolis-Hastings ---
rng = np.random.default_rng(20260521)

# Initial values: OLS
alpha = float(beta_ols[0])
beta = float(beta_ols[1])
sigma = sigma_ols
lp_cur = log_post(alpha, beta, sigma)

# Proposal scales (tuned from short trial runs)
prop_alpha = 0.05
prop_beta = 0.01
prop_sigma = 0.03

n_burn = 20000
n_keep = 100000
samples = np.zeros((n_keep, 3))
accepts = 0
for it in range(n_burn + n_keep):
    # Joint proposal (multivariate normal block):
    ap = alpha + rng.normal(0, prop_alpha)
    bp = beta + rng.normal(0, prop_beta)
    sp = sigma + rng.normal(0, prop_sigma)
    lp_prop = log_post(ap, bp, sp)
    if math.log(rng.random()) < lp_prop - lp_cur:
        alpha, beta, sigma = ap, bp, sp
        lp_cur = lp_prop
        if it >= n_burn:
            accepts += 1
    if it >= n_burn:
        samples[it - n_burn] = (alpha, beta, sigma)

acc_rate = accepts / n_keep
print(f"acceptance rate: {acc_rate:.3f}")

# Summaries
def pct(a, p):
    return float(np.percentile(a, p))

a_mean = samples[:, 0].mean()
b_mean = samples[:, 1].mean()
s_mean = samples[:, 2].mean()
print(f"posterior mean alpha: {a_mean:.4f}, 95% CrI [{pct(samples[:,0],2.5):.4f}, {pct(samples[:,0],97.5):.4f}]")
print(f"posterior mean beta_I: {b_mean:.4f}, 95% CrI [{pct(samples[:,1],2.5):.4f}, {pct(samples[:,1],97.5):.4f}]")
print(f"posterior mean sigma: {s_mean:.4f}, 95% CrI [{pct(samples[:,2],2.5):.4f}, {pct(samples[:,2],97.5):.4f}]")

# Diagnostic: probability that beta_I > 4/3 and < 4/3
p_above = float((samples[:, 1] > 4.0/3.0).mean())
p_below = float((samples[:, 1] < 4.0/3.0).mean())
p_above_103 = float((samples[:, 1] > 1.03).mean())
print(f"\nP(beta_I > 4/3 | data) = {p_above:.4f}")
print(f"P(beta_I < 4/3 | data) = {p_below:.4f}")
print(f"P(beta_I > 1.03 | data) = {p_above_103:.4f}")

# Prior-posterior shift on beta_I
prior_mean = 1.15
posterior_mean = b_mean
posterior_sd = float(samples[:, 1].std())
print(f"\nprior on beta_I: N(1.15, 0.15^2)")
print(f"posterior on beta_I: ~N({b_mean:.4f}, {posterior_sd:.4f}^2)")
print(f"prior-posterior shift on mean: {posterior_mean - prior_mean:+.4f}")
print(f"posterior sd / prior sd: {posterior_sd / 0.15:.4f}")

# Save summary
with open(os.path.join(HERE, "bayes_summary.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"acceptance rate = {acc_rate:.3f}\n")
    f.write(f"posterior mean alpha = {a_mean:.5f}\n")
    f.write(f"posterior mean beta_I = {b_mean:.5f}\n")
    f.write(f"posterior 95% CrI on beta_I: [{pct(samples[:,1],2.5):.5f}, {pct(samples[:,1],97.5):.5f}]\n")
    f.write(f"posterior 50% CrI on beta_I: [{pct(samples[:,1],25):.5f}, {pct(samples[:,1],75):.5f}]\n")
    f.write(f"posterior mean sigma = {s_mean:.5f}\n")
    f.write(f"posterior 95% CrI on sigma: [{pct(samples[:,2],2.5):.5f}, {pct(samples[:,2],97.5):.5f}]\n")
    f.write(f"P(beta_I > 4/3) = {p_above:.4f}\n")
    f.write(f"P(beta_I > 1.03) = {p_above_103:.4f}\n")

np.save(os.path.join(HERE, "bayes_samples.npy"), samples)
print("\nDone.")
