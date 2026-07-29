# TwinPilot Foundation Architecture

This repository is organized as a monorepo with clear boundaries:

- `apps/api`: FastAPI delivery layer and API routing.
- `apps/frontend`: Next.js delivery layer and web UI shell.
- `core`: cross-cutting backend infrastructure (config, logging, DB, cache, vector DB, lifespan).
- `shared`: shared backend contracts and utility code.
- `services`: reserved for future domain/service orchestration.
- `docker`: container build definitions.
- `scripts`: local development helpers.

The current milestone intentionally includes only platform foundations: runtime bootstrapping, connectivity, infrastructure wiring, and operational scaffolding.
