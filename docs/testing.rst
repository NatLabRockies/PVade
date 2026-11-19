========
Testing
========

This section covers the automated test suite used to validate PVade changes.
The tests live under ``pvade/tests/`` and are executed with ``pytest``.

Test Layout
-----------

- ``pvade/tests/test_input_files.py``: validates that the example and tutorial
  input files can be parsed
- ``pvade/tests/test_Parameters.py``: checks parameter handling and defaults
- ``pvade/tests/test_mesh_movement.py``: exercises mesh motion behavior
- ``pvade/tests/test_fsi_mesh.py``: checks coupled mesh setup
- ``pvade/tests/test_transfer_facet_tags.py``: verifies mesh tag transfer
- ``pvade/tests/test_solve.py``: runs solver-level regression checks

Running Tests
-------------

From the repository root:

.. code-block:: bash

   conda run -n pvade pytest pvade/tests

To run a focused test module:

.. code-block:: bash

   conda run -n pvade pytest pvade/tests/test_Parameters.py

To run every YAML file in ``examples/`` end to end (mesh only and a short solve):

.. code-block:: bash

   pytest -sv test_all_inputs.py

Coverage
--------

``pytest-cov`` is part of the development environment. To measure how much of
the ``pvade`` package the tests exercise:

.. code-block:: bash

   pytest pvade/tests --cov=pvade --cov-report=term-missing

The report is informational and there is no coverage threshold. Simulations
launched as separate MPI processes (for example by ``test_all_inputs.py``) are
not included in the measurement.

Continuous Integration
----------------------

GitHub Actions runs the following workflows; each writes a summary of what it
checked to the run page.

- ``test_pvade``: the ``pvade/tests`` suite with coverage, every example input
  file, and Black formatting, on Ubuntu and macOS.
- ``test-packaging``: builds the source and wheel distributions, checks their
  metadata and contents, and installs the wheel in a clean environment.
- ``test-pypi``: installs the release published on PyPI and runs smoke
  simulations, including a two-rank MPI run. It runs weekly, on demand, and
  after each release is published.
- ``Publish to PyPI``: builds, validates and publishes a release when a GitHub
  release is published.

Markers
-------

The test suite defines the following pytest markers in ``pytest.ini``:

- ``unit``: short tests that complete quickly
- ``regression``: longer tests that compare against expected results

Additional Notes
----------------

- Test output artifacts are written under ``pvade/tests/output/``.
- When adding a new input file or tutorial case, consider adding a matching
  test in ``pvade/tests/``.