"""One-time migration: bootstrap the College's department structure.

The qualifying-panel workflow's same-department vs outside-the-discipline
distinction was falling back to a brittle specialization-string heuristic
because no departments were ever initialized. This migration creates the
initial five departments, assigns the current cohort across them (with
cross-listings where the work genuinely bridges), and records the
institutional decision.

The five departments are designed to be forward-looking, not just a fit
for the current cohort:

  1. Mathematical Sciences — formal methods, computation, dynamical
     systems, the mathematics of natural form.
  2. Empirical Inquiry & Measurement — experimental design, instrument
     analysis, observational error, replication.
  3. History, Philosophy & Critical Method — historical reading,
     methodological critique, logic of inquiry, the institutional
     record of how knowledge is produced.
  4. Political Economy & Institutional Inquiry — institutions,
     markets, social mechanisms, organizations.
  5. Letters & Interpretive Studies — hermeneutics, literary analysis,
     narrative, careful reading of texts.

Departments 4 and 5 are intentionally sparse or empty now; they
anchor where future admissions will land as the cohort grows. Cross-
listings handle Fellows whose work genuinely spans territories.

Run once:
    uv run python scripts/migrations/2026-05-20-bootstrap-departments.py
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from institute import db, decisions, departments  # noqa: E402


def main() -> int:
    with db.connection() as conn:
        if departments.is_initialized(conn):
            existing = departments.list_all(conn)
            print(f"Departments already initialized ({len(existing)}):")
            for d in existing:
                print(f"  - {d.name} ({d.id})")
            print("\nThis migration is idempotent; re-running won't duplicate.")

    plan: list[tuple[str, str, str | None, list[str]]] = [
        (
            "Mathematical Sciences",
            (
                "Formal methods, computation, dynamical systems, and the "
                "mathematics of natural form. The work of this department "
                "includes proof, algorithm, model, simulation, and the "
                "rigorous transposition between formal structures and "
                "phenomena. Connects to the Research Agenda's questions "
                "about the geometry of measurement instability and the "
                "grammar of analogy."
            ),
            "henri-poincare",
            ["henri-poincare", "ada-lovelace", "darcy-thompson", "grace-hopper"],
        ),
        (
            "Empirical Inquiry & Measurement",
            (
                "Experimental design, instrument-making, replication, and "
                "the disciplined analysis of observational error. The "
                "department's bar is reproducible procedure under stated "
                "conditions. Connects to the Research Agenda's questions "
                "about inherited bias in instruments and the geometry of "
                "measurement instability."
            ),
            "ibn-al-haytham",
            ["ibn-al-haytham", "darcy-thompson"],
        ),
        (
            "History, Philosophy & Critical Method",
            (
                "Historical reading, methodological critique, logic of "
                "inquiry, and the institutional record of how knowledge is "
                "produced. Where the College examines its own conditions "
                "of possibility. Connects to the Research Agenda's "
                "questions about disagreement-preserving knowledge, "
                "premonitory science, and institutions as epistemic "
                "substrates."
            ),
            "pierre-bayle",
            ["pierre-bayle", "michel-de-montaigne", "charles-sanders-peirce"],
        ),
        (
            "Political Economy & Institutional Inquiry",
            (
                "Institutions, markets, social mechanisms, organizations, "
                "and the structures within which knowledge production "
                "happens. The department reads the College itself as one "
                "such structure. Connects to the Research Agenda's "
                "questions about institutions as epistemic substrates, "
                "the arithmetic of attention, and the economics of slow "
                "thinking."
            ),
            None,  # no Senior Fellow yet; admissions gap
            ["adam-smith"],
        ),
        (
            "Letters & Interpretive Studies",
            (
                "Hermeneutics, literary analysis, narrative, and the long "
                "traditions of careful reading. The department reads "
                "texts the way the empirical departments read instruments: "
                "as objects with provenance, internal structure, and "
                "constraints. Currently sparsely staffed; the department "
                "anchors where future humanistic admissions will land."
            ),
            None,
            ["michel-de-montaigne"],  # cross-listed; primary home is HPC
        ),
    ]

    # Verify every member id corresponds to an active Fellow before we
    # write anything. The membership table FKs to fellows(id); a typo
    # here would otherwise abort the transaction halfway.
    with db.connection() as conn:
        active_ids = {
            r["id"]
            for r in conn.execute("SELECT id FROM fellows WHERE retired_at IS NULL")
        }
    bad: list[str] = []
    for _, _, chair, members in plan:
        if chair is not None and chair not in active_ids:
            bad.append(f"chair {chair}")
        for m in members:
            if m not in active_ids:
                bad.append(f"member {m}")
    if bad:
        print(
            f"Refusing to migrate: unknown Fellow ids referenced: {sorted(set(bad))}",
            file=sys.stderr,
        )
        return 1

    summary_lines: list[str] = []
    with db.connection() as conn, db.transaction(conn):
        for name, description, chair, members in plan:
            dept = departments.create(
                conn,
                name=name,
                description=description,
                chair_fellow_id=chair,
            )
            for fellow_id in members:
                departments.add_member(
                    conn, department_id=dept.id, fellow_id=fellow_id
                )
            chair_label = f" (chair: `{chair}`)" if chair else " (no chair)"
            summary_lines.append(f"- **{name}**{chair_label}")
            for fellow_id in members:
                cross = (
                    " *(cross-listed)*"
                    if fellow_id == "michel-de-montaigne"
                    and dept.id == "letters-and-interpretive-studies"
                    else ""
                )
                summary_lines.append(f"  - `{fellow_id}`{cross}")
            if not members:
                summary_lines.append("  - *(no members yet)*")

        now = datetime.now(UTC).isoformat(timespec="seconds")
        body_lines = [
            "**Effective:** immediately.",
            "",
            "**Scope:** five departments are established with the current "
            "cohort assigned across them.",
            "",
            "## Departments",
            "",
            *summary_lines,
            "",
            "## Why now",
            "",
            (
                "The qualifying-panel workflow distinguishes between a "
                "same-department vote (peer perspective inside the "
                "discipline) and an outside-the-discipline vote "
                "(intelligibility to a reader without the specialist's "
                "training). Without an initialized department structure, "
                "the workflow fell back to a string-equality heuristic on "
                "the `specialization` field; every Fellow has a distinct "
                "specialization string, so the same-department slot "
                "always came up empty and the panel proceeded as a "
                "degenerate two-vote (advisor + outside) panel. "
                "Initializing real departments gives the panel the "
                "two-perspective structure the Chapter 5 design intended."
            ),
            "",
            "## Why this partition",
            "",
            (
                "The department names are chosen to be forward-looking: "
                "they anchor where future admissions can land as the "
                "cohort grows, not just where current Fellows happen to "
                "sit. Political Economy & Institutional Inquiry is "
                "sparsely staffed (Adam Smith only) and Letters & "
                "Interpretive Studies has no primary members yet; both "
                "remain on the books so the admissions committee has "
                "explicit slots to fill rather than discovering the gap "
                "after the fact. The Research Agenda's questions about "
                "institutions as epistemic substrates and the arithmetic "
                "of attention live in those departments by design."
            ),
            "",
            (
                "Cross-listings (D'Arcy Thompson in both Mathematical "
                "Sciences and Empirical Inquiry; Michel de Montaigne in "
                "both History/Philosophy and Letters) reflect work that "
                "genuinely bridges. The panel-selection logic treats "
                "shared membership in any department as 'same-department.'"
            ),
            "",
            f"**Recorded:** {now}",
        ]
        decision = decisions.Decision(
            kind="policy_change",
            title="Departments established: initial five-department structure",
            body="\n".join(body_lines),
            actors=["founder"],
        )
        decisions.record(conn, decision)

    print("Departments created. Final layout:")
    with db.connection() as conn:
        for d in departments.list_all(conn):
            members = departments.member_ids(conn, d.id)
            print(f"  - {d.name} ({d.id})")
            for m in members:
                print(f"      {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
