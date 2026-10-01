# Contributing to PVade

Thank you for your interest in contributing to PVade.
Contributions of all kinds are welcome, including:

- Bug reports and reproducible issue cases.
- New features and solver/geometry improvements.
- Test improvements.
- Documentation updates.

## Before You Start

1. Check whether your topic already exists in the issue tracker: https://github.com/NREL/PVade/issues
2. If not, open a new issue with a clear description and expected behavior.
3. Comment on the issue before starting implementation work, especially for larger changes.

## Development Setup

Use the project conda environment from the repository root:

```bash
mamba env create -n PVade -f environment.yaml
mamba activate PVade
```

This environment includes the FEniCSx/DOLFINx runtime dependencies plus testing and documentation tooling.
See `docs/installing_pvade.rst` for platform-specific notes (including Windows/WSL2 setup).

## Repository Layout

- `pvade_main.py`: entry point for running a simulation, e.g. `python pvade_main.py --input_file examples/panels2d.yaml`.
- `pvade/fluid/`: fluid (CFD) solver components.
- `pvade/structure/`: structural (CSD) solver components.
- `pvade/fsi/`: fluid-structure interaction coupling.
- `pvade/geometry/`: mesh generation and geometry management.
- `pvade/IO/`: input parameter parsing, schema validation, and data/logging output.
- `pvade/tests/`: pytest suite.
- `examples/`: example input YAML files.
- `tutorials/`: standalone tutorial scripts (e.g. `tutorials/poissoneq.py`).
- `docs/`: Sphinx documentation source.

## Local Validation

Run the test suite before opening a pull request:

```bash
PYTHONPATH=. pytest -sv pvade/tests/
```

To also validate that every example input file runs end-to-end:

```bash
pytest -sv test_all_inputs.py
```

To target a specific input file used by the parametrized tests:

```bash
pytest -sv pvade/tests --input-file examples/panels3d.yaml
```

Format code with Black:

```bash
black .
```

Build docs locally when changing documentation:

```bash
cd docs
make html
```

## Coding Guidelines

- Follow PEP 8 and keep code changes focused.
- Prefer small, reviewable pull requests over large mixed changes.
- Add or update tests in `pvade/tests/` when fixing bugs or adding behavior.
- If you add a new input option, update `pvade/IO/input_schema.yaml` and the corresponding section in `docs/input_schema.rst`.
- Keep user-facing defaults and input-file behavior backward compatible where practical.

## Pull Request Checklist

Before submitting a pull request, confirm:

- The change is linked to an issue (or clearly justified).
- `PYTHONPATH=. pytest -sv pvade/tests/` passes locally.
- `black .` has been applied.
- Documentation is updated when behavior, inputs, or outputs changed.
- The PR description explains what changed, why it changed, and how it was validated.

## CI Notes

Current CI (`.github/workflows/test_pvade.yaml`) runs on every push/PR to `main`, `dev`, `sync`, and `dev_wrap`:

- `pytest -sv pvade/tests/` and `pytest -sv test_all_inputs.py` on Ubuntu and macOS.
- Black formatting checks.

If your change affects platform behavior, please call that out in the PR description.

## Reporting Bugs

When reporting a bug, include:

- PVade version or commit hash.
- Operating system and Python version.
- Input file (or minimal subset) to reproduce.
- Full traceback and a short reproduction sequence.

Thanks for helping improve PVade.
