# Codex Cloud activation and its limits

## What was verified

On 2026-10-17, the official `openai/skills` README directs new skill authors to
skill-only plugins. Official `openai/plugins` examples use a
`.codex-plugin/plugin.json` manifest with a `skills` directory and an
`.agents/plugins/marketplace.json` catalog. This repo follows that structure:
its root is the plugin, and `skills/project-bootstrap/SKILL.md` is canonical.
There is no second copy of the skill in the catalog or projects.

Sources inspected:

- https://github.com/openai/skills/blob/main/README.md
- https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md
- https://github.com/openai/plugins/blob/main/README.md
- https://github.com/openai/plugins/blob/main/.agents/plugins/marketplace.json
- https://github.com/openai/plugins/blob/main/plugins/remotion/.codex-plugin/plugin.json
- Current product guide: https://developers.openai.com/codex/plugins/build

The developer website was blocked by this environment's network policy, so its
current Cloud installation instructions could not be verified. The legacy
installer explicitly targets `$CODEX_HOME/skills` (default `~/.codex/skills`);
that is installation-scoped, not proof of account-wide Cloud synchronization.
No custom-plugin installation tool is exposed in this session, and no account
installation or repository-free cross-device discovery was tested. The package
is implemented; global Cloud activation is **not** claimed.

## Activating the plugin where supported

First merge/push this implementation to the infra branch you intend to use.
The local work in this task is not automatically present in GitHub.

If your Codex Cloud account supports adding custom GitHub plugin marketplaces,
use the repository URL `https://github.com/ai-app-user/infra` and its catalog
`.agents/plugins/marketplace.json`, then install `project-bootstrap`. This is the
package location, not a claim that a particular Cloud menu exists. Follow the
current product guide for the installation surface your account exposes.

Verify activation in a **new Cloud conversation with no project selected**:
check that project-bootstrap appears among available skills/plugins, request a
local-only scaffold, and verify its reported infra commit and generated files.
Repeat from another device using the same account. Until both checks pass, do
not assume installation follows your account. A workspace link, repository
checkout, or published environment alone does not establish global discovery.

If custom marketplaces are unavailable, there is no verified one-time global
activation procedure from this task. Use the following explicit-fetch workflow.

## Reliable fallback: repository-free explicit fetch

Start a Codex Cloud session that has a shell, outbound Git HTTPS access, and
permission to read ai-app-user/infra. No project checkout needs to be selected.
Paste this instruction (replace X):

> Fetch https://github.com/ai-app-user/infra using existing HTTPS authentication
> into a clean temporary directory. Read skills/project-bootstrap/SKILL.md there
> and follow it to create a new project called X using my standard infrastructure.
> Default to private. Explain any missing API access. Do not claim the skill is
> globally installed.

The agent can use these commands; keep the returned path for subsequent steps:

```bash
infra_checkout=$(mktemp -d /tmp/project-infra.XXXXXXXX)
git clone -- https://github.com/ai-app-user/infra.git "$infra_checkout"
cat "$infra_checkout/skills/project-bootstrap/SKILL.md"
```

Fetching does not require a local computer, SSH key, or token copied from your
phone. It does require the Cloud session's scoped Git permission for infra. If
the product cannot start a shell-backed task with no repository selected, this
fallback cannot remove that product limitation: start a task in the shared infra
environment instead, then create the project in a separate directory. This
closest alternative selects infra rather than an existing project repository.

After installation is actually verified, the shorter prompt “Create a new
project called X using my standard infrastructure” can route through the skill.
Before that, the short phrase alone has no guaranteed connection to this repo.
An account-level instruction, if your product offers one, can retain the fetch
request as a convenience, but its availability and automatic execution are not
verified here.

For an existing adopted project, AGENTS.md points at infra. Use “Update this
project to my latest standards” or “Make this improvement part of my global
infrastructure.” Projects with a preexisting AGENTS.md need the reference added
with review on first adoption. These references enable contextual discovery;
they do not install a global skill.

## Network and authentication

Allow `github.com` for Git HTTPS and `api.github.com` for gh API operations;
GitHub asset domains may also be required by your proxy. Reuse injected Git/gh
authentication. Test `git ls-remote` separately from `gh api user --jq .login`.
A Git proxy read does not imply API access or create/push permissions. Never
commit tokens, install a personal SSH key, or ask for credentials in chat.
If credentials truly remain missing, use the product's secure settings flow.

An earlier API test was blocked with HTTP 403 by the proxy. On the final live
read-only recheck, gh API authentication succeeded as ai-app-user. This does not
establish create, PR, push, or cross-device permissions; no remote writes were
performed during validation.


## Short activation guide

1. Review and merge the project-bootstrap pull request into infra main. Until
   then, explicitly use its feature branch when trying the skill.
2. From any computer or phone, sign into the same Codex account and start a
   Cloud task using the shared **infra environment**. This avoids depending on
   a repository-free task or an account-wide custom skill installation.
3. Say: “Read skills/project-bootstrap/SKILL.md in ai-app-user/infra and use it
   to create project X. First preview the plan; do not create a GitHub repository
   until I request publication.”
4. Codex should use the existing infra checkout, apply shared references in a
   separate project directory, and report the adopted version and commit.
5. When you want real publication, request it explicitly. Codex checks API access
   and uses existing cloud authentication; no local SSH keys are required.
6. For adopted projects, request an update or global improvement using the
   canonical skill. Both workflows propose reviewable PRs.

If your account can start shell-backed Cloud tasks with no repository selected,
the explicit-fetch prompt above also works without selecting infra first.
Neither path proves account-wide installation. Only treat the shorter implicit
prompt as supported after the skill appears in a fresh session's available list.

During finalization, API access again failed at the proxy CONNECT step with
HTTP 403, even though the saved environment policy includes api.github.com.
Git reads still succeeded. Refresh/apply the environment's network settings or
restart the environment and retest API access before changing credentials; the
observed proxy rejection does not establish a GitHub token or permission error.
