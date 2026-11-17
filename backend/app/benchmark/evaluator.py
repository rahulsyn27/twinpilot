"""Evaluation layer with a stable response shape for Giskard RAGET and the UI."""

from collections.abc import Callable
from typing import Any

from app.benchmark.types import RAGResponse


def evaluate_fixed_testset(
    answer: Callable[[str], RAGResponse], tests: list[dict[str, Any]]
) -> dict[str, Any]:
    """Fast deterministic smoke evaluation; Giskard runs use the same answer contract."""
    rows: list[dict[str, Any]] = []
    for test in tests:
        response = answer(str(test["question"]))
        expected = set(test["reference_document_ids"])
        retrieved = {document.id for document in response.retrieved_documents}
        cited = set(response.citations)
        retrieval_recall = len(expected & retrieved) / len(expected) if expected else 1.0
        citation_recall = len(expected & cited) / len(expected) if expected else 1.0
        rows.append({
            "id": test["id"], "question": test["question"], "answer": response.answer,
            "reference_answer": test["reference_answer"], "retrieved_document_ids": sorted(retrieved),
            "expected_document_ids": sorted(expected), "retrieval_recall": retrieval_recall,
            "citation_recall": citation_recall, "latency_ms": response.latency_ms, "trace": response.trace,
        })
    count = len(rows) or 1
    retrieval_score = sum(row["retrieval_recall"] for row in rows) / count
    citation_score = sum(row["citation_recall"] for row in rows) / count
    return {"summary": {"score": round((retrieval_score * 0.7 + citation_score * 0.3) * 100, 1), "retrieval_recall": round(retrieval_score, 3), "citation_recall": round(citation_score, 3), "average_latency_ms": round(sum(row["latency_ms"] for row in rows) / count, 1), "test_count": len(rows), "evaluator": "fixed-suite (Giskard-compatible response contract)"}, "cases": rows}


def build_giskard_trace_payload(response: RAGResponse) -> dict[str, Any]:
    """Map a plug-in result into the JSON data consumed by Giskard Checks.

    Plug-ins stay independent from Giskard while checks can inspect the answer,
    retrieved context, citations, latency, and implementation trace.
    """
    return {
        "answer": response.answer,
        "retrieved_docs": [document.content for document in response.retrieved_documents],
        "retrieved_document_ids": [document.id for document in response.retrieved_documents],
        "citations": response.citations,
        "latency_ms": response.latency_ms,
        "execution_trace": response.trace,
    }
