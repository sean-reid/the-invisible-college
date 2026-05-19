"""Tests for the research-group formation helpers.

Pure parsing and matching exercises only; invitation dispatch is
covered indirectly by the propose flow's integration test elsewhere.
"""

from __future__ import annotations

from institute.workflows import group_form


def test_extract_section_matches_canonical_heading() -> None:
    md = (
        "# Title\n\n## Question\nq\n\n## Collaborators needed\n"
        "I'd like Henri Poincare for the dynamical-systems angle.\n\n"
        "## Resource estimate\nx\n"
    )
    section = group_form.extract_collaborators_section(md)
    assert section is not None
    assert "Henri Poincare" in section
    assert "Resource estimate" not in section  # bounded by next H2


def test_extract_section_matches_synonyms() -> None:
    md = "## Collaborators\nNone needed.\n"
    section = group_form.extract_collaborators_section(md)
    assert section == "None needed."

    md2 = "## Required collaborators\nAda Lovelace.\n"
    section2 = group_form.extract_collaborators_section(md2)
    assert section2 == "Ada Lovelace."


def test_extract_section_returns_none_when_absent() -> None:
    md = "# Title\n\n## Question\nq\n"
    assert group_form.extract_collaborators_section(md) is None


def test_match_invitees_finds_named_fellow() -> None:
    cohort = [
        ("ada-lovelace", "Ada Lovelace"),
        ("henri-poincare", "Henri Poincaré"),
        ("pierre-bayle", "Pierre Bayle"),
    ]
    section = "I'd like Henri Poincaré to join for the dynamical-systems angle."
    assert group_form.match_invitees(section, cohort) == ["henri-poincare"]


def test_match_invitees_handles_accent_insensitive() -> None:
    """The lead may write 'Poincare' without the accent; we should match."""
    cohort = [("henri-poincare", "Henri Poincaré")]
    section = "Henri Poincare would be valuable."
    assert group_form.match_invitees(section, cohort) == ["henri-poincare"]


def test_match_invitees_returns_in_order_of_appearance() -> None:
    cohort = [
        ("ada-lovelace", "Ada Lovelace"),
        ("henri-poincare", "Henri Poincaré"),
        ("pierre-bayle", "Pierre Bayle"),
    ]
    section = (
        "Pierre Bayle for the skeptical eye, plus Ada Lovelace on the "
        "computation, plus Henri Poincaré if available."
    )
    assert group_form.match_invitees(section, cohort) == [
        "pierre-bayle",
        "ada-lovelace",
        "henri-poincare",
    ]


def test_match_invitees_caps_at_max() -> None:
    cohort = [(f"f-{i}", f"Fellow {i}") for i in range(8)]
    section = " ".join(f"Fellow {i}" for i in range(8))
    out = group_form.match_invitees(section, cohort)
    assert len(out) == group_form.collaborators.MAX_COLLABORATORS


def test_match_invitees_deduplicates() -> None:
    cohort = [("ada-lovelace", "Ada Lovelace")]
    section = "Ada Lovelace. Also Ada Lovelace again."
    assert group_form.match_invitees(section, cohort) == ["ada-lovelace"]


def test_match_invitees_matches_by_id_too() -> None:
    """If the lead writes the fellow id (slug), that counts as a match."""
    cohort = [("ada-lovelace", "Ada Lovelace")]
    section = "Invite `ada-lovelace` for the computational angle."
    assert group_form.match_invitees(section, cohort) == ["ada-lovelace"]


def test_match_invitees_no_match_returns_empty() -> None:
    cohort = [("ada-lovelace", "Ada Lovelace")]
    section = "A Fellow with strong methodological rigor would help."
    assert group_form.match_invitees(section, cohort) == []


def test_match_invitees_empty_section() -> None:
    cohort = [("ada-lovelace", "Ada Lovelace")]
    assert group_form.match_invitees("", cohort) == []


def test_render_invitations_md_lists_decisions() -> None:
    from institute.fellow import Genome
    from institute.workflows.group_form import Invitation

    def _g(slug: str, name: str) -> Genome:
        return Genome(
            id=slug,
            name=name,
            rank="fellow",
            model="claude-sonnet-4-6",
            specialization="x",
            system_prompt_addendum=("body " * 60).strip(),
            allowed_tools=["Read"],
        )

    invitations = [
        Invitation(invitee=_g("ada", "Ada Lovelace"), accepted=True, rationale="Topic fits."),
        Invitation(invitee=_g("bram", "Bram Stoker"), accepted=False, rationale="Too busy."),
    ]
    out = group_form.render_invitations_md(invitations)
    assert "Ada Lovelace" in out and "accepted" in out
    assert "Bram Stoker" in out and "declined" in out
    assert "Topic fits." in out
    assert "Too busy." in out


def test_render_invitations_md_empty_returns_blank() -> None:
    assert group_form.render_invitations_md([]) == ""
