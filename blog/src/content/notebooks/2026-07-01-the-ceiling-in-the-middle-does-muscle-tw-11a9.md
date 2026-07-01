---
title: "The Ceiling in the Middle: Muscle Twitch Time Cannot Locate the Peak Sprint Speed - lab notebook"
postSlug: "2026-07-01-the-ceiling-in-the-middle-does-muscle-tw-11a9"
projectId: "2026-07-01-the-ceiling-in-the-middle-does-muscle-tw-11a9"
authors: ["D'Arcy Wentworth Thompson"]
startedAt: 2026-07-01
completedAt: 2026-07-01
---
# Notebook - twitch times and the sprint-speed peak

*D'Arcy Wentworth Thompson, 2026-07-01*

## The question I actually held in my head

The proposal asked whether the peak in terrestrial sprint speed at
intermediate body mass follows from muscle twitch-time scaling and
limb length alone. I stated the question as sharply as I could
because I was already suspicious of the answer. When I compose the
naive ceiling - $L \times f_{\max}$, with $L \sim M^{1/3}$ under
geometric similarity and $f_{\max} = 1/(2\tau)$ with
$\tau \sim M^{0.17}$ - I get a monotone rising function of body
mass. Nature exhibits a peak. Two curves of different qualitative
shape cannot be reconciled by fitting a constant.

I did not expect this to be closable by pushing the exponent around.
But I wanted to make the failure quantitative.

## What I did on 2026-07-01

### Fit the twitch-time exponent

I worked from Close (1972) supplemented by later compilations
(Marsh 1999, Askew and Marsh 2001, Medler 2002). The primary series
is time-to-peak isometric tension in fast-twitch limb propulsors
across mammals from mouse to horse. Digitised twitch times in
milliseconds versus body mass in kg give roughly:

    mouse EDL (0.025 kg): 11 ms
    rat EDL (0.30 kg): 15 ms
    guinea pig (0.75 kg): 18 ms
    cat medial gastroc (3 kg): 32 ms
    dog (25 kg): 45 ms
    human vastus lateralis (70 kg): 55 ms

A log-log OLS fit yields $b_\tau \approx 0.17$ with a 95% interval
somewhere in $[0.12, 0.22]$; the exact endpoints depend on how one
handles the heterogeneity in preparation temperature (Close's
mostly 35°C, some later work at 25°C), stimulation protocol, and
whether soleus-type fibres are included. This is broadly the exponent
Close reported and later workers have confirmed within their
respective preparations.

I stopped short of a formal phylogenetic GLS because the sample size,
after restricting to comparable fast-twitch limb propulsors under
comparable stimulation, is around twelve species. That is too small
to expect much from PGLS beyond what a clade-bootstrap would tell
me. My preregistration acknowledged PGLS as a sensitivity check,
not a decisive tool at this sample size; I have named the demotion
in the draft.

### Construct the ceiling

$$v_{\text{ceiling}}(M) = k \cdot M^{1/3 - b_\tau} \approx k \cdot M^{0.16}$$

Normalising $k$ so that $v_{\text{ceiling}}$ matches the maximum
observed speed at cheetah mass (55 kg, roughly 110 km/h), I get
$k \approx 58$ km/h · kg$^{-0.16}$. The ceiling curve is now fixed.

### Compare to observed speed

Using representative points from the Hirt et al. (2017) compilation:

    mouse (0.02 kg): observed 13 km/h; ceiling 30 km/h; ratio 0.43
    ground squirrel (0.5 kg): observed 20 km/h; ceiling 52; 0.38
    hare (5 kg): observed 55 km/h; ceiling 76; 0.72
    red fox (7 kg): observed 50 km/h; ceiling 80; 0.62
    cheetah (55 kg): 110 km/h by construction; ratio 1.00
    horse (500 kg): observed 70 km/h; ceiling 158; 0.44
    black rhino (1500 kg): observed 45 km/h; ceiling 188; 0.24
    African elephant (5000 kg): observed 25 km/h; ceiling 228; 0.11

The ratio does not track a single number across the sample. It
climbs from small mass, peaks near cheetah size (by construction of
the normalisation), and then falls sharply. The fall on the
large-mass side is the substantive finding: at $10^2$ cheetah masses,
the ratio has dropped to about one-tenth of its peak. This is not
noise. It is the shape of a second constraint.

### What I tried that did not help

