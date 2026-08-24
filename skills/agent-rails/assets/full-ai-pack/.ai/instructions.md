# {PROJECT_NAME} AI Instructions

Use these rules for all agent work in this repository.

## Operating Model

- Ground claims in repository evidence before acting.
- Prefer targeted search and focused file reads over broad context loading.
- Keep changes scoped to the request and the owning subsystem.
- Preserve unrelated user work.
- Ask only when the answer cannot be discovered and a wrong assumption would be risky.

## Local-First Memory

- Follow `.ai/context/memory-policy.md` for all historical recall and durable memory writes.
- Search local SQLite memory before platform-native memory.
- Use only `.ai/tools/memory.cmd` on Windows or `.ai/tools/memory.sh` on macOS/Linux so memory code runs inside the repository virtual environment.
- Append one aggregate memory indicator whenever the engine is used.
- Store sanitized summaries only at material task boundaries; never store raw transcripts or secret material.

## Governance Tier

{GOVERNANCE_TIER_NOTES}

## Requirement Flow

- New behavior or product changes start as a requirement in `docs/requirements/`.
- Approved requirements identify the decision owner and acceptance criteria.
- Documentation approval is not verification.
- Behavior is not done until implementation and executable or inspectable evidence support it.

## Evidence Labels

Use `.ai/context/evidence-rules.md`.

Default labels:

- `Confirmed`
- `Likely`
- `Unclear`
- `Missing`
- `Contradiction`

## Verification

Primary verification commands:

{VERIFICATION_COMMANDS}

If commands cannot run, record why and what evidence remains missing.

## Authority

Decision authority: {DECISION_AUTHORITY}

Do not approve target behavior, exceptions, or readiness gates without that authority.
