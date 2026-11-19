Installing PVade 
=================


On a Unix base machine 
--------------------------

PVade is a software that uses FEniCSx for its Finite Element Computation. 
For more information about FEniCSx please refer to https://github.com/FEniCS/dolfinx.

In addition to FEniCSx, PVade uses multiple Python packages as part of the pre- and post-processing steps.
PVade dependencies are included in environment.yaml.

Installation
------------

PVade is available from PyPI (https://pypi.org/project/pvade/). There are three supported ways to install it: from PyPI (recommended for most users), from a source checkout for development, and into an existing HPC environment with externally provisioned native libraries. PVade itself is pip-installable, but pip does not install the native scientific stack (DOLFINx, PETSc, MPI) that full simulations require; that stack comes from Conda/Mamba or from the HPC site. PVade supports Python 3.10 only.

A. Install from PyPI
~~~~~~~~~~~~~~~~~~~~

You do not need to clone the repository. Download the runtime-only Conda environment definition from the official repository. It provisions Python 3.10, DOLFINx 0.6, PETSc, OpenMPI, and every Python dependency PVade needs, with the ``libcxx`` and setuptools pins validated for DOLFINx 0.6 on macOS::

   curl -fsSLO https://raw.githubusercontent.com/NatLabRockies/PVade/main/environment-runtime.yaml
   mamba env create -f environment-runtime.yaml
   mamba activate pvade

To reproduce the environment that belongs to a specific release, download the file from that release tag instead (for example ``.../PVade/v1.1.0/environment-runtime.yaml``).

Then install PVade into that environment without letting pip re-resolve the Conda-managed packages::

   python -m pip install --no-deps pvade

To pin a release, name it explicitly::

   python -m pip install --no-deps pvade==1.1.0

``--no-deps`` is recommended here because ``environment-runtime.yaml`` already provides every dependency. Without it, pip may not recognize Conda's ``python-gmsh`` as satisfying the ``gmsh`` requirement and install the PyPI ``gmsh`` wheel over it (observed on macOS arm64). That wheel is a different Gmsh version from the one the tests were run against, which changes the generated meshes and therefore slightly changes the numerical results. Because Conda's ``python-gmsh`` does not register pip metadata, ``python -m pip check`` reports ``pvade requires gmsh, which is not installed`` in this environment even though ``import gmsh`` works; use the verification commands below instead.

Verify the installation::

   python -m pip show pvade
   python -c "import pvade; print(pvade.__file__)"
   python -c "import gmsh; print(gmsh.__version__)"
   pvade --help
   python -m pvade --help

If you only want the command line help and the input schema, without running simulations, ``python -m pip install pvade`` into any Python 3.10 environment is sufficient. Running a simulation needs the native stack above.

The YAML input file is user-supplied. The example inputs are in the source repository and are not part of the installed package; download one without cloning::

   curl -fsSLO https://raw.githubusercontent.com/NatLabRockies/PVade/main/examples/panels2d.yaml
   pvade --input_file panels2d.yaml

If the native environment has site-specific constraints, follow the HPC instructions below instead.

B. Developer installation from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Developers work from a clone of the repository and use the full development environment defined in ``environment.yaml``. Its environment name is ``pvade``::

   git clone https://github.com/NatLabRockies/PVade.git
   cd PVade
   mamba env create -f environment.yaml
   mamba activate pvade

The environment file installs FEniCSx/DOLFINx, MPICH, the Python libraries needed by PVade, and the testing and documentation tools. After activating it, install the checkout using a separate pip command::

   python -m pip install --no-deps -e .

Run the test suite from the repository root after making changes (see :doc:`testing`)::

   pytest -sv pvade/tests

Editable mode makes source changes immediately visible; ``--no-deps`` leaves dependency management to Conda so pip does not replace or re-resolve MPI/PETSc-related packages. The pip command is deliberately separate from the environment file's ``pip:`` requirements because Conda treats entries in that list as requirements and does not accept pip install options such as ``--no-deps`` there.

Install from source in an existing environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the environment already exists and PVade has not yet been installed into it, run this from the repository root while it is active::

   python -m pip install --no-deps -e .

For a non-editable installation from the checkout, use ``python -m pip install --no-deps .`` instead. Both commands install the ``pvade`` console command. Install the DOLFINx/PETSc/MPI stack first using the supported Conda environment or compatible HPC modules; these native components are intentionally not resolved by pip.

C. Verify installation
~~~~~~~~~~~~~~~~~~~~~~

Run these commands in the activated environment::

   python -m pip show pvade
   python -c "import pvade; print(pvade.__file__)"
   pvade --help
   python -m pvade --help

For a PyPI installation, ``pvade.__file__`` should point into the environment's ``site-packages``; for a developer installation it points into your checkout.

D. Run PVade
~~~~~~~~~~~~

The installed command is the primary interface. Give it the path to a YAML input file::

   pvade --input_file /path/to/your/input.yaml

The same run can be started through Python::

   python -m pvade --input_file /path/to/your/input.yaml

For an MPI run, use the launcher from the activated environment::

   mpirun -np 2 pvade --input_file /path/to/your/input.yaml

From a source checkout, the original script invocation remains supported as a backward-compatible interface::

   python pvade_main.py --input_file examples/panels2d.yaml

``--input`` is accepted as a shorthand for ``--input_file``. Individual input parameters can be overridden on the command line, for example ``--solver.t_final 0.01``. See :doc:`running_pvade` for details.

E. HPC installations
~~~~~~~~~~~~~~~~~~~~

On HPC systems, keep the site's working MPI, PETSc, and DOLFINx stack. Install PVade into an existing compatible environment (a site Conda/Mamba environment or a virtual environment built on the site modules) that already provides DOLFINx, PETSc, mpi4py, and the ordinary Python dependencies declared by PVade (``gmsh``, ``h5py``, ``jsonschema``, ``numba``, ``numpy``, ``pandas``, ``PyYAML``, ``scipy``, ``tqdm``). In that situation install the published release without allowing pip to modify the environment::

   python -m pip install --no-deps pvade

This option is appropriate when the environment is already validated for your site and you do not want pip to change MPI-linked or other native packages. For development from a source checkout, use ``python -m pip install --no-deps -e .`` from the repository root instead. Do not use ``--no-deps`` unless every dependency declared by PVade is already importable in that environment, and do not use pip to replace a site-provided native stack. Launch parallel jobs with the launcher your site's MPI requires (see :doc:`hpc_jobs`).

To obtain Mamba, we can use the following resource: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html.

To obtain Conda, we can use the following resource: https://conda.io/projects/conda/en/latest/user-guide/install/index.html.

.. Note::
   We recommend using Mamba for its fast installation of the environment.



Building Mamba Environment
--------------------------

The Conda/Mamba environment creation commands are given above. To test the DOLFINx and MPI installation, run the following example::
  
  mpirun -np $num_cores python -u $PVade/tutorials/poissoneq.py 64  cg none 1

The example solves a Poisson's equation in 3 dimensions using 64 elements and 1st order Lagrange shape functions with cg as the ksp solver and no pre-conditioners. 
For more details about the Poisson's problem, we refer the user to the following link: https://jsdokken.com/dolfinx-tutorial/chapter1/fundamentals.html 



On a Windows machine
------------------------------------------------------------------------------

See the `Instructions for DOLFINx <https://github.com/FEniCS/dolfinx/blob/main/README.md>`_
for background. Four installation options are described below, in order of
recommendation.

Option 1: Using WSL2 (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the easiest method to set up, access, and understand.

1. Check whether WSL2 is already installed. A Windows 11 computer should have
   WSL natively. In a command prompt, run ``wsl --status`` to check whether you
   have WSL version 2, which is generally preferred.
2. Install a Ubuntu distro in WSL2. In a command prompt, run::

     wsl --install

   You will be prompted to create a username and password. After installation,
   your prompt will be logged in to Ubuntu on WSL. You can also access this
   prompt later by searching your apps for Ubuntu.
3. In Ubuntu, install the DOLFINx environment::

     add-apt-repository ppa:fenics-packages/fenics
     apt update
     apt install fenicsx

   This may take up to an hour to install.
4. After installation, access your environment by opening Ubuntu. Use ``apt``
   or ``pip`` to install any additional packages you need. To access this
   environment in VSCode, use the
   `WSL extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl>`_,
   which works similarly to remotely accessing HPC systems through SSH with the
   `SSH extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh>`_.

Option 2: Using Docker
~~~~~~~~~~~~~~~~~~~~~~~

If you are already comfortable with Docker, we recommend using Docker for
DOLFINx; otherwise, we recommend WSL2 instead.

1. `Install <https://docs.docker.com/desktop/setup/install/windows-install/>`_ Docker.
   Docker Desktop requires a license for large organizations such as NLR;
   check license availability before proceeding. A Docker Desktop license is
   not necessary for installing a DOLFINx environment in Docker.
2. Docker uses images, which are recipes for programming environments, and
   containers, which are instances based on an image. Containers can be
   created and destroyed, entered and exited.
3. Create and start a container by running::

     docker run --name fenicsx -ti dolfinx/dolfinx:nightly

   The image ``dolfinx/dolfinx:nightly`` can be replaced with other options
   listed in the instructions; in most cases we recommend
   ``dolfinx/dolfinx:stable``.
4. The first time this command is run, it also pulls the image data, which may
   take up to 20 minutes. Running the command again creates a new container
   from the same image; in that case, leave out or change the
   ``--name fenicsx`` tag, and expect it to take far less time since the image
   is already pulled.
5. A container runs one command. By default, that command opens a terminal.
   When you exit that terminal, the container also exits.
6. Re-enter a Docker container by running::

     docker start -i fenics

   Exiting and re-entering containers keeps data such as downloaded files and
   installed packages on top of the original image. Removing and re-creating a
   container does not keep this data; only the original image is preserved.
7. To install additional packages, use ``pip`` while inside your Docker
   container.

Option 3: Using Conda
~~~~~~~~~~~~~~~~~~~~~~

.. note::

   As of this writing, ``mpich`` and ``fenics-dolfinx`` are not available for
   Windows on conda-forge, so this option is not currently possible. It is
   included here in case that changes.

Windows supports Miniconda and Anaconda. Current DOLFINx instructions read::

   conda create -n fenicsx-env
   conda activate fenicsx-env
   conda install -c conda-forge fenics-dolfinx mpich pyvista

On conda-forge, ``pyvista`` supports Windows, but ``mpich`` and
``fenics-dolfinx`` do not. If that changes, you could use conda environments on
Windows by:

1. Installing Miniconda or Anaconda
2. Opening Anaconda prompt
3. Following the above instructions to create and set up the environment

Option 4: Using Spack
~~~~~~~~~~~~~~~~~~~~~~

Windows only technically supports Spack, per
`these instructions <https://spack.readthedocs.io/en/latest/getting_started.html#spack-on-windows>`_.
Follow this procedure:

1. Install prerequisites: VSCode with C++ compiler options, Python, and Git.
2. Clone Spack::

     git clone https://github.com/spack/spack.git

3. Open a spack prompt by running ``bin\spack_cmd.bat``.
4. Set up Spack::

     spack compiler find
     spack external find cmake
     spack external find ninja

5. Set up your Spack environment::

     spack env create fenicsx-env
     spack env activate fenicsx-env
     spack add fenics-dolfinx+adios2 py-fenics-dolfinx cflags="-O3" fflags="-O3"
     spack install


On NLR HPC machine Kestrel 
----------------------------

In order to use PVade on Kestrel, we can use one of the two options.

* A conda/mamba installation 
* Loading FEniCSx as a module  



1. conda/mamba installation

In order to install PVade, it is recommended to use a compute node. 
You can allocate one and use it interactively through: 

.. code:: bash

   ~$ salloc --nodes=1 --time=4:00:00 --partition=$partition_name --account $account_name --mem=0 --exclusive

Make sure you specify the partition name ``$partition_name`` and the account name ``$account_name``. 
Next, we clone the repository from https://github.com/NatLabRockies/PVade.

.. code:: bash

   ~$ git clone https://github.com/NatLabRockies/PVade.git

.. note:: 
   the same can be achieved by downloading the latest release from https://github.com/NatLabRockies/PVade/releases


We will refer to ``$PVade`` as the location of the cloned repo. 
We change the directory to ``$PVade`` and load mamba. 


.. code:: bash

   ~$ cd $PVade/
   ~$ module unload PrgEnv-cray/8.3.3
   ~$ module load mamba 


.. note::

   The same can be achieved by using Conda.
   Mamba was shown to be faster.

The repository environment is named ``pvade`` and already installs PVade itself.

.. code::

   ~$ mamba env create -f environment.yaml
   ~$ mamba activate pvade

To test the installation we can run an example using the command:

.. code::

   mpirun -np $num_cores python -u $PVade/tutorials/poissoneq.py 64  cg none 1

The example solves a Poisson's equation in 3 dimensions using 64 elements and 1st order Lagrange shape functions with cg as the ksp solver and no pre-conditioners. 

.. note::

   The conda installed PVade requires the use of mpirun instead of srun since it was not configured against Slurm.

   
   
2. Module access 

On Kestrel, PVade is installed and available as a module. 
PVade can be accessed by loading:

.. code::

   module load fenicsx

This instance of PVade leverages a FEniCSx installation that leverages GNU Programming environment and cray-mpich for its mpi communication.

