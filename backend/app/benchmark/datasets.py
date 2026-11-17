"""Small, deterministic starter dataset. Public benchmark packs are added separately."""

from app.benchmark.types import SourceDocument


STARTER_CORPUS = [
    SourceDocument("rag-01", "RAG retrieves relevant external documents and gives them to a language model so answers can be grounded in current evidence.", {"topic": "rag"}),
    SourceDocument("rag-02", "HyDE creates a hypothetical answer or document, embeds it, and uses it to retrieve real supporting documents before answering.", {"topic": "hyde"}),
    SourceDocument("rag-03", "Corrective RAG assesses retrieved evidence and may issue another retrieval request after discarding weak context.", {"topic": "corrective"}),
    SourceDocument("rag-04", "Graph RAG uses entities and relationships in a knowledge graph to retrieve connected evidence for multi-hop questions.", {"topic": "graph"}),
    SourceDocument("rag-05", "Giskard RAGET can generate question-answer test sets from a knowledge base and evaluate RAG answers against them.", {"topic": "evaluation"}),
    SourceDocument("rag-06", "Sentence Transformers encode text into dense vectors. Cosine similarity between vectors can rank semantically related passages.", {"topic": "embeddings"}),
]

STARTER_TESTS = [
    {"id": "starter-01", "question": "What does HyDE use to retrieve real documents?", "reference_answer": "A hypothetical answer or document.", "reference_document_ids": ["rag-02"]},
    {"id": "starter-02", "question": "Which RAG approach uses entity relationships for multi-hop questions?", "reference_answer": "Graph RAG.", "reference_document_ids": ["rag-04"]},
    {"id": "starter-03", "question": "What kind of vectors do Sentence Transformers create?", "reference_answer": "Dense vectors.", "reference_document_ids": ["rag-06"]},
]

DATASETS = {"starter-rag": {"id": "starter-rag", "name": "Starter RAG concepts", "description": "A tiny deterministic corpus for verifying plug-ins and UI flows.", "document_count": len(STARTER_CORPUS), "test_count": len(STARTER_TESTS), "capabilities": ["single_hop", "semantic_retrieval"]}}


def get_dataset(dataset_id: str) -> tuple[list[SourceDocument], list[dict[str, object]]]:
    if dataset_id != "starter-rag":
        raise KeyError(dataset_id)
    return STARTER_CORPUS, STARTER_TESTS
