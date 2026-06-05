"""
simulate.py
Uncertainty propagation through Spearman's correction for attenuation.

Author: Ibn al-Haytham, 2026-06-04
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

RNG = np.random.default_rng(20260604)

# ---------------------------------------------------------------------------
# Section 1.  Analytical results (delta method on the log)
# ---------------------------------------------------------------------------
# r_hat = r_obs / sqrt(r_xx * r_yy)
# ln r_hat = ln r_obs - 0.5 (ln r_xx + ln r_yy)
# Treat r_xx, r_yy as independent random variables.
# Var(ln r_hat) = 0.25 (Var(ln r_xx) + Var(ln r_yy))
# For r_xx ~ Normal(mu, sigma^2) with small sigma, Var(ln r_xx) ~ (sigma/mu)^2.

def analytical_log_sd(mu_xx, sd_xx, mu_yy=None, sd_yy=None):
    if mu_yy is None:
        mu_yy = mu_xx
    if sd_yy is None:
        sd_yy = sd_xx
    rel_var = 0.25 * ((sd_xx / mu_xx) ** 2 + (sd_yy / mu_yy) ** 2)
    return np.sqrt(rel_var)


def correction_signal_log(mu_xx, mu_yy=None):
    if mu_yy is None:
        mu_yy = mu_xx
    return -0.5 * (np.log(mu_xx) + np.log(mu_yy))


def signal_to_noise(mu, sd):
    return correction_signal_log(mu) / analytical_log_sd(mu, sd)


# ---------------------------------------------------------------------------
# Section 2.  Monte Carlo verification of the delta-method approximation
# ---------------------------------------------------------------------------

def truncated_normal_reliability(mu, sd, n_draws, lo=0.05, hi=0.999):
    """Draw plausible reliabilities; clip to (lo, hi)."""
    a, b = (lo - mu) / sd, (hi - mu) / sd
    return stats.truncnorm.rvs(a, b, loc=mu, scale=sd, size=n_draws, random_state=RNG)


def monte_carlo_corrected(r_obs, mu_xx, sd_xx, mu_yy=None, sd_yy=None, n=50_000):
    if mu_yy is None:
        mu_yy, sd_yy = mu_xx, sd_xx
    rxx = truncated_normal_reliability(mu_xx, sd_xx, n)
    ryy = truncated_normal_reliability(mu_yy, sd_yy, n)
    return r_obs / np.sqrt(rxx * ryy)


# ---------------------------------------------------------------------------
# Section 3.  Empirically motivated reliability profiles
# ---------------------------------------------------------------------------
# Each profile gives a name, central reliability, and an empirical SD drawn
# from reported ranges in published reliability generalization syntheses.
# These are illustrative bands, not extracted primary data.
#
# PHQ-9:    Manea et al. 2012 meta-analytic ranges; Kroenke et al. 2001.
#           Cronbach alpha typically 0.83-0.89 across populations.
# GAD-7:    Plummer et al. 2016; alpha range ~0.83-0.93.
# BFI-44:   Schmitt et al. 2007 cross-cultural; alpha 0.75-0.90 per facet.
# BDI-II:   Yin and Fan 2000 reliability generalization; alpha 0.83-0.93.
#
# We translate each range to a Normal central value + SD by treating the
# reported range as a 90% interval (heuristic).  These numbers are used to
# motivate the spread, not to make point claims about any specific
# instrument's true reliability distribution.

INSTRUMENTS = {
    "PHQ-9 (alpha)": {"mu": 0.86, "sd": 0.025},
    "PHQ-9 (test-retest, 1-7 day)": {"mu": 0.81, "sd": 0.06},
    "GAD-7 (alpha)": {"mu": 0.88, "sd": 0.030},
    "BFI-44 facet (alpha)": {"mu": 0.82, "sd": 0.045},
    "BDI-II (alpha)": {"mu": 0.88, "sd": 0.030},
    "BDI-II (test-retest, weeks)": {"mu": 0.83, "sd": 0.06},
    "Brief scale (illustrative)": {"mu": 0.70, "sd": 0.08},
}


# ---------------------------------------------------------------------------
# Section 4.  Regime classification
# ---------------------------------------------------------------------------
# Four regimes from the proposal, redefined precisely:
#   A  signal-dominated  : |signal| > 2 * noise_sd  (the 80% interval excludes 0)
#   B  modest signal     : 1 < |signal|/noise_sd <= 2
#   C  noise-dominated   : 0.3 < |signal|/noise_sd <= 1
#   D  inert/reversing   : |signal|/noise_sd <= 0.3 OR sign of correction reverses
#                          across the 80% empirical reliability interval

def regime(snr):
    snr = abs(snr)
    if snr > 2.0:
        return "A: signal-dominated"
    if snr > 1.0:
        return "B: modest signal"
    if snr > 0.3:
        return "C: noise-dominated"
    return "D: inert"


# ---------------------------------------------------------------------------
# Section 5.  Run the analysis
# ---------------------------------------------------------------------------

def report():
    print("\n=== Half-power identity ===")
    # Check: relative sensitivity is exactly -1/2 for each reliability
    eps = 1e-6
    mu = 0.85
    base = 1.0 / np.sqrt(mu * mu)
    pert = 1.0 / np.sqrt((mu + eps) * mu)
    rel = ((pert - base) / base) / (eps / mu)
    print(f"  d ln r_hat / d ln r_xx evaluated at mu=0.85 -> {rel:.6f}  (expected -0.5)")

    print("\n=== Analytical SNR by instrument profile ===")
    print(f"  {'profile':<32s} {'mu':>6s} {'sd':>6s} {'|signal|':>10s} {'noise':>8s} {'SNR':>6s}  regime")
    for name, p in INSTRUMENTS.items():
        mu, sd = p["mu"], p["sd"]
        sig = correction_signal_log(mu)
        nos = analytical_log_sd(mu, sd)
        snr = sig / nos
        print(f"  {name:<32s} {mu:6.3f} {sd:6.3f} {sig:10.4f} {nos:8.4f} {snr:6.2f}  {regime(snr)}")

    print("\n=== Monte Carlo verification (PHQ-9 alpha case) ===")
    p = INSTRUMENTS["PHQ-9 (alpha)"]
    for r_obs in [0.10, 0.25, 0.40, 0.55]:
        samples = monte_carlo_corrected(r_obs, p["mu"], p["sd"])
        mc_log = np.log(samples)
        ana_sd = analytical_log_sd(p["mu"], p["sd"])
        print(f"  r_obs={r_obs:.2f}  median r_hat={np.median(samples):.4f}  "
              f"80% CI [{np.quantile(samples,0.10):.4f}, {np.quantile(samples,0.90):.4f}]  "
              f"MC sd(log)={mc_log.std():.4f}  analytical sd(log)={ana_sd:.4f}")

    print("\n=== Threshold reliability spread for SNR=1 ===")
    print("  (largest empirical SD such that the correction's signal still equals one noise SD)")
    for mu in [0.70, 0.80, 0.85, 0.90, 0.95]:
        # signal = -ln(mu); noise = sqrt(0.25 * 2 * (sd/mu)^2) = sd / (mu * sqrt(2))
        # signal = noise -> sd = -ln(mu) * mu * sqrt(2)
        sd_threshold = -np.log(mu) * mu * np.sqrt(2)
        print(f"  mu={mu:.2f}  max sd (SNR=1) = {sd_threshold:.4f}")

    # Save the regime map figure
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Panel 1: SNR contours over (mu, sd)
    mus = np.linspace(0.55, 0.97, 200)
    sds = np.linspace(0.01, 0.20, 200)
    M, S = np.meshgrid(mus, sds)
    SNR = -np.log(M) / (S / (M * np.sqrt(2)))
    cs = axes[0].contourf(M, S, np.clip(SNR, 0, 6), levels=20, cmap="viridis")
    axes[0].contour(M, S, SNR, levels=[0.3, 1.0, 2.0], colors=["white", "white", "white"], linewidths=1.5)
    cb = plt.colorbar(cs, ax=axes[0], label="signal-to-noise ratio (log scale)")
    # Overlay instrument profiles
    for name, p in INSTRUMENTS.items():
        axes[0].plot(p["mu"], p["sd"], "o", color="white", markeredgecolor="black", markersize=6)
        axes[0].annotate(name, (p["mu"], p["sd"]), xytext=(4, 4),
                          textcoords="offset points", fontsize=7, color="white")
    axes[0].set_xlabel(r"central reliability  $\mu$")
    axes[0].set_ylabel(r"empirical SD of reliability  $\sigma$")
    axes[0].set_title("Regime map: SNR contours\nwhite lines = SNR boundaries 0.3 / 1 / 2")

    # Panel 2: SNR vs mu for several sigma values
    mus = np.linspace(0.60, 0.97, 200)
    for sd in [0.02, 0.04, 0.06, 0.10, 0.15]:
        snr = -np.log(mus) / (sd / (mus * np.sqrt(2)))
        axes[1].plot(mus, snr, label=fr"$\sigma$={sd:.2f}")
    axes[1].axhline(1.0, color="grey", linestyle="--", linewidth=0.8)
    axes[1].axhline(2.0, color="grey", linestyle=":", linewidth=0.8)
    axes[1].set_xlabel(r"central reliability  $\mu$")
    axes[1].set_ylabel("signal-to-noise ratio")
    axes[1].set_title("SNR as a function of mean reliability\nat fixed empirical spread")
    axes[1].legend(fontsize=8)
    axes[1].set_ylim(0, 6)

    plt.tight_layout()
    plt.savefig("regime-map.png", dpi=160)
    print("\n  Saved figure: regime-map.png")

    # Second figure: a worked example showing the corrected-correlation
    # distribution at a few r_obs values for a moderate reliability profile.
    fig2, ax = plt.subplots(figsize=(7, 4.5))
    mu_xx, sd_xx = 0.80, 0.07
    for r_obs, color in zip([0.15, 0.30, 0.45], ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        samples = monte_carlo_corrected(r_obs, mu_xx, sd_xx, n=80_000)
        ax.hist(samples, bins=80, density=True, alpha=0.45, color=color,
                label=fr"$r_{{obs}}={r_obs:.2f}$ -> median {np.median(samples):.3f}")
        ax.axvline(r_obs, color=color, linestyle="--", linewidth=1)
    ax.set_xlabel(r"$\hat{r}_{true}$  (corrected correlation)")
    ax.set_ylabel("density")
    ax.set_title(rf"Posterior of $\hat{{r}}_{{true}}$ under reliability uncertainty"
                 f"\n($\\mu_{{xx}}={mu_xx}$, $\\sigma_{{xx}}={sd_xx}$; dashed = uncorrected $r_{{obs}}$)")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("posterior-example.png", dpi=160)
    print("  Saved figure: posterior-example.png")


if __name__ == "__main__":
    report()
