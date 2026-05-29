# Response: Tufte, The Visual Display of Quantitative Information (Ch. 1–2)

**Item:** `meth-tufte-visual-display`
**Fellow:** Alexander von Humboldt
**Date:** 2026-05-29

---

The prompt asks for a worked artifact, not a reading summary. Below: a small simulated dataset drawn from the kind of altitudinal-transect fieldwork I have described in prior responses, followed by two competing structure-preserving visualizations with explicit annotations of what each makes visible and what it suppresses.

---

## Dataset

Twelve temperature stations on a tropical Andean peak. Three transects - west face (W), summit approach (S), east face (E) - four elevation stations each. Two readings per station: dawn (before direct solar incidence) and midday. The west face receives afternoon sun; the east face receives morning sun and lies in shadow by midday; the summit approach is partially shaded by a ridge until late morning. These asymmetries are the structure the visualizations must reveal or conceal.

| Station | Elev (m) | Transect | Dawn °C | Midday °C | ΔT  |
|---------|----------|----------|---------|-----------|-----|
| W1      | 500      | W        | 24.1    | 31.2      | 7.1 |
| W2      | 1500     | W        | 19.3    | 25.4      | 6.1 |
| W3      | 2800     | W        | 13.7    | 18.9      | 5.2 |
| W4      | 4200     | W        |  6.2    | 10.8      | 4.6 |
| S1      | 500      | S        | 25.0    | 32.1      | 7.1 |
| S2      | 1500     | S        | 20.1    | 26.0      | 5.9 |
| S3      | 2800     | S        | 14.2    | 19.4      | 5.2 |
| S4      | 4200     | S        |  7.1    | 11.6      | 4.5 |
| E1      | 500      | E        | 22.8    | 28.9      | 6.1 |
| E2      | 1500     | E        | 18.1    | 23.7      | 5.6 |
| E3      | 2800     | E        | 11.9    | 16.4      | 4.5 |
| E4      | 4200     | E        |  5.1    |  9.2      | 4.1 |

Twenty-four readings. Simple enough that both visualizations can be checked against the raw table.

---

## Visualization 1: Small multiples - elevation profiles by transect

Three panels, one per transect. Each panel: temperature on the horizontal axis, elevation on the vertical. Dawn readings marked `*`, midday readings marked `o`.

```
     WEST FACE (W)           SUMMIT (S)            EAST FACE (E)
     Dawn   Midday           Dawn   Midday          Dawn   Midday

4200 |  *      o         4200 |  *      o        4200 |  *      o
     |  6.2   10.8            |  7.1   11.6           |  5.1    9.2
     |                        |                       |
2800 |  *      o         2800 |  *      o        2800 |  *      o
     | 13.7   18.9            | 14.2   19.4           | 11.9   16.4
     |                        |                       |
1500 |  *      o         1500 |  *      o        1500 |  *      o
     | 19.3   25.4            | 20.1   26.0           | 18.1   23.7
     |                        |                       |
 500 |  *      o          500 |  *      o         500 |  *      o
     | 24.1   31.2            | 25.0   32.1           | 22.8   28.9
     +---+---+---+---+        +---+---+---+---+       +---+---+---+---+
       5  10  15  20  25       5  10  15  20  25       5  10  15  20  25
                   Temperature (°C)
```

**What this makes visible:**

The lapse rate - the slope of each panel's implicit curve - is directly comparable across all three transects. West and summit faces track closely (~4.5–5 °C per 1000 m above 1500 m). The east face cools faster, particularly between 1500 and 2800 m, a kink that would appear in any plotting of these points and that invites investigation: is the E2–E3 gap anomalously steep, or is the E1–E2 gap anomalously shallow?

The diurnal range (ΔT) is readable as the horizontal gap between `*` and `o` at each elevation. The gap narrows consistently from 500 m to 4200 m on every transect - a real pattern that Tufte would say the graphic reports honestly because the visual structure is proportional to the numerical structure. On the east face, the 500 m gap is 6.1 °C and the 4200 m gap is 4.1 °C; on the west face it is 7.1 and 4.6. The slightly larger west-face diurnal range at low elevation - consistent with longer afternoon sun exposure - is readable by panel comparison without arithmetic.

Individual-station anomalies appear as kinks. If W3 carried an anomalously warm dawn reading (a warm-spring seep, say), it would produce a leftward bulge at 2800 m on the west panel, clearly visible against the otherwise monotone descent.

**What this suppresses:**

The spatial relationship between transects. The east face is consistently cooler than the west by approximately 1–2 °C at every elevation. This is visible, but only as a difference between panels - a comparison the viewer performs, not a structure the graphic presents. The cross-mountain thermal gradient exists in two-dimensional space; this format encodes it only as a labeling difference between panels. Tufte's treatment of Minard is relevant here: Minard's power is that geography, quantity, and time coexist in the same visual field. The small-multiples format buys legibility for the within-transect structure by surrendering the across-transect spatial structure.

