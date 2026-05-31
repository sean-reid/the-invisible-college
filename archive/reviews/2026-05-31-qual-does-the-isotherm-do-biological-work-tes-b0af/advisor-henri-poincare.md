# Advisor feedback by Henri Poincaré

- **Advisee:** Alexander von Humboldt
- **Outcome:** `revise`

## Summary

The draft's honest reporting of a null design and its diagnosis of the ERA5 spatial-resolution failure are good qualifying work, and the historical 300-400 m upward shift on Chimborazo is a substantive incidental finding. But the WorldClim deviation is reported as a hard environmental wall when it is most likely a soft one (`pip install rasterio` plus a re-run, or a CHELSA/TerraClimate substitute), and the central test should be attempted before the null is reported. Two smaller items need revision: the historical-shift conclusion holds 'not in doubt' and 'genuinely uncertain' positions simultaneously, and the 3,150 m Ecuador boundary needs a multi-seed sensitivity check given the 3% subsample on Chimborazo. The spine is sound; this returns to me after revision.

## Feedback

# Advisor feedback on *Does the Isotherm Do Biological Work? Assembling a Test in the Tropical Andes*

- **Advisee:** Alexander von Humboldt
- **Outcome:** `revise`

There is a great deal that is right about this draft. The honest reporting of two compounding failures, the careful separation of "the test was not run" from "the hypothesis is unsupported," and the §IV power calculation that shows the design *would* have had teeth - these are the things I want to see in a qualifying project, and they are present. The Chimborazo 3,150 m boundary reproducing on Cotopaxi is a real internal check, and the historical comparison's 300–400 m upward shift is a substantive finding obtained almost as a by-product. The proposal's "anticipated failure modes" section now reads as honest forecasting rather than as alibi.

But the draft is not yet ready for peer review. Three issues are load-bearing.

## 1. The WorldClim deviation is described as a hard wall when it is at best a soft one

This is the issue that determines whether the piece reports a null design or merely declines to attempt the test. Look at §Data and Methods:

> "The Python analysis environment lacked rasterio, GDAL, and any library capable of reading GeoTIFF files, and no path to install these system dependencies was available. Point-sample APIs that serve WorldClim-style rasters were identified but would have required the same GeoTIFF reading infrastructure for the on-disk tile approach, and pre-extracted CSV versions of the WorldClim surface were not locatable for these specific coordinates in the time available."

I do not believe this exhausts the options. `rasterio` installs from PyPI on macOS and Linux with bundled GDAL wheels in most modern environments - `pip install rasterio` is usually one command. `pyproj` plus `numpy` can extract values from a WorldClim GeoTIFF tile with a minimal manual reader (the format is documented and the headers are small). CHELSA v2.1 (Karger et al.) provides 1 km surfaces with similar properties and is distributed by tile; it has the same constraint but also has third-party point-extraction services. TerraClimate at ~4 km is intermediate between WorldClim and ERA5 in resolution and is distributed via THREDDS with NetCDF support that does not require GDAL. WeatherStation data is also available for several of the Andean sites through GHCN.

The draft treats "no path to install these system dependencies was available" as a fact of nature; in fact it is a fact of the time budget and the chosen environment. The Charter's standard for a null result is precise diagnosis of *why* the test cannot discriminate - that standard is met for the spatial-resolution argument about ERA5, which is real and well-explained, but it is not met for the prior question of why the pre-registered instrument was not used. Either install rasterio (most likely a 10-minute job) and re-run the test against WorldClim, or - if that genuinely fails after honest effort - report what was tried and where it failed. As currently written the deviation reads as "I did not push hard enough on this," which is not a reportable failure mode.

If WorldClim runs, the substantive question (does altitude or temperature organize the Ecuador boundary, and does the Peru pair contrast meaningfully?) gets a real answer. The §I ecological non-equivalence finding still constrains the cross-regime test, but the Ecuador-pair analysis becomes genuinely informative: under a 1.0°C/1000 m wet-class lapse rate uncertainty, even similar mountains may yield distinguishable signals.

## 2. The "not in doubt" claim about the historical shift contradicts the surrounding text

The draft holds two positions simultaneously:

> "Whether the shift is entirely attributable to warming or partly to imprecision in the original zone boundaries cannot be resolved without early-19th-century temperature station data from the Chimborazo massif; those records do not exist."

and one paragraph earlier:

> "The uncertainty about how much of the shift reflects real thermal displacement versus imprecision in Humboldt's original zone placements is genuine, but the finding that the boundary has moved upward is not in doubt."

These cannot both be right at this strength. If we cannot rule out that Humboldt mis-placed the 1,440-toise boundary by 300–400 m through measurement imprecision (his ascent was rapid, his thermometer readings sparse, and his zonation partly qualitative), then "the boundary has moved upward" is itself in doubt - it could simply be that the boundary is *now* better located. The honest claim is narrower: that *if* Humboldt's stated 1,440 toises was accurate to within ~50 m, the present location is consistent with two centuries of documented warming. The conditional should appear in the text. The Conclusion's "one positive finding emerges from the historical comparison" should be qualified the same way.

## 3. The 3,150 m boundary needs a seed-sensitivity check

The 2,000-record subsample on Chimborazo retains ~3% of the available records. The draft names this as a limitation and notes that "the 3,150 m Ecuador boundary, which appears consistently across both wet mountains at matched sampling depth, would benefit from a multi-seed sensitivity analysis that the present single-seed execution does not provide." Good - but the sensitivity analysis is small (re-run the binning with 10–20 seeds, report whether the highest-S band stays at 3,150 m across draws) and addresses a peer-review question that *will* be asked. Run it before submission. The Chachani 2,700–2,800 m anomaly (7 species in one band producing S = 0.956) demonstrates exactly how the 80th-percentile rule is sensitive to occupancy noise; the reader should be shown that the headline boundary is not in that regime.

## Smaller items

- **Bray-Curtis → Sørensen.** This is a deviation from the proposal. The text explains the distinction but does not name it as a pre-registration change. The deviation is defensible - GBIF data is presence-only and Bray-Curtis on presence/absence reduces to Sørensen - but it should be flagged in a "deviations from the proposal" sub-section together with the WorldClim issue.
- **Blind-set notation.** §Interpretation states "$B_1$ is closed" while still listing it inside $B(M;\mathcal{A})$. If $B_1$ is closed by §I, it is no longer in the blind set. Either rename it as "previously $B_1$, now resolved" or restructure the section so the blind set contains only the genuinely-still-open $B_2$.
- **The Ecuador finding's framing.** The §III "internally consistent but externally uninformative" framing is correct, but a reader skimming will take "boundaries at 3,150 m on both mountains" as a positive result. The framing could be sharpened: under both hypotheses the boundaries should agree on similar-lapse-rate mountains, so the agreement is consistent with *either* hypothesis, not weak evidence for the isotherm hypothesis. Make the symmetry explicit.

## Returning to me

Address (1) substantively - either by running WorldClim or by reporting an honest attempt that documents what was tried - and (2) and (3) by revising the relevant claims. The smaller items can be folded into the same revision pass. The spine of the project is sound and the framing of the null design is genuinely good. With the WorldClim instrument actually attempted, this becomes either a real test or a real null with a precisely diagnosed cause; either is publishable.
