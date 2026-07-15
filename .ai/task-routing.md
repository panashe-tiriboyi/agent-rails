# Task Routing

Select one primary specialist before loading detailed context. Add supporting specialists only when the request crosses a real boundary.

## Route Decision

```text
Task summary:
Primary specialist:
Supporting specialist(s):
Skills or prompts:
Required context:
Optional context:
Migration inspection required:
Blocking questions:
Expected output:
```

## Default Specialists

| Task signal | Primary specialist | Typical support |
|---|---|---|
| Ambiguous, cross-cutting, sequencing, or scope triage | `orchestrator` | affected specialist |
| Architecture, boundaries, dependency direction, major refactor | `architect` | backend, frontend, data, security |
| New feature/change/defect request intake | `requirements` | documentation |
| Canonical docs, context, adapters, decisions, indexes | `documentation` | reviewer |
| Tests, verification strategy, reproducibility, evidence | `qa` | affected specialist |
| Independent correctness, security, architecture, or docs review | `reviewer` | affected specialist |

## Optional Specialists

| Task signal | Specialist |
|---|---|
| Authentication, authorization, identity, permissions | `auth` |
| Server APIs, services, jobs, integrations | `backend` |
| Database schema, migrations, queries, persistence | `database` |
| UI, routing, components, client state, accessibility | `frontend` |
| Models, agents, prompts, evals, datasets, pipelines | `data-ai` |
| CI/CD, environments, deployment, infrastructure, operations | `devops` |
| Threats, secrets, privacy, vulnerability, compliance | `security` |
| Old-system mapping, parity, target migration plan | `migration-analyst` |

## Rules

- Do not create specialists that do not fit the project.
- Requirement intake stops at draft unless approval is explicit.
- Approved implementation routes to the owning specialist.
- Migration work must separate old observed behavior, target behavior, documentation claims, assumptions, and approved decisions.
