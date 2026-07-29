# TwinPilot

TwinPilot is a monorepo foundation for a production-grade autonomous AI engineering platform.

## Stack

- **Backend**: FastAPI, Python 3.13, SQLAlchemy, Alembic, Pydantic Settings
- **Frontend**: Next.js, React, TypeScript, TailwindCSS, shadcn/ui primitives
- **Infra**: Docker, Docker Compose, PostgreSQL, Redis, Qdrant

## Quick start

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Services:

- API: http://localhost:8000
- API health: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000
- Qdrant: http://localhost:6333
