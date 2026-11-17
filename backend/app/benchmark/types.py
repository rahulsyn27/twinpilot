"""Public contracts for every pluggable RAG implementation."""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class SourceDocument:
    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    retrieved_documents: list[SourceDocument]
    citations: list[str]
    trace: dict[str, Any]
    latency_ms: float


class RAGPlugin(Protocol):
    """The only interface a community implementation needs to satisfy."""

    name: str
    display_name: str
    capabilities: set[str]

    def build(self, corpus: list[SourceDocument], config: dict[str, Any]) -> None: ...

    def answer(self, query: str, history: list[dict[str, str]] | None = None) -> RAGResponse: ...
