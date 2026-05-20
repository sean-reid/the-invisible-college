"""Peer-review exclusion, conflicts of interest, and reputation roll-up for co-authors."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import collaborators, db, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows.peer_review import _pick_review_slots


def _genome(slug: str, name: str, *, rank: str = "fellow", spec: str = "general") -> Genome:
    return Genome(
        id=slug,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


@pytest.fixture()
def cohort(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Genome]:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)

    fellows = {
        "lead": _genome("lead", "Lead Lovelace", spec="applied"),
        "carol": _genome("carol", "Carol Critic", spec="theory"),
        "diana": _genome("diana", "Diana Diderot", spec="critical review"),
        "evan": _genome("evan", "Evan Essayist", spec="long-form essay"),
        "nina": _genome("nina", "Nina Novice", rank="novice", spec="theory"),
        "petra": _genome("petra", "Petra Postulant", rank="postulant", spec="anything"),
        "rita": _genome("rita", "Rita Retired", spec="cartography"),
    }
    with db.connection() as conn, db.transaction(conn):
        for g in fellows.values():
            g.write(tmp_path / "genomes" / f"{g.id}.json")
            fellow_mod.register(conn, g)
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (datetime.now(UTC).isoformat(timespec="seconds"), "rita"),
        )
    return fellows


def _insert_project(
    project_id: str,
    *,
    lead_id: str,
    state: str = "drafted",
    review_round: int = 1,
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, "x", state, lead_id, "draft.md", review_round, now, now),
        )


# --- peer review exclusion ----------------------------------------------


def test_peer_review_excludes_all_co_authors(cohort) -> None:
    """Round-1 reviewer pool excludes lead AND every collaborator."""
    _insert_project("p-exclude", lead_id="lead", state="drafted")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-exclude", fellow_id="carol")
        collaborators.add(conn, project_id="p-exclude", fellow_id="diana")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-exclude", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    # Lead, carol, and diana all sit out; the only remaining non-postulant,
    # non-retired Fellows are evan and nina.
    assert picked.isdisjoint({"lead", "carol", "diana"})
    assert picked <= {"evan", "nina"}


def test_peer_review_works_without_collaborators(cohort) -> None:
    """No collaborators on the project ⇒ reviewer pool unchanged."""
    _insert_project("p-solo", lead_id="lead", state="drafted")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-solo", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "lead" not in picked
    # All other (non-postulant, non-retired) Fellows are eligible.
    assert picked == {"carol", "diana", "evan"}


# --- conflict of interest (Chapter 7) -----------------------------------


def test_peer_review_excludes_advisor_of_lead(cohort) -> None:
    """A Fellow may not review work by their advisee (Chapter 7)."""
    # Give the lead an advisor; that advisor must be filtered out.
    with db.connection() as conn, db.transaction(conn):
        conn.execute("UPDATE fellows SET advisor_id = ? WHERE id = ?", ("carol", "lead"))
    _insert_project("p-advisor", lead_id="lead", state="drafted")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-advisor", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "carol" not in picked


def test_peer_review_excludes_advisees_of_lead(cohort) -> None:
    """A Fellow may not review work by their advisor (Chapter 7)."""
    with db.connection() as conn, db.transaction(conn):
        conn.execute("UPDATE fellows SET advisor_id = ? WHERE id = ?", ("lead", "carol"))
    _insert_project("p-advisee", lead_id="lead", state="drafted")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-advisee", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "carol" not in picked


def test_peer_review_excludes_advisor_of_collaborator(cohort) -> None:
    """CoI extends to advisors of collaborators, not just the lead."""
    with db.connection() as conn, db.transaction(conn):
        conn.execute("UPDATE fellows SET advisor_id = ? WHERE id = ?", ("diana", "evan"))
    _insert_project("p-collab-coi", lead_id="lead", state="drafted")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-collab-coi", fellow_id="evan")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-collab-coi", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "evan" not in picked  # collaborator
    assert "diana" not in picked  # collaborator's advisor


def test_peer_review_excludes_invitation_decliner(cohort) -> None:
    """A Fellow who declined a research-group invitation cannot review (Chapter 7)."""
    _insert_project("p-decliner", lead_id="lead", state="drafted")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO project_invitations "
            "(project_id, fellow_id, decision, rationale, invited_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("p-decliner", "carol", "decline", "too busy", now),
        )
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-decliner", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "carol" not in picked


def test_peer_review_accept_invitation_does_not_block(cohort) -> None:
    """Accepting an invitation makes the Fellow a co-author (already excluded);
    it should not separately get treated as a decliner-CoI even if the row
    happens to exist."""
    _insert_project("p-acceptor", lead_id="lead", state="drafted")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        # Carol accepted but isn't yet recorded as a collaborator (transient state).
        conn.execute(
            "INSERT INTO project_invitations "
            "(project_id, fellow_id, decision, rationale, invited_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("p-acceptor", "carol", "accept", "yes", now),
        )
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-acceptor", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    # Accepting alone shouldn't block: only declines are CoI.
    assert "carol" in picked


def test_decliner_ids_helper(cohort) -> None:
    """collaborators.decliner_ids returns the right set."""
    _insert_project("p-helper", lead_id="lead")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO project_invitations "
            "(project_id, fellow_id, decision, rationale, invited_at) "
            "VALUES (?, 'carol', 'decline', '', ?), (?, 'diana', 'accept', '', ?)",
            ("p-helper", now, "p-helper", now),
        )
    with db.connection() as conn:
        assert collaborators.decliner_ids(conn, "p-helper") == {"carol"}


# --- reputation aggregation ---------------------------------------------


def test_author_stats_counts_co_authored_publication(cohort) -> None:
    """A Fellow's publication count includes projects where they collaborated."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        # carol leads one published piece
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-led", "x", "published", "carol", "draft.md", 2, now, now),
        )
        # diana leads another, with carol as a collaborator
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-collab", "y", "published", "diana", "draft.md", 2, now, now),
        )
        collaborators.add(conn, project_id="p-collab", fellow_id="carol")

    with db.connection() as conn:
        stats = reputation.author_stats(conn, "carol")
    assert stats.publications == 2  # 1 led + 1 co-authored


def test_author_stats_counts_in_flight_co_authored(cohort) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-wip", "x", "researching", "lead", "draft.md", 1, now, now),
        )
        collaborators.add(conn, project_id="p-wip", fellow_id="carol")
    with db.connection() as conn:
        stats_lead = reputation.author_stats(conn, "lead")
        stats_carol = reputation.author_stats(conn, "carol")
    assert stats_lead.projects_in_flight == 1
    assert stats_carol.projects_in_flight == 1
