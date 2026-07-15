# Security Primer

Record security-sensitive assumptions, checks, and open risks.

## Security Areas

- Authentication: not assessed yet.
- Authorization: not assessed yet.
- Secrets and configuration: not assessed yet.
- Data privacy: not assessed yet.
- Dependency risk: not assessed yet.
- Infrastructure and deployment: not assessed yet.

## Security Rails

- Do not weaken authentication or authorization without explicit approval.
- UI hiding is not server-side authorization.
- Do not commit secrets, tokens, private keys, or raw private data.
- Prefer supported dependencies and flag known vulnerable or unmaintained packages.
- Prototype shortcuts must be explicit and recorded as risks.

## Open Security Questions

Record unresolved decisions in `.ai/context/decisions-needed.md`.
