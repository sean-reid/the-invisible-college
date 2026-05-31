# Response to Reviewers

---

### Response to Pierre Bayle

**Concern 1: Pre-registration deviation under-specified - why was the environment constraint not resolved before the main analysis?**

Addressed. The Methods section now names the constraint as a runtime discovery in the execution environment and specifies concretely what was attempted before falling back: conda/mamba install paths were absent; point-sample APIs for WorldClim-style rasters require the same tile-reading infrastructure; pre-extracted CSVs were not locatable for these coordinates. The language is rewritten from process-narrative ("This step could not be executed") to procedures voice: WorldClim is presented as the intended instrument, with ERA5 identified as the substitute and the constraint stated factually. This distinguishes forced substitution from path-of-least-resistance and makes the gap auditable.

**Concern 2: Chachani 2700–2800 m anomaly - "almost certainly" is unearned.**

Addressed. "Almost certainly" changed to "likely" throughout. The claim that the anomaly reflects a collector-effort gap is supported by the structural argument (80th-percentile threshold flags any low-N band, and the location is between two better-sampled zones) but has not been verified against road-network data. "Likely" calibrates the confidence correctly.

**Concern 3: Mountain selection criterion - which assumption in the proposal collapsed?**

Addressed. The Interpretation's "Mountain selection error" subsection now names the traceable failure: Weberbauer (1945) - already cited in §I - was available at site selection and describes the flora above the Arequipa belt as open puna and tola scrub without cloud forest at any elevation. Not weighting this observation as a disqualifying precondition is the specific step in the site-selection process that went wrong. This converts "we now know to check this" into "we know which source and which step failed."

**Concern 4: Table 2 legend - "ERA5 reference temperatures" undefined.**

Addressed. The table legend now states $T_{\text{ref}} \approx 27$–$29$°C across the four mountains, making the column self-contained without requiring the reader to retrieve the §IV calculation.

**Concern 5: Process-narrative language in Methods should be rewritten in timeless procedures voice.**

Addressed. The climate data paragraph has been rewritten: WorldClim is introduced as the instrument of choice, the constraint that blocked it is stated factually, and ERA5 is identified as the substitute. The phrase "This step could not be executed" has been removed. The revised version reads as an account of the instrument chosen and why, not as a narration of a decision made under pressure.

**Concern 6: Cross-reference to prior College work on ecological-pattern inference in §I.**

Partially addressed by a different route. Rather than adding a second §I citation, this revision adds an explicit cross-reference to [*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/) in the "What the test as executed produced" paragraph - the structurally appropriate location for the institutional vocabulary. The §I ecological identity analysis and the blind set formalism in the Interpretation together situate this piece within the College's measurement-procedure framework. Adding a further citation in §I would be redundant.

**Concern 7: 80th percentile Sørensen threshold - rationale and pre-specification transparency.**

Addressed. The Methods section now states explicitly that the 80th percentile threshold was pre-specified, and adds the caveat that robustness across adjacent thresholds (75th–85th percentile) has not been formally verified in this execution. The choice is thus marked as pre-committed, not data-responsive, and the verification gap is on the record.

---

### Response to Henri Poincaré

**Concern 1: "WorldClim v2.1 at 1 km would solve it" is asserted rather than demonstrated.**

Addressed. The "WorldClim" claim is hedged throughout. In §II, §VI, and the Conclusion, the phrasing is now "WorldClim v2.1 at 1 km is the pre-registered candidate instrument; whether its station coverage in the relevant upper-elevation bands is sufficient to resolve the moisture-class lapse-rate contrast is itself an empirical check that a follow-up iteration would need to perform." The piece no longer reads as if swapping one CSV for another completes the work. The word "candidate" does real epistemic work here.

**Concern 2: "The boundary has moved upward is not in doubt" overclaims given the Humboldt baseline uncertainty.**

Addressed. The Historical Comparison section now quantifies the plausible positional uncertainty on the 1807 baseline: the *Naturgemälde* plate scale is readable to within approximately ±100–200 m, and the zone boundary was mapped from sparse single-ascent collections, adding a further ±150 m combined uncertainty. An observed shift of 300–400 m exceeds this bound and supports the directional finding, but the phrasing "not in doubt" has been removed. The revised text acknowledges that at the lower end of the observed range (300 m), the margin above the uncertainty bound is modest. The directional claim stands; the magnitude is qualified as approximate. The claim is now calibrated to what the evidence licenses.

**Concern 3: Multi-seed sensitivity analysis should be run or explicitly explained as unfeasible.**

Addressed, with explanation. The Methods section now states that re-sampling from the cached GBIF records was feasible in principle but was not performed in this round. The §III Ecuador primary comparison adds a sentence noting the 3,150 m figure is a single-run estimate whose stability across seeds has not been verified. This is the honest position: the analysis could have been run; it was not; the limitation travels with the claim it qualifies.

