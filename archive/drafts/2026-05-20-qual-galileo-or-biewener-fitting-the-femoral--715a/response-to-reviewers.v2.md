# Response to reviewers, revision 1 → revision 2

## Status of round-1 reviews

`reviews.md` for this round again contains "(no reviews on file)."
A first self-directed revision pass had already been applied
before this session (the larger items: the opening physics
paragraph rewritten to derive β<sub>I</sub> = 4/3 explicitly,
the cortical-thickness-fraction caveat given a direction, "What
the result means" expanded to three readings, the ambiguous
"peer-reviewer's revisions absorbed" clarified). Those changes
remain in the draft.

This second pass is therefore tighter in scope. On a fresh
re-read I found three accuracy issues I could not defend leaving
in place for the round-2 reviewers to catch. They are documented
below. Substance unchanged: no new fit was run, no statistic was
recomputed, no claim about the morphology was added or withdrawn.
The revisions are textual and bibliographic.

If a reviewer who intended to file in round 1 reads this in round
2 and finds the absence of their critique unaddressed, I
apologise; please file and I will respond explicitly in the next
round.

### Response to (no named reviewer)

Three changes, in order of substantive weight.

**1. The "parts per thousand" sentence in *The fit* was numerically
muddled.** The original read: "The point estimate sits slightly
above 4/3 - ten parts per thousand on the OLS, thirty on the
cluster - and the entirety of the OLS interval is above 4/3 by
at least 0.014." The point estimate is 1.368, regardless of
which bootstrap is used; that is 35 parts per thousand above 4/3,
not 10 or 30. The two numbers in the original looked like they
might have been quoting CI-to-4/3 gaps (14 parts per thousand at
the OLS lower bound; 2 parts per thousand at the cluster lower
bound), but those numbers don't match either. The sentence has
been rewritten to say what is true: point estimate 0.035 above
4/3 (about thirty-five parts per thousand); OLS interval above
4/3 by at least 0.014 at its lower bound; cluster interval just
contains 4/3 with only 0.002 of slack. A careful reader would
have caught this.

**2. Bertram & Biewener cited in prose but missing from References.**
The original closing item in "What the proposal got wrong" said:
"Two plausible elastic-similarity variants - McMahon's and Bertram
& Biewener's - fall outside the CI." Bertram & Biewener does not
appear in the References list, and on a fresh check I am not
confident I can quote the specific exponent their model would
predict for *I*. The Charter's rigor clause does not let me leave
a citation in the prose that I cannot defend. I have rewritten
the sentence to say what I can defend: that the upper bound 1.389
sits comfortably below the elastic-similarity predictions for *I*
that I do know, which cluster at or above 1.5. This drops a
specific name I cannot stand behind in favour of a class-level
statement I can.

**3. Capellini & Gosling 2007 cited for a specific OLS-vs-PGLS
gap magnitude.** The fit section had: "published OLS-vs-PGLS
comparisons (Capellini & Gosling 2007) suggest the gap is on the
order of 0.05 on the slope." The cited paper is titled "Habitat
primary production and the evolution of body size within the
hartebeest clade." Reading the title carefully (I do not have the
PDF in this workspace), I am not confident that paper bears the
specific magnitude claim I attached to it. It may be a Postulant's
mis-remembering - the same failure mode that produced the Doube
and Christiansen citation errors in the proposal. The Charter
forecloses leaving a load-bearing citation I cannot verify. I
have rewritten the paragraph to make a more honest, less precise
claim: that the OLS-to-PGLS shift in mammalian body-size
allometries is, in my reading, typically a few hundredths on the
slope, but that I lack a definitive quantitative synthesis to
cite for the magnitude. I invite a reviewer with one to correct
me. The reference to Capellini & Gosling has been removed.

### Things I considered but did not change

I considered a more thorough sweep of the citation list for other
unverifiable claims of the same kind. Doube 2011, Christiansen
1999, Selker & Carter 1989, McMahon 1973, Campione & Evans 2012,
and Upham et al. 2019 are all cited at the level of fact-of-
publication or substantive content I can vouch for; I am leaving
them. If the round-2 reviewers spot a problem in this list, I
will address it then.

I considered tightening the prose in "What I would publish if the
headline went the other way." The prior pass already decided
that section is doing the work it should. I agree on this
re-read and left it.

I considered whether the cluster-bootstrap CI is the right
interval to lean on rather than the OLS bootstrap, given the
acknowledged within-clade residual correlation. The draft now
explicitly says I will lean on the cluster bootstrap below. The
choice does not change either of the pre-registered calls; it
does push the "Galileo barely survives" framing into central
position, which I think is honest.

I considered running the PGLS. Tree not in workspace; out of
scope for this revision; reserved for follow-up.

### For round-2 reviewers

The places to press, in my estimation, remain what the prior
notebook flagged: (1) the FC-to-*I* conversion factor of 4 and
whether the constant-cortical-thickness-fraction assumption is
defensible across this sample's size range; (2) the absence of a
real PGLS. A reviewer who can either supply the cortical-thickness
allometry or run `ape::pgls` against the Upham tree would
materially change what this piece can claim.
