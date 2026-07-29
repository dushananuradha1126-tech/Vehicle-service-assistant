import logging
from typing import Dict, Any

from agents.intent_agent import classify_intent
from agents.knowledge_agent import synthesize_knowledge_response
from agents.diagnostic_agent import analyze_diagnostic_symptoms
from agents.schedule_agent import calculate_service_schedule

logger = logging.getLogger(__name__)

def process_vehicle_query(query: str, vehicle_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Central Coordinator / Agent Orchestrator.
    1. Classifies user query intent.
    2. Routes to specialized agents (Diagnostic Agent, Schedule Agent, or Knowledge Agent).
    3. Aggregates final answer, agent execution trace, and source documents.
    """
    logger.info(f"Orchestrator received query: '{query}'")

    if vehicle_info is None:
        vehicle_info = {}

    # Step 1: Classify intent
    intent_meta = classify_intent(query)
    intent_category = intent_meta.get("intent", "GENERAL_QUERY")
    confidence = intent_meta.get("confidence", 1.0)
    reasoning = intent_meta.get("reasoning", "")

    agent_used = "Knowledge Agent (RAG)"
    additional_notes = ""

    # Step 2: Route based on classified intent
    if intent_category == "FAULT_DIAGNOSTICS":
        agent_used = "Diagnostic Agent"
        diag_res = analyze_diagnostic_symptoms(query, vehicle_info)
        primary_response = diag_res.get("diagnosis", "")
    elif intent_category == "MAINTENANCE_SCHEDULE":
        agent_used = "Schedule Agent"
        mileage = vehicle_info.get("mileage", 5000)
        vtype = vehicle_info.get("type", "Vehicle")
        sched_res = calculate_service_schedule(mileage, vtype)
        primary_response = sched_res.get("checklist", "")
    else:
        # Default or Technical / Warranty query -> Knowledge Agent with RAG
        agent_used = "Knowledge Agent (RAG)"
        rag_res = synthesize_knowledge_response(query, vehicle_info)
        primary_response = rag_res.get("answer", "")

    # Step 3: Fetch RAG context to attach references if available
    rag_context = synthesize_knowledge_response(query, vehicle_info)
    retrieved_sources = rag_context.get("retrieved_sources", [])
    snippets = rag_context.get("snippets", [])

    return {
        "query": query,
        "primary_answer": primary_response,
        "intent_category": intent_category,
        "confidence": confidence,
        "intent_reasoning": reasoning,
        "agent_used": agent_used,
        "retrieved_sources": list(set(retrieved_sources)),
        "snippets": snippets,
        "status": "success"
    }

if __name__ == "__main__":
    result = process_vehicle_query(
        "Why is there a squeaking sound when I apply the brakes at low speeds?",
        {"make": "Toyota", "model": "Corolla", "mileage": 45000}
    )
    print(f"Intent: {result['intent_category']} (Agent: {result['agent_used']})")
    print(result["primary_answer"])
