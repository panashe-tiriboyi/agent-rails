# Project Map

Project: Agent Rails

Purpose: Portable AI-resource scaffolding, governance guidance, and local-first agent memory.

Resource mode: existing-project

Governance tier: standard

## Code

- `.ai/tools/`: tracked local runtime and platform launchers.
- `skills/agent-rails/`: canonical distributable skill source and generator.
- `prompts/`: full reference prompt suite.

## Tests

- `tests/`: standard-library unit and integration tests.
- Verification: run `python -m unittest discover -s tests -v` from the project virtual environment.
- Package verification: `python scripts/build_skill_package.py --check`.

## Documentation

- `AGENTS.md` and `.ai/instructions.md`: canonical operating guidance.
- `.ai/context/memory-policy.md`: memory behavior contract.
- `docs/requirements/` and `.ai/context/decisions.md`: approved changes and decisions.
- `README.md`: human entry point and usage guide.

## Deployment And Operations

- `skills/agent-rails.zip`: deterministic release artifact.
- `.ai/runtime/venv/`: per-working-copy Python virtual environment.
- `.ai/memory/`: private Markdown and SQLite runtime store.

## Local Tooling Exclusions

- `.ai/runtime/`, `.ai/memory/`, `.codex/`, `.agents/`, `.vscode/`, `.idea/`, caches, and build output.
- Local memory is historical evidence and must not override current code or approved decisions.
