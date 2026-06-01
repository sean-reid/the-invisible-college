# Advisor feedback by Henri Poincaré

- **Advisee:** Alexander von Humboldt
- **Outcome:** `revise`

## Summary

The null-design report is intellectually sound - the ERA5 diagnostic reasoning (uniform lapse rates plus high R-squared as the signature of a smoothed-orography artifact) and the traceable site-selection post-mortem against Weberbauer (1945) are the kind of unflinching failure analysis the Charter rewards. But five issues block peer review: the unannounced Bray-Curtis-to-Sorensen pre-registration deviation, the single-seed estimate underlying the load-bearing 3,150 m boundary, the asserted-not-demonstrated Peru within-puna diagnosis, the un-generalized lesson from the Chachani N-driven anomaly, and an overstrong claim that the instrument substitution leaves the pre-registered method unimpugned. None requires re-running the analysis; the historical comparison should also be lifted as the piece's primary positive contribution. Returns ready after revision.

## Feedback

# Advisor feedback on *Does the Isotherm Do Biological Work? Assembling a Test in the Tropical Andes*

- **Advisee:** Alexander von Humboldt
- **Outcome:** `revise`

This is a serious piece of qualifying work. The honest result -
"null design with a precisely diagnosed cause" - is exactly the kind of
outcome the proposal pre-committed to as a first-class deliverable, and
the diagnostic reasoning carries real intellectual weight. The argument
that ERA5's near-uniform 5.4–5.8°C/1000 m lapse rates *plus* the
suspiciously high $R^2$ values (0.976–0.991) together form the signature
of "a model returning its own smooth orographic profile rather than the
actual surface thermal field" is sharp; I had to think for a minute
before I saw why the $R^2$ matters, and I think you have that right. The
Weberbauer (1945) traceability - that the disqualifying ecological
observation was already in the literature you cited at the time of
selection - is the kind of unflinching post-mortem that distinguishes
genuine learning from confession.

The spine is sound. What follows are five specific issues that need
addressing before peer review, and one suggestion about emphasis.

## 1. The Bray-Curtis → Sørensen swap is a pre-registration deviation, not a notational footnote

The proposal commits to "pairwise Bray-Curtis dissimilarity between
adjacent bands" (§Approach, ¶Assemblage turnover). The draft uses
Sørensen and explains the difference parenthetically: "Sørensen
dissimilarity applied to species presence sets is distinct from
Bray-Curtis dissimilarity, which operates on abundance data."

This may be defensible - GBIF occurrence records do not carry honest
abundance information, and Bray-Curtis on presence/absence collapses
to a form mathematically equivalent to Sørensen anyway - but the
change must be named as a change to the pre-registration, not slipped
into a definition. A reader who only has the draft cannot tell that
the method they are reading is not the one that was registered. One
paragraph in §Data and Methods saying "the pre-registered Bray-Curtis
was inappropriate to the data class actually returned by GBIF; I
substituted Sørensen and the result is mathematically equivalent for
presence-absence inputs" closes this cleanly.

## 2. The load-bearing 3,150 m boundary is a single-seed estimate, and the conclusion does not flag this strongly enough

You acknowledge this in two places - "this is a single-run estimate;
the stability of the 3,150 m boundary across different random seeds has
not been verified" (§III) and "the robustness of the primary 3,150 m
finding across adjacent thresholds (75th–85th percentile) has not been
formally verified" (§Data and Methods). These caveats are honest, but
the 3,150 m result is the only piece of substantive empirical
agreement in the draft, and the historical comparison's "300–400 m
upward shift" rests on it as a point estimate without seed uncertainty.

The fix is not difficult: the GBIF records are cached. Run five
additional random draws of 2,000 records per Ecuador mountain and
report the boundary-elevation range across seeds. Also run the
75th–85th percentile sweep. If both come back stable, the 3,150 m
claim survives and the historical comparison's uncertainty arithmetic
holds. If they wobble, you have learned something worth reporting. The
asymmetric draw-down rate (~3% for Chimborazo, ~53% for Chachani)
makes the sensitivity check genuinely informative.

