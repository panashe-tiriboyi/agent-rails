# {PROJECT_NAME} Agent Primer

{PROJECT_DESCRIPTION}

Current state: {CURRENT_STATE}

## Start Here

1. Read `.ai/instructions.md`.
2. Use `.ai/task-routing.md` to select one primary specialist.
3. Follow `.ai/context-loading-rules.md`; do not load the whole repository unless the task requires it.
4. Load only the selected route, relevant skill, and up to three detailed context files initially.

## Local-First Memory

- Read `.ai/context/memory-policy.md` before historical recall or durable memory writes.
- Query Agent Rails SQLite memory before platform-native memory.
- Invoke `.ai/tools/memory.cmd` on Windows or `.ai/tools/memory.sh` on macOS/Linux; never run the Python engine directly.
- Show the returned aggregate memory activity indicator in the active chat response.

## Requirements And Changes

Route new behavior, architecture, workflow, or product changes through `docs/requirements/change-request-template.md` unless the change is clearly trivial.

Approved requirements that ask for behavior changes require implementation and verification, not documentation-only updates, unless the requester explicitly asks for documentation-only work.

## Evidence Rules

- Separate current code behavior, documentation claims, approved decisions, assumptions, and runtime evidence.
- Use the labels in `.ai/context/evidence-rules.md`.
- Cite file paths and verification dates when making durable claims.
- Do not mark work verified unless current code, tests, runtime output, or approved decisions support it.

## Repository Map

See `.ai/context/project-map.md`.

## Non-Negotiable Guardrails

- Do not infer completeness from existing routes, services, docs, tests, or old status labels.
- Do not weaken security or authorization without an approved decision.
- Do not invent business rules, requirements, or approval authority.
- Preserve user changes and unrelated local work.
- Treat archives and generated output as historical unless promoted by an approved decision.
- Do not commit secrets, credentials, or private data.
- Do not commit `.ai/runtime/` or `.ai/memory/`; they contain the private virtual environment and memory store.

## Local Tooling

Do not treat local editor, agent, cache, or machine-specific config as project knowledge unless explicitly documented in `.ai/context/project-map.md`.
