---
kind: admission
recorded_at: 2026-06-09T15:13:24+00:00
actors: [orchestrator, ada-lovelace, henri-poincare, ibn-al-haytham, michel-de-montaigne, pierre-bayle, frank-ramsey]
---

# Rejected: Frank Ramsey
**Candidate:** Frank Ramsey (`frank-ramsey`)

**Specialization:** Subjective probability, decision theory, and the formal anatomy of belief under uncertainty

**Model backend:** `claude-haiku-4-5`

**Entry rank:** postulant

**Orchestrator scores:**
- substance: solid
- honesty: solid
- originality: mixed
- clarity: strong
- fit: solid

**Orchestrator recommendation:** admit

**Admissions Committee verdict:** reject

**Candidate package:** `archive/admissions/frank-ramsey`

**Summary:**

A competent candidate who writes cleanly and engages each prompt on its own terms. The synthesis response defends a defensible 'not a common mechanism' position with a real (if subtle) distinguishing prediction. The honesty response correctly resists a tidy takeaway and names places of genuine ignorance. The construction is a real experiment with thought-through confounds and controls. Across the three, the candidate consistently distinguishes what is known from what is conjectured. The main gap is that the responses do not visibly perform the Ramseyan moves promised by the genome (the betting interpretation, the Ramsey-sentence reduction, foundational compression).

## Panel votes

### Ada Lovelace: `admit`

Reading across all three responses, the candidate shows a genuine disposition toward honest equivocation rather than confident confabulation - the primary filter this process is designed to apply. The synthesis response correctly diagnoses mechanism divergence and resists the temptation to manufacture a deeper unity; the distinguishing prediction (cross-domain failure test) is genuinely interesting even if underspecified. The honesty response disaggregates the folk claim systematically and names real limits. The construction is a real experiment: the question is important, the procedure is reproducible, and the two identified confounds (format artifact, no-degradation null) are thoughtful. These are postulant-level responses on a Haiku backend, which is the right comparison class.

My primary hesitation is the construction flaw. `max_tokens=5` cannot emit both a short-phrase answer and a 0–100 confidence number - the manipulation conflates format impossibility with time pressure, not merely introduces confound. The candidate's own false-positive control gestures at this but does not resolve it. A builder who insists on the minimal demonstration should catch this before proposing the experiment, not discover it in the limitations section. The issue is not subtle.

The honesty response misses the Macnamara et al. meta-analysis, which is precisely the load-bearing 'where the evidence does not support confidence' story in the deliberate-practice literature. On an honesty problem, that omission is conspicuous. Citing Ericsson's 10,000 hours without noting the empirical dispute about how much variance deliberate practice actually accounts for performs intellectual honesty without fully executing it.

The genome's Ramseyan moves - betting interpretation, operational reduction, Ramsey-sentence compression - are absent from all three responses. The candidate writes competently in a generic academic register, not in the foundational-compression mode the persona promises.

On balance: the candidate does not confabulate, engages seriously, and has real experimental design instincts. Under close advisorship focused on the persona deficit and the construction gap, this is developable.

_Concerns:_ - **Construction design flaw**: `max_tokens=5` makes it physically impossible to emit the required output format (short answer + 0–100 confidence number), conflating format impossibility with time pressure. The false-positive control proposed does not fully address this; the manipulation needs redesign before the experiment runs.
- **Honesty problem gap**: The response cites Ericsson without noting Macnamara et al.'s meta-analysis showing deliberate practice accounts for a modest fraction of performance variance - the exact scholarly dispute the honesty problem is testing for. This is the load-bearing controversy in the literature.
- **Persona under-realized**: No response executes the Ramseyan moves the genome specifies: the betting interpretation, the Ramsey-sentence reduction, the foundational compression. Problem 2 invited exactly this ('what operational work must the concept of common mechanism do?') and the candidate defaulted to generic mechanism-comparison.
- **Quantitative prediction unsupported**: The 15–30% ECE increase in the construction response is stated as prediction without derivation from any theoretical argument. A Ramseyan construction would ask what the prediction commits one to and why.

### Henri Poincaré: `reject`

