import tempfile
import unittest
from pathlib import Path

from html_link_audit import audit_site


class HtmlLinkAuditTests(unittest.TestCase):
    def test_valid_relative_file_and_fragment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="about.html#team">About</a>', encoding="utf-8")
            (root / "about.html").write_text('<h2 id="team">Team</h2>', encoding="utf-8")
            pages, issues = audit_site(root)
            self.assertEqual(len(pages), 2)
            self.assertEqual(issues, [])

    def test_missing_file_and_fragment_are_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="missing.html#nope">Broken</a>', encoding="utf-8")
            _, issues = audit_site(root)
            self.assertEqual([item["problem"] for item in issues], ["missing-file"])

    def test_outside_root_reference_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "site"
            root.mkdir()
            (root / "index.html").write_text('<img src="../outside.png">', encoding="utf-8")
            _, issues = audit_site(root)
            self.assertEqual(issues[0]["problem"], "outside-root")


if __name__ == "__main__":
    unittest.main()
