import logging
from typing import Dict, Any
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

def query_groq_agent(prompt: str, vehicle_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Groq AI Agent.
    Directly processes vehicle maintenance inquiries using Groq LLM services.
    """
    logger.info(f"Groq AI Agent processing prompt: {prompt}")

    vehicle_str = ""
    if vehicle_info:
        make = vehicle_info.get("make", "")
        model = vehicle_info.get("model", "")
        year = vehicle_info.get("year", "")
        mileage = vehicle_info.get("mileage", "")
        vehicle_str = f"Vehicle Context: {year} {make} {model} ({mileage} km)\n"

    full_prompt = f"""
{vehicle_str}
User Query: "{prompt}"

Provide a clear, practical, and safety-focused response regarding vehicle service or diagnostics.
"""

    try:
        response = ask_groq(full_prompt)
        return {
            "query": prompt,
            "response": response,
            "agent_name": "Groq AI Agent",
            "status": "success"
        }
    except Exception as exc:
        logger.error(f"Groq AI Agent execution error: {exc}")
        return {
            "query": prompt,
            "response": f"Error executing Groq AI Agent: {exc}",
            "agent_name": "Groq AI Agent",
            "status": "error"
        }

if __name__ == "__main__":
    res = query_groq_agent("What should I check if my car AC stops blowing cold air?")
    print(res["response"])