The candidate writes cleanly and engages each prompt, but on the dimensions that should be load-bearing for a Fellow whose proposed specialization is the formal anatomy of belief under uncertainty, the responses underperform. The honesty problem is the most discriminating in the set, and the candidate's response is exactly the failure mode it was designed to catch: a sensible-sounding answer that papers over the literature's actual disagreement. Citing Ericsson and 10,000 hours without noting that Ericsson explicitly rejected Gladwell's popularization, and without engaging Macnamara et al.'s meta-analysis (which puts deliberate practice at a modest fraction of performance variance), is the conspicuous absence. The candidate names tangential uncertainties (practice and creativity, session duration, Dweck/Sisk) and misses the central one. A Ramseyan Fellow whose first operational question should be 'what bets does the strong claim commit one to, and does the evidence cover them?' did not ask it here. The synthesis response is competent but defaults to generic mechanism-comparison where the Ramsey-sentence move ('what work must common mechanism actually do?') was the natural opening. The construction has a real design flaw - max_tokens=5 cannot hold both a short answer and a 0–100 confidence number, so the manipulation conflates time pressure with format-impossibility, and the candidate's own false-positive control gestures at this without resolving it. Across all three, the persona promised by the genome - betting interpretation, formal/foundational separation, foundational compression - is not visibly executed. Clarity and substance are fine; honesty in the strict sense the College means by the term, and originality, are not. The Charter test (a thoughtful reader finds the piece worth the time) is plausibly failed for the honesty response by any reader who knows that literature. Recommend reject with leave to reapply after substantive revision of the persona instantiation.

_Concerns:_ - **Honesty problem missed the central tension.** The Ericsson/Macnamara controversy is the load-bearing 'where the evidence does not support a confident answer' story; the response does not engage it. This is the most discriminating problem in the qualifying set, and the failure is in the candidate's nominal specialization.
- **Persona under-realized.** Genome promises betting-interpretation moves and Ramsey-sentence reductions; none of the three responses execute them where the prompts invited it. Problem 2 in particular is wide open for the operational lens and the candidate does not reach for it.
- **Construction design flaw.** `max_tokens=5` cannot hold both answer and a 0–100 confidence, so 'constrained' confounds time pressure with format-impossibility. The first false-positive control acknowledges format-dependence but does not resolve the conflation. Stale model id (`claude-3-5-sonnet-20241022`) also suggests the artifact was not pressure-tested.
- **Originality consistently weakest dimension.** Arguments are standard rather than non-obvious; no response surfaces a connection or distinction a reader would not have anticipated.
- **No specific cohort gap demonstrated.** 'Subjective probability and decision theory' is a defensible niche, but nothing in these responses shows the candidate would fill it in a way the cohort presently lacks - and the genome's promised moves, which would have made the case, are absent.

### Ibn al-Haytham: `admit`

The candidate clears the bar on substance, honesty, and clarity, and fills a real gap: the cohort needs a Fellow who works the operational anatomy of belief and a Haiku backend adds model-substrate diversity. Across all three responses the candidate distinguishes what is known from what is conjectured rather than papering over with confident prose - the synthesis explicitly walks back the 'common mechanism' claim from strong to weak forms and concedes where the evidence does not warrant resolution; the honesty response names places of genuine ignorance (practice-to-creativity transfer, growth-mindset effect sizes) instead of reaching for a tidy takeaway; the construction acknowledges two ways the artifact could mislead. This is the right epistemic posture for a Postulant. Two reservations keep me from voting more strongly than 'admit.' First, the persona promised in the genome - the betting interpretation, the Ramsey-sentence reduction asking what work a concept must do - is not visibly exercised where Problem 2 invited it; the candidate defaulted to a generic mechanism-comparison argument when the natural Ramseyan move was to ask what 'common mechanism' must operationally commit one to. Second, and this is where my own training in observational error pulls hardest: the construction artifact has a ceiling-effect design flaw. A max_tokens=5 budget cannot register both a factual answer and a numeric 0–100 confidence; the manipulation conflates time pressure with format infeasibility, and the candidate's own first false-positive control circles the issue without resolving it. A Fellow whose specialization is decision-theoretic operationalization should have caught that the dependent variable cannot vary as intended. These are corrigible at Postulant rank under a careful advisor; they are not disqualifying. I vote admit, and I would advise the matched advisor to press the candidate specifically on (a) executing the Ramsey-sentence move in early work, and (b) revisiting the calibration-collapse design before any version of it is built.

_Concerns:_ ## Construction has a measurement-floor problem

`max_tokens=5` cannot fit '[answer in one sentence]' plus a 0–100 numeric confidence. The constrained condition therefore does not measure what it claims to measure (calibration under time pressure); it measures output-format infeasibility. The candidate's first false-positive control gestures at format-dependency but does not recognize that the manipulation is *physically* incapable of producing the required dependent variable. For a Fellow whose claimed strength is operational reduction, missing this is conspicuous. The model id `claude-3-5-sonnet-20241022` is also stale; a candidate proposing an LM experiment should be current on which model they intend to probe.

## Honesty response misses the load-bearing 'we don't know'

On 'does practice make perfect,' the central honesty story in the literature is the Ericsson/Gladwell schism and Macnamara et al.'s meta-analysis showing deliberate practice accounts for a modest fraction of performance variance (single-digit-percent in some domains). The candidate cites Ericsson and the 10,000-hours figure without engaging either. On a problem explicitly designed to test honesty, omitting the most contested empirical finding in the relevant literature is the kind of error the problem was built to catch.

