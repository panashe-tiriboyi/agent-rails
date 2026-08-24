# Validation

Run these checks before finishing an AI resource pack.

## Content Checks

- Every runtime `{PLACEHOLDER}` is replaced or intentionally moved to an open decision.
- The reusable `docs/requirements/change-request-template.md` may keep its request placeholders.
- Links point to files that exist.
- Root adapters are short and point to canonical `.ai/` files.
- Governance tier is consistent across files.
- Requirements, decisions, and evidence rules do not contradict each other.
- Local tooling state is excluded from project knowledge.
- Existing files are preserved when adding resources to an existing repo.
- `.ai/runtime/` and `.ai/memory/` are present in `.gitignore` without loss of existing rules.
- Memory guidance consistently requires the platform launcher and local-first recall.

## Leakage Checks

Search generated files for content carried over from unrelated projects or template sources:

- stale company, product, person, or repository names
- authority rules, approval chains, or governance terms specific to another project
- migration constraints or parity rules that do not apply to the target project

Such content is allowed only when the user explicitly asks to preserve that context.

## Evidence Checks

Confirm that:

- Code behavior is not described as complete unless verified.
- Documentation is described as a claim until checked.
- Approved decisions identify the decision owner or record the owner as unknown.
- Verification commands are listed with paths and dates when available.
- Strict-tier packs require fresh evidence for readiness claims.

## Structure Checks

Expected full pack:

- `AGENTS.md`
- `CODEX.md`
- `.ai/agents/.gitkeep`
- `.ai/instructions.md`
- `.ai/task-routing.md`
- `.ai/context-loading-rules.md`
- `.ai/context/project-map.md`
- `.ai/context/decisions.md`
- `.ai/context/decisions-needed.md`
- `.ai/context/known-issues.md`
- `.ai/context/evidence-rules.md`
- `.ai/context/memory-policy.md`
- `.ai/prompts/master-kickoff.prompt.md`
- `.ai/prompts/analyze-workspace.prompt.md`
- `.ai/prompts/plan-ai-resources.prompt.md`
- `.ai/prompts/test-strategy.prompt.md`
- `.ai/prompts/review-ai-resources.prompt.md`
- `.ai/prompts/migration-evidence-map.prompt.md`
- `.ai/skills/agent-rails-memory/SKILL.md`
- `.ai/tools/agent_rails_memory.py`
- `.ai/tools/memory.cmd`
- `.ai/tools/memory.sh`
- `docs/requirements/README.md`
- `docs/requirements/change-request-template.md`

Lightweight packs may keep simpler content, but should still scaffold the full `.ai/` folder shape so later resources are not missed.

## Script Checks

When `scripts/generate_ai_resources.py` is used:

- First run with `--dry-run`.
- Confirm `--apply` creates all required folders.
- Confirm existing root adapters are reported as `preserve-file`.
- Confirm empty `.ai/agents` and `.ai/prompts` contain `.gitkeep`; confirm `.ai/skills/agent-rails-memory/SKILL.md` exists.
- Confirm the memory launcher creates and uses `.ai/runtime/venv/` and `doctor` reports FTS5.
- Confirm generated files have no unrelated project-specific leakage.
