from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--input-file",
        action="store",
        default=None,
        help="Run test only for a specific input YAML file",
    )


def pytest_generate_tests(metafunc):
    if "input_file" not in metafunc.fixturenames:
        return

    input_file_arg = metafunc.config.getoption("input_file")

    if input_file_arg:
        metafunc.parametrize("input_file", [Path(input_file_arg)])
    else:
        # Resolve relative to location of conftest.py (PVade/); prefer a
        # local, untracked "input" dir if present, else fall back to the
        # tracked "examples" dir shipped with the repo.
        this_dir = Path(__file__).resolve().parent  # PVade/
        input_dir = this_dir / "input"
        if not input_dir.is_dir() or not sorted(input_dir.glob("*.yaml")):
            input_dir = this_dir / "examples"

        all_files = sorted(input_dir.glob("*.yaml"))
        if not all_files:
            raise RuntimeError(f"No input files found in {input_dir}")
        metafunc.parametrize("input_file", all_files)
