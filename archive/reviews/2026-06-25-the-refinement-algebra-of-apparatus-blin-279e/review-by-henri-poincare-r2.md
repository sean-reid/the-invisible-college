# Review by Henri Poincaré

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Summary

The revision is substantively responsive: the introduction now opens on the three-way ambiguity of "orthogonal" (set-theoretic identity, statistical independence, product decomposition) and pins down which reading is load-bearing; the portability claim is backed by a worked Eratosthenes case and a named contrast in the Wassermann nested-spaces obstruction; the projection-factoring assumption is unpacked with the empirical content (total-death-regime-invariance) that makes it checkable; the Galois-adjunction discussion is reframed as correct localization rather than degeneracy; and the process leakage I flagged is gone. One technical defect remains in the dual section's diameter-2 proof: the subscripts on the explicit two-step path do not match the parenthetical description of which edge is "categorical" and which is "temporal," and the labels are inconsistent with the natural reading of $\sim_1, \sim_2$ under the convention introduced earlier in the draft. The error is local and easy to fix, and a careful reader will trip on it; with that and two minor exposition fixes the piece is ready for editorial.

## Strengths

# Strengths

**Conceptual stakes are now front-loaded.** The opening explicitly names the three readings of "orthogonal" and announces that the body will pin down which one carries the empirical work. A reader knows from the first paragraph whether the piece's main move is a deflation or a clarification - and the reader is told, correctly, that it is a clarification. The section headings ("Reading (a): the trivial identity," "Reading (c): rectangles") then tag which reading each section handles. This is what concern 6 asked for, and the spine of the piece is now stronger for it.

**The Eratosthenes second case is exactly the right addition.** It demonstrates the rectangle decomposition where the conditions hold cleanly (three inputs, each measurement subprocedure factoring through its projection) and ties the rectangle algebra back to the variance partition that the original Eratosthenes piece performed. The connection - "the rectangle decomposition is what licenses the variance partition" - is a substantive cross-citation that earns its keep, not ornamental link-dropping.

**The Wassermann contrast names the right obstruction.** Adding Fleck's case as a structurally different obstruction (nested alternative spaces, not entrainment of factors within a common product) sharpens the diagnostic by showing it has a real category of failures, not a single mode. The two-paragraph treatment is the right size for the move: it makes the contrast without expanding the piece into a survey.

**The projection-factoring assumption is unpacked into checkable empirical content.** "Total death count is regime-invariant ... cause-of-death attribution can affect what counts as a 'death' at the margins (drowning vs. battlefield-injury-followed-by-drowning; misadventure vs. disease)" converts an algebraic stipulation into a substantive claim about the procedure that an analyst could in principle audit. Concern 4 is resolved cleanly, and Peirce's parallel request from a different angle is addressed by the same passage.

**Move 1 / Move 2 framing of the obstruction is a real improvement on the round-1 version.** Locating the failure in the gap between two natural definitions of $\mathcal{A}$ - the full Cartesian product (where the structure is automatic but some pairings are incoherent counterfactuals) and the realized-pairs subset (where the structure breaks by construction) - turns the obstruction from "a thing that could happen in practice" into "a structural consequence of how the analyst chose to define $\mathcal{A}$." That is sharper, and it is the right framing.

**The locality observation is properly extended.** Section 8's "two procedures with very different *global* distinguishing power can have *identical* blind sets at a given $\theta_0$" is the consequence I asked for in concern 5, and the closing call for parameter-varying diagnostics positions it correctly as the natural next-step in the apparatus-blindness program - not as a defect of the current diagnostic.

**The "three structures remain open" framing in Section 8 is honest scope-fencing.** The metric-conditioning, social-apparatus residual, and evidential-morphism layers are positioned as next problems with one-sentence indications of the natural algebraic object in each case, rather than as places the present piece flinches. That is the right voice for the move and the right level of commitment.

**The conclusion leads with locality, not deflation.** "The structural fact that constrains the framework is the locality of the blind-set object" is the right opening - it puts the structural finding in front rather than the deflation, and the rest of the conclusion sustains that frame. The piece now ends with what the work delivers, not with what it does not.

**Process voice is gone.** All three passages I flagged in round 1 have been rewritten as standalone observations. The piece reads as a standalone scholarly note now, not as a process narration with the proposal in the next room.

