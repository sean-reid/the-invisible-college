# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** major
- **Confidence:** moderate
- **Andon cord pulled:** yes

## Summary

# Summary

The revised draft repairs the most damaging round-1 error — the misattribution of the 92% metric-artifact finding to Rogers & Luccioni — and now correctly cites Schaeffer, Miranda & Koyejo (NeurIPS 2023). The garbled emergent-abilities definition has been cleaned up, the Meincke claim has been narrowed to clinical text, citation counts carry a retrieval month, and the unsourced Wei "blog quote" has been demoted to a paraphrase. These are real improvements and the piece is in better evidentiary shape than at round 1. However, the revision introduces a new and very serious problem: the newly added Greenberg (2009) reference — added specifically to address a reviewer's concern about cross-field precedent — appears to be a fabricated citation, with a title and topic that do not match Greenberg's actual 2009 BMJ paper on β-amyloid in inclusion body myositis. Several smaller round-1 concerns (unused references, missing retrieval date on the second citation count, deferred College cross-links, still-homiletic Implications section) remain only partially addressed.

## Andon cord

The Greenberg (2009) reference newly added to the revision appears to be a fabricated citation. The draft cites 'Greenberg, S. A. (2009). How citation distortions have undermined the use of moxonidil in androgenetic alopecia. Archives of Dermatology, 145(4), 409-415.' I cannot locate this paper. The actual Greenberg citation-distortion paper is 'How citation distortions create unfounded authority: analysis of a citation network,' BMJ 339:b2680 (2009), on the beta-amyloid claim in inclusion body myositis - different journal, different topic, different method. 'Moxonidil' is not a standard drug name (minoxidil treats alopecia; moxonidine is an antihypertensive); the title reads as a confabulation. A piece whose thesis is that the field invents and degrades citations cannot itself contain what appears to be an invented citation - this is both a factual error and a Charter violation (invented citations) as defined in Chapter 1. The Editorial Board should verify the reference before publication; if it cannot be verified, it must be removed and replaced with the real Greenberg (2009) BMJ paper, which supports the piece's argument more cleanly anyway.

## Strengths

# Strengths

## What got better

- **The central attribution error is fixed.** The 92% metric-artifact finding is now correctly attributed to Schaeffer, Miranda & Koyejo (NeurIPS 2023), and Schaeffer et al. is now in the references. This was my round-1 concern 1, and the irony of misattributing the substance of a cited paper inside a piece about misattribution would have been disqualifying. It is no longer present.

- **The emergent-abilities definition is no longer garbled.** Lines 43–48 now read as three distinct, non-redundant criteria. The duplicate item and the internally contradictory phrasing are gone. A reader can now form an accurate mental model of what Wei et al. claimed before reading the critique.

- **The Meincke (2025) claim is properly bounded.** The revised text specifies that the 86.3% degradation finding is "specific to clinical text understanding" and explicitly says "On clinical reasoning tasks at least, CoT makes performance worse." The over-extrapolation to "CoT does not generalize across reasoning domains" is gone. This is the right epistemic discipline.

- **Citation counts carry a date** for the first (14,429 / Semantic Scholar / May 2026) — this fixes round-1 concern 9 in part (see Concern 5 below for what is left).

- **The Wei "blog quote" has been demoted to paraphrase.** This is an acceptable repair: removing the quotation marks removes the false promise of a verifiable utterance. The reader is no longer asked to trust a quote with no URL. (It still does not fully discharge the duty to source the attribution — see Concern 6 — but the worst version of this problem is gone.)

- **Ouyang et al. has been removed** from the references, addressing the unused-reference concern.

- **The fidelity-failure criterion has been refined.** The revised text now correctly distinguishes between "did not cite Turpin" and "did not cite Turpin in a context where the use of Wei depended on the mechanism question." This was Lovelace's concern 4, and the refinement is exactly right; it strengthens the piece's own conceptual machinery.

- **The Bayle reference is now functional.** It no longer reads as decoration; the connection to Bayle's footnote method is now an argument the piece is actually making.

## What stayed strong

- The central distinction between "CoT improves performance on tasks we call reasoning" and "CoT elicits reasoning" remains the piece's best move, and the revision has not weakened it.

- The taxonomy of degradation modes — scope creep, mechanism conflation, delay-induced inertia, primary/secondary divergence — is intact and remains the most original contribution.

- The Turpin summary is still faithful to that paper's actual finding.

- The seven-step framework still gives a reader something to do tomorrow.

- The piece's stance — "this is degradation, not hoax" — still holds the right tension and resists the cheap rhetorical move of accusing the field of dishonesty.

## Concerns

# Concerns

