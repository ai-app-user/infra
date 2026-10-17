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
