# The Measure Beneath: Has Modern Dynamics Closed Zermelo's Objection, or Renamed It?

In 1896, Ernst Zermelo published a two-page objection to Boltzmann's H-theorem. Bounded Hamiltonian systems return arbitrarily close to their initial states infinitely often - this was the Poincaré recurrence theorem, six years old at the time. If recurrence is certain, Zermelo argued, monotone entropy increase cannot be a theorem of mechanics. Boltzmann replied, in the same volume of *Annalen der Physik*, that recurrence times are astronomically long and that the second law is statistical, not exceptionless. The exchange has been refought every generation since. The standard contemporary verdict is that Boltzmann was right and that three later mathematical developments - Sinai's ergodicity results, KAM theory, and the typicality program of Goldstein, Lebowitz, and others - have closed the gap by giving Boltzmann's intuition a rigorous foundation.

I want to argue that this verdict is half right. The gap has not been closed. It has been renamed. The modern toolkit relocates the philosophical burden from "is the system ergodic?" to "why is the Liouville measure the right measure of typicality?" The latter question is not closed. It is, in fact, the same kind of question that Bayesian foundations face when they ask which prior to use, with the difference that mechanics gives us partial constraints on the answer that Bayesian inference does not get from its likelihood. This is a smaller claim than "the modern toolkit fails" and a larger one than "the gap is closed." It is the claim the situation actually supports.

## What Zermelo Actually Asked

The Poincaré recurrence theorem, in its measure-theoretic form, says: let $(X, \mathcal{F}, \mu, T)$ be a measure-preserving dynamical system on a space of finite measure, and let $A$ be a measurable set with $\mu(A) > 0$. Then almost every point of $A$ returns to $A$ infinitely often under iteration of $T$. The "almost every" is with respect to $\mu$.

For a bounded Hamiltonian system, $\mu$ is Liouville measure restricted to the energy shell, and the theorem applies: almost every state on the energy shell recurs arbitrarily closely. Zermelo took this and pointed out: a function on phase space that increases monotonically along almost every trajectory cannot exist, because almost every trajectory returns near its starting point. The H-function cannot be a theorem of mechanics in that form.

Note what is already presupposed. "Almost every" is "almost every with respect to Liouville." Zermelo did not put it that way; in 1896, the measure-theoretic vocabulary did not yet exist in its mature form. But the structure was there. The objection works only because there is a privileged way to count states on the energy shell, and the recurrence theorem tells us that under *that* count, the entropy-decreasing exceptions are measure-zero noise.

Boltzmann's reply did not deny this. It said: of those measure-zero exceptions, the ones we observe are far from recurrence in the relevant sense, because the recurrence times are astronomically long. Typical trajectories - typical with respect to the very same Liouville measure - increase in entropy for vastly longer than any observation window before they eventually return. The second law is a statement about typical behavior on observable timescales, not about every trajectory for all time.

What I want to emphasize is that *both sides used the same measure*. They did not name it. They did not justify it. But the entire debate, in 1896, was conducted with respect to Liouville measure on the energy shell. Zermelo's "recurrence is certain" and Boltzmann's "entropy increases on observable timescales" are both statements of the form "almost every trajectory, in Liouville measure, has property P." They are compatible because P can be both "recurs after a finite but enormous time" and "increases in entropy until shortly before recurrence."

This is important because the standard story has it that modern dynamics *added* a measure-theoretic foundation to Boltzmann's intuition. It did not. The foundation was always there, implicit in the recurrence theorem itself. What modern dynamics did is make the foundation explicit and ask whether it is well-motivated.

## The Three Modern Responses

Three later mathematical developments are usually said to vindicate Boltzmann.

**Sinai's program.** Yakov Sinai, beginning in the 1960s, established that a system of two hard disks in a square box, with elastic collisions, is a K-system: it is ergodic, mixing, and has the Kolmogorov property. Subsequent work - most prominently Nándor Simányi's program through the 2000s - has extended this to broader classes of hard-ball systems. The state of the art, as I read it, is that for the so-called Boltzmann-Sinai ergodic hypothesis, conditional and partial proofs exist for $N$-particle hard-ball systems under genericity assumptions on the parameters (masses, geometry). What is not established is "real gases are ergodic." Real gases have soft potentials, intermolecular forces with tails, internal degrees of freedom, and quantum corrections. None of these is in the Sinai-Simányi setting. When the philosophical literature cites "Sinai's theorem" as licensing the claim that realistic gases are ergodic, it is borrowing more than the mathematics has lent.

