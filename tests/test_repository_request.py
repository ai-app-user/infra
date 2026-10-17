"""Offline tests for the privileged request validation (no GitHub API calls)."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "process-repo-request.py"
spec = importlib.util.spec_from_file_location("bootstrap_request", SOURCE)
processor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(processor)


class RepositoryRequestTests(unittest.TestCase):
    def valid(self):
        return {"schema": 1, "owner": "ai-app-user", "name": "demo", "private": True}

    def test_valid_private_request(self):
        self.assertEqual(processor.validate(self.valid(), "bootstrap-requests/demo"), "demo")

    def test_public_rejected(self):
        req = self.valid()
        req["private"] = False
        with self.assertRaises(ValueError):
            processor.validate(req, "bootstrap-requests/demo")

    def test_other_owner_rejected(self):
        req = self.valid()
        req["owner"] = "someone-else"
        with self.assertRaises(ValueError):
            processor.validate(req, "bootstrap-requests/demo")

    def test_wrong_branch_rejected(self):
        with self.assertRaises(ValueError):
            processor.validate(self.valid(), "bootstrap-requests/other")

    def test_extra_field_rejected(self):
        req = self.valid()
        req["command"] = "anything"
        with self.assertRaises(ValueError):
            processor.validate(req, "bootstrap-requests/demo")

    def test_bad_repository_name_rejected(self):
        for name in ("../demo", "hello world", "a/b", "."):
            req = self.valid()
            req["name"] = name
            with self.subTest(name=name), self.assertRaises(ValueError):
                processor.validate(req, "bootstrap-requests/" + name)

    def test_scaffold_install_only_into_empty_repo(self):
        calls = []
        def fake_api(token, endpoint, method="GET", data=None):
            calls.append((method, endpoint, data))
            if "/git/ref/heads/main" in endpoint:
                return 404, None
            return 201, {}
        files = {"README.md": b"# Test", "AGENTS.md": b"Rules",
                 ".project-bootstrap.json": b'{"version":"1.1.0"}'}
        with patch.object(processor, "api", side_effect=fake_api):
            self.assertTrue(processor.install_scaffold("synthetic", "demo", files))
        self.assertEqual([c[0] for c in calls], ["GET", "PUT", "PUT", "PUT"])
        self.assertIn("/contents/README.md", calls[1][1])
        self.assertEqual(calls[1][2]["branch"], "main")

    def test_existing_project_is_never_overwritten(self):
        with patch.object(processor, "api", return_value=(200, {})) as fake_api:
            self.assertFalse(processor.install_scaffold("synthetic", "demo",
                                                         {"README.md": b"new"}))
        self.assertEqual(fake_api.call_count, 1)

    def test_write_permission_failure_is_reported(self):
        def fake_api(token, endpoint, method="GET", data=None):
            return (404, None) if method == "GET" else (403, None)
        with patch.object(processor, "api", side_effect=fake_api):
            with self.assertRaisesRegex(ValueError, "Contents:write"):
                processor.install_scaffold("synthetic", "demo", {"README.md": b"test"})

    def test_generated_scaffold_contains_workflow(self):
        # Tests run from a checked-out repository, so its manifest is committed.
        state, files = processor.scaffold()
        self.assertEqual(state["version"], "1.1.0")
        self.assertIn("docs/DEVELOPMENT.md", files)
        self.assertIn(b"Start of a session", files["AGENTS.md"])


if __name__ == "__main__":
    unittest.main()
