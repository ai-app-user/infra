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

## WSync Project Boundaries

Current sibling projects:

- `piper`: reusable pipeline infrastructure such as queues, buffer pools,
  generic jobs, monitoring, and autoscaling.
- `utils`: generic helper functions and small reusable algorithms, such as
  content hashing over bytes, with no pipeline, socket, filesystem, or product
  scenario semantics.
- `connector`: generic socket transport for opaque buffers and lengths,
  including TCP/Unix socket helpers and buffer sender/receiver jobs.
- `filer`: reusable filesystem I/O jobs and backend adapters such as
  metadata/data readers, target writers, NFS, and NULL backends.
- `hypersync`: product scenarios, CLI commands, profiler policy, scan/diff/copy
  and sync behavior, product configuration, and performance gates.

Workspace-level builds should include source roots in dependency order:

```text
piper/src -> utils/src -> connector/src -> filer/src -> hypersync/src
```

Do not move product scenario logic into `filer` just because it touches files;
`filer` owns backend mechanics, while `hypersync` owns scenario composition.

## Development Rules

- Use `dev` as the default working branch. Push normal iteration commits to
  `dev`; merge or push to `main` only when the maintainer explicitly asks for a
  main merge or release promotion.
- Keep reusable infrastructure separate from product/application-specific code.
- Prefer small, focused scripts under `scripts/` for repeatable operational tasks.
- Keep docs close to decisions: requirements, design, runbooks, and performance notes.
- Validate with local tests before pushing.
- Do not commit credentials, tokens, private keys, mounted data, or generated scan output.

## AI Session Context

Each project should keep AI session handoff context tracked in Git under
`doc/ai/`. If the project uses `docs/` as its documentation root, use
`docs/ai/` instead.

Required files:

- `chat.md`: concise timestamped conversation history with both User and Codex
  messages. Record decisions, requests, summaries of actions, and final
  outcomes. Do not paste huge command outputs.
- `kb.md`: durable handoff facts such as hosts, paths, commands, deployment
  locations, branch rules, benchmark baselines, operational state, important
  decisions, known failures, and current next steps. Keep it useful as
  future-session context, not as a raw transcript.
- `scripts/`: reusable scripts created or modified during AI sessions.

When the maintainer sends exactly `sync`, update `chat.md` and `kb.md` with the
latest conversation and current important facts, then commit and push those
context updates to `dev`.

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
