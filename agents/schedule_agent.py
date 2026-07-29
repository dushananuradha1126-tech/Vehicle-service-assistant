import logging
from typing import Dict, Any
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

STANDARD_MILEAGE_BRACKETS = [
    5000, 10000, 15000, 20000, 30000, 40000, 50000, 60000, 80000, 100000
]

def calculate_service_schedule(mileage_km: int, vehicle_type: str = "Car", last_service_km: int = 0) -> Dict[str, Any]:
    """
    Calculates recommended maintenance checklist based on vehicle mileage and type.
    """
    logger.info(f"Schedule Agent evaluating mileage: {mileage_km} km for {vehicle_type}")

    prompt = f"""
You are a Lead Service Advisor for Automotive & Motorcycle Maintenance.

Vehicle Type: {vehicle_type}
Current Odometer Reading: {mileage_km:,} km
Last Recorded Service: {last_service_km:,} km

Provide a structured, personalized service checklist covering:
1. Immediate Maintenance Items (Due Now).
2. Major Component Replacement Milestones (e.g. Timing Belt, Spark Plugs, Fluids).
3. Inspection Checklist (Brakes, Suspension, Battery, Tires).
4. Next Scheduled Service Milestone (Distance & Estimated Timeframe).

Format clearly with bullet points and bold section headings.
"""

    try:
        schedule_text = ask_groq(prompt)
        return {
            "mileage_km": mileage_km,
            "vehicle_type": vehicle_type,
            "checklist": schedule_text,
            "status": "success"
        }
    except Exception as exc:
        logger.error(f"Schedule agent evaluation error: {exc}")
        return {
            "mileage_km": mileage_km,
            "vehicle_type": vehicle_type,
            "checklist": f"Error generating service schedule: {exc}",
            "status": "error"
        }

if __name__ == "__main__":
    res = calculate_service_schedule(25000, "Motorcycle")
    print(res["checklist"])
