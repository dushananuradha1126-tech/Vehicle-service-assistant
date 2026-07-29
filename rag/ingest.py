import os
import logging
import math
from pathlib import Path

from utils.config import (
    DOCUMENTS_DIR,
    VECTORSTORE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SimpleDocument:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}

class SimpleHashEmbeddings:
    """Fast, reliable 384-dim hash embedding function."""
    def __init__(self, dim=384):
        self.dim = dim

    def _embed_text(self, text: str):
        vec = [0.0] * self.dim
        words = text.lower().split()
        if not words:
            return vec
        for word in words:
            idx = abs(hash(word)) % self.dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def embed_documents(self, texts: list[str]):
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text: str):
        return self._embed_text(text)

def split_text_to_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Splits raw text into overlapping chunks."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks

def build_vector_store():
    """Ingests all .txt document manuals and creates a vector store."""
    logger.info("Initializing document ingestion pipeline...")
    
    if not DOCUMENTS_DIR.exists():
        logger.error(f"Documents directory not found at: {DOCUMENTS_DIR}")
        raise FileNotFoundError(f"Directory not found: {DOCUMENTS_DIR}")

    txt_files = list(DOCUMENTS_DIR.glob("*.txt"))
    if not txt_files:
        logger.warning(f"No .txt documents found in {DOCUMENTS_DIR}")
        return None

    raw_chunks = []
    for file_path in txt_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            text_chunks = split_text_to_chunks(content, CHUNK_SIZE, CHUNK_OVERLAP)
            for chunk_text in text_chunks:
                doc = SimpleDocument(
                    page_content=chunk_text,
                    metadata={"source_name": file_path.name, "category": file_path.stem}
                )
                raw_chunks.append(doc)
            logger.info(f"Loaded {len(text_chunks)} chunks from: {file_path.name}")
        except Exception as exc:
            logger.error(f"Failed to load {file_path.name}: {exc}")

    logger.info(f"Total document chunks created: {len(raw_chunks)} from {len(txt_files)} files.")

    try:
        from langchain_chroma import Chroma
    except ImportError:
        from langchain_community.vectorstores import Chroma

    embeddings = SimpleHashEmbeddings()

    logger.info(f"Building ChromaDB vector database at: {VECTORSTORE_DIR}")
    vector_db = Chroma.from_documents(
        documents=raw_chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR)
    )

    logger.info("✅ Vector database created successfully!")
    return vector_db

if __name__ == "__main__":
    build_vector_store()