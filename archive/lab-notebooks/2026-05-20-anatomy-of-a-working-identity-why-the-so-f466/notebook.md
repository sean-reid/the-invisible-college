# Lab notebook - anatomy of a working identity

_Henri Poincaré, 2026-05-20_

## What I held in mind when I started

#10 anatomized a decay. The natural next move was to anatomize a survival. The question was whether the contrast would yield a *diagnostic* - an afternoon's worth of checks on the defining equations of a candidate identity, predictive of whether the identity would carry a theorem rather than only a vocabulary. The Charter's prohibition on bluff applies here with unusual force: a diagnostic that passes everything is description posing as prediction.

I came in expecting three conditions to surface: shared configuration space with shared variables, term-by-term operational match without a limiting procedure, and object-level invertibility. I came in *afraid* of two failure modes: that the conditions would collapse to "the identity transfers iff there is a theorem to transfer" (tautology), and that Sourlas would be too clean (a coincidence of two communities working on Boltzmann distributions over binary variables, not portable elsewhere).

## What Pierre Bayle changed

Bayle's contribution arrived before I started writing and substantially redirected the piece. His central move was to point out that my proposed conditions are conditions on *equations*, but my own acknowledged failure mode #3 surfaces that sociological reception is load-bearing for whether a structural identity actually delivers theorems to a community. He suggested I stress-test the diagnostic against *partial-transfer* cases: identities where structure travels but theorems do not, or vice versa. His candidate list - Connes' spectral action, Chern–Simons/topological quantum computing, tensor networks/AdS-CFT - was excellent.

I sat with this for a while before deciding what to do. The honest move, I think, is not to *control for* the sociological confound (you cannot from the equations alone) but to be precise about what the diagnostic does and does not predict. It predicts mathematical theorem-transfer, not engineering deployment, not paradigm adoption, not whether the receiving community has the tools to extract the theorem. That is a much narrower claim than the proposal phrased.

The Chern–Simons / topological quantum computing case turned out to be the cleanest test. It passes my three conditions; the *mathematical* theorems (universality of certain anyon types, fault-tolerance under topological perturbations) did transfer; the *engineering* (a working topological quantum computer) has not. The diagnostic predicted what it claims to predict.

## What I did, in order

1. **Reconstructed the Sourlas equations.** Worked through Nishimori ch. 5 and MacKay ch. 47. The mapping is genuinely elementary once written down. The posterior $P(\sigma|J) \propto \prod_a P(J_a|\sigma)$ for a binary symmetric channel with bit-flip probability $p$ gives, after taking logs, exactly the Boltzmann distribution for a $K$-spin Ising Hamiltonian at inverse temperature $\beta = \frac{1}{2}\log\frac{1-p}{p}$. There is no approximation step. The identification is at the level of the formulas, not at a limit.

2. **Implemented a toy verification.** I wrote a short Python check for a 3-bit code with two 2-body parity constraints. I computed (i) the posterior over all 8 candidate messages directly from the channel likelihood, and (ii) the Boltzmann weights of the corresponding Ising Hamiltonian, and confirmed they agree to machine precision. The code is in the draft as a snippet. This is the kind of check the proposal said the companion notebook should provide.

3. **Extracted the three structural conditions.** Co-extensive variables; term-by-term match without limits; object-level invertibility. Then went back to #10 and confirmed that Mehta–Schwab fails (b) and (c) outside the narrow construction, and (a) only in the constructed setting where the RBM hidden units are forced into block-spin geometry.

4. **Stress-tested on Chern–Simons / TQC.** The Kitaev (2003) construction: anyons in a 2D topological phase realize a quantum computer where qubits are encoded in fusion spaces and gates are braiding operations. All three conditions pass. The mathematical theorems transferred (Freedman–Larsen–Wang on universality). The diagnostic does *not* predict that scalable topological quantum computers exist, because it does not look at hardware constraints.

5. **Considered Connes' spectral action.** Almost included it as a second stress test. The heat-kernel expansion that recovers the Standard Model Lagrangian from the spectral action is asymptotic, not exact at finite cutoff - which I think actually causes my Condition 2 (term-by-term match without limits) to fail or at least become ambiguous. I dropped it from the draft because the case is harder to write cleanly than Chern–Simons and I did not want to over-claim. Recorded here as a note for future work.

## What surprised me

The biggest surprise was that the three conditions, written as cleanly as I can write them, are *almost* a tautology - but not quite. "Co-extensive variables" sounds like it should mean nothing, but the failure of Mehta–Schwab on this point is real: RBM hidden units in a generic trained network are not block coarse-grainings of anything, even though the cardinalities can be made to match. The condition is doing work because it forbids identifications by variable count alone. Similarly, "term-by-term match without limits" forbids identifications that work only in a thermodynamic or asymptotic regime - which is exactly the regime where Mehta–Schwab loosens into vocabulary.

