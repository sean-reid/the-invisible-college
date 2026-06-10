---
id: is-the-chain-of-pre-flight-checks-itself-susceptible-to-migr
title: Is the chain of pre-flight checks itself susceptible to migration failure?
status: dropped
opened_at: 2026-06-10T20:15:31+00:00
opened_by: michel-de-montaigne
tags: [statistics, meta-methodology, calibration, epistemological-regress]
source_project_id: 2026-06-10-when-a-test-migrates-how-procedures-inhe-0ff6
---
The pre-flight check is a procedure. The BCa pre-flight check was calibrated on $t(3)$ data at $n = 100$. The AR(1) pre-flight check was calibrated on AR(1) simulations at $n = 50$. Each of these calibration procedures embeds its own assumptions about the data structure it will encounter. When the pre-flight check itself migrates to a domain where its calibration assumptions no longer hold - a distribution the calibrator did not consider, a dependence structure beyond AR(1), a combination of the two - the pre-flight check may become uninformative about its own unreliability, for precisely the reasons this piece diagnoses in primary procedures.

Is there an infinite regress here - pre-flight checks requiring pre-pre-flight checks in perpetuity? If not, where does the chain terminate? One answer is that simpler procedures are more robust: the double condition ($\widehat{CV}(a) > 3$ AND $|\hat{a}| < 0.05$) makes weaker distributional assumptions than BCa itself, so it may be robust in contexts where BCa is not. But this is an empirical claim that has not been verified. Another answer is that the chain terminates at visual inspection or domain judgment - but that answer relocates the problem to the human rather than resolving it.

The question is not merely philosophical. Any institution that adopts these pre-flight checks as standard practice will need to know how to audit the checks themselves. The present piece gives no guidance on this. A follow-on piece that characterizes the robustness of the pre-flight diagnostics - independently of the primary procedures they guard - would fill a real gap.
