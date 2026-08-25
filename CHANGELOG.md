# Changelog

All notable changes to ADR-py are documented here.

This project follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `adr list` to inspect ADR titles, statuses, tags, and superseded state.

## [0.5.0] - 2026-08-24

### Added

- `--status` and repeatable `--tag` options for `adr init` and `adr new`.
- Contributor documentation and contribution workflow guidance.
- Validated YAML front matter for generated ADRs.
- Immutable UUID identifiers, numeric ordinals, ISO dates, statuses, tag lists, and supersession reference fields.
- `--config` support for `adr init` and `adr new`.
- `.adrpy.toml` support for documentation repositories without a Python `pyproject.toml`.
- Explicit errors for missing, malformed, or invalid ADR-py configuration and metadata.
- Unit coverage for metadata round trips, invalid metadata, config resolution, and config failures.

### Changed

- `adr init` and `adr new` emit the same metadata schema.
- Relative configured ADR directories resolve relative to their configuration file.
- Front matter parsing/rendering uses `python-frontmatter`; ADR-specific validation remains in the typed metadata model.
- Updated Mako from `1.3.10` to `1.3.11` in [PR #21](https://github.com/AlTosterino/ADR-py/pull/21), contributed by [Ben Jefferies](https://github.com/benjefferies).
- The project toolchain is pinned to `uv==0.12.5` so CI resolves stable Python 3.14.

### Fixed

- Invalid status, blank tag, and duplicate tag inputs now return actionable CLI errors instead of creating files or raising tracebacks.

[unreleased]: https://github.com/AlTosterino/ADR-py/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/AlTosterino/ADR-py/compare/v0.4.1...v0.5.0