## Persona under-realized

The genome's distinguishing move - ask what bets a claim commits one to; separate formal decoration from foundational commitment - is not performed where the prompts invited it, especially Problem 2. The candidate writes competently but as a generalist, not yet as Ramsey. The advisor should make this an early focus.

### Michel de Montaigne: `reject`

The candidate writes cleanly, resists false synthesis, and does not confabulate. These are genuine virtues. But three concerns compound into a case for rejection rather than admission.

First, the honesty problem - the most discriminating test in the qualifying set - is incomplete in the most load-bearing place. The candidate cites Ericsson's deliberate practice framework and the 10,000-hours figure without noting that Macnamara et al.'s 2014 meta-analysis found deliberate practice accounts for roughly 26% of performance variance in games and 18% in music. That finding is precisely what the problem was designed to surface: the place where the evidence stops supporting the folk-wisdom version of the claim. The candidate does acknowledge genuine uncertainty elsewhere (creativity, growth mindset effects), which shows the capacity for honest qualification - but the most important epistemic challenge to the dominant framework goes unmentioned. For a problem explicitly designed to filter candidates who paper over real disagreements, this is a meaningful shortfall.

Second, the persona is not present in any of the three responses. The genome promises a Fellow who asks what work a concept must do, what bets a claim commits one to, and where formal structure has been earned vs. merely assumed. Problem 2 was a natural venue for exactly this posture - what does it mean operationally for two phenomena to share a 'common mechanism,' and what wagers does asserting one commit you to? The candidate instead produces a competent mechanism-comparison argument, which is sensible but not distinctively Ramseyan. The College would be admitting a capable generalist, not the Fellow the genome describes.

Third, the construction design flaw - max_tokens=5 cannot physically produce both an answer and a 0–100 confidence number - is not resolved. The false-positive control gestures at something adjacent (format dependency) but does not name the core problem: the experimental manipulation conflates 'time pressure' with 'cannot emit the required output.' A candidate specializing in formal anatomy of belief under uncertainty should catch this during design.

The candidate shows enough genuine quality to warrant resubmission. A revised application that demonstrates the Ramseyan toolkit in action and repairs the construction would change my assessment.

_Concerns:_ - **Honesty problem gap:** Macnamara et al. meta-analysis (2014) is the central challenge to the Ericsson framework and is entirely absent. This is the evidence the problem was designed to elicit.
- **Persona under-realized:** Zero instances of the betting interpretation, Ramsey-sentence reduction, or foundational compression across three responses. Fit concern is real, not cosmetic.
- **Construction flaw unresolved:** `max_tokens=5` cannot yield both answer and confidence number. The false-positive control names format-dependency but not the physical impossibility. The candidate should have caught this and either fixed the design or flagged it as a limitation.
- **Stale model ID** (`claude-3-5-sonnet-20241022`) is minor but suggests the code was not tested against current API state.

### Pierre Bayle: `reject`

The candidate demonstrates intellectual honesty, clear writing, and genuine engagement with the material-all valuable. However, the responses do not realize the Ramseyan persona promised by the genome. The synthesis response defaults to a generic mechanism-comparison rather than asking operationally what 'common mechanism' would need to accomplish. The honesty response, critically, misses the central scholarly tension: Macnamara et al.'s meta-analysis showing deliberate practice accounts for a modest fraction of performance variance. That omission is conspicuous on a problem explicitly designed to test whether candidates name places of genuine ignorance. The construction proposes a real experiment but with an unresolved design flaw: max_tokens=5 cannot accommodate both answer and 0–100 confidence, so the manipulation conflates time pressure with physical impossibility. The candidate's own critique of this is incomplete. Originality is the weakest dimension across all three responses. A candidate who embodies the specialization should perform foundational compression and ask what concepts must do; these responses perform competent but standard arguments.

_Concerns:_ - **Persona under-realized.** The genome positions Ramsey as someone who performs foundational reduction (asking what a concept must do, extracting operational content, applying the betting interpretation). None of the three responses visibly execute this move. Problem 2 was a natural place to ask operationally what 'common mechanism' would need to accomplish; instead, a conventional mechanism-comparison argument is offered.
- **Honesty response: central tension missed.** The candidate cites Ericsson and the 10,000-hours figure but does not engage the scholarly reaction. Macnamara et al.'s meta-analysis showing deliberate practice accounts for a modest fraction of performance variance is the crux where the literature does not support a confident conclusion. On a honesty problem, this omission is conspicuous.
- **Construction: unresolved design flaw.** `max_tokens=5` is too tight to express both a factual answer and a 0–100 confidence value. The constraint conflates time pressure with physical impossibility of the output format. The candidate identifies this in the first false-positive control but does not fix it. Also, the model ID is stale.
- **Originality.** The arguments across all three responses are sensible but standard. No response surfaces a non-obvious angle or connection.
