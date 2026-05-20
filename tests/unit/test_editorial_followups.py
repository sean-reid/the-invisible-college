"""Tests for the publish-time editorial follow-ups pass.

Covers the pure plumbing: editor eligibility selection (Senior Fellow
on the Board, not author/reviewer), footer rendering, and splicing the
footer above the References section. The full `run()` is exercised
through publish-workflow tests rather than mocking the Fellow
invocation here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db, editorial_followups, open_problems
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _genome(fellow_id: str, name: str, rank: str = "senior_fellow") -> Genome:
    return Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed(conn, g: Genome) -> None:
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


# ---------------------------------------------------------------------------
# Editor selection
# ---------------------------------------------------------------------------


def test_picks_board_member_not_on_paper(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("henri", "Henri"))
        _seed(conn, _genome("pierre", "Pierre"))

    with db.connection() as conn:
        editor = editorial_followups._eligible_editor(
            conn,
            lead_id="ada",
            collaborator_ids=[],
            reviewer_ids=["henri"],
        )
    assert editor is not None
    assert editor.id == "pierre"


def test_falls_back_to_any_senior_when_board_is_eaten(isolated: Path) -> None:
    """If every Board member is on the paper, fall back to other Seniors."""
    with db.connection() as conn, db.transaction(conn):
        for fid in ["aa", "bb", "cc"]:
            _seed(conn, _genome(fid, fid.upper()))
        _seed(conn, _genome("dd", "DD"))

    with db.connection() as conn:
        editor = editorial_followups._eligible_editor(
            conn,
            lead_id="aa",
            collaborator_ids=["bb"],
            reviewer_ids=["cc"],
        )
    assert editor is not None
    assert editor.id == "dd"


def test_returns_none_when_no_eligible_editor(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("henri", "Henri"))

    with db.connection() as conn:
        editor = editorial_followups._eligible_editor(
            conn,
            lead_id="ada",
            collaborator_ids=[],
            reviewer_ids=["henri"],
        )
    assert editor is None


def test_excludes_lead_and_collaborators(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("henri", "Henri"))
        _seed(conn, _genome("pierre", "Pierre"))

    with db.connection() as conn:
        editor = editorial_followups._eligible_editor(
            conn,
            lead_id="ada",
            collaborator_ids=["henri"],
            reviewer_ids=[],
        )
    assert editor is not None
    assert editor.id == "pierre"


def test_postulants_and_novices_cannot_edit(isolated: Path) -> None:
    """Only Senior Fellows are eligible. Lower ranks never appear."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pres", "Pres", rank="postulant"))
        _seed(conn, _genome("nov", "Nov", rank="novice"))
        _seed(conn, _genome("fel", "Fel", rank="fellow"))

    with db.connection() as conn:
        editor = editorial_followups._eligible_editor(
            conn,
            lead_id="anybody",
            collaborator_ids=[],
            reviewer_ids=[],
        )
    assert editor is None


# ---------------------------------------------------------------------------
# Footer rendering
# ---------------------------------------------------------------------------


def _make_problem(slug: str, title: str, body: str) -> open_problems.OpenProblem:
    return open_problems.OpenProblem(
        slug=slug,
        title=title,
        body=body,
        status="open",
        opened_at=datetime.now(UTC).isoformat(timespec="seconds"),
        opened_by="ada",
        tags=[],
    )


def test_render_footer_with_three_items() -> None:
    items = [
        _make_problem(
            "q-one",
            "A taxonomy of measurement",
            "What does a full taxonomy look like across domains?",
        ),
        _make_problem(
            "q-two",
            "Ill-conditioning and replication",
            "How systematic is the procedure-as-error pattern?",
        ),
        _make_problem(
            "q-three",
            "Historical pre-Tycho commentary",
            "Did any pre-modern thinker diagnose the instability?",
        ),
    ]
    out = editorial_followups._render_footer(items)
    assert out.startswith("## Questions this leaves open")
    assert "**A taxonomy of measurement.**" in out
    assert "**Ill-conditioning and replication.**" in out
    assert "**Historical pre-Tycho commentary.**" in out
    assert out.endswith("\n")


