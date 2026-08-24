# Architecture Overview

Use this file to summarize the current and intended architecture.

## System Purpose

Agent Rails is a portable AI-resource kit and generator. It supplies canonical
agent guidance, requirement and evidence rails, and a local-first historical
memory capability to target repositories.

## Major Components

- Reference pack: root adapters, `.ai/`, prompts, and project documentation.
- Canonical distributable source: `skills/agent-rails/`.
- Generator: `skills/agent-rails/scripts/generate_ai_resources.py`.
- Memory runtime: `.ai/tools/agent_rails_memory.py` plus platform launchers.
- Memory data flow: agent-authored JSON -> validated Markdown record -> SQLite
  FTS5 index -> ranked historical chunks -> visible chat indicator.
- External runtime prerequisite: Python 3.11+ with `venv` and SQLite FTS5; no
  third-party Python packages or network services are used.

## Architecture Principles

- Prefer clean architecture for the selected stack.
- Keep responsibilities separated.
- Keep security and data ownership explicit.
- Record material trade-offs in `.ai/context/decisions.md`.
- Keep Markdown as canonical memory content and SQLite as the rebuildable recall index.
- Keep private runtime state under ignored `.ai/runtime/` and `.ai/memory/` directories.

## Open Questions

Record future schema, encryption, synchronization, embeddings, or platform-hook
decisions in `.ai/context/decisions-needed.md` before implementation.
