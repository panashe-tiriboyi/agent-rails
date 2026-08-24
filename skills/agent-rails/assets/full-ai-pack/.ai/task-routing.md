# Task Routing

Select one primary route before loading detailed context.

Historical recall is a pre-route action: use the `agent-rails-memory` skill and
`.ai/context/memory-policy.md` before platform-native memory whenever prior
decisions, fixes, rationale, preferences, or task outcomes may matter.

## Requirements

Use for new behavior, scope changes, acceptance criteria, approvals, or trade-off decisions.

Initial context:

- `docs/requirements/README.md`
- `docs/requirements/change-request-template.md`
- `.ai/context/decisions.md`

## Architecture

Use for system boundaries, major refactors, data flow, service ownership, and integration design.

Initial context:

- `.ai/context/project-map.md`
- `.ai/context/decisions.md`
- architecture docs discovered in the repo

## Frontend

Use for UI, routing, components, client state, accessibility, and browser behavior.

Initial context:

- `.ai/context/project-map.md`
- frontend package/config files
- relevant design or product docs

## Backend

Use for APIs, services, persistence, authorization, jobs, and server-side integrations.

Initial context:

- `.ai/context/project-map.md`
- API contracts or backend entrypoints
- relevant tests

## Data AI

Use for data pipelines, models, prompts, agents, evaluations, notebooks, and dataset handling.

Initial context:

- `.ai/context/project-map.md`
- model/eval/data docs
- privacy or dataset constraints

## Testing

Use for test strategy, failing checks, coverage, reproducibility, and verification evidence.

Initial context:

- `.ai/context/project-map.md`
- test configs
- `.ai/context/known-issues.md`

## DevOps

Use for CI/CD, deployment, infrastructure, environments, secrets handling, and operational runbooks.

Initial context:

- `.ai/context/project-map.md`
- CI/IaC/deployment files
- `.ai/context/decisions.md`

## Documentation

Use for docs structure, primers, evidence records, changelogs, and knowledge capture.

Initial context:

- docs indexes
- `.ai/context/evidence-rules.md`
- `.ai/context/known-issues.md`

## Security

Use for authentication, authorization, secrets, data exposure, dependency risk, and threat-sensitive changes.

Initial context:

- `.ai/context/decisions.md`
- security/auth docs or code
- relevant tests