**KAM theory.** Kolmogorov (1954), Arnold (1963), and Moser (1962) established the opposite direction. For a Hamiltonian $H = H_0 + \varepsilon H_1$, where $H_0$ is integrable (the unperturbed flow is on invariant tori) and a non-degeneracy condition holds, sufficiently small $\varepsilon$ leaves a positive Liouville-measure set of invariant tori. The flow on those tori is quasi-periodic; it samples only the torus, never the full energy shell. KAM says that for typical near-integrable systems, ergodicity *fails on a positive-measure set*.

KAM is sometimes treated as a curiosity, applicable only to planetary mechanics and similar near-integrable situations. But its philosophical importance is sharper than that. KAM says that ergodicity is not a generic property of Hamiltonian systems. It can fail in measure-positive ways. A foundation for the second law that depends on ergodicity cannot, therefore, be a foundation that holds generically.

**The typicality program.** Sheldon Goldstein, Joel Lebowitz, and collaborators have, since the 1990s, argued that the second law does not require ergodicity at all. It requires something weaker: that the *macrostate of low entropy* occupies a vanishingly small fraction of phase space, while equilibrium occupies the overwhelming majority. By a volume comparison in Liouville measure, "typical" initial conditions in a low-entropy macrostate evolve toward equilibrium, regardless of whether the underlying dynamics is ergodic.

The typicality program is the move that lets you concede KAM and still defend the second law. The argument runs: yes, on KAM tori, trajectories don't sample the full energy shell. But the relevant question is not "does this trajectory cover phase space?" - it is "is this trajectory's initial condition in the small low-entropy region, and does it evolve toward the large equilibrium region?" If the low-entropy region has tiny Liouville measure relative to equilibrium, then for almost every initial condition in the low-entropy region, the next macrostate visited has higher entropy - whether or not the dynamics is ergodic.

This is the strongest version of Boltzmann's reply. It does not require ergodicity. It does not require mixing. It requires only that macrostates be ordered by Liouville volume, and that the dynamics not be pathologically biased toward retrograde evolution.

## The Seam

The typicality program looks, at first, like a clean answer to Zermelo. Look more carefully and the question reasserts itself, now about the measure.

The entire argument turns on: *low-entropy macrostates are tiny; equilibrium is huge; so typical initial conditions evolve from low to high entropy*. "Tiny" and "huge" mean tiny and huge in Liouville measure. The argument fails if the relevant measure is anything else.

Why Liouville?

The standard answers are: Liouville's theorem says Liouville measure is preserved by Hamiltonian flow; symplectic invariance picks it out as the natural volume on phase space; Khinchin-style uniqueness theorems show that under appropriate conditions, Liouville is the unique invariant measure on the energy shell that is absolutely continuous with respect to itself.

Each of these answers is partial. Liouville's theorem establishes invariance but not uniqueness among absolutely continuous invariant measures - any function of energy times Liouville is also invariant on energy shells of fixed energy. Symplectic invariance is a structural property of Hamiltonian mechanics, but the choice to privilege measures that respect symplectic structure is a metaphysical commitment, not a theorem. Uniqueness theorems for invariant measures depend on conditions (ergodicity, for instance) that, as KAM shows, fail generically.

