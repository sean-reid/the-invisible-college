"""Tests for the propose workflow's parsing and validation helpers."""

import pytest

from institute.workflows import propose

VALID_PROPOSAL = """## Title

A modest test of proposal parsing

## Question

Can we parse our own proposal format reliably?

## Background

Yes, if the parser is strict and the prompt template enforces structure.

## Approach

Write a regex matcher and feed it the expected sections.

## Expected output

A passing test.

## Resource estimate

Negligible.

## Anticipated failure modes

Failure to match section headers, or missing sections.

## Collaborators needed

None.
"""


def test_propose_brief_references_research_agenda() -> None:
    """When the lead Fellow chooses freely, their brief should point at
    research-agenda.md so the institutional priorities act as a
    gravitational field on topic selection, not just the recent
    Archive. A Founder-supplied topic overrides this, by design."""
    assert "research-agenda.md" in propose.TOPIC_SECTION_FREE


def test_extract_title_from_valid_proposal() -> None:
    title = propose._extract_title(VALID_PROPOSAL)
    assert title == "A modest test of proposal parsing"


def test_extract_title_raises_when_missing() -> None:
    bad = "## Question\n\nWhat happens?\n"
    with pytest.raises(RuntimeError, match="title"):
        propose._extract_title(bad)


def test_extract_title_raises_when_only_sections_present() -> None:
    bad = "## Title\n\n\n## Question\nx\n"
    with pytest.raises(RuntimeError, match="title"):
        propose._extract_title(bad)


def test_extract_title_from_h1() -> None:
    md = "# A real H1 title\n\n## Question\nq\n"
    assert propose._extract_title(md) == "A real H1 title"


def test_extract_title_from_leading_h2() -> None:
    """Fellows sometimes write the title as the first ## heading instead of `## Title`."""
    md = "## Citation Accuracy in ML Research\n\n## Question\nq\n"
    assert propose._extract_title(md) == "Citation Accuracy in ML Research"


def test_validate_sections_accepts_valid() -> None:
    assert propose._validate_sections(VALID_PROPOSAL) == []


def test_validate_sections_lists_missing() -> None:
    truncated = "## Title\n\nX\n\n## Question\n\nY\n"
    missing = propose._validate_sections(truncated)
    assert "Background" in missing
    assert "Approach" in missing
    assert "Question" not in missing


def test_slugify_is_url_safe() -> None:
    assert propose._slugify("A modest test of proposal parsing!") == (
        "a-modest-test-of-proposal-parsing"
    )
    assert propose._slugify("Foo / Bar :: Baz") == "foo-bar-baz"


def test_pick_lead_excludes_postulants(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Postulants can't be picked as proposal leads (they propose under sponsorship)."""
    from institute import db
    from institute import fellow as fellow_mod
    from institute.fellow import Genome

    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)

    seasoned = Genome(
        id="seasoned",
        name="Seasoned",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="theory of x",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    new_arrival = Genome(
        id="newcomer",
        name="Newcomer",
        rank="postulant",
        model="claude-sonnet-4-6",
        specialization="anything",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    seasoned.write(fellow_mod.genome_path(seasoned.id))
    new_arrival.write(fellow_mod.genome_path(new_arrival.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, seasoned)
        fellow_mod.register(conn, new_arrival)

    with db.connection() as conn:
        chosen = propose._pick_lead(conn, None)
    assert chosen.id == seasoned.id, "Postulant must not be picked as lead author"


def test_project_id_format() -> None:
    pid = propose._project_id("My research question")
    parts = pid.split("-")
    # date is YYYY-MM-DD = 3 dash-separated parts
    assert len(parts) >= 5
    assert parts[0].isdigit() and len(parts[0]) == 4  # year
    assert pid.endswith(parts[-1])
    # the last token is 4 hex chars
    assert len(parts[-1]) == 4
    assert all(c in "0123456789abcdef" for c in parts[-1])
