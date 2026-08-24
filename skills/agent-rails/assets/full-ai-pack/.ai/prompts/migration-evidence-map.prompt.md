# Migration Evidence Map Prompt

Use this prompt when the project involves moving from an old system to a new one.

```text
Prepare migration AI resources by mapping old-system evidence to target-project context.

Inputs:
- Old system paths, docs, repos, exports, screenshots, schemas, APIs, workflows, or runbooks.
- Target project paths or desired stack.
- Known migration goals, non-goals, and deadlines.
- Approved differences from old behavior, if any.

Instructions:
- Do targeted inspection. Do not load the entire old system by default.
- Identify old-system workflows, API contracts, data model, auth model, integrations, reports, jobs, and operational behavior.
- Separate observed old behavior, current target behavior, documentation claims, assumptions, and approved decisions.
- Identify parity requirements, intentional changes, unknowns, and risks.
- Recommend migration-specific context primers, prompts, agent archetypes, and test strategy.
- Require approval before implementing target behavior or accepting a parity exception.

Output:
- Old-system map
- Target-system map
- Evidence labels and sources
- Parity or change matrix
- Migration risks
- Tests and verification evidence needed
- Open decisions
- AI-resource files to generate
```
