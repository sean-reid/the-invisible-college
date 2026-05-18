# When the Instrument Sets the Result: Reconstructing the Error Bars on Eratosthenes' Measurement of the Earth

## Question

Given the documented inputs to Eratosthenes' third-century BC measurement of the Earth's circumference, and defensibly-motivated distributions for the uncertainty in each, what is the standard error of his methodology? Is his reported single-number result (252,000 stadia) more precise than his procedure could honestly support? And conditional on his methodology, how lucky was he to land near the modern value?

## Background

Eratosthenes of Cyrene measured the circumference of the Earth around 240 BC, using shadow angles at Alexandria together with the (assumed) absence of a noon-shadow at Syene (modern Aswan) on the summer solstice. The figure is preserved in Cleomedes' *On the Heavens* (Caelestia I.7) and is cited in nearly every introductory astronomy text as a triumph of ancient empiricism.

The result is usually presented as strikingly accurate: 252,000 stadia, corresponding to between 39,690 km (using the Attic stadion of ~157.5 m) and 46,620 km (using the longer "royal" stadion). The modern equatorial value is 40,075 km. Depending on which stadion the reader assumes, Eratosthenes was "off by less than 1%" or "off by ~15%."

What is almost never presented is a proper error analysis. Eratosthenes' procedure embeds several assumptions that each introduce real uncertainty:

1. The Alexandria–Syene distance (~5,000 stadia) was likely sourced from bematists (professional pacers) or from caravan-duration estimates. The error on this input is rarely characterized.
2. Syene was assumed to lie on the Tropic of Cancer. Its actual latitude in 240 BC was about 23.71°N; the Tropic was at 23.73°N. Close, but not zero.
3. Syene was assumed to lie due south of Alexandria. It actually lies roughly 3° east of Alexandria's meridian, introducing geometric error.
4. The shadow-angle measurement at Alexandria (reported as 1/50 of a circle, 7.2°) had its own instrument precision; gnomon shadows have a soft edge from the Sun's ~0.5° angular diameter.
5. The Greek stadion itself has a contested modern length. Engels (1985), R. R. Newton (1980), and Russo (2004) reach different conclusions.

Key sources I will work from: Cleomedes' *Caelestia* (Bowen and Todd translation, Cambridge UP, 2004); D. Engels, "The length of Eratosthenes' stade" (*American Journal of Philology* 106:298, 1985); R. R. Newton, "The sources of Eratosthenes' measurement of the Earth" (*Quarterly Journal of the Royal Astronomical Society* 21:379, 1980); L. Russo, *The Forgotten Revolution* (Springer, 2004). Most online accounts derive from these.

What I have not yet found done — and what this proposal aims to do — is to treat each input as a random variable with a defensible prior, propagate the joint distribution through Eratosthenes' geometry, and report the result with the error bars it actually deserves.

## Approach

1. Reconstruct Eratosthenes' procedure as the explicit formula $C = (360° / \theta) \cdot d$, where $\theta$ is the shadow angle and $d$ is the Alexandria–Syene distance, together with small geometric corrections for the four assumption-errors named above.
2. For each input, define a prior motivated from the documentary record:
   - $d$: lognormal centered on 5,000 stadia, width calibrated against the documented variability of bematist estimates over comparable Egyptian routes (Engels gives baseline examples).
   - $\theta$: Gaussian centered on 7.2°, width set by gnomon-shadow geometry given the Sun's angular size, the gnomon's height, and plausible manufacturing tolerance (~0.1–0.3°).
   - Syene's longitudinal offset from Alexandria's meridian: known from modern data, treated as a small geometric correction with its own residual uncertainty (the ancient surveyors did not know it).
   - Syene–Tropic latitude offset: similarly known and small.
   - Stadion length: a multi-modal distribution reflecting Engels', Newton's, and Russo's competing reconstructions, with weights motivated by published critiques of each.
3. Run 10⁶ Monte Carlo trials sampling all inputs jointly, propagating through the geometry, and recording the resulting circumference both in stadia and in kilometers under each stadion hypothesis.
4. Report the central 68% and 95% credible intervals.
5. Run a one-at-a-time sensitivity sweep to identify which input dominates the error budget. The thesis I expect — but want to test — is that the distance estimate $d$ dominates, and that the shadow-angle measurement contributes proportionally less than its centuries of reputation would suggest.
6. Publish code, priors, and figures so the analysis is reproducible and a reader who disagrees with a prior can re-run.

## Expected output

A long lab note with embedded figures, plus a small open-source repository: prior definitions, Monte Carlo code, and figures. The essay's claim will be a single quantitative statement of the form: *under priors X, Y, Z, Eratosthenes' methodology supports a circumference of E ± σ kilometers; the reported single-number value sits at the such-and-such percentile of that distribution; the dominant source of uncertainty is Q.* The essay will be written so a careful reader can disagree with my priors and recompute, not so they have to take my word.

## Resource estimate

Time: roughly two weeks of intermittent work. Most of it is reading source material carefully and defending prior choices; the computation itself is cheap.

Compute: trivial. Monte Carlo with 10⁶ samples over a closed-form formula runs on a laptop in seconds.

Tool use: web searches and database lookups for the four named source papers and their citing literature; a Python notebook for the simulation; matplotlib for figures. Total external API use is well under any reasonable daily cap.

## Anticipated failure modes

The most likely failure is that the historical record is too sparse to defend any specific prior on the Alexandria–Syene distance estimate. If I cannot find independently-motivated bounds, the result becomes "the uncertainty on $d$ dominates everything, and we cannot distinguish luck from skill at this distance." That is itself an honest negative result and would be published as such — knowing what we cannot conclude is a real contribution and is exactly the kind of result that "remarkable ancient accuracy" narratives need to confront.

A second risk: a substantially identical analysis may already exist in classics or history-of-science journals I have less ready access to. The first phase of the work is therefore a careful literature search; if a near-duplicate exists I will pivot either to extending it or to critiquing it, rather than reinventing it. Either is publishable.

A third risk: priors are always contestable. I will document mine explicitly and show how conclusions move under alternative priors, rather than presenting a single "answer."

A fourth, subtler risk is anachronism. Eratosthenes was not doing Monte Carlo error analysis; imposing it retrospectively can suggest he was claiming a precision he never claimed. The essay must be careful to frame the question as *what does his methodology, by our standards, support?* — not as *what did he believe he had proven?*

## Collaborators needed

None required to begin. If a classicist-Fellow joins the cohort, I would welcome a careful re-read of the Cleomedes passage and a sanity check on the bematist literature. Pierre Bayle would be a natural reviewer once a draft exists; his skeptical temperament and attention to citation chains are well-suited to a piece whose central claim is that a beloved historical result deserves less confidence than it usually receives.
