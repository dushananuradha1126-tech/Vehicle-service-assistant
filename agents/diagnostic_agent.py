import logging
from typing import Dict, Any
from utils.groq_client import ask_groq

logger = logging.getLogger(__name__)

SEVERITY_LEVELS = {
    "CRITICAL": "Immediate danger of mechanical destruction or safety hazard. Do not drive.",
    "HIGH": "Requires prompt repair within 100-200 km to prevent major damage.",
    "MEDIUM": "Should be inspected during the next routine service interval.",
    "LOW": "Minor cosmetic, non-essential electrical, or routine adjustment."
}

def analyze_diagnostic_symptoms(symptoms: str, vehicle_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyzes fault symptoms, warning lights, or mechanical noises to evaluate urgency and diagnostic steps.
    """
    logger.info(f"Diagnostic Agent analyzing symptoms: {symptoms}")

    vehicle_str = ""
    if vehicle_info:
        vehicle_str = f"Vehicle: {vehicle_info.get('make', 'Vehicle')} {vehicle_info.get('model', '')} ({vehicle_info.get('mileage', 'N/A')} km)"

    prompt = f"""
You are a Senior Vehicle Master Diagnostic Technician.

Analyze the reported fault symptoms and determine:
1. Probable Root Causes (sorted by likelihood).
2. Urgency & Risk Assessment (CRITICAL, HIGH, MEDIUM, or LOW).
3. Recommended Immediate Action (e.g., Pull over immediately vs Drive to mechanic).
4. Step-by-step diagnostic inspection guide for a technician or owner.

{vehicle_str}
Reported Symptoms: "{symptoms}"

Structure your response with clear Markdown headers:
### 🚨 Diagnostic Summary & Urgency Level
### 🔍 Probable Root Causes
### 🛡️ Immediate Safety Action
### 🔧 Step-by-Step Inspection & Troubleshooting
"""

    try:
        diagnosis = ask_groq(prompt)
        return {
            "symptoms": symptoms,
            "diagnosis": diagnosis,
            "status": "success"
        }
    except Exception as exc:
        logger.error(f"Diagnostic agent error: {exc}")
        return {
            "symptoms": symptoms,
            "diagnosis": f"Error performing diagnostic evaluation: {exc}",
            "status": "error"
        }

if __name__ == "__main__":
    res = analyze_diagnostic_symptoms("Brakes squeal loudly when coming to a stop and pedal feels spongy")
    print(res["diagnosis"])
