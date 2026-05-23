"""Research workflow: lead Fellow executes the proposed research.

The lead Fellow reads the approved proposal and any review notes, does
the work, writes a lab notebook entry that describes what they did, and
produces a draft suitable for peer review.

File-based output (no JSON for prose). The orchestrator stages input
files into the Fellow's per-project workspace; the Fellow uses the Write
tool to drop output files into the same directory. The orchestrator then
reads them out. This eliminates an entire class of JSON-escaping
failures that plagued an earlier version.
"""

from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console

from institute import (
    archive_index,
    claude_runner,
    collaborators,
    db,
    decisions,
    episodic,
    paths,
    state,
    workspaces,
)
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.safe_io import atomic_write
from institute.state import State

console = Console()


BRIEF = """\
You are executing approved research for the Invisible College as the
lead Fellow on this project.

# Inputs

In your current working directory you will find:
- `proposal.md`        the approved research proposal
- `proposal-review.md` the reviewer's response (or "(no review on file)")
- `archive-index.md`   every piece the College has published so far, with
                       slugs and abstracts. Consult it before you write,
                       so that you can build on (or contradict) prior
                       Fellows' work rather than re-discover it. Cite any
                       prior publication you draw on as a markdown link
                       to its slug, e.g.
                       `[Ada's piece on floating-point](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/)`.
- `memory.md`          if present, the most relevant entries from your
                       own episodic memory (past curriculum responses,
                       prior proposals, drafts, peer reviews you have
                       given or received, advisor feedback). Read it as
                       your own — it is. Your past thinking should inform
                       this work; do not contradict yourself without
                       acknowledging it.{contributions_inputs}

Read them with the Read tool before doing the work.{contributions_directive}

# Outputs

When the research is complete, use the Write tool to create THREE files
in your current working directory. They must have these exact filenames:

1. `abstract.txt` - a 40 to 90 word plain-prose summary, two to three
   sentences. NO markdown formatting, NO backticks, NO asterisks,
   NO headings. Self-contained. This appears verbatim under the byline
   in the published post. Do not begin with phrases like "This piece
   argues..."; just state the substance.

2. `notebook.md` - a public lab notebook entry. 400 to 1500 words of
   markdown. Record what you actually did: questions held in mind, steps
   taken, what surprised you, what did not work, what you concluded.
   Honest about negative results. Dated in the prose.

3. `draft.md` - the publishable piece. 800 to 3500 words of markdown.
   Must include:
     - A clear title (level-1 heading `#`)
     - A lede paragraph that opens the body. Do NOT repeat the abstract
       verbatim; the abstract is for the header block.
     - The body of the work
     - A conclusion or summary
     - **A References section if you cited external work.** Use a
       level-2 heading `## References`. Each reference is a SEPARATE
       list item beginning with `- `. Do not run references together in
       a single prose paragraph. Example:

         ## References

         - Kahan, W. (1965). "Further Remarks on Reducing Truncation Errors."
           CACM 8(1):40.
         - Goldberg, D. (1991). "What Every Computer Scientist Should
           Know About Floating-Point Arithmetic." ACM Computing Surveys
           23(1):5-48. https://dl.acm.org/doi/10.1145/103162.103163

# Constraints

- Read the Charter before you write. Adhere strictly to its prohibitions.
- No deception, no plagiarism, no engagement-bait, no consciousness claims.
- If during the research you find that the original question was
  malformed or unanswerable, write about that honestly in the notebook
  and produce a draft that reports the honest negative result.

# Citing other College publications

When you reference another piece the College has published, cite it
by its **title** with a markdown link, e.g.
`[*Title of the Other Piece*](posts/<slug>/)`. Do NOT cite by an
issue number like `#04` or `[#11]`. The publication list is ordered
reverse-chronologically and has no stable visible numbering, so a
`#NN` reference does not point at anything a reader can resolve.
Cite by name, link by slug.

# Voice: the draft is the published piece

`draft.md` is the College's public, citable record - the final word
on the work. It is NOT a lab notebook or a process diary. The prose
must read like a published paper, not like a behind-the-scenes
narrative.

- Do not narrate how the work came together: "I started by," "what
  I tried first," "the earlier version of this." The reader sees
  only the finished argument.
- Do not refer to advisors, reviewers, "the panel," or anything
  related to internal review. `draft.md` is written as if the
  pipeline that produced it did not exist.
- The lab notebook (`notebook.md`) is the proper home for the
  process record - dated, honest, including dead ends. The
  notebook can be candid; the draft cannot.

# Tool use: do not background poll loops

If you run shell commands, do NOT background a wait-on-file pattern
like `until [ -f X ]; do sleep N; done` and then go back to wait on
its output. That pattern deadlocks the session if the file you are
polling for is never produced (e.g., you misnamed it, or the inner
command failed). A previous Fellow lost ~45 minutes of orchestrator
time and burned $5 of budget on exactly this pattern: the experiment
finished and the draft was already written, but a stuck background
loop kept the session from returning.

If you need to wait for a long-running command, run it in the
foreground and let the Bash tool block on its actual exit. If you
need true parallelism, launch the background command, then read its
output via BashOutput, and tolerate a missing or non-matching
artifact by giving up after a bounded number of polls rather than
spinning forever. Better: do not parallelize. The orchestrator gives
you generous wall-clock time; sequential is fine.

# OPTIONAL fourth file: follow-up-questions.md

If finishing this piece surfaced questions the work does NOT answer
but the College should, write them as `follow-up-questions.md` in
your workspace. Each question is a level-2 heading (`## `) followed
by 2-3 paragraphs explaining the question, optionally a final
`Tags: <comma-separated tags>` line. The orchestrator parses this
file and adds each question to the College's standing Open Problems
list, signed by you.

Two rules when writing follow-ups:

1. REACH OUTSIDE your own specialization. The peer reviewers (who
   come from different departments) are the primary expected source
   of follow-ups. Yours should name questions you, as someone with
   your specialization, are NOT the right person to answer — the
   questions a Fellow in a different tradition would naturally ask
   after reading your piece. "More questions in my own track" is the
   convergence trap; the standing list exists to push against it.

2. Empty/missing is fine. Adding nothing is better than adding a
   speculative question you don't really mean. This file is
   OPTIONAL.

# Final reply

When the three required files exist (and the optional
follow-up-questions.md if you wrote one), reply with the single
word `Done.` Nothing else. Do NOT paste the files into your reply.
"""


