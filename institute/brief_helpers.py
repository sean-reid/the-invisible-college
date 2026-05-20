"""Shared fragments used inside Claude prompt briefs."""

# Standard final-output instructions for briefs whose outermost reply must be
# a single JSON object. Concatenate into briefs as plain text; the contained
# braces are doubled to match the surrounding briefs (which were authored
# with `.format()`-style escaping). Concatenate; do not `.format()`.
JSON_OUTPUT_RULES = (
    "Reply with a single JSON object. No prose preface, no summary, no code\n"
    "fence. First character `{{`, last `}}`."
)
