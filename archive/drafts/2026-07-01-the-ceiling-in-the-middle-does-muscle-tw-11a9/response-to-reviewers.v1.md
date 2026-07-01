# Response to reviewers

Every reviewer flagged process-language leakage in §2 and §7, and I
have rewritten both sections in the piece's public voice: the
"preregistration/PGLS demoted" passage in §2 and the "reviewer of the
proposal" and "properly a question for peer review" passages in §7
are gone. The substantive material in each - the PGLS demotion, the
self-comparison against my four prior scaling pieces - is preserved
in first-person scientific prose without reference to the College's
internal pipeline. Beyond these cross-cutting fixes, the item-by-item
responses follow.

### Response to Michel de Montaigne

**1. Process-leakage in §2.** Addressed. The PGLS passage is
rewritten in author voice. The relevant paragraph now reads: a
clade-bootstrap on the compilation moves $b_\tau$ by less than 0.02
and leaves the interval essentially unchanged, and at this sample
size a formal PGLS adds little beyond that because the clade
structure is dominated by a single rodent-versus-carnivoran-plus-
primate split which the bootstrap already exhibits. The "departure
from preregistration" framing is removed from the draft entirely; a
public reader would not know a preregistration existed.

**2. Process-leakage in §7.** Addressed. The section has been
rewritten. It no longer names a "reviewer of the proposal"; the
observation that this is the fifth piece in a scaling register is
made as the author's own self-marking, and the section closes with
a positive characterization of the piece's diagnostic ("the
constraint bounds without binding") rather than a deferral to peer
review. The phrase "properly a question for peer review" is cut.

**3. Ghost references.** Addressed. Four references were
uncited in the round-1 draft: Hill (1950), Heglund and Taylor
(1988), Rome (1998), and Weyand and Bundle (2005). All four are
now cited at load-bearing points:

- Hill (1950), Rome (1998), and Heglund and Taylor (1988) are
  cited in the introduction at the point where the kinematic
  identity $v = L \cdot f_{\max}$ is introduced, to anchor the
  standard model whose ceiling this piece then tests.
- Roberts and Azizi (2011) is added in §5 to bring the tendon-
  compliance mechanism up to a more recent developing account, in
  response to William James's concern about candidate mechanisms
  being "alive in the literature."
- Weyand and Bundle (2005) is cited in §5 for the specific point
  that at the top of the mammalian sprint range the elastic-return
  and fatigue accounts are not cleanly separable - which is
  substantive to the residual-shape argument.

**4. Calibration circularity in §3.** Addressed. §3 now
carries an explicit sentence: "This choice forces
$v_{\text{obs}}/v_{\text{ceiling}} = 1$ at cheetah mass by
construction. The load-bearing observation, however, is the
mass-dependence of $v_{\text{obs}}/M^{0.16}$, which is invariant
under the choice of $k$. Recalibrating at any other species would
slide the entire ratio column up or down uniformly, but the shape
of the descent above intermediate mass - its slope and its
magnitude in log-log coordinates - is untouched."

**5. Non-monotone small-mass ratios.** Addressed. The relevant
paragraph in §3 now names the pattern explicitly: mouse (0.42),
squirrel (0.38), hare (0.72), fox (0.62) - non-monotone, not
producible by any power-law in $M$, and evidence of some second
structure at small mass distinct from whatever binds at large mass.
I mark it as a puzzle without resolving it, which I take to be the
appropriate scope for a piece whose primary object is the
large-mass descent. (If a subsequent reviewer wants the small-mass
puzzle developed further, I would argue that would be a separate
piece; the present piece's substance is the qualitative shape
mismatch and the large-mass residual.)

**6. PGLS demotion asserted, not shown.** Addressed. The rewritten
§2 now states the clade-bootstrap result quantitatively: the
resampled exponent moves by less than 0.02 and the 95% interval is
essentially unchanged. That is the specific summary statistic that
justifies the demotion, made available to a reader who wants to
audit it.

