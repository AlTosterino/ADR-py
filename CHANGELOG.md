# Changelog

All notable changes to ADR-py are documented here.

## Unreleased — P0 metadata and configuration foundation

### Added

- Added validated YAML front matter to generated ADRs.
- Added immutable UUID identifiers, numeric ordinals, ISO dates, normalized statuses, tag lists, and supersession reference fields.
- Added `--config` to `adr init` and `adr new`.
- Added `.adrpy.toml` configuration for documentation repositories that do not contain a Python `pyproject.toml`.
- Added explicit errors for missing, malformed, or invalid ADR-py configuration and metadata.
- Added unit coverage for metadata round trips, invalid metadata, config resolution, and config failures.

### Changed

- `adr init` and `adr new` now emit the same metadata schema.
- Relative configured ADR directories resolve relative to their configuration file.
- The YAML implementation uses PyYAML rather than a partial hand-written parser.
- The project toolchain is pinned to `uv==0.12.5` so CI resolves stable Python 3.14 instead of the obsolete 3.14 alpha selected by uv 0.7.8.

### Metadata contract

Generated ADR front matter has this shape:

```yaml
---
id: 12345678-1234-5678-1234-567812345678
ordinal: 7
title: Use PostgreSQL
status: accepted
date: '2026-08-24'
tags:
- database
- persistence
supersedes: []
superseded_by: null
---
```

`id` is immutable and UUID-based. `ordinal` is a display/order value and remains mirrored in the filename. `tags` is always a YAML list. Relationship fields contain UUIDs, not filenames.

### Release decision

This change should be published to PyPI as `0.5.0` after the PR is merged and the migration/configuration documentation is reviewed. Do not publish from this feature branch. The release should include a built-wheel smoke test and a clean-environment CLI test.
