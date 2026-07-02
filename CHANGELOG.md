# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2026-07-02

### Added

- `partial=True` support for PATCH-style partial validation.
- `SECURITY.md` vulnerability reporting policy.
- PyPI publish workflow on version tags.
- README examples for `EnumField` and partial updates.

## [1.3.0] - 2026-07-02

### Added

- `BytesField` for proper protobuf bytes handling.
- `EnumField` for protobuf enum values (int or name input).
- Field options: `read_only`, `write_only`, `required`, `allow_null`.
- `CONTRIBUTING.md`, `CHANGELOG.md`, and proto regeneration script.
- Dev tooling: Ruff, Mypy, pre-commit, and `py.typed` marker.
- GitHub Actions CI matrix for Python 3.8–3.12 with lint and type checks.

### Fixed

- Package exports: `from protolizer import fields` and exception helpers.
- `validate_{field}` hooks now receive validated values.
- Read path no longer runs write validation hooks on `.data`.
- `InvalidDataError` is surfaced through `is_valid().errors`.
- `ListSerializer` preserves validation error details.
- `pre_serialize` receives a copy of data to avoid mutating cached output.
- Missing `Meta.schema` raises a clear error instead of returning `None`.
- Custom fields use `get_custom_*` on serialization (read path).
- Documentation references to nonexistent `.json` property.

## [1.2.0] - 2024

### Added

- Initial published release with DRF-style serializers for protobuf messages.
- Core field types, nested serializers, hooks, and examples.

[Unreleased]: https://github.com/its0x4d/protolizer/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/its0x4d/protolizer/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/its0x4d/protolizer/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/its0x4d/protolizer/releases/tag/v1.2.0
