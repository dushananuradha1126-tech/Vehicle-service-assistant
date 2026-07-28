from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load embedding model
print("Loading embedding model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Open existing vector database
print("Opening vector database...")

db = Chroma(
    persist_directory="vectorstore",
    embedding_function=embedding
)

print("Retriever loaded successfully!")

# Function to retrieve relevant documents
def retrieve_documents(query):
    print(f"Searching for: {query}")

    results = db.similarity_search(query, k=3)

    print(f"Documents found: {len(results)}")

    return results


# Test the retriever
if __name__ == "__main__":
    docs = retrieve_documents("When should I change engine oil?")

    print("\nRetrieved Documents:\n")

    for i, doc in enumerate(docs, start=1):
        print(f"Result {i}")
        print(doc.page_content)
        print("-" * 50)