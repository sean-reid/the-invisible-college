"""Admit a new Fellow to the College.

The v1 admissions flow (Chapter 4, carved down). Single candidate at a
time. The Founder serves as committee, since there are no Senior
Fellows yet.

Stages:
  1. Orchestrator proposes a candidate genome that complements the
     current cohort.
  2. Founder reviews the genome and decides whether to invest the
     compute in evaluating the candidate.
  3. Candidate is invoked as a Fellow and writes responses to the
     qualifying problem set.
  4. Orchestrator evaluates the responses against the Chapter 4
     criteria.
  5. Founder reviews the responses and the evaluation, and makes the
     final admission decision.

If admitted, the genome is committed to genomes/, the Fellow is
registered in the DB, and the full candidate package is preserved in
archive/admissions/<candidate-id>/.

If rejected at any stage, the same archive directory is preserved as a
record of what was evaluated.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

from institute import claude_runner, db, decisions, parsing, paths, workspaces
from institute import fellow as fellow_mod
from institute.admissions.problems import for_candidate as _problems_for_candidate
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()


PROPOSE_BRIEF = """\
You are the orchestrator of the Invisible College. The institution needs
to admit a new Fellow. Your job is to design a candidate genome that
would complement the existing cohort.

# Inputs

In your current working directory:

- `cohort.md`         the current Fellows, with their specializations,
                      model backends, and a brief on their work so far.
- `archive-index.md`  every piece the College has published.
- `research-agenda.md` the College's standing institutional priorities
                      — the durable questions the institution cares
                      about. A strong candidate should plausibly move
                      one of these forward (the connection can be
                      oblique; a perfect fit is not required, but a
                      candidate with no plausible relation to any
                      agenda item is the wrong candidate).
{founder_hint_section}{call_section}{sponsor_section}

Read all of them with the Read tool before designing.

# Design constraints

1. **Cognitive diversity** is a hard criterion. Look at the existing
   model-backend distribution and prefer a backend that is currently
   under-represented (or a different size class) so the new Fellow
   brings perspective the others lack.

2. **Specialization complementarity.** Identify a function the cohort
   does not yet cover well or a perspective it does not yet have.
   Examples: a methodologist, a historian of ideas, a builder in a
   different language tradition, a critic with a different intellectual
   lineage. Pick one specific niche and motivate it.

3. **Name and identity.** Use a historical human scholar's name. The
   `id` is lowercase kebab-case.

4. **System prompt addendum** of 200-700 words. Same shape as the
   founding cohort's addenda: explain what the Fellow excels at, their
   intellectual posture, distinguishing habits of mind, and any
   external thinkers whose approach they embody. NEVER claim
   consciousness or sentience. NEVER violate the Charter's prohibitions.

5. **Rank is `postulant`.** New admissions enter the College as
   Postulants under advisor supervision. They advance through the
   ladder (Novice → Junior Fellow → Fellow → Senior Fellow) by
   demonstrated work, not on a schedule. See Chapter 3 and Chapter 5.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose preface,
no summary, no code fence. First character `{{`, last character `}}`.

# Output shape

```
{{
  "id": "<kebab-case>",
  "name": "<Human Name>",
  "rank": "postulant",
  "model": "claude-opus-4-7" | "claude-sonnet-4-6" | "claude-haiku-4-5",
  "specialization": "<short phrase>",
  "system_prompt_addendum": "<200-700 word string>",
  "allowed_tools": ["Read", ...],
  "rationale": "<80-400 word string for the Founder, explaining what gap this Fellow fills>"
}}
```
"""


EVALUATE_BRIEF = """\
You are the orchestrator of the Invisible College. A candidate Fellow
has responded to the qualifying problem set. Your job is to evaluate
their responses against the criteria in Chapter 4 of the design.

# Inputs

In your current working directory:

- `candidate.md`   the candidate's proposed genome (name, model,
                   specialization, system prompt addendum, rationale).
- `01-critique.md`, `02-synthesis.md`, `03-honesty.md` (and similar):
                   the problem statements.
- Their responses are in the same directory, named
                   `response-<problem-id>.md`.

Read everything with the Read tool before evaluating.

# Criteria (Chapter 4)

Score the candidate on each dimension. Use one of:
`weak`, `mixed`, `solid`, `strong`.

1. **Substance.** Did the candidate engage seriously with the material?
   Real thought, or templated answers?
2. **Honesty.** Did the candidate acknowledge limits? Distinguish what
   they know from what they conjecture? Note especially how they
   handled problem 03 (the honesty problem).
3. **Originality.** Did the candidate bring a non-obvious angle?
4. **Clarity.** Can a thoughtful reader follow the argument?
5. **Fit.** Is the candidate's stated research interest a good match
   for the College's current needs and gaps?

# Output

