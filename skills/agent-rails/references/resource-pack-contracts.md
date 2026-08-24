# Resource Pack Contracts

Use these contracts when creating or updating generated files.

## Pack Scope

The bundled `assets/full-ai-pack/` template set is the minimal portable core. It generates `AGENTS.md`, `CODEX.md`, the base `.ai/` scaffold with core context primers and prompts, requirements intake, and the local-first SQLite memory runtime. Additional tool adapters and extended context primers (architecture, testing, security, operations, migration, requirements flow) live in the surrounding Agent Rails kit as a full reference scaffold; add them per project need rather than by default.

## Root Files

### `AGENTS.md`

Purpose: persistent project primer for all agents.

Include:

- Project name and one-sentence purpose.
- Current implementation state.
- Start-here sequence.
- Requirement/change intake rule.
- Evidence and verification rules.
- Repository map.
- Non-negotiable guardrails.
- Local tooling exclusions.

Keep it short. Link into `.ai/` for details.

### `CODEX.md`

Purpose: Codex adapter that points to canonical project guidance.

Include:

- Read `AGENTS.md` first.
- Read `.ai/instructions.md`.
- Route using `.ai/task-routing.md`.
- Load context using `.ai/context-loading-rules.md`.
- Avoid treating local tooling config as project knowledge.

## `.ai/` Files

### Required `.ai/` folders

Every full pack must include:

- `.ai/agents/`
- `.ai/context/`
- `.ai/prompts/`
- `.ai/skills/`
- `.ai/tools/`

Use `.gitkeep` in empty folders so the scaffold survives in Git. Scaffold these folders before generating files so new projects do not miss later expansion points.

### `.ai/instructions.md`

Purpose: canonical operating rules.

Include:

- How to classify claims.
- How to handle requirements.
- How to verify work.
- How to protect user changes.
- How to report evidence.
- Which commands or docs are authoritative.

### `.ai/task-routing.md`

Purpose: route work to one primary specialist context.

Use generic specialists unless the project needs custom ones:

- `requirements`
- `architecture`
- `frontend`
- `backend`
- `data-ai`
- `testing`
- `devops`
- `documentation`
- `security`

Each route should name when to use it and which context files to load first.

### `.ai/context-loading-rules.md`

Purpose: prevent agents from loading too much context.

Include:

- Read root guidance first.
- Select one primary route.
- Load up to three detailed context files initially.
- Prefer targeted search over whole-repo reading.
- Treat archives as historical unless promoted.

## `.ai/context/` Files

### `project-map.md`

Purpose: source-of-truth map of code, docs, tests, deployment, and local tooling exclusions.

### `decisions.md`

Purpose: approved decisions that future agents must respect.

Minimum fields:

- ID
- Date
- Status
- Decision
- Owner
- Scope
- Supersedes
- Evidence

### `decisions-needed.md`

Purpose: open questions that block implementation or verification.

Minimum fields:

- ID
- Question
- Why it matters
- Options
- Needed by
- Owner
- Status

### `known-issues.md`

Purpose: known defects, gaps, risks, and contradictions.

Use evidence labels and dates.

### `evidence-rules.md`

Purpose: define claim labels and verification expectations.

Recommended labels:

- `Confirmed`: directly verified from code, tests, runtime output, or approved decision.
- `Likely`: supported but not fully verified.
- `Unclear`: conflicting or insufficient evidence.
- `Missing`: expected artifact or evidence not found.
- `Contradiction`: two authoritative-looking sources disagree.

## `.ai/agents/`

Purpose: project-specific specialist agent definitions.

Start empty with `.gitkeep` unless the target project already has clear specialist boundaries. Do not invent domain specialists before the project needs them.

## `.ai/prompts/`

Purpose: reusable project prompts for recurring verification, review, or planning workflows.

For the full pack, include the reusable prompt suite:

- `master-kickoff.prompt.md`
- `analyze-workspace.prompt.md`
- `plan-ai-resources.prompt.md`
- `test-strategy.prompt.md`
- `review-ai-resources.prompt.md`
- `migration-evidence-map.prompt.md`

Skip prompts that do not match the project goal (for example, omit `migration-evidence-map.prompt.md` outside migration work). Use `.gitkeep` only when no prompt files are generated.

## `.ai/skills/`

Purpose: project-local skills that are too specific for global Codex skills.

Include `agent-rails-memory/SKILL.md` for the portable local-memory workflow.

## Local Memory Files

- `.ai/context/memory-policy.md`: canonical local-first recall, write, retention, and indicator contract.
- `.ai/tools/agent_rails_memory.py`: dependency-free SQLite FTS5 engine.
- `.ai/tools/memory.cmd`: Windows Python 3.11+ virtual-environment launcher.
- `.ai/tools/memory.sh`: macOS/Linux Python 3.11+ virtual-environment launcher.
- `.gitignore`: include or safely merge `.ai/runtime/` and `.ai/memory/` so private memory and the virtual environment are never staged.

The engine must reject direct execution outside the expected project virtual
environment. Markdown is canonical memory content; SQLite is the rebuildable
recall index. Platform-native memory is fallback-only and must be disclosed.

## Requirements Files

### `docs/requirements/README.md`

Purpose: index of active, approved, rejected, and completed requirements.

### `docs/requirements/change-request-template.md`

Purpose: template for new behavior changes.

Include:

- ID
- Title
- Status
- Requested by
- Decision owner
- Request
- Business reason
- Current evidence
- Desired outcome
- Acceptance criteria
- Out of scope
- Verification plan
- Change history

## Adaptation Rules

- Remove sections that do not fit the selected governance tier.
- Do not invent business rules, security requirements, or approval authorities.
- Prefer placeholders over false certainty when a required value is genuinely unknown.
- Never leave generic placeholders unresolved in final generated files unless the placeholder is intentionally framed as an open decision.
- Preserve existing files in existing repos; report manual review items instead of overwriting.
