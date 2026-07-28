import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCUMENTS_PATH = "documents"
VECTORSTORE_PATH = "vectorstore"

documents = []

print("Loading documents...")

for filename in os.listdir(DOCUMENTS_PATH):
    if filename.endswith(".txt"):
        file_path = os.path.join(DOCUMENTS_PATH, filename)
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

print(f"Loaded {len(documents)} documents.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")

print("Creating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating vector database...")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=VECTORSTORE_PATH
)

print("✅ Vector database created successfully!")