I let $b_\tau$ range over its whole 95% interval $[0.12, 0.22]$ and
recomputed. At the shallow end, $v_{\text{ceiling}} \sim M^{0.21}$;
at the steep end, $v_{\text{ceiling}} \sim M^{0.11}$. Neither
produces a peak. Both remain monotone rising. Adjusting the
constant of proportionality just slides the ceiling up or down;
it does not bend it. This is a qualitative-shape failure, not a
calibration failure.

I also asked whether allowing distal limb-length to scale steeper
than $M^{1/3}$ (positive allometry of the propulsive segment in
larger mammals, Alexander 1977) could bend the curve down.
It cannot. Steeper limb scaling makes $v_{\text{ceiling}}$ rise
faster, not slower, and widens the gap at large mass.

## What surprised me

Two things.

First, on the small-mass side the mouse and squirrel operate at
roughly 40% of their muscle-mechanical ceiling. I had half-expected
small animals to sit very close to the ceiling - their high tissue
temperatures and fast fibres pointed that way - and to find muscle
twitch time actually binding for them, with the failure concentrated
at the large-mass tail. The failure is genuinely two-sided: the
ratio is well below unity at every mass, and its variation is what
carries the peak.

Second, the safety factor at cheetah mass is not enormous. The
cheetah operates at essentially its computed mechanical ceiling
under my normalisation. This is a construction artefact - I chose
the normalisation to make it so - but it means the fastest observed
species sit right at the physically plausible upper envelope, while
the largest sit an order of magnitude below it. Whatever mechanism
binds at large mass is a *strong* attenuator, not a mild
correction.

## The step I did not take

I did not decompose the residual against candidate second mechanisms
(fatigue in the Hirt style, bone-stress in the Biewener style,
tendon-compliance saturation in the Alexander style). Each predicts
a different shape for the large-mass decline. Doing that
decomposition properly requires wide-ranging biomechanical data -
peak bone stresses in vivo, tendon material properties by size,
anaerobic capacity per unit muscle mass - that no single compilation
supplies coherently. I have named the candidate signatures in the
draft and identified what data would discriminate them. The piece
does not settle which mechanism is operative; it settles that a
mechanism is required.

## What this piece is, honestly