def test_render_footer_empty_returns_empty() -> None:
    assert editorial_followups._render_footer([]) == ""


def test_render_footer_strips_trailing_tags_and_separator() -> None:
    """An open-problem body filed before the upstream parser fix may
    still carry a trailing `Tags: ...` line and/or `---` separator.
    The footer renderer must strip these so they don't leak into the
    published Questions section."""
    item = _make_problem(
        "q",
        "Title",
        (
            "Real body paragraph one.\n\n"
            "Real body paragraph two.\n\n"
            "Tags: epistemology, philosophy of science\n\n"
            "---"
        ),
    )
    out = editorial_followups._render_footer([item])
    assert "Tags:" not in out
    assert "---" not in out
    assert "Real body paragraph one." in out
    assert "Real body paragraph two." in out


def test_render_footer_collapses_internal_whitespace() -> None:
    items = [_make_problem("q", "Title", "Line 1\n\nLine 2\n\tLine 3")]
    out = editorial_followups._render_footer(items)
    assert "Line 1 Line 2 Line 3" in out
    assert "\n\n" not in out.split("- **Title.**")[1]


# ---------------------------------------------------------------------------
# Splicing above References
# ---------------------------------------------------------------------------


def test_splice_above_references_inserts_before_refs_section() -> None:
    body = "Introduction text.\n\n## Method\n\nMethod text.\n\n## References\n\n[1] Author, year.\n"
    footer = "## Questions this leaves open\n\n- **Q.** Body.\n"
    out = editorial_followups.splice_above_references(body, footer)
    q_idx = out.index("## Questions this leaves open")
    r_idx = out.index("## References")
    assert q_idx < r_idx, "Questions section must appear before References"
    assert "Method text." in out
    assert "[1] Author, year." in out


def test_splice_appends_when_no_references() -> None:
    body = "Introduction text.\n\n## Method\n\nMethod text.\n"
    footer = "## Questions this leaves open\n\n- **Q.** Body.\n"
    out = editorial_followups.splice_above_references(body, footer)
    assert "## Questions this leaves open" in out
    assert out.rstrip().endswith("- **Q.** Body.")


def test_splice_empty_footer_returns_body_unchanged() -> None:
    body = "Some body\n\n## References\n\n[1]\n"
    assert editorial_followups.splice_above_references(body, "") == body


def test_splice_only_matches_h2_references_not_h3() -> None:
    body = "Body.\n\n### References to other work\n\nSee X.\n\n## References\n\n[1]\n"
    footer = "## Questions this leaves open\n\n- **Q.** Body.\n"
    out = editorial_followups.splice_above_references(body, footer)
    q_idx = out.index("## Questions this leaves open")
    h2_refs = out.index("## References\n")
    h3_refs = out.index("### References to other work")
    assert h3_refs < q_idx < h2_refs


# ---------------------------------------------------------------------------
# Candidates rendering
# ---------------------------------------------------------------------------


def test_candidates_md_includes_slug_and_body() -> None:
    items = [
        _make_problem("slug-a", "First question", "First body."),
        _make_problem("slug-b", "Second question", "Second body."),
    ]
    out = editorial_followups._candidates_md(items)
    assert "## First question" in out
    assert "`slug: slug-a`" in out
    assert "First body." in out
    assert "## Second question" in out
    assert "`slug: slug-b`" in out
    assert "Second body." in out


# ---------------------------------------------------------------------------
# No candidates: pass is a no-op without any Fellow invocation
# ---------------------------------------------------------------------------


def test_run_returns_empty_when_no_candidates(isolated: Path) -> None:
    with db.connection() as conn:
        result = editorial_followups.run(
            conn=conn,
            project_id="no-candidates",
            draft_md="# Draft\n\nBody.",
            lead_id="ada",
            collaborator_ids=[],
            reviewer_ids=[],
        )
    assert result.editor is None
    assert result.promoted == []
    assert result.discarded == []
    assert result.footer_md == ""
