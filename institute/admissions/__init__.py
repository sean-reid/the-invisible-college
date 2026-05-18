"""Admissions: how new Fellows are vetted and admitted to the College.

Chapter 4 of the design covers this in depth. The implementation here is
a v1 carve-out: single-candidate admissions (not cohort), the Founder
serves as committee (since there are no Senior Fellows yet), no mentor
matching. Once the institution has Senior Fellows, the committee
structure can rotate and the workflow can scale to cohort intake.

The flow:

  1. The orchestrator proposes a candidate genome, informed by the
     current cohort's specializations and model backends (to seek
     complementary diversity).
  2. The Founder reviews the proposed genome and approves, edits, or
     rejects it.
  3. The candidate is invoked as a Fellow and writes responses to a
     fixed set of qualifying problems.
  4. The orchestrator evaluates the responses against the criteria in
     Chapter 4: substance, honesty, originality, clarity, fit.
  5. The Founder reviews the responses and the evaluation, and makes
     the final admission decision.
  6. If admitted, the candidate's genome is written to genomes/ and
     registered in the DB; the full candidate package (genome,
     responses, evaluation, decision) is preserved in
     archive/admissions/<candidate-id>/ for the institutional record.

This module is small. The qualifying-problem set is a directory of
markdown files; the workflow lives in institute/workflows/admit.py;
the CLI surface is `institute admit`.
"""
