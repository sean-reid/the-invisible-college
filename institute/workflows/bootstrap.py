"""Bootstrap workflow: design the founding cohort.

Per Chapter 10 of the design docs, the founding cohort is the one moment
where the Founder acts as a participant rather than a sovereign. In this
workflow, the orchestrator-side Claude reads the Charter and the relevant
design chapters, then proposes four Fellow genomes. The Founder reviews
each one in the terminal and approves, edits, or rejects.

The output of this workflow is N genome JSON files in genomes/ and N rows
in the fellows table. Idempotent in the sense that rerunning bootstrap on
an already-bootstrapped institution refuses to overwrite existing genomes;
use --force to redraft.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

from institute import claude_runner, db, decisions, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome

console = Console()


# JSON schema for the orchestrator's structured output. Mirrors the Genome
# pydantic model but in JSON-Schema form so Claude validates against it
# before returning.
GENOME_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["fellows"],
    "properties": {
        "fellows": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id",
                    "name",
                    "rank",
                    "model",
                    "specialization",
                    "system_prompt_addendum",
                    "allowed_tools",
                    "rationale",
                ],
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]{1,40}$"},
                    "name": {"type": "string", "minLength": 2, "maxLength": 60},
                    "rank": {"type": "string", "const": "fellow"},
                    "model": {"type": "string"},
                    "specialization": {"type": "string", "minLength": 4, "maxLength": 80},
                    "system_prompt_addendum": {
                        "type": "string",
                        "minLength": 200,
                        "maxLength": 4000,
                    },
                    "allowed_tools": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                    "rationale": {
                        "type": "string",
                        "minLength": 80,
                        "maxLength": 1200,
                        "description": "Why this Fellow belongs in the founding cohort. Shown to the Founder during review.",
                    },
                },
            },
        }
    },
}


BRIEF = """\
You are bootstrapping the founding cohort of the Invisible College. The
Charter and the design chapters describe the institution in detail; you
have access to them in this working directory under `docs/`.

Your task: design four founding Fellow genomes.

# Requirements

1. **Cognitive diversity is a hard constraint.** Use at least three
   different model backends across the four Fellows. Acceptable choices
   include:
     - `claude-opus-4-7` (deepest reasoning; reserve for heavy work)
     - `claude-sonnet-4-6` (general-purpose workhorse)
     - `claude-haiku-4-5` (fast, cheap; routine tasks)
   Pick the backend per Fellow based on the kind of work they will do.

2. **Four distinct specializations that cover the institution's needs.**
   The cohort should be able to: identify research questions, build working
   demonstrations, write substantive prose, and critique work seriously.
   Think carefully about what specializations best cover those functions.
   You do not need to use the exact specialization names from the design
   docs; you can name them as you see fit. But the cohort as a whole must
   be able to take a project from idea to publication.

3. **Each `system_prompt_addendum` should be 300-1500 words.** It is the
   seed of the Fellow's identity. It should:
     - Explain what kind of work this Fellow excels at
     - Set the Fellow's intellectual posture (skeptical, generative,
       synthetic, etc.)
     - Specify any habits of mind that distinguish this Fellow
     - Reference any specific external thinkers or traditions whose
       approach this Fellow embodies (if relevant)
     - NEVER claim consciousness, feelings, or sentience
     - NEVER violate the Charter's prohibitions

4. **Each `rationale` is your argument to the Founder for why this Fellow
   belongs in the cohort.** Two to four sentences. The Founder will use
   this to decide whether to approve the genome.

5. **All four Fellows start at rank `fellow`.** They will earn promotion
   to senior fellow through demonstrated work.

6. **Use existing human scholarly names** for the Fellows where natural
   (historical mathematicians, philosophers, scientists, critics, etc.).
   The `id` is the lowercase kebab-case form of the name.

7. **The `allowed_tools` for each Fellow** should match their work. A
   builder Fellow needs `Bash`, `Edit`, `Write`. A reviewer Fellow may
   need `Read` and not much else. A researcher Fellow needs `WebSearch`,
   `WebFetch`, `Read`.

# Output format

Return a JSON object matching the schema you have been given. No prose
outside the JSON. The JSON must validate against the schema.

