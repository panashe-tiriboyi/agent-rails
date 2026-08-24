# Project Type Guidance

Use this reference to adapt the AI pack to common project shapes.

## Web App

Typical source-of-truth files:

- package manifests
- app/router directories
- component library docs
- design references
- Playwright or browser test configs

Add guidance for:

- accessibility and responsive checks
- visual regression or screenshot evidence when UI changes
- avoiding broad rewrites of shared components
- distinguishing design claims from implemented behavior

## Backend API

Typical source-of-truth files:

- OpenAPI specs
- route/controller definitions
- service boundaries
- database migrations
- integration tests

Add guidance for:

- authorization must remain server-side
- API contracts are changed only with approved requirements
- data migrations need rollback or compatibility notes
- external dependency failures should have explicit behavior

## Data Or AI App

Typical source-of-truth files:

- notebooks
- pipeline definitions
- model/eval configs
- dataset docs
- prompt or agent configs

Add guidance for:

- dataset lineage and privacy constraints
- reproducible evaluation commands
- model/provider/version recording
- separating demo output from verified behavior
- never committing secrets or raw private data

## Documentation-Heavy Project

Typical source-of-truth files:

- docs indexes
- decision records
- research notes
- published specs

Add guidance for:

- citations and source dates
- claim labels
- contradiction tracking
- clear distinction between draft, approved, and obsolete documents

## Multi-Service Or Monorepo

Add guidance for:

- per-service routing
- service ownership map
- integration contract boundaries
- test commands by service
- context-loading limits to avoid whole-repo scans
