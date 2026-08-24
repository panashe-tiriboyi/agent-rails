## Summary

Describe the problem, the implemented change, and its user-facing impact.

## Requirement and Decision

- Requirement: <!-- Link docs/requirements/REQ-... or explain why the change is trivial. -->
- Decision: <!-- Link .ai/context/decisions.md entry when applicable. -->

## Verification

List the exact commands run and their current results.

```text
command:
result:
```

## Documentation

- [ ] README and usage guidance are current.
- [ ] CHANGELOG includes the user-facing change.
- [ ] Architecture, security, operations, and testing docs are updated where applicable.
- [ ] Generated guidance contains no unresolved placeholders or unrelated project leakage.

## Distribution and Safety

- [ ] Tests pass on the current branch.
- [ ] `skills/agent-rails.zip` matches canonical `skills/agent-rails/` source.
- [ ] Existing target-repository files are preserved or safely merged.
- [ ] `.ai/memory/`, `.ai/runtime/`, credentials, tokens, and private data are not committed.
- [ ] This pull request targets `main`; no direct merge or release tag should occur before required review and checks pass.
