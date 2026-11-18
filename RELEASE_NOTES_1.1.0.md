# PVade 1.1.0

PVade 1.1.0 prepares the existing PV aerodynamic design and fluid-structure interaction application for its first public Python Package Index (PyPI) distribution. PyPI installation is pending completion of the first publication; no public distribution is available yet.

## Packaging and Installation

- Defines PVade as a standard Python distribution with wheel and source packages.
- Adds the installed `pvade` command and `python -m pvade` entry point, including schema-based command-line overrides.
- Preserves `pvade_main.py` as a backward-compatible script and import interface.
- Includes the runtime input schema in the installed package and accesses it package-relatively.
- Adds a runtime-only Conda environment for users to provision native scientific dependencies without cloning the repository.
- Retains the editable Conda/Mamba developer workflow and documents HPC installation with externally provisioned native dependencies.

## Scientific Capabilities

PVade's existing capabilities are unchanged in this release:

- Incompressible flow solved with a fractional-step pressure-correction method in an Arbitrary Lagrangian-Eulerian frame for moving meshes.
- Fluid traction transfer to a finite-element structural solver for nonlinear elastodynamics.
- Panel-array geometry and mesh generation/reuse, thermal analysis, and uniform, parabolic, log-law, and time-resolved HDF5 inflow profiles.
- Parallel finite-element simulations through compatible DOLFINx, PETSc, and MPI installations.

No numerical algorithms are changed as part of this packaging release.

## Release Automation and Validation

- Adds GitHub Actions release automation using PyPI Trusted Publishing and OIDC, gated on a published official GitHub Release.
- Builds and validates source and wheel distributions, checks release-tag/version agreement, and publishes the same validated artifacts without rebuilding.
- Requires package tests, representative single-rank execution, and a two-rank MPI run before publication.
- Adds maintainer procedures in `RELEASING.md`.

Local validation has covered wheel and source builds, Twine metadata checks, wheel contents, clean wheel installation outside the checkout, CLI/resource checks, simulation execution, and MPI execution. The GitHub Actions release workflow itself has not yet been run remotely.

## Limitations

- Python 3.10 is the currently tested and declared version.
- DOLFINx, PETSc, MPI, and other native numerical components must be provisioned separately using a compatible Conda/Mamba environment or HPC modules. `pip install pvade` installs PVade and its Python dependencies, not a complete solver stack.
- The tested runtime recipe uses DOLFINx 0.6, PETSc 3.19.6, and OpenMPI 4.1.6. Platform-specific native library compatibility constraints are documented in `environment-runtime.yaml`.
- PyPI installation is not available until the first public release is successfully published.
