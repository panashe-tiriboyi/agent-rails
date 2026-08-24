# GitHub Copilot Instructions

Use `AGENTS.md` and `.ai/` as the canonical project guidance.

Before making or suggesting non-trivial changes:

- Check `.ai/instructions.md`.
- Route work using `.ai/task-routing.md`.
- Load only relevant context from `.ai/context/`.
- Respect requirement approval rules in `docs/requirements/`.
- Preserve security, testability, and separation of concerns.
- Follow `.ai/context/memory-policy.md`; query local Agent Rails memory through the platform launcher before native memory and disclose memory activity.