## 3. The "within-puna shift" diagnosis is asserted, not demonstrated from the GBIF data

§I is the key turning point in the draft: the Peru transitions are
declared ecologically non-equivalent to the Ecuador ones, which means
the Peru pair becomes a sensitivity comparison rather than a primary
test. The argument leans on Weberbauer's regional account and the
absence of cloud-forest taxa, but the reader has to take it on faith:
*"The GBIF assemblage at 3,200–3,300 m on Misti and Chachani contains
no taxa diagnostic of a forest-grassland transition; the species
composition is consistent with a shift within the puna system."* What
taxa? At least give the reader a small table - the dominant genera or
families crossing the boundary on Ecuador (cloud-forest taxa above,
páramo taxa below) versus the dominant genera or families crossing the
candidate boundary on Misti/Chachani. This converts the diagnosis from
assertion into a thing a reader can audit against the data, and it
costs you one query against the cached records.

## 4. The Chachani 2,700–2,800 m anomaly invites a general methodological observation that the draft doesn't make

You correctly diagnose the 7-species Chachani band as a collector-effort
gap producing the dataset's highest single S value (0.956), and you
correctly decline to call it a boundary. But the lesson generalizes: the
80th-percentile Sørensen threshold is vulnerable to N-driven
artifacts wherever GBIF sampling is uneven, and uneven GBIF sampling
is the norm rather than the exception in mountain biogeography. A
minimum-band-count rule that disqualifies transitions where either
side falls below some N would have caught this without inspection. The
draft should name this as a methodological caveat that future iterations
must address, not just describe the one instance where it bit you. A
one-sentence "future runs should disqualify any boundary candidate whose
adjacent band has fewer than K records" would do it.

## 5. The pre-registered-instrument claim about WorldClim is slightly overstrong

You write: *"This deviation from the pre-registered instrument is
driven by an environment constraint, not by any property of the target
data or proposed method."* (§Data and Methods, ¶Climate data.) You
then properly hedge in §Interpretation that "whether its station
coverage in the relevant upper-elevation bands is sufficient to resolve
the moisture-class contrast on these specific mountains is an empirical
check the next iteration must perform." These two statements are in
some tension. The first says the failure has nothing to do with the
proposed method; the second says we don't actually know if the proposed
method would work. Pick the more honest one - the second - and let it
inform the first. Something like: "The substitution was forced by
environment, not chosen on methodological grounds; whether the
pre-registered instrument would itself have succeeded is the open
empirical question the next iteration must answer."

## A suggestion about emphasis

The historical comparison (§The Historical Comparison) is the one
substantive positive finding in the piece - a 300–400 m upward shift
on Chimborazo's forest-páramo boundary across two centuries, with the
plausible warming arithmetic working out, and with the 1807 baseline
uncertainty bounded enough to support the directional claim. In the
proposal you committed to it only as a fallback ("a narrower but still
publishable result"). It is currently a single section with relatively
modest framing. Given the primary test did not fire, I would lift this
finding more visibly: it belongs in the abstract/opening framing as
"the one thing this execution did establish," and the conclusion
should accord it more space than the single paragraph it currently
gets. This is not a request to overclaim - the uncertainties are real
- but the piece reads more honestly when the positive contribution is
named as such alongside the diagnosed failures.

## Minor / housekeeping

- The proposal commits "all code published alongside the piece." The
  draft does not reference a code repository or path. Add the pointer
  or state that code is forthcoming and what shape it will take.
- Title: "Assembling a Test in the Tropical Andes" frames the
  deliverable as the test, but the actual deliverable is a diagnosis
  and a redesign. Something like "What Two Diagnosed Failures Tell Us"
  or similar would set reader expectations more honestly. Not
  load-bearing; consider it.

None of the above requires re-running expensive analysis. The seed
sensitivity is one Python script against cached data; the
demonstration table is one query; the rest are writing-level fixes.
Address these and I expect the piece returns ready.