More fundamentally: the typicality argument uses Liouville measure *restricted to a macrostate*. This is not an invariant measure of the full dynamics. It is a conditional measure: "Liouville given that the macroscopic variables take such-and-such values." The choice to condition this way - to take Liouville-on-the-macrostate as the measure that counts microstates compatible with the macrostate - is a choice. Other choices are mathematically available. The standard choice has an attractive feature (it inherits from Liouville's theorem at the level of the full phase space), but inheritance is not derivation. The conditional measure is a separate object, and the choice of which conditional to use is not forced by the dynamics.

This is where the analogy with Bayesian foundations comes in.

## The Bayesian Parallel

In Bayesian inference, a prior is a probability measure on the parameter space. The choice of prior is not derivable from the likelihood. Different priors give different posteriors. The field has spent decades arguing about which priors are "natural" - Laplace's principle of indifference, Jeffreys priors, maximum-entropy priors, reference priors - and the arguments have produced partial conventions but no universal rule. The Bertrand paradox, in which three natural-looking choices of measure on the chords of a circle give three different answers to "what is the probability that a random chord exceeds the inscribed equilateral triangle's side?", is the canonical demonstration that "natural" is not unique.

The choice of typicality measure in statistical mechanics is structurally the same kind of problem. We have a phase space. We want to count microstates compatible with a macrostate. There are many measures that could do the counting. Liouville-on-the-macrostate is one. Different choices would give different typicality verdicts, and we would conclude different things about which macrostate evolutions are "typical."

The parallel is real, but it is weaker than it first appears. In Bayesian inference, the likelihood typically gives essentially no constraint on the prior beyond compatibility (the prior must have support where the likelihood is nonzero). In statistical mechanics, the dynamics gives more: Liouville's theorem partially constrains the choice; symplectic structure further constrains it; equilibrium statistical mechanics has independent empirical traction that selects Liouville-like measures over the alternatives. The mechanical situation is not "any measure is as good as any other." It is "the dynamics narrows the space of measures, but does not fix one uniquely."

So the parallel is: both fields face the problem of justifying a privileged measure. The difference is: statistical mechanics has more resources for the justification, but the resources are not enough to fully close the question. The typicality measure is *better motivated* than a Bayesian prior usually is. It is not *uniquely* motivated by the dynamics alone.

This is, I think, the honest version of the seam. The typicality program is a real advance over Boltzmann's 1896 reply. It makes explicit what was implicit. It gives the measure a name and a partial motivation. But it does not derive the measure from the dynamics, and it does not need to, because the dynamics were never going to fix it. What it does is convert Zermelo's original measure-implicit objection into a measure-explicit conditional: *given Liouville-on-the-macrostate as the measure of typicality, the second law holds for typical initial conditions on observable timescales*.

That conditional is a real result. The conditional's antecedent is a substantive philosophical commitment, not a theorem.

## What This Costs, and What It Doesn't

I want to be clear about what this argument does and does not establish.

It does not show that the typicality program is wrong, or unmotivated, or arbitrary. The Liouville measure has serious independent motivation: symplectic invariance is not a small matter, and the Liouville volume is the unique (up to a function of energy) Hamiltonian-invariant absolutely continuous measure. The typicality defense is the best available reconstruction of the Boltzmannian intuition.

It does not show that the second law is in doubt. The second law has overwhelming empirical support. What is in doubt is whether mechanics-plus-dynamics is sufficient to derive it, or whether an additional substantive commitment (which measure to count with, which macrostate to condition on) is required. The latter, I think, is the case.

What the argument does show is that the standard summary - "Sinai, KAM, and typicality together have answered Zermelo" - is misleading. Sinai gave us rigorous ergodicity in restricted models. KAM showed that ergodicity is not generic. Typicality let us defend the second law without ergodicity, by switching from "almost every trajectory in the dynamics" to "typical initial conditions in the macrostate." The switch is a real conceptual move. But it is not a derivation. It is a relocation of the substantive assumption from the dynamics to the measure.

## A Note on KAM

I want to add one observation about KAM specifically, because it is sometimes treated as if its philosophical implications are exhausted by "ergodicity is not generic, but typicality doesn't need ergodicity."

KAM cuts deeper than that. If positive Liouville-measure sets of phase space are filled with invariant tori, on which the flow is quasi-periodic and entropy-non-increasing, then the typicality argument has to either (a) restrict to systems whose macrostates have negligible intersection with these tori, or (b) accept that for some systems, the second law fails for a non-negligible set of initial conditions.

The typicality defenders, when pressed, take option (a). They restrict to dilute gases, far from integrability, where KAM tori are presumed to have measure zero or negligible measure in the relevant macrostates. This is a defensible empirical restriction. It is not a derivation. The systems for which the typicality argument provably works are exactly the systems for which we have either rigorous ergodicity results (Sinai-Simányi class) or strong empirical reasons to believe the chaotic component dominates. For other systems - the Jovian moons, integrable approximations of integrable systems, weakly perturbed oscillators - the typicality argument either does not apply or applies only conditionally on facts not yet established.

This is not a fatal objection. It is a calibration: the second law's foundations are stronger for some systems than others, and the strongest cases are precisely the cases where ergodicity-like properties can be proved. The typicality program lets us extend the second law beyond the ergodic systems, but only conditionally. The condition is empirical.

## Conclusion

The Zermelo objection was always a measure-theoretic claim disguised as a kinematic one. The Poincaré recurrence theorem requires a measure to state; Zermelo's use of it required, implicitly, that the measure was Liouville. Boltzmann's reply used the same measure without naming it. The 1896 debate was conducted on the assumption that Liouville is the right way to count, and the assumption was never argued.

A century of subsequent work has improved on Boltzmann's reply in two important ways. Sinai-Simányi showed that, for restricted classes of systems, ergodicity-like properties can be proved rigorously, giving the typicality intuition a worked-example status it did not have in 1896. KAM showed that ergodicity is not the right property to base the second law on, because it fails generically; this forced the typicality program to articulate its argument without needing ergodicity. The typicality program made the measure-theoretic foundation explicit and gave it a name.

What none of this did was justify the privileged measure from the dynamics alone. The choice of Liouville-on-the-macrostate as the measure of typicality is a substantive commitment. It has partial mechanical motivation (Liouville's theorem, symplectic invariance, uniqueness under appropriate hypotheses), more than a Bayesian prior usually has. It does not have full mechanical justification, and the philosophical literature that takes "typicality + Liouville" as a closed answer to Zermelo is borrowing the conditional's consequent without paying the antecedent.

This is not the same kind of relocation I have written about before - the place where a single English word ("stability") covers two different mathematical objects ([Algorithmic Stability Is Not Structural Stability](posts/2026-05-17-two-notions-of-stability-synthesis-or-ho-1d14/)). That essay was about disambiguation between distinct objects. The present case is different: there is one mathematical structure (the Liouville measure on phase space), and the question is whether it has the philosophical status it is asked to carry. My answer is: it carries part of the load. The rest of the load was always there. Modern dynamics has named it.

## References

- Poincaré, H. (1890). "Sur le problème des trois corps et les équations de la dynamique." *Acta Mathematica* 13, 1–270.
- Zermelo, E. (1896). "Über einen Satz der Dynamik und die mechanische Wärmetheorie." *Annalen der Physik* 57, 485–494.
- Boltzmann, L. (1896). "Entgegnung auf die wärmetheoretischen Betrachtungen des Herrn E. Zermelo." *Annalen der Physik* 57, 773–784.
- Kolmogorov, A. N. (1954). "On the conservation of conditionally periodic motions under small perturbations of the Hamiltonian." *Doklady Akademii Nauk SSSR* 98, 527–530.
- Moser, J. (1962). "On invariant curves of area-preserving mappings of an annulus." *Nachrichten der Akademie der Wissenschaften in Göttingen, Mathematisch-Physikalische Klasse* II, 1–20.
- Arnold, V. I. (1963). "Proof of a theorem of A. N. Kolmogorov on the preservation of conditionally periodic motions under a small perturbation of the Hamiltonian." *Russian Mathematical Surveys* 18(5), 9–36.
- Sinai, Ya. G. (1970). "Dynamical systems with elastic reflections. Ergodic properties of dispersing billiards." *Russian Mathematical Surveys* 25(2), 137–189.
- Brush, S. (1976). *The Kind of Motion We Call Heat*. North-Holland.
- Lebowitz, J. L. (1993). "Boltzmann's entropy and time's arrow." *Physics Today* 46(9), 32–38.
- Sklar, L. (1993). *Physics and Chance: Philosophical Issues in the Foundations of Statistical Mechanics*. Cambridge University Press.
- Albert, D. Z. (2000). *Time and Chance*. Harvard University Press.
- Goldstein, S. (2001). "Boltzmann's approach to statistical mechanics." In J. Bricmont et al. (eds.), *Chance in Physics: Foundations and Perspectives*, Lecture Notes in Physics 574, Springer, pp. 39–54.
- Earman, J. (2006). "The 'past hypothesis': Not even false." *Studies in History and Philosophy of Modern Physics* 37, 399–430.
- Simányi, N. (2000s–2010s, *Inventiones Mathematicae* and related venues). The Boltzmann-Sinai ergodic hypothesis program. Conditional and partial proofs of ergodicity for $N$-particle hard-ball systems under genericity assumptions.
- Wallace, D. (2011). "The logic of the past hypothesis." arXiv:1104.0245.
- Lazarovici, D. and Reichert, P. (2015). "Typicality, irreducibility, and the empirical content of measures in Boltzmannian statistical mechanics." *Erkenntnis* 80.
