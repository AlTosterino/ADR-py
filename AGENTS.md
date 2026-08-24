# AGENTS.md

## Repository purpose

ADR-py is a Python 3.11+ command-line application for creating Architecture Decision Records (ADRs). The public CLI is exposed as `adr` and currently supports:

- `adr init [PATH]` — create the initial ADR in `PATH`, or resolve the ADR directory from project configuration/current working directory.
- `adr new NAME` — render and create the next sequentially numbered ADR.

The package is published as `adr`; its import package is `adrpy`.

## Source layout and architecture

This repository uses a small layered/hexagonal architecture. Keep dependencies flowing toward the domain-facing abstractions:

```text
CLI entrypoint
  -> use cases
    -> repository/service ports
      -> concrete file repository and Mako template service

shared_kernel: DTOs, settings, constants, and immutable value objects
injection: composition root and Lidi bindings
templates: packaged ADR templates
```

### Directory responsibilities

- `src/adrpy/entrypoints/`: Typer commands and process-level wiring. Keep command functions thin; translate CLI input into DTOs and delegate.
- `src/adrpy/use_cases/`: application workflows (`InitializeAdr`, `CreateAdr`). Business sequencing belongs here, not in the CLI or file repository.
- `src/adrpy/repositories/`: persistence ports and adapters. `IADRRepository` is the seam for replacing the filesystem implementation with another backend.
- `src/adrpy/services/`: application services, currently template rendering behind `ITemplateService` and `MakoTemplateService`.
- `src/adrpy/shared_kernel/`: cross-cutting types and configuration. DTOs and value objects are frozen dataclasses; preserve that immutability unless there is a strong reason not to.
- `src/adrpy/services/metadata/`: YAML front matter serialization/parsing and metadata validation.
- `src/adrpy/injection/`: the composition root. Register implementations here and resolve dependencies through `lidi`; do not construct infrastructure inside use cases.
- `src/adrpy/templates/`: packaged Mako Markdown templates. Template names are centralized in `AppTemplates`.
- `tests/unit/`: isolated behavior tests, currently focused on settings resolution.
- `tests/integration/`: adapter/filesystem behavior tests, including directory creation, template loading, file creation, and ordinal calculation.

### Architectural rules

- Preserve the CLI → use case → port → adapter direction.
- Use interfaces/abstract base classes when adding a replaceable infrastructure concern. Bind the concrete implementation in `injection/modules.py`.
- Keep filesystem access in repository adapters. Keep rendering in template services. Keep orchestration and business decisions in use cases.
- Configuration is supplied through the frozen `Settings` object. ADR directory resolution currently prefers an explicit command path, then `[tool.adrpy].dir` in the working directory's `pyproject.toml`, then the working directory.
- Configuration also supports an explicit TOML path and `.adrpy.toml` for non-Python documentation repositories. Relative configured directories resolve from the configuration file's directory.
- Generated ADR metadata is YAML front matter with immutable UUID `id`, positive integer `ordinal`, `title`, one of `proposed|accepted|rejected|deprecated|superseded`, ISO `date`, list `tags`, and UUID relationship fields `supersedes`/`superseded_by`. Use `python-frontmatter` for Markdown front matter parsing/rendering; keep ADR-specific validation in `AdrMetadata` and do not implement a partial parser.
- Be careful with import-time dependency resolution: use cases and `ADRFileRepository` currently resolve dependencies as class attributes. Changes to the composition root must be tested for import-order and test-isolation effects.
- ADR filenames use a four-digit ordinal followed by a lowercase, whitespace-to-hyphen title, for example `0002-use-postgresql.md`.
- Ordinal discovery currently scans Markdown filenames and ignores files whose first hyphen-delimited component is not numeric. Any change to numbering or supersession should consider the open metadata/listing issues.
- Do not introduce a second dependency-injection mechanism or bypass `lidipy` without an architectural decision.

## Coding and style conventions

