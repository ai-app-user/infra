# One-request automatic private project bootstrap

A single approved request creates a private GitHub repository **and initializes
its shared development files** through GitHub Actions. Codex does not need
GitHub API connectivity, a second task, or a project-specific environment to
finish the standard scaffold.

## Secret setup (required)

Store `BOOTSTRAP_GITHUB_TOKEN` as a GitHub Actions repository secret in
`ai-app-user/infra`. The token needs repository creation permission **and
Contents: write** for newly created repositories under `ai-app-user`.
GitHub may require a classic token or GitHub App installation token if the
fine-grained token does not grant write access to future repositories. Never
put this token into a prompt, project request, repository, or log. Rotate it
before expiry.

## Submit one request

Using a clean checkout of infra/main, prepare a Git branch named
`bootstrap-requests/PROJECT_NAME` with only the request JSON:

```json
{"schema":1,"owner":"ai-app-user","name":"PROJECT_NAME","private":true}
```

Commit this as `bootstrap-request.json` and push the branch over Git HTTPS.
The *Bootstrap request signal* workflow runs without secrets. The privileged
*Bootstrap repository creation* workflow, running trusted code from infra/main,
then verifies the request, creates the private repository, generates its scaffold
using the canonical bootstrap CLI, and commits these files to its main branch:

- `README.md`
- `AGENTS.md`
- `docs/DEVELOPMENT.md`
- `.gitignore`
- `.project-bootstrap.json`

Use the latest accepted infra/main baseline. A separate Git push to populate
the new project is no longer necessary. The project README is a starting
template; Codex should fill in project-specific requirements in a subsequent
project-specific development task.

View the GitHub Actions workflow logs for the created repository URL, standards
version, and errors. Creation requests require explicit user authorization;
do not create real repositories merely for tests.

## Operational limitations

- New repositories are private. Only the designated owner is accepted.
- An existing project branch is never overwritten. Repeating a request leaves
  the repository unchanged. An interrupted first initialization may require
  review and repair before retrying.
- GitHub Actions is asynchronous; Cloud cannot always query the run when its
  network proxy fails. Do not claim completion until the GitHub run confirms it.
- The caller still needs enough Git HTTPS connectivity to push a request. If
  the Cloud proxy is down, the connected GitHub integration can create the same
  branch and JSON file.
- This does **not** install a global Codex skill or create a Codex Cloud
  environment. Those remain separate steps.

## Security

The unprivileged signal workflow receives no repository creation secret.
The privileged `workflow_run` job executes only trusted code checked out from
infra/main, never code from the request branch. It reads the exact triggering
commit's `bootstrap-request.json` as untrusted data, validates owner/name and
private visibility, and cannot be instructed to run arbitrary code.

The secret is only available to the trusted processing step. No permissions
are given to request-branch code. Creation uses the narrowest practicable
credential, and the target repository is never modified once it has a main
branch. Proxy, token, and access errors must be reported separately.
