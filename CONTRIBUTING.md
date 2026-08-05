# Contributing

## Development setup

Use Python 3.9 or newer. Create and activate a virtual environment, then
install the package with its development and test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,test]"
```

Before opening a pull request, run the focused checks for your change. The
complete local check is:

```bash
python -m pytest
ruff check .
ruff format --check .
hatch build
python -m twine check dist/*
```

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
comment with the exact version and installation command. Label-triggered
publication is skipped for pull requests from forks.

The workflow reacts when the label is added; pushing another commit while the
label remains on the pull request does not publish a new preview. To publish the
new pull request head or retry a failed publication, remove `publish-preview`
and apply it again.

Maintainers can also open **Actions > Publish PR Preview > Run workflow** and
enter the pull request number. Manual dispatch is useful when a label should
remain unchanged or a publication needs to be retried.
