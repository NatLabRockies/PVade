"""Command-line entry point for PVade."""

import argparse
from importlib import resources
import sys

import yaml


def _add_input_schema_arguments(parser):
    schema_path = resources.files("pvade.IO").joinpath("input_schema.yaml")
    with schema_path.open("r", encoding="utf-8") as schema_file:
        schema = yaml.safe_load(schema_file)

    def add_properties(properties, prefix=""):
        for name, definition in properties.items():
            key = f"{prefix}.{name}" if prefix else name
            if definition.get("type") == "object":
                add_properties(definition.get("properties", {}), key)
                continue

            schema_type = definition.get("type")
            if isinstance(schema_type, list):
                argument_type = str
            elif schema_type == "number":
                argument_type = float
            elif schema_type == "integer":
                argument_type = int
            elif schema_type == "string":
                argument_type = str
            else:
                argument_type = None

            help_text = definition.get("description", "")
            units = definition.get("units")
            if units:
                help_text = f"{help_text} (Units = {units})"
            parser.add_argument(f"--{key}", metavar="", type=argument_type, help=help_text)

    add_properties(schema.get("properties", {}))


def main():
    """Run PVade, handling help without importing the native solver stack."""
    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        parser = argparse.ArgumentParser(
            prog="pvade",
            description="Run a PVade fluid-structure interaction simulation.",
            epilog=(
                "Simulation parameters may also be overridden with options such "
                "as --solver.dt. DOLFINx, PETSc, and MPI must be installed."
            ),
        )
        parser.add_argument(
            "--input_file",
            "--input",
            dest="input_file",
            metavar="",
            help="Path to the simulation input YAML file (--input_file is an alias).",
        )
        _add_input_schema_arguments(parser)
        parser.parse_args()
        return

    from pvade.application import cli

    cli()