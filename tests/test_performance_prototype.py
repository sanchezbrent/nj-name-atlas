"""Reject runtime drift and writes to editorial/publishing sources."""
import importlib.util
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('performance_prototype', ROOT / 'scripts/build_performance_prototype.py')
performance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(performance)
layout = performance.layout


class PerformanceBoundaryTests(unittest.TestCase):
    def test_both_editions_preserve_every_byte_outside_approved_runtime_patches(self):
        for edition in ['primary', 'young-explorers']:
            with self.subTest(edition=edition):
                source = (ROOT / 'docs' / edition / 'index.html').read_text()
                candidate = performance.transform(source)
                performance.verify_preservation(source, candidate)
                before, after = layout.Document(source), layout.Document(candidate)
                self.assertEqual(before.blocks('style'), after.blocks('style'))
                self.assertEqual(before.ids(), after.ids())
                self.assertEqual(before.blocks('script')[:3], after.blocks('script')[:3])

    def test_a_later_snapshot_keeps_unrelated_runtime_changes_exact(self):
        # Unit tests also run in the standard shallow quality checkout. The
        # full-history performance workflow composes both actual editorial refs.
        for edition in ['primary', 'young-explorers']:
            with self.subTest(edition=edition):
                source = (ROOT / 'docs' / edition / 'index.html').read_text()
                future = source.replace('function createAtlasPilotCore(', '/* later source revision */ function createAtlasPilotCore(', 1)
                candidate = performance.transform(future)
                performance.verify_preservation(future, candidate)
                self.assertIn('/* later source revision */', candidate)

    def test_primary_layout_composes_before_performance_without_changing_layout_contract(self):
        source = (ROOT / 'docs/primary/index.html').read_text()
        composed, _ = layout.transform(source, (layout.PROTOTYPE / 'layout.css').read_text())
        performance.verify_preservation(composed, performance.transform(composed))

    def test_missing_duplicate_or_changed_runtime_anchor_fails_closed(self):
        source = (ROOT / 'docs/primary/index.html').read_text()
        for before, _ in performance.patches():
            for changed in [source.replace(before, '', 1), source.replace(before, before + before, 1),
                            source.replace(before, before.replace('atlas-', 'future-atlas-'), 1)]:
                if changed == source:
                    continue
                with self.assertRaises(layout.ContractError):
                    performance.transform(changed)

    def test_modified_data_guards_markup_or_helpers_are_rejected(self):
        source = (ROOT / 'docs/primary/index.html').read_text()
        candidate = performance.transform(source)
        for before, after in [
            ('const validView=', 'const changedView='),
            ('id="atlas-pilot-data"', 'id="changed-payload"'),
            ('<h1>New Jersey</h1>', '<h1>Changed</h1>'),
            ('currentMatches.has(code)', 'true'),
        ]:
            self.assertIn(before, candidate)
            with self.subTest(before=before), self.assertRaises(layout.ContractError):
                performance.verify_preservation(source, candidate.replace(before, after, 1))

    def test_reapplying_is_rejected(self):
        source = (ROOT / 'docs/primary/index.html').read_text()
        with self.assertRaises(layout.ContractError):
            performance.transform(performance.transform(source))

    def test_output_cannot_target_git_or_unmanaged_directory(self):
        with self.assertRaises(layout.ContractError):
            performance.validate_destination(ROOT / 'docs')
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            (destination / 'keep.txt').write_text('untouched')
            with self.assertRaises(layout.ContractError):
                performance.validate_destination(destination)
            self.assertEqual((destination / 'keep.txt').read_text(), 'untouched')

    def test_output_cannot_cross_preview_ownership_or_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            (destination / layout.MARKER).write_text('{"generator":"primary-layout-prototype-v1"}')
            with self.assertRaises(layout.ContractError):
                performance.validate_destination(destination)
            link = destination / 'linked'
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(layout.ContractError):
                performance.validate_destination(link)

    def test_build_records_inputs_and_only_changes_two_edition_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            ref = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD']).decode().strip()
            report = performance.build(ref, Path(folder), reader_layout=True)
            self.assertFalse(report['publication_cleared'])
            self.assertTrue(report['layout_composition']['original_script_bytes_preserved'])
            self.assertEqual(set(report['layout_input_sha256']), {'layout.css', 'navigation.js', 'checkpoint.json'})
            self.assertEqual(set(report['editions']), {'primary', 'young-explorers'})
            changed = {p for p in layout.ASSETS if report['source_asset_sha256'][p] != report['output_asset_sha256'][p]}
            self.assertEqual(changed, {'primary/index.html', 'young-explorers/index.html'})
            self.assertEqual(performance.validate_destination(Path(folder)), Path(folder).resolve())
            self.assertFalse((Path(folder) / layout.MARKER).exists())


if __name__ == '__main__':
    unittest.main()
