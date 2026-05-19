"""The College's standing list of Open Problems.

Per Chapter 2, the Institute Layer maintains a list of standing open
problems any Fellow may take on. This module is that list. Each
problem is a markdown file with YAML frontmatter under
`archive/open-problems/<slug>.md`. Open problems are surfaced into
the propose workflow as a hint — leads can browse and pick one when
choosing what to investigate.

The list is the design's diversity lever: without it, leads default
to whatever is nearest in their own episodic memory, which converges
hard on whatever the most recent publications happened to be about.
A standing list pulls attention sideways into questions the College
genuinely wants answered.

Lifecycle:
  - Founder or orchestrator adds a problem via `institute open-problems
    add` or by writing a file directly to archive/open-problems/.
  - A lead may take a problem by referencing its id in the Background
    section of their proposal. Marking the problem `resolved` is a
    follow-up action: `institute open-problems resolve <id>
    --project <pid>`.
  - The blog can render the list at /open-problems (future).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from institute import paths

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)


@dataclass(frozen=True)
class OpenProblem:
    """One entry on the standing Open Problems list."""

    slug: str  # filename stem under archive/open-problems/
    title: str
    body: str
    status: str  # 'open' or 'resolved'
    opened_at: str
    opened_by: str  # 'founder', 'orchestrator', or a fellow id
    tags: list[str]
    resolved_at: str | None = None
    resolved_by_project: str | None = None
    resolved_by_fellow: str | None = None

    @property
    def path(self) -> Path:
        return paths.OPEN_PROBLEMS / f"{self.slug}.md"


def _slugify(text: str) -> str:
    out: list[str] = []
    last_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    s = "".join(out).strip("-")
    return s[:60] if s else "untitled"


def _parse_frontmatter(text: str) -> tuple[dict[str, str | list[str]], str]:
    """Parse a YAML-ish frontmatter block. Returns (fields, body).

    Intentionally small parser — these files are machine-written by
    `add()` and meant to round-trip through `load()` without surprises.
    Supports scalar fields and `tags: [a, b, c]` lists. Unrecognized
    fields are preserved as strings.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    fields: dict[str, str | list[str]] = {}
    for line in raw.splitlines():
        line = line.rstrip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fields[key] = (
                [item.strip() for item in inner.split(",") if item.strip()] if inner else []
            )
        else:
            fields[key] = value
    return fields, body.lstrip("\n")