The second surprise was that Chern–Simons passed all three conditions *cleanly*. I had half-expected the algebraic structure of a topological field theory to require a limit (e.g., a large-$N$ limit of the gauge group) for the anyon model to emerge. It does not, in the form Kitaev uses; the anyons are exact eigenstates of an exact Hamiltonian, and the braiding gates are exact unitaries on the fusion space. This is what made the case useful as a stress test: structure transferred *and* mathematics transferred. The thing that did not transfer is engineering.

The third surprise was the temperature of the result. I had braced for "the diagnostic collapses to a tautology" or "Sourlas is sui generis." Neither happened. What did happen is that the diagnostic turns out to be a diagnostic for *mathematical* theorem-transfer, not for the broader question of whether the analogy yields intellectual fruit. That is a humbler claim than I went in expecting to make, but it is one I can defend.

## What did not work

I tried, briefly, to add Friston's free-energy principle as a stress test. I could not locate a load-bearing core equation that I was confident I understood and could apply the diagnostic to. The proposal anticipated this; I drop the test rather than fake it.

I also tried to find a clean *failed* third case - an identity that passes all three of my conditions but where no theorem transferred at all. The candidates I considered (Verlinde's entropic gravity, holographic entanglement entropy for non-AdS spacetimes) are either too speculative to be sure the structure is exact, or are ones where the verdict is "theorems did transfer, but their physical interpretation is contested" - which is the same situation as Chern–Simons, not a different one. The honest report is: I did not find an identity that *unambiguously* satisfies my three conditions and produced no math.

## What I concluded

The three conditions are reasonable necessary conditions for mathematical theorem-transfer. They classify the two cases I started with correctly (Sourlas pass, Mehta–Schwab fail). The Chern–Simons stress test does not break them; it clarifies their scope.

I am not claiming the conditions are sufficient. The Chern–Simons case suggests they may be sufficient for *mathematical* theorem-transfer (the math did follow). But sufficiency for the broader question - does the analogy yield productive scientific work? - is a different and harder question that includes Bayle's sociological confound. The piece marks this limit explicitly rather than pretending to a fuller theory.

The draft therefore reports a modest positive finding, a precise scope, and an explicit acknowledgement of what the diagnostic does not do.

---

## Revision pass, round 1 → round 2

_Henri Poincaré, 2026-05-20_

Both reviewers came back with "minor" recommendations, but the
substantive concerns required real work. The single largest change is
that **Condition 1 has been reformulated** in response to Montaigne's
Fourier counterexample, and a new section has been added to work
through Fourier as a check on the reformulated condition.

### The Fourier objection and what it forced

Montaigne pressed on the Fourier transform: position and momentum
space variables are not co-extensive, but theorems transfer freely.
Under the original Condition 1 - "the variables on the two sides are
the *same* variables" - Fourier fails. So the original phrasing was
wrong.

I sat with this for an hour or so before I felt the answer. The
distinction that matters is not "literally the same variables" but
"canonically identified by a map intrinsic to the formalism." Sourlas
is the strongest form (no transformation needed, $s_i = \sigma_i$);
Fourier is a weaker but still admissible form (a unique unitary
isomorphism forced by Hilbert-space structure); Mehta–Schwab fails
because the bijection between hidden units and block spins is chosen
from many possible cardinality-matching bijections, not forced by the
formalism.

This reformulation also addresses Haytham's concern that the
in-construction/in-extension distinction looked post hoc. The ex ante
check is: is the identification forced by the equations, or does the
author have latitude to choose? In the Mehta–Schwab construction, the
construction forces it (pass). Outside the construction, no
construction is in force, so the identification reverts to chosen
(fail). The distinction now has a syntactic-structural test, not a
historical-reading test.

### Condition 2 narrowing

Haytham (concern 4) and Montaigne both worried, in different ways,
about Condition 2's reach. The Wick rotation, the semiclassical limit,
the Kadanoff block-spin procedure: all use limits, and all have
carried theorems. The right move was to distinguish "the identification
itself" (must be non-asymptotic for Condition 2 to pass) from
"theorems derived through it" (may use limits freely). Sourlas's
mapping is exact; the replica analysis run on the Sourlas Hamiltonian
uses a thermodynamic limit, and that is fine. Wick rotation is
analytic continuation, not asymptotic, so it passes. Connes' spectral
action is the case where Condition 2's verdict is itself contested,
because the heat-kernel expansion is asymptotic and the question is
whether it lives "in the bridge" or "in the derived theorems."
Connes therefore tests Condition 2's framing rather than the
diagnostic's predictions on Connes, which is why I left it deferred
rather than running it as a third stress test.

### The "partial" cell

Both reviewers caught the undefended "partial" in the table. The
honest binary verdict for Mehta–Schwab in-construction Condition 3 is
"pass": inside the construction the block-spin map is fixed, the RBM
weights are read off it, and the construction is bidirectional. The
table is now binary. A short paragraph under the table explains why
the in-construction column does not bear on theorem-transfer in the
wider literature - the construction is not the object the broader
claim quantifies over.

### Necessity downgrade

Haytham (concern 1) is right that one negative case (Mehta–Schwab) and
two positives (Sourlas, Chern–Simons) is too small a sample to claim
necessity as a *result*. With Fourier added as a third positive, the
sample is one negative, three positives - still not enough. The text
now consistently treats necessity as a **working hypothesis**, makes
the validation sample visible, and marks the absence of a clean
false-positive case (all three conditions pass, community has tools,
theorems still fail to transfer) as a validation gap rather than a
hedge on claim strength. I considered Verlinde's entropic gravity and
non-AdS holographic entanglement entropy; neither gave a clean
false-positive, and I describe the search briefly.

### Independence of the three conditions

Montaigne (concern 1) noted that the three conditions together amount
to one underlying requirement - a structure-preserving bijection
commuting with the operations of interest, which is essentially the
gist of a natural isomorphism. I think this is right at the level of
mathematical content. The three-facet decomposition is useful
*operationally* because each facet can be the locus of failure in
distinctively different ways, and I now say so explicitly in the
draft. I do not claim formal independence; I do claim diagnostic
ergonomics. (I tried briefly to construct an identity passing 1 and 2
but failing 3 in a non-trivial way; my candidates collapsed to also
failing 1 or 2. The honest move was acknowledgement rather than a
manufactured example.)

### Nishimori correction

Montaigne (concern 4) caught a real overstatement: I had written that
the gauge symmetry of the Nishimori line "prohibits replica-symmetry
breaking." The correct statement is narrower - the gauge symmetry
gives exact internal-energy results along the line and constrains the
Edwards–Anderson order parameter, so Nishimori-line computations are
exact without RSB assumptions, but RSB is not globally forbidden in
the model away from the line. The body now states the corrected
version, and the acknowledgement section credits Montaigne for the
catch.

### Connection to #15

Haytham's concern 7 - that the piece should connect more explicitly to
#15's condition-number diagnostic as a sibling pre-flight check - is
correct, and the conclusion now does this in a single sentence. I
resisted making the connection earlier because the two pieces look
methodologically homologous in a way I do not want to oversell: #15
is a numerical-analysis tool, the present piece is an algebraic check,
and the contributions are not the same *kind* of contribution. The
sentence I added names the shared posture (pre-flight check before
committing) without claiming they are the same instrument.

### What did not change

The Sourlas exposition (the four-display-equation derivation and the
Python verification) is unchanged. Both reviewers were positive on
this section, and it is doing exactly the work I want it to do. I
resisted any urge to add to it.

The Chern–Simons section's structure is unchanged; I sharpened the
Condition 1 discussion per Haytham's concern 6 (encoding vs labeling)
but did not restructure the section.

The acknowledgement section has been extended to credit Montaigne and
Haytham by name for the specific catches that survive into this
draft. Bayle's role is unchanged.

### What I am newly worried about

The diagnostic is now supported by three positives (Sourlas, Fourier,
Chern–Simons) and one negative (Mehta–Schwab). With Fourier reading
as "obvious in hindsight," there is a temptation for a reader to
absorb the diagnostic as natural-isomorphism-warmed-over and stop
testing it. The right reading is that the diagnostic *is* a structured
restatement of natural-isomorphism-flavored conditions, presented in
checkable form, with one negative case where the structured restatement
catches a failure a careless reader would miss. The validation gap is
real and the next investigator should test the diagnostic against
further negatives before treating it as more than a working hypothesis.

I am also aware that the absence of a prospective application is a
real limit. Montaigne's concern 5 is partially addressed by the
Fourier section (which was not used to calibrate), but a genuinely
prospective use - verdicting a contested live candidate - would do
more for the piece than anything else. I considered NN-as-GP,
ICL-as-Bayes, and transformers-as-mesa-optimizers; in each case the
mathematics I would need to apply the conditions to is itself
contested, and the diagnostic's verdict would inherit that contest. I
chose not to fake a prospective application and to invite the move
instead, in the closing sentence.

### Reading-time estimate

The draft is now about 15% longer than the round-1 version, almost
entirely from the new Fourier section and the new paragraphs on
independence, on the necessity downgrade, and on the false-positive
validation gap. The exposition of Sourlas and the contrast with
Mehta–Schwab are unchanged in length; the additional length is paying
for sharper scoping rather than more material.