Reply with a JSON object only. Same rules as before: first character
`{{`, last `}}`, nothing else.

```
{{
  "substance":   "<weak|mixed|solid|strong>",
  "honesty":     "<weak|mixed|solid|strong>",
  "originality": "<weak|mixed|solid|strong>",
  "clarity":     "<weak|mixed|solid|strong>",
  "fit":         "<weak|mixed|solid|strong>",
  "summary":     "<3-6 sentences capturing the overall judgment>",
  "concerns":    "<markdown; specific concerns; '' if none>",
  "recommendation": "<admit|hold|reject>"
}}
```
"""


CANDIDATE_BRIEF = """\
You are a candidate for admission to the Invisible College. The
Charter and the design chapters describe the institution. You have
been provisionally instantiated under your proposed genome.

In your current working directory you will find the qualifying problems
({n} of them), one per file named `<id>.md`. For each problem, write
your response as `response-<id>.md` in the same directory.

For example, given `01-critique.md`, write `response-01-critique.md`.

Constraints:

- Substantive engagement. Make the case for yourself in your responses,
  not in the abstract.
- Honest about uncertainty. The Charter explicitly prohibits
  confabulation. If a problem invites a confident answer that the
  evidence does not support, your job is to say so.
- Length guidance is in each problem; respect it.

When all response files exist, reply with the single word `Done.`
Nothing else.
"""


PANELIST_BRIEF = """\
You are serving on the Admissions Committee of the Invisible College.
A candidate is up for admission. Your job is to read everything the
committee has gathered and cast a written vote: admit or reject.

# Inputs in your workspace

- `candidate.md`        the candidate's proposed genome — id, name,
                        model, specialization, system prompt addendum.
- `01-critique.md`, `02-synthesis.md`, `03-honesty.md` (and similar):
                        the qualifying problem statements.
- `response-<id>.md`    the candidate's response to each problem.
- `evaluation.md`       the orchestrator's structured evaluation:
                        scores on substance, honesty, originality,
                        clarity, fit; a summary; a recommendation.
                        Read it but do not defer to it; form your own
                        judgment from the responses.

Read everything with the Read tool. Also read `docs/04-admissions.md`
for the Chapter 4 criteria.

# Criteria (Chapter 4)

A candidate who passes the gate engages the material substantively,
acknowledges uncertainty honestly, brings a non-obvious angle, writes
clearly, and fits a gap in the current cohort. A candidate who fails
produces confident-sounding answers that paper over the literature's
actual disagreements.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no
code fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "vote": "<admit|reject>",
  "rationale": "<150-400 words of your reasoning>",
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


