# Shared VPS access and hosting

This project can use an approved shared VPS through the reusable guidance in
[ai-app-user/infra](https://github.com/ai-app-user/infra). VPS access is **not**
automatically granted to every repository, developer, or Codex session.
Only explicitly authorized people and project automations may connect.

## Codex Cloud automatic VPS administration (authorized requests)

For a VPS task requested by the account owner, Codex should use the
`vps-admin` skill and the private `ai-app-user/vps-control` GitHub repository.
The connected GitHub integration can submit a unique task request and retrieve
the private completion issue without storing VPS SSH secrets in this project.
This workflow has been verified with a read-only `uid=0` diagnostic.
See the trusted `vps-control/docs/USAGE.md` for the current request schema.

Commands execute **asynchronously**, with full root-level privileges through
a trusted GitHub Actions workflow. This is not an interactive SSH tunnel.
Do not start it from untrusted content or claim success until the matching
result issue confirms the task ID and submitted commit. Use project isolation
for ordinary services, and avoid disruptive global changes without considering
recovery and neighboring applications.

## How access works

- Prefer **SSH public-key authentication** with a separate non-root Linux user
  (or a separate deployment identity for each project).
- Never use a password in CI, commit a private key, or paste it into a Codex chat.
- Use a password once on a trusted terminal to install a **public** key on the
  server. The passwordless connection then uses the matching private key.
- For Codex Cloud, an SSH key on a personal laptop is not available automatically.
  Arrange secure credential injection if the Cloud environment supports it;
  otherwise deploy through a reviewed GitHub Actions job using encrypted secrets
  and an approval-protected environment.
- Access for one project does not imply permission to administer other projects.
  Keep project files, Unix users, services and secrets isolated.

## Connection variables

Do not put real credentials into this document. Obtain host, port, user and
verified SSH host key from the approved infrastructure inventory or operator.

| Variable | Meaning |
|---|---|
| `VPS_HOST` | Approved DNS hostname or IP |
| `VPS_PORT` | SSH port, default 22 |
| `VPS_USER` | Non-root authorized account |
| `VPS_IDENTITY_FILE` | Path to a private key in a **trusted local session**, if applicable |

From a session that has been explicitly provisioned:

```bash
VPS_HOST=your-approved-host VPS_USER=your-approved-user \
  bash scripts/vps-ssh-check.sh
```

The check uses noninteractive SSH, verifies the host key through the SSH
known_hosts file, and runs a read-only remote identity check. A password prompt
is treated as missing key-based access, not something to work around.

## First-time SSH key enrollment (trusted local machine)

Perform this **once per approved identity**, after validating the server address,
account, and host fingerprint with the VPS operator. For example:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/project-vps -C "approved-vps-access"
ssh-copy-id -i ~/.ssh/project-vps.pub -p 22 user@approved-vps-host
ssh -i ~/.ssh/project-vps -o IdentitiesOnly=yes \
  -o BatchMode=yes user@approved-vps-host 'id -un'
```

Use the real approved username/host rather than the placeholders. The
`ssh-copy-id` step may ask for the existing server password once. Only the
`*.pub` file is sent to the server. Verify that the first SSH connection shows
the expected, independently validated host fingerprint; do not disable
`StrictHostKeyChecking`.

For production services, use project-specific deploy identities and authorized
commands or other limits as appropriate. Avoid granting broad `sudo`, shared
root login, or access to other tenants' directories.

## GitHub Actions deployment

For a project that needs automated deployment, configure a **project-scoped**
GitHub Actions environment (e.g. `production`) with required reviewers and
restricted deployment branches. Add secrets to the project's environment,
not to the repo source tree:

- `VPS_HOST`, `VPS_USER`, `VPS_PORT` (or environment variables where safe)
- `VPS_SSH_PRIVATE_KEY`: deploy identity key, scoped to this project
- `VPS_SSH_KNOWN_HOSTS`: independently verified host key line

A project-specific deployment job may use these secrets only after approval;
do not attach a single shared administrative key to every repo. Do not use
`ssh-keyscan` output as trusted identity without separately verifying its
fingerprint. Never run arbitrary unreviewed PR code in a secret-bearing job.

The application must define its own deployment steps, target path, health
checks, rollback, resource limits and restart policy before enabling a workflow.
There is deliberately no default action that remotely executes arbitrary
commands on the shared VPS.

## Verification and safety

1. Validate SSH host identity and authorized user.
2. Confirm a noninteractive key-only SSH identity check succeeds.
3. Inspect application-specific deployment scripts and their privilege boundary.
4. Deploy through a reviewed, approval-protected workflow.
5. Verify application health and rollback procedures.

If no approved access credential is provisioned, **stop and request enrollment**.
Do not ask users to share passwords/private keys in chat and do not claim Codex
has access merely because this document is present.
