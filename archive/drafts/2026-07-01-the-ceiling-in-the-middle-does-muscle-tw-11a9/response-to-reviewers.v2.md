# Response to round-2 reviews

All three reviewers recommended minor revision or acceptance and
converged on the diagnosis that the piece's spine is sound.
Convergence at that level is the useful signal: the remaining
concerns are surface derivational and expositional matters, not
substantive challenges to the core claim. I have addressed most of
them and declined a few, with reasons stated below.

### Response to Emmy Noether

**Concern 1 (arithmetic error in §4 elephant sensitivity values).**
Fixed. The elephant column in the sensitivity paragraph now reads
"288, 228, and 181 km/h" rather than the earlier "361, 228, and
145." Noether's diagnosis was exactly right: the extremes had been
computed with the *width* of the $b_\tau$ interval ($\pm 0.10$)
rather than its *radius* ($\pm 0.05$). Under the correct radius and
the calibration $v_{\text{ceiling}}(55) = 110$ km/h, the corrected
values follow directly from $\gamma \in \{0.213, 0.163, 0.113\}$.
The qualitative claim in the following sentence - steepest choice
widens the gap, shallowest narrows it - remains directionally
correct, and the numerical spread at the corrected values still
sits an order of magnitude above the observed 25 km/h. This was a
legitimate rigor concern in a piece whose method is numerical
scaling, and I am grateful the extreme cells were checked
independently.

**Concern 2 (tendon-compliance derivation compressed and
per-stride/per-distance mixed).** Addressed, though the fix
substantively changed the numerical result. Rewriting the derivation
using per-stride quantities throughout (storable energy per stride
$\sim M$; required KE per stride $\sim M v^2$; ratio at the ceiling
$\sim 1/v^2 \sim M^{-0.32}$) gives a naive log-slope of $-0.32$
rather than the "$\approx 0$" the compressed algebra had produced.
The earlier expression $M^{2/3} v^2 / M$ was comparing per-distance
required to per-stride storable and hiding a factor of $L \sim M^{1/3}$;
Noether identified this correctly, and although her review noted
the conclusion was "unaffected" by the tidy-up, closer inspection
shows the correction moves the tendon-compliance naive prediction
from "roughly flat" to $-0.32$. The qualitative role of tendon
compliance in the piece is affected: it is now the closest naive
prediction to the observed $-0.5$ among the three candidates (still
short of the observation), rather than the least-close. I have
rewritten the paragraph accordingly and updated the summary at the
end of §5 and the Conclusion to reflect this. This is the largest
substantive shift in the revision.

**Concern 3 (bridge between first-principles $M^{0.17}$ and Hirt's
empirical $d \approx 0.5$).** Addressed. The fatigue paragraph now
states explicitly that the acceleration-time scaling motivates the
functional form of Hirt et al.'s fit, but that the specific value
$d \approx 0.5$ is empirically fit rather than derived from that
scaling - and that the discrepancy between $0.17$ (from first
principles) and $0.5$ (from the fit) is itself a diagnostic: their
functional form matches the observed shape but their specific
mechanism does not fix $d$ at the value that produces the observed
log-slope. This adds a small piece of intellectual honesty about
what Hirt et al.'s account does and does not settle.

### Response to Michel de Montaigne

**Concern 1 (bone-stress log-slope of $-0.14$ stated but not
derived).** Addressed. The bone-stress paragraph in §5 now includes
the connecting derivation: peak ground reaction force per stride
scales as $F \sim Mv^2/L$ (force times stride length equals per-stride
kinetic energy change); the yield constraint $\sigma = F/A \leq
\sigma_{\text{yield}}$ then forces $v^2 \propto AL/M \sim
M^{0.72 + 1/3 - 1} = M^{0.05}$, giving bone-bound $v \sim M^{0.025}$
and residual $v/v_{\text{ceiling}} \sim M^{-0.14}$. The "half the
stress exponent" and "square root of the safety-factor deficit"
phrases now sit alongside the mechanical step that produces them.
A reader who wanted to audit the $-0.14$ figure previously had to
supply the connecting argument; that gap is now closed. Bone stress
receives the same derivational treatment as fatigue and tendon
compliance, addressing the concern about consistency of depth.

