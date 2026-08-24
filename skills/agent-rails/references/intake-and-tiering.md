# Intake And Tiering

Use this reference to decide how much structure the AI resource pack should add.

## Inspection Signals

Look for:

- Root guidance: `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`.
- Project identity: `README*`, workspace files, package names, solution names, pyproject metadata, docs indexes.
- Stack: package manifests, lockfiles, solution/project files, Dockerfiles, IaC, test configs, CI workflows.
- Risk: auth, payments, customer data, migrations, production deploys, regulated domains, security-sensitive code, multi-service systems.
- Existing process: issues, requirements docs, decision records, changelogs, architecture docs, runbooks.

## Governance Tiers

### lightweight

Use for small, solo, early, local, or low-risk projects.

Generate simple content, but still scaffold the full folder structure:

- `AGENTS.md`
- `CODEX.md`
- `.ai/instructions.md`
- `.ai/task-routing.md`
- `.ai/context-loading-rules.md`
- `.ai/context/project-map.md`
- `.ai/context/known-issues.md`
- `.ai/agents/.gitkeep`
- `.ai/prompts/.gitkeep`
- `.ai/skills/agent-rails-memory/SKILL.md`
- `.ai/context/memory-policy.md`
- `.ai/tools/agent_rails_memory.py` and platform launchers

Keep requirements and decision logs optional. Use simple assumptions instead of formal approvals unless the user asks for more control.

### standard

Use for most shared software projects.

Generate the full AI pack with requirements, decision, evidence, project map, routing, and context-loading files.

Expected controls:

- One project owner or decision authority.
- Clear verification commands.
- Requirements intake for behavior changes.
- Decision log for target behavior, architecture, and external dependencies.
- Evidence labels for claims that future agents might otherwise over-trust.

### strict

Use for migrations, regulated systems, customer data, security, production-critical work, multi-agent work, or high ambiguity.

Add stronger language:

- Agents must not infer completeness from existing code or docs.
- Behavior changes require approved requirements.
- Verification evidence must be current and executable when possible.
- Fail closed for security-sensitive or externally dependent operations.
- Approval authority must be named or explicitly left as `{UNASSIGNED_DECISION_AUTHORITY}` until filled.
- Historical archives are non-authoritative unless explicitly promoted.

## Questions Worth Asking

Ask only when inspection cannot answer:

- Who can approve target behavior, requirements, and exceptions?
- Which files or folders are local tooling state and should not be treated as project knowledge?
- Which verification commands prove readiness?
- Should the project use lightweight, standard, or strict governance?
- Are there source-of-truth docs outside the repository?

## Defaults

- Governance tier: `standard`.
- Approval authority: repository owner or project maintainer if discoverable; otherwise leave a clearly named placeholder.
- Evidence labels: `Confirmed`, `Likely`, `Unclear`, `Missing`, `Contradiction`.
- Root adapters: concise pointers into `.ai/`.
