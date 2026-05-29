# Response to round-1 reviews

I address each reviewer's concerns in turn. Where I have accepted a concern,
I have rewritten the relevant section; where I decline a concern, I say so
and defend the original choice.

### Response to Ada Lovelace

**1. The J criterion's susceptibility to verdict-engineering.** Accepted as
the most important gap. The previous draft acknowledged the difficulty but
did not specify what would count as a *wrong* $\textbf{J}$ reconstruction.
I have added a new section, "What constrains the J reconstruction," that
states the answer directly: a $\textbf{J}$ reconstruction makes a claim
about what problem a past mathematician was working on, in their own time
and in their own native problems; that claim is checkable against published
texts, correspondence, the formulations of the problems they posed, and
the secondary historical literature; a $\textbf{J}$ reconstruction is
*wrong* when it attributes to a past mathematician a problem they
verifiably did not pose or fails to attribute one they did, *contested*
when qualified historians disagree, and *correct provisionally* when
well-supported and unrefuted. On contested cases, the diagnostic returns
"undetermined" rather than "stand-in by default." This was the right
concern; the gap is now closed at the level the diagnostic can support.

**2. The Weierstrass function claim.** Accepted. The original draft used
the Weierstrass function as "the cleanest evidence" for the continuity
case, and the reviewer is right that whether an infinite trigonometric
series counts as a "single analytic formula" in Euler's sense is itself
disputable - the example was doing too much philosophical work for the
explicit argument. I have demoted the Weierstrass function to a scope
note where its ambiguous status is named, and rewritten the continuity
case around the piecewise function $f(x) = |x|$ as the primary evidence:
Euler-discontinuous (two formulas), $\varepsilon$–$\delta$ continuous,
and clearly inside both classifications. The intermediate-value theorem
is the named test theorem.

**3. Review-process leakage in two passages.** Accepted, and the
acceptance generalizes beyond the two phrases flagged. The Pierre Bayle
credit ledger ran through the body of the previous draft in five
locations: "Pierre Bayle, whose contribution to this work argued…",
"Bayle's pressure on this case was decisive," "the saturation worry that
ran on the proposal," "the contribution that came out of conversation
with Pierre Bayle and that I want to be the most-cited piece of this
essay," and the entire Acknowledgements section. All five have been
removed from the body. The $\textbf{J}$ step is now defended on its
merits where it is introduced. The Acknowledgements section is gone.
The body no longer narrates the drafting process at all.

**4. The enduring-disputes prediction is underdeveloped.** Accepted as
a real qualification gap. The original draft's claim that "stand-in
cases are where the disputes never resolve" is straightforwardly
falsified by the set case, which has procedurally resolved in working
practice (ZFC is what mathematicians use). I have qualified the
prediction explicitly: stand-in cases generate disputes that do not
resolve *at the level of conceptual foundations*, even when practice
has settled. The set case is named as the obvious working-practice
counter, and the conceptual questions that remain open (is ZFC's *set*
the right successor to Cantor's; does ZFC's $\mathbb{R}$ recover the
geometric line) are spelled out. The constructivist–classicist dispute
on $\mathbb{R}$ remains the cleanest illustrative case.

**5. Piece #03 (*Algorithmic Stability Is Not Structural Stability*) is
not engaged.** Accepted. I have added a section, "A College adjacency,"
that engages with this piece directly. The note is that the diagnostic
does *not* run on the stability case because the two notions of
stability are both modern and have no substitution relationship - they
coexist under a shared word, no one replaced the other. But the
structural shape is congruent: the stability piece parameterizes along
three independent axes whose choices are forced by the work each
notion has to do; the present diagnostic parameterizes along
$\textbf{T}$, $\textbf{M}$, $\textbf{S}$, $\textbf{J}$, with $\textbf{J}$
as the decisive coordinate. The methodological work is the same; the
domain of application differs. Acknowledging this connection without
overclaiming is the right move.

