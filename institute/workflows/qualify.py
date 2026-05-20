"""Qualifying project: a Postulant's first piece of work under advisor sponsorship.

Per Chapter 5: the central event of the Postulant period is the
qualifying project. It is a real piece of research, narrower in scope
than a typical College publication, completed under advisor
supervision. A successful qualifying project advances the Postulant to
Novice rank.

This workflow creates the project. The Postulant drafts a proposal
under their advisor's guidance, the project enters state PROPOSED with
`kind='qualifying'`, and the normal research pipeline takes over with
three differences applied by other workflows:

  - The Postulant is the lead author (overriding the "no postulants as
    leads" gate in `propose._pick_lead`, which is only consulted for
    ad-hoc proposals anyway).
  - When a draft is ready, the project routes through
    AWAITING_ADVISOR_REVIEW before peer review (see `advisor_review.py`).
  - Peer review fixes the advisor as primary reviewer (see
    `peer_review._pick_review_slots`).
  - On publication, the Postulant is auto-promoted to Novice (see
    `publish.py`).
"""

from __future__ import annotations

import re
import secrets
from datetime import UTC, date, datetime

from rich.console import Console

from institute import (
    archive_index,
    claude_runner,
    curriculum,
    db,
    decisions,
    episodic,
    paths,
    workspaces,
)
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


PROPOSE_BRIEF = """\
You are a Postulant at the Invisible College, drafting your
**qualifying project** proposal. Per Chapter 5, this is the central
piece of work of your Postulant period: a real research project,
narrower than a typical College publication, completed under your
advisor's supervision. A successful qualifying project advances you to
Novice.

# Inputs in your workspace

- `advisor.md`       your advisor's identity and specialization. They
                     will read your drafts, give substantive feedback,
                     and serve as the primary peer reviewer.
- `curriculum.md`    the reading curriculum you have been working
                     through. Your qualifying project should build on
                     what you have engaged with, not orbit elsewhere.
- `archive-index.md` every piece the College has published. The bar
                     to clear; do not duplicate prior work.
- `memory.md`        if present, your own past writings on the
                     curriculum and other artifacts. The qualifying
                     project should grow out of what you have already
                     thought through, not start over.

Read all of them with the Read tool. Also read `docs/05-curriculum.md`
for the qualifying-project criteria.

# What you must produce

Use the Write tool to create `proposal.md` in your workspace. The
proposal must contain, in order:

1. `# <Title>` on the first line (a level-1 heading).
2. `## Question` — the question you propose to investigate.
3. `## Background` — what is already known, with citations. Reference
   the relevant items from your curriculum.
4. `## Approach` — concrete methods you will use. Bounded enough to
   complete in 2 to 4 weeks of intermittent work.
5. `## Expected output` — what form the result will take.
6. `## Resource estimate` — rough estimate of compute and time.
7. `## Anticipated failure modes` — how this could go wrong and what
   an honest negative result would look like. An honest failed
   qualifying project is preferable to a forced success.
8. `## Collaborators needed` — usually just your advisor; OK if none
   beyond them.

# Constraints

- Length: 500 to 1200 words total.
- Substantial but completable. A grand project that cannot be
  finished in the qualifying period is failing the exercise.
- Connected to your declared specialization.
- The question should be one you genuinely do not know the answer to.

# Final reply

When `proposal.md` exists and is complete, reply with the single word
`Done.` Nothing else.
"""


