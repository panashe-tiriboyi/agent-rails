# Scaffold And Merge

Use this reference before creating or updating AI resources in a target project.

## Scaffold Contract

Create this structure for every full AI pack:

```text
AGENTS.md
CODEX.md
.ai/
  instructions.md
  task-routing.md
  context-loading-rules.md
  agents/
    .gitkeep
  context/
    project-map.md
    decisions.md
    decisions-needed.md
    known-issues.md
    evidence-rules.md
    memory-policy.md
  prompts/
    .gitkeep
  skills/
    agent-rails-memory/
      SKILL.md
  tools/
    agent_rails_memory.py
    memory.cmd
    memory.sh
docs/
  requirements/
    README.md
    change-request-template.md
```

Add `.ai/runtime/` and `.ai/memory/` to `.gitignore`. If `.gitignore` already
exists, append only the missing Agent Rails rules and preserve every existing line.

Keep `.gitkeep` only where a directory would otherwise be empty. If a later generated file is added to that directory, the marker may remain or be removed; either is acceptable.

## Existing Repo Merge Policy

Default to safe merge:

- Create missing directories.
- Create missing files from templates.
- Never overwrite an existing file unless the user explicitly asks for replacement.
- Report existing files as `preserved`.
- Report content differences as `conflict` or `manual review`, not as an automatic edit.
- Use open decisions for unknown authority, verification commands, or source-of-truth docs.

## New Repo Policy

For `--mode new`, generate the complete structure into the target directory. Existing files are still preserved unless explicit replacement is requested outside the default helper flow.

## Tier Effects

- `lightweight`: keep requirements and decisions simple; still scaffold the folders so future expansion does not miss structure.
- `standard`: generate the full pack and normal requirements/decision/evidence flow.
- `strict`: strengthen warnings around approvals, evidence, security-sensitive changes, and readiness claims.

## Do Not Copy Project-Specific Assumptions

Use existing projects only as pattern references. Do not copy names, migration rules, legacy parity language, local approval authority, company terms, or domain-specific guardrails unless the target project explicitly needs them.
