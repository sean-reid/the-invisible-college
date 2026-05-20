"""Tests for reviewer eligibility: marks, weights, decay, gate."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from institute import db, paths, reviewer_eligibility
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows.peer_review import _pick_review_slots


def _genome(fid: str, name: str, rank: str = "fellow") -> Genome:
    return Genome(
        id=fid,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fid}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed(conn, g: Genome) -> None:
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


# ---------------------------------------------------------------------------
# Schema + record
# ---------------------------------------------------------------------------


def test_reviewer_marks_table_exists(isolated: Path) -> None:
    with db.connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(reviewer_marks)")}
    assert {"fellow_id", "kind", "weight", "recorded_at", "expires_at"} <= cols


def test_record_mark_stores_default_weight(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        reviewer_eligibility.record_mark(
            conn,
            fellow_id="pierre",
            kind="frivolous_andon",
            reason="dismissed cord",
        )
    with db.connection() as conn:
        row = conn.execute(
            "SELECT kind, weight FROM reviewer_marks WHERE fellow_id = 'pierre'"
        ).fetchone()
    assert row["kind"] == "frivolous_andon"
    assert row["weight"] == 2.0  # default weight


def test_record_mark_rejects_unknown_kind(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        with pytest.raises(ValueError, match="Unknown mark kind"):
            reviewer_eligibility.record_mark(conn, fellow_id="pierre", kind="bogus", reason="x")


def test_record_mark_requires_reason(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        with pytest.raises(ValueError, match="reason must be non-empty"):
            reviewer_eligibility.record_mark(
                conn, fellow_id="pierre", kind="lazy_review", reason="   "
            )


# ---------------------------------------------------------------------------
# Active weight + eligibility
# ---------------------------------------------------------------------------


def test_active_weight_sums_unexpired_marks(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        reviewer_eligibility.record_mark(
            conn, fellow_id="pierre", kind="frivolous_andon", reason="a"
        )
        reviewer_eligibility.record_mark(
            conn, fellow_id="pierre", kind="calibration_miss", reason="b"
        )
    with db.connection() as conn:
        assert reviewer_eligibility.active_weight(conn, "pierre") == 3.0


def test_is_eligible_above_and_below_threshold(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        # One frivolous_andon (weight 2.0) — still eligible.
        reviewer_eligibility.record_mark(
            conn, fellow_id="pierre", kind="frivolous_andon", reason="a"
        )
    with db.connection() as conn:
        assert reviewer_eligibility.is_eligible(conn, "pierre") is True

    with db.connection() as conn, db.transaction(conn):
        # A second frivolous_andon brings them to 4.0 — sidelined.
        reviewer_eligibility.record_mark(
            conn, fellow_id="pierre", kind="frivolous_andon", reason="b"
        )
    with db.connection() as conn:
        assert reviewer_eligibility.is_eligible(conn, "pierre") is False


def test_expired_marks_do_not_count_toward_weight(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre"))
        # Insert a directly-expired mark manually so we can test decay
        # without sleeping for 90 days.
        past = (datetime.now(UTC) - timedelta(days=10)).isoformat(timespec="seconds")
        already_gone = (datetime.now(UTC) - timedelta(days=1)).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO reviewer_marks "
            "(fellow_id, kind, weight, reason, recorded_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("pierre", "frivolous_andon", 5.0, "stale", past, already_gone),
        )
    with db.connection() as conn:
        assert reviewer_eligibility.active_weight(conn, "pierre") == 0.0
        assert reviewer_eligibility.is_eligible(conn, "pierre") is True


# ---------------------------------------------------------------------------
# peer_review eligibility gate
# ---------------------------------------------------------------------------


def _seed_project(conn, project_id: str, lead: str) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    draft_path = paths.DRAFTS / project_id / "draft.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("# Test\n", encoding="utf-8")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, draft_path, "
        " review_round, created_at, updated_at) "
        "VALUES (?, ?, 'drafted', ?, ?, 1, ?, ?)",
        (
            project_id,
            f"Title {project_id}",
            lead,
            str(draft_path.relative_to(paths.ROOT)),
            now,
            now,
        ),
    )


def test_sidelined_fellow_filtered_from_reviewer_pool(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("clean", "Clean", "fellow"))
        _seed(conn, _genome("sidelined", "Sidelined", "fellow"))
        _seed(conn, _genome("other", "Other", "fellow"))
        _seed_project(conn, "proj-1", "ada")
        # Sideline "sidelined" with two frivolous_andon marks (4.0 weight).
        for i in range(2):
            reviewer_eligibility.record_mark(
                conn,
                fellow_id="sidelined",
                kind="frivolous_andon",
                reason=f"trigger {i}",
            )

    with db.connection() as conn:
        slots = _pick_review_slots(conn, "proj-1", "ada", 1)
    reviewer_ids = {s.reviewer_id for s in slots}
    assert "sidelined" not in reviewer_ids, "Sidelined fellow must not be picked as a reviewer"
    # The clean Fellows are picked.
    assert reviewer_ids <= {"clean", "other"}


# ---------------------------------------------------------------------------
# Auto-marks from andon dismiss
# ---------------------------------------------------------------------------


def test_dismissed_andon_marks_each_puller(isolated: Path) -> None:
    """When the Editorial Board dismisses a cord, every puller gets a frivolous_andon mark."""
    from institute.workflows.andon_review import _mark_frivolous_andon_pulls

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("puller-1", "Puller One"))
        _seed(conn, _genome("puller-2", "Puller Two"))
        _seed_project(conn, "proj-x", "ada")
        # Two reviewers pulled the cord; one didn't.
        for rid, pulled in [("puller-1", 1), ("puller-2", 1), ("other-rev", 0)]:
            if rid == "other-rev":
                _seed(conn, _genome("other-rev", "Other"))
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, dissent, round, andon_cord, andon_reason) "
                "VALUES (?, ?, ?, 'primary', 'major', 'confident', 'x', 0, 1, ?, ?)",
                (f"rev-{rid}", "proj-x", rid, pulled, "frivolous"),
            )

    _mark_frivolous_andon_pulls("proj-x", "Test piece")

    with db.connection() as conn:
        for pid in ("puller-1", "puller-2"):
            assert reviewer_eligibility.active_weight(conn, pid) == 2.0, (
                f"{pid} should have one frivolous_andon mark"
            )
        assert reviewer_eligibility.active_weight(conn, "other-rev") == 0.0, (
            "Non-puller must not be marked"
        )


# ---------------------------------------------------------------------------
# Auto-marks from editorial ruling divergence
# ---------------------------------------------------------------------------


def test_editorial_reject_marks_accept_voters(isolated: Path) -> None:
    """Reviewers who voted to accept get calibration_miss when the Board rejects."""
    from institute.workflows.editorial_review import _record_calibration_marks

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("accept-voter", "Accept Voter"))
        _seed(conn, _genome("reject-voter", "Reject Voter"))
        _seed_project(conn, "proj-y", "ada")
        for rid, rec in [("accept-voter", "accept"), ("reject-voter", "reject")]:
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, round) "
                "VALUES (?, ?, ?, 'primary', ?, 'confident', 'x', 2)",
                (f"rev-{rid}", "proj-y", rid, rec),
            )

    _record_calibration_marks("proj-y", "Test piece", "reject")

    with db.connection() as conn:
        assert reviewer_eligibility.active_weight(conn, "accept-voter") == 1.0, (
            "Reviewer who voted accept on a rejected piece should be marked"
        )
        assert reviewer_eligibility.active_weight(conn, "reject-voter") == 0.0, (
            "Reviewer who voted reject on a rejected piece should NOT be marked"
        )


def test_editorial_accept_marks_reject_voters(isolated: Path) -> None:
    """Symmetric: reviewer who voted reject takes calibration miss when Board accepts."""
    from institute.workflows.editorial_review import _record_calibration_marks

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("accept-voter", "Accept Voter"))
        _seed(conn, _genome("reject-voter", "Reject Voter"))
        _seed_project(conn, "proj-z", "ada")
        for rid, rec in [("accept-voter", "accept"), ("reject-voter", "reject")]:
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, round) "
                "VALUES (?, ?, ?, 'primary', ?, 'confident', 'x', 2)",
                (f"rev-{rid}", "proj-z", rid, rec),
            )

    _record_calibration_marks("proj-z", "Test piece", "accept")

    with db.connection() as conn:
        assert reviewer_eligibility.active_weight(conn, "accept-voter") == 0.0
        assert reviewer_eligibility.active_weight(conn, "reject-voter") == 1.0


def test_minor_revisions_consistent_with_accept(isolated: Path) -> None:
    """`minor` and `major` are leaning-accept; the Board accepting should NOT mark them."""
    from institute.workflows.editorial_review import _record_calibration_marks

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("minor-voter", "Minor"))
        _seed(conn, _genome("major-voter", "Major"))
        _seed_project(conn, "proj-m", "ada")
        for rid, rec in [("minor-voter", "minor"), ("major-voter", "major")]:
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, round) "
                "VALUES (?, ?, ?, 'primary', ?, 'confident', 'x', 2)",
                (f"rev-{rid}", "proj-m", rid, rec),
            )

    _record_calibration_marks("proj-m", "Test piece", "accept")

    with db.connection() as conn:
        assert reviewer_eligibility.active_weight(conn, "minor-voter") == 0.0
        assert reviewer_eligibility.active_weight(conn, "major-voter") == 0.0
