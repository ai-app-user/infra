# Security Rules

## Tokens

- Do not store GitHub tokens in repos, scripts, shell history, or docs.
- Prefer `gh auth login` storing credentials in the OS keyring.
- For automation, pass tokens through environment variables or stdin.

## SSH Keys

- Public keys may be listed or fingerprinted.
- Private keys must never be printed, copied into repos, or shared in logs.

## Shared VPS deployment

- Authorize access per person/project; do not make production VPS administration
  available to anyone simply because they can read an infra repository.
- Use per-project deploy identities with minimum filesystem/service permissions.
- Prefer key-based SSH with verified host keys. Do not bypass SSH host checking.
- Store CI deploy keys only in protected, appropriately scoped secret stores;
  never include passwords or private keys in project files or Codex prompts.
- Deploy only reviewed project-specific commands, with health checks and rollback;
  do not offer a generic arbitrary-command executor with a production key.

## GitHub Permissions

For private repositories, use tokens with the smallest practical scope. The
classic token scope usually needed for full private repo automation is `repo`.

## Project Data

Do not commit:

- Build directories.
- Temporary files.
- Large generated datasets.
- Parquet/CSV scan outputs unless intentionally curated and small.
- `.env` files or local config containing credentials.

