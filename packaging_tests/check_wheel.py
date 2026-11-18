"""Verify that a built PVade wheel contains the installable package surface."""

import json
import sys
import zipfile
from pathlib import Path

from packaging.specifiers import SpecifierSet


wheel_path = Path(sys.argv[1])
repository_root = Path(__file__).resolve().parents[1]
codemeta = json.loads((repository_root / "codemeta.json").read_text(encoding="utf-8"))
with zipfile.ZipFile(wheel_path) as wheel:
    names = set(wheel.namelist())
    required_files = {
        "pvade/__init__.py",
        "pvade/__main__.py",
        "pvade/application.py",
        "pvade/cli.py",
        "pvade/IO/__init__.py",
        "pvade/IO/input_schema.yaml",
        "pvade/fluid/FlowManager.py",
        "pvade/fsi/FSI.py",
        "pvade/geometry/MeshManager.py",
        "pvade/structure/StructureMain.py",
        "pvade_main.py",
    }
    missing = required_files - names
    assert not missing, f"wheel is missing required files: {sorted(missing)}"
    assert not any(name.startswith("pvade/tests/") for name in names)
    assert not any(name.endswith((".h5", ".xdmf")) for name in names)

    metadata_path = next(name for name in names if name.endswith(".dist-info/METADATA"))
    metadata = wheel.read(metadata_path).decode("utf-8")
    assert "Name: pvade\n" in metadata
    assert f"Version: {codemeta['version']}\n" in metadata
    requires_python = next(
        line.partition(": ")[2]
        for line in metadata.splitlines()
        if line.startswith("Requires-Python:")
    )
    assert SpecifierSet(requires_python) == SpecifierSet(">=3.10,<3.11")
    assert "License-Expression: BSD-3-Clause\n" in metadata

    entry_points_path = next(
        name for name in names if name.endswith(".dist-info/entry_points.txt")
    )
    entry_points = wheel.read(entry_points_path).decode("utf-8")
    assert "pvade = pvade.cli:main" in entry_points

print(f"Validated wheel contents: {wheel_path}")