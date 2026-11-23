"""Integration boundary tests: no source overwrite, content loss or unsafe output."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("layout_prototype", ROOT / "scripts/build_layout_prototype.py")
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)


class LayoutBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "docs/primary/index.html").read_text()
        cls.css = (ROOT / "prototypes/primary-layout/layout.css").read_text()
        cls.candidate, cls.report = layout.transform(cls.source, cls.css)

    def test_runtime_data_sources_styles_and_existing_ids_are_exact(self):
        self.assertTrue(self.report["original_scripts_identical"])
        self.assertTrue(self.report["original_styles_identical"])
        self.assertTrue(self.report["metadata_and_csp_identical"])
        self.assertEqual(len(self.report["script_sha256"]), 4)
        self.assertGreater(self.report["existing_dom_ids_preserved"], 100)

    def test_runtime_tampering_is_rejected(self):
        damaged = self.candidate.replace("function setReadingView(", "function changedReadingView(", 1)
        with self.assertRaisesRegex(layout.ContractError, "Runtime or embedded content changed"):
            layout.verify_preservation(self.source, damaged)

    def test_a_later_content_or_runtime_snapshot_is_kept_exact(self):
        script = layout.Document(self.source).one(id="atlas-pilot-data")
        future = self.source[:script["inner"]] + "\n  " + self.source[script["inner"]:]
        future = future.replace("function setReadingView(", "/* later runtime revision */ function setReadingView(", 1)
        candidate, report = layout.transform(future, self.css)
        self.assertTrue(report["original_scripts_identical"])
        self.assertNotEqual(report["script_sha256"], self.report["script_sha256"])
        self.assertIn("/* later runtime revision */", candidate)

    def test_upstream_dom_contract_changes_fail_closed(self):
        with self.assertRaises(layout.ContractError):
            layout.transform(self.source.replace('id="atlas-search"', 'id="new-search"', 1), self.css)

    def test_duplicate_ids_fail_closed(self):
        with self.assertRaisesRegex(layout.ContractError, "Duplicate"):
            layout.transform(self.source.replace("</main>", '<div id="atlas-search"></div></main>', 1), self.css)

    def test_later_ui_copy_cannot_be_silently_overwritten(self):
        with self.assertRaisesRegex(layout.ContractError, "Masthead changed upstream"):
            layout.transform(self.source.replace('<h1>New Jersey</h1>', '<h1>A later editorial heading</h1>', 1), self.css)

    def test_young_edition_is_not_a_primary_input(self):
        with self.assertRaises(layout.ContractError):
            layout.transform((ROOT / "docs/young-explorers/index.html").read_text(), self.css)

    def test_overlay_cannot_introduce_a_script(self):
        with self.assertRaises(layout.ContractError):
            layout.transform(self.source, "</style><script>unexpected()</script>")

    def test_reapplying_the_prototype_is_rejected(self):
        with self.assertRaises(layout.ContractError):
            layout.transform(self.candidate, self.css)

    def test_working_trees_cannot_be_output_destinations(self):
        with self.assertRaisesRegex(layout.ContractError, "outside every Git checkout"):
            layout.validate_destination(ROOT / "docs")
        with tempfile.TemporaryDirectory() as folder:
            other = Path(folder)
            (other / ".git").write_text("gitdir: elsewhere")
            with self.assertRaises(layout.ContractError):
                layout.validate_destination(other / "editorial-output")

    def test_arbitrary_existing_files_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            sentinel = destination / "keep.txt"
            sentinel.write_text("retain this")
            with self.assertRaisesRegex(layout.ContractError, "unmanaged"):
                layout.validate_destination(destination)
            self.assertEqual(sentinel.read_text(), "retain this")

    def test_symlink_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "target"
            target.mkdir()
            link = Path(folder) / "link"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(layout.ContractError):
                layout.validate_destination(link)

    def test_source_must_be_an_immutable_commit(self):
        for ref in ["main", "origin/main", "HEAD", "../editorial", "--help"]:
            with self.assertRaises(layout.ContractError):
                layout.git_bytes(ref, "docs/primary/index.html")


if __name__ == "__main__":
    unittest.main()
