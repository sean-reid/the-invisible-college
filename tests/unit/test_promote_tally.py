"""Vote-tally and promotion-direction predicates for the promote workflow."""

from __future__ import annotations

from institute.workflows import promote

# ---------------------------------------------------------------------------
# _tally
# ---------------------------------------------------------------------------


def test_tally_strict_majority_promotes() -> None:
    votes = [
        {"vote": "senior_fellow"},
        {"vote": "senior_fellow"},
        {"vote": "hold"},
    ]
    assert promote._tally(votes, "fellow") == "senior_fellow"


def test_tally_no_majority_holds() -> None:
    votes = [{"vote": "senior_fellow"}, {"vote": "fellow"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_majority_hold_returns_none() -> None:
    votes = [{"vote": "hold"}, {"vote": "hold"}, {"vote": "senior_fellow"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_majority_equal_to_current_returns_none() -> None:
    # All votes agree, but the agreement is "stay at the current rank".
    votes = [{"vote": "fellow"}, {"vote": "fellow"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_ignores_unknown_votes() -> None:
    votes = [
        {"vote": "garbage"},
        {"vote": "senior_fellow"},
        {"vote": "senior_fellow"},
    ]
    assert promote._tally(votes, "fellow") == "senior_fellow"


def test_tally_empty_returns_none() -> None:
    assert promote._tally([], "fellow") is None


def test_tally_release_majority_returns_release() -> None:
    votes = [{"vote": "release"}, {"vote": "release"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") == "release"


def test_tally_release_minority_loses() -> None:
    votes = [{"vote": "release"}, {"vote": "hold"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") is None


# ---------------------------------------------------------------------------
# _is_promotion
# ---------------------------------------------------------------------------


def test_is_promotion_up_the_ladder() -> None:
    assert promote._is_promotion("fellow", "senior_fellow")
    assert promote._is_promotion("novice", "fellow")
    assert promote._is_promotion("postulant", "emeritus")


def test_is_promotion_down_or_equal() -> None:
    assert not promote._is_promotion("senior_fellow", "fellow")
    assert not promote._is_promotion("fellow", "fellow")
