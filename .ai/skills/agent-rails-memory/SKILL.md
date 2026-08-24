---
name: agent-rails-memory
description: Query and maintain the repository-local Agent Rails SQLite memory before using platform-native historical memory.
---

# Agent Rails Memory

Use this skill when a request depends on earlier decisions, fixes, rationale,
preferences, or task outcomes, and when a completed task produces durable
project knowledge.

## Required Workflow

1. Read `.ai/context/memory-policy.md`.
2. Select `.ai/tools/memory.cmd` on Windows or `.ai/tools/memory.sh` on macOS/Linux.
3. Search local memory before any platform-native memory lookup.
4. Use only the returned relevant chunks; verify current claims against current evidence.
5. At material task boundaries, submit one sanitized structured summary when warranted.
6. Append one aggregate Agent Rails memory indicator to the chat response whenever the engine was used.

Never execute the Python engine directly, store a raw transcript, bypass a
sensitive-content rejection, or forget records without explicit user authority.
