# Changelog

## 1.2.0

- Include a Codex Cloud environment handoff guide in every project.
- Explain the supported first-time web/desktop setup, publishing, and cross-device use.
- Explicitly distinguish GitHub bootstrap automation from Codex Cloud environment provisioning.

## Plugin packaging update

- Add a portable root plugin manifest with an onboarding skill for supported personal installs.
- Clarify installation-scoped versus account-wide Codex Cloud discovery and improve automatic skill matching metadata.

## Pending — one-request repository bootstrap

- Make trusted GitHub Actions create and initialize the private project in one operation.
- Preserve existing repositories and report Contents:write permission failures explicitly.

## 1.1.0

- Expand the default AGENTS.md into a session-start, development, and shared-infra lifecycle contract.
- Add docs/DEVELOPMENT.md to every new project with engineering workflow, validation, and standards synchronization instructions.
- Make the project README an onboarding guide with links to requirements, testing, and global-infra improvement workflows.
- Clarify when reusable improvements are proposed, when infra PRs require approval, and how updates reach existing projects.

## 1.0.0

- Add the canonical project-bootstrap skill and skill-only plugin package.
- Add reference-based standards, local scaffolding, explicit GitHub publication,
  versioned adoption, and conservative three-way upgrades.
- Document reviewable global improvements and Cloud activation limitations.
- Add offline functional tests; no real GitHub repositories are created by tests.
