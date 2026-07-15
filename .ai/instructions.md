# AI Instructions

Use these rules for all AI-assisted work in this repository.

## Operating Model

- Ground durable claims in repository evidence before acting.
- Prefer targeted search and focused file reads over broad context loading.
- Keep changes scoped to the request and the owning subsystem.
- Preserve unrelated user work.
- Ask only when the answer cannot be discovered and a wrong assumption would be risky.

## Requirement Flow

- New behavior, architecture, workflow, data, security, deployment, or product changes start as requirements in `docs/requirements/`.
- A draft requirement does not authorize implementation.
- Approved requirements identify the decision owner, acceptance criteria, and verification expectations.
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

Record project-specific verification commands in `.ai/context/project-map.md`.

If commands cannot run, record why and what evidence remains missing.

## Security And Quality

- Prefer clean architecture for the chosen stack.
- Preserve separation of concerns and testability.
- Prefer supported stable versions and secure dependencies.
- Flag security, privacy, authorization, data, infrastructure, and dependency risks.
- Allow prototype shortcuts only when explicitly approved and recorded.

## Authority

Record decision authority in `.ai/context/decisions.md` or the relevant requirement. Do not approve target behavior, exceptions, or readiness claims without that authority.
