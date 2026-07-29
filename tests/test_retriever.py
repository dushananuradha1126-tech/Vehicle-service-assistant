import unittest
from rag.retriever import format_context_for_prompt

class TestRetrieverUtils(unittest.TestCase):

    def test_format_context_for_prompt_empty(self):
        result = format_context_for_prompt([])
        self.assertEqual(result, "No specific manual documentation available.")

    def test_format_context_for_prompt_valid(self):
        sample_docs = [
            {"source": "engine_oil.txt", "content": "Change oil every 5,000 km.", "relevance_score": 0.1}
        ]
        result = format_context_for_prompt(sample_docs)
        self.assertIn("engine_oil.txt", result)
        self.assertIn("Change oil every 5,000 km.", result)

if __name__ == "__main__":
    unittest.main()
