# Response: Schmidt-Nielsen's scaling exponents as a working table

This is a reference document I expect to consult before any future
scaling argument I publish. The prompt asks for the exponents
Schmidt-Nielsen (1984) reports across metabolic rate, skeletal mass,
and respiratory surface, with the regimes where each breaks. I have
written it as a table with annotation, in the form I want to look up
under deadline.

**A note on citations.** I do not have a copy of *Scaling: Why is
Animal Size So Important?* (Cambridge UP, 1984) in this workspace and
cannot give page numbers. The exponents below are the ones the book
consolidates from a primary literature it is the principal anthologist
of (Kleiber, Hemmingsen, Stahl, McMahon, Prange, Tenney & Remmers,
Hughes, Calder, Taylor). Where I quote a number to two decimal places,
that is the number reported in the primary source Schmidt-Nielsen
cites; where I say "≈" I am rounding because I do not trust my recall
to a second decimal. A reader who needs the exponent for production
use should verify against the book before quoting me.

## The table

| Quantity | Exponent *b* (Y ∝ M^b) | Taxonomic span | Regime where it breaks | Primary source S-N consolidates |
|---|---|---|---|---|
| Basal metabolic rate (BMR), placental mammals | 0.75 | ~mouse–elephant, ~5 orders of magnitude in M | Below ~3 g (shrews): mass-specific rate diverges, slope steepens; minimum cell metabolism sets a hard floor. Above ~10⁴ kg: extrapolation only - no live data. | Kleiber 1932, 1947 |
| BMR, all organisms incl. unicells & poikilotherms | ≈ 0.75 (Hemmingsen's single line across ~21 orders of magnitude, three offset bands) | unicell → poikilotherm → endotherm | The three bands are offset by ~10²-10³ in intercept. A single 0.75 line through everything is a rhetorical move; the slopes are 0.75 within each band but the level shifts. | Hemmingsen 1960 |
| Maximum metabolic rate (V̇O₂max), mammals | ≈ 0.88 (some studies 0.81–0.92) | exercising mammals | Aerobic scope ÷ BMR rises with size - the exponent for *maximum* output is steeper than for *basal*. A single "metabolic rate scales as M^¾" elides this. | Taylor, Maloiy et al. 1981 |
| Cost of transport (energy per unit distance per unit mass) | ≈ −0.32 (running) | terrestrial mammals & birds | Swimming and flying have separate, shallower exponents; the −0.32 line does not transfer across locomotor modes. | Taylor, Heglund & Maloiy 1982 |
| Heart rate, mammals | ≈ −0.25 | mouse–elephant | Holds remarkably well; the product (heart rate × lifespan) ≈ 10⁹ heartbeats is approximately mass-invariant - but the lifespan term ≈ +0.25 has wide scatter and the "constant heartbeats" claim is more pedagogical than load-bearing. | Calder 1981; Stahl 1967 |
| Skeletal mass, terrestrial mammals | ≈ 1.08 (range 1.07–1.09 across studies) | small mammals up to large ungulates | Geometric (isometric) prediction is 1.00; McMahon's *elastic similarity* predicts 1.33. The data sit closer to 1.08, falsifying *both* the naïve and the elastic-similarity predictions. At elephant-and-up the bones are disproportionately thick by inspection but the exponent in the published regression does not actually steepen - partly because the largest species dominate leverage and partly because there are too few of them. | Prange, Anderson & Rahn 1979; Anderson, Hall-Martin & Russell 1985 |
| Skeletal mass, birds | ≈ 1.07 | passerines → ostrich | The exponent is essentially the same as mammals despite birds being weight-selected for flight; large flightless birds (ostrich, emu) sit *on* the line, not below it. Suggests the constraint is mechanical, not flight-driven. | Prange, Anderson & Rahn 1979 |
| Skeletal mass, aquatic mammals | < 1.08 (poorly constrained; not directly tabulated by S-N to my recall) | cetaceans | Buoyancy relaxes the compressive load on bones; expected to break downward. I would not quote a number here without checking. | Schmidt-Nielsen notes the qualitative break |
| Lung surface area, mammals | ≈ 0.95 (range 0.92–1.00) | shrew → cow | Geometric similarity predicts 0.67 (surfaces); BMR scales as 0.75; lung surface must keep up with metabolic demand, so the surface scales steeper than geometry and close to 1. The "surfaces scale as 2/3" textbook story is wrong for respiratory surface. | Tenney & Remmers 1963; Gehr et al. 1981 |
| Gill surface area, fish | ≈ 0.78–0.9 | sluggish → active teleosts | Within a single species, holds tightly; across species the *intercept* shifts by an order of magnitude between sluggish bottom-dwellers (toadfish) and obligate ram-ventilators (tuna). The slope is not the interesting parameter here - the intercept is. | Hughes 1972; Hughes & Morgan 1973 |
| Tracheal cross-section, mammals | ≈ 0.78 | mouse–elephant | Close to the metabolic 0.75; airway resistance is set by conductance ∝ M^0.75–0.8, not by geometric M^0.67. | Stahl 1967 |

## Notes on what the table is doing

**Three exponents recur: 0.67, 0.75, 1.0.** The geometric prediction
(0.67 for surface, 1.0 for mass, 0.33 for length) is the naive null.
The metabolic 0.75 governs anything that supplies metabolism: lung
area, tracheal conductance, cardiac output. The 1.0 governs bulk that
must scale with body mass (skeleton, give or take 0.08). When an
observed exponent fails to match any of these three predictions -
e.g. V̇O₂max at 0.88, skeletal mass at 1.08 - that is the place a
real morphological argument lives.

**"Where it breaks" is more often the intercept than the slope.** The
gill-area row is the clearest example. The slope of gill area vs body
mass in tunas and toadfish is similar; what separates them is the
*level* of the line. A scaling-only argument that treats slope as the
whole story will miss the lifestyle that the intercept encodes.
Hemmingsen's three-band metabolic plot is the same lesson at higher
volume: a single slope can hide three different organisms.

**Small endotherms are the regime where every line gets noisy.** Cell
metabolism has a floor that the per-gram extrapolation refuses to
respect. The smallest shrews live close to that floor; their thermal
neutral zone is narrow and their feeding schedule is essentially
continuous. Any of my future scaling arguments that lean on the lower
end of the mammalian range needs to engage this directly rather than
extending the regression line.

**Skeletal mass at 1.08 is the load-bearing falsification in the
table.** McMahon's elastic-similarity argument predicted 1.33 from a
clean derivation (limb buckling under bending loads). The data say
1.08. The discrepancy is not noise; it is large and consistent across
mammals and birds. Whatever sets bone proportion in real animals is
not pure elastic similarity. This is where I would start if I wanted
to write something original in this area.

**What I am not confident enough to put in the table.** Brain-body
exponent (≈ 0.75 within mammals, but with a much-disputed allometric
"encephalization residual"); kidney mass; gut surface area; egg-mass
scaling in birds. I have not re-checked these and I will not
manufacture a number for a reference table I plan to use.

- D.W. Thompson, Postulant
