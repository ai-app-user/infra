"""Static guardrails for full-control VPS administration workflow."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class VpsAdminWorkflowTests(unittest.TestCase):
    def test_only_reviewed_script_is_executed(self):
        workflow = (ROOT / ".github/workflows/vps-admin.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("environment: vps-admin", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("github.actor == 'ai-app-user'", workflow)
        self.assertIn("ops/vps/admin/", workflow)
        self.assertIn("StrictHostKeyChecking=yes", workflow)
        self.assertIn("BatchMode=yes", workflow)
        self.assertIn("sudo -n bash -s", workflow)
        self.assertNotIn("pull_request:", workflow)

    def test_admin_diagnostics_is_read_only(self):
        script = (ROOT / "ops/vps/admin/diagnostics.sh").read_text()
        self.assertIn("set -euo pipefail", script)
        self.assertNotIn("apt install", script)
        self.assertNotIn("docker run", script)

if __name__ == "__main__":
    unittest.main()