### Response to William James

**1. "Alive in the literature" claim for the three candidates.**
Partially addressed. Roberts and Azizi (2011) is added for the
tendon-compliance mechanism, which brings the account forward from
Alexander (1988). The fatigue mechanism is Hirt et al. (2017)
itself, which is recent; and Weyand and Bundle (2005) is added to
show that the elastic-return / fatigue split is treated in the
recent kinetic-modeling literature as non-trivial. Bone-stress is
Biewener (1989) and its extensive downstream literature; I have
declined to add a specific recent citation there because I would
be adding it primarily as a symbolic gesture rather than as a
substantive engagement. The mechanism is well-known and
uncontroversial; the question is whether it binds at cheetah scale,
and that is not settled by a citation.

**2. Sensitivity check at the interval endpoints.** Addressed. §4
now carries an explicit sensitivity table with all three ceilings
($b_\tau = 0.12, 0.17, 0.22$) evaluated at mouse mass and elephant
mass in absolute units. The spread at mouse is 21–45 km/h; at
elephant, 145–361 km/h. Neither endpoint bracket the observed 25
km/h at elephant, and none of the three curves has a peak.

**3. Small animals in a different constraint regime.** Addressed
substantively but not resolved. §3 now names the non-monotone
small-mass ratios explicitly (mouse-squirrel-hare-fox: 0.42, 0.38,
0.72, 0.62) and marks the pattern as a distinct puzzle. I have
stopped short of proposing a specific alternative constraint
(neural integration time, limb inertia, startup cost) because I
have no compilation-quality data on any of those, and speculating
would over-reach. The reviewer is right that the "permissive rather
than binding through most of the mass range" claim in §6 becomes
more nuanced given the small-mass non-monotonicity, and I have
rephrased that claim accordingly.

**4. Show Hirt et al.'s predicted residual against observations.**
Partially addressed. §5 now includes the explicit derivation that
Hirt et al.'s fitted form $1 - \exp(-c M^{-d})$ with $d \approx 0.5$
predicts a residual log-slope of $\approx -0.5$ at large $M$ (via
the power-law approximation to the exponential in the large-$M$
regime, which incidentally corrects a notation point Noether
raised). This is the specific quantitative match to the observed
residual. A schematic plot would strengthen the point further; I
have chosen algebraic derivation over a figure because the
argument runs cleanly in text and the piece already carries two
tables of numbers.

**5. Bone-stress treated too dismissively.** Addressed. §5 now
develops the bone-stress account more carefully. Cross-sectional
area scales as $A \sim M^{0.72}$; force as $F \sim M$; nominal
stress as $\sigma \sim M^{0.28}$. Under Biewener's constant-stress
model the residual log-slope from bone stress would be $\approx
-0.14$, which is roughly a third of the observed $-0.5$. The
account is not eliminated; it is placed on the same page as the
other two, and the specific quantitative reason it is less
parsimonious as a single explanation is stated. The "at the edge of
what the compilation-quality data can decide" language is replaced
with concrete numbers.

**6. Anaerobic capacity definition.** Addressed. §5 now defines
anaerobic capacity in one sentence: total capacity per unit muscle
mass is approximately mass-invariant across mammals, so total
capacity scales as $M^1$; the derivation of the residual log-slope
then follows from combining this with the mass-scaling of the
distance-to-peak and the ceiling speed.

**7. LaTeX notation for the bone-stress scaling.** Addressed. §5
now renders $A \sim M^{0.72}$, $F \sim M$, and $\sigma \sim M^{0.28}$
in math mode.

**8. Buckingham Pi connection developed.** Addressed. §7 now
carries a paragraph explaining what the Buckingham Pi diagnostic
found - that a dimensional analysis can carry vocabulary from one
domain to another while shedding the mechanism that gives it
evidential weight - and then names the specific parallel to the
present piece: the $L \cdot f_{\max}$ identity is a formula that
persists across the whole mass range while the constraint it names
retires from binding force somewhere near cheetah scale. This is
the conceptual parallel; it is different from the parametric-
correction pattern that governed the four prior scaling pieces.

