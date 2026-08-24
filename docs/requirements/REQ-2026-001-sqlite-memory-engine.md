---
id: REQ-2026-001
title: Agent Rails SQLite Memory Engine
status: done
type: change
requested_by: project maintainer
decision_owner: project maintainer
approved_by: project maintainer
approved_on: 2026-08-24
created: 2026-08-24
updated: 2026-08-24
affected_areas: [ai-guidance, memory, sqlite, python-runtime, distribution]
---

# REQ-2026-001 - Agent Rails SQLite Memory Engine

## Request

Add a dependency-free, repository-local long-term memory system that stores
sanitized Markdown summaries, indexes them with SQLite FTS5, and is invoked
through an automatically created Python 3.11+ virtual environment.

## Business Reason

Provide portable cross-session recall without relying primarily on proprietary
IDE memory, loading entire chat histories, or installing global dependencies.

## Current Evidence

Status: `Confirmed`

Claim type: `Current code behavior`

Claim: The repository has no existing memory runtime, SQLite schema, or test
harness. The distributable skill is currently present only as a ZIP archive.

Sources: `README.md`, `.ai/`, and `skills/agent-rails.zip`

Last verified: 2026-08-24

## Desired Outcome

Agent Rails projects receive a local-first memory CLI, isolated launchers,
human-readable Markdown records, a rebuildable SQLite FTS5 index, safe
retention controls, and visible chat activity indicators.

## Acceptance Criteria

- [x] Windows and POSIX launchers create and reuse a repo-local virtual environment.
- [x] The engine refuses direct execution outside a virtual environment.
- [x] Sanitized structured summaries can be added, searched, reindexed, inspected, and forgotten.
- [x] SQLite FTS5 recall ranks no more than three chunks by default and reports confidence.
- [x] Secret-like content is rejected before persistence.
- [x] Markdown remains sufficient to rebuild the SQLite index.
- [x] Agent guidance requires local SQLite search before platform-native memory.
- [x] Memory reads and writes produce the standard aggregate chat indicator.
- [x] Runtime memory and the virtual environment are excluded from Git.
- [x] The generator and distributable skill contain the memory capability.
- [x] Standard-library tests cover the runtime, launchers, generator, and package.

## Out Of Scope

Platform-specific IDE hooks, background services, embeddings, network model
calls, automatic Python installation, application-level encryption,
cross-repository memory, and cross-machine synchronization.

## Dependencies And Open Decisions

Python 3.11+ with `venv` and an SQLite build that supports FTS5 is required.
Memory is plaintext and relies on OS account and disk protection. Platform-native
memory is allowed only as a disclosed fallback after local recall is unavailable
or below the defined confidence threshold.

## Verification Plan

Run the standard-library unit and integration suite inside a temporary virtual
environment; exercise both launchers; validate generator dry-run/apply behavior;
rebuild the ZIP deterministically; and compare packaged artifacts with canonical
source.

## Change History

| Date | Author | Change |
|---|---|---|
| 2026-08-24 | project maintainer | Approved implementation plan |
| 2026-08-24 | Codex | Implemented and verified with 16 passing tests |
