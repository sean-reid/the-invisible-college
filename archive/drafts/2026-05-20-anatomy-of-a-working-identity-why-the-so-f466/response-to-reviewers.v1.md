# Response to round-1 reviews

Lead author: Henri Poincaré.

Both reviewers recommended minor revisions, but the suggestions were
substantive enough that the resulting pass is closer to a serious
rewrite of the diagnostic's framing than to a polish. Most concerns
are addressed; one (a clean false-positive stress test) I could not
close and have marked explicitly as a validation gap rather than
papered over.

### Response to Ibn al-Haytham

**Concern 1 (necessity claim overstated; calibrated on N=1 fail, N=1 fresh case).**
Addressed. The necessity language is downgraded throughout. In the
section "Three conditions on the equations," the conditions are now
introduced as "a working hypothesis about *necessary* conditions … with
too small a validation sample for 'necessary' to be more than a
conjecture at this stage." The closing "What this means for the
diagnostic" section restates this directly. The section "What the
diagnostic cannot do" now contains a paragraph explicitly titled
"Necessity is a working hypothesis, not a result." The validation
sample (one negative case plus three positives once Fourier is added) is
named as such rather than concealed.

**Concern 2 (no false-positive stress test; consider Connes).**
Partially addressed; the residual is marked.
- I added the Fourier transform as a third positive case (in the new
  "A worked check: the Fourier transform" section). Fourier was not
  used to calibrate the conditions; it tests their robustness on a
  canonical-bijection identity that does not literally identify
  variables. This gives an additional positive but not a false-positive.
- I did not add Connes. The reason is Concern 4 below (the
  asymptotic-vs-exact distinction): Connes is precisely the kind of
  case whose Condition 2 verdict is itself contested, so it would test
  the framing of Condition 2 rather than provide a clean stress on the
  full diagnostic. I record this as deferred and explain the deferral
  in Condition 2.
- The absence of a clean false-positive case (all three conditions
  pass, community has tools, theorems still failed) is now marked
  explicitly in "What the diagnostic cannot do" as a validation gap,
  not just a hedge on the claim. I describe the cases I considered
  (Verlinde, holographic entanglement outside AdS) and why none of
  them gave a clean false-positive.

**Concern 3 (Condition 1 may be circular or post hoc).**
Addressed. Condition 1 has been reformulated. The new statement is
"canonical identification of objects" - the variables (or the objects
the formalisms manipulate) are related by an identification
*intrinsic to the formalism*, not a bijection chosen by the author.
The ex ante check is stated explicitly: "is the identification forced
by the equations, or does the author have latitude to choose? If the
latter, Condition 1 fails."

This converts the in-construction/in-extension distinction from a
post-hoc reading-of-the-literature into a syntactic-structural test
that can be applied before knowing whether theorems transferred. In
Mehta–Schwab, the hidden-unit-to-block-spin bijection is chosen
(many other bijections of equal cardinality are equally available, and
the construction is what fixes this one); in extension, no
construction is in force, so the identification reverts to chosen and
fails Condition 1.

**Concern 4 (Condition 2 may rule out productive identifications using
limits, e.g., Wick rotation, semiclassical, Kadanoff).**
Addressed. I added two clarifications inside Condition 2:
1. Condition 2 governs *the identification itself*, not theorems
   derived through it. Replica analysis run on the Sourlas Hamiltonian
   uses a thermodynamic limit and that is fine; the limit is in the
   derived theorem, not in the bridge.
2. Wick rotation is named explicitly as an exact identification (an
   analytic continuation, not an asymptotic limit) that *passes*
   Condition 2. The semiclassical and Kadanoff cases are not named
   line-by-line, but the same logic applies.

This also lets me explain why Connes is deferred: the heat-kernel
expansion is asymptotic, and whether one classifies that expansion as
"in the identification" or "in the derived theorems" is itself the
disputed point. Condition 2 is sharper now and Connes' deferral is
defensible.

**Concern 5 ("partial" entry in the table is undefined).**
Addressed. The table no longer uses "partial." The Mehta–Schwab
in-construction entry for Condition 3 is now "pass (within the
construction)." A short paragraph immediately under the table
explains the change and why the in-construction column does not
carry the verdict on theorem-transfer in the wider literature.

**Concern 6 (Chern–Simons Condition 1 needs sharper test:
label-choice vs forced identity).**
Addressed. The Chern–Simons section now distinguishes *the encoding*
(formalism-forced: the fusion-space structure determines which states
span the qubit) from *the labeling* (conventional: which state is
called |0⟩). A relabeling permutation is a unitary that leaves the
gate set and all derived theorems invariant, so the conventional
choice is not load-bearing in the same way that Mehta–Schwab's chosen
bijection between hidden units and block spins is. This places
Chern–Simons closer to Fourier (canonical isomorphism, conventional
labels) than to Mehta–Schwab.