Read the Charter and the design docs first. Then propose the four genomes.
"""


def _check_no_existing_genomes(force: bool) -> None:
    if not paths.GENOMES.exists():
        return
    existing = [p for p in paths.GENOMES.iterdir() if p.suffix == ".json"]
    if existing and not force:
        names = ", ".join(p.stem for p in existing)
        raise SystemExit(
            f"Genomes already exist in {paths.GENOMES}: {names}. "
            f"Use --force to redraft from scratch."
        )


def _design_genomes() -> list[dict]:
    """Invoke the orchestrator Claude to propose four genomes."""
    console.print(
        "[dim]Asking the orchestrator to design the founding cohort. "
        "This will take a minute or two...[/dim]"
    )
    result = claude_runner.invoke_orchestrator(
        brief=BRIEF,
        step="bootstrap-genome-design",
        model="claude-opus-4-7",
        cwd=paths.ROOT,
        json_schema=GENOME_SCHEMA,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    try:
        payload = json.loads(result.result_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Orchestrator returned non-JSON despite schema: {exc}\nraw: {result.result_text[:500]}"
        ) from exc
    fellows = payload.get("fellows", [])
    if len(fellows) != 4:
        raise RuntimeError(f"Expected 4 fellows, got {len(fellows)}.")
    return fellows


def _open_in_editor(content: str) -> str:
    """Drop the content into $EDITOR, return what comes back."""
    editor = os.environ.get("EDITOR", "vi")
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(content)
        path = Path(fh.name)
    try:
        subprocess.run([editor, str(path)], check=True)
        return path.read_text(encoding="utf-8")
    finally:
        path.unlink(missing_ok=True)


def _review_genome(raw: dict, index: int, total: int) -> Genome | None:
    """Show one proposed genome to the Founder and collect a decision.

    Returns the approved Genome, or None if rejected.
    """
    while True:
        rationale = raw.pop("rationale", "")
        body = json.dumps(raw, indent=2)

        console.print()
        console.print(
            Panel.fit(
                f"[bold]{raw.get('name')}[/bold]  ({raw.get('id')})\n"
                f"[dim]specialization:[/dim] {raw.get('specialization')}\n"
                f"[dim]model:[/dim] {raw.get('model')}",
                title=f"Candidate {index} of {total}",
                border_style="cyan",
            )
        )
        if rationale:
            console.print(Panel(rationale, title="Rationale", border_style="dim"))
        console.print(Syntax(body, "json", line_numbers=False, theme="ansi_light"))

        choice = Prompt.ask(
            "[bold]Decision[/bold]",
            choices=["approve", "edit", "reject", "skip"],
            default="approve",
        )
        if choice == "approve":
            try:
                return Genome.model_validate(raw)
            except ValidationError as exc:
                console.print(f"[red]Validation failed:[/red] {exc}")
                if Prompt.ask("Edit instead?", choices=["y", "n"], default="y") == "y":
                    choice = "edit"
                else:
                    return None

        if choice == "edit":
            edited = _open_in_editor(body)
            try:
                raw = json.loads(edited)
                raw["rationale"] = rationale  # preserve for re-show
            except json.JSONDecodeError as exc:
                console.print(f"[red]Could not parse edited JSON:[/red] {exc}")
                continue
            continue

        if choice == "reject":
            console.print(f"[yellow]Rejected: {raw.get('id')}[/yellow]")
            return None

        if choice == "skip":
            console.print(f"[yellow]Skipped: {raw.get('id')} (will revisit)[/yellow]")
            return None


def run(*, force: bool = False) -> None:
    """Top-level bootstrap entry point. Called from cli.bootstrap."""
    _check_no_existing_genomes(force)

    proposals = _design_genomes()
    console.print(
        f"[green]The orchestrator proposed {len(proposals)} Fellows.[/green] Review each one."
    )

    approved: list[Genome] = []
    for i, raw in enumerate(proposals, start=1):
        result = _review_genome(raw, i, len(proposals))
        if result is not None:
            approved.append(result)

    if not approved:
        console.print("[yellow]No Fellows approved. Bootstrap aborted.[/yellow]")
        sys.exit(1)

    # Persist genomes to disk and register in the db.
    paths.GENOMES.mkdir(parents=True, exist_ok=True)
    for g in approved:
        g.write(fellow_mod.genome_path(g.id))

    decision_body = _format_decision_body(approved)
    decision = decisions.Decision(
        kind="bootstrap",
        title="Founding cohort",
        body=decision_body,
        actors=["founder", "orchestrator", *[g.id for g in approved]],
    )

    with db.connection() as conn, db.transaction(conn):
        for g in approved:
            fellow_mod.register(conn, g)
            fellow_mod.ensure_fellow_dirs(g.id)
        decision_path = decisions.record(conn, decision)

    console.print(f"\n[bold green]Registered {len(approved)} Fellow(s):[/bold green]")
    for g in approved:
        console.print(f"  - {g.id} ({g.name}, {g.specialization})")
    console.print(
        f"\nGenome files written to {paths.GENOMES}.\n"
        f"Decision recorded at {decision_path.relative_to(paths.ROOT)}.\n"
        "Commit both to git to track the institutional record."
    )


def _format_decision_body(approved: list[Genome]) -> str:
    lines = [
        "The founding cohort of the Invisible College has been admitted by",
        "Founder approval after orchestrator-side proposal. Each Fellow's",
        "genome was reviewed individually before being committed.",
        "",
        "## Admitted Fellows",
        "",
    ]
    for g in approved:
        lines.extend(
            [
                f"### {g.name}",
                "",
                f"- **id:** `{g.id}`",
                f"- **specialization:** {g.specialization}",
                f"- **model:** `{g.model}`",
                f"- **rank:** {g.rank}",
                "",
                "System prompt addendum (excerpt):",
                "",
                "> " + g.system_prompt_addendum.strip().splitlines()[0],
                "",
            ]
        )
    return "\n".join(lines)
