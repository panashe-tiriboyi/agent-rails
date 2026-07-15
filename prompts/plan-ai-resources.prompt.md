# Plan AI Resources Prompt

Use this prompt after the kickoff QA or workspace analysis.

```text
Create an AI-resource implementation plan for this project.

Inputs:
- Project mode: new project, existing project, or migration.
- User answers from the kickoff questionnaire.
- Workspace evidence if available.
- Desired governance tier.
- Known constraints, risks, non-goals, and approval authority.

Plan:
- Recommend files and folders to create.
- Recommend agent archetypes to include or omit.
- Define context primers and their ownership.
- Define prompt modules to include.
- Define requirements and approval flow.
- Define clean architecture and separation-of-concerns guidance for the detected stack.
- Define test, review, security, and dependency checks.
- Define migration evidence mapping if migration mode is selected.
- Identify open decisions before generation.

Output:
- Summary
- Recommended agent set
- Context and prompt files
- Requirements and approvals
- Architecture and security rails
- Verification plan
- Open decisions

Do not generate files until the user approves this plan.
```
