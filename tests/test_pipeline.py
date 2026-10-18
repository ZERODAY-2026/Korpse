
import json
import unittest
from unittest.mock import patch

from ai.pipeline import analyze_document


VALID_RESULT = {
    "document_type": "Notice to Vacate",
    "summary": "The landlord requests that the tenant vacate.",
    "key_issues": ["Alleged non-payment of rent"],
    "important_dates": ["25 October 2026"],
    "urgency": "unclear",
    "urgency_reason": "The available information is insufficient.",
    "missing_information": ["Jurisdiction"],
}


class TestLegalTriagePipeline(unittest.TestCase):

    @patch("ai.pipeline.generate_response")
    def test_valid_document(self, mock_generate):
        mock_generate.return_value = json.dumps(VALID_RESULT)

        result = analyze_document("Sample notice text")

        self.assertEqual(result["document_type"], "Notice to Vacate")
        self.assertEqual(result["urgency"], "unclear")
        self.assertIn("disclaimer", result)
        mock_generate.assert_called_once()

    def test_empty_document_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_document("   ")

    @patch("ai.pipeline.generate_response")
    def test_invalid_json_is_rejected(self, mock_generate):
        mock_generate.return_value = "This is not JSON"

        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            analyze_document("Sample notice text")

    @patch("ai.pipeline.generate_response")
    def test_missing_fields_are_rejected(self, mock_generate):
        mock_generate.return_value = json.dumps(
            {"document_type": "Notice to Vacate"}
        )

        with self.assertRaisesRegex(RuntimeError, "missing required"):
            analyze_document("Sample notice text")

    @patch("ai.pipeline.generate_response")
    def test_unknown_urgency_becomes_unclear(self, mock_generate):
        invalid_result = {
            **VALID_RESULT,
            "urgency": "critical",
        }
        mock_generate.return_value = json.dumps(invalid_result)

        result = analyze_document("Sample notice text")

        self.assertEqual(result["urgency"], "unclear")


if __name__ == "__main__":
    unittest.main()
