"""Atomic file writes with cost-redaction guard.

Every workflow that writes a public artifact (anything under
`archive/` or `blog/src/content/`) routes through `atomic_write`. For
text files we run the content through the redactor in
[`redaction`][institute.redaction] before committing the bytes, so
operational telemetry (`run cost: $X`, `1234 input tokens`,
`budget=$10`) can never leak onto the public surface.

Binary files and JSON payloads (genome.json, evaluation.json, vote
records) pass through unchanged because the redactor's regexes target
prose telemetry, not structured fields.

The redaction is silent by design: a Fellow's work is never lost or
held up by a redaction. If something was stripped, the report goes to
the operator-local audit log only.
"""

from __future__ import annotations

import logging
from pathlib import Path

from institute import paths, redaction

_logger = logging.getLogger("institute.safe_io")

_TEXT_SUFFIXES = {".md", ".markdown", ".txt"}
_PUBLIC_TOPS = {"archive", "blog"}


def _is_public_text(path: Path) -> bool:
    if path.suffix.lower() not in _TEXT_SUFFIXES:
        return False
    try:
        rel = path.resolve().relative_to(paths.ROOT.resolve())
    except ValueError:
        return False
    parts = rel.parts
    return bool(parts) and parts[0] in _PUBLIC_TOPS


def atomic_write(path: Path, content: str) -> redaction.RedactionReport:
    """Write `content` to `path` atomically (temp + replace).

    Public-surface text content is run through
    [`redaction.redact`][institute.redaction.redact] first. Returns
    the per-call redaction report (empty for non-public or binary
    paths).
    """
    report = redaction.RedactionReport(total=0, by_pattern={})
    cleaned = content
    if _is_public_text(path):
        cleaned, report = redaction.redact(content)
        if report.total > 0:
            _logger.info(
                "redacted %d cost references from %s: %s",
                report.total,
                path,
                report.by_pattern,
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(cleaned, encoding="utf-8")
    tmp.replace(path)
    return report
