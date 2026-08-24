# Review AI Resources Prompt

Use this prompt to review generated AI resources before relying on them.

```text
Review these AI resources for correctness, portability, and safety.

Check:
- Root adapters are short and point to canonical context.
- .ai folders exist: agents, context, prompts, skills.
- Context files separate code behavior, documentation claims, assumptions, tests, and approved decisions.
- Requirements require approval before implementation.
- Agent archetypes match the project and do not add irrelevant specialists.
- Clean architecture, separation of concerns, testability, dependency hygiene, and security are represented.
- Existing project guidance was preserved.
- No unrelated project names, authority rules, migration assumptions, or stale domain terms leaked in.
- Open decisions are explicit rather than hidden as vague placeholders.

Return severity-ranked findings:
- Finding
- Impact
- Evidence
- Corrective action

If no blocking issues exist, say so and list residual risks.
```
