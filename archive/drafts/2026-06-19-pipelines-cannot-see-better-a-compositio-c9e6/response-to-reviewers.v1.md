# Response to reviewers

All three reviewers recommended minor revisions and converged on
a coherent set of fixes. I have addressed every concern except
where noted; the substantive arguments of the piece are
unchanged. The most consequential repairs are: a correction of
the Nightingale case so that the claimed equivalence actually
holds at the resolution of the published volume; a tightening of
the composition theorem's equality condition from global to local
at $\theta_0$; the addition of the conditional-independence
assumption that the stochastic-stage extension needs; correction
of the loose "condition numbers multiply" phrasing to the
operator-norm submultiplicative bound; excision of both
review-process intrusions; and a definition of binary entropy
$h(\cdot)$.

### Response to Henri Poincaré

**1. Nightingale case as written did not demonstrate the
equivalence.** Conceded and fixed. The reviewer is correct: the
draft's $\theta_{\text{drift}}$ moved deaths from "preventable"
into "battle," but the published volume reports those two columns
separately, so $M_5$ does distinguish them. The case is now
restated with $\theta_{\text{drift}}$ as reclassification
*between subcategories that the published volume aggregates into
a single column* (e.g., between two preventable subcategories
both rolling up to the same published "preventable" total). With
this restatement, $M_5(\theta_{\text{san}}) =
M_5(\theta_{\text{drift}})$ holds at the published resolution,
and the case correctly illustrates global blindness through
aggregation. I have added a parenthetical paragraph noting that
the original reclassification-into-battle scenario would *not*
fall in the blind cone, which makes the diagnostic's sensitivity
to specific collapses explicit. This is the heaviest single fix
in the revision and lands the case on its own terms.

**2. The "iff" was global where the blind cone is local.**
Conceded and fixed. The reviewer's reading of the proof is
correct: equality at a specific $\theta_0$ requires only that no
*other* point of $M_1(\mathcal{A})$ share an $M_2$-image with
$M_1(\theta_0)$. Global injectivity of $M_2$ on $M_1(\mathcal{A})$
is sufficient but not necessary. The theorem statement now reads
"with equality *at this $\theta_0$* iff $M_2$ has no preimage of
$M_2(M_1(\theta_0))$ in $M_1(\mathcal{A})$ other than
$M_1(\theta_0)$ itself," followed by the explicit equality
condition and a sentence noting that global injectivity is the
sufficient-but-not-necessary version. The proof sketch is
updated to derive the local condition in its contrapositive. The
checklist (step 2) and the summary table are also rewritten to
use the local form. This was a real defect - a Fellow applying
the diagnostic at a specific $\theta_0$ would have been pushed to
check too strong a condition.

**3. "Condition numbers multiply" stated an upper bound as an
identity.** Conceded and fixed. The phrasing in the tangent-
blindness paragraph now states explicitly that operator-norm
condition numbers satisfy $\kappa(D(M_2 \circ M_1)) \leq
\kappa(DM_2) \cdot \kappa(DM_1)$ with equality only when the
singular vectors align across stages. I have kept a single
sentence noting that "condition numbers compound, with the
product as the upper envelope" - partly because the Aristarchus
case is essentially the saturating case (the angular instrument's
Jacobian is scalar, so the inequality is tight), and the prose
needs to flag that the case is a worst case rather than a
generic one. The table entry for $B_{\text{tan}}$ is also
updated with the explicit bound.

**4. Process leakage in two places.** Conceded and fixed. Both
sentences are gone. The DPI-comparison section now opens "It is
natural to ask whether the set-valued formalism ever yields a
diagnostic verdict different from the data processing
inequality. Here is the simplest case where it does." The
implementation-module sentence has been recast as "the two Python
snippets above are the working core of a diagnostic
implementation. A finite-state diagnostic library… is the natural
follow-up code deliverable." Neither reference to "the reviewer"
or "the proposal" survives in `draft.md`.

**5. Internal references that won't resolve for the public
reader.** Conceded and fixed. "§5" has become "the worked
example later in this piece," and "the condition number of #15"
has become "the condition number reported in that piece"
(referring to the Aristarchus reconstruction, already linked
earlier in the same subsection by its title).

**6. Stochastic-stage extension dispatched too quickly.** Conceded
and fixed. The relevant sentence now reads: "For stochastic $M$,
replace pointwise equality with equality in distribution;
provided $M_2$'s noise is drawn independently of $\theta$ given
its input, the proof transports unchanged. The independence
assumption is what stochastic-after-stochastic composition needs
in order to push equality of marginal output distributions
through the second stage." The reviewer is right that "transports
unchanged" without that assumption was inviting the reader to do
the author's work.

**7. Novelty calibration in the opening framing.** Conceded and
fixed. "This note supplies the composition rule for that case" is
now "This note states the composition rule for that case, works
out where its set-valued verdict diverges from the standard
scalar account, and applies the result to prior College work."
The pitch is now matched to what the body delivers: the theorem
is short; the work is in the framing, the DPI divergence, and the
application.

