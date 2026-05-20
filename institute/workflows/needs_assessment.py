"""Chapter 4 admissions: Recruitment Needs Assessment.

Per the spec, before a cohort opens "the committee assesses what the
College needs": current Fellow population by specialization/rank/model,
recent publication trends, departed Fellows, diversity targets. The
output is a call for applications naming cohort size, specializations
recruited for, and intellectual orientations being prioritized.

This module runs that pass. The orchestrator reads the cohort
composition + archive index + open problems, returns a structured
call recommendation, the Founder approves (panel-fallback when an
Admissions Committee has formed), and on approve a cohort call opens.

The needs-assessment recommendation is its own decision record. Even
when the Founder declines, the analysis is preserved so future passes
can see what the orchestrator was thinking last time.
"""

from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from institute import archive_index, claude_runner, cohort_calls, db, decisions, parsing, paths

console = Console()


BRIEF = """\
You are the orchestrator of the Invisible College. The Admissions
Committee has asked you to perform a Recruitment Needs Assessment
ahead of opening a cohort call for applications.

# Inputs in your working directory

- `cohort.md`         current Fellows by specialization, rank, model
- `archive-index.md`  every piece the College has published so far
- `open-problems.md`  standing questions the College wants answered
- `coverage.md`       a precomputed breakdown of cohort coverage by
                      specialization keyword + model backend, with
                      gaps surfaced explicitly

Read all four with the Read tool before you analyze. Also consult
`docs/04-admissions.md` for the Committee's responsibilities and
`docs/11-risks.md` for the convergence-to-consensus failure mode.

# What the recommendation must do

Produce a call that pushes against current cohort weaknesses:

- **Diversify model backends** when one backend dominates.
- **Add specializations** the Archive needs but no current Fellow
  covers. Look at the Open Problems list and the publication trail —
  if one topic cluster is saturated, recruit OUT of it, not into it.
- **Restore departed capabilities** when retired Fellows have left
  gaps.
- **Set a realistic cohort size**. Chapter 4 says typically 3 to 8.
  Default to 3 unless the cohort is genuinely under-served.

A successful call says "we are short on X, recruit for X" with
concrete reasoning. A failing call says "more like what we have."

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no
code fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "target_size": <integer, 3 to 8>,
  "target_specializations": ["<short phrase>", ...],
  "target_models": ["<model id or family>", ...],
  "orientations": ["<intellectual-orientation phrase>", ...],
  "rationale": "<200-600 words explaining why these targets, with
                concrete references to the cohort + archive>"
}}
```

Empty arrays are fine. A call with no specific specializations is
"admit at committee discretion"; a call with no model targets is
"any backend." But the rationale must explain WHY the targets are
what they are, in a way the Founder can either trust or push back on.
"""


def _compute_coverage_md() -> str:
    """Precompute a coverage summary the orchestrator reads alongside
    the raw cohort markdown. Surfaces specialization keyword frequency,
    model-backend distribution, and the topic-cluster signal from
    recent publication titles.
    """
    with db.connection() as conn:
        active = list(
            conn.execute(
                "SELECT id, name, rank, model, specialization "
                "FROM fellows WHERE retired_at IS NULL ORDER BY name"
            )
        )
        retired = list(
            conn.execute(
                "SELECT id, name, rank, model, specialization, retired_at "
                "FROM fellows WHERE retired_at IS NOT NULL"
            )
        )
        publications = list(
            conn.execute(
                "SELECT title FROM projects WHERE state = 'published' "
                "ORDER BY updated_at DESC LIMIT 20"
            )
        )

    lines = ["# Cohort coverage analysis", ""]
    if not active:
        lines.append("_No active Fellows. The Founder must bootstrap the cohort first._")
        return "\n".join(lines) + "\n"

    # Model backend distribution.
    model_counts = Counter(r["model"] for r in active)
    total = sum(model_counts.values())
    lines.extend(["## Model backends", ""])
    for model, count in model_counts.most_common():
        share = count / total * 100
        lines.append(f"- `{model}`: {count}/{total} ({share:.0f}%)")
    top_model, top_count = model_counts.most_common(1)[0]
    if total >= 3 and top_count / total > 0.5:
        lines.append("")
        lines.append(
            f"> **Imbalance:** `{top_model}` is {top_count}/{total} of the "
            "active cohort. Chapter 11 calls a model monoculture a "
            "shared-blind-spots risk. Prefer a different backend for new admits."
        )

    lines.extend(["", "## Rank distribution", ""])
    rank_counts = Counter(r["rank"] for r in active)
    for rank, count in rank_counts.most_common():
        lines.append(f"- {rank}: {count}")

    lines.extend(["", "## Specializations (by keyword)", ""])
    keywords: Counter[str] = Counter()
    for r in active:
        for token in _spec_keywords(r["specialization"]):
            keywords[token] += 1
    for tok, count in keywords.most_common(10):
        lines.append(f"- `{tok}`: {count}")

    if retired:
        lines.extend(["", "## Departed Fellows", ""])
        for r in retired:
            lines.append(
                f"- {r['name']} (`{r['id']}`, was {r['rank']}, "
                f"{r['specialization']}, retired {r['retired_at']})"
            )

    if publications:
        lines.extend(["", "## Recent publication titles (newest first)", ""])
        for p in publications[:10]:
            lines.append(f"- {p['title']}")
        title_tokens = _publication_topic_tokens(publications)
        if title_tokens:
            lines.extend(["", "**Frequent topic tokens across publications:**", ""])
            for tok, count in title_tokens.most_common(8):
                lines.append(f"- `{tok}`: {count}")
            top_tok, top_n = title_tokens.most_common(1)[0]
            if top_n >= 3:
                lines.append("")
                lines.append(
                    f"> **Topic saturation signal:** `{top_tok}` appears in "
                    f"{top_n} of the last {min(len(publications), 10)} titles. "
                    "Strongly prefer recruits outside this cluster."
                )

    return "\n".join(lines) + "\n"


