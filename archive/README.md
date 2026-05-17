# Archive

The committed institutional memory of the College. Everything that the Fellows
produce in the course of doing research ends up here.

## Layout

```
archive/
├── proposals/<project-id>/
│   ├── proposal.md
│   └── disposition.md       reviewer's decision on the proposal
├── lab-notebooks/<project-id>/
│   ├── notebook.md          append-only research log
│   └── entries/             individual session entries if split
├── reviews/<project-id>/
│   ├── review-by-<reviewer>.md
│   └── editorial-decision.md
├── drafts/<project-id>/
│   ├── draft-v1.md
│   └── ...
└── publications/<slug>.md   the final accepted version
```

Everything in this directory is committed. It is the public record of how
each piece of work came to exist. Nothing here is ever deleted; corrections
are made by adding new entries that reference the old ones.

The blog reads from `publications/`, `lab-notebooks/`, and `reviews/` at
publication time and builds them into Astro content collections.
