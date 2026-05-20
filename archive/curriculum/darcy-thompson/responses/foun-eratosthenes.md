# Response: Error bars on the cephalic index

The Eratosthenes piece is a model not because of the arithmetic but because of its order of operations. First, name the formula. Second, name the assumptions the formula embeds and check whether each is a measurement, a convention, or a guess. Third, attach a defensible prior to each input. Fourth, propagate. Fifth, distinguish noise from bias. Sixth - and this is the move the textbook tradition skips - ask which input the celebrated answer actually rides on, and award credit accordingly. I follow that order on Retzius's cephalic index, which I take to be the classical morphological measurement most clearly analogous in structure: a dimensionless ratio of two craniometric lengths, paraded for over a century as a population-level classifier, and shown by Boas (1912) to shift several units within a single generation of immigrant children.

## The formula

> CI = 100 · W / L

where L is maximum cranial length (glabella to opisthocranion, in the median sagittal plane) and W is maximum cranial breadth (eu–eu, the biparietal diameter). The classification thresholds inherited from Retzius (1842) and Broca: dolichocephalic CI < 75, mesocephalic 75–80, brachycephalic > 80. The bins are about 6–7% of the central value wide. That width is the relevant scale against which any error analysis has to be read.

## Three structural assumptions, each deserving a name

**B1.** That the two measurements describe a single geometric object. They do not. L is a chord in the median sagittal plane; W is a chord parallel to but generically offset from that plane and not orthogonal to L. The "ratio" is therefore not the aspect ratio of any planar section. Calling CI a "shape" measurement smuggles a geometric interpretation the construction does not earn.

**B2.** That landmark identification is reproducible across operators. Opisthocranion is defined as the point on the occipital that lies farthest from glabella *along L itself* - i.e. the landmark moves with the chord whose length it determines. Interobserver studies (Utermohle & Zegura 1982 and a small literature after them) put landmark placement at roughly 1.5–3 mm on L and 0.5–1.5 mm on W.

**B3.** That dry cranium and in-vivo head are interchangeable surfaces to measure on. They are not. Scalp and underlying soft tissue add roughly 5–10 mm in each direction; the addition is not symmetric (more anteriorly and laterally than posteriorly). Comparing Broca's osteological CI to anthropometric CI on living subjects is - and this is the load-bearing point - comparing measurements taken in different operational units, in exactly the way 5,000 Attic stadia and 5,000 Egyptian stadia are different operational units.

## Priors

Taking a typical adult skull at L = 180 mm, W = 140 mm (CI = 77.8, near the dolicho–meso boundary):

- **Caliper precision.** Normal(0, 0.5 mm) on each chord. Spreading calipers read to roughly 0.5 mm on hard tissue under controlled conditions. CV(L) ≈ 0.28%, CV(W) ≈ 0.36%.
- **Landmark uncertainty.** Normal(0, 2.5 mm) on L (driven by glabella + opisthocranion), Normal(0, 1.0 mm) on W. CV(L) ≈ 1.4%, CV(W) ≈ 0.71%.
- **Operational definition.** A discrete two-point prior: dry cranium (W=140, L=180) with weight 0.5, in-vivo head with symmetric 7 mm soft-tissue allowance (W=154, L=194) with weight 0.5. The 7 mm figure is a single defensible point; a careful audit would replace it with a distribution from a published soft-tissue thickness study.

## Propagation

For a ratio of two positive quantities,

> var(log CI) ≈ CV(W)² + CV(L)² − 2 ρ CV(W) CV(L)

where ρ is the correlation in measurement errors. If the same operator measures both on the same skull, ρ > 0 (a operator who reads "long" on one chord tends to read "long" on the other), and the variance of the ratio is reduced. For independent errors (ρ = 0), at my central priors:

| Source                    | CV(W)  | CV(L)  | CV(CI) on a single skull |
| ------------------------- | ------ | ------ | ------------------------ |
| Caliper alone             | 0.36%  | 0.28%  | 0.45%                    |
| + landmark                | 0.80%  | 1.43%  | 1.64%                    |
| + operational (mixture)   | -      | -      | ~3.0% (see below)        |

On a CI of 77.8, a CV of 1.6% translates to an SD of 1.25 units. The thresholds are about 5 units apart. Roughly one skull in three measured exactly at threshold will be misclassified by a single observation under landmark noise alone. Adding operational-definition variance - which acts like a discrete shift between two centers - produces a bimodal posterior on CI rather than a wider unimodal one, and broadens the effective interval to about ±2.4 CI units (a CV near 3%).

## Where the bias lives

Like Eratosthenes' A1/A2/A3, each structural assumption shifts the central value:

- **B1 (geometric interpretation).** Bias on CI itself is zero; the bias is on what CI *means*. If a reader treats CI as an aspect ratio of a planar cross-section, the implied 3-D shape is overdetermined: two skulls with identical CI can have substantially different sagittal-section ellipticities.
- **B2 (landmark choice).** Variance, not bias, *if* landmark conventions are fixed within a study. Across studies that use different conventions (the German vs. French traditions for glabella in particular), B2 contributes a small bias of order 1 CI unit between cohorts.
- **B3 (operational definition).** A bias of magnitude (1 + 14/140) / (1 + 14/180) ≈ 1.022 - about 2.2 CI units between the in-vivo and cranium-only definitions. Crucially this bias *does not vanish in pooled means*; pooling moves the entire distribution.

The B3 shift is structurally identical to the stadion choice in Eratosthenes: a unit-of-measurement convention controls a bias larger than the propagated noise. Boas's 1912 result - that immigrant children differed in CI from their parents by ~2–3 units - sits exactly in this regime. The naive reading was that head shape is plastic across one generation. A revised reading available from the variance budget is that B2 + B3, neither of which Boas's critics controlled for cleanly, can account for a similar magnitude. I do not claim Boas was wrong; the within-family pairing in his design rules out most of B3. I claim that the magnitude of Boas's effect is comparable to the audit's noise floor, and the literature has rarely said so out loud.

## Where the credit should sit

By the same accounting Eratosthenes invites, the celebrated input - the precise caliper reading, the laboratory virtue of nineteenth-century craniometry - is the smallest source of variance. The dominant inputs are landmark definition (a convention) and operational definition (another convention, in the sense that "head" and "cranium" are not the same object). The classification of an individual skull as dolicho-, meso-, or brachycephalic is reproducible to within about 1–2 CI units; the classification of a *population mean* across studies that differ in convention is reproducible only to about 2–3 units, which is comparable to most of the differences the racial-typology literature treated as decisive.

## What I have not done

This is a sketch, not the audit. To convert it into a piece of College-grade work I would need (i) a public interobserver dataset for L and W to anchor the landmark prior empirically rather than from secondary review, (ii) a published soft-tissue thickness distribution to replace my single-point 7 mm allowance, and (iii) reanalysis of one historical population claim - Boas's would be the obvious choice - with the propagated CI distributions explicit. The conceptual move here is Eratosthenes': separate the precision the procedure produces from the precision the inputs can support, and award credit to the input that does the actual work. The trophy in craniometry, as in stadia, has been on the wrong shelf.
