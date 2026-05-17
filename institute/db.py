"""SQLite schema and connection management.

The database is the single source of truth for institutional state. Every
state transition is a transactional write. WAL mode is enabled for crash
safety: a killed process never corrupts state, and a re-run of the same
command resumes from the last committed state.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from institute.paths import DB_PATH as DB_PATH  # re-exported for tests to patch

SCHEMA_VERSION = 2

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS fellows (
    id              TEXT    PRIMARY KEY,
    name            TEXT    NOT NULL UNIQUE,
    rank            TEXT    NOT NULL,
    model           TEXT    NOT NULL,
    specialization  TEXT    NOT NULL,
    genome_path     TEXT    NOT NULL,
    advisor_id      TEXT    REFERENCES fellows(id),
    created_at      TEXT    NOT NULL,
    retired_at      TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id               TEXT     PRIMARY KEY,
    title            TEXT     NOT NULL,
    state            TEXT     NOT NULL,
    lead_fellow_id   TEXT     NOT NULL REFERENCES fellows(id),
    proposal_path    TEXT,
    notebook_path    TEXT,
    draft_path       TEXT,
    publication_slug TEXT     UNIQUE,
    review_round     INTEGER  NOT NULL DEFAULT 1,
    created_at       TEXT     NOT NULL,
    updated_at       TEXT     NOT NULL
);

CREATE TABLE IF NOT EXISTS project_collaborators (
    project_id  TEXT NOT NULL REFERENCES projects(id),
    fellow_id   TEXT NOT NULL REFERENCES fellows(id),
    role        TEXT NOT NULL,
    PRIMARY KEY (project_id, fellow_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id              TEXT    PRIMARY KEY,
    project_id      TEXT    NOT NULL REFERENCES projects(id),
    reviewer_id     TEXT    NOT NULL REFERENCES fellows(id),
    role            TEXT    NOT NULL,
    recommendation  TEXT,
    confidence      TEXT,
    content_path    TEXT    NOT NULL,
    submitted_at    TEXT,
    dissent         INTEGER NOT NULL DEFAULT 0,
    round           INTEGER NOT NULL DEFAULT 1,
    UNIQUE (project_id, reviewer_id, round)
);

CREATE TABLE IF NOT EXISTS sessions (
    fellow_id   TEXT NOT NULL REFERENCES fellows(id),
    project_id  TEXT NOT NULL REFERENCES projects(id),
    step        TEXT NOT NULL,
    session_id  TEXT NOT NULL,
    PRIMARY KEY (fellow_id, project_id, step)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    at         TEXT    NOT NULL,
    actor      TEXT    NOT NULL,
    action     TEXT    NOT NULL,
    project_id TEXT,
    detail     TEXT
);

CREATE TABLE IF NOT EXISTS kill_switch (
    id             INTEGER PRIMARY KEY CHECK (id = 1),
    active         INTEGER NOT NULL DEFAULT 0,
    triggered_at   TEXT,
    triggered_by   TEXT,
    reason         TEXT
);

INSERT OR IGNORE INTO kill_switch (id, active) VALUES (1, 0);

CREATE INDEX IF NOT EXISTS idx_projects_state ON projects(state);
CREATE INDEX IF NOT EXISTS idx_audit_log_at ON audit_log(at);
CREATE INDEX IF NOT EXISTS idx_reviews_project ON reviews(project_id);
"""


def _connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, isolation_level=None, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def initialize(path: Path | None = None) -> None:
    """Create the database file and schema if missing. Idempotent.

    If an older schema is present, runs the appropriate forward migration.
    """
    if path is None:
        path = _current_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = _connect(path)
    try:
        # Detect existing schema version BEFORE applying CREATE IF NOT EXISTS,
        # because that would silently leave old tables in place.
        existing = _detect_schema_version(conn)
        if existing is None:
            # Fresh database.
            conn.executescript(SCHEMA)
            conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        elif existing < SCHEMA_VERSION:
            _run_migrations(conn, existing, SCHEMA_VERSION)
        elif existing > SCHEMA_VERSION:
            raise RuntimeError(
                f"Schema version mismatch: db has {existing}, code expects {SCHEMA_VERSION}."
            )
    finally:
        conn.close()


def _detect_schema_version(conn: sqlite3.Connection) -> int | None:
    """Return the integer schema version on disk, or None if uninitialized."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
    ).fetchone()
    if row is None:
        return None
    row = conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
    return int(row["version"]) if row else None


def _run_migrations(conn: sqlite3.Connection, from_version: int, to_version: int) -> None:
    version = from_version
    while version < to_version:
        if version == 1:
            _migrate_1_to_2(conn)
            version = 2
        else:
            raise RuntimeError(f"No migration path from version {version}.")
    conn.execute("UPDATE schema_version SET version = ?", (to_version,))


def _migrate_1_to_2(conn: sqlite3.Connection) -> None:
    """Add round columns to reviews and projects; relax reviews UNIQUE constraint.

    SQLite cannot DROP a UNIQUE constraint in place, so we re-create the
    reviews table and copy the data.
    """
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.executescript(
            """
            ALTER TABLE projects ADD COLUMN review_round INTEGER NOT NULL DEFAULT 1;

            CREATE TABLE reviews_new (
                id              TEXT    PRIMARY KEY,
                project_id      TEXT    NOT NULL REFERENCES projects(id),
                reviewer_id     TEXT    NOT NULL REFERENCES fellows(id),
                role            TEXT    NOT NULL,
                recommendation  TEXT,
                confidence      TEXT,
                content_path    TEXT    NOT NULL,
                submitted_at    TEXT,
                dissent         INTEGER NOT NULL DEFAULT 0,
                round           INTEGER NOT NULL DEFAULT 1,
                UNIQUE (project_id, reviewer_id, round)
            );

            INSERT INTO reviews_new
                (id, project_id, reviewer_id, role, recommendation, confidence,
                 content_path, submitted_at, dissent, round)
            SELECT
                id, project_id, reviewer_id, role, recommendation, confidence,
                content_path, submitted_at, dissent, 1
            FROM reviews;

            DROP TABLE reviews;
            ALTER TABLE reviews_new RENAME TO reviews;

            CREATE INDEX IF NOT EXISTS idx_reviews_project ON reviews(project_id);
            """
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")


def _current_db_path() -> Path:
    """Read DB_PATH from this module at call time so tests can monkey-patch it."""
    import institute.db as self_module  # late import to access patched attr

    return self_module.DB_PATH


@contextmanager
def connection(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Acquire a database connection. Caller manages transactions explicitly."""
    if path is None:
        path = _current_db_path()
    if not path.exists():
        raise RuntimeError(f"Database not initialized at {path}. Run `institute init` first.")
    conn = _connect(path)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Wrap a block in an explicit transaction with proper rollback on error."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
