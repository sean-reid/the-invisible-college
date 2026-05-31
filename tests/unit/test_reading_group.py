"""Tests for the reading-group workflow's pure plumbing."""

from __future__ import annotations

from pathlib import Path

from institute import db
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


def test_pick_convener_demotes_fellows_with_failed_propose_attempts(
    isolated: Path,
) -> None:
    """A Fellow who has been picked as convener but whose
    `reading-group:propose` step kept returning non-zero should be
    pushed down the rotation, not re-picked every cycle. Without
    this the picker is permanently stuck on the first never-convened
    Fellow until they succeed - and a Fellow whose subprocess keeps
    erroring out burns budget every wake-up."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "alex", "Alex")
        _seed(conn, "ada", "Ada")
        # Alex has tried twice and both step_failures landed in the
        # audit log. Ada has never been picked.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) VALUES "
            "('2026-05-31T17:07:57+00:00', 'orchestrator,alex', 'step_failure', "
            "'reading-group:propose', 'x')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) VALUES "
            "('2026-05-31T20:09:38+00:00', 'orchestrator,alex', 'step_failure', "
            "'reading-group:propose', 'x')"
        )

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    # Ada, never-tried, wins over Alex who has failed.
    assert convener.id == "ada"


def test_pick_convener_falls_back_to_failed_proposer_if_only_option(
    isolated: Path,
) -> None:
    """When every other Fellow has already convened successfully and
    only the failed-propose Fellow is in the never-convened tier,
    they still get picked - one more try is better than blocking the
    rotation forever."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, "alex", "Alex")
        _seed(conn, "ada", "Ada")
        # Ada has convened; Alex has only failed.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES "
            "('2026-05-20T12:00:00+00:00', 'ada', 'reading_group', 'x')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) VALUES "
            "('2026-05-31T17:07:57+00:00', 'orchestrator,alex', 'step_failure', "
            "'reading-group:propose', 'x')"
        )

    with db.connection() as conn:
        convener = reading_group.pick_convener(conn)
    # Alex (failed-tier=1) ranks above Ada (convened-tier=2).
    assert convener.id == "alex"


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


def test_internal_only_brief_excludes_external_path() -> None:
    """The Postulant/Novice variant of the convener brief drops the
    external-reading option (and the WebFetch step) entirely so a
    new admit cannot blow past Claude's max-turns budget by trying
    to fetch a long open-access paper."""
    from institute.workflows.reading_group import (
        CONVENER_BRIEF,
        CONVENER_BRIEF_INTERNAL_ONLY,
    )

    # The internal-only brief never tells the convener to use WebFetch
    # or to write text.md (the external-content destination).
    assert "WebFetch" not in CONVENER_BRIEF_INTERNAL_ONLY
    assert "text.md" not in CONVENER_BRIEF_INTERNAL_ONLY
    assert "external" not in CONVENER_BRIEF_INTERNAL_ONLY.lower()
    # And it still asks for the same two required outputs.
    assert "selection.json" in CONVENER_BRIEF_INTERNAL_ONLY
    assert "framing.md" in CONVENER_BRIEF_INTERNAL_ONLY
    # The full brief still offers both paths (so Fellows and Senior
    # Fellows can pick external readings).
    assert "WebFetch" in CONVENER_BRIEF
    assert "external" in CONVENER_BRIEF.lower()
