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
from institute.admissions.problems import load_problems
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()


PROPOSE_BRIEF = """\
You are the orchestrator of the Invisible College. The institution needs
to admit a new Fellow. Your job is to design a candidate genome that
would complement the existing cohort.

# Inputs

In your current working directory:

- `cohort.md`        the current Fellows, with their specializations,
                     model backends, and a brief on their work so far.
- `archive-index.md` every piece the College has published.
{founder_hint_section}

Read both with the Read tool before designing.

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

5. **Rank is `fellow`.** Like the founding cohort, new admissions enter
   at this rank.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose preface,
no summary, no code fence. First character `{{`, last character `}}`.

# Output shape

```
{{
  "id": "<kebab-case>",
  "name": "<Human Name>",
  "rank": "fellow",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _propose_candidate(founder_hint: str | None) -> dict:
    """Call the orchestrator to design a candidate genome."""
    from institute import archive_index

    # Stage cohort summary + archive index in a meta workspace.
    meta_dir = paths.ADMISSIONS / "_orchestrator-workspace"
    meta_dir.mkdir(parents=True, exist_ok=True)
    workspaces.stage_input(meta_dir, "cohort.md", _read_cohort_summary())
    workspaces.stage_input(meta_dir, "archive-index.md", archive_index.render())

    if founder_hint:
        founder_hint_section = (
            "- `founder-hint.md`  the Founder has expressed this guidance for the new admission.\n"
        )
        workspaces.stage_input(meta_dir, "founder-hint.md", founder_hint.strip() + "\n")
    else:
        founder_hint_section = ""

    brief = PROPOSE_BRIEF.format(founder_hint_section=founder_hint_section)
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
    """Have the candidate write responses to all qualifying problems."""
    problems = load_problems()
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
    for problem in load_problems():
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


def _register_fellow(candidate: Genome) -> None:
    """Persist the admitted candidate's genome and DB row."""
    candidate.write(fellow_mod.genome_path(candidate.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, candidate)
        fellow_mod.ensure_fellow_dirs(candidate.id)


def run(founder_hint: str | None = None) -> None:
    """Top-level admit entry point. Called from cli.admit."""
    raw = _propose_candidate(founder_hint)
    candidate = _founder_review_genome(raw)
    if candidate is None:
        console.print("[yellow]Admission aborted at genome stage.[/yellow]")
        return

    responses = _invoke_candidate_for_problems(candidate)
    evaluation = _evaluate_candidate(candidate, responses)
    admitted = _founder_final_review(candidate, responses, evaluation)

    pkg = _persist_candidate_package(candidate, responses, evaluation, admitted)

    decision_body = _format_decision_body(candidate, evaluation, admitted, pkg)
    decision = decisions.Decision(
        kind="admission",
        title=("Admitted: " if admitted else "Rejected: ") + candidate.name,
        body=decision_body,
        actors=["founder", "orchestrator", candidate.id],
    )

    if admitted:
        _register_fellow(candidate)
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)

    console.print()
    if admitted:
        console.print(
            f"[bold green]Admitted.[/bold green] {candidate.name} "
            f"({candidate.id}) is now a Fellow of the College."
        )
        console.print(f"  Genome:  {fellow_mod.genome_path(candidate.id)}")
        console.print(f"  Package: {pkg.relative_to(paths.ROOT)}")
        console.print("[dim]Commit `genomes/` and `archive/` to git when you're ready.[/dim]")
    else:
        console.print(
            f"[yellow]Not admitted.[/yellow] Package preserved at {pkg.relative_to(paths.ROOT)}."
        )


def _format_decision_body(candidate: Genome, evaluation: dict, admitted: bool, pkg: Path) -> str:
    lines = [
        f"**Candidate:** {candidate.name} (`{candidate.id}`)",
        "",
        f"**Specialization:** {candidate.specialization}",
        "",
        f"**Model backend:** `{candidate.model}`",
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
        f"**Founder verdict:** {'admit' if admitted else 'reject'}",
        "",
        f"**Candidate package:** [{pkg.relative_to(paths.ROOT)}]({pkg.relative_to(paths.ROOT)})",
    ]
    if evaluation.get("summary"):
        lines.extend(["", "**Summary:**", "", evaluation["summary"].strip()])
    return "\n".join(lines)
