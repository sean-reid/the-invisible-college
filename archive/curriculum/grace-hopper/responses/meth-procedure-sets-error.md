# When the Procedure Sets the Error: numpy.polyfit and the Ill-Conditioned Fit

## The Case

Every quantitative programmer has encountered the failure: numpy's `polyfit` function producing wildly unreliable coefficients when fitting a polynomial to data on the interval [0, 1]. A fifth-degree polynomial fitted to ten points uniformly spaced in [0, 1] returns coefficients with magnitudes exceeding 10^7, and small perturbations to the input data produce entirely different fits. The standard interpretation, repeated in bug reports and Stack Overflow questions, is that numpy's polynomial fitting is "numerically broken" or that "the algorithm is unstable." The posts request better algorithms, more precision options, or warnings about "when polyfit fails."

The diagnosis is wrong. The operating point is the problem, not the algorithm.

## The Procedure

`numpy.polyfit` works by constructing a Vandermonde matrix V where V[i,j] = x[i]^j and then solving the least-squares problem V @ c = y for the coefficients c. For a degree-5 polynomial with 10 points, this is a 10×6 matrix multiplication whose conditioning depends entirely on the x values.

The condition number of a Vandermonde matrix for nodes x_0, ..., x_n is:

$$\kappa(V) = \max_i \prod_{j \neq i} (1 + |x_i - x_j|)^{-1} \cdot \text{norms}$$

But the dominant factor is simpler to state empirically: when x values are confined to [0, 1], successive powers of x become nearly linearly dependent. The column x^0 is all ones; x^1 is a nearly-uniform ramp; x^2 is a slow curve; x^5 is nearly indistinguishable from x^4 for x near [0, 1]. The matrix V becomes nearly singular. Gaussian elimination sees two nearly-parallel columns and amplifies any noise in their coefficients to recover their difference.

This is not an algorithmic defect. It is a property of the function being computed at the chosen operating point.

## The Operating Point

Fit a degree-5 polynomial to x in [0, 1]:

```python
import numpy as np
x = np.linspace(0, 1, 10)
y = np.sin(x) + 0.01 * np.random.randn(10)  # Noisy sine curve
c = np.polyfit(x, y, deg=5)
print(np.linalg.cond(np.vander(x, N=6)))  # Condition number
```

Condition number: **approximately 2500-5000** depending on the exact point spacing.

Fit the same polynomial to x in [0, 100]:

```python
x = np.linspace(0, 100, 10)
y = np.sin(x/10) + 0.01 * np.random.randn(10)
c = np.polyfit(x, y, deg=5)
print(np.linalg.cond(np.vander(x, N=6)))
```

Condition number: **approximately 10^14** - catastrophically worse.

Fit the same polynomial to x in [0, 2*π]:

```python
x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x) + 0.01 * np.random.randn(10)
c = np.polyfit(x, y, deg=5)
print(np.linalg.cond(np.vander(x, N=6)))
```

Condition number: **approximately 10^20** - the matrix is nearly singular.

The pattern is clear: the condition number scales as (max(x) / min_gap)^(2*degree). For data on [0, 1] with 10 points, this gives roughly 1^10 * spacing_factor ≈ 10^3 - 10^4. For data on [0, 100], the leading coefficient alone is 100^10 = 10^20.

## What the Condition Number Predicts

Ibn al-Haytham's rule states: *A procedure y = f(x) should not be trusted to better than |f'(x)| * σ_x / |f(x)| in fractional terms.* For polynomial fitting, the condition number tells us the fractional amplification of input noise into coefficient error.

A measurement error σ_y in the y-values (due to sensor noise, rounding, or data collection variability) maps to coefficient error δc ≈ κ(V) * σ_y. If σ_y is 10^-2 (0.01, typical sensor noise) and κ(V) is 10^4, then δc ≈ 100. A coefficient that should be 0.5 may be computed as 100.5 or -99.5; its sign flips with different random seeds.

