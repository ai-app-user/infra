# Open this project in Codex Cloud

This repository was bootstrapped using [ai-app-user/infra](https://github.com/ai-app-user/infra).
For development in a browser, on another computer, or on mobile, use a
**repository-backed Codex Cloud environment**.

## First-time environment setup (web or desktop)

1. Open [Codex Cloud](https://chatgpt.com/codex) using your ChatGPT account.
2. Start a new task and choose **Cloud → Select environment → Create environment**.
3. Select **this repository** from the connected GitHub repositories, on its
   default `main` branch. Do not select `infra` when working on this project.
4. Ask Codex to inspect `README.md`, `AGENTS.md`,
   `docs/DEVELOPMENT.md`, and `.project-bootstrap.json`. It should determine
   install and startup commands from the project's actual dependencies.
   Do not install tools or create services that the project does not need.
5. Confirm that Git operations work; test Git HTTPS separately from GitHub API
   access. Keep internet access restricted to necessary domains. Never paste
   tokens into chat or commit secrets.
6. Review any generated install/start scripts and test results. Resolve
   outstanding setup problems, then **Publish** the environment through the UI.
7. Open a **new Cloud task** using that published environment, and ask Codex to
   summarize this project's instructions and run an appropriate read-only check.

## Subsequent work from any device

Select the previously published project environment in Codex Cloud. A new
task gets its own workspace; it does not depend on your original laptop or
terminal. The Project Bootstrap personal plugin may be available in the
account, but its presence in every new session must be verified.

**On mobile:** select the already published project environment. First-time
environment creation may require web or desktop.

## What is and is not automated

The GitHub Actions bootstrap creates the **GitHub repository and its files**.
It does **not** create or publish a ChatGPT Codex Cloud environment. As of the
documented product interface, repository-backed Cloud environment creation
still requires the web/desktop setup and publish flow. Do not claim otherwise
or use private/undocumented APIs.

The separate OpenAI Agents API hosted environment endpoint is not a
replacement for a repository-backed Codex Cloud environment in ChatGPT.

If no environment exists yet, give the user this repository's GitHub URL and
these setup steps. Once published, the user can resume from their phone.

## Troubleshooting

- If the repository is missing from the picker, verify GitHub integration
  access to this specific private repository.
- A failing GitHub API call is not evidence that Git HTTPS fails (or vice versa).
- If Save/Publish reports an error, do not claim the environment is ready.
  Preserve the repository and report the setup issue.
- The authoritative development rules remain in `AGENTS.md` and the
  version-pinned shared infra; environment setup must not duplicate standards.