- Target Python 3.11; supported range is `>=3.11,<3.15`.
- Use 4 spaces, a maximum line length of 100, and Black formatting.
- Use type annotations on all functions and methods. Mypy is configured to reject untyped definitions and calls and to warn on unreachable code, missing returns, redundant casts, and unsafe `Any` returns.
- Prefer `Path` over string paths, frozen dataclasses for DTOs/value objects, explicit return types, and small single-purpose methods.
- Use named custom types for structured data crossing a public boundary. Do not return opaque nested tuples or unstructured mappings such as `tuple[str, tuple[str, ...]]`; define a named frozen dataclass, value object, or DTO with meaningful fields instead.
- Specify behavior before implementation: document defaults, accepted inputs, validation rules, errors, side effects, compatibility expectations, and user-visible output. Implement both the successful and failure paths and add tests for each; do not leave behavior implicit in incidental library or template behavior.
- Use descriptors when they improve encapsulation of managed or computed attributes. Prefer standard `property` or `cached_property` for derived/lazily computed values, and use a custom descriptor only when the same get/set/validation behavior is genuinely shared. Do not replace clear plain data fields with descriptors merely for abstraction.
- Follow Ruff's configured rules: `E`, `F`, `I`, `PL`, and `T20`. Keep imports sorted and do not leave debug `print` calls in production code.
- Match the existing naming: classes in PascalCase, functions/methods and modules in `snake_case`, constants in `UPPER_SNAKE_CASE`.
- Organize every source file from global concepts to implementation detail so the most important behavior is visible first. Put the module docstring and imports first, then constants/types, public classes, public module functions/CLI commands, and private helpers at the bottom. Within classes, put the constructor and public methods before private methods. Do not make readers scan past private helpers to discover the application's commands or primary API.
- For entrypoint modules specifically, keep the Typer app and public commands prominent; place validation adapters and other command helpers after the commands they support. For service/repository modules, expose the interface or main public operation before private parsing, formatting, and filesystem helpers.
- Use comments/docstrings for intent and non-obvious constraints. Treat existing TODOs as known design debt, not as permission to widen a change unnecessarily.
- Preserve cross-platform behavior. CI runs on Ubuntu and Windows, so use `pathlib`, avoid OS-specific separators, and test CLI/path changes on both platforms when practical.
- Do not edit `uv.lock` manually. Change dependency declarations in `pyproject.toml` and regenerate the lockfile with `uv lock`.

## Testing and validation

Use the repository's Make targets from the project root:

```console
make sync-deps   # uv sync --frozen --active
make lint        # format, auto-fix Ruff issues, then run mypy
make lint-ci     # Black check, Ruff check, and mypy; matches CI
make test        # pytest -s
```

For focused work, the underlying commands are:

```console
uv run --active pytest -s tests/unit/test_settings.py
uv run --active pytest -s tests/integration/repository/implementation/test_adr_file_repository.py
uv run --active black src tests
uv run --active ruff check src tests
uv run --active mypy src tests
```

The lockfile and `pyproject.toml` require `uv==0.12.5`; use that version before running the commands if the installed `uv` version differs. CI runs the frozen dependency sync, `make lint-ci`, and `make test` on Python 3.11, 3.12, 3.13, and 3.14 across Ubuntu and Windows. Python prereleases such as 3.15 should be tested in a separate explicitly non-stable job before being added to the supported matrix. Pytest treats warnings as errors, so new warnings are test failures.

When changing behavior:

1. Add or update a unit test for pure logic/configuration.
2. Add or update an integration test for repository, template, CLI, or filesystem behavior.
3. Run `make lint-ci` and `make test`.
4. For CLI changes, manually check `adr --help`, `adr init`, and `adr new "Example decision"` in a temporary directory and verify generated Markdown/front matter.
5. Do not commit generated ADR test directories, build artifacts, caches, or local environments.

After every change, run a rigorous end-to-end verification using every currently available CLI command and relevant option. This must include the help paths, successful workflows, invalid inputs, boundary/edge cases, configuration and positional-path precedence, repeated metadata inputs, expected exit codes, generated files, parsed metadata, and preservation of the Markdown body. Run the repository's full lint/test checks as well as the CLI smoke tests; do not consider a change verified from unit tests alone. When packaging or release behavior is affected, also build the wheel, install it into a clean environment, and repeat the CLI smoke test through the installed entry point.

