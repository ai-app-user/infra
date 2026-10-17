"""Offline tests for the privileged request validation (no GitHub API calls)."""
import importlib.util
from pathlib import Path
import unittest

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


if __name__ == "__main__":
    unittest.main()