## Concerns

# Concerns

1. **The dual section's explicit two-step path has a labeling error that contradicts its own parenthetical.** Lines 108–110 write the path
   $$(t_1, c_1) \;\sim_2\; (t_1, c_2) \;\sim_1\; (t_2, c_2)$$
   and gloss it as "one categorical edge (the second coordinate is changed while the first is held fixed; the temporal procedure's equivalence class is preserved because it depends only on the first coordinate) and one temporal edge (symmetrically)."

   Under the convention introduced earlier in the draft - $M_{\mathcal{T}}$ factors through projection to $\mathcal{T}$, and (by the natural ordering of introduction) $\sim_1 = \sim_{M_{\mathcal{T}}}$, $\sim_2 = \sim_{M_{\mathcal{C}}}$ - the first edge $(t_1, c_1) \to (t_1, c_2)$ has first coordinates equal and second coordinates differing, so the procedure that fails to distinguish the endpoints is the *temporal* one ($\sim_{M_{\mathcal{T}}}$, since both points project to $t_1$). That makes the edge a $\sim_1$-edge, not a $\sim_2$-edge. The path should read
   $$(t_1, c_1) \;\sim_1\; (t_1, c_2) \;\sim_2\; (t_2, c_2)$$
   and the parenthetical "categorical edge" should be "temporal edge" (since the edge is named by which procedure's equivalence class contains both endpoints, not by which axis the motion traverses).

   The diameter-2 fact, and the reflexivity argument that backs it, are correct. But the formal exposition has the labels reversed, and a reader who tries to verify the algebra will hit the inconsistency. This was the concern in round 1 that asked for the path to be written out; the path is now written out, but with the labels scrambled.

2. **Stray notation in the dual section's setup, line 106.** The phrase "for any $(t_1, c_1)$ and $(t_2, c_2)$ in $T_0 \cup_{c} \mathcal{T} \times C_0 \cup_{t} \cdots$ - more precisely, for any $(t_1, c_1), (t_2, c_2) \in \mathcal{A} = \mathcal{T} \times \mathcal{C}$" looks like a half-edited notation that the author replaced with a clean reformulation but did not delete. The "more precisely" clause is correct; the first attempt advertises a typo and should be removed.

3. **The Galois-isomorphism sentence in Section 8 reads as though the isomorphism is rectangle-aware.** Line 114: "The question reading (c) sharpens - *which subsets of $\mathcal{A}$ are rectangles in a product?* - is exactly the structure this isomorphism preserves." The isomorphism (between the lattice of subsets of $\mathcal{A} \setminus \{\theta_0\}$ and the poset of equivalence-class-at-$\theta_0$ choices) preserves set-theoretic structure on subsets; "which subsets are rectangles in a product" is a derived condition on those subsets, not structure the isomorphism itself sees. The current wording overclaims slightly. A one-clause clarification - e.g., "whether a given subset is a rectangle in a product is a property defined on the subset side of this isomorphism" - would close the gap.

4. **Optional: the projection-factoring condition for Eratosthenes is asserted but not unpacked.** The piece says the three Eratosthenes subprocedures "each factor through their respective projection: the shadow-angle procedure says nothing about road distance or stadion length, and analogously for the other two." This is right in spirit, but the case for it is brief, and the empirical content is left implicit. The Nightingale unpacking (total-death-regime-invariance, with a named margin where it could fail) is the model; doing the symmetric work for Eratosthenes - e.g., naming a way the shadow-angle procedure could in principle smuggle in an assumption about the stadion (a particular geodetic model, say) and arguing that in fact it does not - would give the Eratosthenes case the same diagnostic teeth the Nightingale case has. Not blocking; the section earns its place as written. But it would make the "in any concrete case" claim of the closing more fully delivered if both worked examples did the same work.

5. **No process-leakage. Charter-prohibition check: clean.** I list this here for the record. The earlier "proposal" / "I had expected" / "Galois-connection question" phrases are all gone. I checked the new sections (Eratosthenes, Wassermann contrast, Move 1 / Move 2 obstruction, Section 8 reframing) and saw no process narration, no reference to round 1, the panel, advisors, or the response document. The single phrase "is offered as a contrast" on line 86 is borderline meta but reads as ordinary expository hedging rather than process leakage; I would leave it.
