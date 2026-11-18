# PVade

`PVade` is an open source fluid-structure interaction model which can be used to study wind loading and stability on solar-tracking PV arrays. `PVade` can be used as part of a larger modeling chain to provide stressor inputs to mechanical module models to study the physics of failure for degradation mechanisms such as cell cracking, weathering of cracked cells, and glass breakage. For more information, visit the [PVade Documentation](https://pvade.readthedocs.io/en/latest/index.html).

[![test_pvade](https://github.com/NatLabRockies/PVade/actions/workflows/test_pvade.yaml/badge.svg)](https://github.com/NatLabRockies/PVade/actions/workflows/test_pvade.yaml)
[![Documentation Status](https://readthedocs.org/projects/pvade/badge/?version=latest)](https://pvade.readthedocs.io/en/latest/?badge=latest)

## Getting Started

New users are encouraged to review the [installation guide](https://pvade.readthedocs.io/en/latest/installing_pvade.html) for the supported Conda environment and package installation instructions.

PyPI installation instructions for PVade 1.1.0, the first public distribution, are pending successful publication. The Conda/Mamba developer workflow below is available now.

## Quick Start

1. From the repository root, create the supported scientific-computing environment:
    ```bash
    mamba env create -f environment.yaml
    ```
    Activate the environment:
    ```bash
    mamba activate pvade
    ```
    Install the checkout in editable mode without asking pip to re-resolve Conda-managed dependencies:
    ```bash
    python -m pip install --no-deps -e .
    ```
2. Verify the package and command:
    ```bash
    python -m pip show pvade
    python -c "import pvade; print(pvade.__file__)"
    pvade --help
    ```
3. Run an example from the repository root:
   ```bash
    pvade --input examples/panels2d.yaml
   ```

Both `--input` and `--input_file` are accepted. To install from a source checkout into an already provisioned environment, run `python -m pip install --no-deps .`. PyPI installation instructions are pending the first public release.



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
