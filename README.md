# PVade

`PVade` is an open source fluid-structure interaction model which can be used to study wind loading and stability on solar-tracking PV arrays. `PVade` can be used as part of a larger modeling chain to provide stressor inputs to mechanical module models to study the physics of failure for degradation mechanisms such as cell cracking, weathering of cracked cells, and glass breakage. For more information, visit the [PVade Documentation](https://pvade.readthedocs.io/en/latest/index.html).

[![PyPI version](https://img.shields.io/pypi/v/pvade)](https://pypi.org/project/pvade/)
[![Python versions](https://img.shields.io/pypi/pyversions/pvade)](https://pypi.org/project/pvade/)
[![License](https://img.shields.io/pypi/l/pvade)](https://github.com/NatLabRockies/PVade/blob/main/LICENSE.txt)
[![Latest GitHub release](https://img.shields.io/github/v/release/NatLabRockies/PVade)](https://github.com/NatLabRockies/PVade/releases/latest)

[![test_pvade](https://github.com/NatLabRockies/PVade/actions/workflows/test_pvade.yaml/badge.svg?branch=main)](https://github.com/NatLabRockies/PVade/actions/workflows/test_pvade.yaml)
[![test-packaging](https://github.com/NatLabRockies/PVade/actions/workflows/test_packaging.yaml/badge.svg?branch=main)](https://github.com/NatLabRockies/PVade/actions/workflows/test_packaging.yaml)
[![test-pypi](https://github.com/NatLabRockies/PVade/actions/workflows/test_pypi.yaml/badge.svg?branch=main)](https://github.com/NatLabRockies/PVade/actions/workflows/test_pypi.yaml)

[![Documentation Status](https://readthedocs.org/projects/pvade/badge/?version=latest)](https://pvade.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://img.shields.io/badge/DOI-10.11578%2Fdc.20231208.1-blue)](https://doi.org/10.11578/dc.20231208.1)

- **test_pvade** runs the pytest suite (unit, input-validation and regression tests), runs every example input file end to end, and checks Black formatting, on Ubuntu and macOS.
- **test-packaging** builds the source and wheel distributions, checks their metadata and contents, and installs the wheel.
- **test-pypi** installs the published release from PyPI and runs smoke simulations (weekly, on manual request, and after each release is published).

## Getting Started

PVade is available on [PyPI](https://pypi.org/project/pvade/). It is pip-installable, but full simulations also need the native scientific stack (DOLFINx, PETSc, MPI), which pip does not provide. The recommended route is to provision that stack with Conda/Mamba and install PVade into it. See the [installation guide](https://pvade.readthedocs.io/en/latest/installing_pvade.html) for platform-specific notes, including HPC systems and Windows.

## Installation

### Install from PyPI (recommended)

You do not need to clone the repository. Create the runtime environment (Python 3.10, DOLFINx 0.6, PETSc, OpenMPI and all Python dependencies) from the official environment file, then install PVade into it:

```bash
curl -fsSLO https://raw.githubusercontent.com/NatLabRockies/PVade/main/environment-runtime.yaml
mamba env create -f environment-runtime.yaml
mamba activate pvade
python -m pip install --no-deps pvade
```

To install a specific release, use `python -m pip install --no-deps pvade==1.1.0` and take `environment-runtime.yaml` from the matching release tag (for example `.../PVade/v1.1.0/environment-runtime.yaml`). `--no-deps` keeps the Conda-provided packages, including the tested Gmsh, in place; without it pip may replace Gmsh with a different PyPI build, which changes the generated meshes. Verify the installation:

```bash
python -m pip show pvade
pvade --help
python -m pvade --help
```

### Developer installation

From a clone of the repository, create the development environment and install PVade in editable mode:

```bash
git clone https://github.com/NatLabRockies/PVade.git
cd PVade
mamba env create -f environment.yaml
mamba activate pvade
python -m pip install --no-deps -e .
pytest -sv pvade/tests
```

### HPC installation

On a system with a working MPI, PETSc and DOLFINx stack, keep that stack and install only PVade into the existing environment:

```bash
python -m pip install --no-deps pvade
```

Use this only when every dependency declared by PVade is already importable in that environment.

## Running PVade

Run a simulation by giving the installed command a YAML input file:

```bash
pvade --input_file configuration.yaml
python -m pvade --input_file configuration.yaml
mpirun -np 2 pvade --input_file configuration.yaml
```

`--input` is accepted as a shorthand for `--input_file`. Any input parameter can be overridden on the command line, for example `--solver.t_final 0.01`. From a source checkout, the original script interface still works:

```bash
python pvade_main.py --input_file examples/panels2d.yaml
```

Example input files live in the [`examples/`](https://github.com/NatLabRockies/PVade/tree/main/examples) directory of the repository and are not part of the installed package. To get one without cloning:

```bash
curl -fsSLO https://raw.githubusercontent.com/NatLabRockies/PVade/main/examples/panels2d.yaml
pvade --input_file panels2d.yaml
```



## Citation

To cite PVade, please use the "Cite this repository" feature available on the right-hand side of this repository page or copy the BibTeX reference below:

```bibtex
@software{Young_PVade_PV_Aerodynamic_2023,
    author = {Young, Ethan and Arsalane, Walid and Stanislawski, Brooke and He, Xin and Ivanov, Chris and Dana, Scott and Deceglie, Michael},
    doi = {10.11578/dc.20231208.1},
    month = sep,
    title = {{PVade (PV Aerodynamic Design Engineering) [SWR-23-49]}},
    url = {https://github.com/NatLabRockies/PVade},
    year = {2023}
}
```
