"""Tests for the reading-group workflow's pure plumbing."""

from __future__ import annotations

from pathlib import Path

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