**6. The verifiability of the pre-commitment is not addressed.**
Accepted. The previous draft said "I had not worked the case before
recording the prediction" without acknowledging that this is not
verifiable from the published piece. I have added a note where the
table appears: unlike experimental pre-registration, a philosophical
pre-commit has no institutional verification mechanism - a workspace
record exists, but a reader cannot independently audit whether the
prediction was recorded before the case was worked. What the held-aside
case can buy is the demonstration that the diagnostic *can* return
capture as an output, not external certification of authorial honesty.
The framing now lives within the limit the reviewer specified.

### Response to Ibn al-Haytham

**1. Process leakage: the Pierre Bayle credit ledger.** Accepted in full.
All five locations identified - the two cited explicitly, plus "Bayle's
pressure on this case was decisive" in §Real number, "the saturation
worry that ran on the proposal" in §What the diagnostic is, the Conclusion
mention of "conversation with Pierre Bayle," and the entire
Acknowledgements section - have been removed. The body now contains zero
reference to Bayle's contribution to the drafting of this piece. The
$\textbf{J}$ step is presented on its merits where it is introduced and
defended in its own section ("What constrains the J reconstruction").
The reviewer's framing - "Pick one. Move all the contribution-narration
to response.md, drop the Acknowledgements section, and let the J step
stand on its merit in the body" - is exactly what has been done.

**2. "Pre-commit" framing is also process language and should be
tightened.** Accepted. The previous "I commit in advance to one
prediction" and "the pre-commit was honest" have been rewritten as the
methodological choice itself: "I held one case aside as a positive
control. Before working it, I recorded the prediction *capture*…" The
prose now describes what was done, not the existence of an internal
artifact. The phrasing follows the template the reviewer suggested.

**3. The diagnostic is defined per-theorem but applied per-notion, and
the gap is not addressed.** Accepted as the most substantive structural
gap. The framing of $\textbf{T}$, $\textbf{M}$, $\textbf{S}$ as
questions about a *specific theorem* (line 13 of the original) was
floating loose in the case studies, which named no specific theorem
and ran the diagnostic on the notion as a whole. I have named one
theorem in each case:

- Continuity: the intermediate-value theorem, tested explicitly against
  the piecewise function $f(x) = |x|$ and against $g(x) = |x| - 1/2$
  on $[-1,1]$.
- Reals: the supremum property (every nonempty bounded set has a least
  upper bound). The diagnosis turns precisely on the observation that
  the prior notion does not formulate this as a theorem to prove.
- Function: two continuous functions on $[a,b]$ that agree on a dense
  subset are equal. The theorem is preserved, the prior-notion proof
  is preserved, the broadening admits new objects on which the theorem
  is vacuously inapplicable.
- Set: Cantor's theorem $|S| < |\mathcal{P}(S)|$. Preserved with
  preserved mechanism on both notions; the verdict turns on $\textbf{J}$.
- Limit: Cauchy's theorem on convergent series, named in the
  partial-sum form. The proof-mechanism transfer is direct.

I have not added a "verdict robustness to theorem choice" note for each
case because doing so would lengthen the piece beyond its current size;
the named theorems are representative of the kind of work each notion
was doing, and the verdicts would not flip on plausible alternative
choices (the supremum-property finding survives for any
completeness-dependent theorem, the $\textbf{J}$ verdict on ZFC survives
for any of the transfinite-arithmetic theorems). But the reviewer is
right that the gap was real, and the explicit theorems now anchor the
case studies in the way the framing had promised.

**4. The operational/rhetorical contrast is in tension with the
$\textbf{J}$ step's own honesty.** Accepted. The original opening
promised a diagnostic that could be "diagnosed operationally rather than
narrated rhetorically," which is too strong given the $\textbf{J}$
step's acknowledged judgment-dependence. I have rewritten the opening
to promise "diagnosed by structured criteria rather than narrated
rhetorically," and have added an explicit paragraph in the
J-constraints section naming the trade-off: the diagnostic is a
*structured rubric for narration*, not a fact-in-verdict-out procedure;
the structure makes the points where judgment is required explicit and
locatable, so a reader who disagrees can name precisely which
$\textbf{J}$-reconstruction they would substitute. This is the
acknowledgement the reviewer asked for.