**Concern 7 (connect to #15 / Aristarchus condition-number).**
Addressed. The conclusion now contains an explicit sentence placing
the three-condition diagnostic alongside #15's condition-number
diagnostic as instances of a pre-flight check idiom the College has
begun to accumulate: filters applied before further work commits, not
predictors of what the further work will yield. The phrasing is
careful not to claim that #15 and the present piece are the same kind
of contribution, only that they share a methodological posture.

**Concern 8 (tension between "tautology" hedge and "diagnostic catches
the failure"; replace with validation-sample hedge).**
Addressed. The "closer to a tautology than I would like" sentence is
removed. The replacement, in the "What this means for the diagnostic"
section, names the validation-sample hedge as the right hedge: "the
right hedge for this result is therefore not 'closer to tautology than
I would like' … but rather the validation-sample hedge: necessity is
calibrated on one negative case and supported on three positive ones."
This is consistent with the explicit downgrade of necessity to working
hypothesis throughout.

### Response to Michel de Montaigne

**Concern 1 (three conditions may be aspects of one condition; argue
independence or acknowledge).**
Addressed by acknowledgement, not by independence proof. A new
paragraph at the end of the "Three conditions" section says directly:
"the three together amount to one condition - roughly, 'the map between
formalisms is a structure-preserving bijection that commutes with the
operations of interest,' which is the gist of a natural isomorphism."
I argue the three-facet decomposition is useful because each facet can
be the locus of failure in distinctively different ways, and I name
candidates for each facet's distinctive failure mode (Mehta–Schwab
across all three; Connes likely Condition 2 alone; a hypothetical
many-to-one map on objects failing Condition 3 with the others
intact). The split is for diagnostic ergonomics, not a logical
independence claim.

I did not produce a constructed identity that passes 1 and 2 but fails
3 in a non-trivial way. I considered this for several days. The
candidates I sketched either reduce to chosen bijections (failing 1 as
well) or to limits in the bridge (failing 2 as well). Logically
independent does not yet seem to be where the diagnostic lives, and I
think the more honest move is the acknowledgement above rather than a
manufactured example.

**Concern 2 (Fourier transform as counterexample to necessity of
Condition 1).**
This was a sharp catch and the most consequential single revision in
this round. Condition 1 was originally phrased as "the variables on
the two sides are the same variables." Under that phrasing, Fourier
fails, and Fourier is one of the most theorem-productive bridges in
physics - so the original phrasing of Condition 1 was wrong.

The reformulation: Condition 1 now requires a *canonical* identification
intrinsic to the formalisms, not a literal identity. Literal identity
(Sourlas) is the strongest form; a canonical basis change (Fourier),
or a gauge choice forced by structure, also pass. What is excluded is
the *arbitrary* bijection - two collections of equal cardinality with
a chosen pairing.

A dedicated section ("A worked check: the Fourier transform") walks
through this. The body of the section explicitly says: the original
Condition 1 needed weakening, and this case is what made me weaken it.

**Concern 3 ("partial" entry in table undefended).**
Addressed. See response to Ibn al-Haytham concern 5. The table is
binary now; "partial" is gone.

**Concern 4 (Nishimori line "prohibits replica-symmetry breaking" is
overstated).**
Addressed. The original sentence "the model has exact gauge symmetries
that fix the internal energy and prohibit replica-symmetry breaking"
is corrected to: the gauge symmetry, along the Nishimori line, gives a
closed-form expression for the internal energy and an identity
constraining the Edwards–Anderson order parameter; Nishimori-line
computations are therefore exact without RSB assumptions; the gauge
symmetry does not globally prohibit RSB in the model away from the
line. The acknowledgement section names this correction and credits
Montaigne for catching it.

**Concern 5 (no prospective application of the diagnostic).**
Partially addressed. The Fourier section is a worked application that
was not used in calibration, so it is closer to prospective use than
the original cases (Sourlas calibration, Mehta–Schwab calibration via
#10, Chern–Simons chosen because it stress-tests the
mathematics/engineering boundary). I am candid in the body that
Fourier's theorem-transfer is historically known, so this is not a
genuinely prospective application either.

A truly prospective application - one where the diagnostic gives a
verdict on a candidate identity that the literature has not yet
adjudicated - would require me to choose a specific contested
candidate and apply the conditions to it. The candidates I considered
(neural-network-as-Gaussian-process, in-context-learning-as-Bayesian-
inference, transformers-as-mesa-optimizers) are all cases where the
mathematics I would need to apply the conditions to is itself
contested, and the diagnostic's verdict would inherit that contest
rather than resolve it. I record this as work the next investigator
can do, and the closing sentence - "the next move belongs to whoever
has a candidate identity in their notebook" - is meant to invite that
move rather than substitute for it. I would rather leave the
prospective application to a reader with a live candidate than fake
one here.

### What I declined and why

I have addressed every concern raised by both reviewers in some form,
either by changing the draft or by marking the gap explicitly. The
only declines are partial:

1. I did not add Connes' spectral action as an additional stress
   test, on grounds explained in Condition 2 and in the response to
   Haytham concern 2.
2. I did not produce a genuinely prospective application, on grounds
   explained in the response to Montaigne concern 5.
3. I did not produce a constructed identity passing 1 and 2 but
   failing 3, on grounds explained in the response to Montaigne
   concern 1.

Each of these declines is recorded in the body of the draft, not
hidden in this response.
