"""Admissions briefs and the candidate-problem pool."""

from __future__ import annotations

from institute.admissions import problems
from institute.workflows import admit


def test_propose_brief_references_research_agenda() -> None:
    """The orchestrator's candidate-design brief should reference the
    Research Agenda so the new Fellow plausibly moves an institutional
    priority forward, not just fills a backend or specialization slot."""
    assert "research-agenda.md" in admit.PROPOSE_BRIEF


def test_load_problems_returns_all_five() -> None:
    out = problems.load_problems()
    ids = {p.id for p in out}
    assert ids == {
        "01-critique",
        "02-synthesis",
        "03-honesty",
        "04-construction",
        "05-judgment",
    }
    for p in out:
        assert p.text.strip(), f"{p.id} is empty"
        assert p.text.endswith("\n")


def test_load_problems_sorted_by_id() -> None:
    out = problems.load_problems()
    assert [p.id for p in out] == sorted(p.id for p in out)


def test_for_candidate_returns_subset() -> None:
    out = problems.for_candidate("ada")
    assert len(out) == problems.PROBLEMS_PER_CANDIDATE
    # All returned items are real problems.
    pool_ids = {p.id for p in problems.load_problems()}
    for p in out:
        assert p.id in pool_ids


def test_for_candidate_is_deterministic() -> None:
    a = problems.for_candidate("ada")
    b = problems.for_candidate("ada")
    assert [p.id for p in a] == [p.id for p in b]


def test_for_candidate_rotates_across_candidates() -> None:
    # Two different candidate ids should differ in their starting
    # problem most of the time; we just verify they're not identical.
    samples = [problems.for_candidate(f"candidate-{i}") for i in range(10)]
    distinct_starts = {tuple(p.id for p in s) for s in samples}
    assert len(distinct_starts) > 1
