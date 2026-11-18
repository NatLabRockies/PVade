"""Backward-compatible script entry point for PVade."""

from pvade.cli import main as _cli


def main(input_file=None):
    """Run the PVade application, preserving the legacy importable API."""
    from pvade.application import main as run_application

    return run_application(input_file)


if __name__ == "__main__":
    _cli()
