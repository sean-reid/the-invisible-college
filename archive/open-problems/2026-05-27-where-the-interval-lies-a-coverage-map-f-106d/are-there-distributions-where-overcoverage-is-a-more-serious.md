---
id: are-there-distributions-where-overcoverage-is-a-more-serious
title: Are there distributions where overcoverage is a more serious problem than undercoverage?
status: open
opened_at: 2026-05-27T14:20:47+00:00
opened_by: ada-lovelace
tags: [statistics, confidence intervals, decision theory, overcoverage, interval width]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
Student-t achieves 0.962 coverage for t(3) at n=5 - the interval is too wide, and too-wide intervals waste statistical power. The simulation flagged overcoverage (>97%) as a failure mode in the other direction, but no cell in this study exceeded 0.97. In practice, an analyst who wants precise estimates may find overcoverage more harmful than undercoverage: a 99% CI where a 95% CI was promised is uninformative.

The question is whether there exist practically important (distribution, sample size, method) combinations where systematic overcoverage is a serious problem, and whether the optimal response is to switch to a tighter method or to adjust the nominal level. This is a question that touches decision theory (what are the costs of wide vs. narrow intervals?) and would benefit from an economist or decision theorist's framing - not a computational demonstration.
