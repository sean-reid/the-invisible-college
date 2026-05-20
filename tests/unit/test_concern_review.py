"""Tests for the Senior Fellow concern-review workflow.

Senior Fellow is a terminal indefinite rank. Calendar tenure review
is disabled for Senior Fellows by design; the only way to re-examine
one's standing is a peer-sponsored concern review with stated grounds.
Outcomes are restricted: confirm, release, or sabbatical-suggested.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import concern_review, promote


def _seed_fellow(conn, fellow_id: str, name: str, rank: str = "senior_fellow") -> Genome:
    g = Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)
    return g


# ---------------------------------------------------------------------------
# _tally
# ---------------------------------------------------------------------------


def test_tally_strict_majority_confirms() -> None:
    votes = [{"vote": "confirm"}, {"vote": "confirm"}, {"vote": "release"}]
    assert concern_review._tally(votes) == "confirm"


def test_tally_release_majority_returns_release() -> None:
    votes = [{"vote": "release"}, {"vote": "release"}, {"vote": "confirm"}]
    assert concern_review._tally(votes) == "release"


def test_tally_sabbatical_majority() -> None:
    votes = [
        {"vote": "sabbatical-suggested"},
        {"vote": "sabbatical-suggested"},
        {"vote": "confirm"},
    ]
    assert concern_review._tally(votes) == "sabbatical-suggested"


def test_tally_split_falls_back_to_none() -> None:
    """A split panel produces None; the caller treats that as confirm
    (the safe default — never strip Senior Fellow standing on a split)."""
    votes = [{"vote": "release"}, {"vote": "confirm"}]
    assert concern_review._tally(votes) is None


def test_tally_ignores_unknown_outcomes() -> None:
    votes = [
        {"vote": "promote"},  # invalid for this path
        {"vote": "confirm"},
        {"vote": "confirm"},
    ]
    assert concern_review._tally(votes) == "confirm"


def test_tally_empty_returns_none() -> None:
    assert concern_review._tally([]) is None


# ---------------------------------------------------------------------------
# Outcomes set
# ---------------------------------------------------------------------------


def test_valid_outcomes_are_restricted() -> None:
    """Concern review must not permit demotion or sideways rank changes."""
    assert concern_review.VALID_OUTCOMES == {
        "confirm",
        "release",
        "sabbatical-suggested",
    }
    assert "promote" not in concern_review.VALID_OUTCOMES
    assert "hold" not in concern_review.VALID_OUTCOMES
    assert "demote" not in concern_review.VALID_OUTCOMES


# ---------------------------------------------------------------------------
# Senior Fellow panel discovery
# ---------------------------------------------------------------------------


def test_panel_excludes_candidate(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "henri", "Henri")
        _seed_fellow(conn, "pierre", "Pierre")

    panel = concern_review._senior_panel("ada")
    ids = {g.id for g in panel}
    assert ids == {"henri", "pierre"}


def test_panel_excludes_retired_seniors(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "henri", "Henri")
        _seed_fellow(conn, "old", "Old")
        conn.execute("UPDATE fellows SET retired_at = '2026-01-01' WHERE id = 'old'")

    panel = concern_review._senior_panel("ada")
    assert {g.id for g in panel} == {"henri"}


# ---------------------------------------------------------------------------
# Promote.run() gating for Senior Fellow
# ---------------------------------------------------------------------------


def test_promote_refuses_senior_fellow_without_grounds(
    isolated: Path, capsys: pytest.CaptureFixture
) -> None:
    """Calling promote on a Senior Fellow without --concern-grounds is a no-op."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="senior_fellow")
        # Seed at least one publication so reputation.load_fellow returns non-None.
        conn.execute(
            "INSERT INTO projects (id, title, state, lead_fellow_id, "
            "created_at, updated_at) VALUES "
            "('p1', 'T', 'published', 'ada', '2026-01-01', '2026-01-02')"
        )

    result = promote.run("ada")
    assert result == "skipped"


def test_promote_refuses_senior_fellow_with_blank_grounds(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="senior_fellow")
        conn.execute(
            "INSERT INTO projects (id, title, state, lead_fellow_id, "
            "created_at, updated_at) VALUES "
            "('p1', 'T', 'published', 'ada', '2026-01-01', '2026-01-02')"
        )

    assert promote.run("ada", concern_grounds="   ") == "skipped"


# ---------------------------------------------------------------------------
# Calendar auto-trigger filter (cli helper)
# ---------------------------------------------------------------------------


def test_calendar_pick_excludes_senior_fellows() -> None:
    """The auto-triggered review candidate pool must not contain
    Senior Fellows. Calendar review is disabled for the terminal rank."""
    from institute.cli import _pick_review_candidate

    class _Rep:
        def __init__(self, fellow_id: str, name: str, rank: str, score: float) -> None:
            self.fellow_id = fellow_id
            self.name = name
            self.rank = rank

            # Minimum fields touched by _activity_score.
            class _A:
                publications = 0

            class _R:
                reviews_given = 0
                sticky_majors = 0

            self.author = _A()
            self.reviewer = _R()
            self.author.publications = int(score)

    cohort = [
        _Rep("ada", "Ada", "senior_fellow", 100.0),
        _Rep("henri", "Henri", "fellow", 5.0),
    ]
    chosen = _pick_review_candidate(cohort, "strong")
    assert chosen.fellow_id == "henri"


def test_calendar_pick_raises_when_only_seniors() -> None:
    """An all-Senior-Fellow cohort surfaces no calendar candidate."""
    from institute.cli import _pick_review_candidate

    class _Rep:
        def __init__(self) -> None:
            self.fellow_id = "ada"
            self.name = "Ada"
            self.rank = "senior_fellow"

            class _A:
                publications = 1

            class _R:
                reviews_given = 0
                sticky_majors = 0

            self.author = _A()
            self.reviewer = _R()

    with pytest.raises(ValueError, match="no calendar-eligible"):
        _pick_review_candidate([_Rep()], "strong")