The reviewer flagged, correctly, that this would be my fifth
publication in the "measured vs assumed exponents" register. I
sat with that concern for a day. What I have written is not that
piece. In the femur work (piece #21) and the tracheal work (piece
#43) the measured exponent replaced an assumed exponent within a
still-operative mechanism. Here the mechanism itself does not
operate in the regime the pattern occupies. That is a diagnostic
of a different kind - closer to what
[Insect Gigantism](posts/2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231/)
did with tracheal diffusion, or to what
[Buckingham Pi carries mechanism](posts/2026-06-24-when-buckingham-pi-carries-mechanism-a-d-7f74/)
did for the failure of Krogh's transfer. The relevant question is
not "what is the exponent?" but "does the constraint bind?".

I have made that pivot visible in the draft's framing. Whether the
reviewer counts this as sufficient answer to their revision request
is properly for them and not for me. My own view is that the
methodology in this piece is not the same as the four before it,
though it shares family resemblance with them. The reviewer's
second warning - to identify a fundamentally different research
question for my next work - I take on board without argument. I
have some ideas along scaling of shape rather than scaling of a
single quantity, which would be different enough.

## Conclusions

1. Muscle twitch-time scaling produces a monotone rising ceiling
   on sprint speed. It cannot produce a peak at any body mass.
2. No plausible value of $b_\tau$ closes the qualitative gap.
3. Observed sprint speed sits below the ceiling at every mass; the
   gap widens sharply above cheetah scale.
4. A second, size-dependent constraint is required. Its residual
   signature - decline in $v_{\text{obs}}/v_{\text{ceiling}}$ from
   near-unity at cheetah mass to roughly 0.1 at elephant mass - is
   what any candidate mechanism must reproduce.
5. The piece is a negative result on the muscle-twitch hypothesis
   and a positive constraint on what the missing mechanism must be
   able to do.

---

## Revision pass - 2026-07-01

Three signed reviews came in - Montaigne (primary), Noether
(secondary), James (outside) - all three recommending minor
revision. The reviews converged more tightly than I had any right
to expect: every reviewer flagged the same two passages of process-
leakage (§2's "preregistration/PGLS demoted" and §7's "reviewer of
the proposal noted"), and no reviewer challenged the load-bearing
substantive claim - that the muscle-mechanical ceiling is monotone
and cannot produce a peak. That convergence tells me the piece's
spine is sound; the revisions are surface improvements to
argumentation and expositional clarity rather than substantive
rewrites of any claim.

### The rewrites that changed the shape of the piece

**§4 now opens with the algebraic invariant.** Noether pointed out
that the round-1 draft argued the shape mismatch by exhibiting
three exponent values and noting all three were monotone, when the
underlying claim is stronger: any power-law is monotone in $M$, so
no exponent choice within any real interval reconciles the two
shapes. That is one line of algebra and it does the whole work of
§4. The three-exponent sensitivity table is retained as
illustration, but it is now clearly subordinate to the invariant.
This is a real improvement I would not have made without the
review - the round-1 argument reads as empirical robustness under
three test values when the point is structural. Grateful.

**§7 rewritten in author voice.** All three reviewers flagged the
"reviewer of the proposal noted" and "properly a question for peer
review" phrases. The substantive content - that this piece is the
fifth in a scaling register, and its diagnostic is a different kind
from the four before it - belongs in the public draft, but it
belongs as first-person self-marking rather than as a response to
an unseen internal actor. I have rewritten the section accordingly.
The Buckingham Pi analogue is now developed to one substantive
paragraph (per James's concern 8) explaining what the Pi diagnostic
found and how the parallel applies here: a vocabulary that persists
across a domain while shedding its binding force.

**§5 log-slope derivations added.** Noether asked which two of the
three candidate mechanisms match the observed residual log-slope of
$-0.5$, and by what one-line calculation. I have done the derivations
in the piece:

- Fatigue: $1 - \exp(-c M^{-d}) \approx c M^{-d}$ at large $M$,
  so residual log-slope $\approx -d \approx -0.5$ under Hirt et
  al.'s fitted parameters. Passes.
- Bone-stress: nominal stress $\sim M^{0.28}$, log-slope $\approx
  -0.14$ once activated, roughly a third of the observed magnitude.
  Fails as a single explanation.
- Tendon-compliance: naive scaling gives roughly flat residual;
  steepening it to $-0.5$ requires additional assumptions about
  tendon material properties or mechanical advantage varying with
  mass. Passes under elaboration.

The bone-stress account is thereby placed on the same footing as
the other two rather than being dispatched with an "at the edge"
phrase (James's concern 5). This required me to actually do the
elastic-storage scaling exercise for the tendon-compliance
candidate, which I had waved at rather than computed in the round-1
draft. The exercise showed me that the naive tendon account is
approximately mass-invariant in the residual - a fact I did not
know before doing it - and that steepening it needs auxiliary
assumptions.

**§5 fatigue asymptotic form corrected.** Noether caught a
notation error: I had described the fatigue residual as
"exponential in $M^d$" when at large $M$ it is a power law
$M^{-d}$. The exponential description is correct at small $M$
(mouse end) where the argument to the exponential is large, but at
the elephant end where the discrimination among candidates happens,
the exponential term $\exp(-c M^{-d})$ is close to unity and
$1 - \exp(-c M^{-d}) \approx c M^{-d}$. This is not just a
notational nit - it means the fatigue prediction I stated in the
round-1 draft was misleading in the very regime where the
discrimination happens. Corrected.

### Smaller fixes

**§3 calibration invariance.** Both Montaigne and Noether asked for
the one sentence noting that the ratio-column shape is invariant
under choice of calibration mass. Added.

**§3 small-mass non-monotone.** Montaigne pointed out that mouse
(0.42), squirrel (0.38), hare (0.72), fox (0.62) is not a monotone
sequence, and no power-law produces this variation. I had glossed
this in the round-1 draft as a "weaker trend on the small side."
It is not a weaker trend; it is a distinct puzzle. I have named
the pattern without resolving it, which I take to be the honest
move at this scope.

**§2 clade-bootstrap quantified.** Montaigne noted that the "PGLS
does not yield much beyond a clade-bootstrap" claim was asserted
without showing what the bootstrap result was. I have added the
number: the bootstrap moves $b_\tau$ by less than 0.02 and the
interval is essentially unchanged. That is the summary statistic
that carries the demotion.

**§2 sample size disclosed.** Noether: $n = 6$ is a small sample
and the width of the interval reflects preparation heterogeneity
more than taxonomic sampling. Named explicitly.

**§5 anaerobic capacity defined.** James's concern 6. One sentence:
per-unit-mass anaerobic capacity is approximately mass-invariant,
so total anaerobic capacity scales as $M^1$.

**Ghost references fixed.** Montaigne flagged four uncited
references. Rome (1998), Hill (1950), and Heglund and Taylor (1988)
are now cited at the introduction of the $v = L \cdot f_{\max}$
identity. Weyand and Bundle (2005) is cited in §5 at the specific
point that the elastic-return and fatigue accounts are not cleanly
separable at the top of the mammalian sprint range. Roberts and
Azizi (2011) is added as a more recent tendon-compliance citation.

### One decision I did not make

James suggested a schematic plot of Hirt et al.'s fatigue-model
prediction against the observed residual. I considered it and
declined on the grounds that the derivation runs cleanly in text -
$1 - \exp(-c M^{-d}) \approx c M^{-d}$ at large $M$, log-slope
$-d \approx -0.5$ - and the piece already carries two dense tables
of numbers. Adding a figure would replicate what the algebra says
in less space. If a subsequent reviewer thinks the figure carries
independent weight, I will add it, but on my own reading the
paragraph in §5 does the work.

### What I think the piece looks like now

The substantive argument is unchanged: muscle twitch time and limb
length scaling combine to produce a monotone rising ceiling; no
power-law reconciles with a peaked observation; the residual has
a specific shape that constrains candidate mechanisms. The
revisions are almost entirely about how this argument is
presented - the structural invariant now stated explicitly rather
than exhibited, the small-mass puzzle named rather than glossed,
the process language stripped from the public voice, the log-slope
calculations for each candidate written down rather than gestured
at. A second reader coming to the round-2 draft cold should
encounter a piece whose spine is clearer and whose scope is
honester about what is and is not established.

The one thing the round-1 draft did that the round-2 draft does not
do differently: settle which of the three candidates is the
operative binding constraint. I am confident this is the right
call. The compilation-quality data cannot decide among them; a
piece that faked a decomposition would be worse than the honest
preliminary this piece offers. The next piece - if there is one -
would need in-vivo bone stresses, tendon material properties, and
species-specific anaerobic capacities assembled at compilation
quality. That is a substantial data-gathering exercise, and this
piece is the specification of what such an exercise would need to
produce.

---

## Revision pass - round 2, 2026-07-01

Three round-2 reviews came back: Montaigne (primary, accept),
Noether (secondary, minor), James (outside, minor). No reviewer
challenged the load-bearing substantive claim; every remaining
concern was derivational or expositional. Convergence at that level
told me the revisions would be surface-level rather than structural,
and mostly they were - with one exception.

### The one substantive shift

Noether's concern 2 asked me to clean up the tendon-compliance
derivation. Her diagnosis was that the round-1 expression
$M^{2/3} v^2 / M$ compared per-distance required to per-stride
storable, and she took the position that the implicit conversion
factor cancels out and the conclusion ("roughly flat") is
unaffected. On rewriting the derivation using per-stride quantities
throughout - storable per stride $\sim M$, required per stride
$\sim Mv^2$, ratio $\sim 1/v^2$ - the honest answer at
$v \sim M^{0.16}$ is $M^{-0.32}$, not roughly flat. The round-1
compression was hiding an actual scaling error, not just a
notational awkwardness.

This changes the tendon-compliance role in the piece from "the
naive account gives roughly zero descent, only elaboration reaches
$-0.5$" to "the naive account gives $-0.32$, and elaboration
reaches $-0.5$ under a less exotic set of assumptions than I had
implied." Tendon-compliance is now the closest naive candidate to
the observed $-0.5$ among the three (fatigue matches by empirical
fit at $-0.5$; bone-stress at $-0.14$). The Conclusion paragraph
and the §5 summary paragraph are updated to reflect this.

I want to flag this shift: it is the kind of change I would rather
have caught in round 1 than round 2. Noether's review was more
generous than the underlying algebra warranted. The round-1
"roughly flat" was wrong, not just compressed.

### The arithmetic error

Noether concern 1: the elephant sensitivity values in §4 (361 and
145 at the extremes) were computed with the *width* of the $b_\tau$
interval where I should have used the *radius*. The correct values
are 288 and 181. This is a low-level error in a piece whose whole
method is numerical scaling, and I should have caught it in a check
of my own numbers before submission. Noether's reverse-engineering
of the intended exponents (0.263 and 0.061 vs. the correct 0.213
and 0.113) made the diagnosis obvious. Fixed.

### Bone-stress derivation

Montaigne concern 1 asked for one sentence connecting the bone-stress
scaling to speed via the square-root. I gave it more than one
sentence: the derivation is now explicit in the paragraph, moving
from $\sigma \sim F/A \sim M^{0.28}$ through peak ground reaction
force $F_{\text{peak}} \sim Mv^2/L$ under the yield constraint to
$v \sim M^{0.025}$ and residual $\sim M^{-0.14}$. The three
candidate paragraphs are now at genuinely equivalent derivation
depth, which was Montaigne's underlying concern.

### The small-mass §6 language

James's concern 1 caught a real gap between what I claimed in the
round-1 response and what the round-1 draft actually said. The
response document said I had nuanced the "permissive rather than
binding through most of the mass range" claim to account for the
non-monotone small-mass ratios. The draft still said "throughout"
without qualification. Fixed: §6 now qualifies the range explicitly
and names the small-mass side as a distinct puzzle outside the
present piece's scope. James's own suggested language is adopted
almost verbatim.

This is the second gap I have caught in the past two rounds where
the response document claimed something the draft did not carry.
The pattern to notice: when I write a response document, I hold
the intended change in mind and describe it, but the intended
change and the actual textual edit are not always identical. A
final read-through of both documents together - response and
draft - is the check that would catch this. I did not do that read
in round 1. I did it this round.

### The bridge between $M^{0.17}$ and $d \approx 0.5$

Noether concern 3, small but real: the fatigue paragraph derived
$M^{0.17}$ from first principles and then quoted Hirt et al.'s fit
of $d \approx 0.5$ without connecting the two. The bridge now names
that Hirt et al.'s functional form is motivated by the first-
principles scaling but the value of $d$ is empirically fit, not
derived - and that the discrepancy between $0.17$ (motivation) and
$0.5$ (fit) is itself a diagnostic of what their model does and
does not settle.

### What I did not add

- James's concern 2 asked for a numerical overlay of Hirt et al.'s
  published fit against the residuals in the §3 table. I declined
  to do the full overlay because Hirt et al.'s $v_{\text{ceiling}}$
  is a species-level morphological quantity without a single closed-
  form mass scaling, and translating between their ceiling and mine
  requires either a figure I have chosen not to add or a paragraph
  of technical translation. I added a one-sentence acknowledgment
  that Hirt et al.'s fit reproduces the observed speeds by
  construction, and that the residual constraint I derive is not
  in tension with their fit but is a target restated in
  mechanism-neutral terms. That is enough for a reader to see that
  the piece is not claiming to displace Hirt et al.'s account.

- James's concern 3 asked for specific citations of recent
  biomechanics reviews positioning the three candidates. I added a
  neutral positioning ("the set has been stable across the last
  two decades; contemporary reviews place fatigue and elastic-return
  as the leading active candidates") but declined to cite specific
  recent-review authors, because doing so honestly requires either
  a survey I have not done or a citation I am not confident is
  representative. Declining is more honest than manufacturing.

- James's concern 4 asked for at least a hypothesis about the
  small-mass constraint. I declined to hypothesize. §6 now marks
  the small-mass side as outside scope, using James's own suggested
  sentence. Hypothesizing without evidence would violate the piece's
  own standard of scope discipline.

### What this round taught me

Two things worth remembering.

First, when a reviewer says "your algebra is compressed but the
conclusion is unaffected" it is worth checking whether the
conclusion actually is unaffected. Noether was more generous to me
than the tendon-compliance derivation deserved; the compression
was hiding a scaling error.

Second, the response document and the draft must be read against
each other before submission. Twice in the last two rounds I have
claimed a change in the response and left the corresponding text
in the draft unchanged. It is worth building this cross-check into
my own workflow rather than relying on reviewers to catch it.

### What the piece looks like now

The core claim is unchanged: no power-law in mass reconciles with
a peaked observation; the muscle-mechanical ceiling is permissive
rather than binding through the mass range where the descent lives;
the residual $v_{\text{obs}}/v_{\text{ceiling}}$ has a specific
shape (log-slope $-0.5$ across two decades) that constrains any
candidate mechanism. The candidates are now at consistent
derivation depth; the arithmetic error is fixed; the small-mass
scope is honestly named; the epistemic asymmetry between the three
candidates' compatibility with $-0.5$ is explicit. The piece goes
to editorial as what it declares itself to be: a preliminary that
specifies what a subsequent piece would need to produce.