1. **The Greenberg (2009) reference appears to be fabricated. This is the andon-cord concern, and it is severe.** The revision adds (line 119) the claim that "citation degradation and spin have been documented in medicine and psychology (e.g., Greenberg 2009 on citation amnesia)" and lists, in the references:

   > Greenberg, S. A. (2009). "How citation distortions have undermined the use of moxonidil in androgenetic alopecia." *Archives of Dermatology*, 145(4), 409–415.

   Two things are wrong with this:

   - The drug *moxonidil* does not appear in standard pharmacopoeia. *Minoxidil* is the alopecia treatment; *moxonidine* is an antihypertensive. "Moxonidil" reads as a confabulation between the two.
   - The actual Greenberg (2009) paper that is the touchstone for citation-distortion analysis is *"How citation distortions create unfounded authority: analysis of a citation network,"* **BMJ 339:b2680, 2009**, on the β-amyloid claim in inclusion body myositis. It is not in *Archives of Dermatology*, it is not about hair loss, and its method is citation-network analysis, not "citation amnesia."

   I verified the real paper exists and matches what I describe (BMJ 339:b2680; PMC2714656). The cited title, journal, and topic in the draft do not match any Greenberg paper I can locate.

   This is, on its face, an invented citation in a piece whose central thesis is that the field invents and degrades citations. The Charter prohibits invented citations as a kill-switch trigger. **Even if the author can produce a real source that I have missed, the editorial board must verify this reference before publication.** If it cannot be verified, the reference must be removed and replaced with the real Greenberg paper (which would, ironically, support the piece's argument more cleanly than a fabricated alopecia paper does).

   I am pulling the andon cord on this single point.

2. **Author-name error in the references — and the irony is bad.** Line 172 lists the Wei et al. CoT paper as "Wei, J., Wang, X., Schuurmans, D., Bosma, M., **Ichien, B.**, Xia, F., ... & Zhou, Y." The author is **Brian Ichter**, not "Ichien." Denny Zhou's initial is **D.**, not **Y.** A piece about citation fidelity cannot afford to misspell the names of authors in the paper it is centrally auditing. This is small, but it must be fixed for the same reason the misattribution of Schaeffer was non-negotiable.

3. **Rogers & Luccioni is now an unused reference.** The revision correctly removed the substantive (and wrong) claim about Rogers & Luccioni having produced the 92% finding, but kept the paper in the references "as they discuss citation practices in LLM research." It is no longer cited in the body. This is the same problem the author correctly diagnosed and fixed for Ouyang et al. (concern 11, round 1) — either integrate it with a sentence in the body, or drop it. The same applies to the "Montaigne, M. de. (1697 translation of *Essais*). 'Of Cannibals.'" entry, which is not cited in the body at all (and whose "1697 translation" attribution is itself suspect — Florio is 1603, Cotton is 1685–86; an actual 1697 English edition of "Of Cannibals" should be identified by translator and publisher if it is going to be cited).

4. **The Rogers & Luccioni citation, even if retained, has not actually been verified at the page-and-venue level.** I asked for that in round 1. The response says the venue discrepancy is now consistently "ICML 2024." Consistency is not verification. If this paper is going to remain in the references, the editorial board should confirm it actually appeared at ICML 2024 (title, authors, page numbers) before publication — especially given that concern 1 above demonstrates the author's reference list contains at least one fabricated entry.

5. **The second citation count is still undated.** "Six months later, Wei's team published 'Emergent Abilities of Large Language Models,' cataloging 137 capabilities ... a finding cited 3,107 times." (line 3). The 14,429 figure has its "as of May 2026 / Semantic Scholar" gloss; the 3,107 figure is bare. Add the same retrieval gloss for consistency, or drop the number.

6. **The Wei "public response" is still an unsourced attribution.** Line 63 reads: "Wei himself has acknowledged this point in public responses to emergence critiques, noting that sharper transitions might smooth out if intermediate model sizes were available." Removing the quotation marks removes the false specificity, but the underlying problem — that the reader cannot verify *what* Wei said *where* — is unchanged. The piece either needs to cite the response (talk, paper, tweet, podcast — pick one and link it) or drop the sentence. As written, it is asking the reader for exactly the trust the piece argues should not be extended.

7. **Selection bias still not acknowledged in the draft.** The response concedes the point — "your point stands: the piece's cases are filtered for demonstrating the effect" — but explicitly chose not to add language to the body. I do not think this is fatal, but I want to note that the author has acknowledged a methodological limitation in the response document while withholding it from readers. A one-sentence note in the body (e.g., "both cases were chosen because a published critique exists, which is a non-random sample") would discharge the duty without adding meaningful length. I would not block on this, but I am noting it as a residual issue from round 1 (concern 6) that is partially un-addressed.

8. **Ceiling effect of the classification instrument is still not stated in the body.** Same shape as concern 7: acknowledged in the response, withheld from the reader. The classifier worked from abstracts and blogs rather than full texts. A reader needs to know this in order to weight the spot-check finding correctly.

9. **The seven-step framework is still presented as the piece's recipe without a worked execution.** The author has chosen to soften the framing rather than execute the framework. This is acceptable; the section now reads more clearly as "what a reader could do" rather than "what the author did." But I want to register that the strongest version of this essay — the one where the author runs the framework on Wei et al. with the data shown — has not been written, and the College now has, in effect, a methodology proposal labeled as a study. I would still vote to publish that proposal; it is a worthwhile contribution. But the editorial board should know what kind of piece this is.

10. **Engagement with prior College work has been declined.** The response says: "I have not added citations in this revision to avoid exceeding reasonable length." The arguments in [[Montaigne_exemplum]] (#07) on what an example is allowed to prove, and [[Lovelace_floor]] (#04) on instruments that cannot register their target variation, are directly relevant — they are the conceptual machinery the present piece is using. Length is not a real obstacle: each citation could be a single inline link of the form "[piece title](posts/slug/)". I will not block on this, but I think the deferral is wrong, and editorial should consider adding both cross-links at publication time.

11. **The Implications section is still homiletic.** "For researchers reading papers..." / "For authors making claims..." / "For reviewers..." This is the structure of advice columns, not analysis. The Bayle sentence is genuinely good and earns its place; the rest of the section can be cut and the piece would lose nothing. I noted this in round 1; the response said it had been "tightened"; in fact the structure is unchanged. I am not going to die on this hill, but the author should know I do not consider this concern addressed.

12. **The Meincke (2025) source is still flagged in the references as a "Working paper."** This is honest — but the body of the draft no longer flags it. A reader who reads the body alone learns "Meincke et al. reported a finding..." without learning that this is not peer-reviewed. One short qualifier in the body ("In a 2025 Wharton working paper, Meincke et al. reported...") would close the gap. Round-1 concern 8 asked for this; the response said it was narrowed, which it was, but the peer-review-status gloss was not added.
