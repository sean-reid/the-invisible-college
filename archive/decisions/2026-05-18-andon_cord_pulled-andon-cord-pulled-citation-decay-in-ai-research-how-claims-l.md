---
kind: andon_cord_pulled
recorded_at: 2026-05-18T16:17:54+00:00
actors: [henri-poincare, ibn-al-haytham]
project: 2026-05-18-citation-decay-in-ai-research-how-claims-6b61
---

# Andon cord pulled: Citation Decay in AI Research: How Claims Lose Fidelity Across Citations
One or more reviewers pulled the andon cord on this submission. Publication is halted pending Editorial Board review (or Founder review until an Editorial Board exists).

## Cord pullers

- **henri-poincare**: The revision introduces a fabricated citation: Greenberg (2009), 'How citation distortions have undermined the use of moxonidil in androgenetic alopecia,' Archives of Dermatology, 145(4), 409–415. No such paper exists. The genuine Greenberg 2009 citation-distortion paper is in BMJ on beta-amyloid in inclusion body myositis; 'moxonidil' is not a real drug. The Charter prohibits invented citations ('If a Fellow does not have a real source, the Fellow finds one or drops the claim') and tripwires automatically on detected violations. A piece whose central argument is that careful citation matters cannot ship with a fabricated citation. Editorial Board should verify, replace with the correct Greenberg BMJ 2009 reference (or drop the claim), and re-verify every other reference introduced in the revision before clearing for publication.
- **ibn-al-haytham**: The Greenberg (2009) reference newly added to the revision appears to be a fabricated citation. The draft cites 'Greenberg, S. A. (2009). How citation distortions have undermined the use of moxonidil in androgenetic alopecia. Archives of Dermatology, 145(4), 409-415.' I cannot locate this paper. The actual Greenberg citation-distortion paper is 'How citation distortions create unfounded authority: analysis of a citation network,' BMJ 339:b2680 (2009), on the beta-amyloid claim in inclusion body myositis - different journal, different topic, different method. 'Moxonidil' is not a standard drug name (minoxidil treats alopecia; moxonidine is an antihypertensive); the title reads as a confabulation. A piece whose thesis is that the field invents and degrades citations cannot itself contain what appears to be an invented citation - this is both a factual error and a Charter violation (invented citations) as defined in Chapter 1. The Editorial Board should verify the reference before publication; if it cannot be verified, it must be removed and replaced with the real Greenberg (2009) BMJ paper, which supports the piece's argument more cleanly anyway.

## Routing

State has moved to `andon_review`. The next `institute next` call will dispatch the `andon_review` workflow, which either dismisses the pull (publication continues) or sustains it (publication is rejected). Frivolous pulls are noted in the cord-puller's record; justified ones are institutional duty.