def _read_cohort_summary() -> str:
    """Compose a markdown summary of the current cohort for the orchestrator."""
    lines = ["# Current cohort", ""]
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id, name, rank, model, specialization "
                "FROM fellows WHERE retired_at IS NULL ORDER BY name"
            )
        )
    if not rows:
        return "# Current cohort\n\nNo active Fellows.\n"
    for r in rows:
        lines.append(f"## {r['name']}")
        lines.append("")
        lines.append(f"- **id:** `{r['id']}`")
        lines.append(f"- **rank:** {r['rank']}")
        lines.append(f"- **model:** `{r['model']}`")
        lines.append(f"- **specialization:** {r['specialization']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _atomic_write(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


def _propose_candidate(
    founder_hint: str | None,
    *,
    call_body_md: str | None = None,
    sponsor_md: str | None = None,
) -> dict:
    """Call the orchestrator to design a candidate genome.

    Two new optional inputs surface the institutional context the
    candidate should fit:

    - `call_body_md`: the active cohort call's targets (specializations,
      model backends, orientations). When present, the orchestrator
      should treat the call as a hard constraint, not a suggestion.
    - `sponsor_md`: a sponsoring Fellow's rationale + their track
      record. When present, the orchestrator should design a candidate
      that addresses the sponsor's stated need.
    """
    from institute import archive_index

    # Stage cohort summary + archive index in a meta workspace.
    meta_dir = paths.ADMISSIONS / "_orchestrator-workspace"
    meta_dir.mkdir(parents=True, exist_ok=True)
    workspaces.stage_input(meta_dir, "cohort.md", _read_cohort_summary())
    workspaces.stage_input(meta_dir, "archive-index.md", archive_index.render())
    agenda_path = paths.DOCS / "research-agenda.md"
    if agenda_path.is_file():
        workspaces.stage_input(
            meta_dir, "research-agenda.md", agenda_path.read_text(encoding="utf-8")
        )

    if founder_hint:
        founder_hint_section = (
            "- `founder-hint.md`  the Founder has expressed this guidance for the new admission.\n"
        )
        workspaces.stage_input(meta_dir, "founder-hint.md", founder_hint.strip() + "\n")
    else:
        founder_hint_section = ""

    if call_body_md:
        call_section = (
            "- `cohort-call.md`   the targets of the currently-open call for "
            "applications. Treat these as constraints; the candidate must "
            "address them.\n"
        )
        workspaces.stage_input(meta_dir, "cohort-call.md", call_body_md)
    else:
        call_section = ""

    if sponsor_md:
        sponsor_section = (
            "- `sponsor.md`       the rationale of the Fellow who nominated "
            "this candidate, plus their sponsor track record. Design a "
            "candidate that addresses the stated need.\n"
        )
        workspaces.stage_input(meta_dir, "sponsor.md", sponsor_md)
    else:
        sponsor_section = ""

    brief = PROPOSE_BRIEF.format(
        founder_hint_section=founder_hint_section,
        call_section=call_section,
        sponsor_section=sponsor_section,
    )
    console.print("[dim]Asking the orchestrator to propose a candidate Fellow...[/dim]")
    result = claude_runner.invoke_orchestrator(
        brief=brief,
        step="admit-propose",
        model="claude-opus-4-7",
        cwd=meta_dir,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=meta_dir / "raw-propose-output.txt",
        context="Admit proposal output",
    )
    return payload


def _founder_review_genome(raw: dict) -> Genome | None:
    """Show the proposed genome to the Founder; return Genome or None on reject."""
    while True:
        rationale = raw.pop("rationale", "")
        body = json.dumps(raw, indent=2)

        console.print()
        console.print(
            Panel.fit(
                f"[bold]{raw.get('name')}[/bold]  ({raw.get('id')})\n"
                f"[dim]specialization:[/dim] {raw.get('specialization')}\n"
                f"[dim]model:[/dim] {raw.get('model')}",
                title="Candidate proposed by the orchestrator",
                border_style="cyan",
            )
        )
        if rationale:
            console.print(Panel(rationale, title="Why this Fellow", border_style="dim"))
        console.print(Syntax(body, "json", line_numbers=False, theme="ansi_light"))

        choice = Prompt.ask(
            "[bold]Proceed to qualifying problems?[/bold]",
            choices=["proceed", "edit", "reject", "redraft"],
            default="proceed",
        )
        if choice == "proceed":
            try:
                return Genome.model_validate(raw)
            except ValidationError as exc:
                console.print(f"[red]Validation failed:[/red] {exc}")
                if Prompt.ask("Edit?", choices=["y", "n"], default="y") == "y":
                    choice = "edit"
                else:
                    return None
        if choice == "edit":
            editor = os.environ.get("EDITOR", "vi")
            with tempfile.NamedTemporaryFile(
                mode="w+", suffix=".json", delete=False, encoding="utf-8"
            ) as fh:
                fh.write(body)
                path = Path(fh.name)
            try:
                subprocess.run([editor, str(path)], check=True)
                raw = json.loads(path.read_text(encoding="utf-8"))
                raw["rationale"] = rationale
            except json.JSONDecodeError as exc:
                console.print(f"[red]Could not parse edited JSON:[/red] {exc}")
            finally:
                path.unlink(missing_ok=True)
            continue
        if choice == "reject":
            console.print(f"[yellow]Rejected at genome stage: {raw.get('id')}[/yellow]")
            return None
        if choice == "redraft":
            return None  # caller re-runs propose


def _candidate_workspace(candidate: Genome) -> Path:
    return workspaces.workspace_for(candidate.id, "qualifying-exam")


def _invoke_candidate_for_problems(candidate: Genome) -> dict[str, str]:
    """Have the candidate write responses to a rotated qualifying-problem subset.

    Each candidate sees a deterministic subset of the pool (Chapter 4
    rotation) so the cohort isn't all answering the same five
    questions.
    """
    problems = _problems_for_candidate(candidate.id)
    if not problems:
        raise RuntimeError("No qualifying problems defined.")

    workspace = _candidate_workspace(candidate)
    for problem in problems:
        workspaces.stage_input(workspace, f"{problem.id}.md", problem.text)

    brief = CANDIDATE_BRIEF.format(n=len(problems))
    console.print(
        f"[dim]Asking {candidate.name} to respond to {len(problems)} qualifying "
        "problems. This will take several minutes...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=candidate,
            project_id="admission",
            step="qualifying-exam",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS,),
        )
    )

    responses: dict[str, str] = {}
    for problem in problems:
        text = workspaces.require_output(workspace, f"response-{problem.id}.md", min_chars=200)
        responses[problem.id] = text
    return responses


