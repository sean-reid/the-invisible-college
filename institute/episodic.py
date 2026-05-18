"""Episodic memory: per-Fellow long-term store with vector retrieval.

Chapter 3 of the design specifies three memory tiers:

  1. Working memory (the active context window; not persistent)
  2. Episodic memory: per-Fellow long-term store with vector retrieval
  3. The Archive: shared institutional artifacts

This module owns tier 2. Each Fellow's prior work — curriculum
responses, proposals, drafts, lab notes, peer reviews (given and
received), advisor feedback — is embedded and stored. When the Fellow
is invoked, the orchestrator retrieves the top-K most semantically
relevant entries and stages them into the workspace as `memory.md`.

This is the closest approximation of "what they learned" reachable
without fine-tuning. The Fellow does not remember from one session to
the next, but their own past writings are present in every workspace,
retrieved by relevance to the current task.

# Backend choice

Embeddings are computed by a lightweight ONNX model via `fastembed`
(BAAI/bge-small-en-v1.5, 384-dim). No network at runtime once the
model is cached locally. The backend is pluggable via the
`EmbeddingBackend` protocol so tests can inject a deterministic mock.
"""

from __future__ import annotations

import json
import sqlite3
import struct
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Protocol

import numpy as np

# Embedding dimension produced by BAAI/bge-small-en-v1.5.
EMBEDDING_DIM = 384


class EmbeddingBackend(Protocol):
    """Anything that can turn a list of strings into float32 vectors.

    Implementations:
      - FastembedBackend: production, uses BAAI/bge-small-en-v1.5 via ONNX.
      - HashBackend: deterministic stub for tests (no network, no model file).
    """

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Return an (N, D) float32 matrix, L2-normalized rows."""
        ...


# ---------------------------------------------------------------------------
# Backends
# ---------------------------------------------------------------------------


class FastembedBackend:
    """Production backend: BAAI/bge-small-en-v1.5 via fastembed."""

    def __init__(self) -> None:
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        vectors = list(self._model.embed(list(texts)))
        if not vectors:
            return np.zeros((0, EMBEDDING_DIM), dtype=np.float32)
        matrix = np.vstack(vectors).astype(np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return matrix / norms


class HashBackend:
    """Deterministic hash-based pseudo-embedding for tests.

    Not semantically meaningful — overlapping content tokens produce
    similar vectors, which is good enough to exercise the retrieval
    plumbing without pulling a real model.
    """

    def __init__(self, dim: int = EMBEDDING_DIM) -> None:
        self.dim = dim

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        vectors = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, text in enumerate(texts):
            tokens = [
                t for t in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if t
            ]
            for tok in tokens:
                idx = (hash(tok) & 0x7FFFFFFF) % self.dim
                vectors[i, idx] += 1.0
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms


# ---------------------------------------------------------------------------
# Active backend (module-level, swappable)
# ---------------------------------------------------------------------------


_active_backend: EmbeddingBackend | None = None


def set_backend(backend: EmbeddingBackend) -> None:
    """Replace the active embedding backend. Tests use this."""
    global _active_backend
    _active_backend = backend


@lru_cache(maxsize=1)
def _default_backend() -> EmbeddingBackend:
    return FastembedBackend()


def active_backend() -> EmbeddingBackend:
    if _active_backend is not None:
        return _active_backend
    return _default_backend()


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------


def _embedding_to_blob(vector: np.ndarray) -> bytes:
    return struct.pack(f"<{vector.size}f", *vector.tolist())


def _blob_to_embedding(blob: bytes) -> np.ndarray:
    count = len(blob) // 4
    return np.array(struct.unpack(f"<{count}f", blob), dtype=np.float32)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MemoryEntry:
    id: int
    fellow_id: str
    kind: str
    title: str
    content: str
    source_path: str | None
    project_id: str | None
    metadata: dict
    created_at: str
    embedding: np.ndarray


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


_INGEST_KINDS = frozenset(
    {
        "curriculum_response",
        "proposal",
        "proposal_review",
        "lab_notebook",
        "draft",
        "revision",
        "review_given",
        "review_received",
        "advisor_feedback_given",
        "advisor_feedback_received",
    }
)


def ingest(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    kind: str,
    title: str,
    content: str,
    source_path: str | None = None,
    project_id: str | None = None,
    metadata: dict | None = None,
) -> int:
    """Embed and store a memory entry. Returns the new row id.

    Caller manages the transaction.
    """
    if kind not in _INGEST_KINDS:
        raise ValueError(f"Unknown episodic memory kind: {kind!r}")
    if not content.strip():
        raise ValueError("Cannot ingest empty content into episodic memory.")

    # Use the title + first chunk of content for embedding context; the
    # embedding model has a finite window and the title carries the most
    # disambiguating signal anyway.
    embed_text = f"{title}\n\n{content[:4000]}"
    matrix = active_backend().embed([embed_text])
    blob = _embedding_to_blob(matrix[0])

    now = datetime.now(UTC).isoformat(timespec="seconds")
    cursor = conn.execute(
        """
        INSERT INTO episodic_memory
            (fellow_id, kind, title, content, source_path, project_id,
             metadata, embedding, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fellow_id,
            kind,
            title,
            content,
            source_path,
            project_id,
            json.dumps(metadata or {}),
            blob,
            now,
        ),
    )
    return int(cursor.lastrowid or 0)


