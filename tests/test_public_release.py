from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_public_release", ROOT / "scripts" / "verify_public_release.py"
)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VERIFY
SPEC.loader.exec_module(VERIFY)


class PublicReleaseVerificationTests(unittest.TestCase):
    def test_repository_candidate_passes(self) -> None:
        findings, scanned = VERIFY.verify_repository(ROOT)
        self.assertGreater(scanned, 20)
        self.assertEqual([], [finding.render(ROOT) for finding in findings])

    def test_external_denylist_marker_is_rejected(self) -> None:
        marker = "nonpublic-marker-001"
        findings = VERIFY.scan_text(Path("sample.md"), marker, (marker,))
        self.assertTrue(
            any("external denylist" in finding.message for finding in findings)
        )

    def test_non_example_email_is_rejected(self) -> None:
        address = "person" + "@" + "company.test"
        findings = VERIFY.scan_text(Path("sample.md"), address)
        self.assertTrue(
            any("non-example email" in finding.message for finding in findings)
        )

    def test_credential_like_assignment_is_rejected(self) -> None:
        value = "a" * 24
        findings = VERIFY.scan_text(Path(".env"), f"WEBEX_BOT_TOKEN={value}\n")
        self.assertTrue(
            any("credential-like" in finding.message for finding in findings)
        )

    def test_broken_local_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[missing](docs/missing.md)\n", encoding="utf-8"
            )
            findings = VERIFY.validate_markdown_links(root)
        self.assertEqual(1, len(findings))
        self.assertIn("broken local Markdown link", findings[0].message)

    def test_candidate_cannot_be_answerable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            example_dir = root / "examples"
            example_dir.mkdir()
            payload = {
                "records": [
                    {
                        "record_id": "synthetic-unsafe-001",
                        "source_class": "candidate",
                        "answerable": True,
                        "citable": False,
                    }
                ]
            }
            (example_dir / "sample-records.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
            findings = VERIFY.validate_json_files(root)
        self.assertEqual(1, len(findings))
        self.assertIn("permissive policy", findings[0].message)

    def test_runtime_database_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.db").write_bytes(b"synthetic")
            findings, _ = VERIFY.scan_files(root)
        self.assertTrue(any("runtime" in finding.message for finding in findings))

    def test_license_is_required_for_final_gate(self) -> None:
        findings, _ = VERIFY.verify_repository(ROOT, require_license=True)
        self.assertFalse(
            any("approved license" in finding.message for finding in findings)
        )

        with tempfile.TemporaryDirectory() as directory:
            findings, _ = VERIFY.verify_repository(
                Path(directory), require_license=True
            )
        self.assertTrue(any("approved license" in item.message for item in findings))


if __name__ == "__main__":
    unittest.main()
