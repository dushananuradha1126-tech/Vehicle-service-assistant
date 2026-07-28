from rag.retriever import retrieve_documents

query = "When should I change engine oil?"

results = retrieve_documents(query)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(results, start=1):
    print(f"Result {i}:")
    print(doc.page_content)
    print("-" * 50)