#!/usr/bin/env bash
# Usage: validate_release_install.sh <wheel path or pip requirement> <source checkout> <release tag>
#
# Optional environment variables:
#   PVADE_PIP_INSTALL_ARGS    extra pip install arguments, e.g. --no-deps
#   PVADE_SKIP_PIP_CHECK=1    skip `pip check` (Conda's python-gmsh has no pip metadata)
#   PVADE_TEST_SOURCE_SCRIPT=0  skip running the checkout's pvade_main.py; that script
#                             imports the checkout's pvade package rather than the installed one
set -euo pipefail

wheel_path="$1"
source_root="$(cd "$2" && pwd)"
release_tag="$3"
expected_version="${release_tag#v}"
runner_temp="${RUNNER_TEMP:-/tmp}"

python -m pip uninstall -y pvade
# shellcheck disable=SC2086
python -m pip install --no-cache-dir ${PVADE_PIP_INSTALL_ARGS:-} "$wheel_path"
if [ "${PVADE_SKIP_PIP_CHECK:-0}" != "1" ]; then
    python -m pip check
fi
cd "$runner_temp"
unset PYTHONPATH 2>/dev/null || true

PVADE_SOURCE_ROOT="$source_root" EXPECTED_PVADE_VERSION="$expected_version" python - <<'PY'
import os
from importlib import metadata, resources
from pathlib import Path

import pvade

source_root = Path(os.environ["PVADE_SOURCE_ROOT"]).resolve()
expected_version = os.environ["EXPECTED_PVADE_VERSION"]
module_path = Path(pvade.__file__).resolve()
try:
    module_path.relative_to(source_root)
except ValueError:
    pass
else:
    raise AssertionError(f"PVade imported from source checkout: {module_path}")

assert metadata.version("pvade") == expected_version
assert resources.files("pvade.IO").joinpath("input_schema.yaml").is_file()
print(f"Installed pvade {metadata.version('pvade')} from {module_path}")
PY

pvade --help > "$runner_temp/pvade-cli-help.txt"
grep -q -- '--input' "$runner_temp/pvade-cli-help.txt"
grep -q -- '--input_file' "$runner_temp/pvade-cli-help.txt"
grep -q -- '--solver.dt' "$runner_temp/pvade-cli-help.txt"
python -m pvade --help > "$runner_temp/pvade-module-help.txt"
grep -q -- '--input' "$runner_temp/pvade-module-help.txt"
python -m pvade_main --help > "$runner_temp/pvade-main-module-help.txt"
grep -q -- '--input_file' "$runner_temp/pvade-main-module-help.txt"

legacy_script="$(python -c 'from importlib.util import find_spec; print(find_spec("pvade_main").origin)')"
python "$legacy_script" --help > "$runner_temp/pvade-legacy-help.txt"
grep -q -- '--input_file' "$runner_temp/pvade-legacy-help.txt"

python -m pvade --input_file "$source_root/examples/panels2d.yaml" \
    --general.output_dir "$runner_temp/pvade-pypi-module" \
    --general.mesh_only true

python "$legacy_script" --input_file "$source_root/examples/panels2d.yaml" \
    --general.output_dir "$runner_temp/pvade-pypi-legacy" \
    --general.mesh_only true

if [ "${PVADE_TEST_SOURCE_SCRIPT:-1}" = "1" ]; then
    python "$source_root/pvade_main.py" --input_file "$source_root/examples/panels2d.yaml" \
        --general.output_dir "$runner_temp/pvade-main-source" \
        --general.mesh_only true
fi

pvade --input "$source_root/examples/panels2d.yaml" \
    --general.output_dir "$runner_temp/pvade-pypi-single" \
    --solver.t_final 0.001
test -s "$runner_temp/pvade-pypi-single/logfile.log"

mpiexec -n 2 pvade --input_file "$source_root/pvade/tests/input/yaml/flag2d.yaml" \
    --general.output_dir "$runner_temp/pvade-pypi-mpi"
test -s "$runner_temp/pvade-pypi-mpi/solution/solution_fluid.xdmf"
test -s "$runner_temp/pvade-pypi-mpi/solution/lift_and_drag.csv"