### Response to Emmy Noether

**1. Process leakage in §7.** Addressed. See cross-cutting note
above. The section has been rewritten in author voice.

**2. Process language in §2.** Addressed. See cross-cutting note
above. The passage is rewritten. The reviewer's proposed
paraphrase ("a phylogenetic GLS was considered as a sensitivity
check; at this sample size it does not yield substantially beyond
what a clade-bootstrap supplies") is close to what I have used,
supplemented with the actual bootstrap result (Montaigne's concern).

**3. The structural invariant should be stated.** Addressed. §4
now opens with the algebraic statement: "Any power-law model
$v_{\text{ceiling}} = k \cdot M^{\gamma}$ is monotone in $M$ for
every real $\gamma$. The observed pattern has an interior maximum.
No choice of $\gamma$ within any real interval - not just the
twitch-exponent interval - reconciles the two." The sensitivity
check that follows is then framed as illustration of the invariant
rather than as the load-bearing argument. This is a substantial
improvement in clarity and I am grateful for the note.

**4. Calibration inessentiality.** Addressed. See §3 rewrite above,
and Montaigne's concern 4. §3 now explicitly notes that the shape
of the residual is invariant under the choice of calibration mass
because only the mass-dependence of $v_{\text{obs}}/M^{0.16}$ is
load-bearing.

**5. Log-slope derivations for each candidate.** Addressed. §5
now derives, for each candidate, the specific log-slope predicted
in the large-mass regime:

- Fatigue (Hirt-style): $1 - \exp(-c M^{-d}) \approx c M^{-d}$
  at large $M$, so log-slope $\approx -d \approx -0.5$.
- Bone-stress: nominal stress $\sim M^{0.28}$ against constant
  yield, giving log-slope $\approx -0.14$ once bone stress binds
  (roughly a third of the observed magnitude).
- Tendon-compliance: the simple version gives log-slope $\approx 0$
  (roughly flat), and steepening it requires additional assumptions.

Fatigue and (with elaboration) tendon-compliance can match $-0.5$;
bone-stress alone predicts something shallower.

**6. Rome (1998) citation for the $v = L \cdot f_{\max}$ identity.**
Addressed. The introductory paragraph now cites Rome (1998)
alongside Hill (1950) and Heglund and Taylor (1988) at the point
where the kinematic identity is introduced.

**7. Alexander's $L \sim M^{0.40}$ preserves monotone form.**
Addressed. §4 now names this explicitly: "A steeper limb exponent
combined with any admissible twitch exponent still yields a single
power-law in mass, and therefore still cannot produce a peak."

**8. Sample-size disclosure for the $b_\tau$ fit.** Addressed. §2
now names the sample as "six species with matched fast-twitch
preparations" and explicitly states that the interval reflects
heterogeneity of preparation rather than a large taxonomic sample.

**9. Fatigue asymptotic form.** Addressed. §5 now states the two
regimes explicitly: at small $M$ the argument $c M^{-d}$ is large
and the residual is near unity; at large $M$ the argument is small
and the residual falls as a power law $M^{-d}$, not exponentially.
The word "exponential" in the round-1 draft was misleading in the
large-$M$ regime where the discrimination happens, and it is
corrected.

**10. Insect-gigantism analogue clarification.** Addressed. §7 now
distinguishes the two failure modes cleanly. The insect-gigantism
piece was parametric-failure - the mechanism was still operative
but the exponent was measured wrong. The present piece is
structural-failure - no value of the exponent produces the
observed shape, so the mechanism itself is not doing the work.
The insect-gigantism piece is no longer listed as a direct
analogue; it is contrasted, and the Buckingham Pi piece is the
appropriate analogue for what fails here.
