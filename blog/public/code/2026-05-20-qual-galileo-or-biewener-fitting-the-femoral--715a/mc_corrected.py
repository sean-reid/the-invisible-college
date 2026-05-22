"""
Pre-flight Monte Carlo, re-run at the empirical residual sigma.

The proposal's MC used sigma=0.10 on log10(I); empirical residual sd on
log10(FC) is 0.057 which translates to sigma=4*0.057 ~ 0.227 on log10(I)
under the geometric assumption that maps slopes by a factor of 4.

Re-run the MC at the empirical sigma so the pre-flight table closes the
loop with the realised half-width.
"""
import math
import random

random.seed(20260521)

def ols_slope(x, y):
    n = len(x)
    mx = sum(x)/n; my = sum(y)/n
    sxx = sum((xi-mx)**2 for xi in x)
    sxy = sum((xi-mx)*(yi-my) for xi,yi in zip(x,y))
    b = sxy/sxx
    resid = [yi - (my + b*(xi - mx)) for xi,yi in zip(x,y)]
    s2 = sum(r*r for r in resid)/(n-2)
    se = math.sqrt(s2/sxx)
    return b, se

def sim(n, beta_true, sigma, n_sim=2000, x_low=-2.0, x_high=3.7):
    halfs = []
    for _ in range(n_sim):
        x = [random.uniform(x_low, x_high) for _ in range(n)]
        y = [beta_true*xi + random.gauss(0, sigma) for xi in x]
        b, se = ols_slope(x, y)
        halfs.append(1.96*se)
    halfs.sort()
    return halfs[n_sim//2]

print("Pre-flight MC re-run, sigma = 0.10 (proposal) and sigma = 0.227 (empirical)")
print()
print(f"{'n':>4} {'beta_true':>10} {'sigma':>6} {'med 95% half-width':>20}")
for n in (90, 198):
    for s in (0.10, 0.227):
        for bt in (1.0, 4.0/3.0):
            hw = sim(n, bt, s, n_sim=2000)
            print(f"{n:>4} {bt:>10.4f} {s:>6.3f} {hw:>20.4f}")
print()
print("At n=198, sigma=0.227 (empirical translation of 0.057 on log FC),")
print("the predicted half-width is ~0.02 - closely matches the realised")
print("OLS bootstrap half-width of 0.021.")