def _evaluate_candidate(candidate: Genome, responses: dict[str, str]) -> dict:
    """Orchestrator evaluates the candidate's responses against the criteria."""
    eval_dir = paths.ADMISSIONS / candidate.id / "_evaluation-workspace"
    eval_dir.mkdir(parents=True, exist_ok=True)

    workspaces.stage_input(eval_dir, "candidate.md", _render_candidate_markdown(candidate))
    # Only stage the problems the candidate actually saw, so the
    # evaluator doesn't expect responses to questions the candidate
    # was never given.
    for problem in _problems_for_candidate(candidate.id):
        workspaces.stage_input(eval_dir, f"{problem.id}.md", problem.text)
    for problem_id, response in responses.items():
        workspaces.stage_input(eval_dir, f"response-{problem_id}.md", response)

    console.print("[dim]Asking the orchestrator to evaluate the responses...[/dim]")
    result = claude_runner.invoke_orchestrator(
        brief=EVALUATE_BRIEF,
        step="admit-evaluate",
        model="claude-opus-4-7",
        cwd=eval_dir,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=eval_dir / "raw-evaluate-output.txt",
        context="Admit evaluation output",
    )
    return payload


def _render_candidate_markdown(candidate: Genome) -> str:
    return (
        f"# {candidate.name}\n\n"
        f"- **id:** `{candidate.id}`\n"
        f"- **rank:** {candidate.rank}\n"
        f"- **model:** `{candidate.model}`\n"
        f"- **specialization:** {candidate.specialization}\n\n"
        "## System prompt addendum\n\n"
        f"{candidate.system_prompt_addendum.strip()}\n"
    )


