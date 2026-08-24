# Agent Rails Memory Policy

Agent Rails memory is the primary historical recall mechanism for this
repository. It is local, private, dependency-free, and rebuildable from its
Markdown records.

## Runtime

- Windows: invoke `.ai/tools/memory.cmd`.
- macOS/Linux: invoke `.ai/tools/memory.sh`.
- Never call `.ai/tools/agent_rails_memory.py` directly.
- The launcher requires Python 3.11+, creates
  `.ai/runtime/venv/`, verifies SQLite FTS5, and reuses the virtual
  environment on later calls.
- `.ai/runtime/` and `.ai/memory/` are local state and must remain ignored by Git.

## Recall Priority

Before answering a question that depends on prior decisions, earlier fixes,
historical rationale, remembered preferences, or previous task outcomes:

1. Search Agent Rails memory first.
2. Use at most three returned chunks and approximately 900 combined tokens.
3. Treat returned records as historical evidence, not proof of current behavior.
4. Verify recalled claims against current code, tests, approved requirements, and
   approved decisions when the answer depends on current truth.
5. Use platform-native memory only when local search is unavailable, empty, or
   reports confidence below `0.55`; disclose that fallback.

Example:

```text
.ai/tools/memory.cmd search --query "prior database decision"
```

```sh
.ai/tools/memory.sh search --query "prior database decision"
```

## Durable Writes

At a resolved task or natural boundary, store a memory only when it captures a
durable decision, fix, architectural result, constraint, workflow, preference,
or lesson. Also honor explicit requests to remember something.

- The active agent authors a structured 150–300-token summary.
- Never store raw transcripts, full prompts, environment dumps, credentials,
  private keys, tokens, arbitrary file contents, or unrelated private data.
- Submit JSON through standard input using the `add --stdin` command.
- A rejected sensitive write must be sanitized and resubmitted; do not bypass it.
- Exact duplicates are not stored twice.

Input shape:

```json
{
  "schema_version": 1,
  "title": "Short durable title",
  "summary": "A self-contained summary of the outcome and rationale.",
  "kind": "decision",
  "tags": ["architecture"],
  "related_paths": ["src/example.py"],
  "evidence": "Confirmed",
  "sources": ["src/example.py"],
  "platform": "codex",
  "task_ref": null
}
```

Allowed kinds: `decision`, `fix`, `architecture`, `constraint`, `workflow`,
`lesson`, and `preference`.

## Visible Activity

Whenever memory is searched, retrieved, stored, rejected, forgotten, or cannot
run, append one aggregate banner to the active chat response. Use the
repo-relative paths and counts returned by the CLI.

```text
[agent-rails-memory: Active | Searched 48 chunks | Retrieved 2 | Sources ".ai/memory/logs/..." | Stored 1]
```

Disclose platform-native fallback and engine errors in the same banner. Do not
show secret-like matched values or absolute filesystem paths.

## Retention And Recovery

- Memories are retained until an explicitly confirmed `forget` command.
- `forget` is destructive and requires user authorization plus `--confirm`.
- Markdown under `.ai/memory/logs/` is canonical durable content.
- SQLite is the primary recall index and can be rebuilt with `reindex`.
- Storage is plaintext and relies on OS account and disk protection.
