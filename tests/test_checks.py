"""Prove the checks reject corruption and unintended public material."""
import importlib.util,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checks',ROOT/'scripts/check_project.py');checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        shutil.copytree(ROOT/'docs',self.root/'docs');shutil.copytree(ROOT/'project',self.root/'project')
    def tearDown(self):self.tmp.cleanup()
    def test_unchanged_baseline_passes(self):self.assertEqual(checks.check(self.root,syntax=False)['public_assets'],7)
    def test_historical_asset_corruption_fails(self):
        p=self.root/'docs/primary/index.html';p.write_bytes(p.read_bytes()+b'<!-- unintended change -->')
        with self.assertRaisesRegex(checks.CheckError,'asset changed'):checks.check(self.root,syntax=False)
    def test_extra_website_file_fails(self):
        (self.root/'docs/raw-export.json').write_text('{}')
        with self.assertRaisesRegex(checks.CheckError,'allowlist changed'):checks.check(self.root,syntax=False)
    def test_private_workbook_in_public_source_fails(self):
        (self.root/'master.xlsx').write_bytes(b'synthetic test only')
        with self.assertRaisesRegex(checks.CheckError,'forbidden in public Git'):checks.check(self.root,syntax=False)
    def test_website_symlink_fails(self):
        p=self.root/'docs/styles.css';p.unlink();p.symlink_to(ROOT/'docs/styles.css')
        with self.assertRaisesRegex(checks.CheckError,'symlink'):checks.check(self.root,syntax=False)
if __name__=='__main__':unittest.main()
