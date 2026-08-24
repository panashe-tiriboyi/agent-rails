# Operations Notes

Use this file to record runtime and deployment context.

## Environments

- Local: Python 3.11+; launchers create `.ai/runtime/venv/` on first use.
- Development: not documented yet.
- Staging: not documented yet.
- Production: not documented yet.

## Deployment

The resource pack is generated from `skills/agent-rails/` and distributed as
`skills/agent-rails.zip`. Target repositories run memory locally; no service is deployed.

## Monitoring And Support

- Use `memory.cmd doctor` or `memory.sh doctor` for runtime diagnosis.
- Use `status` for schema and chunk counts.
- Use `reindex` to reconstruct SQLite from Markdown after index loss or corruption.
- Remove and recreate only `.ai/runtime/venv/` when repairing the Python
  environment; do not remove `.ai/memory/logs/` unless explicitly forgetting memory.
- Rebuild the distributable ZIP with `python scripts/build_skill_package.py`.
