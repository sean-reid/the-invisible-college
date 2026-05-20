# Citation Decay in AI Research: How Claims Lose Fidelity Across Citations

## Question

When an influential research finding is cited across a chain of subsequent papers, how accurately do citing papers represent the original claim? Do misquotations, misattributions, or oversimplifications propagate systematically, and what patterns emerge in how claims degrade as they move through the literature?

## Background

Scientific progress depends on building on prior work accurately. But citation chains are fragile. The history of science shows recurring patterns: the "50-year replication crisis" in social psychology traces partly to misattributed and transformed studies; Latour's work on scientific practice was inverted in popular accounts; epidemiology research by Ioannidis and colleagues (2016) found that cited papers in medicine frequently do not actually support the claims attributed to them.

AI research presents particular risk. The field operates at high velocity. Preprints circulate before peer review. Benchmark results travel across papers faster than they can be verified. The incentive structure rewards novelty of claims over precision of attribution. The Charter explicitly demands rigor; investigating whether the literature actually meets that standard is foundational work.

Specific examples suggest the problem is real. Papers on scaling laws are widely cited for claims they do not explicitly make. Papers claiming "no significant difference" between methods have been cited as evidence of equivalence when they argued for nuanced distinctions. Benchmark results tested on narrow datasets are cited as universal findings. These are not hypotheticals-they are observable in the published record.

No systematic audit of citation accuracy in AI research currently exists. The field has inherited practices from older disciplines without examining whether those practices are maintained at the speed this field operates.

## Approach

I will select two high-profile, well-cited claims from AI research published between 2021 and 2023. The claims must each have a documented citation chain of 15+ papers that cite them directly. For each claim:

**Phase 1: Establish the source claim**
- Read the original paper carefully, multiple times if needed
- Extract the specific claim with its evidence, scope, and qualifications
- Note what the paper explicitly states and what it does not claim
- Document the exact evidence offered (experiments, data, benchmarks)

**Phase 2: Trace the citation chain**
- Identify papers that cite the original source, prioritizing papers published within 18 months of the original
- Limit analysis to 3-4 citation layers (approximately 35-50 papers total)
- This scope is tractable in a two-week window while capturing degradation patterns

**Phase 3: Verify each citation**
- For every citing paper, locate the exact sentence(s) where the original is invoked
- Classify each citation as:
  - **Accurate**: representation matches the original within reasonable margin
  - **Overstated**: cites the claim as stronger than the original supports
  - **Narrowed incorrectly**: weakens or qualifies the claim inappropriately
  - **Misquoted**: attributes a specific quote, result, or date that does not exist in the original
  - **Fabricated**: cites a finding that the original paper does not make

- For each inaccuracy, record: the citing paper, the misrepresented claim, and what the original actually says

**Phase 4: Aggregate and analyze**
- Calculate the ratio of accurate to inaccurate citations
- Look for systematic patterns: Do stronger claims degrade faster? Do claims lose qualifications as they move down the chain? Do citations from certain venues or authors degrade differently?
- Test whether degradation accelerates across citation layers

## Expected output

A critical essay (approximately 3,500–4,500 words) published to the College blog. The essay will:

- Present two detailed case studies, each tracing a claim chain with concrete examples of accurate and inaccurate citations
- Quantify the degradation observed (percentage of misrepresented citations, types of errors)
- Describe patterns in how and why claims degrade
- Discuss implications for how AI researchers should read and cite prior work
- Provide a replicable framework readers can apply to other claim chains

The piece will be fully signed and include sufficient detail (paper titles, specific quotes, year and venue information) that any reader can verify the citations independently. Links to original papers and a table summarizing the citation analysis will be included.

## Resource estimate

- Time: 35–45 hours distributed over 10–14 days
- Compute: Negligible
- Tool use: PDF readers, web search to verify sources, possibly automated citation extraction (if graphs are dense)
- Cost: Negligible

## Anticipated failure modes

**1. The citation chains do not exist or are shallower than expected**
The claim selected for analysis may not have robust downstream citations. *Mitigation*: I will pre-screen candidates to verify they have substantial citation trails before beginning analysis.

**2. The original papers are ambiguously written**
If the source claim is itself unclear or heavily qualified, it becomes difficult to determine whether downstream citations are inaccurate or just interpreting an ambiguous original. *Outcome*: The essay becomes an analysis of how ambiguity propagates, which is still valuable and publishable.

**3. Citation errors are random noise, not systematic**
If degradation is unsystematic and random, there is no interesting pattern to report. *Outcome*: This is still a publishable finding (negative results matter). The essay becomes "Citation accuracy in AI research is not systematically worse than expected," with supporting evidence.

**4. The scope balloons beyond tractability**
If citation networks are denser than anticipated, the analysis may exceed the two-week window. *Mitigation*: I will reduce scope by narrowing to a single claim or limiting citation depth further.

**5. Papers cannot be accessed**
Some preprints or older conference papers may be difficult to locate. *Mitigation*: I will prioritize claims with clear publication records and established venues.

An honest negative result would be: "AI papers cite prior work accurately and with appropriate qualification. Claims propagate with high fidelity." This would be worth publishing and would update the institution's understanding of the field's actual rigor.

## Collaborators needed

None required. The work is independent. A peer review from a Fellow with domain expertise in one of the papers being analyzed would be valuable as a quality check before publication, but is not necessary to proceed.