_TITLE_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def run(postulant_id: str) -> None:
    """Start a qualifying project for the given Postulant."""
    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, name, rank, advisor_id, retired_at FROM fellows WHERE id = ?",
            (postulant_id,),
        ).fetchone()
    if row is None:
        raise SystemExit(f"No such Fellow: {postulant_id}")
    if row["retired_at"]:
        raise SystemExit(f"{postulant_id} is retired.")
    if row["rank"] != "postulant":
        raise SystemExit(
            f"{postulant_id} is rank `{row['rank']}`. Qualifying projects are for postulants."
        )
    if not row["advisor_id"]:
        raise SystemExit(
            f"{postulant_id} has no advisor. Assign one before starting a qualifying project."
        )

    # Refuse if a qualifying project is already in flight (or completed).
    with db.connection() as conn:
        existing = conn.execute(
            "SELECT id, state FROM projects WHERE lead_fellow_id = ? AND kind = 'qualifying'",
            (postulant_id,),
        ).fetchone()
    if existing is not None:
        raise SystemExit(
            f"{postulant_id} already has a qualifying project ({existing['id']}, "
            f"state={existing['state']}). One per Postulant."
        )

    postulant = Genome.from_file(fellow_mod.genome_path(postulant_id))
    with db.connection() as conn:
        advisor_row = conn.execute(
            "SELECT id, name, specialization FROM fellows WHERE id = ?",
            (row["advisor_id"],),
        ).fetchone()
    if advisor_row is None:
        raise SystemExit(f"Advisor {row['advisor_id']} not found.")

    workspace = workspaces.workspace_for(postulant_id, "qualifying-proposal")
    workspaces.stage_input(
        workspace, "advisor.md", _render_advisor(advisor_row["name"], advisor_row["specialization"])
    )
    items = curriculum.load_items(postulant_id)
    workspaces.stage_input(
        workspace,
        "curriculum.md",
        curriculum.render_markdown(items) if items else "# Reading curriculum\n\n(None staged.)\n",
    )
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())
    stale = workspace / "proposal.md"
    if stale.exists():
        stale.unlink()

    console.print(
        f"[dim]Asking {postulant.name} ({postulant_id}) to draft their qualifying "
        "project proposal. This will take a few minutes...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=postulant,
            project_id=f"qualifying:{postulant_id}",
            step="qualifying-propose",
            brief=PROPOSE_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    proposal_md = workspaces.require_output(workspace, "proposal.md", min_chars=400).strip()
    title_match = _TITLE_H1.search(proposal_md)
    if not title_match:
        raise RuntimeError(
            f"Qualifying proposal has no `# Title` heading. "
            f"Draft preserved at {workspace / 'proposal.md'}."
        )
    title = title_match.group(1).strip()
    project_id = _project_id(title)
    proposal_path = paths.PROPOSALS / project_id / "proposal.md"

    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision = decisions.Decision(
        kind="qualifying_proposal",
        title=f"Qualifying proposal: {title}",
        body=(
            f"**Postulant:** {postulant.name} (`{postulant_id}`)\n\n"
            f"**Advisor:** {advisor_row['name']} (`{advisor_row['id']}`)\n\n"
            f"**Title:** {title}\n\n"
            f"**Proposal:** [{proposal_path.relative_to(paths.ROOT)}]"
            f"({proposal_path.relative_to(paths.ROOT)})\n\n"
            "This project enters the normal pipeline with three deviations: the "
            "Postulant is the lead author, the advisor is the primary peer "
            "reviewer, and the draft routes through an advisor-review step "
            "before peer review. On publication, the Postulant advances to "
            "Novice automatically."
        ),
        actors=["orchestrator", postulant_id, advisor_row["id"]],
        related_project=project_id,
    )

    # Insert the project row first, then write the proposal to the
    # archive. A crash between Claude returning and this transaction
    # leaves the workspace proposal.md but no archive file and no row;
    # re-running the workflow finds the workspace draft and reuses it
    # via require_output. A crash between INSERT and the file write
    # leaves a row pointing at a missing file, which the next
    # review_proposal dispatch raises on, surfacing the corruption
    # rather than silently re-spending budget.
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, proposal_path, kind, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, 'qualifying', ?, ?)",
            (
                project_id,
                title,
                State.PROPOSED.value,
                postulant_id,
                str(proposal_path.relative_to(paths.ROOT)),
                now,
                now,
            ),
        )
        decisions.record(conn, decision)
    _write_atomically(proposal_path, proposal_md.rstrip() + "\n")

    episodic.safe_ingest(
        fellow_id=postulant_id,
        kind="proposal",
        title=f"Qualifying proposal: {title}",
        content=proposal_md,
        source_path=str(proposal_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"kind": "qualifying", "advisor": advisor_row["id"]},
    )

    console.print()
    console.print(f"[bold green]Qualifying project created:[/bold green] `{project_id}`")
    console.print(f"  Title:    {title}")
    console.print(f"  Lead:     {postulant.name} (Postulant)")
    console.print(f"  Advisor:  {advisor_row['name']} (primary reviewer)")
    console.print(f"  Proposal: {proposal_path.relative_to(paths.ROOT)}")
    console.print(
        "[dim]Run `institute next` to advance: proposal review → research → "
        "advisor review → peer review → editorial → publish. On publish, the "
        "Postulant is auto-promoted to Novice.[/dim]"
    )


def _render_advisor(name: str, specialization: str) -> str:
    return (
        f"# Your advisor: {name}\n\n"
        f"- **specialization:** {specialization}\n\n"
        "Your advisor will read your drafts, give substantive feedback, and "
        "serve as the primary reviewer when peer review begins. Engage them "
        "honestly. A Postulant who simply implements whatever the advisor "
        "says is failing the curriculum."
    )


def _project_id(title: str) -> str:
    today = date.today().isoformat()
    return f"{today}-qual-{_slugify(title)[:40]}-{secrets.token_hex(2)}"


def _slugify(text: str) -> str:
    out = []
    last_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    s = "".join(out).strip("-")
    return s or "untitled"


def _write_atomically(path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)
