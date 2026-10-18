import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bootstrap', ROOT / 'scripts/project-bootstrap.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.infra = self.root / 'infra'
        self.infra.mkdir()
        for name in ['standards.json', 'templates', 'docs']:
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.infra / name)
            else:
                shutil.copy2(source, self.infra / name)
        self.global_config = self.root / 'gitconfig'
        self.global_config.write_text('[user]\nname = Test\nemail = test@example.invalid\n')
        self.env = patch.dict(os.environ, {'GIT_CONFIG_GLOBAL': str(self.global_config),
                                          'GIT_CONFIG_NOSYSTEM': '1',
                                          'GIT_TERMINAL_PROMPT': '0'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.git(self.infra, 'init', '-b', 'main')
        self.commit()
        self.project = self.root / 'project'
        self.project.mkdir()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.calls = self.root / 'calls'
        self.remote_exists = self.root / 'exists'
        self.mode = self.root / 'mode'
        self.mode.write_text('ok')
        gh = self.bin / 'gh'
        gh.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
root = pathlib.Path(os.environ['FAKE_GH_ROOT'])
with (root / 'calls').open('a') as f: f.write(json.dumps(args) + '\\n')
mode = (root / 'mode').read_text()
if args[:2] == ['api', 'user']:
    if mode == 'authfail': sys.exit(1)
    print('test-user'); sys.exit(0)
if args[:2] == ['api', '--include']:
    if mode == 'lookupfail':
        print('HTTP/2 403 Forbidden'); sys.exit(1)
    if (root / 'exists').exists():
        print('HTTP/2 200 OK'); sys.exit(0)
    print('HTTP/2 404 Not Found'); sys.exit(1)
if args[:2] == ['repo', 'create']:
    if mode == 'createfail': sys.exit(1)
    (root / 'exists').touch(); sys.exit(0)
sys.exit(99)
''')
        gh.chmod(0o755)
        self.gh_env = patch.dict(os.environ, {'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                                             'FAKE_GH_ROOT': str(self.root)})
        self.gh_env.start()
        self.addCleanup(self.gh_env.stop)

    def git(self, cwd, *args):
        return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()

    def commit(self):
        self.git(self.infra, 'add', '.')
        self.git(self.infra, 'commit', '-m', 'Fixture standards')

    def sync(self, apply=True, adopt=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return b.sync(self.project, self.infra, apply, adopt)

    def change(self, relative, text):
        (self.infra / relative).write_text(text)
        manifest = json.loads((self.infra / 'standards.json').read_text())
        major, minor, patch = map(int, manifest['version'].split('.'))
        manifest['version'] = f'{major}.{minor + 1}.0'
        (self.infra / 'standards.json').write_text(json.dumps(manifest))
        self.commit()

    def snapshot(self):
        return {str(p.relative_to(self.project)): p.read_bytes()
                for p in self.project.rglob('*') if p.is_file()}

    def call_log(self):
        return [json.loads(s) for s in self.calls.read_text().splitlines()] if self.calls.exists() else []

    def test_preview_writes_nothing(self):
        self.sync(False)
        self.assertEqual(self.snapshot(), {})

    def test_create_and_repeat_are_identical(self):
        state = self.sync()
        self.assertEqual(state['version'], json.loads((self.infra / 'standards.json').read_text())['version'])
        self.assertTrue((self.project / 'docs/DEVELOPMENT.md').exists())
        self.assertTrue((self.project / 'docs/CODEX_CLOUD.md').exists())
        self.assertTrue((self.project / 'docs/VPS_ACCESS.md').exists())
        self.assertTrue((self.project / 'scripts/vps-ssh-check.sh').exists())
        self.assertEqual(state['commit'], self.git(self.infra, 'rev-parse', 'HEAD'))
        before = self.snapshot()
        self.sync()
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.calls.exists())

    def test_update_preserves_local_instructions(self):
        self.sync()
        agents = self.project / 'AGENTS.md'
        agents.write_text(agents.read_text() + '\nUse Python for this project.\n')
        source = self.infra / 'templates/project/AGENTS.md'
        self.change('templates/project/AGENTS.md', source.read_text().replace('# Project agent contract', '# Updated project agent contract'))
        self.sync()
        self.assertIn('Use Python for this project.', agents.read_text())
        self.assertIn('# Updated project agent contract', agents.read_text())
        before = self.snapshot()
        self.sync()
        self.assertEqual(before, self.snapshot())

    def test_conflict_aborts_all_writes(self):
        self.sync()
        local = self.project / 'README.md'
        local.write_text(local.read_text().replace('# Project', '# Local'))
        source = self.infra / 'templates/project/README.md'
        self.change('templates/project/README.md', source.read_text().replace('# Project', '# Incoming'))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            self.sync()
        self.assertEqual(before, self.snapshot())
        local.write_text(source.read_text())
        self.sync()
        self.assertEqual(json.loads((self.project / b.STATE).read_text())['version'], '1.4.0')

    def test_adoption_retains_existing_files(self):
        (self.project / 'README.md').write_text('My existing project\n')
        (self.project / 'AGENTS.md').write_text('Existing agent instructions\n')
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            self.sync()
        self.sync(adopt=True)
        self.assertEqual((self.project / 'README.md').read_text(), 'My existing project\n')
        self.assertEqual((self.project / 'AGENTS.md').read_text(), 'Existing agent instructions\n')
        self.sync()
        self.assertEqual((self.project / 'README.md').read_text(), 'My existing project\n')

    def test_local_deletion_preserved(self):
        self.sync()
        (self.project / 'README.md').unlink()
        self.sync()
        self.assertFalse((self.project / 'README.md').exists())

    def test_changed_upstream_deleted_locally_conflicts(self):
        self.sync()
        (self.project / 'README.md').unlink()
        self.change('templates/project/README.md', '# Changed\n')
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            self.sync()

    def test_upstream_removal(self):
        self.sync()
        manifest = json.loads((self.infra / 'standards.json').read_text())
        del manifest['templates']['README.md']
        (self.infra / 'standards.json').write_text(json.dumps(manifest))
        self.commit()
        self.sync()
        self.assertFalse((self.project / 'README.md').exists())

    def test_symlink_refused(self):
        outside = self.root / 'outside'
        outside.write_text('keep')
        (self.project / 'AGENTS.md').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.sync()
        self.assertEqual(outside.read_text(), 'keep')

    def test_path_traversal_in_state_refused(self):
        self.sync()
        state = json.loads((self.project / b.STATE).read_text())
        state['base_files']['../outside'] = 'bad'
        (self.project / b.STATE).write_text(json.dumps(state))
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            self.sync()

    def test_dirty_bundle_cannot_claim_a_commit(self):
        (self.infra / 'docs/security.md').write_text('Uncommitted policy')
        with self.assertRaisesRegex(ValueError, 'commit shared bundle'):
            self.sync()
        self.assertEqual(self.snapshot(), {})

    def test_downgrade_refused(self):
        self.sync()
        self.change('templates/project/README.md', '# Upgrade\n')
        self.sync()
        self.git(self.infra, 'checkout', 'HEAD~1')
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            self.sync()

    def test_auth_failure_no_local_or_remote_mutation(self):
        self.sync()
        self.mode.write_text('authfail')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'failed'):
            b.publish(self.project, 'owner', 'example')
        self.assertEqual(before, self.snapshot())
        self.assertEqual(len(self.call_log()), 1)
        self.assertFalse(self.remote_exists.exists())

    def test_lookup_failure_never_creates(self):
        self.sync()
        self.mode.write_text('lookupfail')
        with self.assertRaisesRegex(ValueError, 'lookup failed'):
            b.publish(self.project, 'owner', 'example')
        self.assertFalse(self.remote_exists.exists())
        self.assertFalse((self.project / '.git').exists())

    def test_creation_failure_stops_before_git_init(self):
        self.sync()
        self.mode.write_text('createfail')
        with self.assertRaisesRegex(ValueError, 'failed'):
            b.publish(self.project, 'owner', 'example')
        self.assertFalse((self.project / '.git').exists())

    def prepare_local_remote(self):
        remote = self.root / 'remote.git'
        remote.mkdir()
        self.git(remote, 'init', '--bare', '-b', 'main')
        # Exact GitHub remote is rewritten locally only inside the test configuration.
        with self.global_config.open('a') as handle:
            handle.write(f'[url "{remote}"]\n insteadOf = https://github.com/owner/example.git\n')
        return remote

    def test_publication_and_repeated_execution_with_local_push(self):
        self.sync()
        remote = self.prepare_local_remote()
        (self.project / '.env').write_text('SECRET=not-a-real-secret\n')
        (self.project / 'unreviewed.txt').write_text('do not stage\n')
        with contextlib.redirect_stdout(io.StringIO()):
            b.publish(self.project, 'owner', 'example')
            first = self.git(self.project, 'rev-parse', 'HEAD')
            b.publish(self.project, 'owner', 'example')
        self.assertEqual(first, self.git(self.project, 'rev-parse', 'HEAD'))
        self.assertEqual(first, self.git(remote, 'rev-parse', 'refs/heads/main'))
        tracked = self.git(self.project, 'ls-files').splitlines()
        self.assertIn(b.STATE, tracked)
        self.assertNotIn('.env', tracked)
        self.assertNotIn('unreviewed.txt', tracked)
        self.assertEqual(sum(c[:2] == ['repo', 'create'] for c in self.call_log()), 1)
        create = next(c for c in self.call_log() if c[:2] == ['repo', 'create'])
        self.assertIn('--private', create)

    def test_unrelated_origin_not_replaced(self):
        self.sync()
        self.git(self.project, 'init', '-b', 'main')
        self.git(self.project, 'remote', 'add', 'origin', 'https://github.com/other/repo.git')
        with self.assertRaisesRegex(ValueError, 'origin differs'):
            b.publish(self.project, 'owner', 'example')
        self.assertEqual(self.git(self.project, 'remote', 'get-url', 'origin'), 'https://github.com/other/repo.git')
        self.assertFalse(self.remote_exists.exists())

    def test_staged_changes_prevent_publication(self):
        self.sync()
        self.git(self.project, 'init', '-b', 'main')
        (self.project / 'local.txt').write_text('user work')
        self.git(self.project, 'add', 'local.txt')
        with self.assertRaisesRegex(ValueError, 'staged changes'):
            b.publish(self.project, 'owner', 'example')
        self.assertFalse(self.remote_exists.exists())

    def test_credential_path_in_state_is_rejected(self):
        self.sync()
        state = json.loads((self.project / b.STATE).read_text())
        state['base_files']['.env'] = 'never publish'
        (self.project / b.STATE).write_text(json.dumps(state))
        with self.assertRaisesRegex(ValueError, 'credential paths'):
            b.publish(self.project, 'owner', 'example')
        self.assertEqual(self.call_log(), [])

    def test_malformed_state_is_rejected(self):
        (self.project / b.STATE).write_text('[]')
        with self.assertRaisesRegex(ValueError, 'invalid state'):
            self.sync()

    def test_plugin_and_skill_package(self):
        manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        catalog = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(manifest['name'], 'project-bootstrap')
        portable = json.loads((ROOT / 'plugin.json').read_text())
        self.assertEqual(portable['name'], manifest['name'])
        self.assertEqual(portable['version'], manifest['version'])
        self.assertTrue((ROOT / portable['extensions']['com.openai']['onboardingSkill']).is_file())
        self.assertIn('GitHub', (ROOT / 'skills/project-bootstrap/SKILL.md').read_text().split('---')[1])
        self.assertTrue((ROOT / manifest['skills'] / 'project-bootstrap/SKILL.md').is_file())
        self.assertEqual(catalog['plugins'][0]['source']['path'], './')
        self.assertIn('name: project-bootstrap', (ROOT / 'skills/project-bootstrap/SKILL.md').read_text())

    def test_invalid_name_rejected_before_gh(self):
        with self.assertRaisesRegex(ValueError, 'invalid'):
            b.github_preflight('owner', '../bad')
        self.assertEqual(self.call_log(), [])

    def test_legacy_auth_failure_does_not_init(self):
        self.mode.write_text('authfail')
        result = subprocess.run(['bash', str(ROOT / 'scripts/new-github-project.sh'),
                                 '--owner', 'owner', '--repo', 'example', '--source', str(self.project)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.project / '.git').exists())
        self.assertFalse(self.remote_exists.exists())

    def test_cli_preview_and_create_repeat(self):
        target = self.root / 'new-project'
        command = ['python3', str(ROOT / 'scripts/project-bootstrap.py'), '--infra', str(self.infra),
                   'create', '--project', str(target)]
        subprocess.run(command, check=True, capture_output=True)
        self.assertFalse(target.exists())
        subprocess.run([*command, '--apply'], check=True, capture_output=True)
        before = (target / b.STATE).read_bytes()
        subprocess.run([*command, '--apply'], check=True, capture_output=True)
        self.assertEqual(before, (target / b.STATE).read_bytes())


if __name__ == '__main__':
    unittest.main()
