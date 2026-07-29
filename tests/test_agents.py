import unittest
from unittest.mock import patch

from agents.intent_agent import classify_intent
from agents.cost_agent import estimate_service_cost
from agents.orchestrator import process_vehicle_query

class TestVehicleAgents(unittest.TestCase):

    @patch("utils.groq_client.ask_groq")
    def test_intent_classification(self, mock_ask_groq):
        mock_ask_groq.return_value = '{"intent": "FAULT_DIAGNOSTICS", "confidence": 0.95, "reasoning": "Symptom query"}'
        res = classify_intent("Why is my brake pedal spongy?")
        self.assertEqual(res["intent"], "FAULT_DIAGNOSTICS")

    @patch("utils.groq_client.ask_groq")
    def test_cost_estimator_agent(self, mock_ask_groq):
        mock_ask_groq.return_value = "### Estimated Total Cost\n$150 - $250"
        res = estimate_service_cost("Brake pad replacement", {"make": "Honda"})
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["cost_report"]) > 0)

    @patch("utils.groq_client.ask_groq")
    def test_orchestrator_cost_routing(self, mock_ask_groq):
        mock_ask_groq.side_effect = [
            '{"intent": "COST_ESTIMATION", "confidence": 0.95, "reasoning": "Price query"}',
            '### Cost Report\nParts: $100, Labor: $80',
            '### RAG Synthesis\nStandard brake pad guidelines.'
        ]
        res = process_vehicle_query("How much for brake replacement?", {"make": "Toyota"})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["agent_used"], "Cost Estimator Agent")

if __name__ == "__main__":
    unittest.main()