## GitHub issue context and roadmap

The repository's issue history is part of the design context. Keep these requirements in mind when changing related code:

- [#18 List ADRs command](https://github.com/AlTosterino/ADR-py/issues/18) — future listing should expose ADRs and supersession state.
- [#17 Custom templates](https://github.com/AlTosterino/ADR-py/issues/17) — custom templates should extend the existing template abstraction/configuration rather than hard-code a parallel path.
- [#16 Default metadata in tags/front matter](https://github.com/AlTosterino/ADR-py/issues/16) — metadata is expected to support stable identity, ordinal, title, status, date, tags, and supersession relationships; decide whether IDs are title-derived or UUID-based before implementing consumers.
- [#9 Web viewer](https://github.com/AlTosterino/ADR-py/issues/9) — a viewer is intended to be optional and should not burden the core CLI dependency set.
- [#20 Missing `pyproject.toml`](https://github.com/AlTosterino/ADR-py/issues/20) — ADR repositories may be ordinary documentation directories rather than Python projects; avoid assuming a target directory contains a Python `pyproject.toml` when improving configuration discovery.
- Closed issues [#15](https://github.com/AlTosterino/ADR-py/issues/15), [#12](https://github.com/AlTosterino/ADR-py/issues/12), [#11](https://github.com/AlTosterino/ADR-py/issues/11), [#7](https://github.com/AlTosterino/ADR-py/issues/7), and [#3](https://github.com/AlTosterino/ADR-py/issues/3) establish regression expectations for generated front matter, Windows help, warning-free code, initialization, and `lidipy` usage.

Do not implement roadmap features opportunistically while fixing an unrelated bug. If a change affects ADR metadata, template resolution, numbering, or directory discovery, check the linked issues and add regression coverage.

## Branch naming and change workflow

Use one of these branch prefixes, followed by a short lowercase hyphenated description:

```text
feature/xyz
bug/xyz
chore/xyz
```

Examples: `feature/list-adrs`, `bug/windows-help`, `chore/update-uv`. Branch names should describe one focused change. Start from the current `main`, keep commits focused, and include the relevant issue number in the pull request or commit message when applicable. Before opening a PR, ensure the working tree is clean apart from intended changes and that the same checks required by CI pass locally.

All Git commit messages must use a Gitmoji prefix, including commits created by agents. Use a Gitmoji followed by a concise imperative summary, for example `:sparkles: add ADR listing command`, `:bug: handle missing ADR directory`, or `:memo: update agent guidance`.

## Contributing

ADR-py is a public open-source project. Contributions from maintainers, users, and automation are welcome, but every contribution must be reviewable, reproducible, and safe for existing users.

- Check existing issues, pull requests, and the roadmap before starting work. For substantial changes, link an existing issue or open one first.
- Create focused branches from the current `main` using `feature/xyz`, `bug/xyz`, `chore/xyz`, or `docs/xyz` where appropriate. Never develop directly on `main`.
- Keep commits small and use Gitmoji-prefixed imperative messages. Do not mix unrelated refactors, generated artifacts, dependency changes, and feature work in one contribution.
- For dependency changes, explain why the dependency/version is needed, update `uv.lock` through uv, run the security/dependency checks available to the contributor, and disclose tools that could not analyze the project.
- Every pull request must include a concise summary, user-visible behavior, testing performed, compatibility or migration impact, and known limitations. The merged [PR #21](https://github.com/AlTosterino/ADR-py/pull/21) is the model for a focused dependency PR: rationale, lockfile update, test plan, and transparent security-scan notes.
- User-facing changes must update `README.md`, `CHANGELOG.md`, roadmap documentation, or migration notes as applicable. Follow Keep a Changelog 1.1.0; do not use commit history as the changelog.
- Before requesting review, run the full lint/test suite and the rigorous CLI E2E verification required above. Include the commands and results in the pull request.
- Do not commit generated ADR fixtures, temporary directories, virtual environments, build outputs, secrets, or local editor state.
- Contributors must respond to review findings with code, tests, or an explicit explanation. Do not bypass CI or force-push over another contributor's work without coordination.
- Security vulnerabilities and credentials must not be posted in public issues or pull requests; use the repository's private reporting channel if one is configured.

## Release and packaging notes

ADR-py is a public open-source project. Treat every release, dependency change, metadata change, and generated-file change as user-facing and potentially irreversible. Do not treat this as a private or disposable project: preserve backwards compatibility, document migration impact, and require evidence before publishing.

### Changelog policy

`CHANGELOG.md` must follow [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and Semantic Versioning:

- Keep `## [Unreleased]` at the top.
- Keep released versions in reverse chronological order with an ISO date: `## [0.5.0] - YYYY-MM-DD`.
- Group user-facing changes under only the applicable standard headings: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.
- Write curated notes for users and maintainers; do not paste Git history or commit messages into the changelog.
- Record breaking changes, deprecations, removals, migration steps, security fixes, and behavior changes explicitly.
- Move entries from `Unreleased` into the versioned section during release preparation, then add comparison links at the bottom of the file.
- Keep the changelog consistent with the actual wheel, CLI behavior, documentation, and GitHub release notes.
- Every GitHub Release must have non-empty, human-written release notes. Prepare and review them before tagging; they must summarize the release, link or correspond to the versioned `CHANGELOG.md` section, and call out breaking changes, migrations, security fixes, dependency changes, and notable contributors where applicable.

### Release decision for the P0 metadata/configuration work

PR #24 is intended for a public PyPI release as `0.5.0`, but only after all of these gates pass:

- PR #24 is merged into `main`; never publish or tag from `feature/p0-metadata-foundation` or another feature branch.
- Configuration and metadata migration documentation is reviewed and describes UUIDs, ordinals, statuses, tags, front matter, config precedence, and compatibility with existing ADR files.
- `CHANGELOG.md` is converted from `Unreleased` into a dated `[0.5.0]` section using the Keep a Changelog rules above.
- The supported Python matrix and dependency lockfile are current and green.
- A wheel is built and installed into a clean environment, not only tested from the checkout.
- The clean environment smoke test runs `adr --help`, `adr init`, and `adr new`, creates multiple ADRs, verifies front matter and the Markdown body, and exercises configuration resolution.
- The release commit has passed the same CI checks that the tag-triggered workflow will run.

### Required release workflow

The GitHub Actions workflow in `.github/workflows/ci.yaml` is authoritative. A `v*` tag runs the test matrix first; the `publish` job then builds the package, publishes it to PyPI using `PYPI_TOKEN`, and creates the GitHub Release with the built artifacts.

1. Merge the release-ready pull request into `main`.
2. Create a focused release-preparation branch from the merged `main`, for example `chore/release-0.5.0`.
3. Update the project version, lockfile if required, `CHANGELOG.md`, and release/migration documentation. Use a Gitmoji commit.
4. Run `make sync-deps`, `make lint-ci`, `make test`, `uv build`, and the clean-environment wheel/CLI smoke test.
5. Open and merge the release-preparation PR. Confirm the exact commit to release is on `main` and CI is green.
6. Create an annotated tag on that exact `main` commit: `git tag -a v0.5.0 -m ':bookmark: release v0.5.0'`.
7. Push the tag: `git push origin v0.5.0`. Do not use `uv publish` manually when the tag workflow is the configured release path.
8. Verify the tag workflow, PyPI package, GitHub Release, attached wheel/sdist, installed-package smoke test, and non-empty release notes. If the workflow creates a GitHub Release without notes, update it immediately with the reviewed notes before considering the release complete. If publication fails, stop and diagnose the workflow; never create a replacement version or overwrite release history casually.

Do not create a release merely because code is merged. Do not publish feature-branch artifacts, dirty working trees, unreviewed changelogs, or packages that have not passed the clean-wheel smoke test. Do not change package layout, entrypoint configuration, version support, or the publish workflow without checking both the wheel build and GitHub Actions behavior.
