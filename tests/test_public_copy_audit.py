"""Regression tests for the candidate-only public-copy audit patterns."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_public_copy import find_candidates


class PublicCopyAuditTests(unittest.TestCase):
    def test_internal_original_wording_panel_is_flagged(self):
        self.assertIn("original_research_control",
                      find_candidates("Original research wording"))

    def test_workflow_ids_and_uninspected_sources_are_flagged(self):
        findings = find_candidates(
            "AS-617 said the PDF was not read; AI-generated HTML was used "
            "in this batch. The order remains uninspected."
        )
        for rule in ("internal_audit_id", "source_not_inspected",
                     "generated_intermediary", "batch_process_description"):
            self.assertIn(rule, findings)

    def test_historical_uncertainty_is_not_itself_flagged(self):
        self.assertEqual([], find_candidates(
            "Several historical accounts offer different explanations "
            "for the name, and the available evidence does not establish one."
        ))

    def test_source_citation_is_not_flagged(self):
        self.assertEqual([], find_candidates(
            "A. Historian, History of This Township (1882), pp. 12–14."
        ))


if __name__ == "__main__":
    unittest.main()