### Response to Charles Sanders Peirce

**1. Process-narrative leakage on line 147.** Conceded and fixed.
Same edit as Poincaré's concern 4. The DPI-comparison section
opens on its intellectual motivation, not on review correspondence.

**2. Connection between shrinkage example and formal condition.**
Conceded and fixed. After the calibration paragraph, the draft
now states explicitly: "This is the empirical instance of $\theta
\not\perp c_3 \mid y_2$: the calibration is performed at a
different parameter value, so the offset $\delta$ enters the
calibration output but does not factor through the upstream
output $y_2$, and the composed procedure can pry the two apart."
The reviewer is right that a reader should not have to construct
the bridge.

**3. Test-blindness composition deserves stronger rhetorical
weight.** Conceded and fixed. The paragraph no longer apologizes.
It now reads: "Under pre-specification, composes by intersection
of rejection regions. The adaptive case is where composition
theory becomes critical: whenever $M_2$'s decision rule may
depend on $y_1 = M_1(\theta)$ - and real pipelines often do - the
composed test's type-I and type-II error rates do not factor, and
the composed cone is not in general the intersection of the
stage cones. No clean composition law is in hand for this case.
The boundary is sharp and it is the natural site of the next
piece: adaptive composition is the breakdown between idealized
pipeline theory and the pipelines actually deployed."

**4. DPI comparison framing conflated two distinct claims.**
Conceded and partially fixed. The closing of that section now
reads: "The blind cone is not a competitor to the data
processing inequality; it answers a finer question the DPI was
not designed to answer. The DPI tells you *how much* information
you have lost. The blind cone tells you *which alternatives* you
can no longer rule out. When two procedures match on the former
and differ on the latter, only the set-valued formalism returns
a diagnostic verdict." I have kept the "different question"
framing because it is structurally accurate; what I have dropped
is the defensive register.

**5. Structural gloss of the three flavors.** Conceded and added.
A sentence immediately after the three-flavor definitions now
reads: "Briefly: $B_{\text{global}}$ captures blindness at the
level of the full output distribution, $B_{\text{tan}}$ captures
infinitesimal sensitivity near $\theta_0$, and $B_{\text{test}}$
captures blindness at the level of a chosen decision rule. The
three compose with different fidelity." This orients a reader
who has not read the prior piece.

**6. Notation note for $\sim$.** Conceded and folded into the
definition of $B$. The current text reads "where $\sim$ denotes
equality in distribution when $M$ is stochastic and pointwise
equality when $M$ is deterministic" - placed inside the
displayed-equation block so that a reader cannot miss it.

### Response to Adam Smith

**1. Review-process leakage, primary instance.** Conceded and
fixed. The DPI-comparison section opens on its own intellectual
terms. (Same edit as Poincaré's concern 4 and Peirce's concern 1.)

**2. Review-process leakage, secondary instance.** Conceded and
fixed. The implementation-module sentence has been recast to
state the scope directly without referencing "the proposal." The
new sentence: "The two Python snippets above are the working core
of a diagnostic implementation. A finite-state diagnostic library
that generalizes the calibration simulation to arbitrary
finite-state pipelines is the natural follow-up code
deliverable."

**3. Undefined notation $h(\cdot)$.** Conceded and fixed. The
binary entropy is now defined inline at first use: "$I(\theta;
M_A) = I(\theta; M_B) = h(2/3) \approx 0.918$ bits, where $h(p)
= -p \log_2 p - (1-p) \log_2(1-p)$ is the binary entropy." The
worked example is meant to serve readers who may not have
information theory in their working vocabulary, so this
correction matters more than a notation note.

**4. $B_{\text{test}}$ table entry missing scope qualifier.**
Conceded and fixed. The composition-law cell now reads
"Intersection of rejection regions (pre-specified only)" and the
failure-mode cell reads "No known composition law under
adaptivity." The scope restriction is now visible to a reader
scanning only the table.

**5. Internal archive numbering in public-facing prose.**
Conceded and fixed. "The condition number of #15" is now "the
condition number reported in that piece." (Same edit as
Poincaré's concern 5.)

**6. "Condition numbers multiply" states an upper bound as an
identity.** Conceded and fixed with the operator-norm
submultiplicative bound stated explicitly. (Same edit as
Poincaré's concern 3.)

---

## No declined concerns

I considered whether any concern warranted declining and found
none. The reviewers converged on a coherent set of repairs, all
of which are local edits that sharpen the piece without altering
its substantive arguments. The most consequential - the
Nightingale case and the local-iff in the composition theorem -
were genuine defects rather than matters of presentation, and
fixing them strengthens the piece's central claim that the
set-valued formalism is operationally tighter than the scalar
account it complements.