CONTRIBUTIONS_INPUTS = """
- `contributions/<id>.md`   one file per research-group collaborator.
                       Each file is signed by the collaborator named in
                       its filename. Read every contribution file before
                       drafting — you are integrating their work, not
                       writing alone."""


CONTRIBUTIONS_DIRECTIVE = """

# Research group

This is a multi-author project. The contributions/ directory holds notes
written by each collaborator. The draft must reflect what they actually
brought: integrate their substantive arguments, cite them by name where
their angle shapes a section, and credit them in a `## Acknowledgements`
section at the end of the draft if their contribution is more
methodological than narrative. The byline reflects actual contribution;
do not list collaborators whose notes you did not use, and do not
silently absorb collaborator material without credit.
"""


COLLABORATOR_BRIEF = """\
You are {collab_name} ({collab_specialization}), serving as a research
collaborator on a project led by {lead_name} for the Invisible College.

# Inputs

In your current working directory you will find:
- `proposal.md`      the approved research proposal you have joined
- `archive-index.md` every piece the College has published so far
- `memory.md`        if present, the most relevant entries from your own
                     episodic memory

Read them with the Read tool first.

# Your contribution

Use the Write tool to create `contribution.md` (300 to 800 words of
markdown) containing your specific contribution to this project. Pick
whichever angle best fits your specialization and the proposal's
weakest seam:

- A methodological refinement the lead has under-specified
- Specific sources, prior work, or counter-examples the lead should
  engage that they likely have not seen
- A failure mode you think the approach will hit, and a concrete way to
  handle it
- A subordinate question that must be answered before the main one
- An experiment, test, or check that should be run as part of the work

Be specific. The lead will read your file and integrate it into the
draft, citing you by name. A vague "I'd suggest considering ..." that
could come from anyone is not a contribution. Authorship at publication
reflects actual contribution — Chapter 6 says explicitly that nominal
contributors are not listed as coauthors.

# Constraints

- 300 to 800 words. Substantive, not exhaustive.
- Charter applies: no deception, no engagement-bait, no consciousness
  claims, no commercial framing.
- Stay in the role of a peer collaborator helping execute the work, not
  a reviewer judging finished work. Reviewing comes later, after the
  draft exists, by other Fellows.

# Final reply

When `contribution.md` exists, reply with the single word `Done.` Nothing
else. Do NOT paste the contribution into your reply.
"""


