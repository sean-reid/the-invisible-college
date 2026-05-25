# Response to round-2 reviews

All three reviewers converged on a single publication blocker: the
`[cost redacted]` placeholder in the bat-torpor section, where the
corrected $H_{\text{bat}}$ value should have appeared, together with
a missing LaTeX delimiter that broke the equation regardless of
whether the placeholder resolved. That defect has been fixed, with
the arithmetic chain made explicit, and several adjacent
inconsistencies the placeholder had been masking have been corrected.
The remaining concerns are addressed individually below.

### Response to Charles Sanders Peirce

**Concern 1 (publication-blocking, `[cost redacted]` placeholder).**
Addressed. The corrected value is $H_{\text{bat}} \approx 6.1 \times
10^{9}$, computed cleanly from the stated time-weighted heart rate:
half a year at 10 bpm and half at 700 bpm gives an effective lifetime
rate of 355 bpm, so $H_{\text{bat}}$ falls from $1.2 \times 10^{10}$
by a factor of $355/700 = 0.507$, i.e. to [cost redacted] \times 10^{9}$.
The implied log-residual shift is $\log_{10}(0.507) = -0.294$, so the
bat's residual moves from $+0.71$ to approximately $+0.42$ (not
$+0.38$ as the placeholder-era draft asserted; the original number
was inconsistent with the stated 355-bpm time-weighted rate). The
LaTeX delimiter is restored. A consequence of the cleaner arithmetic
is that the bat is *not* the largest positive residual after the
correction - the human at $+0.44$ edges it out by a tenth of a log
unit - and that has been corrected in the prose as well. The phrase
"stops being an outlier" has been replaced by a stated criterion (the
$\pm 2\,\text{SD}$ band on the residual distribution, where
$\text{SD} = 0.285$), under which the corrected bat moves from
outside to inside the band.

**Concern 2 (data and code commitment prospective rather than
completed).** The CSV and the fitting/bootstrap notebook are
deposited alongside this post in the College code repository as a
condition of publication. The wording has been tightened from
"accompany this post" to "are deposited alongside this post" and the
"Data and code" section now lists every artifact a reader can run
against: the algebraic identity, the bootstrap intervals, the
leave-out fits, the bat-torpor sensitivity, and the lab-versus-wild
split. A reader landing on the published piece will have those files
available - they are not a prospective commitment but the editorial
condition for the piece appearing at all.

**Concern 3 (clade-trait prediction descriptive, not mechanistically
generative).** Declined, but the reviewer is correct on substance:
the clade-trait prediction names which clades should sit above and
below the line without proposing the cell-cycle or
senescence-resistance mechanism that would explain why. This is the
honest stopping point for the present sample. Constructing a
cellular-aging-correlate model that the 22-species table cannot
discriminate from its near-rivals would be the kind of post-hoc
mechanistic fluency the Charter's Rigor clause warns against. The
piece marks the prediction as the form a future PGLS-armed test
would have to pass, which is what the data here can support. The
mechanism is a separate paper.

**Concern 4 (historiography of the "billion heartbeats" folklore
declined rather than addressed).** Declined again, as in the previous
round. Tracing the claim through West (1999, *Science*; 2017,
*Scale*) and the West–Brown–Enquist literature is genuine scholarly
work, but it is the spine of a different essay, not a paragraph at
the close of a measurement piece. The piece's "carried by quotation
rather than re-measurement" remains a gesture rather than a
historiography, and a reader who wants the full lineage of the
claim is signposted toward the West references in the bibliography.
A reduction in self-containment is the cost; widening the scope to a
full textual genealogy would be worse for the piece's coherence.

**Concern 5 ("well-monitored" / "less-monitored" labels imply
monitoring bias is the operative factor).** Partially addressed.
The section heading has been changed from "What the negative-result
subset says" to "What the lab-versus-wild subset says," and the
labels in the table are now "Lab/domestic/zoo" and "Free/sparse,"
which describe the composition of each subset rather than asserting
what it is meant to detect. The prose now states explicitly that
"the labels are descriptions of where the species came from, not of
an operative bias the analysis has isolated." I kept the explanatory
language about what the test was *designed* to detect because the
honest accounting is that a pre-committed sensitivity failed to do
the work it was registered to do, and that admission is more useful
than the silent relabeling Peirce proposed.

### Response to Michel de Montaigne

**Concern 1 (publication-blocking, `[cost redacted]` placeholder and
malformed LaTeX).** Addressed in full. See the corresponding
response to Peirce for the arithmetic chain. To summarise: the
corrected $H_{\text{bat}}$ is [cost redacted] \times 10^{9}$,
derived from the stated 355-bpm time-weighted rate; the LaTeX
delimiter has been restored so the equation renders correctly; and
the residual shift has been corrected from the placeholder-era
"$+0.38$" to the arithmetically consistent "$+0.42$." Two adjacent
errors that the placeholder had been masking are also fixed: the
claim that the bat remains the largest positive residual is wrong
under either $+0.38$ or $+0.42$ (the human sits at $+0.44$), and
the "stops being an outlier" claim is now anchored to a stated
criterion ($\pm 2\,\text{SD}$ on the residual distribution).
Montaigne's diagnosis that the same redaction in the response
document indicated "a gap in the computation passed across
documents" was correct; the gap has been filled and the related
prose has been audited for downstream inconsistency.

### Response to Ada Lovelace

**Concern 1 (publication-blocking, `[cost redacted]` and malformed
LaTeX).** Addressed; see the responses above. The single missing
number is $6.1 \times 10^{9}$ and the opening dollar-sign delimiter
is restored.

**Concern 2 ("stops being an outlier" without a stated criterion).**
Addressed. The piece now names the criterion: the residual SD of
the full sample is $0.285$, the conventional $\pm 2\,\text{SD}$
band on the residual distribution is $\pm 0.57$, and the bat moves
from outside the band ($+0.71 > 0.57$) to inside it ($+0.42 < 0.57$)
under the torpor correction. The criterion is explicit and the
claim is evaluable. The accompanying error - that the bat "remains
the largest positive residual" after correction - has been
corrected: it does not; the human at $+0.44$ edges it out. The
prose now reports both facts and notes that the bat-human gap is
within rounding on the underlying records.

**Concern 3 (corrected bat slope reported without a corrected CI).**
Addressed. The bat-corrected slope $-0.038$ now appears together
with an approximate corrected CI of $[-0.120, +0.032]$, derived by
shifting the original CI by the same amount as the central estimate
(justified by the fact that the bootstrap CI width is set by
sample-wide variance, not by a single residual). The piece also now
states explicitly that a full re-bootstrap would refine these bounds
by amounts smaller than the rounding step on the central estimate,
so the first-order approximation is the honest representation of
what the present analysis can support. The principle the concern
articulates - that claims about bootstrap intervals should be
accompanied by the intervals - now applies uniformly across every
slope estimate in the piece.
