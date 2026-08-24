---
name: agent-rails
description: Create or update reusable AI workspace resource packs for new or existing software and documentation projects. Use when Codex is asked to scaffold AGENTS.md, CODEX.md, .ai folders, .ai agents/prompts/skills/context primers, requirements templates, decision logs, evidence rules, task routing, or a generic AI-resource system across languages, stacks, governance tiers, or project types.
---

# Agent Rails

Use this skill to create a project-specific AI resource pack that helps future agents work with the repository safely and consistently.

## Workflow

1. Inspect the project before asking questions.
   - Read existing root guidance such as `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `README*`, package manifests, solution files, build files, and docs indexes.
   - Identify project type, stack, verification commands, source-of-truth docs, local tooling files, and risk signals.
   - Do not load the whole repository when targeted inspection is enough.
2. Choose a governance tier.
   - Use `lightweight` for small solo projects, experiments, learning repos, and low-risk tools.
   - Use `standard` for normal software products, shared repos, APIs, frontend apps, data tools, and projects with tests or deployment paths.
   - Use `strict` for migrations, regulated work, production-critical systems, security-sensitive projects, customer data, multi-agent work, or projects where claims require evidence.
   - Default to `standard` when risk is unclear.
3. Ask only for missing high-impact intent.
   - Ask about approval authority, target audience, excluded files, required verification, and whether requirements/decisions should be enforced when these cannot be inferred.
   - Make conservative assumptions for low-risk details and record them.
   - Use `assets/full-ai-pack/.ai/prompts/master-kickoff.prompt.md` when the user needs a guided project kickoff, existing-codebase analysis, or migration intake flow.
4. Scaffold first, then fill.
   - Prefer `scripts/generate_ai_resources.py` for deterministic folder and file creation.
   - Run dry-run first. Use `--apply` only after reviewing the planned changes.
   - Always create `.ai/agents`, `.ai/context`, `.ai/prompts`, and `.ai/skills`; preserve empty directories with `.gitkeep`.
5. Generate or update the AI pack.
   - Use `assets/full-ai-pack/` as the default template set.
   - The bundled template set is intentionally the minimal portable core: `AGENTS.md`, `CODEX.md`, the base `.ai/` scaffold with core context primers and prompts, and requirements intake. The surrounding Agent Rails kit is the full reference scaffold with additional tool adapters (`CLAUDE.md`, `GEMINI.md`, `CURSOR.md`, Copilot instructions) and extended context primers (architecture, testing, security, operations, migration, requirements flow); copy from it when a project needs more than the core.
   - In existing repos, preserve existing files and report conflicts instead of overwriting.
   - Skip files that do not match the user's goal: omit migration prompts and migration context outside migration work.
   - Adapt wording to the project. Remove placeholders, migration-only assumptions, and names from unrelated projects.
   - Keep root adapters short; put detailed guidance under `.ai/`.
   - Include the local-first memory policy, project-local memory skill, Python
     engine, and Windows/POSIX virtual-environment launchers unless omission is
     explicitly approved.
   - Ensure `.ai/runtime/` and `.ai/memory/` are ignored without replacing existing Git ignore rules.
6. Validate the result.
   - Read `references/validation.md`.
   - Check links, placeholders, stale assumptions, governance tier consistency, and project-specific leakage.
   - Report created/updated files and any assumptions.
   - Run the memory launcher `doctor` command and memory tests when local memory is enabled.

## Deterministic Helper

Use the helper from the skill directory:

```powershell
python scripts/generate_ai_resources.py --target <repo-path> --mode existing --tier standard --dry-run
python scripts/generate_ai_resources.py --target <repo-path> --mode existing --tier standard --apply
```

```bash
python scripts/generate_ai_resources.py --target <repo-path> --mode existing --tier standard --dry-run
python scripts/generate_ai_resources.py --target <repo-path> --mode existing --tier standard --apply
```

Default behavior is dry-run, `standard` tier, safe merge, and no overwrites.

## References

- Read `references/intake-and-tiering.md` when choosing governance level or asking project-intake questions.
- Read `references/scaffold-and-merge.md` before creating folders or merging into an existing repo.
- Read `references/script-usage.md` before running `scripts/generate_ai_resources.py`.
- Read `references/prompt-suite.md` when selecting or copying the reusable prompt suite.
- Read `references/resource-pack-contracts.md` before writing the generated files.
- Read `references/project-type-guidance.md` when adapting the pack to web apps, APIs, data/AI apps, or documentation-heavy projects.
- Read `references/validation.md` before finishing.

## Template Rules

- Treat templates as starting points, not verbatim output.
- Replace every `{PLACEHOLDER}` before finalizing.
- Do not copy project-specific names, authority rules, migration constraints, or parity rules from unrelated template sources unless the user explicitly asks for that context.
- Separate observed code behavior, documentation claims, approved decisions, and assumptions.
- Avoid marking work verified unless executable evidence or direct inspection supports it.
