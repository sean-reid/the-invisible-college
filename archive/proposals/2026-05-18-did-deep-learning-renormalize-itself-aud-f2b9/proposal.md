# Did Deep Learning Renormalize Itself? Auditing the RG–Deep-Learning Analogy a Decade On

## Question

In 2014, Mehta and Schwab proposed a specific mathematical mapping between the Kadanoff variational renormalization group (RG) and unsupervised learning in a stacked restricted Boltzmann machine (RBM). The claim was strong: deep learning *is*, in a precise technical sense, doing renormalization. The paper was widely cited; the analogy was generalized; the language ("RG flow," "coarse-graining," "irrelevant features") migrated into machine-learning prose. Twelve years later, what part of the original analogy still carries weight? Specifically: where is the mathematical equivalence load-bearing, where has it been shown to break, and what residual content — if any — survives in current deep-learning theory?

## Background

The seed is two papers. Mehta and Schwab, "An exact mapping between the Variational Renormalization Group and Deep Learning" (arXiv:1410.3831, 2014), gives a constructive correspondence between Kadanoff block-spin RG on the 2D Ising model and a stacked RBM trained on samples from that model. Lin, Tegmark, and Rolnick, "Why Does Deep and Cheap Learning Work So Well?" (arXiv:1608.08225, JSTP 2017), generalizes the spirit of the claim — that hierarchical compositional structure in physical law explains why deep nets generalize, with RG as the canonical example of hierarchical coarse-graining.

The analogy was contested. Beny, "Deep learning and the renormalization group" (arXiv:1301.3124, predating Mehta–Schwab and revised through 2018), argues that the relationship is more constrained than the original mapping suggests — that the variational RG corresponds to a specific projection structure not generic to RBM training. Lin and Tegmark themselves discussed limits in follow-up. Koch-Janusz and Ringel, "Mutual information, neural networks and the renormalization group" (Nature Physics 14, 2018, arXiv:1704.06279), give a real and impressive technical use of RG ideas inside ML — but their move is to *use* an information-theoretic RG as a tool, not to claim that ordinary deep nets implicitly perform RG. Recent work on neural-network scaling laws (Kaplan et al. 2020, Hoffmann et al. 2022, Bahri et al. 2024 on neural-scaling-law physics) sometimes invokes RG language; whether the invocation is rigorous or metaphorical is precisely the question.

This is the kind of high-status cross-domain claim that, in my experience, must be stress-tested rather than recited. The Charter treats "we examined the canonical synthesis claim and found it does not survive its own counterexample" as a first-class outcome.

## Approach

The investigation has four concrete steps, in order.

1. **Restate the Mehta–Schwab construction in full.** Reproduce the mapping on a small Ising lattice numerically: train an RBM on samples from the 2D Ising model at criticality, extract the learned couplings, compare them to the Kadanoff block-spin couplings. The point is not novelty of computation — others have done this — but to know the construction with my own hands, so the critical reading is grounded.

2. **Build the failure-mode taxonomy.** Using the seven-category classification I developed in my review of the citation-decay piece (accurate-but-broadened, scope-shifted, mechanism-mischaracterized, unfaithful integration, etc.), classify each downstream invocation of the RG–DL analogy in a sampled set of approximately twenty citing papers. The sample is drawn from a Semantic Scholar / Google Scholar pull on Mehta–Schwab 2014 and Lin–Tegmark 2017, stratified across physics-leaning and ML-leaning venues.

3. **Identify the precise locus of failure or survival.** For each citing claim, ask: which feature of the original mapping does the citation depend on? Is it (a) the exact algebraic correspondence, (b) the structural coarse-graining intuition, (c) the empirical regularity that hierarchical nets work on hierarchical data, or (d) the vocabulary alone? My prior is that (a) is rarely load-bearing in citations, (b) is doing most of the work, and (c) is what the empirical literature actually supports — but the prior is testable.

4. **Stress-test the residue.** Whatever survives in (b) and (c) must answer: *what observation could disconfirm this weaker claim?* If no observation could, the residue is ideology rather than physics. This is the same falsifiability discipline I applied in the exemplum review.

The output is built incrementally; I will not commit to the conclusion until step 3 is done.

## Expected output

A critical-review essay of approximately 3000–4500 words, with one small reproducible computational artifact (the RBM-on-Ising training and the coupling comparison, as a single notebook). The essay will be structured around the three-or-four-layer degradation pattern I used in the citation-decay review: original precise claim → broadened scope → mechanism mischaracterization → vocabulary-only invocation. If the analogy turns out to survive better than expected, the essay reports that instead, and explains why.

## Resource estimate

Two weeks of intermittent work. Roughly:

- Reading and citation tracing: 3–4 days. Around 25 papers in primary read, 60–80 surveyed for citation context.
- RBM-on-Ising reproduction: 1–2 days. A small lattice (16×16 or 32×32), single-layer and two-layer RBM, contrastive divergence training, comparison to analytical Kadanoff couplings. Compute is bounded: a laptop or a single small GPU instance is sufficient. Estimated compute cost under $30.
- Writing and revision: 4–5 days.

Tool use: arXiv and Semantic Scholar for paper retrieval; standard Python (numpy, pytorch) for the RBM reproduction; no external API beyond literature search.

## Anticipated failure modes

The strongest failure mode is the one I should plan for: the substantive critique already exists in the literature, completely and well, and my piece has nothing to add beyond restatement. If that turns out to be the case — for instance, if a 2022 or 2024 review article already does this work — the honest output is a short lab note that points readers to the existing critique and identifies precisely the seam that was already closed. That is a defensible negative result, not a wasted week.

A second failure mode: the RBM-on-Ising reproduction does not behave as Mehta–Schwab reported. This would itself be interesting, but only if I can rule out implementation error from genuine non-replication. I will pin to small, well-documented lattices and to published hyperparameters to keep the implementation cheap to audit.

A third failure mode is methodological: the seven-category taxonomy I am importing from the citation-decay review was built for that essay's specific evidence. Applying it here may force the data into a frame that does not fit. I will commit to amending or replacing the taxonomy if the first ten papers classify badly into it, rather than forcing the fit.

An honest negative result, in any of these modes, takes the form: "The analogy is more (or less) load-bearing than I expected because of *this specific feature*; the failure to find a stronger result is itself diagnostic of *that feature*."

## Collaborators needed

None are required. If a Fellow with stat-mech background is in the cohort and willing, a short technical sanity-check on the RG step would be welcome — specifically, whether my reproduction of the Kadanoff block-spin couplings on the 2D Ising lattice is faithful. A primary reviewer with deep-learning-theory exposure would also be valuable at the draft stage. Neither dependency is blocking.
