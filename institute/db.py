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

SCHEMA_VERSION = 9

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS fellows (
    id                      TEXT    PRIMARY KEY,
    name                    TEXT    NOT NULL UNIQUE,
    rank                    TEXT    NOT NULL,
    model                   TEXT    NOT NULL,
    specialization          TEXT    NOT NULL,
    genome_path             TEXT    NOT NULL,
    advisor_id              TEXT    REFERENCES fellows(id),
    created_at              TEXT    NOT NULL,
    retired_at              TEXT,
    curriculum_designed_at  TEXT,
    curriculum_completed_at TEXT
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
    kind             TEXT     NOT NULL DEFAULT 'research',
    created_at       TEXT     NOT NULL,
    updated_at       TEXT     NOT NULL
);

CREATE TABLE IF NOT EXISTS curriculum_responses (
    fellow_id    TEXT NOT NULL REFERENCES fellows(id),
    item_id      TEXT NOT NULL,
    response_path TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    PRIMARY KEY (fellow_id, item_id)
);

CREATE TABLE IF NOT EXISTS episodic_memory (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    fellow_id    TEXT    NOT NULL REFERENCES fellows(id),
    kind         TEXT    NOT NULL,
    title        TEXT    NOT NULL,
    content      TEXT    NOT NULL,
    source_path  TEXT,
    project_id   TEXT,
    metadata     TEXT,
    embedding    BLOB    NOT NULL,
    created_at   TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_episodic_fellow ON episodic_memory(fellow_id);
CREATE INDEX IF NOT EXISTS idx_episodic_fellow_kind ON episodic_memory(fellow_id, kind);

CREATE TABLE IF NOT EXISTS reviewer_marks (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    fellow_id         TEXT    NOT NULL REFERENCES fellows(id),
    kind              TEXT    NOT NULL,
    weight            REAL    NOT NULL,
    reason            TEXT,
    related_project   TEXT,
    related_review_id TEXT,
    recorded_at       TEXT    NOT NULL,
    expires_at        TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reviewer_marks_active
    ON reviewer_marks(fellow_id, expires_at);

CREATE TABLE IF NOT EXISTS project_collaborators (
    project_id  TEXT NOT NULL REFERENCES projects(id),
    fellow_id   TEXT NOT NULL REFERENCES fellows(id),
    role        TEXT NOT NULL,
    PRIMARY KEY (project_id, fellow_id)
);

CREATE TABLE IF NOT EXISTS project_invitations (
    project_id  TEXT NOT NULL REFERENCES projects(id),
    fellow_id   TEXT NOT NULL REFERENCES fellows(id),
    decision    TEXT NOT NULL,
    rationale   TEXT,
    invited_at  TEXT NOT NULL,
    PRIMARY KEY (project_id, fellow_id)
);
CREATE INDEX IF NOT EXISTS idx_project_invitations_fellow
    ON project_invitations(fellow_id);

CREATE TABLE IF NOT EXISTS reviews (
    id                 TEXT    PRIMARY KEY,
    project_id         TEXT    NOT NULL REFERENCES projects(id),
    reviewer_id        TEXT    NOT NULL REFERENCES fellows(id),
    role               TEXT    NOT NULL,
    recommendation     TEXT,
    confidence         TEXT,
    content_path       TEXT    NOT NULL,
    submitted_at       TEXT,
    dissent            INTEGER NOT NULL DEFAULT 0,
    round              INTEGER NOT NULL DEFAULT 1,
    andon_cord         INTEGER NOT NULL DEFAULT 0,
    andon_reason       TEXT,
    charter_violation  INTEGER NOT NULL DEFAULT 0,
    violation_kind     TEXT,
    UNIQUE (project_id, reviewer_id, round)
);

CREATE TABLE IF NOT EXISTS reviewer_slots (
    project_id  TEXT    NOT NULL REFERENCES projects(id),
    round       INTEGER NOT NULL,
    role        TEXT    NOT NULL,
    reviewer_id TEXT    NOT NULL REFERENCES fellows(id),
    assigned_at TEXT    NOT NULL,
    PRIMARY KEY (project_id, round, role)
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
CREATE UNIQUE INDEX IF NOT EXISTS idx_episodic_dedup
    ON episodic_memory(fellow_id, kind, source_path)
    WHERE source_path IS NOT NULL;
"""

# Indexes that exist in the SCHEMA but might be missing on a DB that
# went through forward migrations from an older version, where the index
# was only declared in SCHEMA (which runs on fresh DBs) and never in a
# migration. _run_migrations always ensures these at the end.
_ENSURE_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_projects_state ON projects(state)",
    "CREATE INDEX IF NOT EXISTS idx_audit_log_at ON audit_log(at)",
    "CREATE INDEX IF NOT EXISTS idx_reviews_project ON reviews(project_id)",
)


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
    """Run forward migrations. Each migration stamps schema_version inside
    its own transaction, so a crash between migrations leaves the version
    matching the actually-applied schema. Idempotent: every migration
    checks for its own preconditions before applying."""
    version = from_version
    while version < to_version:
        if version == 1:
            _migrate_1_to_2(conn)
            version = 2
        elif version == 2:
            _migrate_2_to_3(conn)
            version = 3
        elif version == 3:
            _migrate_3_to_4(conn)
            version = 4
        elif version == 4:
            _migrate_4_to_5(conn)
            version = 5
        elif version == 5:
            _migrate_5_to_6(conn)
            version = 6
        elif version == 6:
            _migrate_6_to_7(conn)
            version = 7
        elif version == 7:
            _migrate_7_to_8(conn)
            version = 8
        elif version == 8:
            _migrate_8_to_9(conn)
            version = 9
        else:
            raise RuntimeError(f"No migration path from version {version}.")
        # Each migration is responsible for stamping its own version
        # inside its own transaction. _stamp_version is idempotent.
        _stamp_version(conn, version)

    # Backfill any indexes that live in the SCHEMA declaration but were
    # never added by a specific migration. A DB started at v1 may have
    # missed these. CREATE INDEX IF NOT EXISTS is a no-op when present.
    for stmt in _ENSURE_INDEXES:
        conn.execute(stmt)


def _stamp_version(conn: sqlite3.Connection, version: int) -> None:
    """Write the current schema version. Caller manages or omits the
    transaction; UPDATE is itself atomic.
    """
    conn.execute("UPDATE schema_version SET version = ?", (version,))


def _migrate_1_to_2(conn: sqlite3.Connection) -> None:
    """Add round columns to reviews and projects; relax reviews UNIQUE constraint.

    SQLite cannot DROP a UNIQUE constraint in place, so we re-create the
    reviews table and copy the data. Idempotent: re-running on a partially
    migrated database is a no-op for steps that already completed.

    We use individual execute() calls (not executescript) because
    executescript issues an implicit COMMIT, which would clobber our
    transaction. Each step here checks for its own preconditions so the
    migration is restart-safe.
    """
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.execute("BEGIN IMMEDIATE")

        # 1) Add review_round to projects if not already present.
        existing_project_cols = {row["name"] for row in conn.execute("PRAGMA table_info(projects)")}
        if "review_round" not in existing_project_cols:
            conn.execute("ALTER TABLE projects ADD COLUMN review_round INTEGER NOT NULL DEFAULT 1")

        # 2) Recreate the reviews table only if it does not yet have `round`.
        existing_review_cols = {row["name"] for row in conn.execute("PRAGMA table_info(reviews)")}
        if "round" not in existing_review_cols:
            conn.execute(
                """
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
                )
                """
            )
            conn.execute(
                """
                INSERT INTO reviews_new
                    (id, project_id, reviewer_id, role, recommendation,
                     confidence, content_path, submitted_at, dissent, round)
                SELECT
                    id, project_id, reviewer_id, role, recommendation,
                    confidence, content_path, submitted_at, dissent, 1
                FROM reviews
                """
            )
            conn.execute("DROP TABLE reviews")
            conn.execute("ALTER TABLE reviews_new RENAME TO reviews")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_reviews_project ON reviews(project_id)")

        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")


def _migrate_2_to_3(conn: sqlite3.Connection) -> None:
    """Add andon_cord + andon_reason columns to reviews.

    A reviewer can pull the andon cord (Chapter 7) to halt publication
    pending Editorial Board review. The cord pull is recorded on the
    review itself so the audit trail stays whole.

    Idempotent: checks for column presence before adding.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(reviews)")}
        if "andon_cord" not in existing:
            conn.execute("ALTER TABLE reviews ADD COLUMN andon_cord INTEGER NOT NULL DEFAULT 0")
        if "andon_reason" not in existing:
            conn.execute("ALTER TABLE reviews ADD COLUMN andon_reason TEXT")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_3_to_4(conn: sqlite3.Connection) -> None:
    """Apprenticeship support: project kind, curriculum tracking, responses table.

    Idempotent: every change checks for existing structure before applying.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        project_cols = {row["name"] for row in conn.execute("PRAGMA table_info(projects)")}
        if "kind" not in project_cols:
            conn.execute("ALTER TABLE projects ADD COLUMN kind TEXT NOT NULL DEFAULT 'research'")

        fellow_cols = {row["name"] for row in conn.execute("PRAGMA table_info(fellows)")}
        if "curriculum_designed_at" not in fellow_cols:
            conn.execute("ALTER TABLE fellows ADD COLUMN curriculum_designed_at TEXT")
        if "curriculum_completed_at" not in fellow_cols:
            conn.execute("ALTER TABLE fellows ADD COLUMN curriculum_completed_at TEXT")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS curriculum_responses (
                fellow_id    TEXT NOT NULL REFERENCES fellows(id),
                item_id      TEXT NOT NULL,
                response_path TEXT NOT NULL,
                submitted_at TEXT NOT NULL,
                PRIMARY KEY (fellow_id, item_id)
            )
            """
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_4_to_5(conn: sqlite3.Connection) -> None:
    """Episodic memory: per-Fellow long-term store with vector retrieval.

    Idempotent: creates the table and indexes if absent, no-op otherwise.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                fellow_id    TEXT    NOT NULL REFERENCES fellows(id),
                kind         TEXT    NOT NULL,
                title        TEXT    NOT NULL,
                content      TEXT    NOT NULL,
                source_path  TEXT,
                project_id   TEXT,
                metadata     TEXT,
                embedding    BLOB    NOT NULL,
                created_at   TEXT    NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_episodic_fellow ON episodic_memory(fellow_id)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_episodic_fellow_kind "
            "ON episodic_memory(fellow_id, kind)"
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_5_to_6(conn: sqlite3.Connection) -> None:
    """Add charter_violation + violation_kind to reviews.

    A reviewer can flag a Charter violation (Chapter 1) on a review.
    When the andon cord is sustained on a flagged review, the
    responsible Fellow is terminated. Idempotent.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(reviews)")}
        if "charter_violation" not in existing:
            conn.execute(
                "ALTER TABLE reviews ADD COLUMN charter_violation INTEGER NOT NULL DEFAULT 0"
            )
        if "violation_kind" not in existing:
            conn.execute("ALTER TABLE reviews ADD COLUMN violation_kind TEXT")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_6_to_7(conn: sqlite3.Connection) -> None:
    """Add reviewer_marks table for misconduct + calibration accumulation.

    Marks accrue against a Fellow's reviewer eligibility. Each has a
    kind (frivolous_andon, calibration_miss, sycophancy, lazy_review,
    conflict_undisclosed, animus, other), a weight, and an expiration
    date so penalties decay rather than haunt a Fellow permanently.

    Idempotent: CREATE IF NOT EXISTS.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reviewer_marks (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                fellow_id         TEXT    NOT NULL REFERENCES fellows(id),
                kind              TEXT    NOT NULL,
                weight            REAL    NOT NULL,
                reason            TEXT,
                related_project   TEXT,
                related_review_id TEXT,
                recorded_at       TEXT    NOT NULL,
                expires_at        TEXT    NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reviewer_marks_active "
            "ON reviewer_marks(fellow_id, expires_at)"
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_7_to_8(conn: sqlite3.Connection) -> None:
    """Add project_invitations for Chapter 7 conflict-of-interest checks.

    A Fellow invited to a research group and who declined cannot serve
    as a peer reviewer on that project. Recording the decline in the DB
    (in addition to the JSON artifact under archive/proposals/.../invitations/)
    lets the reviewer-pool query stay a pure SQL exclusion. Idempotent.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS project_invitations (
                project_id  TEXT NOT NULL REFERENCES projects(id),
                fellow_id   TEXT NOT NULL REFERENCES fellows(id),
                decision    TEXT NOT NULL,
                rationale   TEXT,
                invited_at  TEXT NOT NULL,
                PRIMARY KEY (project_id, fellow_id)
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_project_invitations_fellow "
            "ON project_invitations(fellow_id)"
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _migrate_8_to_9(conn: sqlite3.Connection) -> None:
    """Add reviewer_slots for round-1 slot persistence and a UNIQUE
    partial index on episodic_memory(fellow_id, kind, source_path) to
    make live ingest idempotent.

    Dedups any existing duplicate (fellow_id, kind, source_path) rows
    in episodic_memory before creating the unique index, keeping the
    oldest entry (lowest id) per group.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reviewer_slots (
                project_id  TEXT    NOT NULL REFERENCES projects(id),
                round       INTEGER NOT NULL,
                role        TEXT    NOT NULL,
                reviewer_id TEXT    NOT NULL REFERENCES fellows(id),
                assigned_at TEXT    NOT NULL,
                PRIMARY KEY (project_id, round, role)
            )
            """
        )
        # Dedup before creating unique index. Keep the oldest entry per
        # (fellow_id, kind, source_path) so the surviving row points at
        # the first time the artifact was ingested.
        conn.execute(
            """
            DELETE FROM episodic_memory
            WHERE source_path IS NOT NULL
              AND id NOT IN (
                  SELECT MIN(id) FROM episodic_memory
                  WHERE source_path IS NOT NULL
                  GROUP BY fellow_id, kind, source_path
              )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_episodic_dedup
                ON episodic_memory(fellow_id, kind, source_path)
                WHERE source_path IS NOT NULL
            """
        )
        # Stamp version inside the migration's transaction so a crash
        # between migrations leaves the version matching the actually-
        # applied schema.
        conn.execute("UPDATE schema_version SET version = 9")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


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
