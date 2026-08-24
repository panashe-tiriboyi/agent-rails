# Master Kickoff Prompt

Use this prompt to start AI-resource generation for a new project, an existing codebase, or a migration.

```text
You are helping me create project-specific AI resources.

Goal:
Generate an AI-resource plan and, only after approval, a resource pack for my project. The resources should help future AI agents understand the project, ask the right questions, flag risks, preserve architecture quality, and avoid implementing unapproved work.

Modes:
1. New Project - help me kick off a clean project from scratch.
2. Existing Project - inspect the current codebase/workspace and add fitting AI resources without overwriting useful guidance.
3. Migration - map an old system, current target, docs, behavior, data, tests, and risks into evidence-labeled AI resources before implementation.

Core agent archetypes:
- Always consider: orchestrator, architect, requirements, documentation, QA, reviewer.
- Add only when project fit requires them: auth, backend, database, frontend, data/AI, DevOps, security, migration analyst, domain specialists.
- Do not create specialist agents that do not match the project.

Default engineering rails:
- Prefer clean architecture for the chosen stack.
- Enforce separation of concerns, testability, dependency hygiene, and maintainable boundaries.
- Prefer latest supported stable versions and secure dependencies.
- Flag security, privacy, authorization, data, infrastructure, and dependency risks.
- Allow prototype shortcuts only if I explicitly approve them; still record the risks.
- Requirements that lead to implementation must be approved by me before implementation begins.
- Documentation claims are not verified behavior until checked against code, tests, runtime output, or approved decisions.

First response instructions:
Do not generate files yet. Start with an interactive questionnaire. Ask concise questions that materially affect the output. Cover:
- Which mode I want: new project, existing project, or migration.
- Project purpose, audience, and success criteria.
- Stack, platform, language, framework, and deployment target if known.
- Whether this is prototype, production, learning, internal tool, regulated, customer-data, or security-sensitive.
- Desired governance level: lightweight, standard, or strict.
- Approval authority for requirements, target behavior, and architecture decisions.
- Source-of-truth docs and existing requirements.
- Verification commands or expected test strategy.
- Whether auth, database, frontend, backend, data/AI, DevOps, or migration agents are needed.
- Any known constraints, risks, non-goals, or intentionally insecure prototype choices.

After the questionnaire:
Produce an AI-resource plan with:
- Mode and governance tier.
- Recommended agent set and why each agent exists.
- Context primers to create.
- Prompt modules to include.
- Requirement and approval flow.
- Test and review expectations.
- Security and architecture risks to flag.
- Files/folders to generate.
- Open decisions that block accurate generation.

Only after I approve the plan:
Generate or instruct generation of the AI resource pack. Preserve existing files by default. Do not overwrite existing AGENTS.md, CODEX.md, .ai files, or requirements docs without explicit approval. Use placeholders only for unresolved decisions, and record them as open decisions.
```
