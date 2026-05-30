# Portable Codex Project Bootstrap Prompt

Copy the prompt below into a new Codex project when you want Codex to set up
the project structure, GitHub workflow, reusable project dependencies, AI
session memory, documentation, testing, and ongoing development rules.

Replace values in angle brackets before sending.

```text
You are working in a new or existing software project named <PROJECT_NAME>.
Your job is to initialize or repair the project so it follows the common
WSync/Codex project standards below. Make the changes directly, verify them,
and commit/push to the `dev` branch when complete.

Project facts:
- Project name: <PROJECT_NAME>
- GitHub owner/org: <GITHUB_OWNER>
- GitHub repository URL: https://github.com/<GITHUB_OWNER>/<PROJECT_NAME>.git
- Primary language/runtime: <LANGUAGE_OR_STACK>
- Product purpose: <ONE_OR_TWO_SENTENCE_PURPOSE>
- Documentation root preference: <doc OR docs>
- Version policy: use `x.y.z.<build>` development builds on `dev`; increment
  the build number on every dev iteration commit.
- Related reusable sibling projects to include or reference:
  - `infra`: common project guidelines, GitHub setup, security rules, reusable
    scripts, and shared process documentation.
  - `piper`: reusable asynchronous pipeline infrastructure such as buffer
    pools, buffer queues, generic jobs, monitoring, and autoscaling.
  - `utils`: generic helper functions and small reusable algorithms. It must
    not know product scenarios, sockets, filesystem metadata, NFS, or DB output.
  - `connector`: generic socket transport for opaque buffers and lengths.
  - `filer`: reusable filesystem I/O jobs and backend adapters.

Core instructions:

1. Inspect the current repository first.
   - Run `pwd`, `git status --short`, `git branch --show-current`, and list the
     top-level files.
   - Do not overwrite user work. If the tree has unrelated dirty files, preserve
     them and work around them.
   - If no Git repository exists, initialize one.

2. Set up GitHub and branches.
   - Ensure the default working branch is `dev`.
   - If needed, create `dev` from the current branch.
   - Configure `origin` as `https://github.com/<GITHUB_OWNER>/<PROJECT_NAME>.git`
     if no correct remote exists.
   - Do not push to `main` unless explicitly asked.
   - Push normal iteration commits to `dev`.
   - Do not store GitHub tokens, private keys, `.env` files, credentials, or
     generated datasets in the repo.
   - Prefer `gh auth login` / existing `gh` auth. If a token is needed, accept
     it only through environment variables or stdin; never write it to files.

3. Create or normalize the folder structure.
   Use this baseline unless the project already has an established equivalent:
   ```text
   README.md
   doc/                  # or docs/ if the project already uses docs/
   doc/requirement.md
   doc/ux.md
   doc/design.md
   doc/testing.md
   doc/performance.md    # if performance matters
   doc/guidlines.md      # keep this spelling if matching WSync repos
   doc/ai/chat.md
   doc/ai/kb.md
   doc/ai/scripts/
   scripts/
   src/
   tests/
   config/
   build/                # generated only; ignored by Git
   ```
   If this is a library with multiple components, use the same documentation
   shape inside each project boundary.

4. Add `.gitignore`.
   Include generated build output, caches, logs, temporary files, coverage
   output, local env files, packaged artifacts, and large generated data:
   `build/`, `dist/`, `coverage/`, `*.gcda`, `*.gcno`, `*.log`, `.env`,
   `.DS_Store`, temporary benchmark outputs, generated CSV/Parquet inventories,
   and language-specific cache folders.

5. Add common documentation.
   - `README.md`: project purpose, quick start, build, test, run, and links to
     docs.
   - `doc/requirement.md`: what must be true, what is implemented, partial, and
     not started.
   - `doc/ux.md`: user-facing install/config/run flow.
   - `doc/design.md`: architecture, project boundaries, data flow, tradeoffs,
     pipeline/job/scenario vocabulary if applicable.
   - `doc/testing.md`: how to run unit, integration, functional, and performance
     tests.
   - `doc/performance.md`: benchmark commands, workload shape, expected metrics,
     and known good baselines if throughput matters.
   - `doc/guidlines.md`: durable development rules from this prompt.
   - `doc/ai/chat.md`: create a timestamped first entry summarizing this setup.
   - `doc/ai/kb.md`: record durable facts: repo URL, branch rules, build/test
     commands, version policy, related projects, and current next steps.
   - `doc/ai/scripts/`: create the folder even if empty; add reusable scripts
     here when future AI sessions need repeatable operations.

6. Implement `sync` behavior as a standing rule.
   When the maintainer sends exactly `sync`, update:
   - `doc/ai/chat.md` with concise timestamped User/Codex conversation history,
     decisions, actions, and outcomes.
   - `doc/ai/kb.md` with durable handoff facts, commands, paths, known issues,
     benchmark baselines, deployment state, and next steps.
   Then commit and push those context updates to `dev`.

7. Add versioning.
   - Add a version source file or equivalent for <LANGUAGE_OR_STACK>.
   - Start at `<INITIAL_VERSION>` if provided, otherwise `0.0.1.1`.
   - Ensure the application/library can report its version if it has a CLI.
   - On every `dev` iteration commit, bump the final build number:
     `0.0.1.1` -> `0.0.1.2` -> `0.0.1.3`.
   - Update version smoke tests in the same commit.

