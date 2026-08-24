# Test Strategy

Use this file to define how the project proves behavior.

## Test Levels

- Unit: Python standard-library `unittest` coverage for the memory engine.
- Integration: launcher, generator, reindex, and package-contract tests.
- Contract: not configured yet.
- UI or end-to-end: not configured yet.
- Security or migration-specific: not configured yet.

## Commands

Run inside the automatically created project virtual environment:

```powershell
.ai\tools\memory.cmd doctor
.ai\runtime\venv\Scripts\python.exe -m unittest discover -s tests -v
python scripts\build_skill_package.py --check
```

```bash
.ai/tools/memory.sh doctor
.ai/runtime/venv/bin/python -m unittest discover -s tests -v
python3 scripts/build_skill_package.py --check
```

## Evidence Rules

Do not claim tests passed unless they ran in the current session. Record command, date, result, and known limitations.

## Verification Evidence

- Date: 2026-08-24
- Command: `.ai/runtime/venv/Scripts/python.exe -m unittest discover -s tests -v`
- Result: 17 tests passed after runtime-path consolidation.
- Package check: `scripts/build_skill_package.py --check` confirmed the ZIP matches canonical source.
- Platform coverage: the Windows launcher was executed end to end; the POSIX launcher contract is covered statically and is ready for execution in POSIX CI.
- Concurrency hardening: the concurrent-write case passed ten consecutive stress runs after adding bounded WAL-initialization retries.
