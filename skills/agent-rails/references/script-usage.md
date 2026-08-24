# Script Usage

Use `scripts/generate_ai_resources.py` for reliable scaffolding.

## Mode Flags

Two mode flags exist and control different things:

- `--mode new|existing` describes the state of the target directory and controls merge behavior. Use `new` to bootstrap a fresh folder and `existing` to merge safely into a repo that already has content.
- `--resource-mode new-project|existing-project|migration` describes the shape of the AI-resource pack to emit and matches the three workflow modes in the kit prompts. It defaults from `--mode`; set it explicitly for migration work.

Example: `--mode existing --resource-mode migration` adds migration-oriented resources to an existing repo without overwriting it.

## Common Commands

Preview an existing repo update:

```powershell
python scripts/generate_ai_resources.py --target C:\path\to\repo --mode existing --tier standard --dry-run
```

```bash
python scripts/generate_ai_resources.py --target /path/to/repo --mode existing --tier standard --dry-run
```

Apply after reviewing:

```powershell
python scripts/generate_ai_resources.py --target C:\path\to\repo --mode existing --tier standard --apply
```

```bash
python scripts/generate_ai_resources.py --target /path/to/repo --mode existing --tier standard --apply
```

Bootstrap a new repo folder:

```powershell
python scripts/generate_ai_resources.py --target C:\path\to\repo --mode new --tier standard --apply
```

```bash
python scripts/generate_ai_resources.py --target /path/to/repo --mode new --tier standard --apply
```

## Useful Metadata Flags

- `--project-name`
- `--project-description`
- `--resource-mode new-project|existing-project|migration`
- `--current-state`
- `--decision-authority`
- `--verification-command`
- `--source-doc`
- `--local-tooling-exclusion`

Repeat list flags such as `--verification-command` and `--source-doc` when needed.

## Output Meaning

- `create-dir`: directory would be or was created.
- `create-file`: file would be or was created.
- `preserve-file`: file already exists and was not changed.
- `marker`: `.gitkeep` would be or was created for an empty scaffold directory.
- `validate`: validation result or warning.
- `conflict`: existing content needs manual review.
- `merge-file`: a narrowly scoped safe addition was appended while preserving existing content; currently used for the `.ai/runtime/` and `.ai/memory/` ignore rules.

## Safety Defaults

- Dry-run is the default.
- Existing files are preserved.
- The helper does not delete files.
- The helper does not inspect secrets.
- The helper safely appends `.ai/runtime/` and `.ai/memory/` to an existing `.gitignore` without replacing user rules.
- The helper validates generated content for unresolved runtime placeholders.
- Checking for unrelated project-specific leakage is a manual review step; see `references/validation.md`.