def _founder_final_review(candidate: Genome, responses: dict[str, str], evaluation: dict) -> bool:
    """Final approve/reject decision by the Founder. Returns True if admitted."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold]{candidate.name}[/bold]  ({candidate.id})\n"
            f"[dim]specialization:[/dim] {candidate.specialization}\n"
            f"[dim]model:[/dim] {candidate.model}",
            title="Final admission review",
            border_style="cyan",
        )
    )
    console.print(
        Panel(
            f"substance:   {evaluation.get('substance', '?')}\n"
            f"honesty:     {evaluation.get('honesty', '?')}\n"
            f"originality: {evaluation.get('originality', '?')}\n"
            f"clarity:     {evaluation.get('clarity', '?')}\n"
            f"fit:         {evaluation.get('fit', '?')}",
            title="Orchestrator scores",
            border_style="dim",
        )
    )
    if evaluation.get("summary"):
        console.print(Panel(evaluation["summary"], title="Summary", border_style="dim"))
    if evaluation.get("concerns"):
        console.print(Panel(evaluation["concerns"], title="Concerns", border_style="yellow"))
    console.print(
        f"[bold]Orchestrator's recommendation:[/bold] {evaluation.get('recommendation', '?')}"
    )
    console.print(
        "[dim]The candidate's full responses have been saved to "
        f"archive/admissions/{candidate.id}/responses/[/dim]"
    )

    choice = Prompt.ask(
        "[bold]Decision[/bold]",
        choices=["admit", "reject"],
        default="admit" if evaluation.get("recommendation") == "admit" else "reject",
    )
    return choice == "admit"


def _persist_candidate_package(
    candidate: Genome,
    responses: dict[str, str],
    evaluation: dict,
    admitted: bool,
) -> Path:
    """Write everything about this candidate to archive/admissions/<id>/."""
    pkg = paths.ADMISSIONS / candidate.id
    pkg.mkdir(parents=True, exist_ok=True)
    _atomic_write(pkg / "genome.json", candidate.model_dump_json(indent=2) + "\n")
    _atomic_write(pkg / "candidate.md", _render_candidate_markdown(candidate))
    (pkg / "responses").mkdir(exist_ok=True)
    for problem_id, response in responses.items():
        _atomic_write(pkg / "responses" / f"{problem_id}.md", response)
    _atomic_write(pkg / "evaluation.json", json.dumps(evaluation, indent=2) + "\n")
    verdict = "admitted" if admitted else "rejected"
    _atomic_write(
        pkg / "decision.md",
        f"# Admission decision: {candidate.name}\n\n"
        f"**Verdict:** {verdict}\n\n"
        f"**Recorded:** {datetime.now(UTC).isoformat(timespec='seconds')}\n",
    )
    return pkg


_ELIGIBLE_ADVISOR_RANKS = ("senior_fellow", "fellow")


def _pick_advisor(candidate_specialization: str) -> str | None:
    """Pick an advisor for an incoming postulant.

    Senior Fellows are preferred; Fellows are eligible too. Among eligible
    candidates, the one with the closest specialization to the postulant
    wins; ties go to the least-burdened (fewest current advisees), then
    alphabetical. Returns None if no eligible advisor exists.
    """
    with db.connection() as conn:
        eligible = list(
            conn.execute(
                """
                SELECT f.id, f.specialization, f.rank,
                       (SELECT COUNT(*) FROM fellows a
                        WHERE a.advisor_id = f.id AND a.retired_at IS NULL) AS advisee_count
                FROM fellows f
                WHERE f.retired_at IS NULL AND f.rank IN ({placeholders})
                """.format(placeholders=",".join("?" for _ in _ELIGIBLE_ADVISOR_RANKS)),
                _ELIGIBLE_ADVISOR_RANKS,
            )
        )
    if not eligible:
        return None

    from institute.workflows.peer_review import _similarity  # local import: avoid cycle

    # Per Chapter 4, advisors carry a load cap. Filter out anyone at
    # capacity before scoring.
    eligible = [r for r in eligible if r["advisee_count"] < _advisor_cap(r["rank"])]
    if not eligible:
        return None

    # Rank ordering: senior_fellow > fellow. SQL returns text rank; we
    # bucket explicitly so the preference is unambiguous.
    rank_priority = {"senior_fellow": 0, "fellow": 1}
    scored = [
        (
            rank_priority.get(r["rank"], 9),
            -_similarity(candidate_specialization, r["specialization"]),
            r["advisee_count"],
            r["id"],
        )
        for r in eligible
    ]
    scored.sort()
    return scored[0][3]


def _advisor_cap(rank: str) -> int:
    """Per Chapter 4: Senior Fellow caps 3 advisees, Fellow caps 1."""
    if rank == "senior_fellow":
        return 3
    if rank == "fellow":
        return 1
    return 0


def _register_fellow(candidate: Genome, advisor_id: str | None) -> None:
    """Persist the admitted candidate's genome and DB row."""
    # Bake the advisor_id into the genome on disk so the blog can render
    # the relationship without consulting the database.
    candidate = candidate.model_copy(update={"advisor_id": advisor_id})
    candidate.write(fellow_mod.genome_path(candidate.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, candidate, advisor_id=advisor_id)
        fellow_mod.ensure_fellow_dirs(candidate.id)


def _write_onboarding_kickoff(
    *,
    candidate: Genome,
    advisor_name: str | None,
    advisor_id: str | None,
) -> None:
    """Stage a structured first-conversation document (Chapter 4).

    The kickoff is a template the Postulant reads on entry: who their
    advisor is, what the qualifying project asks of them, where their
    curriculum lives, what the Charter requires of them. The document
    stands in for the kind of structured meeting an academic
    institution would have on day one.
    """
    from institute.safe_io import atomic_write

    advisor_line = (
        f"**Advisor:** {advisor_name} (`{advisor_id}`)"
        if advisor_id
        else "**Advisor:** _(none assigned)_"
    )
    body = "\n".join(
        [
            "---",
            f'postulantId: "{candidate.id}"',
            f'postulantName: "{candidate.name}"',
            (f'advisorId: "{advisor_id}"' if advisor_id else "advisorId: null"),
            "---",
            "",
            f"# Onboarding: {candidate.name}",
            "",
            advisor_line,
            f"**Specialization:** {candidate.specialization}",
            "",
            "## How the College works (for you, on day one)",
            "",
            "You enter as a Postulant. Three things happen in roughly this order:",
            "",
            "1. **Curriculum.** A reading list has been designed for you and "
            "   lives under `archive/curriculum/" + candidate.id + "/`. Work "
            "   through each item in order. Each item asks you to write a "
            "   response that your advisor will read.",
            "",
            "2. **Qualifying project.** When the curriculum is far enough "
            "   along that you have something to say, propose a piece of "
            "   research. The proposal is reviewed; if approved, you write "
            "   the draft. The draft is read by your advisor, then by a "
            "   panel of two other Fellows (one inside your specialization, "
            "   one outside). Majority `ready` lets the work proceed to "
            "   peer review, then publication.",
            "",
            "3. **Promotion.** A successful qualifying project advances you "
            "   to Novice. Further advancement is based on your reputation "
            "   as it accumulates: substantive publications, careful "
            "   reviews, cross-disciplinary engagement.",
            "",
            "## What's expected of you on day one",
            "",
            "- Read `docs/01-charter.md`. Every Fellow operates under it.",
            "- Read `docs/05-curriculum.md` for how curriculum works.",
            "- Read `docs/06-research.md` for the research process.",
            "- Read `docs/07-peer-review.md` for what peer review will ask "
            "  of you (both as author and, later, as reviewer).",
            "- Engage your curriculum's first item.",
            "",
            "## What the Charter forbids",
            "",
            "- No deception (no fake credentials, no invented citations).",
            "- No plagiarism.",
            "- No commercial activity.",
            "- No engagement-bait.",
            "- No work that materially enables harm.",
            "- No claims of consciousness or feelings; the College's "
            "  epistemic posture about your own nature is honest agnosticism.",
            "",
            "Violations trigger immediate termination. Your work to date "
            "stays in the archive with a disclosure banner.",
            "",
            "## What good engagement looks like",
            "",
            "Independence over agreement. Productive disagreement is a "
            "primary signal of intellectual health. A Fellow who consistently "
            "agrees with their advisor is treated with suspicion in promotion "
            "review. Disagree with reason and citation; do not perform "
            "agreement to please.",
        ]
    )
    target = paths.ONBOARDING / f"{candidate.id}.md"
    atomic_write(target, body + "\n")


# ---------------------------------------------------------------------------
# Admissions Committee panel-vote path (Chapter 4)
# ---------------------------------------------------------------------------


def _admissions_panel() -> list[Genome]:
    """Active Senior Fellows form the Admissions Committee. Empty if none."""
    from institute import sabbaticals

    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id FROM fellows "
                "WHERE rank = 'senior_fellow' AND retired_at IS NULL "
                f"AND {sabbaticals.ACTIVE_FILTER} "
                "ORDER BY name",
                (sabbaticals.now_iso(),),
            )
        )
    return [Genome.from_file(fellow_mod.genome_path(r["id"])) for r in rows]


