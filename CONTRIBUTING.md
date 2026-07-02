# Contributing to Protolizer

Thank you for your interest in contributing!

## Getting started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dev dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

3. Regenerate protobuf test stubs after editing `.proto` files:

```bash
bash scripts/regenerate_proto.sh
```

## Development workflow

1. Create a branch for your change.
2. Make your changes with tests.
3. Run the checks locally:

```bash
ruff check .
ruff format --check .
mypy protolizer
python -m unittest discover -s tests -v
```

4. Open a pull request against `main` or `master`.

## Releasing

1. Update version in `pyproject.toml` and `CHANGELOG.md`.
2. Create and push a tag: `git tag v1.4.0 && git push origin v1.4.0`
3. The `publish` workflow builds and uploads to PyPI.

### PyPI API token setup

1. On [pypi.org](https://pypi.org), go to **Account settings** → **API tokens**.
2. Create a token scoped to the `protolizer` project.
3. In GitHub: repo **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
4. Name: `PYPI_API_TOKEN`, value: the token (including the `pypi-` prefix).

The publish workflow reads `secrets.PYPI_API_TOKEN` when a `v*` tag is pushed.

## Code guidelines

- Match existing style and keep changes focused.
- Add tests for bug fixes and new behavior.
- Update `CHANGELOG.md` under **Unreleased** for user-visible changes.
- Avoid breaking public API changes without a changelog note.

## Reporting issues

Please include:

- Python version
- `protobuf` version (`pip show protobuf`)
- A minimal reproduction snippet
- Expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
