# Security Notes

Use this file to track project security posture and unresolved risks.

## Areas To Assess

- Authentication
- Authorization
- Secrets and configuration
- Data privacy
- Dependencies
- Infrastructure and deployment

## Rules

- Do not commit secrets.
- Do not weaken authorization without explicit approval.
- Record intentionally insecure prototype choices as approved risks.
- Prefer supported and maintained dependencies.

## Local Memory

- `.ai/memory/` and `.ai/runtime/` are Git-ignored and contain plaintext Markdown
  summaries, SQLite data, and the project-local virtual environment.
- The engine never intentionally stores raw transcripts, prompts, environment
  dumps, arbitrary file contents, or credentials.
- High-confidence credential patterns are rejected before the Markdown file or
  database row is written; errors do not echo the matched value.
- Secret detection is defense in depth, not a guarantee. Agents must sanitize
  summaries before submission.
- Data-at-rest confidentiality relies on OS account and disk protection.
- `forget` requires explicit authorization and the `--confirm` flag.
