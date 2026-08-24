# Decisions

Record approved project decisions that future agents must follow.

## Format

```md
## DEC-001 - <title>

Status: Approved
Date: <yyyy-mm-dd>
Owner: <decision authority>
Scope: <scope>
Supersedes: None

Decision:
<decision>

Evidence:
<evidence>
```

## Active Decisions

## DEC-001 - Local-first SQLite memory with isolated Python runtime

Status: Approved
Date: 2026-08-24
Owner: Project maintainer
Scope: Agent Rails runtime, generated resource packs, and supported adapters
Supersedes: None

Decision:
Agent Rails will use a repository-local Markdown and SQLite FTS5 memory store as
the first recall mechanism for historical questions. The dependency-free Python
engine must run through launchers that create and reuse a local Python 3.11+
virtual environment. Platform-native memory is permitted only as a disclosed
fallback when local results are unavailable or have confidence below 0.55.

Evidence:
Approved requirement `docs/requirements/REQ-2026-001-sqlite-memory-engine.md`.

## DEC-002 - Consolidate private runtime state under .ai

Status: Approved
Date: 2026-08-24
Owner: Project maintainer
Scope: Memory storage, Python virtual environment, generator, and distributions
Supersedes: DEC-001 runtime-path locations only

Decision:
Store private memory under `.ai/memory/` and the project virtual environment
under `.ai/runtime/venv/`. Ignore only those local-state subdirectories; keep
the remainder of `.ai/` tracked. The obsolete `.agent-rails/` path must not be
generated or referenced.

Evidence:
Approved requirement `docs/requirements/REQ-2026-002-ai-runtime-path-consolidation.md`.

## DEC-003 - Review-first GitHub integration

Status: Approved
Date: 2026-08-24
Owner: Project maintainer
Scope: Contributions, integration, releases, and tags
Supersedes: None

Decision:
Develop non-trivial changes on focused branches and integrate them into `main`
through GitHub pull requests after required review and checks. Do not create
release tags from unreviewed development branches.

Evidence:
Approved requirement `docs/requirements/REQ-2026-003-development-branch-pr-workflow.md`.
