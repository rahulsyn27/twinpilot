# TwinPilot Foundation Architecture

This repository is organized as a monorepo with clear boundaries:

- `backend`: Python backend runtime, API delivery, and internal application layers.
- `frontend`: Next.js delivery layer and web UI shell.
- `infrastructure`: Docker Compose and service-level infrastructure assets.
- `scripts`: local development helpers.

The current milestone intentionally includes only platform foundations: runtime bootstrapping, connectivity, infrastructure wiring, and operational scaffolding.
