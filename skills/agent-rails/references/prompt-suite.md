# Prompt Suite

Use this reference when a project needs guided prompts in addition to scaffold files.

## Required Prompt Assets

The full AI pack includes these prompt modules under `.ai/prompts/`:

- `master-kickoff.prompt.md`
- `analyze-workspace.prompt.md`
- `plan-ai-resources.prompt.md`
- `test-strategy.prompt.md`
- `review-ai-resources.prompt.md`
- `migration-evidence-map.prompt.md`

Not every project needs every prompt: migration-evidence-map applies to migration work only, and analyze-workspace applies when a repo already exists. Skip prompts that do not match the user's goal.

## When To Use Each Prompt

- Use `master-kickoff.prompt.md` for the first conversation in a new project, an existing-codebase AI-resource setup, or a migration setup.
- Use `analyze-workspace.prompt.md` when the repo exists and the agent needs to infer project shape from files.
- Use `plan-ai-resources.prompt.md` after the questionnaire or analysis to create a file-generation plan.
- Use `test-strategy.prompt.md` when requirements, architecture, security, or migration work needs verification planning.
- Use `review-ai-resources.prompt.md` before relying on generated AI resources.
- Use `migration-evidence-map.prompt.md` when old-system behavior, docs, data, or workflows must be mapped before implementation.

## Prompt Principles

- Ask questions before generating files.
- Require approval before implementation.
- Preserve existing project guidance.
- Default to clean architecture, separation of concerns, tests, dependency hygiene, and security review.
- Adapt agent archetypes to the project instead of always creating every possible specialist.
- Keep migration evidence separate from target decisions.
