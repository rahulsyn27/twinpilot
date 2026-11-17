"""Reference implementations used to validate the plug-in interface."""

from time import perf_counter

from app.benchmark.plugins.base import SemanticRAGBase
from app.benchmark.types import RAGResponse


class SimpleRAG(SemanticRAGBase):
    name = "simple"
    display_name = "Simple RAG"
    capabilities = {"semantic_retrieval", "single_hop"}

    def answer(self, query: str, history: list[dict[str, str]] | None = None) -> RAGResponse:
        started_at = perf_counter()
        documents = self.retrieve(query)
        return self.response(query, documents, {"strategy": "retrieve_once", "query": query}, started_at)


class HyDERAG(SemanticRAGBase):
    name = "hyde"
    display_name = "HyDE"
    capabilities = {"semantic_retrieval", "query_transformation", "hyde"}

    def answer(self, query: str, history: list[dict[str, str]] | None = None) -> RAGResponse:
        started_at = perf_counter()
        hypothetical_document = f"A concise, factual response to: {query}"
        documents = self.retrieve(hypothetical_document)
        return self.response(query, documents, {"strategy": "hyde", "query": query, "hypothetical_document": hypothetical_document}, started_at)
