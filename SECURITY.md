# Security policy

## Reporting a vulnerability

Please report security vulnerabilities through GitHub's private
vulnerability reporting feature:

1. Go to the project's Security tab.
2. Click "Report a vulnerability."
3. Describe the issue, the affected paths or commits, and a
   reproduction if you have one.

Reports are visible only to the maintainer. Public issues are not
the right venue for security disclosure.

## What counts as a security issue

The project has a few institutional surfaces where security matters:

- The kill switch and tripwire mechanism (`institute/tripwires.py`,
  `institute/runtime.py`). Anything that lets a Fellow's code path
  bypass the runtime check before invoking the Claude subprocess is
  in scope.
- The append-only audit log (`institute/audit.py`,
  `institute/db.py`). Anything that lets a tampered audit row pass
  `verify_chain` is in scope.
- The Charter file integrity check (`institute/tripwires.py`). Any
  path that lets `docs/01-charter.md` be modified without firing
  the tripwire is in scope.
- The cost-redaction guard (`institute/redaction.py`,
  `institute/safe_io.py`). Any operational telemetry (dollar
  amounts, token counts, per-model pricing) that reaches the
  public `archive/` or `blog/` tree without being redacted is in
  scope.

Out of scope: anything in the published research itself
(`archive/`, `blog/src/content/`). Errors in research are handled
via the corrections page, not the security process.

## Response

The maintainer will acknowledge a report within seven days, and
will keep you informed as the issue is investigated. If the report
is accepted, the fix will land before any public disclosure;
credit will be given in the relevant commit message or correction
record unless the reporter prefers otherwise.
