"""Regression tests for the candidate-only public-copy audit patterns."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_public_copy import find_candidates, check_html
from project_public_copy import pack
import json


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

    def test_compressed_fallback_and_category_guards_cannot_hide_notes(self):
        embedded=json.dumps(pack({'views': {}}))
        legacy=pack({'profiles': {'0000': {'notes': 'AS-617'}}})
        overlay=pack({'rows': [{'expected_data': 'PDF was not read in this batch'}]})
        main='data=await decodeAtlasPacked('+json.dumps(legacy['payload'])+','+json.dumps(legacy['sha256'])+');'
        main+='const packedCategoryOverlay='+json.dumps(overlay)+';'
        for name, obj in [('discovery',{}),('storyHookData',{}),('presentationEdits',{}),('curated',{})]:
            main+='const '+name+'='+json.dumps(obj)+';'
        html='<script id="atlas-pilot-data" type="application/json">'+embedded+'</script><script>'+main+'</script>'
        matches=check_html(html,'synthetic')
        self.assertTrue(any(x['location'].startswith('map_and_fallback') and x['rule']=='internal_audit_id' for x in matches))
        self.assertTrue(any(x['location'].startswith('category_overlay') and x['rule']=='batch_process_description' for x in matches))

    def test_packed_identity_failure_is_blocking(self):
        from project_public_copy import unpack
        wrapper=pack({'text':'synthetic'})
        wrapper['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity mismatch'):
            unpack(wrapper)


if __name__ == "__main__":
    unittest.main()