def _render_frontmatter(problem: OpenProblem) -> str:
    lines = [
        "---",
        f"id: {problem.slug}",
        f"title: {problem.title}",
        f"status: {problem.status}",
        f"opened_at: {problem.opened_at}",
        f"opened_by: {problem.opened_by}",
        f"tags: [{', '.join(problem.tags)}]",
    ]
    if problem.resolved_at:
        lines.append(f"resolved_at: {problem.resolved_at}")
    if problem.resolved_by_project:
        lines.append(f"resolved_by_project: {problem.resolved_by_project}")
    if problem.resolved_by_fellow:
        lines.append(f"resolved_by_fellow: {problem.resolved_by_fellow}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def load_all() -> list[OpenProblem]:
    """Every problem on disk, newest-opened first."""
    paths.OPEN_PROBLEMS.mkdir(parents=True, exist_ok=True)
    problems: list[OpenProblem] = []
    for path in sorted(paths.OPEN_PROBLEMS.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        problems.append(_load_path(path))
    problems.sort(key=lambda p: (p.status != "open", p.opened_at), reverse=False)
    # Open first (status sorts 'open' before 'resolved' because that's
    # how the boolean tuple key resolves). Within each group, oldest
    # first so reading top-to-bottom is chronological.
    return problems


def open_problems() -> list[OpenProblem]:
    """Subset that are still open."""
    return [p for p in load_all() if p.status == "open"]


def _load_path(path: Path) -> OpenProblem:
    text = path.read_text(encoding="utf-8")
    fields, body = _parse_frontmatter(text)
    tags = fields.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    return OpenProblem(
        slug=path.stem,
        title=str(fields.get("title") or "").strip(),
        body=body.strip(),
        status=str(fields.get("status") or "open").strip(),
        opened_at=str(fields.get("opened_at") or "").strip(),
        opened_by=str(fields.get("opened_by") or "").strip(),
        tags=[str(t) for t in tags],
        resolved_at=str(fields.get("resolved_at") or "").strip() or None,
        resolved_by_project=str(fields.get("resolved_by_project") or "").strip() or None,
        resolved_by_fellow=str(fields.get("resolved_by_fellow") or "").strip() or None,
    )


def get(slug: str) -> OpenProblem | None:
    path = paths.OPEN_PROBLEMS / f"{slug}.md"
    if not path.is_file():
        return None
    return _load_path(path)


def add(
    *,
    title: str,
    body: str,
    opened_by: str = "founder",
    tags: list[str] | None = None,
) -> OpenProblem:
    """Create a new open problem on disk. Raises if the slug collides."""
    slug = _slugify(title)
    if not slug:
        raise ValueError("Title produced an empty slug.")
    paths.OPEN_PROBLEMS.mkdir(parents=True, exist_ok=True)
    target = paths.OPEN_PROBLEMS / f"{slug}.md"
    if target.exists():
        raise ValueError(
            f"An open problem with slug {slug!r} already exists. Pick a "
            "different title or edit the existing file directly."
        )
    now = datetime.now(UTC).isoformat(timespec="seconds")
    problem = OpenProblem(
        slug=slug,
        title=title.strip(),
        body=body.strip(),
        status="open",
        opened_at=now,
        opened_by=opened_by,
        tags=list(tags or []),
    )
    _write(problem)
    return problem


def resolve(slug: str, *, project_id: str, fellow_id: str) -> OpenProblem:
    """Mark a problem resolved by a specific project + lead Fellow."""
    existing = get(slug)
    if existing is None:
        raise ValueError(f"No such open problem: {slug!r}")
    if existing.status == "resolved":
        raise ValueError(f"Open problem {slug!r} is already resolved.")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    updated = OpenProblem(
        slug=existing.slug,
        title=existing.title,
        body=existing.body,
        status="resolved",
        opened_at=existing.opened_at,
        opened_by=existing.opened_by,
        tags=existing.tags,
        resolved_at=now,
        resolved_by_project=project_id,
        resolved_by_fellow=fellow_id,
    )
    _write(updated)
    return updated


def _write(problem: OpenProblem) -> None:
    """Atomic write of a single problem file."""
    paths.OPEN_PROBLEMS.mkdir(parents=True, exist_ok=True)
    text = _render_frontmatter(problem) + problem.body.rstrip() + "\n"
    tmp = problem.path.with_suffix(problem.path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(problem.path)


def render_summary_md() -> str:
    """One-line-per-problem summary the propose workflow stages into the
    lead's workspace. Empty list yields a sentinel note so the brief's
    'if the file is present' check still makes sense.

    Surfaces tag-cluster distribution at the top so the lead can see
    which areas dominate the list (and ideally pick from an
    under-represented tag instead).
    """
    open_list = open_problems()
    if not open_list:
        return (
            "# Open Problems\n\n"
            "(None on the standing list. Free to pick any question that "
            "advances the Charter; the diversity-nudge guidance in your "
            "topic-guidance section still applies.)\n"
        )
    lines = [
        "# Open Problems",
        "",
        "Standing questions the College wants answered. Picking one is "
        "encouraged but not required. Reference the `id` in your "
        "Background section if you take one on.",
        "",
    ]
    cluster_summary = _render_cluster_summary(open_list)
    if cluster_summary:
        lines.append(cluster_summary)
        lines.append("")
    for p in open_list:
        tag_str = f" [{', '.join(p.tags)}]" if p.tags else ""
        lines.append(f"## `{p.slug}` — {p.title}{tag_str}")
        lines.append("")
        body_preview = p.body.strip().split("\n\n", 1)[0]
        lines.append(body_preview)
        lines.append("")
    return "\n".join(lines)


def _render_cluster_summary(open_list: list[OpenProblem]) -> str:
    """Tag-distribution header so the lead can see which clusters
    dominate the open list. Soft signal, not a block.
    """
    if not open_list:
        return ""
    tag_counts: dict[str, int] = {}
    untagged = 0
    for p in open_list:
        if not p.tags:
            untagged += 1
            continue
        for tag in p.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    if not tag_counts and not untagged:
        return ""
    total = len(open_list)
    sorted_tags = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    parts = [f"`{tag}` ({n})" for tag, n in sorted_tags]
    if untagged:
        parts.append(f"untagged ({untagged})")
    distribution = ", ".join(parts)
    # Flag saturation when one tag is at least 40% of the list and
    # the list is meaningfully populated. The lead can read this and
    # pick from an under-represented area instead.
    saturation_note = ""
    if total >= 5 and sorted_tags:
        top_tag, top_count = sorted_tags[0]
        if top_count / total >= 0.4:
            saturation_note = (
                f"\n\n> **Cluster saturation:** `{top_tag}` is "
                f"{top_count}/{total} of the open list. Strongly prefer a "
                "question outside this tag if you can."
            )
    return f"## Tag distribution\n\nOpen problems by tag: {distribution}.{saturation_note}"


__all__ = [
    "OpenProblem",
    "add",
    "get",
    "load_all",
    "open_problems",
    "render_summary_md",
    "resolve",
]
