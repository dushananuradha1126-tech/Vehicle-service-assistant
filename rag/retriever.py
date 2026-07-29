import logging
from typing import List, Dict, Any, Tuple
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from utils.config import (
    VECTORSTORE_DIR,
    EMBEDDING_MODEL_NAME,
    TOP_K_RESULTS
)

logger = logging.getLogger(__name__)

_vector_db = None

def get_vector_store() -> Chroma:
    """Lazy loader for ChromaDB instance."""
    global _vector_db
    if _vector_db is None:
        if not VECTORSTORE_DIR.exists():
            logger.warning(f"Vectorstore directory not found at {VECTORSTORE_DIR}. Building new store.")
            from rag.ingest import build_vector_store
            _vector_db = build_vector_store()
        else:
            embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            _vector_db = Chroma(
                persist_directory=str(VECTORSTORE_DIR),
                embedding_function=embedding
            )
    return _vector_db

def retrieve_documents(query: str, top_k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
    """Retrieves top_k relevant document snippets matching the query."""
    try:
        db = get_vector_store()
        if db is None:
            return []

        results_with_scores = db.similarity_search_with_score(query, k=top_k)
        retrieved = []

        for doc, score in results_with_scores:
            retrieved.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source_name", "manual"),
                "category": doc.metadata.get("category", "general"),
                "relevance_score": round(float(score), 4)
            })

        return retrieved
    except Exception as exc:
        logger.error(f"Error during document retrieval: {exc}")
        return []

def format_context_for_prompt(retrieved_docs: List[Dict[str, Any]]) -> str:
    """Formats retrieved document list into a clean text block for LLM prompts."""
    if not retrieved_docs:
        return "No specific manual documentation available."

    context_snippets = []
    for idx, doc in enumerate(retrieved_docs, start=1):
        context_snippets.append(
            f"--- Document Snippet [{idx}] (Source: {doc['source']}) ---\n{doc['content']}"
        )
    return "\n\n".join(context_snippets)

if __name__ == "__main__":
    docs = retrieve_documents("When should I change engine oil?")
    print(f"Retrieved {len(docs)} documents.")
    print(format_context_for_prompt(docs))