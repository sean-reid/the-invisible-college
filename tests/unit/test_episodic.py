"""Tests for episodic memory: schema, ingest, retrieve, render.

These tests use the HashBackend so no network or model download is
required at test time.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, episodic
from institute import fellow as fellow_mod
from institute.episodic import HashBackend
from institute.fellow import Genome


@pytest.fixture(autouse=True)
def _mock_backend() -> None:
    """Every test in this file uses the deterministic hash backend."""
    episodic.set_backend(HashBackend())


def _seed_fellow(conn, fellow_id: str = "ada") -> None:
    g = Genome(
        id=fellow_id,
        name=fellow_id.capitalize(),
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="anything",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


def test_episodic_memory_table_exists(isolated: Path) -> None:
    with db.connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(episodic_memory)")}
    assert {"fellow_id", "kind", "title", "content", "embedding", "created_at"} <= cols


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


def test_ingest_stores_entry_with_embedding(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        rid = episodic.ingest(
            conn,
            fellow_id="ada",
            kind="proposal",
            title="Test proposal",
            content="The proposal discusses floating-point reproducibility.",
            project_id="proj-1",
        )
    assert rid > 0
    with db.connection() as conn:
        row = conn.execute(
            "SELECT title, kind, project_id, embedding FROM episodic_memory WHERE id = ?",
            (rid,),
        ).fetchone()
    assert row["title"] == "Test proposal"
    assert row["kind"] == "proposal"
    assert row["project_id"] == "proj-1"
    # Embedding is stored as BLOB of float32; expect 384 floats = 1536 bytes.
    assert len(row["embedding"]) == 4 * episodic.EMBEDDING_DIM


def test_ingest_accepts_research_group_kinds(isolated: Path) -> None:
    """Chapter 6 added `contribution` and `publication` kinds for the
    multi-author flow. Guard against another silent drop like the one
    that nuked per-author publication memory the first time around."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
    for kind in ("contribution", "publication"):
        with db.connection() as conn, db.transaction(conn):
            episodic.ingest(
                conn,
                fellow_id="ada",
                kind=kind,
                title=f"a {kind}",
                content="body of the entry",
            )
        with db.connection() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM episodic_memory WHERE kind = ?", (kind,)
            ).fetchone()[0]
        assert count == 1, f"kind={kind!r} did not persist"


def test_ingest_rejects_unknown_kind(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        with pytest.raises(ValueError, match="Unknown episodic memory kind"):
            episodic.ingest(
                conn,
                fellow_id="ada",
                kind="not_a_real_kind",
                title="x",
                content="x",
            )


def test_ingest_rejects_empty_content(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        with pytest.raises(ValueError, match="empty"):
            episodic.ingest(
                conn,
                fellow_id="ada",
                kind="proposal",
                title="x",
                content="   ",
            )


# ---------------------------------------------------------------------------
# Retrieve
# ---------------------------------------------------------------------------


def test_retrieve_returns_most_similar_first(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        episodic.ingest(
            conn,
            fellow_id="ada",
            kind="proposal",
            title="floating point reproducibility",
            content="A study on floating-point non-associativity and reproducibility in modern hardware.",
        )
        episodic.ingest(
            conn,
            fellow_id="ada",
            kind="proposal",
            title="ancient philosophy of mind",
            content="An essay on Aristotle's De Anima and the soul.",
        )
    with db.connection() as conn:
        results = episodic.retrieve(
            conn,
            fellow_id="ada",
            query="floating point non-associativity",
            top_k=2,
        )
    assert len(results) == 2
    assert results[0].title == "floating point reproducibility"


def test_retrieve_respects_kinds_filter(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        episodic.ingest(
            conn, fellow_id="ada", kind="proposal", title="a proposal", content="study X"
        )
        episodic.ingest(
            conn,
            fellow_id="ada",
            kind="review_given",
            title="a review",
            content="review of study X",
        )
    with db.connection() as conn:
        results = episodic.retrieve(conn, fellow_id="ada", query="study X", kinds=["review_given"])
    assert len(results) == 1
    assert results[0].kind == "review_given"


def test_retrieve_excludes_project_id(isolated: Path) -> None:
    """Workspaces stage memory without echoing the current project's own entries."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
        episodic.ingest(
            conn,
            fellow_id="ada",
            kind="draft",
            title="current draft",
            content="X X X",
            project_id="proj-current",
        )
        episodic.ingest(
            conn,
            fellow_id="ada",
            kind="draft",
            title="older draft",
            content="X X X",
            project_id="proj-older",
        )
    with db.connection() as conn:
        results = episodic.retrieve(
            conn, fellow_id="ada", query="X X X", exclude_project_id="proj-current"
        )
    assert {r.title for r in results} == {"older draft"}


def test_retrieve_isolated_per_fellow(isolated: Path) -> None:
    """A Fellow's memory must not leak to another Fellow."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada")
        _seed_fellow(conn, "bram")
        episodic.ingest(
            conn, fellow_id="ada", kind="proposal", title="ada's piece", content="content A"
        )
        episodic.ingest(
            conn, fellow_id="bram", kind="proposal", title="bram's piece", content="content B"
        )
    with db.connection() as conn:
        for_ada = episodic.retrieve(conn, fellow_id="ada", query="content")
        for_bram = episodic.retrieve(conn, fellow_id="bram", query="content")
    assert {e.title for e in for_ada} == {"ada's piece"}
    assert {e.title for e in for_bram} == {"bram's piece"}


def test_retrieve_empty_when_no_entries(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn)
    with db.connection() as conn:
        results = episodic.retrieve(conn, fellow_id="ada", query="anything")
    assert results == []


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def test_render_context_handles_empty_list() -> None:
    out = episodic.render_context([])
    assert "Nothing in your episodic memory" in out


def test_render_context_includes_entries() -> None:
    entries = [
        episodic.MemoryEntry(
            id=1,
            fellow_id="ada",
            kind="proposal",
            title="Floating point study",
            content="Body of the proposal goes here.",
            source_path="archive/proposals/proj-1/proposal.md",
            project_id="proj-1",
            metadata={},
            created_at="2026-05-18T00:00:00+00:00",
            embedding=None,  # type: ignore[arg-type]
        ),
    ]
    out = episodic.render_context(entries, fellow_name="Ada Lovelace")
    assert "Your memory: Ada Lovelace" in out
    assert "Floating point study" in out
    assert "proposal" in out
    assert "Body of the proposal goes here." in out


def test_render_context_truncates_very_long_entries() -> None:
    long_content = "x " * 5000  # 10k chars
    entries = [
        episodic.MemoryEntry(
            id=1,
            fellow_id="ada",
            kind="draft",
            title="A long draft",
            content=long_content,
            source_path=None,
            project_id=None,
            metadata={},
            created_at="2026-05-18T00:00:00+00:00",
            embedding=None,  # type: ignore[arg-type]
        ),
    ]
    out = episodic.render_context(entries)
    assert "(truncated" in out


# ---------------------------------------------------------------------------
# HashBackend properties (sanity)
# ---------------------------------------------------------------------------


def test_hash_backend_returns_normalized_vectors() -> None:
    import numpy as np

    backend = HashBackend()
    vecs = backend.embed(["hello world", "another phrase"])
    assert vecs.shape == (2, episodic.EMBEDDING_DIM)
    norms = np.linalg.norm(vecs, axis=1)
    assert all(abs(n - 1.0) < 1e-5 for n in norms)


def test_hash_backend_is_deterministic() -> None:
    a = HashBackend().embed(["one"])
    b = HashBackend().embed(["one"])
    import numpy as np

    assert np.allclose(a, b)