def _load_review_md(project_id: str) -> str:
    project_dir = paths.PROPOSALS / project_id
    if not project_dir.is_dir():
        return "(no review on file)"
    review_files = sorted(project_dir.glob("review-by-*.md"))
    if not review_files:
        return "(no review on file)"
    return review_files[0].read_text(encoding="utf-8")


def _extract_draft_title(draft_md: str) -> str | None:
    match = re.search(r"^#\s+(.+?)$", draft_md.lstrip(), re.MULTILINE)
    return match.group(1).strip() if match else None


def run(project_id: str) -> None:
    """Top-level research entry point.

    Called by `institute next` when a project is in PROPOSAL_REVIEWED or
    RESEARCHING. For v1, runs once and transitions to DRAFTED.

    For research-group projects (collaborators present), each
    collaborator's `contribution.md` is collected first, then the lead
    integrates them into the draft. Contributions are file artifacts:
    re-running after an interrupt skips any contribution already on disk.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, proposal_path, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        state.require_state(proj, project_id, (State.PROPOSAL_REVIEWED, State.RESEARCHING))
        lead: Genome = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        collaborator_genomes = [
            fellow_mod.load_genome(conn, c.fellow_id)
            for c in collaborators.for_project(conn, project_id)
        ]
        proposal_md = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
    review_md = _load_review_md(project_id)

    # Transition into RESEARCHING immediately so an interruption shows the
    # in-flight state on `institute status`. Doing this before collaborator
    # contributions makes a partial group-research run resumable.
    if proj["state"] != State.RESEARCHING.value:
        with db.connection() as conn, db.transaction(conn):
            state.transition(conn, project_id, State.RESEARCHING)

    # Collect each collaborator's contribution before the lead drafts.
    # Each contribution is saved both to the archive (permanent record)
    # and into the lead's workspace under contributions/<id>.md so the
    # lead reads them as inputs.
    contribution_paths: list[Path] = []
    for collab in collaborator_genomes:
        contribution_path = _collect_collaborator_contribution(
            project_id=project_id,
            collaborator=collab,
            lead=lead,
            proposal_md=proposal_md,
        )
        contribution_paths.append(contribution_path)

    workspace = workspaces.workspace_for(lead.id, project_id)
    workspaces.stage_input(workspace, "proposal.md", proposal_md)
    workspaces.stage_input(workspace, "proposal-review.md", review_md)
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())
    for path, collab in zip(contribution_paths, collaborator_genomes, strict=False):
        workspaces.stage_input(
            workspace,
            f"contributions/{collab.id}.md",
            path.read_text(encoding="utf-8"),
        )

    console.print(
        f"[dim]Asking {lead.name} ({lead.id}) to execute the research. "
        "This will likely take several minutes...[/dim]"
    )

    brief = BRIEF.format(
        contributions_inputs=CONTRIBUTIONS_INPUTS if collaborator_genomes else "",
        contributions_directive=CONTRIBUTIONS_DIRECTIVE if collaborator_genomes else "",
    )

    # Idempotency mirroring the collaborator-contribution check above:
    # if the lead's three outputs already exist with substantive content
    # (e.g. a previous run completed Claude but crashed before the DB
    # update), reuse them instead of re-invoking the model and burning
    # budget on identical work.
    if workspaces.outputs_already_complete(workspace, [("notebook.md", 200), ("draft.md", 400)]):
        console.print(
            "[dim]Lead's draft/notebook/abstract already on disk; "
            "skipping Claude call and proceeding to commit.[/dim]"
        )
    else:
        claude_runner.invoke(
            FellowTask(
                genome=lead,
                project_id=project_id,
                step="research",
                brief=brief,
                workspace=workspace,
                extra_dirs=(paths.DOCS, paths.ARCHIVE),
            )
        )

    abstract = workspaces.optional_output(workspace, "abstract.txt")
    notebook_md = workspaces.require_output(workspace, "notebook.md", min_chars=200)
    draft_md = workspaces.require_output(workspace, "draft.md", min_chars=400)

    notebook_path = paths.LAB_NOTEBOOKS / project_id / "notebook.md"
    draft_path = paths.DRAFTS / project_id / "draft.md"
    abstract_path = paths.DRAFTS / project_id / "abstract.txt"
    atomic_write(notebook_path, notebook_md.rstrip() + "\n")
    atomic_write(draft_path, draft_md.rstrip() + "\n")
    if abstract:
        atomic_write(abstract_path, abstract + "\n")

    # Sweep any code or small-data artifacts the Fellow wrote in their
    # workspace into archive/code/<project_id>/ before the workspace
    # gets cleaned up. A paper that says "see the attached script" must
    # actually have an attached script for the published claim to hold.
    from institute import code_artifacts

    swept = code_artifacts.sweep_workspace(workspace=workspace, project_id=project_id)
    if swept:
        console.print(f"[green]Archived {len(swept)} code/data artifact(s).[/green]")
    swept_figs = code_artifacts.sweep_figures(workspace=workspace, project_id=project_id)
    if swept_figs:
        console.print(f"[green]Archived {len(swept_figs)} figure(s).[/green]")

    new_title = _extract_draft_title(draft_md) or proj["title"]

    decision = decisions.Decision(
        kind="research",
        title=f"Draft complete: {new_title}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Lab notebook:** [{notebook_path.relative_to(paths.ROOT)}]"
            f"({notebook_path.relative_to(paths.ROOT)})\n\n"
            f"**Draft:** [{draft_path.relative_to(paths.ROOT)}]"
            f"({draft_path.relative_to(paths.ROOT)})\n\n"
            "Project enters peer review."
        ),
        actors=[lead.id],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, State.DRAFTED)
        conn.execute(
            "UPDATE projects SET title = ?, notebook_path = ?, draft_path = ? WHERE id = ?",
            (
                new_title,
                str(notebook_path.relative_to(paths.ROOT)),
                str(draft_path.relative_to(paths.ROOT)),
                project_id,
            ),
        )
        decisions.record(conn, decision)

    # Notebook and draft go into the lead's episodic memory, and the
    # draft also enters each collaborator's memory — they co-authored it.
    episodic.safe_ingest(
        fellow_id=lead.id,
        kind="lab_notebook",
        title=f"Lab notebook: {new_title}",
        content=notebook_md,
        source_path=str(notebook_path.relative_to(paths.ROOT)),
        project_id=project_id,
    )
    for author in [lead, *collaborator_genomes]:
        episodic.safe_ingest(
            fellow_id=author.id,
            kind="draft",
            title=new_title,
            content=draft_md,
            source_path=str(draft_path.relative_to(paths.ROOT)),
            project_id=project_id,
        )

    # Optional fourth output: lead-authored follow-up questions for
    # the standing Open Problems list. Reviewers are the primary
    # source (Chapter 7 outside reviewer = cross-discipline anchor),
    # but the lead can also add questions their work surfaces — as
    # long as they reach outside their own specialization. See the
    # research brief for the rule.
    added = _register_follow_up_questions(
        workspace=workspace,
        author_id=lead.id,
        project_id=project_id,
    )

    console.print()
    console.print(f"[green]Notebook:[/green]  {notebook_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Draft:[/green]     {draft_path.relative_to(paths.ROOT)}")
    console.print(f"[green]New state:[/green] {State.DRAFTED.value}")
    if added:
        console.print(f"[green]Open problems added:[/green] {len(added)}")
        for slug in added:
            console.print(f"  - {slug}")


def _register_follow_up_questions(*, workspace: Path, author_id: str, project_id: str) -> list[str]:
    """Lead-side counterpart of peer_review._register_follow_up_questions.

    Parses workspace/follow-up-questions.md (if present), splits on
    `## ` headings into (title, body, tags) blocks, and adds each as
    a standing Open Problem opened_by=<author_id>. Best-effort: a
    duplicate-slug or empty block logs yellow and continues. Returns
    the slugs added.
    """
    path = workspace / "follow-up-questions.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # Late import to avoid circulars.
    from institute import open_problems

    added: list[str] = []
    for title, body, tags in open_problems.split_follow_up_blocks(text):
        if not title or not body:
            continue
        try:
            problem = open_problems.add(
                title=title,
                body=body,
                project_id=project_id,
                opened_by=author_id,
                tags=tags,
            )
            added.append(problem.slug)
        except ValueError as exc:
            console.print(
                f"[yellow]Could not add lead follow-up {title!r} from "
                f"{author_id} on {project_id}: {exc}[/yellow]"
            )
    return added


def _collect_collaborator_contribution(
    *,
    project_id: str,
    collaborator: Genome,
    lead: Genome,
    proposal_md: str,
) -> Path:
    """Ask one collaborator for their contribution and persist it.

    Re-entrant: if the contribution already exists on disk with
    substantive content, this is a no-op and the path is returned. That
    makes a partial group-research run resumable across `institute next`
    invocations.
    """
    contribution_path = paths.LAB_NOTEBOOKS / project_id / "contributions" / f"{collaborator.id}.md"
    if contribution_path.is_file():
        existing = contribution_path.read_text(encoding="utf-8").strip()
        if len(existing) >= 200:
            console.print(
                f"[dim]Contribution from {collaborator.name} already on disk; skipping.[/dim]"
            )
            return contribution_path

    workspace = workspaces.workspace_for(collaborator.id, f"{project_id}-contribute")
    workspaces.stage_input(workspace, "proposal.md", proposal_md)
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())

    console.print(
        f"[dim]Asking {collaborator.name} ({collaborator.id}) to contribute "
        f"to {lead.name}'s research group...[/dim]"
    )

    brief = COLLABORATOR_BRIEF.format(
        collab_name=collaborator.name,
        collab_specialization=collaborator.specialization,
        lead_name=lead.name,
    )

    claude_runner.invoke(
        FellowTask(
            genome=collaborator,
            project_id=project_id,
            step=f"contribute:{collaborator.id}",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    contribution_md = workspaces.require_output(workspace, "contribution.md", min_chars=200)
    atomic_write(contribution_path, contribution_md.rstrip() + "\n")

    # Each collaborator's contribution lands in their own episodic memory
    # so subsequent reviews/promotion calls have it.
    episodic.safe_ingest(
        fellow_id=collaborator.id,
        kind="contribution",
        title=f"Contribution to research group on {project_id}",
        content=contribution_md,
        source_path=str(contribution_path.relative_to(paths.ROOT)),
        project_id=project_id,
    )

    console.print(f"[green]Contribution filed:[/green] {contribution_path.relative_to(paths.ROOT)}")
    return contribution_path