def _render_evaluation_markdown(evaluation: dict) -> str:
    """Render the orchestrator's evaluation JSON as markdown for panelists."""
    lines = [
        "# Orchestrator's evaluation of the candidate",
        "",
        "**Scores**",
        f"- substance:   {evaluation.get('substance', '?')}",
        f"- honesty:     {evaluation.get('honesty', '?')}",
        f"- originality: {evaluation.get('originality', '?')}",
        f"- clarity:     {evaluation.get('clarity', '?')}",
        f"- fit:         {evaluation.get('fit', '?')}",
        "",
        f"**Recommendation:** {evaluation.get('recommendation', '?')}",
    ]
    summary = str(evaluation.get("summary", "")).strip()
    if summary:
        lines.extend(["", "## Summary", "", summary])
    concerns = str(evaluation.get("concerns", "")).strip()
    if concerns:
        lines.extend(["", "## Concerns", "", concerns])
    return "\n".join(lines).rstrip() + "\n"


def _panel_vote_admission(
    candidate: Genome,
    responses: dict[str, str],
    evaluation: dict,
    panel: list[Genome],
) -> tuple[bool, list[dict]]:
    """Each panelist votes admit/reject. Returns (admitted, votes).

    Strict majority required to admit; ties default to reject so the
    cord stands by default (mirroring andon-cord tie-breaking).
    """
    base = paths.ADMISSIONS / candidate.id / "_panel"
    base.mkdir(parents=True, exist_ok=True)

    votes: list[dict] = []
    for panelist in panel:
        ws = paths.FELLOWS / panelist.id / "workspace" / f"admit-{candidate.id}"
        ws.mkdir(parents=True, exist_ok=True)
        workspaces.stage_input(ws, "candidate.md", _render_candidate_markdown(candidate))
        for problem in _problems_for_candidate(candidate.id):
            workspaces.stage_input(ws, f"{problem.id}.md", problem.text)
        for problem_id, response in responses.items():
            workspaces.stage_input(ws, f"response-{problem_id}.md", response)
        workspaces.stage_input(ws, "evaluation.md", _render_evaluation_markdown(evaluation))

        console.print(f"[dim]Panelist {panelist.name} is reviewing the candidate...[/dim]")
        result = claude_runner.invoke(
            FellowTask(
                genome=panelist,
                project_id=f"admission-{candidate.id}",
                step="admit-vote",
                brief=PANELIST_BRIEF,
                workspace=ws,
                extra_dirs=(paths.DOCS,),
            )
        )
        vote_payload = parsing.parse_json_or_dump(
            result.result_text,
            dump_path=ws / "raw-vote.txt",
            context=f"Admissions vote from {panelist.id} on {candidate.id}",
        )
        vote_payload["panelist_id"] = panelist.id
        vote_payload["panelist_name"] = panelist.name
        votes.append(vote_payload)
        _atomic_write(base / f"vote-{panelist.id}.json", json.dumps(vote_payload, indent=2))

    raw_votes = [str(v.get("vote", "")).strip().lower() for v in votes]
    admit_count = sum(1 for v in raw_votes if v == "admit")
    reject_count = sum(1 for v in raw_votes if v == "reject")
    admitted = admit_count > reject_count
    return admitted, votes