_STOPWORDS = frozenset(
    {
        "the",
        "and",
        "of",
        "a",
        "an",
        "in",
        "on",
        "to",
        "with",
        "for",
        "from",
        "by",
        "as",
        "at",
        "is",
        "are",
        "be",
        "this",
        "that",
        "or",
        "not",
        "but",
        "if",
        "it",
        "into",
        "out",
        "when",
        "how",
        "what",
        "where",
        "why",
        "which",
        "their",
        "its",
        "any",
    }
)


def _spec_keywords(spec: str) -> list[str]:
    if not spec:
        return []
    raw = "".join(ch.lower() if ch.isalnum() else " " for ch in spec).split()
    return [t for t in raw if len(t) >= 4 and t not in _STOPWORDS]


def _publication_topic_tokens(rows: list) -> Counter[str]:
    counter: Counter[str] = Counter()
    for r in rows:
        for token in _spec_keywords(r["title"] or ""):
            counter[token] += 1
    return counter


def _orchestrator_recommend() -> dict:
    """Stage inputs, invoke the orchestrator, parse the structured call."""
    from institute import open_problems
    from institute.workflows.admit import _read_cohort_summary

    meta_dir = paths.ADMISSIONS / "_orchestrator-workspace"
    meta_dir.mkdir(parents=True, exist_ok=True)
    _stage(meta_dir / "cohort.md", _read_cohort_summary())
    _stage(meta_dir / "archive-index.md", archive_index.render())
    _stage(meta_dir / "open-problems.md", open_problems.render_summary_md())
    _stage(meta_dir / "coverage.md", _compute_coverage_md())

    console.print("[dim]Asking the orchestrator to draft a Recruitment Needs Assessment...[/dim]")
    result = claude_runner.invoke_orchestrator(
        brief=BRIEF,
        step="needs-assessment",
        model="claude-opus-4-7",
        cwd=meta_dir,
        extra_dirs=(paths.DOCS, paths.ARCHIVE),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=meta_dir / "raw-needs-assessment.txt",
        context="Needs Assessment output",
    )
    return payload


