# Contributing to Agent Rails

Thank you for contributing. Agent Rails is an open-source project with a
review-first GitHub workflow. Changes must reach `main` through a pull request;
do not develop or release directly from `main`.

## Development Workflow

1. Start from an up-to-date `main` branch.
2. Create a focused development branch using the maintainer-approved naming
   convention; the current integration branch is `dev-panashe`.
3. Keep requirements, decisions, implementation, tests, and documentation in
   the same branch when they describe one change.
4. Run the applicable verification commands and record current evidence.
5. Open a GitHub pull request using the repository template.
6. Merge only after required review and repository checks succeed.
7. Create release tags through the repository's GitHub release process after
   the reviewed change is merged.

## Requirements and Evidence

- Route non-trivial behavior, architecture, workflow, data, security,
  deployment, or product changes through `docs/requirements/`.
- Approval authorizes implementation; documentation alone does not verify behavior.
- Record material architecture or workflow decisions in `.ai/context/decisions.md`.
- Follow `.ai/context/evidence-rules.md` and do not report a check as passing
  unless it ran against the current branch.

## Local Setup and Verification

Python 3.11 or newer is required. The memory launcher creates the project-local
virtual environment without installing third-party packages.

Windows:

```powershell
.ai\tools\memory.cmd doctor
.ai\runtime\venv\Scripts\python.exe -m unittest discover -s tests -v
.ai\runtime\venv\Scripts\python.exe scripts\build_skill_package.py --check
```

macOS/Linux:

```bash
.ai/tools/memory.sh doctor
.ai/runtime/venv/bin/python -m unittest discover -s tests -v
.ai/runtime/venv/bin/python scripts/build_skill_package.py --check
```

When canonical skill source changes, rebuild the release artifact before opening the pull request:

```powershell
.ai\runtime\venv\Scripts\python.exe scripts\build_skill_package.py
```

```bash
.ai/runtime/venv/bin/python scripts/build_skill_package.py
```

## Pull Request Expectations

- Keep the change focused and explain its user-facing impact.
- Link the approved requirement and decision when applicable.
- Include verification commands and results.
- Update `README.md`, `CHANGELOG.md`, and relevant architecture, security,
  operations, or testing documentation.
- Confirm generated resources contain no unresolved placeholders or unrelated project leakage.
- Confirm `skills/agent-rails.zip` matches canonical source.
- Never commit `.ai/memory/`, `.ai/runtime/`, secrets, credentials, tokens, or private data.
