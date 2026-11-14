# Contributing

## Development setup

Use Python 3.10 or newer and install [uv](https://docs.astral.sh/uv/). From the
repository root, install the locked development and test dependencies:

```bash
uv sync --locked --extra dev --extra test
make hooks
```

Before opening a pull request, run:

```bash
make lint
make test
uv run --locked hatch build
uv run --locked python -m twine check dist/*
```

## Linting and formatting

Ruff checks Python source, tests, hooks, examples, and developer scripts. The
rule set lives in `pyproject.toml`; CI, Make targets, and pre-commit use the same
Ruff version from `uv.lock`.

`make lint-fix` applies safe lint fixes. `make format` formats files with a line
length of 120. Pre-commit applies both to staged Python files. Review and stage
any edits before committing again. CI checks the full repository on every pull
request and push to `main`.

Functions are limited to cyclomatic complexity 12 and eight arguments. Existing
over-limit functions carry explicit suppressions; split new functions that exceed
the limits. `RUF100` rejects suppressions that become unnecessary. Avoid running
`ruff check --fix` with a narrow `--select` that includes `RUF100`, because it
can remove markers for rules outside that selection.

Integration tests requiring live credentials are opt-in; see
[tests/README.md](tests/README.md). The default `make test` runs unit tests and mocked endpoint tests.

## Pull request validation

The `Package Check` workflow runs automatically for pull requests. It runs the
unit tests, builds and validates the distributions, smoke-tests the wheel, and
uploads the distributions as workflow artifacts. It does not publish a package.

## Publishing a pull request preview

Preview publication is intentionally opt-in. Only request a preview for code
that is trusted to run with the repository's publishing permissions.

For a pull request from this repository, apply the `publish-preview` label. The
`Publish PR Preview` workflow will build and validate a uniquely versioned
`socketdev` prerelease, publish it to TestPyPI, and add or update a pull request
comment with the exact version and installation command. Both label-triggered
and manually dispatched previews are limited to open pull requests whose
branches belong to this repository.

The workflow reacts when the label is added; pushing another commit while the
label remains on the pull request does not publish a new preview. To publish the
new pull request head or retry a failed publication, remove `publish-preview`
and apply it again.

Maintainers can also open **Actions > Publish PR Preview > Run workflow**, run
it from the repository's default branch, and enter the pull request number.
Manual dispatch is useful when a label should remain unchanged or a
publication needs to be retried.
