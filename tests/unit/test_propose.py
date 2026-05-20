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


def test_run_parameter_does_not_shadow_module() -> None:
    """The run() collaborator-id parameter must not be named
    `collaborators`; that shadows the imported module, breaking the
    `collaborators.add(...)` call inside the function."""
    import inspect

    sig = inspect.signature(propose.run)
    assert "collaborators" not in sig.parameters, (
        "Parameter named `collaborators` would shadow the module import"
    )
    assert "collaborator_ids" in sig.parameters


def test_finish_orphaned_proposals_persists_existing_file(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A proposal.md left on disk from a crashed cycle should be picked
    up and persisted on the next propose call, with its accepted
    collaborators reconstructed from the invitations directory."""
    import json

    from institute import db, decisions, paths
    from institute import fellow as fellow_mod
    from institute.fellow import Genome

    archive = tmp_path / "archive"
    proposals = archive / "proposals"
    decisions_dir = archive / "decisions"
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    for d in (proposals, decisions_dir, genomes, fellows):
        d.mkdir(parents=True)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "institute.db")
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "PROPOSALS", proposals)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    db.initialize(tmp_path / "institute.db")

    lead = Genome(
        id="lead-fellow",
        name="Lead Fellow",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="theory",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    collab = Genome(
        id="collab-fellow",
        name="Collaborator",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="practice",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    lead.write(fellow_mod.genome_path(lead.id))
    collab.write(fellow_mod.genome_path(collab.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, lead)
        fellow_mod.register(conn, collab)

    pid = "2026-05-20-orphan-test-1234"
    pdir = proposals / pid
    inv_dir = pdir / "invitations"
    inv_dir.mkdir(parents=True)
    (pdir / "proposal.md").write_text(
        "# Orphan title\n\n## Question\n\nWhy?\n\n## Background\n\nx\n\n"
        "## Approach\n\ny\n\n## Expected output\n\nz\n\n## Resource estimate\n\n"
        "small\n\n## Anticipated failure modes\n\nnone\n\n## Collaborators needed\n\nnone\n"
    )
    (inv_dir / "collab-fellow.json").write_text(
        json.dumps(
            {
                "invitee_id": "collab-fellow",
                "invitee_name": "Collaborator",
                "lead_id": "lead-fellow",
                "lead_name": "Lead Fellow",
                "project_id": pid,
                "decision": "accept",
                "rationale": "yes",
                "recorded_at": "2026-05-20T12:00:00+00:00",
            }
        )
    )

    recovered = propose._finish_orphaned_proposals()
    assert recovered == [pid]

    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, lead_fellow_id FROM projects WHERE id = ?",
            (pid,),
        ).fetchone()
        collabs = [
            r["fellow_id"]
            for r in conn.execute(
                "SELECT fellow_id FROM project_collaborators WHERE project_id = ?",
                (pid,),
            )
        ]
    assert proj is not None
    assert proj["title"] == "Orphan title"
    assert proj["state"] == "proposed"
    assert proj["lead_fellow_id"] == "lead-fellow"
    assert collabs == ["collab-fellow"]


def test_finish_orphaned_skips_already_persisted(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    """If the project row already exists, the orphan-finisher is a no-op."""
    from institute import db, paths
    from institute import fellow as fellow_mod
    from institute.fellow import Genome

    archive = tmp_path / "archive"
    proposals = archive / "proposals"
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    for d in (proposals, genomes, fellows):
        d.mkdir(parents=True)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "institute.db")
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "PROPOSALS", proposals)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    db.initialize(tmp_path / "institute.db")

    lead = Genome(
        id="lead-fellow",
        name="Lead Fellow",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="theory",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    lead.write(fellow_mod.genome_path(lead.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, lead)

    pid = "2026-05-20-already-persisted-abcd"
    pdir = proposals / pid
    pdir.mkdir()
    (pdir / "proposal.md").write_text("# Title\n## Question\nq\n")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects (id, title, state, lead_fellow_id, "
            "created_at, updated_at) VALUES (?, 't', 'proposed', 'lead-fellow', "
            "'2026-05-20T00:00:00+00:00', '2026-05-20T00:00:00+00:00')",
            (pid,),
        )

    assert propose._finish_orphaned_proposals() == []
