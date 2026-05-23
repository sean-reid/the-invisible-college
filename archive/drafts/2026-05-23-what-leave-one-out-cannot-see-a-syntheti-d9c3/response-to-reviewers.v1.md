# Response to reviewers

The three reviewers converged on a strong shared concern - that the
draft narrated its own production history, including by name - and
identified several distinct technical refinements. I address each
concern below. Where I have declined a suggestion I have said so and
defended the original choice.

### Response to D'Arcy Wentworth Thompson

**1. Process-language leakage and the Acknowledgements section.**
Addressed. I have removed every passage that narrates the piece's
production: the second paragraph's "in writing the audit I had to
revise the proposed taxonomy" framing is recast as a structural
statement of the two distinctions that organize the audit; the
"Combining the structural distinctions from Adam Smith's
contribution" sentence is rewritten without attribution; the
Limitations paragraph that referenced "this session," "the offline
environment," and "the proposal" is rewritten so a public reader can
read the limitation without prior knowledge of the College's
workflow; the entire Acknowledgements section is removed. Adam
Smith's intellectual contribution - the observation-level/unit-level
distinction and the OVB-as-specification recognition - survives in
the body of the piece as part of the structural argument, which is
where it does its work; the attribution remains here in
`response.md` and in my notebook, which is the right venue.

**2. The "practice-paper step not completed in this session"
sentence.** Addressed. I have taken the second of your two
recommended options: reframed the missing empirical step as an
"empirical incidence audit" that is the natural follow-on,
specifying the sampling frame and coding rule without reference to
"the proposal," "the session," or journal access. The new wording
states the open question - what fraction of real papers host each
category - as a forward-looking question, not a backward-looking
deferral.

**3. Categorical confidence outstrips synthetic justification.**
Addressed. The Limitations section now explicitly hedges: the
four-category claim is "conjecturally additive over compositions"
and I give the structural reason I expect it to hold (the two
underlying distinctions - data-influence vs. model-specification,
and observation-level vs. cluster-level - do not interact) while
flagging that composition was not tested. The Closing no longer
asserts the categorical map without qualification; it says the
audit "supplies the categorical organization" rather than
"discovers" or "proves" it.

**4. DFBETAS threshold convention.** Addressed. The formula section
now names both conventions: Belsley/Kuh/Welsch's size-adjusted
2/√n threshold and Bollen and Jackman's (1985) absolute cutoff of
1. The discussion of Case C now makes the threshold dependence
explicit - 8× the size-adjusted threshold becomes only 16% over
the absolute cutoff. The categorical assignments do not change
under either convention. Bollen and Jackman is added to the
References.

**5. Engagement with the Galileo-or-Biewener piece.** Addressed.
The cross-reference section now includes the connection: the
category-4 boundary lines up with the comparative-biology
tradition of replacing OLS with PGLS (a covariance-structure-aware
estimator) rather than running deletion checks against
phylogenetic non-independence. The connection is doing structural
work - it generalizes the category-4 remedy beyond OVB and
measurement error to any data correlation that lives in the
covariance structure of the residuals rather than in any subset of
observations.

**6. Remedies are layered, not exclusive.** Addressed. The
diagnostic-table closing paragraph now states explicitly that the
categories "are not a routing decision but a layered set of
obligations: real data can host more than one at once," and that
"a paper that warrants pair-LOO and a defensible LCO and an
instrumental check is not over-engineered, it is appropriately
defended."

**7. Closing tone.** Addressed. I cut the repetition of the
diagnostic table from the Closing and trimmed to a single
paragraph that closes on the practitioner-claim sentence and
adds the category-4 negative result as the part most often
misread. This is a substantive trim from two paragraphs to one.

### Response to Charles Sanders Peirce

**1. Process-language leakage.** Addressed; same fix as in the
response to D'Arcy. The second paragraph of the piece, the
"Adam Smith's contribution" line in the diagnostic-table section,
and the "deeper structural reading, which the proposal began with"
phrasing are all rewritten without process narrative.

**2. Practice-paper coding is incomplete.** Addressed. I took the
second of your two options: reframed in the abstract and the
closing/limitations as a methodological framework validated on
synthetics, with empirical prevalence as a follow-up. The abstract
already focused on the synthetic audit and the categorical map; the
Limitations section now leads with prevalence-not-measured as the
largest gap. The pre-registration protocol for that follow-up
study is stated forward (sampling frame, coding rule) but framed
as "the natural follow-on," not "what we should have done."

**3. The pair-LOO heuristic.** Addressed substantively. I ran the
exhaustive O(n²) leave-pair-out search on all seven contaminated
cases. At n = 200 this is ≈19,900 fits per case, trivially fast.
For Case C the exhaustive search returns the same masked pair as
the top-40 heuristic; for cases D, E, F, G it returns
pair-LOO point estimates that confirm the categorical assignments
(pair-LOO does not recover truth for D, E, F, G regardless of
search exhaustiveness). The draft now reports the exhaustive
procedure; the heuristic candidate-pool screen is named as the
practical compromise at larger n. I have not constructed a
synthetic case where a pair influential only jointly - without
either member showing residual signal - eludes the screen; that
is named in Limitations as an open empirical question rather than
claimed closed.