# ---------------------------------------------------------------------------
# Retrieve
# ---------------------------------------------------------------------------


def retrieve(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    query: str,
    top_k: int = 5,
    kinds: Sequence[str] | None = None,
    exclude_project_id: str | None = None,
) -> list[MemoryEntry]:
    """Return the top-K most relevant entries for `query` from this Fellow.

    `kinds` filters by entry kind. `exclude_project_id` drops entries
    tied to a specific in-flight project (so a Fellow drafting project
    X doesn't get their own current-draft echoed back).
    """
    if not query.strip():
        return []

    matrix = active_backend().embed([query])
    query_vec = matrix[0]

    where = ["fellow_id = ?"]
    params: list[object] = [fellow_id]
    if kinds:
        placeholders = ",".join("?" for _ in kinds)
        where.append(f"kind IN ({placeholders})")
        params.extend(kinds)
    if exclude_project_id is not None:
        where.append("(project_id IS NULL OR project_id != ?)")
        params.append(exclude_project_id)

    sql = (
        "SELECT id, fellow_id, kind, title, content, source_path, project_id, "
        "       metadata, embedding, created_at "
        "FROM episodic_memory "
        f"WHERE {' AND '.join(where)}"
    )
    rows = list(conn.execute(sql, params))
    if not rows:
        return []

    scored: list[tuple[float, MemoryEntry]] = []
    for row in rows:
        emb = _blob_to_embedding(row["embedding"])
        # Both vectors are L2-normalized so dot product is cosine sim.
        score = float(np.dot(query_vec, emb))
        entry = MemoryEntry(
            id=int(row["id"]),
            fellow_id=row["fellow_id"],
            kind=row["kind"],
            title=row["title"],
            content=row["content"],
            source_path=row["source_path"],
            project_id=row["project_id"],
            metadata=json.loads(row["metadata"] or "{}"),
            created_at=row["created_at"],
            embedding=emb,
        )
        scored.append((score, entry))

    scored.sort(key=lambda t: -t[0])
    return [entry for _, entry in scored[:top_k]]


# ---------------------------------------------------------------------------
# Rendering for workspace staging
# ---------------------------------------------------------------------------


