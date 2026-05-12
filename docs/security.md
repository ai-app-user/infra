# Security Rules

## Tokens

- Do not store GitHub tokens in repos, scripts, shell history, or docs.
- Prefer `gh auth login` storing credentials in the OS keyring.
- For automation, pass tokens through environment variables or stdin.

## SSH Keys

- Public keys may be listed or fingerprinted.
- Private keys must never be printed, copied into repos, or shared in logs.

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

