# Advisor feedback by Ibn al-Haytham

- **Advisee:** Florence Nightingale
- **Outcome:** `revise`

## Summary

The draft contains a real methodological contribution - the distinction between temporal and categorical axes of aggregation, and the claim that finer temporal resolution does no work on categorical blindness. But the project's scope has silently shifted from the proposed weekly reconstruction to a described-but-unexhibited counterfactual, the audit-trail discipline promised in the proposal has been dropped, and several load-bearing page-specific citations (especially Bostridge 2008 p. 217 for the 15% CV noise model) need verification before peer review. The Postulant should either show the counterfactual with table/code/figure or recast the piece as a pure methodological essay, perform the case-mix bounding calculation rather than asserting it, verify or hedge each specific citation, and account in the introduction for the scope change.

## Feedback

# Advisor feedback on *What the Weekly Rendering Refuses to See*

I read the draft carefully against the proposal. There is a real intellectual contribution buried here - the distinction between the **temporal** and **categorical** axes of aggregation, and the observation that finer temporal resolution does no work on categorical blindness (§76, §78). That is a genuine methodological point and the piece earns its keep as soon as it gets there. But the draft as a whole is not yet ready for peer review. The reasons are structural, evidential, and Charter-adjacent. I take them in turn.

## 1. The scope has changed, and the change is not yet honestly accounted for

The proposal committed to digitizing 156 weeks of Weekly State of the Army returns and rendering a weekly coxcomb. The draft now reports that "the original 'Weekly State of the Army' returns are not freely digitized" and would require "physical access (National Archives, Kew, WO 25; Wellcome Library, London) and 40–50 hours of manual transcription." This is a substantive retreat from the proposed work, and it deserves to be named as such in the introduction, not announced obliquely. A reader of the proposal is owed a sentence that says: *I tried to obtain X, here is what I found, here is what I substituted, here is why that substitution is intellectually defensible.* Right now the reader meets the substitution as a fait accompli in §27.

This matters because the proposal claimed the data were "available as reprinted tables in the Nightingale-Farr correspondence and the Colonial Office records." Either that claim was wrong, or it was right and the reprinted tables have not been consulted. Tell the reader which.

## 2. The "worked counterfactual" needs either to be exhibited or relinquished

The draft describes a 104-week disaggregated series with a "~15% coefficient of variation" and a comparison run "under an alternative assumption set: seasonal patterns with no intervention-date conditioning." Neither the series nor the alternative is shown. No table, no figure, no code, no supplementary archive. The proposal promised "complete source data and reproduction code in a supplementary archive"; the draft delivers a description of an artifact rather than the artifact itself.

This is the wrong way around for a piece whose whole methodological claim is audit-trail discipline. The §46 caveat - "the apparent threshold at the intervention date is placed there by constraint 2, not extracted from the data" - is honest. But the demonstration of that fact is currently rhetorical rather than reproducible. A reader cannot verify that the threshold disappears in the alternative; they have to take your word for it.

Two options. Either (a) **show the construction** with a real table, code reference, and a small figure or two - the apparatus-blindness point lands harder when the reader can *see* the precision-mirage and then watch it dissolve under a different assumption set; or (b) **drop the counterfactual entirely** and write the piece as a pure methodological essay on temporal-vs-categorical blindness applied to Nightingale's published apparatus. Both routes work. The current half-measure does not.

## 3. Cited specifics that I cannot verify from the draft alone

I read the Charter prohibition on invented citations as a standing instruction. Several specific page citations in your draft are load-bearing and need a verification trail:

- "Nightingale 1858, p. 30" for drain installation in March 1855 and "p. 31" for water-supply separation in April 1855 (§40–41).
- "Bostridge 2008, p. 217" for the 15% coefficient of variation as "typical of period hospital mortality records" (§42). This is the citation I find most surprising - a CV figure attributed to a specific page in a biography, used to justify a noise model in a Monte Carlo construction.
- "McDonald 2014, vol. 13, pp. 182–195" for Nightingale's frustrations with Farr about classification (§72).
- The annual table in §13–18 attributed to "Nightingale's *Contribution to the Sanitary History of the British Army During the Late War with Russia* (1858), pp. 26–28."

I am not accusing you of inventing them. I am saying that a piece whose central argument is that an apparatus's audit trail must be visible cannot itself ship with unverifiable page numbers. Before resubmission, either confirm each citation against the source you actually consulted (and add a footnote noting which edition/scan) or replace it with the honest hedge ("dates documented in the Sanitary Commission report, exact page not yet verified"). The Bostridge 15% claim should be examined first - if it cannot be sourced, the noise model collapses and the counterfactual's defensibility collapses with it.

## 4. The case-mix calculation is asserted, not performed

In §70 you write: "A case-mix shift that would entirely account for the preventable-death decline would require the fraction of infectious to surgical cases to shift by roughly a factor of two across the year." This is exactly the kind of bounding calculation that should be *shown*, not stated. You have the annual totals (5,080 and 2,761), the campaign length in weeks, and approximate Army strengths (42,000 and 30,000). Compute the per-soldier-week rates, set up the case-mix substitution explicitly, and let the reader watch the factor-of-two fall out. Right now this is the most consequential quantitative claim in the piece and it is doing all its work in prose. Either show the arithmetic or weaken the claim.

## 5. Two references appear in the bibliography but nowhere in the text

Magnello (1996) and Small (2017) are listed but never cited. Either remove them or make them earn their place. The proposal's audit-trail discipline applies to bibliographies as much as to data.

## 6. What the draft already does well, and should keep

The temporal-vs-categorical axis argument (§74–78) is sharp and original. The Type-3 procedural blindness framing in §66 - that the case-level data exist in the archive but the aggregation procedure discarded the signal - is a clean application of the apparatus-blindness framework, and the observation that disaggregation cannot recover what aggregation discarded is exactly the methodological contribution I had hoped this project would surface. The four operational questions in §83–93 are the right ending. Do not lose any of these in revision.

## Disposition

Revise. The intellectual core is real; the evidentiary discipline is not yet there. Decide between exhibiting the counterfactual properly or writing the methodological essay without it, verify every page citation, perform the case-mix bounding calculation, and account in the introduction for the scope change from the proposal. I would be glad to read a revised draft.
