# Project Agent Primer

This repository uses portable AI resources to help agents understand the project, route work, capture requirements, and verify claims before implementation.

Current state: not yet project-specific. Fill `.ai/context/project-map.md` after the target project is known.

## Start Here

1. Read `.ai/instructions.md`.
2. Use `.ai/task-routing.md` to select one primary specialist.
3. Follow `.ai/context-loading-rules.md`; do not load the whole repository unless the task requires it.
4. Load only the selected route, relevant skill, and up to three detailed context files initially.

## Routing

Route work through `.ai/task-routing.md`. Choose one primary specialist first, then add supporting specialists only when the project actually crosses those boundaries.

Default specialist archetypes:

- `orchestrator`
- `architect`
- `requirements`
- `documentation`
- `qa`
- `reviewer`

Optional archetypes include `auth`, `backend`, `database`, `frontend`, `data-ai`, `devops`, `security`, `migration-analyst`, and project-specific domain specialists.

## New Requirements Instructions

Route new behavior, architecture, workflow, data, security, deployment, or product changes through `docs/requirements/change-request-template.md`.

Draft requirements capture intent; they do not authorize implementation. Approved requirements must identify the decision owner, acceptance criteria, and verification expectations.

## Approval Rules

- User approval is required before implementation work begins for any non-trivial requirement.
- User approval is required before weakening security, skipping tests, changing target architecture, accepting migration differences, or replacing existing project guidance.
- Documentation approval is not verification.
- Prototype shortcuts are allowed only when explicitly approved and recorded as risks.

## Evidence Rules

- Separate current code behavior, runtime behavior, test evidence, documentation claims, approved decisions, assumptions, and external sources.
- Use the labels in `.ai/context/evidence-rules.md`.
- Cite file paths and verification dates for durable claims.
- Do not mark work verified unless current code, tests, runtime output, or approved decisions support it.

## Repository Map

Fill `.ai/context/project-map.md` after project inspection.

Initial placeholder:

- Code: not mapped yet.
- Tests: not mapped yet.
- Documentation: not mapped yet.
- Deployment: not mapped yet.
- Local tooling exclusions: not mapped yet.

## Canonical AI Resources

- `.ai/instructions.md` owns operating rules.
- `.ai/task-routing.md` owns routing.
- `.ai/context-loading-rules.md` owns context-loading limits.
- `.ai/context/` owns durable project context.
- `.ai/prompts/` owns reusable prompts.
- `.ai/agents/` owns project-specific specialist definitions.
- `.ai/skills/` owns project-local skills.
- `docs/requirements/` owns request intake and approval records.

## Non-Negotiable Guardrails

- Do not infer completeness from existing code, generated docs, old status labels, or passing tests alone.
- Do not invent business rules, security rules, approval authority, or architecture decisions.
- Do not weaken authentication, authorization, data protection, or dependency safety without explicit approval.
- Preserve existing user work and existing guidance unless replacement is explicitly approved.
- Treat archives and generated output as historical or provisional unless promoted by an approved decision.
- Do not commit secrets, credentials, private keys, tokens, or raw private data.
- Keep local tooling state out of project knowledge unless `.ai/context/project-map.md` explicitly promotes it.
