"""Shared local retrieval and Groq generation helpers."""

from time import perf_counter
from typing import Any

import numpy as np
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer

from app.benchmark.types import RAGResponse, SourceDocument
from app.core.config import settings


class SemanticRAGBase:
    name = "base"
    display_name = "Base RAG"
    capabilities: set[str] = {"semantic_retrieval"}

    def __init__(self) -> None:
        self.corpus: list[SourceDocument] = []
        self.config: dict[str, Any] = {}
        self.embedder: SentenceTransformer | None = None
        self.corpus_embeddings: np.ndarray | None = None

    def build(self, corpus: list[SourceDocument], config: dict[str, Any]) -> None:
        self.corpus = corpus
        self.config = config
        self.embedder = SentenceTransformer(config.get("embedding_model", settings.EMBEDDING_MODEL))
        self.corpus_embeddings = self.embedder.encode([item.content for item in corpus], normalize_embeddings=True)

    def retrieve(self, query: str, top_k: int | None = None) -> list[SourceDocument]:
        if self.embedder is None or self.corpus_embeddings is None:
            raise RuntimeError("Plugin must be built before it can answer questions.")
        query_embedding = self.embedder.encode([query], normalize_embeddings=True)[0]
        limit = top_k or int(self.config.get("top_k", 3))
        scores = self.corpus_embeddings @ query_embedding
        indices = np.argsort(scores)[::-1][:limit]
        return [self.corpus[int(index)] for index in indices]

    def generate(self, query: str, documents: list[SourceDocument]) -> str:
        if not settings.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is required to run a benchmark.")
        context = "\n\n".join(f"[{doc.id}] {doc.content}" for doc in documents)
        prompt = f"""Answer the question only from the supplied context. If the context does not support an answer, say so. Cite supporting document ids in square brackets.\n\nContext:\n{context}\n\nQuestion: {query}"""
        llm = ChatGroq(model=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY, temperature=0)
        return str(llm.invoke(prompt).content)

    def response(self, query: str, documents: list[SourceDocument], trace: dict[str, Any], started_at: float) -> RAGResponse:
        answer = self.generate(query, documents)
        return RAGResponse(answer=answer, retrieved_documents=documents, citations=[doc.id for doc in documents if f"[{doc.id}]" in answer], trace=trace, latency_ms=round((perf_counter() - started_at) * 1000, 2))