def render_context(
    entries: Sequence[MemoryEntry],
    fellow_name: str | None = None,
) -> str:
    """Render retrieved entries as a markdown brief for `memory.md`."""
    if not entries:
        return (
            "# Your memory\n\n"
            "Nothing in your episodic memory yet, or nothing relevant to this task.\n"
        )
    header = f"# Your memory: {fellow_name}" if fellow_name else "# Your memory"
    lines = [
        header,
        "",
        "These are pieces of your own past work that the institution thinks",
        "are most relevant to the task in front of you. They were retrieved",
        "by semantic similarity from your episodic memory. Read them as your",
        "own — they are.",
        "",
    ]
    for entry in entries:
        lines.append(f"## {entry.title}  `{entry.kind}`")
        lines.append("")
        meta_bits: list[str] = [f"created {entry.created_at}"]
        if entry.project_id:
            meta_bits.append(f"project `{entry.project_id}`")
        if entry.source_path:
            meta_bits.append(f"source `{entry.source_path}`")
        lines.append(f"_{' · '.join(meta_bits)}_")
        lines.append("")
        excerpt = entry.content.strip()
        if len(excerpt) > 3000:
            excerpt = excerpt[:3000].rstrip() + "\n\n_(truncated; see source path for full text)_"
        lines.append(excerpt)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Inspection helpers
# ---------------------------------------------------------------------------


def list_entries(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    limit: int = 50,
) -> list[dict]:
    """Return entry metadata rows (no embeddings) for the memory CLI."""
    rows = list(
        conn.execute(
            "SELECT id, kind, title, source_path, project_id, created_at "
            "FROM episodic_memory WHERE fellow_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (fellow_id, limit),
        )
    )
    return [dict(r) for r in rows]


def count_entries(conn: sqlite3.Connection, fellow_id: str) -> int:
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM episodic_memory WHERE fellow_id = ?",
        (fellow_id,),
    ).fetchone()
    return int(row["n"]) if row else 0


def write_memory_file(target: Path, content: str) -> None:
    """Atomic write helper for staging memory.md into a workspace."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(target)


def safe_ingest(
    *,
    fellow_id: str,
    kind: str,
    title: str,
    content: str,
    source_path: str | None = None,
    project_id: str | None = None,
    metadata: dict | None = None,
) -> None:
    """Best-effort ingestion wrapper.

    Used by workflows that finish producing an artifact. A failure here
    (missing model, network hiccup on first download, embedding crash)
    should never block the workflow from completing — the artifact is
    already on disk and in the Archive. We just won't have it in
    episodic memory.

    Opens its own short transaction so callers don't need to.
    """
    # Local import to avoid module-level cycle with db.
    from institute import db as _db

    try:
        with _db.connection() as conn, _db.transaction(conn):
            ingest(
                conn,
                fellow_id=fellow_id,
                kind=kind,
                title=title,
                content=content,
                source_path=source_path,
                project_id=project_id,
                metadata=metadata,
            )
    except Exception as exc:  # pragma: no cover - best-effort path
        from rich.console import Console

        Console().print(
            f"[yellow]Episodic memory ingest failed for {fellow_id}/{kind}: "
            f"{exc}. Artifact is still on disk.[/yellow]"
        )


def stage_memory_for(
    workspace: Path,
    *,
    fellow_id: str,
    fellow_name: str | None,
    query: str,
    top_k: int = 5,
    kinds: Sequence[str] | None = None,
    exclude_project_id: str | None = None,
) -> Path | None:
    """Retrieve top-K relevant memory for `query` and write memory.md.

    Returns the path that was written, or None on failure (best-effort).
    """
    from institute import db as _db

    try:
        with _db.connection() as conn:
            entries = retrieve(
                conn,
                fellow_id=fellow_id,
                query=query,
                top_k=top_k,
                kinds=kinds,
                exclude_project_id=exclude_project_id,
            )
        target = workspace / "memory.md"
        write_memory_file(target, render_context(entries, fellow_name))
        return target
    except Exception as exc:  # pragma: no cover - best-effort path
        from rich.console import Console

        Console().print(
            f"[yellow]Episodic memory retrieval failed for {fellow_id}: {exc}. "
            "Workspace will not have memory.md.[/yellow]"
        )
        return None
