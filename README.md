# RAG Benchmark Lab

A plug-and-play benchmark for comparing RAG architectures. The first reference plug-ins are Simple RAG and HyDE; the contract makes it safe to add the remaining RAG patterns without changing the evaluator or UI.

## Stack

- **Backend**: FastAPI, Python 3.13, LangChain Groq, Sentence Transformers, Giskard Checks
- **Frontend**: Next.js, React, TypeScript, TailwindCSS, shadcn/ui primitives
- **Infra**: Docker, Docker Compose, PostgreSQL, Redis, Qdrant

## Local quick start

```bash
cp .env.example .env
# Add GROQ_API_KEY to .env
cd backend && uv sync
uv run uvicorn app.main:app --reload
# In a second terminal
cd frontend && npm install && npm run dev
```

Services:

- API: http://localhost:8000/api/v1
- Frontend: http://localhost:3000

## Add a RAG plug-in

Implement `RAGPlugin` in `backend/app/benchmark/types.py`, then register it in `backend/app/benchmark/plugins/registry.py`. Every plug-in returns a `RAGResponse` containing the answer, retrieved documents, citations, and an execution trace. The benchmark can consequently test retrieval independently of answer quality and pass the result into Giskard Checks.

The starter suite is only a deterministic smoke test. Before publishing any score, run frozen public packs (SciFact for single-hop, HotpotQA for multi-hop, and FinQA for domain reasoning) and a versioned Giskard-generated test set.