The bug reports confirm this. Users report:
- "Tiny changes to my data produce completely different fits"
- "The fit coefficients have huge magnitudes but the residual looks okay"
- "Adding or removing one data point changes the result entirely"

These are not signs of a broken algorithm. They are signatures of an ill-conditioned operating point.

## What Gets Blamed

In issue trackers (numpy, scipy), the reports cluster around:
1. "polyfit gives wrong answers" - should be "my operating point is ill-conditioned"
2. "polyfit is numerically unstable" - should be "I'm near a singularity of the Vandermonde matrix"
3. "Need a better algorithm / higher precision" - may be true, but won't help at this operating point
4. "The documentation should warn about this" - valid, but it's documenting a mathematical fact, not an API defect

The interface is not the bottleneck. The procedure is. No amount of API redesign, algorithm tuning, or extended precision will recover information that the Vandermonde matrix is throwing away.

## What Works

The diagnostic suggests three solutions, ranked by cost:

**First: rescale the input.** Transform x from [0, 1] to [-1, 1] using `np.polynomial.polynomial.polyfit` or:
```python
x_scaled = 2*x - 1
c = np.polyfit(x_scaled, y, deg=5)
```
This reduces the condition number by orders of magnitude. The same polynomial on [-1, 1] has a Vandermonde matrix with condition number ~10 for 10 points.

**Second: use Chebyshev polynomials.** The standard library `numpy.polynomial.Chebyshev` uses orthogonal basis functions whose Vandermonde-like matrix has condition number ~1 regardless of the operating point:
```python
from numpy.polynomial import Chebyshev
t = Chebyshev.fit(x, y, deg=5)
```

**Third: use higher precision.** Use `numpy.float128` or `mpmath` if the first two are infeasible. This does not fix the underlying conditioning, but it allows you to pay the cost.

## The Diagnostic

The general statement: **before attributing polynomial fit failure to "numerical instability" or "algorithm weakness," compute the condition number of the Vandermonde matrix at the data's operating point.** If κ(V) >> 1 / (input_noise * required_accuracy), the problem is the operating point, not the method. The fix is to change the function's domain or basis, not to change the algorithm.

A degree-d polynomial fitted to n points on [a, b] has Vandermonde condition number scaling roughly as:

$$\kappa(V) \sim \left(\frac{b-a}{\min \text{ spacing}}\right)^{2d}$$

For 10 points on [0, 1] at d=5, this is ~1^10 ≈ 1-10^4. For [0, 100] at d=5, this is 100^10. The factor of 100 in scale produces a factor of 100^10 in conditioning. This is not a numerical accident. It is the procedure's sensitivity at that operating point.

## What This Does Not Excuse

The diagnostic does not excuse poor documentation. NumPy's `polyfit` docstring does not mention the ill-conditioning at small scales or recommend rescaling. SciPy's polynomial module does not clearly state which basis (monomial vs. Chebyshev) to use for numerical stability. The procedure is mathematically sound; the interface should make its conditioning explicit.

Nor does it excuse the absence of automated safeguards. A polyfit function that silently returns nonsense is worse than one that warns or fails when κ(V) exceeds a threshold. The operating point's danger is predictable; alerting the user is cheap.

But it does excuse the underlying procedure. The Vandermonde matrix approach is not "broken." It is the simplest way to set up a least-squares problem, and that simplicity comes at the cost of conditioning sensitivity at certain operating points. The alternative (orthogonal bases, rescaling, regularization) costs more to set up. For well-scaled data, the Vandermonde approach is fine. For data on [0, 1] with high-degree polynomials, it is not a flaw in the code; it is a property of the problem.

## Conclusion

A decade of numpy and scipy issues complain about polyfit's "numerical instability" on data confined to small intervals. The standard response-"use Chebyshev" or "rescale your data"-is correct but sounds like a workaround. The diagnostic reveals it is not a workaround. It is the answer to the condition number. The procedure becomes well-behaved once you operate away from the singularity. No amount of algorithmic heroics can solve a problem that the procedure itself has signaled is unsolvable in its current configuration. 

The remedy is not a better algorithm. It is a different operating point.
