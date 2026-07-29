import logging
from typing import Dict, Any
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

def estimate_service_cost(query: str, vehicle_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Cost Estimator Agent.
    Estimates approximate service costs, parts pricing breakdown, labor hours, and budgeting tips.
    """
    logger.info(f"Cost Estimator Agent analyzing query: {query}")

    vehicle_str = "Vehicle: Standard Vehicle"
    if vehicle_info:
        make = vehicle_info.get("make", "")
        model = vehicle_info.get("model", "")
        year = vehicle_info.get("year", "")
        mileage = vehicle_info.get("mileage", "")
        vehicle_str = f"Vehicle Specs: {year} {make} {model} (Mileage: {mileage} km)"

    prompt = f"""
You are a Professional Automotive Cost & Repair Estimator Agent.

{vehicle_str}
Requested Maintenance / Repair Job: "{query}"

Provide an itemized cost estimate report covering:
1. 💵 Estimated Total Price Range (Parts + Labor).
2. 🛠️ Parts Breakdown & Estimated Replacement Costs.
3. ⏱️ Expected Labor Time (Hours) & Labor Rate Estimate.
4. 💡 Cost-Saving Tips & Preventive Advice to avoid higher future expenses.

Format clearly with Markdown headers, tables or bullet points.
"""

    try:
        cost_report = ask_groq(prompt)
        return {
            "query": query,
            "cost_report": cost_report,
            "status": "success"
        }
    except Exception as exc:
        logger.error(f"Cost Estimator Agent error: {exc}")
        return {
            "query": query,
            "cost_report": f"Unable to calculate cost estimate: {exc}",
            "status": "error"
        }

if __name__ == "__main__":
    res = estimate_service_cost("Brake pad replacement and rotor resurfacing", {"make": "Honda", "model": "Civic", "year": 2019})
    print(res["cost_report"])
