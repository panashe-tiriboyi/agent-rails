# Changelog

All notable changes to Agent Rails are documented here. The project follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions. Versions
and release tags are created through the GitHub review and release workflow.

## [Unreleased]

### Added

- Repository-local long-term memory using human-readable Markdown and SQLite FTS5.
- Windows and POSIX launchers that create and reuse an isolated Python 3.11+ virtual environment.
- Local-first historical recall policy, material-boundary ingestion, visible activity indicators, and explicit forgetting.
- Secret-like content rejection, deterministic ranking, deduplication, reindexing, corruption recovery, and concurrent-write support.
- Canonical unpacked skill source under `skills/agent-rails/` and reproducible ZIP packaging.
- Standard-library unit and integration tests for the engine, launchers, generator, and distribution.

### Changed

- Consolidated local state under ignored `.ai/memory/` and `.ai/runtime/` paths.
- Extended generated Agent Rails packs with the memory engine, launchers, policy, and project-local skill.
- Updated Codex, Claude, Gemini, Cursor, and Copilot guidance to use local memory before platform-native recall.
- Updated generator ignore handling to migrate the obsolete runtime rule while preserving unrelated user entries.
- Documented architecture, security, operations, testing, requirements, and contributor workflows.

### Verification

- 17 standard-library tests pass on Windows with Python 3.11 and SQLite FTS5.
- Generated-pack first-run environment creation and reuse are covered end to end.
- POSIX launcher behavior is contract-tested and requires POSIX CI before release tagging.
- `skills/agent-rails.zip` is reproducibly generated and matches canonical source.