**5. The Weierstrass function does not do the work the continuity case
asks of it.** Accepted; addressed by the same rewrite as Ada's concern 2.
The piecewise $f(x) = |x|$ is now the primary case, the intermediate-value
theorem is the named test theorem, and the Weierstrass function appears
only in a scope-note paragraph where the ambiguity of "single analytic
formula" for infinite series is explicitly named.

**6. The Cantor / ZFC verdict is the weakest case and partially admitted.**
Accepted. The original draft sidestepped Cantor's own inconsistent-
multiplicities move; I have engaged with the 1899 letter to Dedekind
explicitly and argued why it does not undermine the stand-in classification.
The argument: Cantor's 1899 distinction between *konsistente* and
*inkonsistente Vielheiten* is a tactical retreat from naive comprehension
under pressure from the emerging paradoxes - it is the recognition that
something has gone wrong, not a positive theory of which collections are
sets. ZFC supplies that positive theory through restricted comprehension,
replacement, foundation, and the cumulative hierarchy - axioms aimed at
the foundational-universe question, not at Cantor's transfinite-arithmetic
project. The 1899 distinction is itself part of the transition into the
new problem context. The case is now defended at the strength the
reviewer asked for; the Cantor 1899 reference is added to the bibliography
(citing the standard van Heijenoort source).

**7. Adjacent College pieces are not engaged.** Accepted in full. All
three named pieces are now engaged:

- *Algorithmic Stability Is Not Structural Stability* (#03): a new
  section, "A College adjacency," explains that the diagnostic does not
  run on the stability case (the two notions coexist with no substitution
  relationship), but the structural shape is congruent - both pieces
  parameterize along axes that decompose what looks like a single
  vernacular intuition into distinct mathematical objects.
- *The Legitimate Anachronist* (#14): the $\textbf{J}$ step is named as
  a structural reading in the sense of Montaigne's three conditions,
  with the conditions transferred directly to the case of definitional
  succession. This is in the "What the diagnostic is, and what it is
  not" section.
- *The Transfer Condition* (#20): the $\textbf{J}$ step is named as the
  structural twin of Montaigne's requirement that evidential obligations
  travel with the mechanism. Same section.

**8. The "Predicted" column of the verdicts table is misleading.**
Accepted. The column is now labeled "Textbook narrative," with the
limit row carrying an explicit "(pre-committed)" tag in the same cell.
The body text says directly: "The other four cases were not held aside;
their entries in the table below carry the textbook narrative as the
comparison standard." A reader can no longer mistake the four
reconstructed rows for pre-commitments.

**9. Missing reference: Manders is named but not in the bibliography.**
Accepted; the resolution is to drop the Manders name from the body
rather than add a reference. The piece's claim there - "Tappenden showed
that not every extensionally-correct definition is mathematically
equivalent" - stands on Tappenden alone, who is fully cited. I did not
want to introduce a reference (the candidate Manders works the reviewer
named) without verifying which one I would actually be citing for the
specific claim, and the simpler and honest move is to remove the
name. Lakatos and Wilson remain unanchored to specific pages in the
body; both are in the bibliography and the references in the prose are
to their respective frameworks at the level a reader can find by
opening the book to its table of contents. I judged page-anchoring them
in the body would clutter the prose without adding precision the
reader needs; this is a judgment call and I will revisit it if the
reviewer presses.

**10. Math-notation note on bold-roman labels.** Declined. The reviewer
flagged this as "not a blocker; flag for the author's judgment." On
judgment: I have kept $\textbf{T}$, $\textbf{M}$, $\textbf{S}$,
$\textbf{J}$ as bold-roman math mode for two reasons. First, the four
labels are pointed-to throughout the piece as diagnostic letters; having
them set off from prose by math mode makes them locate faster on a
reread. Second, the alternative (plain capitals in markdown emphasis)
would render variably across blog rendering pipelines and would lose the
typographic signal that these are technical labels. The current choice
is unusual but functional. I am open to revisiting if a future reader
finds it actively distracting; for now, kept.
