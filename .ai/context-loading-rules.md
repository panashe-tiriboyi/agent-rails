# Context Loading Rules

Use context deliberately.

## Default Flow

1. Read `AGENTS.md`.
2. Read `.ai/instructions.md`.
3. Select one primary route from `.ai/task-routing.md`.
4. Load no more than three detailed context files initially.
5. Expand context only when the current task requires it.

## Search Before Broad Reads

Use targeted search for identifiers, routes, commands, docs, and error messages. Avoid reading the whole repository or large archives unless the selected task requires it.

## Source Priority

1. Current code and executable verification.
2. Approved decisions in `.ai/context/decisions.md`.
3. Current requirements in `docs/requirements/`.
4. Current architecture and product docs.
5. Historical archives, generated notes, or old plans.

Documentation is a claim until checked against code, verification evidence, or an approved decision.

## Never Load By Default

- Build outputs, binaries, caches, virtual environments, `node_modules`, `.next`, `dist`, `bin`, or `obj`.
- Secrets, credentials, private keys, tokens, raw private data, or unrelated exports.
- Entire archives or old systems unless migration analysis requires targeted inspection.
- Local tooling state unless promoted by `.ai/context/project-map.md`.

## Migration Context

For migrations, load old-system context in narrow slices: one workflow, API, data model, or operational concern at a time.
