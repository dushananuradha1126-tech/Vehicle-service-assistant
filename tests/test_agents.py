import unittest
from unittest.mock import patch

from agents.intent_agent import classify_intent
from agents.orchestrator import process_vehicle_query

class TestVehicleAgents(unittest.TestCase):

    @patch("agents.intent_agent.ask_groq")
    def test_intent_classification(self, mock_ask_groq):
        mock_ask_groq.return_value = '{"intent": "FAULT_DIAGNOSTICS", "confidence": 0.95, "reasoning": "Symptom query"}'
        res = classify_intent("Why is my brake pedal spongy?")
        self.assertEqual(res["intent"], "FAULT_DIAGNOSTICS")
        self.assertEqual(res["confidence"], 0.95)

    @patch("agents.orchestrator.ask_groq")
    def test_orchestrator_routing(self, mock_ask_groq):
        mock_ask_groq.return_value = "### Diagnostic Summary\nPossible air in brake line."
        res = process_vehicle_query("Spongy brakes", {"make": "Honda", "mileage": 20000})
        self.assertIn("status", res)
        self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
