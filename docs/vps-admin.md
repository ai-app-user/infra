# Full VPS administration from Codex

## Preferred automatic route

**Current:** The private `ai-app-user/vps-control` repository contains an
unattended GitHub Actions gateway using independently configured `vps-admin`
environment secrets. The user has validated automatic request submission and a
read-only root SSH check. To request authorized work, use
`skills/vps-admin/SKILL.md` and read `vps-control/docs/USAGE.md`.
Results are returned through private GitHub issues associated with the
submitted task commit.

The manual `infra` workflow described below remains a controlled fallback,
not the default. Do not issue the same task through both routes.
A user request to deploy or administer the VPS authorizes that scoped task,
not unrelated or third-party commands. This is a powerful, root-equivalent,
**asynchronous** capability; protect the private repository and credentials.

## Legacy review-gated fallback

## Security model

The user authorized **full administrative capability**, not automatic execution
of unrestricted shell input from arbitrary ChatGPT sessions or project branches.
Root access to a shared VPS can interrupt every hosted project. Keep the
privileged access centralized in the private, review-gated GitHub Actions
environment `vps-admin` in `ai-app-user/infra`. Ordinary project repositories
receive only limited deployment identities.

The admin workflow is manual (`workflow_dispatch`) and only runs from trusted
`infra/main` for the allowed GitHub actor `ai-app-user`. Its workflow job
targets the protected `vps-admin` environment, which must restrict deployment to `main` and should require an independent
reviewer where the GitHub plan/account permits it.
GitHub plan restrictions may affect reviewer protection features; test what
restrictions are actually enforced before storing the admin key. Never claim
a reviewer approval exists unless it is configured and verified.

To perform new administration tasks, Codex prepares a **new reviewed script**
under `ops/vps/admin/NAME.sh` on an infra feature branch with tests/rollback
notes. Review and merge the PR, then explicitly start the VPS administration
GitHub Action with `operation=NAME`. Do not accept arbitrary shell commands
as workflow inputs. Scripts run as root after manual approval. Keep logs
free of private configuration, tokens and sensitive data.

## VPS one-time enrollment (operator on trusted terminal)

An operator with existing sudo-enabled SSH access must do this. These
instructions do **not** connect to or configure the VPS automatically.

1. Verify the VPS address and SSH host fingerprint out of band.
2. Generate a **separate** ed25519 key intended only for admin automation.
   Store its private half in a secure local location until uploaded to GitHub
   Actions environment secrets. Do not reuse personal or application SSH keys.
3. On the VPS, create a dedicated Unix user `codex-admin`, disabled for
   password login, and install only its *public* SSH key into
   `~codex-admin/.ssh/authorized_keys` with ownership and modes 700/600.
4. **After understanding the root-equivalent risk**, grant `codex-admin`
   noninteractive sudo for the workflow. A dedicated file installed using
   `visudo -f /etc/sudoers.d/codex-admin` may contain:
   
   ```text
   codex-admin ALL=(root) NOPASSWD: /usr/bin/bash
   ```

   This restriction is **not a sandbox**: permission to run Bash as root
   permits arbitrary root operations. Protect this SSH identity like root.
   Validate the sudoers syntax and test `sudo -n bash -c 'id -u'` expecting 0.
5. Keep the current manually working SSH identity as break-glass recovery.
   Do not disable passwords or alter SSH networking until verified recovery
   access exists.

## GitHub environment configuration

Repository: `ai-app-user/infra` → Settings → Environments → create `vps-admin`.

Restrict permitted branches to `main`. Ideally require an independent
reviewer and enable prevent-self-review. For a solo-owned account where this
is unavailable, the explicit manual workflow dispatch by `ai-app-user` is
the execution-approval action; require branch protection and review changes
before merging scripts to main. Treat this as a weaker approval boundary
and do not enable unattended triggers.

Store these **environment** secrets (not repository-level secrets):
- `VPS_ADMIN_HOST`: independently verified hostname/IP
- `VPS_ADMIN_USER`: `codex-admin`
- `VPS_ADMIN_SSH_KEY`: entire dedicated private key
- `VPS_ADMIN_KNOWN_HOSTS`: verified known_hosts entry

Optional environment variable: `VPS_ADMIN_PORT` (default 22).
The hostname and public host fingerprint are not confidential, but using an
environment-scoped configuration avoids inconsistent targets.

Never paste SSH passwords or keys into ChatGPT; enter secrets directly in
GitHub's settings interface. Never use a key from someone else's project,
disable host key checking, or print the private key in logs.

## First test

After the protection rules are set up, navigate to GitHub Actions in infra,
select **VPS administration (approved)**, Run workflow, select `main`,
and set `operation` to `diagnostics`. Review/approve the environment
deployment in GitHub. The workflow should print the Linux username (root),
host information and a read-only resource snapshot. It should not modify
packages, containers, networking, or running applications.

## Running future tasks

You can request Codex to prepare changes such as installing Docker, configuring
a reverse proxy, or administering networking. Codex must propose a named
script, risks, maintenance/rollback plan, and PR. After the PR is merged,
an approved admin workflow executes it as root. Network/firewall/SSH changes
should include out-of-band recovery instructions because a failure can cut
off VPS access.

This establishes permission to perform root operations **after review**, not a
promise that every Codex Cloud session can SSH into the VPS directly. The
GitHub Actions runner is the controlled execution point.
