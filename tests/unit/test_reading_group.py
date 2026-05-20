"""Tests for the reading-group workflow's pure plumbing."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import reading_group


def test_slugify_is_url_safe() -> None:
    assert reading_group._slugify("Stability vs. Structural Stability") == (
        "stability-vs-structural-stability"
    )
    assert reading_group._slugify("On Growth & Form (1917)") == "on-growth-form-1917"


def test_slugify_handles_empty_input() -> None:
    assert reading_group._slugify("") == "reading-group"
    assert reading_group._slugify("...!!!") == "reading-group"


def test_slugify_caps_length() -> None:
    long = "a" * 200
    assert len(reading_group._slugify(long)) == 60


class _DummyGenome:
    def __init__(self, fellow_id: str, name: str) -> None:
        self.id = fellow_id
        self.name = name


def test_render_others_pass1_excludes_self_and_missing(tmp_path: Path) -> None:
    genomes = {
        "ada": _DummyGenome("ada", "Ada Lovelace"),
        "henri": _DummyGenome("henri", "Henri Poincaré"),
        "pierre": _DummyGenome("pierre", "Pierre Bayle"),
    }
    ada_resp = tmp_path / "ada.md"
    ada_resp.write_text("Ada's first read.")
    henri_resp = tmp_path / "henri.md"
    henri_resp.write_text("Henri's first read.")
    # Pierre's file deliberately missing.
    pass1_paths = {
        "ada": ada_resp,
        "henri": henri_resp,
        "pierre": tmp_path / "pierre.md",
    }

    rendered = reading_group._render_others_pass1(pass1_paths, excluding="ada", genomes=genomes)
    assert "Ada Lovelace" not in rendered
    assert "Henri Poincaré" in rendered
    assert "Henri's first read." in rendered
    # Pierre's missing file is silently skipped.
    assert "Pierre Bayle" not in rendered


def test_metadata_md_includes_participants_and_note() -> None:
    genomes = [_DummyGenome("ada", "Ada Lovelace"), _DummyGenome("henri", "Henri Poincaré")]
    md = reading_group._metadata_md(
        title="On Growth and Form",
        slug="on-growth-and-form",
        participants=genomes,
        convener="founder",
        convener_note="Focus on the transformation grids chapter.",
        started_at="2026-05-20T12:00:00+00:00",
    )
    assert "On Growth and Form" in md
    assert "Ada Lovelace" in md
    assert "Henri Poincaré" in md
    assert "transformation grids" in md
    assert "founder" in md


def test_metadata_md_omits_empty_convener_note() -> None:
    md = reading_group._metadata_md(
        title="t",
        slug="t",
        participants=[_DummyGenome("ada", "Ada")],
        convener="founder",
        convener_note="",
        started_at="2026-05-20T12:00:00+00:00",
    )
    assert "Convener's note" not in md


# ---------------------------------------------------------------------------
# pick_convener: least-recently-led rotation
# ---------------------------------------------------------------------------


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    archive = tmp_path / "archive"
    decisions_dir = archive / "decisions"
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    for d in (archive, decisions_dir, genomes, fellows):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    db.initialize(db_path)
    return tmp_path


def _seed(conn, fellow_id: str, name: str) -> None:
    g = Genome(
        id=fellow_id,
        name=name,
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


def test_pick_convener_returns_none_when_no_fellows(isolated: Path) -> None:
    with db.connection() as conn:
        assert reading_group.pick_convener(conn) is None


def test_pick_convener_prefers_never_led(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "ada", "Ada")
        _seed(conn, "henri", "Henri")
        _seed(conn, "pierre", "Pierre")
        # Ada has convened before; Henri and Pierre have not.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) "
            "VALUES ('2026-05-19T12:00:00+00:00', 'ada,pierre,henri', 'reading_group', 'x')"
        )

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    # First in alphabetical order among never-led: henri.
    assert convener.id == "henri"


def test_pick_convener_falls_back_to_oldest_among_led(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "ada", "Ada")
        _seed(conn, "henri", "Henri")
        # Both have led; Ada more recently.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES "
            "('2026-05-15T12:00:00+00:00', 'henri', 'reading_group', 'x')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES "
            "('2026-05-19T12:00:00+00:00', 'ada', 'reading_group', 'x')"
        )

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    # Henri led longer ago, so they're next.
    assert convener.id == "henri"


def test_pick_convener_uses_first_actor_as_convener(isolated: Path) -> None:
    """Audit-log actor is a comma-joined list; the convener is the first."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "ada", "Ada")
        _seed(conn, "henri", "Henri")
        # Henri was convener (first actor); Ada was a participant.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES "
            "('2026-05-19T12:00:00+00:00', 'henri,ada', 'reading_group', 'x')"
        )

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    # Ada never led; Henri did. Ada is next.
    assert convener.id == "ada"


def test_pick_convener_skips_retired_fellows(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "ada", "Ada")
        _seed(conn, "old", "Old")
        conn.execute("UPDATE fellows SET retired_at = '2026-01-01' WHERE id = 'old'")

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    assert convener.id == "ada"


# ---------------------------------------------------------------------------
# CONVENER_BRIEF mentions the external option
# ---------------------------------------------------------------------------


def test_convener_brief_mentions_external_option() -> None:
    """The brief must explicitly invite external (open-access)
    readings alongside internal College publications. The mechanism
    only does its cross-pollination job if conveners know they can
    bring outside texts."""
    brief = reading_group.CONVENER_BRIEF
    assert "external" in brief.lower()
    assert "open-access" in brief.lower()
    assert "WebFetch" in brief
    # Both kinds documented.
    assert '"kind": "internal"' in brief
    assert '"kind": "external"' in brief


def test_convener_brief_warns_against_paywalled() -> None:
    """Copyright pressure: paywalled full-text dumps are out."""
    brief = reading_group.CONVENER_BRIEF
    assert "paywalled" in brief.lower()
