# Working in infra

Read `docs/project-guidelines.md` and `docs/security.md` for shared standards.
For project creation, adoption, updates, or global improvements, read the
canonical `skills/project-bootstrap/SKILL.md` and its linked workflow docs.

Changes to shared standards must be explicit, versioned, tested, and proposed
through reviewable pull requests. Never silently merge or propagate them.
Run `python3 -m unittest discover -s tests -v` and `for script in scripts/*.sh; do bash -n "$script"; done`.
Tests must not create real GitHub repositories without user approval.