def _stage(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _normalize_recommendation(payload: dict) -> dict:
    """Coerce the orchestrator's payload into the cohort_calls signature."""
    target_size = int(payload.get("target_size") or 0)
    if target_size < 1 or target_size > 8:
        raise ValueError(
            f"target_size must be 1-8 (got {target_size!r}). "
            "Chapter 4 caps at 8; the orchestrator returned out of range."
        )
    return {
        "target_size": target_size,
        "target_specializations": _as_list(payload.get("target_specializations")),
        "target_models": _as_list(payload.get("target_models")),
        "orientations": _as_list(payload.get("orientations")),
        "rationale": str(payload.get("rationale", "")).strip(),
    }


def _as_list(value: object) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _founder_decide(rec: dict) -> str:
    """Show the recommendation in the terminal; return approve/edit/abort."""
    console.print()
    console.print(
        Panel.fit(
            "[bold]Recruitment Needs Assessment[/bold]\n"
            f"[dim]proposed cohort size:[/dim] {rec['target_size']}",
            border_style="cyan",
        )
    )
    if rec["target_specializations"]:
        console.print(
            Panel(
                "\n".join(f"- {s}" for s in rec["target_specializations"]),
                title="Targeted specializations",
                border_style="dim",
            )
        )
    if rec["target_models"]:
        console.print(
            Panel(
                "\n".join(f"- `{m}`" for m in rec["target_models"]),
                title="Targeted model backends",
                border_style="dim",
            )
        )
    if rec["orientations"]:
        console.print(
            Panel(
                "\n".join(f"- {o}" for o in rec["orientations"]),
                title="Intellectual orientations",
                border_style="dim",
            )
        )
    if rec["rationale"]:
        console.print(Panel(rec["rationale"], title="Rationale", border_style="dim"))
    return Prompt.ask(
        "[bold]Open this call?[/bold]",
        choices=["approve", "abort"],
        default="approve",
    )


def _decision_body(rec: dict, outcome: str, call_id: str | None) -> str:
    lines = [
        f"**Outcome:** {outcome}",
        "",
        f"**Proposed target size:** {rec['target_size']}",
    ]
    if rec["target_specializations"]:
        lines.append(f"**Targeted specializations:** {', '.join(rec['target_specializations'])}")
    if rec["target_models"]:
        lines.append(f"**Targeted model backends:** {', '.join(rec['target_models'])}")
    if rec["orientations"]:
        lines.append(f"**Intellectual orientations:** {', '.join(rec['orientations'])}")
    if call_id:
        lines.append(f"**Opened call:** `{call_id}`")
    lines.extend(["", "## Rationale", "", rec["rationale"] or "(none provided)"])
    return "\n".join(lines)


def run(*, auto: bool = False) -> str:
    """Top-level Needs Assessment entry point.

    The orchestrator drafts a recommendation; the Founder approves or
    aborts. On approve, a cohort call is opened with the recommended
    targets. The recommendation is recorded as a decision either way,
    so the trail of "what the orchestrator wanted" survives the
    Founder's veto.

    `auto=True` opens the call without prompting (used by future
    autopilot integration). Aborts if a call is already open.

    Returns: 'opened', 'aborted', or 'skipped' (call already open).
    """
    if cohort_calls.current_call() is not None:
        active = cohort_calls.current_call()
        if active is not None:
            console.print(
                f"[yellow]A cohort call is already open ({active.id}). "
                "Close it before assessing again.[/yellow]"
            )
        return "skipped"

    payload = _orchestrator_recommend()
    try:
        rec = _normalize_recommendation(payload)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return "aborted"

    if auto:
        choice = "approve"
    else:
        choice = _founder_decide(rec)

    if choice != "approve":
        decision = decisions.Decision(
            kind="needs_assessment_aborted",
            title="Needs Assessment aborted",
            body=_decision_body(rec, outcome="aborted", call_id=None),
            actors=["orchestrator", "founder"],
        )
        with db.connection() as conn, db.transaction(conn):
            decisions.record(conn, decision)
        console.print("[yellow]Aborted; no call opened.[/yellow]")
        return "aborted"

    call = cohort_calls.open_call(
        target_size=rec["target_size"],
        target_specializations=rec["target_specializations"],
        target_models=rec["target_models"],
        orientations=rec["orientations"],
        opened_by="orchestrator+founder" if not auto else "orchestrator",
    )
    decision = decisions.Decision(
        kind="needs_assessment",
        title=f"Cohort call opened: {call.id}",
        body=_decision_body(rec, outcome="opened", call_id=call.id),
        actors=["orchestrator", "founder"] if not auto else ["orchestrator"],
    )
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)
    console.print(f"[green]Opened call:[/green] {call.id}")
    console.print(f"  size:           {call.target_size}")
    if call.target_specializations:
        console.print(f"  specializations: {', '.join(call.target_specializations)}")
    if call.target_models:
        console.print(f"  models:          {', '.join(call.target_models)}")
    if call.orientations:
        console.print(f"  orientations:    {', '.join(call.orientations)}")
    return "opened"
