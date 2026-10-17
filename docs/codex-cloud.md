# Installing Project Bootstrap across Codex sessions

The source of truth is https://github.com/ai-app-user/infra. The skill is
`skills/project-bootstrap/SKILL.md` and the distributable plugin is the
repository root, with its portable `plugin.json` manifest. The previous
`.codex-plugin/plugin.json` is retained as a compatibility fallback.

**What this solves:** After installation on a supported surface, the
`project-bootstrap` skill is advertised to the model, and requests for new
GitHub projects or standards upgrades can activate it without explicitly
naming SKILL.md. The description is designed for those intents.

**What it does not prove:** Putting files in GitHub does not install a plugin
in an account. A Codex CLI/desktop installation is not evidence that a
new Codex Cloud browser task on another device will discover it.
Repository creation also requires permissions and an explicit user request.

## Try the account's Plugins directory

Open ChatGPT/Codex Plugins and check whether your account exposes a **Personal**
plugin or a way to add a custom GitHub marketplace. If supported, add
`https://github.com/ai-app-user/infra`, install `project-bootstrap`, and
run its onboarding skill. Don't assume these controls exist in every
account or browser surface.

For Codex CLI, official documentation supports registering the GitHub
marketplace with:

```bash
codex plugin marketplace add ai-app-user/infra
codex plugin marketplace list
```

Then open `/plugins`, install `project-bootstrap`, and start a new session.
This is installation-scoped. Do not assume it syncs to Codex Cloud.

For supported ChatGPT desktop installs, the repo's catalog is at
`.agents/plugins/marketplace.json`. The catalog is repo-scoped and refers
to the plugin at `./`. Where a local marketplace is exposed in the desktop
Plugins Directory, install from that source.

Sources:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://help.openai.com/en/articles/20001256-plugins-in-codex/

## Verify discovery rather than guessing

1. In a fresh session with the plugin installed, ask: "What project bootstrap
   skills are available?" Confirm it is explicitly listed.
2. Without saying its name or path, ask: "How would you create a private GitHub
   project using my standard infrastructure? Preview only." Confirm Codex
   identifies the correct shared repository and workflow.
3. Repeat in a fresh Codex Cloud browser task with no selected infra checkout,
   if your account supports it, and from another device. Only mark cross-device
   availability as working when those tests succeed.
4. Creation is a write operation. For a live test, ask permission first and
   verify the remote files and GitHub Actions status.

## Reliable fallback (no personal install required)

Start a Codex Cloud task with the existing `infra` environment. Ask it to
read `skills/project-bootstrap/SKILL.md` from the checked-out repository and
use `docs/automatic-repository-creation.md` for new private repositories.
The latter submits a validated Git branch request and GitHub Actions creates
and initializes the repository, even when the Cloud API is unavailable.
Git HTTPS proxy failures can still stop task submission; the connected GitHub
integration can submit the same request.

For an adopted project, `AGENTS.md` and `.project-bootstrap.json` reference
the exact pinned infra version. Those references are project instructions,
not proof of account-wide plugin installation.

## Credential and access boundaries

Never copy tokens into skills, requests or chat. Keep the GitHub Actions secret
`BOOTSTRAP_GITHUB_TOKEN` restricted; new-project initialization needs both
repository creation and Contents:write permissions. Project creation always
requires user authorization. Changes to global infra require reviewed PRs.
