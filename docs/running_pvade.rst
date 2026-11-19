Running PVade
=============

This page shows how to launch PVade simulations with the installed ``pvade``
command. See :doc:`installing_pvade` for installation instructions.

Requirements
------------

- A working PVade environment (see :doc:`installing_pvade`)
- A valid YAML input file
- ParaView (optional, for visualization of XDMF outputs)

.. note::
   If a parameter is omitted in your YAML file, PVade uses the default value
   from the input schema.

Basic Command
-------------

With the PVade environment activated, run:

.. code-block:: bash

   pvade --input_file <path-to-yaml>

The same run can be started through Python:

.. code-block:: bash

   python -m pvade --input_file <path-to-yaml>

``--input`` is accepted as a shorthand for ``--input_file``. To run without
activating the environment, prefix the command with ``conda run -n pvade``.

Running In Parallel
-------------------

Use the MPI launcher from the activated environment and put it in front of the
``pvade`` command:

.. code-block:: bash

   mpirun -np 2 pvade --input_file <path-to-yaml>

On HPC systems, use the launcher your site's MPI requires (see :doc:`hpc_jobs`).

Source Checkout Interface
-------------------------

From a clone of the repository, the original script interface remains
supported and accepts the same arguments:

.. code-block:: bash

   python pvade_main.py --input_file examples/panels2d.yaml

Example Inputs
--------------

The example input files live in the ``examples`` directory of the
`repository <https://github.com/NatLabRockies/PVade/tree/main/examples>`_. They
are not part of the package installed from PyPI. If you installed from PyPI,
download one without cloning the repository:

.. code-block:: bash

   curl -fsSLO https://raw.githubusercontent.com/NatLabRockies/PVade/main/examples/panels2d.yaml
   pvade --input_file panels2d.yaml

The table below lists the example YAML files in the repository.

.. table:: Example cases and input files

   ================================ ================================================
   Case                             Input file
   ================================ ================================================
   Panels 2D                        examples/panels2d.yaml
   Panels 3D                        examples/panels3d.yaml
   Single heliostat 3D              examples/single_heliostat.yaml
   Heated panels 2D                 examples/heated_panels2d.yaml
   ================================ ================================================

Common Run Examples
-------------------

Panels 3D:

.. code-block:: bash

   pvade --input_file examples/panels3d.yaml

Panels 2D:

.. code-block:: bash

   pvade --input_file examples/panels2d.yaml


Output Location
---------------

Output files are written to the directory set by ``general.output_dir`` in your
input YAML. Typical contents include:

- Mesh files under a mesh subdirectory
- Solution files under a solution subdirectory
- A run log file named logfile.log

CLI Parameter Overrides
-----------------------

You can override YAML values from the command line using dotted keys:

.. code-block:: bash

   pvade --input_file examples/panels3d.yaml --solver.dt 0.001 --solver.t_final 0.01

More On Input Parameters
------------------------

For detailed parameter documentation, see :doc:`pvade_input_file` and
:doc:`input_schema`.

Controlling Terminal Verbosity
-------------------------------

PVade's terminal output is controlled by the ``PVADE_VERBOSITY`` environment
variable. It accepts three levels:

- ``0``: quiet mode; INFO messages are suppressed in the terminal (errors are
  always shown)
- ``1`` (default): INFO messages are printed from rank 0 only
- ``2``: verbose mode; INFO messages are printed from every MPI rank

Set it before launching a run, for example:

.. code-block:: bash

   PVADE_VERBOSITY=2 pvade --input_file examples/panels3d.yaml

.. note::
   ``PVADE_VERBOSITY`` only affects what is echoed to the terminal. The full
   set of INFO-level messages is always written to ``logfile.log`` in the
   run's output directory, regardless of the verbosity level.

.. toctree::
   :maxdepth: 1

   pvade_input_file
