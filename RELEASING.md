# PVade Release Process

This document describes how maintainers prepare and publish a PVade release. PyPI publication is automated only after a GitHub Release is explicitly published. The workflow does not publish on pushes or pull requests.

## Versioning

`pyproject.toml` is the authoritative Python distribution version. Update its `[project].version` for every release. Keep the informational `version` in `codemeta.json` synchronized. The wheel-content check compares these values. `CITATION.cff` currently identifies the existing 2023 software citation/DOI and has no package-version field; do not change its citation date merely for a packaging release. Update it only when the citation record itself changes.

The supported Python range is declared in `pyproject.toml`; currently only Python 3.10 is claimed and tested. Do not expand supported Python versions or operating systems without CI and native-stack testing.

## Branch and Pull Request Route

For this 1.1.0 preparation, the working branch is `main` on the personal `arswalid/PVade_pub` fork, as requested. Push that branch only after review, then open a pull request from `arswalid/PVade_pub:main` into `NatLabRockies/PVade:dev`. Complete development and CI review on official `dev`; the maintainer then opens the official `dev` to `main` pull request. The published release tag and GitHub Release must be created from official `main`.

Do not push directly to the official repository. Review the final PR diff to ensure unrelated `paper/` files are not included.

## Checks Before Release

1. For the planned 1.1.0 release, develop on `arswalid/PVade_pub:main`, open a pull request into `NatLabRockies/PVade:dev`, complete development checks there, then submit official `dev` to official `main` for release approval.
2. Confirm `test_pvade.yaml` passes, including the Conda-based simulation tests and formatting job.
3. Confirm `test_packaging.yaml` passes, including source/wheel build, Twine validation, wheel contents, clean install, imports, resources, and CLI checks.
4. From the release candidate checkout, run `python -m build`, `python -m twine check dist/*`, and `python packaging_tests/check_wheel.py dist/*.whl`.
5. Review [RELEASE_NOTES_1.1.0.md](RELEASE_NOTES_1.1.0.md) or prepare the corresponding notes for the next version.

The release workflow builds the candidate distributions, checks their metadata and contents, compares the wheel version to the release tag, then installs that exact wheel into the supported Conda environment. It runs the CLI/import/resource checks, a representative single-rank example, and a two-rank MPI example. Publishing waits for all these jobs to pass and uses those same uploaded artifacts; it does not rebuild them.

## Trusted Publishing Setup

The PyPI project `pvade` has been created as a pending project. Finish configuring its Trusted Publisher before publishing the first release. In the PyPI account that owns the pending project, configure these values exactly:

- PyPI project: `pvade`
- GitHub owner: `NatLabRockies`
- GitHub repository: `PVade`
- Workflow filename: `publish-pypi.yml`
- Environment: `pypi`

The GitHub environment named `pypi` already exists in the official repository. Do not create a duplicate. Configure it to require manual approval by trusted maintainers. PyPA recommends approval protection for PyPI deployments. Workflow jobs have repository contents read access; the publishing job alone receives `id-token: write` for OIDC. It uses `pypa/gh-action-pypi-publish@release/v1` and no PyPI API token or repository secret.

## Publish a Release

1. Ensure the release commit is merged to official `main` and all required checks are green.
2. Ensure `pyproject.toml` contains `1.1.0` and `codemeta.json` matches. `pyproject.toml` is the package-version source; do not rewrite historical `v1.0.0` references or the existing 2023 citation record.
3. Push tag `v1.1.0` to the official repository at the reviewed commit. The workflow strips an optional `v` and requires an exact match to the built wheel version; it also fails unless the tagged commit is contained in official `main`.
4. On GitHub, create a Release from `v1.1.0`, paste [RELEASE_NOTES_1.1.0.md](RELEASE_NOTES_1.1.0.md), and publish the GitHub Release. Creating or pushing a tag alone does not publish to PyPI; the workflow trigger is the `published` release event.
5. Watch the `Publish to PyPI` workflow. The `publish` job cannot start unless both the build and native validation jobs pass. Approve the `pypi` environment deployment if protection rules require it.

Do not create a GitHub release or publish to PyPI until the project owner explicitly approves the publication.

## After Publication

Confirm the version and files on the PyPI project page. In a clean Python 3.10 environment with compatible DOLFINx, PETSc, and MPI already provisioned, verify:

```bash
python -m pip install pvade
python -m pip show pvade
python -c "import pvade; print(pvade.__file__)"
pvade --help
```

Run a short example and, where the environment supports it, a two-rank MPI case. Then replace the pending-release warning in the installation documentation with the published-version instructions and link the public project page. Do not claim that pip alone installs the native scientific stack.

## Failures and Corrections

If build, metadata, or simulation validation fails before upload, nothing has been published. Fix the issue on a branch, merge the correction, and rerun the workflow for the approved release tag only if the tagged source remains correct. Otherwise prepare a new version and tag. A failed workflow can be rerun from the Actions page after confirming that its artifacts correspond to the intended release commit. If PyPI accepted only some files before a publication failure, inspect the project files first; do not enable `skip-existing` or blindly retry an already-uploaded artifact. Coordinate a reviewed recovery that publishes only the missing file, or use a new version if the release contents need correction.

PyPI releases are immutable. If a defective version has already been published, do not try to upload replacement files under the same version. Yank the defective release with an explanation, prepare a corrected patch release, run the full checks, and publish a new GitHub Release/PyPI version. Do not delete a public release merely to reuse its version.

## Version Policy

Follow semantic versioning for the Python distribution:

- Patch (`1.1.1`): backward-compatible fixes and packaging corrections.
- Minor (`1.1.0`): backward-compatible features or supported interface additions.
- Major (`2.0.0`): intentional breaking changes to supported user interfaces or package behavior.

Keep solver numerics, supported Python/platform claims, and native-library compatibility statements explicit in release notes. Every new version must pass the same artifact and native-stack validation before publication.
