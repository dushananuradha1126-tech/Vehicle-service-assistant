import json
import logging
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

INTENT_CATEGORIES = {
    "MAINTENANCE_SCHEDULE": "Periodic service, oil change intervals, filter changes, routine checks.",
    "FAULT_DIAGNOSTICS": "Warning lights, abnormal noises, engine performance issues, leaks, starting failures.",
    "COST_ESTIMATION": "Service price estimates, labor costs, repair quotes, parts replacement pricing.",
    "TECHNICAL_SPEC": "Tire pressure, fluid capacities, battery voltages, oil grades.",
    "WARRANTY_POLICY": "Warranty coverage, terms, claim eligibility, service center policy.",
    "GENERAL_QUERY": "General advice or unclassified vehicle inquiry."
}

def classify_intent(query: str) -> dict:
    """
    Classifies user question into vehicle maintenance intent categories.
    Returns dictionary with intent category, confidence, and recommended agent routing.
    """
    prompt = f"""
You are an Intent Classification Agent for a Vehicle Service System.

Analyze the user's question and classify it into EXACTLY ONE of the following categories:
- MAINTENANCE_SCHEDULE: {INTENT_CATEGORIES['MAINTENANCE_SCHEDULE']}
- FAULT_DIAGNOSTICS: {INTENT_CATEGORIES['FAULT_DIAGNOSTICS']}
- COST_ESTIMATION: {INTENT_CATEGORIES['COST_ESTIMATION']}
- TECHNICAL_SPEC: {INTENT_CATEGORIES['TECHNICAL_SPEC']}
- WARRANTY_POLICY: {INTENT_CATEGORIES['WARRANTY_POLICY']}
- GENERAL_QUERY: {INTENT_CATEGORIES['GENERAL_QUERY']}

User Question: "{query}"

Respond strictly in raw JSON format with the following keys:
{{
  "intent": "<CATEGORY_NAME>",
  "confidence": <float_between_0_and_1>,
  "reasoning": "<brief explanation>"
}}
"""
    try:
        response_text = ask_groq(prompt)
        # Clean JSON text if wrapped in markdown code blocks
        clean_json = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(clean_json)
        return result
    except Exception as exc:
        logger.error(f"Intent classification failed: {exc}")
        return {
            "intent": "GENERAL_QUERY",
            "confidence": 0.5,
            "reasoning": f"Fallback due to classification error: {exc}"
        }

if __name__ == "__main__":
    test_query = "Why is my check engine light flashing when I accelerate?"
    print(classify_intent(test_query))