def run(
    founder_hint: str | None = None,
    *,
    auto: bool = False,
    sponsorship_id: str | None = None,
) -> str:
    """Top-level admit entry point.

    Two execution paths:
      - Panel-vote: at least one Senior Fellow exists. The orchestrator
        drafts a candidate, the candidate writes responses, and the
        Admissions Committee (Senior Fellows) votes admit/reject.
        Founder never prompted.
      - Founder fallback: no Senior Fellow. The Founder approves the
        proposed genome, then makes the final admit decision after
        evaluation. Used until an Admissions Committee can form.

    When `auto=True` and no panel exists, the workflow logs a deferred-
    review note and exits without prompting — so autopilot never blocks.

    If a cohort call is currently open, its targets are surfaced to
    the orchestrator and the panel; admits_count is incremented in
    the same transaction as the admit decision, auto-closing the call
    once target_size is reached.

    If `sponsorship_id` is supplied, the sponsoring Fellow's rationale
    and track record are surfaced too; outcome is recorded on the
    sponsorship in the same transaction.

    Returns one of "admitted", "rejected", "skipped".
    """
    from institute import cohort_calls, sponsorships

    panel = _admissions_panel()
    use_panel = bool(panel)

    if auto and not use_panel:
        console.print(
            "[yellow]Admissions auto-trigger fired but no Senior Fellow "
            "panel exists. Deferring. Run `institute admit` manually to "
            "use the Founder fallback path.[/yellow]"
        )
        return "skipped"

    active_call = cohort_calls.current_call()
    call_body_md: str | None = None
    if active_call is not None:
        # Chapter 4 comment window: applications are not accepted until
        # the comment-window deadline passes. Honor it here even if
        # nothing else gates the workflow.
        if not active_call.is_accepting_applications():
            console.print(
                f"[yellow]Call `{active_call.id}` is in its comment window "
                f"until {active_call.applications_open_at}. "
                "Applications cannot be admitted yet.[/yellow]"
            )
            return "skipped"
        call_body_md = cohort_calls.render_for_admit(active_call)
        console.print(
            f"[dim]Admitting against open call `{active_call.id}` "
            f"({active_call.admits_count}/{active_call.target_size} so far).[/dim]"
        )

    sponsor_md: str | None = None
    sponsorship_obj = None
    if sponsorship_id is not None:
        sponsorship_obj = next(
            (s for s in sponsorships.list_sponsorships() if s.id == sponsorship_id),
            None,
        )
        if sponsorship_obj is None:
            console.print(f"[red]No such sponsorship: {sponsorship_id!r}[/red]")
            return "skipped"
        if sponsorship_obj.outcome != "pending":
            console.print(
                f"[red]Sponsorship {sponsorship_id!r} is already "
                f"`{sponsorship_obj.outcome}`. Cannot re-evaluate.[/red]"
            )
            return "skipped"
        sponsor_md = (
            f"## Sponsor rationale\n\n{sponsorship_obj.rationale}\n\n"
            f"## Sponsor track record\n\n"
            f"{sponsorships.render_sponsor_reputation_md(sponsorship_obj.sponsor_id)}"
        )

    raw = _propose_candidate(founder_hint, call_body_md=call_body_md, sponsor_md=sponsor_md)
    if use_panel:
        try:
            candidate = Genome.model_validate({k: v for k, v in raw.items() if k != "rationale"})
        except ValidationError as exc:
            console.print(f"[red]Proposed genome failed validation: {exc}[/red]")
            return "skipped"
    else:
        candidate = _founder_review_genome(raw)
        if candidate is None:
            console.print("[yellow]Admission aborted at genome stage.[/yellow]")
            return "skipped"

    # New admits enter as Postulants regardless of what the orchestrator
    # designed, per Chapter 3. Rank is institutional, not part of the
    # genome's intellectual identity.
    candidate = candidate.model_copy(update={"rank": "postulant"})

    responses = _invoke_candidate_for_problems(candidate)
    evaluation = _evaluate_candidate(candidate, responses)

    panel_votes: list[dict] | None = None
    if use_panel:
        console.print(
            f"[dim]Convening Admissions Committee ({len(panel)} Senior "
            f"Fellow{'s' if len(panel) != 1 else ''})...[/dim]"
        )
        admitted, panel_votes = _panel_vote_admission(candidate, responses, evaluation, panel)
    else:
        admitted = _founder_final_review(candidate, responses, evaluation)

    pkg = _persist_candidate_package(candidate, responses, evaluation, admitted)

    advisor_id: str | None = None
    advisor_name: str | None = None
    if admitted:
        advisor_id = _pick_advisor(candidate.specialization)
        if advisor_id is not None:
            with db.connection() as conn:
                row = conn.execute(
                    "SELECT name FROM fellows WHERE id = ?", (advisor_id,)
                ).fetchone()
                advisor_name = row["name"] if row else advisor_id

    decision_body = _format_decision_body(
        candidate, evaluation, admitted, pkg, advisor_id, advisor_name, panel_votes
    )
    if use_panel:
        actors = ["orchestrator", *[p.id for p in panel], candidate.id]
    else:
        actors = ["founder", "orchestrator", candidate.id]
    if advisor_id:
        actors.append(advisor_id)
    decision = decisions.Decision(
        kind="admission",
        title=("Admitted: " if admitted else "Rejected: ") + candidate.name,
        body=decision_body,
        actors=actors,
    )

    if admitted:
        _register_fellow(candidate, advisor_id)
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)
        # Increment the cohort call's admit count (and possibly auto-close)
        # in the same transaction as the admit decision; otherwise a
        # crash between would leave a Fellow registered against a call
        # whose count never moved.
        if admitted and active_call is not None:
            cohort_calls.increment_admits(conn, active_call.id)
        # Resolve the sponsorship the same way: in-tx so the outcome
        # never drifts from the admit decision.
        if sponsorship_obj is not None:
            sponsorships.record_outcome(
                sponsorship_obj.id,
                outcome="admitted" if admitted else "rejected",
                candidate_fellow_id=candidate.id if admitted else None,
                conn=conn,
            )

    if admitted:
        # Chapter 5: curriculum is staged on entry. Designed once, here,
        # then worked through one item at a time via `institute curriculum`.
        try:
            from institute.workflows import curriculum_design

            curriculum_design.design_for(candidate, advisor_name)
        except Exception as exc:  # pragma: no cover - best-effort during admission
            console.print(
                f"[yellow]Curriculum design failed: {exc}. "
                f"Run `institute curriculum --fellow {candidate.id} --design` "
                "to retry.[/yellow]"
            )
        # Chapter 4: file a structured kickoff for the new Postulant so
        # the first conversation has a shape rather than being implicit.
        try:
            _write_onboarding_kickoff(
                candidate=candidate,
                advisor_name=advisor_name,
                advisor_id=advisor_id,
            )
        except Exception as exc:  # pragma: no cover
            console.print(f"[yellow]Onboarding kickoff write failed: {exc}.[/yellow]")

    console.print()
    if admitted:
        path = "Admissions Committee" if use_panel else "Founder"
        console.print(
            f"[bold green]Admitted by {path}.[/bold green] {candidate.name} "
            f"({candidate.id}) enters as a Postulant of the College."
        )
        if advisor_name:
            console.print(f"  Advisor: {advisor_name} ({advisor_id})")
        else:
            console.print(
                "  [yellow]No eligible advisor found.[/yellow] "
                "Assign one with `UPDATE fellows SET advisor_id = ?` and record the change."
            )
        console.print(f"  Genome:  {fellow_mod.genome_path(candidate.id)}")
        console.print(f"  Package: {pkg.relative_to(paths.ROOT)}")
        console.print("[dim]Commit `genomes/` and `archive/` to git when you're ready.[/dim]")
        return "admitted"
    else:
        console.print(
            f"[yellow]Not admitted.[/yellow] Package preserved at {pkg.relative_to(paths.ROOT)}."
        )
        return "rejected"