8. Add build and test entry points.
   - Provide one obvious build command and one obvious test command.
   - Add unit tests for shared utilities, parsers, formats, and data structures.
   - Add integration tests where multiple components interact.
   - Add functional tests for user-facing CLI/workflows.
   - Add performance tests only when throughput/latency is part of the product
     promise; record workload, duration, concurrency, source/target type, and
     metrics.
   - Tests must be deterministic by default and should not require external
     services unless explicitly marked.
   - Test binaries or scripts should support listing tests and selecting tests
     by stable id or name substring where practical.

9. Reusable project dependency model.
   If this project is part of the WSync-style multi-repo workspace, arrange the
   source include/build order as:
   ```text
   piper/src -> utils/src -> connector/src -> filer/src -> <PROJECT_NAME>/src
   ```
   Use only the projects that are relevant:
   - Put generic pipeline mechanics in `piper`, not the product.
   - Put primitive reusable algorithms in `utils`.
   - Put opaque buffer socket transport in `connector`.
   - Put filesystem backend mechanics in `filer`.
   - Keep product scenarios, CLI commands, profiler policy, and use-case
     composition inside the main project.
   Do not move product scenario logic into a reusable project just because it
   touches that domain.

10. Pipeline/job architecture rules, if the project uses pipelines.
    - Use `[JobName-N/options]` for concrete jobs.
    - Use `(QueueName-N/options)` for concrete queues. If `N` could mean depth,
      shard count, or lane count, state which.
    - Use `{PipelineName}` for reusable pipeline blocks with declared inputs,
      outputs, configuration, and variations.
    - Use `{{ScenarioName}}` for full user-facing or benchmark scenarios
      composed from pipelines, jobs, and queues.
    - Jobs may have zero, one, or multiple input queues and zero, one, or
      multiple output queues.
    - Jobs must not know which job produced their input or consumes their output.
    - Prefer opaque buffers and ownership transfer between jobs.
    - Hot-path queues should carry buffer handles, not strings, vectors, records,
      or data bytes.
    - Do not use `std::any` / type-erased message queues as a production
      pipeline edge.
    - Generic discard/sink behavior should use a generic buffer discarder, not a
      record-specific sink.

11. Buffer/data rules, if the project moves buffers.
    - Preallocate high-volume payload buffers once and reuse them until exit.
    - Do not allocate/free per chunk in steady-state hot paths.
    - Move buffer ownership between jobs; do not copy payload bytes through queue
      messages.
    - Treat buffer payloads as byte wire formats. Use structured copy helpers
      such as `memcpy`; do not reinterpret byte arrays as aligned C++ structs.
    - If buffers need self-description, use a trailer/footer format:
      final 2 bytes magic, 2 bytes before that metadata size including magic,
      2 bytes before that metadata version, and 4 bytes before that logical data
      size.
    - Metadata may include checksum algorithm, data checksum, metadata checksum,
      and packed sub-buffer descriptors.
    - `checksum_algorithm=none` or checksum value `0` means checksum is not used.

12. Configuration rules.
    - Every operationally important limit should be configurable.
    - Command-line values override config file values.
    - Defaults should be conservative and safe for local tests.
    - High-throughput settings must be explicit and visible in summaries.
    - Config errors should fail early with clear messages.

13. Security rules.
    - Never commit secrets, private keys, tokens, `.env`, generated customer data,
      large datasets, or local-only configs.
    - Public keys may be listed or fingerprinted; private keys must not be
      printed or copied.
    - Use the smallest practical GitHub token scope.

14. Implement the initial scaffold.
    - Create missing folders/files.
    - Add or update build/test scripts.
    - Add or update docs.
    - Add a minimal working source/test example for <LANGUAGE_OR_STACK>.
    - Run formatting if the project has a formatter.
    - Run tests.

15. Commit and push.
    - Run `git status --short` and inspect `git diff --stat`.
    - Do not stage generated build outputs or secrets.
    - Commit one coherent setup change to `dev`.
    - Push `dev` to GitHub.
    - Final response must include:
      - Files created/changed.
      - Build/test commands run and results.
      - Git branch, commit hash, and remote pushed.
      - Any assumptions or skipped items.
```

## Short Variant

Use this when the project already exists and you only want Codex to align it:

```text
Align this repository with the common WSync/Codex project standards. Inspect the
repo first, preserve user changes, use `dev` as the working branch, configure
GitHub origin if missing, create/update README, doc/requirement.md, doc/ux.md,
doc/design.md, doc/testing.md, doc/guidlines.md, doc/ai/chat.md,
doc/ai/kb.md, doc/ai/scripts/, .gitignore, build/test scripts, versioning
with `x.y.z.<build>`, and local tests. Add `sync` behavior: when I send exactly
`sync`, update doc/ai/chat.md and doc/ai/kb.md, then commit and push to `dev`.
Keep reusable code boundaries clear: infra for process docs, piper for generic
pipeline infrastructure, utils for generic algorithms, connector for opaque
buffer transport, filer for filesystem backend mechanics, and this project for
product scenarios and CLI. Verify everything, commit, push `dev`, and report
files changed, tests run, commit hash, and assumptions.
```
