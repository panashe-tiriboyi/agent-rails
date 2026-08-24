# Claude Adapter

Canonical project guidance is in `AGENTS.md` and `.ai/`.

Read `AGENTS.md`, then `.ai/instructions.md`. Route the task with `.ai/task-routing.md` and load context according to `.ai/context-loading-rules.md`.

For historical context, query Agent Rails memory through `.ai/tools/memory.cmd` or `.ai/tools/memory.sh` before using native memory, and show its activity indicator.

Use `.ai/prompts/master-kickoff.prompt.md` for guided new-project, existing-project, or migration setup.

Do not implement unapproved requirements. Treat documentation as a claim until checked against code, tests, runtime output, or approved decisions.
