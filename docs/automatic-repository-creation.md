# Automatic repository creation from Codex Cloud

Codex Cloud can submit a Git HTTPS push, even when its GitHub API access is blocked.
GitHub Actions performs repository creation on GitHub's infrastructure.

## Required setup

In `infra` GitHub Actions secrets, configure `BOOTSTRAP_GITHUB_TOKEN` with a
fine-grained token belonging to `ai-app-user` and the **Repository creation:
Write** permission. Rotate it before expiration.

## Request creation

From a clean checkout of `ai-app-user/infra` at latest `origin/main`:

1. Create branch `bootstrap-requests/PROJECT_NAME` (use a new repository name).
2. Commit ONLY a file named `bootstrap-request.json` in the repository root
   containing `{"schema":1,"owner":"ai-app-user","name":"PROJECT_NAME","private":true}`.
3. Push the branch using Git HTTPS. Never put credentials into the request.
4. GitHub Actions runs **Bootstrap request signal**, then **Bootstrap repository
   creation**. The second workflow prints the private repository URL.
5. Scaffold the project using `skills/project-bootstrap/SKILL.md`; then use
   ordinary Git HTTPS commands to initialize, commit, and push to the new remote.

Do not call `gh repo create` or `gh api` from Codex Cloud for this route.
Never create real test repositories without explicit user approval.

## Security

The signal workflow has no secrets. The privileged `workflow_run` workflow
executes only trusted code from `infra/main`, and never checks out or executes
request-branch code. It fetches a single request file **as data** from the exact
triggering commit SHA, validates its schema, owner, privacy, and name, and only
accepts pushes by `ai-app-user`. It creates private repositories only and
never modifies an existing repository. Repeat requests are idempotent.

If a request fails, inspect the Actions run. An HTTP 403/422 from creation can
mean the secret's permissions or account policy is insufficient; it does not
establish a Codex Cloud networking problem.
