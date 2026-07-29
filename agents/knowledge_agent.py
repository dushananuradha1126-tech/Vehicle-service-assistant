import logging
from typing import Dict, Any, List
from rag.retriever import retrieve_documents, format_context_for_prompt
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

def synthesize_knowledge_response(query: str, vehicle_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Retrieves domain knowledge documents and generates an augmented answer using Groq LLM.
    """
    logger.info(f"Knowledge Agent processing query: {query}")
    
    # Step 1: Retrieve relevant context snippets
    retrieved_snippets = retrieve_documents(query, top_k=3)
    formatted_context = format_context_for_prompt(retrieved_snippets)
    
    # Format vehicle specs if provided
    vehicle_context = ""
    if vehicle_info:
        make = vehicle_info.get("make", "N/A")
        model = vehicle_info.get("model", "N/A")
        year = vehicle_info.get("year", "N/A")
        mileage = vehicle_info.get("mileage", "N/A")
        vehicle_context = f"\nVehicle Specifications: Make={make}, Model={model}, Year={year}, Mileage={mileage} km\n"

    # Step 2: Build LLM RAG Prompt
    prompt = f"""
You are the Lead Knowledge Agent for Vehicle Service & Maintenance.

Use the retrieved documentation context below to answer the user's question accurately.
If the retrieved documentation does not fully cover the user's question, rely on certified automotive engineering best practices while keeping the response practical and safety-focused.

{vehicle_context}

--- RETRIEVED MANUAL DOCUMENTATION ---
{formatted_context}
-------------------------------------

User Question: "{query}"

Instructions:
1. Provide a direct, step-by-step resolution or answer.
2. Highlight potential safety precautions or warnings clearly.
3. Keep the tone professional, concise, and easy to read.
"""

    try:
        answer = ask_groq(prompt)
        return {
            "answer": answer,
            "retrieved_sources": [s["source"] for s in retrieved_snippets],
            "snippets": retrieved_snippets,
            "status": "success"
        }
    except Exception as exc:
        logger.error(f"Knowledge Agent synthesis failed: {exc}")
        return {
            "answer": f"Unable to synthesize response: {exc}",
            "retrieved_sources": [],
            "snippets": [],
            "status": "error"
        }

if __name__ == "__main__":
    res = synthesize_knowledge_response("How often should I change my engine oil?")
    print(res["answer"])