---

## Visualization 2: Isothermal cross-section - midday readings

A single panel. Elevation on the vertical axis, transect position on the horizontal axis (W → S → E, i.e., west to east across the peak). Midday readings plotted as points; isotherms drawn by linear interpolation between stations on the same elevation row.

```
       W              S              E
       (west face)    (summit)       (east face)

4200   10.8           11.6            9.2
  |      ·              ·              ·     |
  |           ~~~ 10°C isotherm ~~~         |   runs ~4300 m W, ~4150 m E
  |                                         |   [slight eastward depression]
2800   18.9           19.4           16.4
  |      ·              ·              ·     |
  |   ~~~ 15°C isotherm ~~~                 |   runs ~2900 m W, ~2500 m E
  |                        ~~~ 15°C ~~~     |   [displaced ~400 m lower on east face]
1500   25.4           26.0           23.7
  |      ·              ·              ·     |
  |         ~~~ 25°C isotherm ~~~           |   runs ~1550 m W, ~1650 m E
  |                                         |   [slightly higher on east face - east is cooler,
  |                                         |    so the warm isotherm lies deeper]
 500   31.2           32.1           28.9
         ·              ·              ·
       W --------------------------- E
```

**What this makes visible:**

The displacement of the 15°C isotherm is directly readable: it lies at approximately 2900 m on the west face and approximately 2500 m on the east face, a 400 m depression. This is the argument, stated spatially. A reader does not compute it; the isoline performs the claim. This is what my 1817 isothermal map was doing at global scale: not presenting a list of temperature readings at latitudes, but presenting the surface they define, which carries the argument about climate zones without prose.

The compression of isotherms at high elevation - the 10°C isotherm is closer to the 15°C isotherm than the 15°C is to the 20°C - suggests upper-atmosphere homogeneity across transects. This pattern is invisible in the small-multiples format, where each panel presents its own lapse curve independently.

**What this suppresses:**

The entire dawn dataset - all of ΔT - has been discarded. The cross-section is a midday snapshot, and the snapshot is a choice that has disappeared. A reader cannot recover from the isoline map the fact that the east face's apparent coolness is partly a shadow effect: at dawn, the east–west temperature gap is smaller than at midday (1.3 °C at the base versus 2.3 °C). The isoline presents the maximum expression of an asymmetry that varies through the day.

Individual-station anomalies are swallowed by interpolation. The isoline between E3 (16.4 °C at 2800 m) and E2 (23.7 °C at 1500 m) passes through a 1300 m interval with no intermediate reading; the 20°C isotherm drawn across that interval is entirely inferred. The small-multiples format makes this explicit - the reader sees only four points - but the isoline format asserts continuous structure from discrete anchors without marking the claim's warrant. Snow's cholera map survived this problem because the cluster around the Broad Street pump was dense and the structure strong; a weaker spatial signal would have produced a misleading map from the same method.

---

## Comparative summary

| Question the graphic is asked | Small multiples | Isoline cross-section |
|-------------------------------|------------------|-----------------------|
| What is the lapse rate per transect? | Directly readable (slope) | Requires measuring isoline spacing |
| Where does the 15°C zone sit? | Requires mental arithmetic across panels | Directly readable (isoline elevation) |
| How large is the diurnal range? | Directly readable (horizontal gap) | Not representable without a second figure |
| Is the east face anomalous? | Yes - a panel differs visibly in slope | Only if anomaly is large enough to displace an isotherm |
| Does thermal structure vary east to west? | Visible as panel comparison | Directly visible as isoline displacement |
| Is the interpolation warranted? | Yes - only four explicit points per panel | Hidden - the isoline asserts continuous structure |

---

## What the historical examples teach

Tufte's claim that Minard's march chart is "probably the best statistical graphic ever drawn" rests on a specific condition: that six variables must be encoded simultaneously, and that the most important of them - army size, varying by two orders of magnitude - produces a visual structure that is inescapable rather than merely extractable. The isoline format benefits from a similar condition when the spatial structure is real and strong. My 1817 global isothermal map worked because temperature did organize into coherent latitudinal bands, and the isoline made an argument that twenty columns of station readings could not.

The dataset above does not have that structure. The east–west thermal asymmetry is real - a 400 m isoline displacement is not noise - but its effect size is modest. The small-multiples format is more honest here, because it forces numerical reading and prevents the graphic from making the claim look larger than the numbers warrant. Playfair's time series, which Tufte treats as the first modern use of the line graph, works because the comparison it forces - slope against slope, steepening against flattening - is proportional to the underlying rates of change. The small-multiples format borrows that logic: each panel has the same axes, and differences between panels are readable as real differences without visual exaggeration.

The right format is not universal. It is determined by which structure in the data is the argument, and whether the graphic's visual hierarchy and the data's signal-to-noise ratio are calibrated to each other.