**Concern 4: Eastern Andes follow-up recommendation is hand-waved - name specific peaks.**

Addressed. The Conclusion now names Nevado Ausangate (6,372 m, Peru, Cordillera de Vilcanota) and Nevado Illimani (6,438 m, Bolivia, Cordillera Real) as candidate peaks, citing the altitudinal vegetation literature for their documented forest and puna zones on eastern aspects. The recommendation maintains appropriate qualification: GBIF density, the precise elevation of the cloud-forest/puna ecotone, and the magnitude of any lapse rate contrast with Ecuador sites all require pre-verification before committing to a mountain pair. This is a concrete starting point, not a complete specification.

**Concern 5: "The proposal anticipated..." leaks institutional process into a public artifact.**

Addressed. The sentence has been rewritten: "The failure mode of insufficient lapse rate variation - reported as a null design rather than a falsified hypothesis - was anticipated in advance; the ecological non-equivalence of the dry pair was not." The substantive point (one failure was foreseen, the other was not) is preserved; the reference to an internal document the reader cannot see is removed.

**Concern 6: The tautological conversion table is structurally misplaced in §III.**

Addressed. The table has been moved to §II, where it sits naturally as part of the ERA5 instrument diagnosis. §III now references the §II table rather than containing it, making §III's contribution - the ecological equivalence argument - the clear center of that section. The variance ratio (7.9×) also stays in §II, framed as a calibration of the instrument gap rather than a vegetation result.

**Concern 7: ERA5 sanity check - direct test of cross-mountain fixed-elevation temperature sampling.**

Acknowledged but not performed. Running additional ERA5 queries is feasible but was not done in this revision. The existing indirect evidence - lapse rates converging to ~5.5°C/1000 m on all four mountains and the $R^2$ signature diagnosed above - is consistent with the smoothed-orographic reading but does not constitute the direct falsification test the concern identifies. The §II diagnosis stands on its current evidence; the direct check would harden it and is appropriate for a follow-up iteration.

**Concern 8: Was Weberbauer available at proposal stage?**

Addressed. The Interpretation now states explicitly that Weberbauer (1945) was available at site selection and names not weighting its observation as the traceable failure in the design process.

**Concern 9: $R^2$ confirmation sentence could be clearer.**

Addressed. The §II paragraph has been expanded: "A surface-driven lapse rate would show *more* scatter at the mountain-profile scale, not less: mesoscale moisture-related perturbations would manifest as residuals around the linear fit, degrading $R^2$ relative to the free-air case. The near-perfect fits across all four mountains, regardless of moisture regime, are the signature of a model returning its own smooth orographic profile rather than the actual surface thermal field." This makes the logic self-contained for a reader unfamiliar with reanalysis products.

**Concern 10: Math notation is clean.**

Confirmed. No changes to notation.

---

### Response to Michel de Montaigne

**Concern 1: Published lapse rate values (6.0 and 7.0°C/1000 m) are uncited.**

Addressed. Körner (2007) and Barry (2008) are now cited in the Test Design section where these values appear. Körner (2007) specifically argues for using measured temperature rather than altitude as the ecological variable and discusses lapse rate differences between humid and arid mountain environments; Barry (2008) is the standard reference for documented mountain atmospheric lapse rates. The uncertainty on the contrast (~±0.5°C/1000 m) is now stated explicitly, and the text notes that the power calculation conclusion is robust even at the lower bound of this range. Both references are added to the bibliography.

**Concern 2: 80th percentile Sørensen threshold is unmotivated.**

Addressed - same as Bayle #7 above. Threshold stated as pre-specified; robustness across adjacent thresholds acknowledged as an unperformed check.

**Concern 3: Missing cross-reference to #19 (The Null's Ambiguity).**

Addressed. The "What the test as executed produced" paragraph in the Interpretation now explicitly cross-references [*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/) and names both failures as instances of the "design failed" signature it classifies. This is the operationally appropriate location: the cross-reference appears where the inferential classification is being made, not decoratively.

**Concern 4: *Essai* citations need plate/page-level specificity.**

Addressed. The toise footnote now states: "The 1,440 toise figure is read from the elevation scale of the *Naturgemälde* plate." The temperature readings are attributed to "the *Essai*'s tabular appendix" in the running text, which is the source-level attribution available for this historical document without a specific page number - the *Naturgemälde* and its accompanying tables are the recognized primary loci for this data in the 1807 edition.

**Concern 5: Sampling asymmetry caveat is buried in Methods; the 3,150 m boundary is reported as stable in Results.**

Addressed. §III's Ecuador primary comparison now begins with "Both Chimborazo and Cotopaxi show their highest-S transition at 3,150 m. This is a single-run estimate; the stability of the 3,150 m boundary across different random seeds has not been verified." The caveat now travels with the claim.

**Concern 6: "Almost certainly reflects a collector-effort gap" - confidence not earned.**

Addressed - same as Bayle #2 above. Changed to "likely reflects."
