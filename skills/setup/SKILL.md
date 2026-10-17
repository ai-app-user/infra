---
name: setup-project-bootstrap
description: Check readiness and explain how to use the project-bootstrap plugin to create and maintain GitHub projects; never create a repository during setup.
---

# Set up Project Bootstrap

This is a non-mutating onboarding check. Do not request credentials in chat.

1. Confirm whether the `project-bootstrap` skill appears among the available skills in this installation. Installing this plugin does not prove it appears in every Codex Cloud session.
2. Explain that the shared rules live at `https://github.com/ai-app-user/infra`, and the canonical skill is `skills/project-bootstrap/SKILL.md`.
3. If the session can access the repository, read its `standards.json` and report the version; otherwise explain the missing permission or network capability without guessing.
4. Give two example prompts: "Create a private GitHub project called X using my standard infrastructure" and "Update this project to the latest infra standards."
5. Explain that repository creation must be explicitly authorized, and will use the GitHub Actions request workflow when direct API access is blocked. Do not create or modify repositories as part of setup.
6. Clarify which capability is actually verified (this installation, new Cloud session, other device); do not claim global availability without cross-session testing.
