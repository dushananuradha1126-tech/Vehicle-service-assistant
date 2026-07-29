import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# LLM & Embedding Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# RAG Settings
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

def validate_config() -> dict:
    """Validates configuration parameters and returns health status."""
    status = {
        "groq_key_set": bool(GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here"),
        "documents_dir_exists": DOCUMENTS_DIR.exists(),
        "vectorstore_exists": VECTORSTORE_DIR.exists(),
        "model": GROQ_MODEL,
        "embedding_model": EMBEDDING_MODEL_NAME
    }
    return status