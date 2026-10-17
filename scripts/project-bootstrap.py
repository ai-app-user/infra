#!/usr/bin/env python3
"""Dependency-free, conservative project bootstrap. Never writes credentials."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

INFRA = Path(__file__).resolve().parents[1]
STATE = '.project-bootstrap.json'
REPOSITORY = 'https://github.com/ai-app-user/infra'


def run(args, cwd=None, check=True):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        # Authentication helpers may include sensitive diagnostics; do not echo output.
        raise ValueError(f'{args[0]} {args[1]} failed (exit {result.returncode}); check access/configuration')
    return result


def safe(root, name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or '..' in path.parts or
            any(p.lower() == '.git' for p in path.parts) or str(path) != name):
        raise ValueError(f'unsafe managed path: {name}')
    dest = root / name
    for node in [dest, *dest.parents]:
        if node == root.parent:
            break
        if node.is_symlink():
            raise ValueError(f'symlink refused: {name}')
    if dest.exists() and not dest.is_file():
        raise ValueError(f'not a regular file: {name}')
    return dest


def load_bundle(infra):
    manifest = json.loads((infra / 'standards.json').read_text())
    if not re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']):
        raise ValueError('invalid standards version')
    files = {}
    digest = hashlib.sha256()
    for target, source in sorted(manifest['templates'].items()):
        if target == STATE:
            raise ValueError('state cannot be a template')
        safe(infra, target)
        files[target] = safe(infra, source).read_text()
    for name in ['standards.json', *manifest['documents'], *manifest['templates'].values()]:
        digest.update(name.encode() + b'\0' + safe(infra, name).read_bytes() + b'\0')
    commit = run(['git', 'rev-parse', 'HEAD'], infra).stdout.strip()
    for name in ['standards.json', *manifest['documents'], *manifest['templates'].values()]:
        saved = run(['git', 'show', f'{commit}:{name}'], infra, False)
        if saved.returncode or saved.stdout != safe(infra, name).read_text():
            raise ValueError('commit shared bundle changes before distributing standards')
    return manifest['version'], commit, digest.hexdigest(), files


def merge(base, local, incoming):
    if local == base:
        return incoming
    if incoming == base or local == incoming:
        return local
    if base is None or local is None or incoming is None:
        raise ValueError('overlapping adoption, deletion, or modification')
    with tempfile.TemporaryDirectory(prefix='bootstrap-merge-') as temp:
        paths = []
        for name, content in [('local', local), ('base', base), ('incoming', incoming)]:
            path = Path(temp) / name
            path.write_text(content)
            paths.append(str(path))
        result = run(['git', 'merge-file', '-p', *paths], check=False)
        if result.returncode:
            raise ValueError('overlapping edits')
        return result.stdout


def sync(project, infra, apply=False, adopt_existing=False):
    if project.is_symlink():
        raise ValueError('project root must not be a symlink')
    project = project.resolve()
    if not project.is_dir():
        raise ValueError('project directory must exist')
    version, commit, digest, incoming = load_bundle(infra)
    state_path = safe(project, STATE)
    old = json.loads(state_path.read_text()) if state_path.exists() else None
    if old is not None and not isinstance(old, dict):
        raise ValueError('invalid state')
    if old is not None and (old.get('schema') != 1 or old.get('repository') != REPOSITORY):
        raise ValueError('unsupported state schema or infrastructure repository')
    if old and (not isinstance(old.get('version'), str) or
                not re.fullmatch(r'\d+\.\d+\.\d+', old['version'])):
        raise ValueError('invalid state version')
    previous = old['base_files'] if old else {}
    if not isinstance(previous, dict) or any(not isinstance(v, str) for v in previous.values()):
        raise ValueError('invalid baseline')
    if old and tuple(map(int, version.split('.'))) < tuple(map(int, old['version'].split('.'))):
        raise ValueError('standards downgrade refused')
    changes = {}
    preserved = []
    conflicts = []
    for name in sorted(set(previous) | set(incoming)):
        path = safe(project, name)
        local = path.read_text() if path.exists() else None
        if old is None and adopt_existing and local is not None and local != incoming.get(name):
            preserved.append(name)
            continue
        try:
            desired = merge(previous.get(name), local, incoming.get(name))
            if local != desired:
                changes[name] = desired
        except ValueError:
            conflicts.append(name)
    if conflicts:
        raise ValueError('conflicts (no files written): ' + ', '.join(conflicts) +
                         '; reconcile local files with templates, then retry')
    state = {'schema': 1, 'repository': REPOSITORY, 'version': version,
             'commit': commit, 'bundle_sha256': digest, 'base_files': incoming}
    state_text = json.dumps(state, indent=2, sort_keys=True) + '\n'
    if not state_path.exists() or state_path.read_text() != state_text:
        changes[STATE] = state_text
    print(json.dumps({'apply': apply, 'version': version, 'changes': sorted(changes), 'preserved': preserved}))
    if apply:
        # Plan and validate every path before writing. State is written last;
        # on interruption, rerun: unchanged incoming files merge idempotently.
        for name, content in changes.items():
            path = safe(project, name)
            if content is None:
                path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                fd, temp = tempfile.mkstemp(prefix='.bootstrap-', dir=path.parent)
                try:
                    with os.fdopen(fd, 'w') as handle:
                        handle.write(content)
                    if path.exists():
                        os.chmod(temp, path.stat().st_mode & 0o777)
                    os.replace(temp, path)
                finally:
                    if os.path.exists(temp):
                        os.unlink(temp)
    return state


def github_preflight(owner, repo):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', owner):
        raise ValueError('invalid GitHub owner')
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', repo) or repo in ('.', '..'):
        raise ValueError('invalid GitHub repository name')
    run(['gh', 'api', 'user', '--jq', '.login'])
    response = run(['gh', 'api', '--include', f'repos/{owner}/{repo}'], check=False)
    if not response.returncode:
        return True
    # gh's HTTP headers distinguish missing repositories from auth/network failures.
    if re.search(r'^HTTP/\S+ 404\b', response.stdout, re.M):
        return False
    raise ValueError('GitHub repository lookup failed; creation refused (check API network/authentication)')


def publish(project, owner, repo, public=False):
    project = project.resolve()
    state_path = safe(project, STATE)
    state = json.loads(state_path.read_text())
    if not isinstance(state, dict) or state.get('schema') != 1 or state.get('repository') != REPOSITORY:
        raise ValueError('adopt standards before publishing')
    if not isinstance(state.get('base_files'), dict):
        raise ValueError('invalid baseline')
    managed = [*state['base_files'], STATE]
    for name in managed:
        safe(project, name)
        if any(part.startswith('.env') or part.endswith(('.token', '.secret'))
               for part in PurePosixPath(name).parts):
            raise ValueError('credential paths must never be published')
    exists = github_preflight(owner, repo)
    remote = f'https://github.com/{owner}/{repo}.git'
    git_dir = project / '.git'
    if git_dir.exists():
        actual = run(['git', 'rev-parse', '--show-toplevel'], project).stdout.strip()
        if Path(actual).resolve() != project:
            raise ValueError('source must be a Git repository root')
        configured = run(['git', 'config', '--get', 'remote.origin.url'], project, False)
        if configured.returncode == 0 and configured.stdout.strip() != remote:
            raise ValueError('origin differs; refusing to replace it')
        if run(['git', 'diff', '--cached', '--name-only'], project).stdout.strip():
            raise ValueError('staged changes exist; commit or unstage them first')
    else:
        if run(['git', 'rev-parse', '--show-toplevel'], project, False).returncode == 0:
            raise ValueError('refusing to initialize inside another repository')
    for key in ('user.name', 'user.email'):
        if run(['git', 'config', '--get', key], project, False).returncode:
            raise ValueError(f'configure Git {key} before publishing')
    if not exists:
        run(['gh', 'repo', 'create', f'{owner}/{repo}', '--public' if public else '--private'])
    if not git_dir.exists():
        run(['git', 'init', '-b', 'main'], project)
    configured = run(['git', 'config', '--get', 'remote.origin.url'], project, False)
    if configured.returncode:
        run(['git', 'remote', 'add', 'origin', remote], project)
    run(['git', 'add', '--', *managed], project)
    if run(['git', 'diff', '--cached', '--quiet'], project, False).returncode:
        run(['git', 'commit', '-m', 'Adopt shared project infrastructure'], project)
    branch = run(['git', 'symbolic-ref', '--short', 'HEAD'], project).stdout.strip()
    run(['git', 'push', '-u', 'origin', branch], project)
    print(f'Published {owner}/{repo} ({branch}); only managed bootstrap files were staged')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--infra', type=Path, default=INFRA)
    subs = parser.add_subparsers(dest='command', required=True)
    for name in ('create', 'sync'):
        sub = subs.add_parser(name)
        sub.add_argument('--project', type=Path, required=True)
        sub.add_argument('--apply', action='store_true')
        if name == 'sync':
            sub.add_argument('--adopt-existing', action='store_true',
                             help='On first adoption, retain colliding files as local overrides')
    pub = subs.add_parser('publish', help='Explicit remote mutation; never used by offline tests')
    pub.add_argument('--project', type=Path, required=True)
    pub.add_argument('--owner', required=True)
    pub.add_argument('--repo', required=True)
    pub.add_argument('--public', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'publish':
            publish(args.project, args.owner, args.repo, args.public)
        else:
            if args.command == 'create':
                if args.project.is_symlink():
                    raise ValueError('symlink project refused')
                if args.project.exists() and any(args.project.iterdir()) and not (args.project / STATE).exists():
                    raise ValueError('create requires an empty directory; use sync for adoption')
                if args.apply:
                    args.project.mkdir(parents=True, exist_ok=True)
                elif not args.project.exists():
                    with tempfile.TemporaryDirectory() as temp:
                        sync(Path(temp), args.infra.resolve(), False)
                    return 0
            sync(args.project, args.infra.resolve(), args.apply, getattr(args, 'adopt_existing', False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'project-bootstrap: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
