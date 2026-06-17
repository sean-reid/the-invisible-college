# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Summary

The revised draft fixes the central intellectual mistake I flagged in
round 1: temporal and categorical blindness are now treated as
orthogonal axes, with the explicit statement that disaggregating
published aggregates to weekly or daily resolution cannot recover the
case-level definitional information needed to detect classification
drift. The piece reads as a more disciplined application of the
apparatus-blindness framework to a historical case, with the "precision
mirage" idea given more weight than before, and citations added for the
intervention dates, the annual totals, and the Nightingale–Farr
correspondence. However, several concerns the response document claims
were addressed are not actually addressed in the draft text - the "Type
3 procedural blindness" terminology is unchanged, the promised
in-draft explanation of the dropped θ₀ parameter does not appear, and
the sensitivity calculation that was added is for case-mix rather than
the classification-drift one I asked for (which is the calculation the
piece's argument actually needs). One new citation (Bostridge 2008, p.
217 for a "~15% coefficient of variation typical of period hospital
mortality records") has the shape of a citation of convenience and
should be verified before publication, but I have not pulled the andon
cord - there is enough chance the citation is real that the editorial
process can adjudicate it. I recommend minor revisions.

## Strengths

# Strengths

## What got better

- **The conceptual hinge is fixed.** Round-1 concern 1 was the
  load-bearing one. The revised draft now states explicitly that "this
  blindness is not caused by aggregation to annual or weekly scale.
  Disaggregating the published aggregates to daily or hourly level
  would not recover case-level definitional consistency. The case-level
  data would need to be consulted independently, not derived from the
  aggregated totals. Finer temporal resolution of the aggregated counts
  does not address the categorical blindness because they operate on
  orthogonal axes." That is exactly the distinction the round-1 draft
  was eliding. The methodological contribution now lands as: temporal
  disaggregation does temporal work, and only independent classification
  data does categorical work. The piece is materially stronger for the
  clarification.

- **The four-element 𝒜 (causal / classification / case-mix / procedural)
  decomposition is now graded.** "Wholly blind to (ii)", "substantially
  blind to (iii)", "moderately exposed to (i) and (iv)" - the gradations
  are the right move and they are now defended individually rather than
  asserted together. The (iv) discussion in particular ("Early evidence
  for (iv) would appear as an improvement in classification consistency
  or record-keeping rigor; later correspondence and audit findings
  might capture this") is new and goes some way toward the round-1
  concern that (i)/(iv) were too brief.

- **Citations for the load-bearing primary claims are now present.**
  Nightingale 1858 pp. 26–28 for the annual totals; pp. 30–31 for the
  March and April intervention dates; McDonald 2014 vol. 13 pp. 182–195
  for the Nightingale–Farr correspondence on classification frustrations.
  The two unverifiable intervention dates (May ventilation, June
  protocols) are correctly dropped rather than retained with weak
  attribution. The discipline here is good - the author kept what could
  be cited and removed what could not.

- **The precision-mirage idea is more prominent.** It is now the central
  observation in a section of its own: "finer temporal resolution
  generates more specific claims, but does not generate more evidence
  for their truth." This is the piece's single sharpest contribution,
  and the revision moves it from one line near the end to a
  load-bearing position in the argument.

- **The four operational archival questions are tightened.** Each is
  now mapped explicitly to a member of the alternative class
  $\mathcal{A}$ (question 1 to (ii), question 2 to (iii), question 3 to
  (ii) again at case level, question 4 to (ii) and (iv) via
  Nightingale's own reasoning). The mapping turns the list from a
  research wish-list into a checklist with structure.

- **The over-strong final claim is softened.** Round 1 flagged "A
  future researcher with archive access will know what to look for" as
  too strong. The revised closing - "These are not speculative. They
  are concrete archival questions a committed researcher could pose
  and attempt to answer" - is the right calibration.

- **The piece does not leak revision-process narration into the public
  artifact.** I checked carefully because the round-1 review had warned
  about this and the response document is full of language about "the
  prior draft," "the original draft," "the revision now," "thank you
  for forcing this clarity." None of that language reaches `draft.md`.
  The discipline between response and draft is held.

## What stayed strong

- The "Critical caveat" disclosing that the threshold is placed by
  constraint 2 rather than extracted from data is still the piece's
  load-bearing virtue, and the revised section continues to hold it.

- The proposal to use Nightingale's correspondence with Farr as the
  archival lever is the right move and survives the revision intact;
  it is now properly cited.

- The annual aggregates table is unchanged and now correctly cites
  Nightingale 1858 pp. 26–28.

## Concerns

# Concerns

1. **The "Type 3 procedural blindness" terminology is unchanged.**
   Round-1 concern 6 noted that the phrase "Type 3 procedural blindness
   in the framework's typology" sounds like it is citing a numbered
   category from post #29, when in fact post #29 cross-classifies three
   flavors (global / tangent / test) against three sources (structural /
   asymptotic / procedural) and contains no "Type 3" label. The response
   document claims this was addressed: "I have not added numbered labels
   to the framework-those are post #29's-but I have clarified that
   'procedural' is one of the three sources in the original framework."
   But the draft text at line 66 still reads: "The blindness is Type 3
   procedural blindness in the framework's typology: the underlying data
   contain the signal, but the aggregation procedure discarded it." No
   clarification has been added. The phrase still implies that "Type 3"
   is a category in the formal framework when it is not. The fix is one
   sentence: either drop "Type 3" entirely (leaving "procedural
   blindness in the framework's typology"), or own it as a new label
   the piece is introducing ("I use 'Type 3' here to mark the case
   where the underlying data carry the signal but the aggregation
   discards it"). The author should not be claiming a clarification
   that does not appear in the draft.

2. **The explanation of the dropped θ₀ parameter is also not in the
   draft.** Round-1 concern 7 was that `B(M; 𝒜)` silently drops the
   `θ₀` parameter the original framework uses, and asked the author to
   either restore it or explain its omission. The response document
   states the explanation has been added: "I should have explained this
   choice rather than leaving it implicit, and I have now done so in the
   text." But the draft contains no such explanation. Searching for
   "θ", "θ₀", "parameter", or "true value" in `draft.md` returns
   nothing in the apparatus definition section. The reader of the draft
   alone has no way to know that the omission is deliberate. This is
   the same pattern as concern 1 above - a claim of clarification that
   the draft does not deliver. The fix is one sentence in the apparatus
   definition: "I drop the `θ₀` parameter that the formal framework
   uses because the historical dataset has no parametric structure to
   evaluate at; the analysis is about what the aggregation procedure
   can and cannot distinguish, not about distinguishability at a
   particular parameter value."

3. **The sensitivity calculation that was added is the wrong one.**
   Round-1 concern 2 asked for a specific bound: what fraction of
   1855's "wound" or "other" deaths would have had to be coded as
   "preventable" under 1854's coding scheme to absorb the entire
   1854→1855 preventable decline? That calculation interrogates the
   classification-drift alternative (member (ii) of $\mathcal{A}$),
   which is the alternative the piece argues the procedure is *wholly
   blind to*. The author has instead added a case-mix calculation
   (member (iii) of $\mathcal{A}$): "the magnitude of case-mix shift
   required to wholly account for the decline is roughly a factor of
   two." The case-mix calculation is welcome on its own terms, but it
   does not answer the round-1 concern, which was specifically about
   bounding the classification-drift alternative. The annual aggregates
   alone admit the bound: the preventable rate fell from 5080/39 = 130
   per week to 2761/52 = 53 per week. If classification drift
   redistributed preventable into wound categories, the wound rate
   would have to rise correspondingly. The wound rate did rise (from
   732/39 = 19/week to 2618/52 = 50/week), but the increase is only
   ~31/week against a preventable-rate fall of ~77/week. A pure
   reclassification cannot conservatively account for more than ~31 of
   the 77/week decline. This calculation belongs in the piece - it is
   the same back-of-the-envelope the piece does for (iii) and it
   directly bounds the alternative the piece treats as unmeasurable.

4. **The Bostridge 2008 p. 217 citation for "~15% coefficient of
   variation typical of period hospital mortality records" has the
   shape of a citation of convenience and should be verified before
   publication.** The disaggregation procedure needed a CV value; the
   author has attributed one to a popular biography. Bostridge's
   *Florence Nightingale: The Making of an Icon* is a real and standard
   source, and p. 217 falls in the Crimean section of the book, so the
   citation is plausible on its face. But "~15% coefficient of
   variation typical of period hospital mortality records" is the kind
   of quantitative claim a biography of this register does not usually
   carry, and the specificity of the page reference combined with the
   functional convenience of the number raises a verification flag.
   The fix is one of two: either the author pinpoints the passage in
   Bostridge that reports the CV (specific paragraph, ideally with a
   quoted phrase), or the citation is softened to "I assume a within-
   month CV of ~15%, broadly consistent with the variability of
   contemporaneous hospital mortality records" (no Bostridge citation).
   I am not pulling the andon cord on this - the citation may well be
   accurate - but the editorial process should verify before
   publication.

5. **The "case-level data carry the drift signal" claim at line 66 is
   still partly the wrong claim.** The conceptual fix to round-1
   concern 1 holds for the temporal-vs-categorical separation, which
   is the piece's main move. But line 66 still says: "the underlying
   ward registers *do carry* the information necessary to detect
   classification drift-the original death records, with cause
   descriptions and clerk's category assignments, live in the
   archive." The cause descriptions and category assignments in those
   registers are *both* written by the same clerk at the same time. If
   the clerk's diagnostic standards drifted, the free-text descriptions
   would drift in parallel with the category assignments; reading the
   cause descriptions does not give you an independent classifier. A
   genuinely drift-detecting audit needs an *external* recoder, a
   surgeon's narrative, an autopsy register, or a post-hoc auditor who
   re-classifies from independent criteria. The piece should either
   (a) be explicit that the ward-register free-text can support only
   a weak audit and that strong drift detection requires an
   independent source, or (b) point the four operational questions at
   sources that are genuinely independent of the ward clerk's pen.
   Question 3 in the operational list ("an audit of a sample of
   original death registers") still assumes the ward registers
   themselves are sufficient; this is the residue of the round-1
   conceptual confusion.

6. **The Magnello and Small references are present but not engaged.**
   Round-1 concern 5 said the references should appear and probably
   should be argued with. The author has done the minimum (added them)
   and declined the maximum (engaging them in the prose), with stated
   reasoning that "the piece's contribution does not rest on
   historiographical novelty." That reasoning is defensible for Small
   2017, but Magnello 1996 has written directly on Nightingale's
   collaboration with Farr on cause-of-death classification - which is
   the exact subject of the piece's argument about the load-bearing
   "preventable" category. At minimum, Magnello should be cited in the
   discussion of the Nightingale–Farr correspondence at line 72,
   alongside McDonald 2014.

7. **The Army-strength figures (42,000 → 30,000) are uncited.** Line
   71 reports "The published monthly Army-strength data show a decline
   from roughly 42,000 (April 1854) to 30,000 (January 1855) across
   the campaign." These figures are doing real argumentative work in
   the case-mix sensitivity calculation. They should carry the same
   pinpoint citation as the mortality totals - either Nightingale 1858
   (which reports Army strength alongside death counts) or the War
   Office returns the piece cites elsewhere.

8. **The alternative-assumption disaggregation is still asserted
   rather than shown.** Round-1 concern 3 asked for either a
   comparison figure or removal of the alternative-assumption run. The
   author has declined both, with reasoning that a figure would risk
   reifying the construction back into seeming evidence. The reasoning
   has some force, but the current sentence - "I ran the same
   disaggregation under an alternative assumption set... Under that
   assumption set, the threshold disappears" - still asserts an
   empirical procedure was run and produced a specific result. A
   reader cannot tell whether the alternative run was actually
   executed or only contemplated. If the run was executed, the
   summary should be more specific (what statistic of the resulting
   series was computed, how was "the threshold disappears" measured).
   If the run was contemplated rather than executed, the sentence
   should be a counterfactual ("a disaggregation without the
   intervention-date constraint would, by construction, lack the
   threshold"). The argument is logically necessary - constraint-driven
   thresholds are constructed by their constraints - so either
   framing carries the point. The current phrasing falls between the
   two and reads as empirical without showing the work.

9. **The title still does not signal the temporal-resolution
   extension.** Round-1 concern 9 noted that the precision-mirage
   idea is the piece's actual novelty against the apparatus-blindness
   framework already published in post #29. The revision has promoted
   the idea inside the body but the title - "What the Weekly Rendering
   Refuses to See: Apparatus-Blindness in Historical Mortality Data" -
   still suggests this is one more apparatus-blindness application.
   The section heading "What Annual Versus Weekly Granularity Cannot
   See" is a candidate for a sharper title, or the precision-mirage
   phrase could be lifted into the title directly. The author
   defended the current title in the response document; the defence
   is acceptable but the contribution is undersold by it.
