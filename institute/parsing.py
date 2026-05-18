"""Shared helpers for extracting structured output from Claude responses.

Headless Claude often wraps its final JSON in a code fence and prefixes it
with prose ("Here is the JSON:", "I have all results. Now I will compose...").
These helpers salvage the JSON regardless.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import json_repair


def extract_json_object(text: str) -> str | None:
    """Find the outermost JSON object in `text`, ignoring surrounding prose.

    Returns the substring from the first `{` to its matching `}`, with
    braces inside string literals correctly ignored. Returns None if no
    object can be found.
    """
    s = text.strip()
    if not s:
        return None
    if s.startswith("```"):
        first_newline = s.find("\n")
        if first_newline != -1:
            s = s[first_newline + 1 :]
        if s.rstrip().endswith("```"):
            s = s.rstrip()[:-3].rstrip()

    start = s.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return s[start : i + 1]
    return None


def parse_json_or_dump(text: str, dump_path: Path, context: str) -> dict[str, Any]:
    """Salvage a JSON object from `text`. On failure, save the raw text to
    `dump_path` and raise with a helpful message.

    Three escalating attempts:
      1. Strict json.loads on the extracted object.
      2. json_repair, which heals common LLM-JSON mistakes (one unescaped
         double-quote inside a string, a trailing comma, smart quotes).
      3. json_repair on the original text without extraction, in case the
         extractor itself trimmed too much.
    """
    extracted = extract_json_object(text)
    if extracted is not None:
        try:
            payload = json.loads(extracted)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass
        try:
            payload = json_repair.loads(extracted)
            if isinstance(payload, dict) and payload:
                return payload
        except Exception:
            pass

    try:
        payload = json_repair.loads(text)
        if isinstance(payload, dict) and payload:
            return payload
    except Exception:
        pass

    # All three attempts failed: save raw and complain.
    dump_path.parent.mkdir(parents=True, exist_ok=True)
    dump_path.write_text(text, encoding="utf-8")
    raise RuntimeError(
        f"{context}: could not parse JSON from the response. "
        f"Raw text saved to {dump_path}. "
        f"First 500 chars: {text[:500]}"
    )
