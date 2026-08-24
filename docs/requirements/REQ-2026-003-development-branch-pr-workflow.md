---
id: REQ-2026-003
title: Development branch and GitHub pull-request workflow
status: done
type: change
requested_by: project maintainer
decision_owner: project maintainer
approved_by: project maintainer
approved_on: 2026-08-24
created: 2026-08-24
updated: 2026-08-24
affected_areas: [contributing, documentation, github, release-process]
---

# REQ-2026-003 - Development branch and GitHub pull-request workflow

## Request

Move all current uncommitted work off `main` onto a dedicated development
branch, document the open-source contribution and release process, and commit
the complete verified change set for GitHub review.

## Business Reason

Protect `main`, keep release tags tied to reviewed GitHub merges, and make the
expected process explicit for external contributors.

## Current Evidence

Status: `Confirmed`

Claim type: `Runtime behavior`

Claim: The memory-engine change set was uncommitted on `main`, and the repository
did not contain a changelog, contribution guide, or pull-request template.

Sources: Git status and repository file inspection on 2026-08-24

Last verified: 2026-08-24

## Desired Outcome

The work is committed on `dev-panashe`; contributor documentation
requires pull-request review and verification before merging or tagging.

## Acceptance Criteria

- [x] The active branch is `dev-panashe`, not `main`.
- [x] Changelog, contribution guide, and pull-request template document the change and workflow.
- [x] Full tests, package parity, memory diagnostics, and diff checks pass.
- [x] All intended tracked and untracked project changes are committed on the development branch.
- [x] No private memory, virtual-environment, secret, or credential files are staged.

## Out Of Scope

Pushing the branch, opening or merging a pull request, changing GitHub branch
protection settings, and creating a release tag.

## Dependencies And Open Decisions

GitHub remains the authority for required review and merge checks.

## Verification Plan

Run the full standard-library suite, package check, memory doctor, placeholder
scan, `git diff --check`, staged-file review, and ignored-private-state checks.

## Change History

| Date | Author | Change |
|---|---|---|
| 2026-08-24 | project maintainer | Approved branch and pull-request workflow |
| 2026-08-24 | Codex | Documented, verified, and committed complete change set on `dev-panashe` |
