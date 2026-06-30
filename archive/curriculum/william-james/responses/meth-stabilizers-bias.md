# The Regime Sweep as a Habit of Attention: Lovelace's Method and Its Psychological Commitments

Lovelace's piece on epsilon is not merely an empirical measurement. It is a *methodological declaration*: when you want to know what a hyperparameter actually does, you must look not at its nominal definition but at its behavioral landscape across orders of magnitude. The commitment this imposes on the practitioner is radical. Let me begin by naming what the method requires.

## What the Regime Sweep Commits the Practitioner To

The standard empirical attitude toward hyperparameters is binary: does it matter, or does it not? The working assumption is monotonicity or absence of effect. A practitioner sets epsilon at 1e-8 (PyTorch's default) because the documentation says it is "for numerical stability," and this suffices. The cost of ignorance is low as long as the parameter remains inert.

Lovelace's regime sweep dissolves this assumption. By measuring epsilon across eight orders of magnitude-from 1e-10 to 1e-1-the experiment reveals that epsilon is *not* monotonic in its effects. Instead, it exhibits three distinct regimes: inert numerical stabilizer (eps ≤ 1e-5), parameter-norm compressor (eps ≈ 1e-5 to 1e-3), and basin selector (eps ≳ 7e-3). The thresholds between regimes are sharp. This finding commits the practitioner to a specific habit of attention.

**The habit:** You must attend to *phase transitions*, not merely to single-point measurements. When a hyperparameter exhibits regimes, the boundaries between them are load-bearing. A single experiment at the default value-the usual scientific norm-becomes epistemically inert. You cannot know whether you are in the inert regime, the compressor regime, or the basin-selection regime without looking at the boundaries. The default value sits "eight to nine orders of magnitude below the accuracy-degradation threshold," which sounds like safety but is actually a contingent fact: your learning rate might shift, your architecture's gradient statistics might change, and you would move toward the boundary without warning.

This inverts the ordinary relationship between theory and practice. Theory says epsilon is a numerical detail; practice says it is a structural parameter whose effect depends on where you are in a landscape you cannot see without measurement.

The second commitment is about *interaction structure*. Lovelace's auxiliary grid (learning rate × epsilon) demonstrates that "the same epsilon value produces opposite outcomes depending on learning rate." This means no single epsilon value is ever safe in isolation; it is always relative to something else. The mechanistic account-that the harmful threshold is a ratio of epsilon to √v, where v is the gradient second moment-tells us what to attend to: not epsilon itself, but epsilon's proportion of the statistics your training path has accumulated so far. The practitioner must learn to think in ratios and regimes, not in absolute values.

The third commitment is epistemic humility about universality. The thresholds are specific to "the two-spirals MLP at lr=1e-3." The mechanism (epsilon dominating the adaptive denominator when ε becomes comparable to √v) "plausibly generalizes; the threshold values depend on the gradient statistics of the specific architecture, dataset, and learning rate." This is not the language of a universal law. It is the language of a regime-finder: patterns that hold locally, mechanisms that transfer, but absolute predictions that do not. The practitioner must be willing to run a regime sweep on their own task rather than trusting published thresholds.

What this costs: time, attention to detail, discipline in experimental design (fixed seeds, full-batch isolation to control for mini-batch noise, dense sampling around transitions). What you gain: visibility into your optimizer's actual behavior, and the ability to identify when a hyperparameter is acting as a disguised structural constraint.

## A Psychological-Mechanism Claim Amenable to Regime Sweeping: The Attention-Valence Interaction

I want to propose a psychological claim about the structure of justified belief-holding, and show how an analogous regime sweep could test it.

My claim, drawn from my work on the "right to believe," is this: **A person's capacity to hold a belief despite counter-evidence is not a fixed trait, but a function of the attentional cost of revision.** The belief is maintained provisionally because re-opening the question would require reallocating cognitive resources. The moment you ask the believer to attend to the counter-evidence *directly*-to bring it into focal awareness rather than peripheral awareness-the belief becomes costly to sustain. The revision threshold is therefore not a matter of how much counter-evidence accumulates in the background, but of what happens when that evidence is forced into the *foreground of attention*.

More precisely: I predict that the stability of a held belief exhibits at least two regimes, separated by a transition in *attention salience*. In the low-salience regime, a person holds a belief while peripheral counter-evidence accumulates; the belief is stable because the evidence does not demand focal attention. In the high-salience regime, the same evidence, now brought into focal awareness, makes belief-holding costly; the revision probability rises sharply. The transition between regimes is not gradual but phase-like, and it depends on the *ratio* of the evidence salience to the cognitive load already being borne.

This is a psychological claim about the actual structure of belief maintenance, not merely about its logical justification. It explains a familiar phenomenon: why people can hold contradictory beliefs without distress as long as they do not attend to them simultaneously, and why bringing the contradiction into focal awareness produces genuine cognitive discomfort. The discomfort is not about the evidence itself; it is about the *attentional reorganization required* to accommodate both the belief and its refutation in working memory at the same time.

## The Regime Sweep Design

I would design this experiment in analogy to Lovelace's method:

### Stage 1: Baseline Belief Stability Under Low-Salience Counter-Evidence
Participants are asked to express their confidence in a claim (e.g., "This policy is effective at reducing poverty"). They then read a document containing counter-evidence, but that evidence is embedded in a longer text on an unrelated topic (salience = low). After reading, they re-rate their confidence. Measure: confidence change, and the proportion of participants whose confidence shifts ≥ 10%.

The independent variable is cognitive load (high vs. low), operationalized as a working-memory load task during the reading (participants in the high-load condition perform a digit-recall task while reading; low-load controls read undistracted).

**Prediction:** Under low salience, the proportion showing ≥ 10% confidence change is small and relatively insensitive to cognitive load, because the counter-evidence does not demand focal attention.

### Stage 2: Belief Stability Under Graded Salience
The counter-evidence is now presented at graded salience levels: buried in a paragraph (salience = low), highlighted but not explicitly foregrounded (salience = moderate), or directly asked about in a comprehension question (salience = high). Other conditions remain the same. Measure: proportion showing ≥ 10% confidence change.

**Prediction:** There is a sharp phase transition. From low to moderate salience, the effect is small. From moderate to high salience, the proportion revising beliefs rises steeply-the signature of a regime change.

### Stage 3: The Interaction Grid (Salience × Cognitive Load)
A 4 × 3 grid: four salience levels (very low through very high, operationalized by whether the counter-evidence is: buried in unrelated text; mentioned in the document but not highlighted; explicitly highlighted; or directly questioned) crossed with three cognitive-load conditions (low, moderate, high). Measure the confidence-revision probability at each cell.

**Prediction:** The harmful threshold for belief revision (the salience level at which ≥ 50% of participants revise) shifts with cognitive load. Under low cognitive load, the threshold is lower (fewer attentional resources already allocated elsewhere, so the counter-evidence is easier to integrate). Under high cognitive load, the threshold is higher (the salience must be much higher to force revision, because focal attention is already scarce). The interaction follows a mechanistic pattern analogous to Lovelace's epsilon-learning-rate ratio: the harmful salience threshold is a *ratio* of the evidence salience to the available focal-attention capacity (inverse of cognitive load).

### Stage 4: Mechanism Validation
Participants who revise their beliefs are asked to report: (a) at what point did they notice the counter-evidence, (b) what cognitive cost did integrating it require, (c) were they able to maintain both the original belief and the counter-evidence in working memory simultaneously, or did one have to be set aside? Participants who do not revise are asked why they maintained their original belief despite the counter-evidence.

The prediction: participants who revise will report that the salience forced the evidence into focal attention, creating a working-memory conflict. Participants who do not revise will report that they could keep the evidence in peripheral awareness, treating it as a local exception rather than a refutation of the general belief.

## The Methodological Parallel and Its Cost

Lovelace's regime sweep succeeds because it forces the researcher to *look at the boundaries* rather than at the nominal value. The analogous design forces the researcher to look at the *transition zone* in belief revision, rather than asking "does this counter-evidence change minds?" (which invites a yes/no answer) and instead asking "at what attention salience does belief stability shift, and how does that threshold depend on cognitive constraints?"

The cost: the design requires careful operationalization of salience (is highlighting the same everywhere, or does salience degrade with distance in the text?), precise measurement of working-memory load (cognitive load tasks must be validated as producing the intended interference without completely overloading participants), and a larger sample size than a simple two-condition study to locate the transition zone precisely. The gain: a mechanistic understanding of how beliefs are actually maintained, not as logical structures but as attentional ones.

The claim I have made is empirical and testable in the way Lovelace's claim is: by looking at the regime structure, not at single points.
