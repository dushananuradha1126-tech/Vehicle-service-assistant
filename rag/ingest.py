import os
import logging
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from utils.config import (
    DOCUMENTS_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def build_vector_store() -> Chroma:
    """Loads text documents from documents directory and creates vector store."""
    logger.info("Initializing document ingestion pipeline...")
    
    if not DOCUMENTS_DIR.exists():
        logger.error(f"Documents directory not found at: {DOCUMENTS_DIR}")
        raise FileNotFoundError(f"Directory not found: {DOCUMENTS_DIR}")

    raw_documents = []
    txt_files = list(DOCUMENTS_DIR.glob("*.txt"))

    if not txt_files:
        logger.warning(f"No .txt documents found in {DOCUMENTS_DIR}")
        return None

    for file_path in txt_files:
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source_name"] = file_path.name
                doc.metadata["category"] = file_path.stem
            raw_documents.extend(loaded_docs)
            logger.info(f"Loaded: {file_path.name}")
        except Exception as exc:
            logger.error(f"Failed to load {file_path.name}: {exc}")

    logger.info(f"Total documents loaded: {len(raw_documents)}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(raw_documents)
    logger.info(f"Created {len(chunks)} text chunks.")

    logger.info(f"Generating embeddings using model: {EMBEDDING_MODEL_NAME}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    logger.info(f"Building ChromaDB vector database at: {VECTORSTORE_DIR}")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR)
    )

    logger.info("✅ Vector database created successfully!")
    return vector_db

if __name__ == "__main__":
    build_vector_store()