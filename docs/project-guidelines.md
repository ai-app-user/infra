# Common Project Guidelines

## Repository Layout

Prefer a predictable structure:

```text
README.md
docs/
scripts/
src/
tests/
config/
```

Keep generated build artifacts, datasets, logs, and secrets out of Git.

## Development Rules

- Keep reusable infrastructure separate from product/application-specific code.
- Prefer small, focused scripts under `scripts/` for repeatable operational tasks.
- Keep docs close to decisions: requirements, design, runbooks, and performance notes.
- Validate with local tests before pushing.
- Do not commit credentials, tokens, private keys, mounted data, or generated scan output.

## Testing

Each project should define:

- Unit tests for isolated logic.
- Integration tests for multi-component behavior.
- Functional tests for user-facing CLI/workflows.
- Performance tests where throughput is part of the product promise.

## Git Hygiene

- Inspect `git status --short` before committing.
- Review `git diff --stat` and suspicious generated files before staging.
- Prefer one coherent commit per logical change.
- Use branches for risky or exploratory work.

