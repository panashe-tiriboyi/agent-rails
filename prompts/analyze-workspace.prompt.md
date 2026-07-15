# Analyze Workspace Prompt

Use this prompt when adding AI resources to an existing repo or checking whether a new repo has enough context.

```text
Analyze this workspace for AI-resource generation.

Do not modify files. Inspect targeted project files first: root guidance, README files, package manifests, solution/project files, build/test configs, docs indexes, CI files, deployment files, and existing .ai resources.

Return:
- Project purpose inferred from evidence.
- Stack, framework, runtime, package manager, and deployment signals.
- Existing architecture shape and likely clean-architecture boundaries.
- Existing tests and verification commands.
- Security, auth, database, frontend, backend, data/AI, DevOps, and migration signals.
- Existing docs or requirements that should become source-of-truth context.
- Conflicts, stale claims, missing files, and risky assumptions.
- Recommended governance tier: lightweight, standard, or strict.
- Recommended agent archetypes and context primers to generate.

Use evidence labels:
- Confirmed
- Likely
- Unclear
- Missing
- Contradiction

Do not infer completeness from existing code or docs. Documentation is a claim until checked.
```
