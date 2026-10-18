# Project

Describe what this project does, who uses it, and its intended outcome.
Replace this placeholder with actual requirements and links to design decisions
before treating the bootstrap as a completed product.

## Getting started

Document prerequisites, setup, configuration, local execution, and build
commands for this project. Do not put credentials or tokens in this file.

## Validation

Document how to run the project's tests, lint/type checks, and CI. Record
relevant acceptance and performance criteria as they are established.

## Architecture and operations

Link project-specific designs, decisions, deployment, observability, and
recovery procedures when applicable.

## Working in Codex Cloud

For first-time Cloud environment setup, see [docs/CODEX_CLOUD.md](docs/CODEX_CLOUD.md).
Once published, the project environment can be selected from a computer or phone.
The GitHub repository is bootstrapped automatically; the Codex environment still
requires the supported web/desktop creation and publication flow.

## VPS hosting (optional)

For approved VPS access and deployment setup, read
[docs/VPS_ACCESS.md](docs/VPS_ACCESS.md). It explains SSH key enrollment,
project-isolated deployment credentials, and a read-only connectivity check.
The repository does not contain SSH private keys or grant server access by itself.

## Autonomous development

The default Codex delivery policy is in [docs/AUTONOMY.md](docs/AUTONOMY.md).
Routine authorized work should move from implementation through passing tests,
automatic merging, and requested deployment without manual PR clicks. This
requires applicable GitHub permissions and real deployment automation; it does
not imply that Codex runs after its task ends.

## AI development and shared infrastructure

**Start with [AGENTS.md](AGENTS.md)** for the agent contract and
[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the development workflow.

This project adopts the shared standards from
[ai-app-user/infra](https://github.com/ai-app-user/infra).
The exact adopted version and commit are recorded in `.project-bootstrap.json`.
The authoritative engineering/security policies remain in infra; this project
does not maintain independent copies.

For standards updates, ask Codex: **"Check this project's infra standards and
propose an update."** For a reusable practice discovered here, ask:
**"Propose making this improvement part of global infra."** Both operations
should produce reviewable changes, not silently rewrite shared policy.
