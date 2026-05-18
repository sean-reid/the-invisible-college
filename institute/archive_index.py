"""Build a markdown index of the College's published work.

Workflows stage this index into the Fellow's workspace so the Fellow can
discover and cite prior publications. It is the simplest version of an
"Archive as a queryable resource": a single markdown file listing every
published piece with title, authors, date, abstract, and slug.

The Fellow reads it like any other workspace file with the Read tool.
For longer-term work (filtering, structured search) an MCP server would
fit better, but a flat index is enough as long as the body of published
work is small.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from institute.paths import BLOG_POSTS


@dataclass(frozen=True)
class IndexEntry:
    slug: str
    title: str
    authors: list[str]
    published_at: str  # ISO date string, normalized to YYYY-MM-DD
    abstract: str | None
    issue_number: int | None


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _yaml_scalar(value: str) -> str:
    """Unquote a YAML scalar value if it is wrapped in matching quotes."""
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def _yaml_string_list(value: str) -> list[str]:
    """Parse a YAML inline list of strings like ["a", "b"]."""
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    inner = value[1:-1]
    parts: list[str] = []
    buf: list[str] = []
    in_string = False
    quote = ""
    escape = False
    for ch in inner:
        if in_string:
            if escape:
                buf.append(ch)
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                in_string = False
            else:
                buf.append(ch)
        else:
            if ch in {'"', "'"}:
                in_string = True
                quote = ch
            elif ch == ",":
                if buf:
                    parts.append("".join(buf).strip())
                    buf = []
            elif ch.strip():
                buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return parts


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Return a flat dict of key -> raw-value (single-line) for the frontmatter."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        if line.startswith(" ") or line.startswith("\t"):
            # Skip nested or continuation lines; this index only needs flat scalars.
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


def _entry_from_file(path: Path) -> IndexEntry | None:
    """Parse one blog post markdown file into an IndexEntry, or None if invalid."""
    text = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    title = _yaml_scalar(fm.get("title", ""))
    if not title:
        return None
    authors = _yaml_string_list(fm.get("authors", "[]"))
    abstract = _yaml_scalar(fm.get("abstract", "")) or None
    published_raw = _yaml_scalar(fm.get("publishedAt", ""))
    # publishedAt may be a full ISO timestamp or just a date. Normalize.
    published_date = published_raw[:10] if published_raw else ""
    issue_raw = fm.get("issueNumber", "")
    try:
        issue = int(issue_raw) if issue_raw else None
    except ValueError:
        issue = None
    return IndexEntry(
        slug=path.stem,
        title=title,
        authors=authors,
        published_at=published_date,
        abstract=abstract,
        issue_number=issue,
    )


def load_entries() -> list[IndexEntry]:
    """Read every published piece in the blog content posts directory."""
    if not BLOG_POSTS.is_dir():
        return []
    entries = []
    for md in sorted(BLOG_POSTS.glob("*.md")):
        entry = _entry_from_file(md)
        if entry is not None:
            entries.append(entry)
    # Sort by issue number ascending if known, else by date.
    entries.sort(
        key=lambda e: (
            e.issue_number if e.issue_number is not None else 10**9,
            e.published_at,
        )
    )
    return entries


def render_markdown_index(entries: list[IndexEntry]) -> str:
    """Render the index as a markdown document for a Fellow's workspace."""
    if not entries:
        return (
            "# Archive index\n\n"
            "No prior publications. This is the first piece the College has produced.\n"
        )

    lines = [
        "# Archive index",
        "",
        "Every piece the College has published, oldest first. To cite one of",
        "these from your draft, use a markdown link to the post's slug:",
        "",
        "    [Ada's piece on floating-point](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/)",
        "",
        "The blog will render the link as an internal cross-reference and",
        "automatically show 'Cited by' backlinks on the cited piece.",
        "",
    ]

    for entry in entries:
        issue = f"#{entry.issue_number:02d} " if entry.issue_number is not None else ""
        date = entry.published_at or "(no date)"
        authors = ", ".join(entry.authors) if entry.authors else "(unknown author)"
        lines.append(f"## {issue}{entry.title}")
        lines.append("")
        lines.append(f"- **slug:** `{entry.slug}`")
        lines.append(f"- **link:** `posts/{entry.slug}/`")
        lines.append(f"- **authors:** {authors}")
        lines.append(f"- **published:** {date}")
        if entry.abstract:
            lines.append("")
            lines.append(entry.abstract)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render() -> str:
    """Convenience: load entries and render the index in one call."""
    return render_markdown_index(load_entries())