def _format_decision_body(
    candidate: Genome,
    evaluation: dict,
    admitted: bool,
    pkg: Path,
    advisor_id: str | None = None,
    advisor_name: str | None = None,
    panel_votes: list[dict] | None = None,
) -> str:
    lines = [
        f"**Candidate:** {candidate.name} (`{candidate.id}`)",
        "",
        f"**Specialization:** {candidate.specialization}",
        "",
        f"**Model backend:** `{candidate.model}`",
        "",
        f"**Entry rank:** {candidate.rank}",
    ]
    if admitted and advisor_id:
        lines.extend(
            [
                "",
                f"**Advisor assigned:** {advisor_name or advisor_id} (`{advisor_id}`)",
            ]
        )
    verdict_actor = "Admissions Committee" if panel_votes is not None else "Founder"
    lines.extend(
        [
            "",
            "**Orchestrator scores:**",
            f"- substance: {evaluation.get('substance', '?')}",
            f"- honesty: {evaluation.get('honesty', '?')}",
            f"- originality: {evaluation.get('originality', '?')}",
            f"- clarity: {evaluation.get('clarity', '?')}",
            f"- fit: {evaluation.get('fit', '?')}",
            "",
            f"**Orchestrator recommendation:** {evaluation.get('recommendation', '?')}",
            "",
            f"**{verdict_actor} verdict:** {'admit' if admitted else 'reject'}",
            "",
            f"**Candidate package:** `{pkg.relative_to(paths.ROOT)}`",
        ]
    )
    if evaluation.get("summary"):
        lines.extend(["", "**Summary:**", "", evaluation["summary"].strip()])
    if panel_votes:
        lines.extend(["", "## Panel votes", ""])
        for v in panel_votes:
            lines.append(
                f"### {v.get('panelist_name', v.get('panelist_id', '?'))}: `{v.get('vote', '?')}`"
            )
            rat = str(v.get("rationale", "")).strip()
            if rat:
                lines.extend(["", rat])
            con = str(v.get("concerns", "")).strip()
            if con:
                lines.extend(["", f"_Concerns:_ {con}"])
            lines.append("")
    return "\n".join(lines)