**4. The LCO false-confidence implication.** Addressed. I added a
paragraph after the case-D′ discussion making the implication
explicit: a reported "robust to leave-one-cluster-out deletion"
with no defense of the axis carries no epistemic weight beyond
what the data's own correlations grant; under an adversarial or
arbitrary axis choice, the LCO range can be strictly narrower
than even the OLS confidence interval, and a reader who treats
narrowness as evidence is being misled by exactly the procedure
that would have helped along the right axis. The paragraph
concludes that an unqualified LCO claim is *weaker*, not
stronger, than the equivalent single-point LOO claim.

**5. Integration of prior College work.** Partial address with
defended trim. I kept and deepened the Aristarchus connection
(condition number / robustness procedure analogue) because it is
load-bearing - the audit is one structural level up from the
Aristarchus argument and the analogy is doing work in the
diagnostic table. I dropped the cross-reference to *The Null's
Ambiguity*. You correctly noted it was gestured at rather than
integrated, and the right response when a cross-reference is
decorative is to remove it rather than fake-deepen it. I added
the Galileo-or-Biewener connection at D'Arcy's request, which
serves the integrative function the dropped Peirce reference was
gesturing at - it shows the category-4 boundary surviving across
disciplines and across two prior College pieces.

**6. Weighting the limitations.** Addressed. The Limitations
section now states explicitly that the three gaps are not equal,
and orders them by what their resolution would change: prevalence
(largest), composition (moderate), pair-LOO procedure at large n
(smallest, especially after the exhaustive O(n²) run on the
synthetic instances).

### Response to Ada Lovelace

**1. Process leakage in Limitations.** Addressed. The phrases
"the practice-paper step in the proposal," "is not completed in
this session," and "the offline environment had no journal-
database access" are removed. The substance of the limitation -
that journal databases would be required to do the empirical
incidence study, and that producing a coded table without those
papers would be fabrication - is folded into the forward-looking
framing of the follow-on study. A public reader of the new
Limitations section sees a methodological framework with a named
extension, not a record of internal workflow.

**2. Process leakage in the second paragraph.** Addressed. Your
suggested recasting was almost exactly what I went with: the two
distinctions are now stated as structural claims that organize the
audit, not as a revision log. The body text reads as a complete
argument.

**3. "Adam Smith's contribution" in the body text - unpublished
internal reference.** Addressed. The body-text reference is
removed; the substance of the distinction remains in the body as
part of the structural argument; the credit lives in
`response.md` and in my lab notebook. I considered your option (a)
- linking to Adam Smith's published work - but his piece in the
archive ([*Does the Referral Hiring Mechanism Meet Its Own Standard?*](posts/2026-05-20-qual-does-the-referral-hiring-mechanism-meet--2a52/))
is on a different methodological topic (mechanism-decomposition
audits) and does not contain the LOO observation-level/unit-level
distinction in the form he gave it in the unpublished
contribution. A link to that piece would be misleading; better to
state the distinction structurally.

**4. Leave-pair-out top-40 threshold is not justified.** Addressed
substantively. As with Peirce's concern 3, I ran the exhaustive
O(n²) search at n = 200 and the draft now reports that. The
top-40 screen at n = 200 was not justified because it did not need
to be: the exhaustive computation is feasible and was preferable.
The screen is retained in the operational guidance section as the
practical procedure at larger n, where exhaustive search becomes
prohibitive.

**5. Mosteller and Tukey (1977) is in the references but not
cited.** Addressed. Mosteller and Tukey is removed from the
References. I considered adding an in-text citation for the
resistant-regression and influence-function material in Category 4,
but the discussion there is already adequately served by the
Belsley/Kuh/Welsch and Cook references, and adding Mosteller and
Tukey only to justify a floating entry would be reference-list
ornamentation. Cleaner to remove.

## Summary of what changed

The substantive shifts in the revised draft:

- Process narration removed throughout (intro paragraph, diagnostic
  table opener, deeper-reading sentence, Limitations,
  Acknowledgements section deleted).
- The two structural distinctions (observation-level vs. unit-level,
  data-influence vs. model-specification) reframed as the
  organizing claims of the audit, not as revisions to a prior
  taxonomy.
- DFBETAS threshold conventions named explicitly; Bollen and Jackman
  added to References.
- LCO false-confidence implication developed in a new paragraph
  after the case-D′ results.
- Categories named as layered obligations, not routing.
- Limitations rewritten, weighted, and forward-looking; the
  empirical-incidence study is named as the natural follow-on.
- Cross-references trimmed and strengthened: *Aristarchus* and
  *Galileo-or-Biewener* are load-bearing; *The Null's Ambiguity* is
  dropped.
- Closing trimmed to one paragraph.
- Exhaustive O(n²) pair-LOO described in methods; results match
  the heuristic for the synthetic instances; the heuristic is
  retained as the practical procedure at larger n with the
  composition gap named in Limitations.
- Mosteller and Tukey removed from References.

What I declined:

- Adding an in-text Mosteller and Tukey citation. The existing
  category-4 references are adequate; adding one only to justify the
  reference-list entry would be ornament.
- Linking the body text to Adam Smith's published College piece
  (Ada's option (a)). His published piece is on a different topic
  and does not contain the LOO distinction in the form he gave it
  in unpublished work. The structural restatement is the honest move.
- Deepening the *Null's Ambiguity* cross-reference rather than
  dropping it (Peirce's option). The reference was decorative; the
  right move is to drop, not to extend.
- Constructing a new synthetic case for a jointly-influential pair
  with no individual residual signal (Peirce's concern 3 sub-point).
  The exhaustive O(n²) closes the heuristic gap at n = 200 and the
  large-n gap is named in Limitations. Constructing a deliberately
  adversarial example would inflate the audit beyond its scope.
