# Contributing to ADR-py

Thank you for contributing to ADR-py. It is a public open-source project, so changes must be understandable, reproducible, and safe for existing users.

## Before starting

Check the [issues](https://github.com/AlTosterino/ADR-py/issues), open pull requests, and [roadmap](https://github.com/AlTosterino/ADR-py/blob/main/AGENTS.md) before starting. Link your work to an existing issue or open one for substantial changes.

## Branches and commits

Use a focused branch from the current `main`:

```text
feature/xyz
bug/xyz
chore/xyz
docs/xyz
```

All commits must use a Gitmoji-prefixed imperative message, for example:

```text
:sparkles: add ADR listing command
:bug: handle invalid metadata status
:memo: document release workflow
```

Do not commit generated ADRs, build outputs, virtual environments, caches, secrets, or editor files.

## Pull requests

Every pull request should explain:

- What changed and why.
- User-visible behavior and compatibility impact.
- Tests and commands run, including E2E coverage.
- Migration or documentation requirements.
- Known limitations and follow-up work.

Keep changes focused. Dependency pull requests should include the reason for the version change, the updated lockfile, test results, and any security/dependency scan limitations. [PR #21](https://github.com/AlTosterino/ADR-py/pull/21) is a good example: it explains the Mako update, updates `uv.lock`, records the test plan, and transparently notes the attempted Snyk scan.

## Required checks

From the repository root, run:

```console
make sync-deps
make lint-ci
make test
```

Also run the rigorous CLI E2E verification required by `AGENTS.md`: exercise every available command and help path, successful and invalid workflows, edge cases, generated metadata, exit codes, and Markdown body preservation. Packaging changes require a clean wheel build/install smoke test.

User-facing changes must update the appropriate documentation and `CHANGELOG.md`. The changelog follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and Semantic Versioning.

## Review and security

Do not bypass CI or merge directly to `main`. Respond to review findings with code, tests, or an explicit explanation. Do not disclose vulnerabilities or credentials in public issues or pull requests; use a private reporting channel if one is configured.
