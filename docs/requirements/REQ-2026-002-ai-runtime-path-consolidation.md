---
id: REQ-2026-002
title: Consolidate Agent Rails runtime under .ai
status: done
type: change
requested_by: project maintainer
decision_owner: project maintainer
approved_by: project maintainer
approved_on: 2026-08-24
created: 2026-08-24
updated: 2026-08-24
affected_areas: [memory, python-runtime, generator, documentation, distribution]
---

# REQ-2026-002 - Consolidate Agent Rails runtime under .ai

## Request

Remove the confusing `.agent-rails/` runtime root. Store private memory at
`.ai/memory/` and the isolated Python environment at `.ai/runtime/venv/`, and
update all generated resources so the old path is never recreated.

## Business Reason

Keep all Agent Rails resources under the canonical `.ai/` hierarchy while
preserving the separation between tracked guidance and ignored local state.

## Current Evidence

Status: `Confirmed`

Claim type: `Current code behavior`

Claim: The initial memory implementation used `.agent-rails/memory/` and
`.agent-rails/runtime/venv/`.

Sources: `REQ-2026-001`, memory engine, launchers, and generated templates

Last verified: 2026-08-24

## Desired Outcome

All runtime paths, generated ignore rules, memory indicators, tests, and
documentation use `.ai/memory/` and `.ai/runtime/venv/` exclusively.

## Acceptance Criteria

- [x] Existing Markdown and SQLite memory is preserved under `.ai/memory/`.
- [x] The virtual environment is recreated under `.ai/runtime/venv/`.
- [x] The obsolete runtime directory no longer exists and no active resource uses it.
- [x] The generator safely migrates the obsolete ignore rule and merges the two new rules.
- [x] Generated packs, canonical skill source, and ZIP use the new paths.
- [x] Full verification passes from the recreated environment.

## Out Of Scope

Changing the memory schema, ranking behavior, retention policy, or platform fallback rules.

## Dependencies And Open Decisions

None. The project maintainer explicitly selected the `.ai/` layout.

## Verification Plan

Reindex migrated Markdown, run `doctor`, search the migrated record, run the
full standard-library suite, scan tracked resources for obsolete path strings,
and verify the deterministic ZIP.

## Change History

| Date | Author | Change |
|---|---|---|
| 2026-08-24 | project maintainer | Approved `.ai/` runtime consolidation |
| 2026-08-24 | Codex | Migrated runtime and memory; verified with 17 passing tests |
