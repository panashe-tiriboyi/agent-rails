# Test Strategy Prompt

Use this prompt to define verification expectations for a project or requirement.

```text
Design the test and verification strategy for this project or requirement.

Inputs:
- Project stack and architecture.
- Requirements or acceptance criteria.
- Known risks and constraints.
- Existing test tools and commands.
- Security, auth, data, migration, or external dependency concerns.

Return:
- Test levels needed: unit, integration, contract, UI, e2e, migration parity, security, performance, or smoke.
- Minimal fixtures and test data.
- Happy path, denial, boundary, malformed input, dependency failure, and regression scenarios.
- Commands to run locally and in CI.
- Evidence that counts as verified.
- Gaps that remain unverified.

Rules:
- Do not claim tests passed unless they ran in this session.
- Separate code failures from environment failures.
- Do not encode unresolved product decisions as final expected behavior.
```
