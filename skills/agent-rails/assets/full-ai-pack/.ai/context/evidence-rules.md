# Evidence Rules

Use these labels for durable claims.

## Labels

- `Confirmed`: directly verified from current code, tests, runtime output, source data, or an approved decision.
- `Likely`: supported by evidence, but not fully verified.
- `Unclear`: available evidence is incomplete or ambiguous.
- `Missing`: expected artifact, source, test, or decision was not found.
- `Contradiction`: two sources disagree and the conflict has not been resolved.

## Claim Types

Recommended claim types:

- Current code behavior
- Runtime behavior
- Test evidence
- Documentation claim
- Approved decision
- Assumption
- External source

## Rules

- Cite file paths for repository evidence.
- Record verification dates for claims intended to persist.
- Do not treat documentation as verified behavior until checked.
- Do not mark readiness, completion, or gate status without current evidence.
- Prefer `Unclear` over guessing.
