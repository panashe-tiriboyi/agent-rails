# Architecture Primer

Record the target architecture and current implementation boundaries.

## Current Shape

- Application boundaries: not mapped yet.
- Data boundaries: not mapped yet.
- External integrations: not mapped yet.
- Deployment boundaries: not mapped yet.

## Architecture Rails

- Prefer clean architecture for the selected stack.
- Keep domain or business logic separate from transport, persistence, UI, and infrastructure concerns.
- Keep dependencies pointed inward where the stack supports it.
- Add abstractions only when they reduce meaningful complexity or protect a boundary.
- Record deviations and trade-offs as decisions.

## Open Architecture Questions

Record unresolved boundaries in `.ai/context/decisions-needed.md`.