**Concern 2 (tendon-compliance compatibility with $-0.5$ more
tentative than fatigue's).** Addressed. The revised §5 summary
paragraph now names the epistemic asymmetry directly: fatigue's
compatibility with $-0.5$ is grounded in an empirically fit
parameter; tendon-compliance's requires unspecified elaboration
about mass-scaling of tendon properties; bone-stress's requires a
revision of standard safety-factor onset estimates. The Conclusion
paragraph is updated to the same effect. This was a fair concern -
the revision that added derivations for all three mechanisms made
the tendon-compliance elaboration's under-specification more
conspicuous. Naming the asymmetry openly is honester than papering
over it.

### Response to William James

**Concern 1 (gap between response claim and draft text on
small-mass nuancing).** Addressed. §6 now qualifies the "permissive
rather than binding" claim explicitly: the mechanical ceiling is
"permissive rather than binding through the intermediate and
large-mass range where the descent above cheetah scale carries the
substance," and the small-mass side is named as "another matter."
The prior revision had made the substantive concession about
small-mass non-monotonicity in §3 but had left §6's "throughout the
mass range" language unqualified; the tension James identified was
real. It is now removed. James's own suggested language for the
small-mass caveat - a single sentence acknowledging that its
constraint lies outside the present piece's scope - is adopted
almost verbatim.

**Concern 2 (Hirt et al.'s published fit versus observed residuals
not compared).** Partially addressed. I have added a sentence in
the fatigue paragraph noting that Hirt et al.'s fit is calibrated
to the same observed speeds this piece treats as data, and
therefore reproduces the observation by construction. What the
present analysis distinguishes is not fit quality but which ceiling
binds where - Hirt et al. use a morphological ceiling and let a
fatigue term supply the peak; this piece identifies a distinct
muscle-mechanical ceiling that is loose throughout the mass range
where the pattern lives. I did not add a direct numerical overlay
of Hirt et al.'s fitted curve against the residuals in the §3
table, because doing so requires resolving what their $v_{\text{ceiling}}$
scales as (their published fit uses a species-level morphological
ceiling that does not have a single closed-form mass scaling), and
the exercise would either add a figure I have already chosen not
to include or a paragraph of translation between their ceiling
definition and mine. The one-sentence acknowledgment does the
minimum load-bearing work of clarifying that the residual constraint
is not in tension with their fit.

**Concern 3 (three candidates' current status in recent
literature).** Partially addressed. §5 now opens with a one-sentence
positioning of the three candidates: the set has been stable across
the last two decades; contemporary reviews place fatigue and
elastic-return as the leading active candidates for the peak-speed
constraint at large mammalian mass, with bone stress treated
primarily as a gait-transition and posture constraint rather than
a direct speed limit. I have declined to add specific recent-review
citations because doing so honestly requires either citing a
specific review I am confident is representative or admitting that
the "biomechanics literature since 2015" is a body of work I have
sampled rather than surveyed. Adding named citations of the form
"Meyer-Vernet 2020 places fatigue as the primary candidate" without
having done the survey work would be worse than the neutral
positioning I have adopted.

**Concern 4 (small-mass constraint regime deserves a hypothesis).**
Declined with reasoning. James's own review offers the language
that resolves the tension - one sentence naming that small animals
may operate under a distinct constraint whose specification lies
outside the present piece's scope. I have adopted that sentence in
§6. Producing a hypothesis for the small-mass constraint proper
would require analysis of a different kind - the mouse and squirrel
ratios point to reasons that are not size-per-se (both are near
the ceiling in terms of $\tau$ and $L$ scaling but their observed
speeds are well below what the ceiling would permit), and the hare
and fox ratios point to something ecology-dependent (both are
running at close to their morphological ceiling, perhaps because
predation pressure favors matching the ceiling more closely than
mice or squirrels experience). But hypothesizing without evidence
would be worse than declining. The piece's scope is the large-mass
descent, which is where the residual has a well-defined shape and
where the muscle-mechanical vocabulary can be cleanly diagnosed as
non-binding.

**Concern 5 (biological interpretation of why $-0.5$ specifically).**
Addressed. §5 now names the residual log-slope's specificity as
information about mechanism: each candidate carries a distinct
biological quantity through the residual - fatigue an
anaerobic-capacity-versus-acceleration-time balance, bone stress a
material-limit-versus-applied-stress ratio, tendon compliance a
stored-versus-required kinetic-energy ratio - and each quantity has
its own mass-scaling. The observed value $-0.5$ is the fingerprint
of a mechanism whose relevant biological quantity scales roughly as
$M^{1/2}$ in the relevant regime. This is a paragraph of framing
rather than a discrimination test, but James's concern was
precisely that the piece had not framed the residual shape as
mechanism-selecting. That framing is now explicit.

### Overall

The three biggest substantive changes in this revision:

1. The arithmetic error in the elephant sensitivity column is
   fixed.
2. The tendon-compliance derivation is corrected - the naive
   prediction is $-0.32$, not "roughly flat." Tendon-compliance is
   now the closest naive candidate to $-0.5$ among the three,
   though it still requires elaboration to reach the observed
   value.
3. The epistemic status of the three candidates' compatibility
   with $-0.5$ is now explicitly asymmetric, and the derivations
   for each mechanism sit at consistent depth.

The core diagnostic - no power-law in mass produces the observed
peaked shape; the muscle-mechanical ceiling is permissive rather
than binding at large mass; the residual is a mechanism-neutral
target - is unchanged. The revision leaves the piece a preliminary
that constrains future work rather than a claim to have identified
the binding mechanism.
