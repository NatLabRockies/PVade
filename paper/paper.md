---
title: "`PVade`: A Python package for simulating wind loading and aerodynamic
stability in solar-tracking PV arrays"
tags:
  - Python
  - astronomy
  - dynamics
  - galactic dynamics
  - milky way
authors:
  - name: Walid Arsalane
    # orcid: 0000-0000-0000-0000
    affiliation: 1 # (Multiple affiliations must be quoted)
    corresponding: true # (This is how to denote the corresponding author)
  - name: Ethan Young
    affiliation: 1
  - name: Brooke Stanislawski
    affiliation: 1
  - name: Xin He
    affiliation: 1
  - name: Martin Springer
    affiliation: 1
  - name: Andrew Glaws
    affiliation: 1
affiliations:
 - name: National Laboratory of the Rockies, Golden, CO, United States
   index: 1
date: 11 September 2026
bibliography: paper.bib

---

# Summary

Wind-driven degradation of single-axis tracking photovoltaic (PV) systems
encompasses a range of different phenomena, from small-scale fluctuating
pressures that can exacerbate cracks to large-scale "torsional galloping"
events which can lead to broken glass and catastrophic damage to tracker
hardware. Modern PV panels and mounting structures are particularly susceptible
to these phenomena, in large part due to industry trends toward larger module
areas, thinner layers of encapsulating glass, and lightweight mounting
components. Both the small- and large-scale dynamic responses to wind loading
are fundamentally driven by the same multi-physics interaction; namely, how
atmospheric flows induce loads on the panel surface and cascade through the
array, generating non-uniform deformation and displacement in the structure as
a function of both operational (e.g., tracker tilt angle) and design
(e.g., panel frame stiffness) choices.

To address these issues and provide actionable guidance for system owners, we
developed PV Aerodynamic Design Engineering (`PVade`) [@pvade:2023], an
open-source, HPC simulation framework capable of resolving the full
fluid-structure interaction (FSI) between multiple rows of compliant PV
hardware and realistic wind loading. `PVade` predicts pressure distributions on
the panel surfaces, inertial dynamics of hardware elements, and predictions of
aeroelastic instabilities across a range of different weather conditions,
operating choices, and design choices. These outcomes provide guidance on which
tracker tilt angles are more or less stable in a given weather condition and
feedback on the efficacy of strengthening measures. Additionally, `PVade`
outputs (e.g., time-varying pressure maps) can be used as part of a larger,
co-simulation framework to predict the drivers of microcrack growth from a
micro-scale model subjected to accurate wind loading boundary conditions. 


# Statement of need

Wind-induced mechanical degradation remains one of the most difficult
reliability challenges for PV systems. Existing computational approaches either
treat panels and mounting structures as rigid bodies, approximate multi-row
effects with periodic boundary conditions, or require a prohibitively high
computational cost to capture the coupled FSI between wind and hardware. This
limits their ability to capture fluttering and torsional galloping events,
ignores differences between perimeter and interior effects, or fails to capture
the cascade of waking and complex loading conditions associated with interior
rows with multiple upstream neighbors, respectively. Researchers and system
owners alike need realistic stressor inputs (e.g., pressure, inertial dynamics,
and deformations) to integrate into mechanical module models for crack
weathering, glass breakage, and wind stow and deployment guidance. Industry
partners need tools to study layout choices, tracker stiffness, panel
thickness, and inter-row spacing to mitigate wind-related degradation.
Importantly, prior work within the Durable Module Materials
(DuraMAT) Consortium [@duramat:2023] has demonstrated that mounting hardware
dynamics play a critical role in amplifying small motions into destructive
rotations, but there is no existing open-source, HPC-capable modeling framework
that can capture these FSI instabilities across multi‑row PV arrays. This
software fills that gap by providing an accurate, scalable framework that
integrates high-fidelity CFD, structural dynamics, and mesh motion into a
single accessible tool.


# State of the field

Outside DuraMAT and the field of PV, open-source computational fluid dynamics
(CFD) solvers exist, but adapting them to the fluid and structure boundary
conditions defined by single-axis tracking systems and adapting the mesh for
the specifics of large-scale fluttering is a significant barrier to entry for
new users. 


# Software design

`PVade` is designed as a modular, component-based multiphysics simulation
framework built on top of `FEniCSx` for finite element discretization and
solution of partial differential equations
[@dolfinx:2023; @ScroggsEtal2022; @AlnaesEtal2014] and `Gmsh` for geometry
construction and mesh generation [@gmsh:2009] . The architecture is organized
into five primary modules---Geometry, I/O, Fluid, Structure, and FSI---which
collectively define the core structure and execution workflow of the framework.
This modular design enables separation of concerns between geometry generation,
physics definition, coupling, and data management, improving maintainability
and extensibility.

The Geometry module is responsible for converting user-defined inputs into
computational meshes. `PVade` supports multiple geometries including two- and
three-dimensional cylinders (used for benchmarking and verification),
photovoltaic (PV) modules in 2D and 3D, a 2D flag configuration, and a 3D
heliostat model. The geometry subsystem is centered around a MeshManager
component, which either reads externally generated meshes in XDMF format or
constructs meshes from scratch. Mesh creation begins with a domain-specific
geometry definition file corresponding to each supported configuration. Once
the geometric domain is defined, mesh generation proceeds through facet and
volume initialization, element length scale definition, and boundary tagging.
The module outputs both XDMF mesh files and distributed mesh objects compatible
with `FEniCSx` for subsequent physics solves.

The I/O module manages input parsing, data formatting, logging, and solution
output. It controls the transfer of data between physics modules, supports
interpolation required for mesh motion in multiphysics simulations, and handles
generation of mesh and solution files in XDMF format. All simulation inputs are
provided through YAML configuration files, while output files---including mesh
and solution fields---are written in XDMF format to ensure compatibility with
standard post-processing tools.

The Fluid module defines all fluid-related variables and governing equations.
This includes formulation of the variational statements, boundary condition
specification, matrix assembly, and solution of the discretized fluid PDE
system using the finite element capabilities of `FEniCSx`.

The Structure module encapsulates structural physics models, including
elasticity, thermal analysis, and modal analysis. Boundary conditions are
defined and applied according to the selected structural physics model. A
central structural driver coordinates the interaction between different
structural analyses while maintaining modular separation of each physical
formulation.

The FSI module manages mesh motion and coupling in fluid--structure interaction
simulations. It coordinates data transfer between fluid and structural domains,
leveraging the I/O module for consistent interpolation of field variables
between nonconforming meshes when necessary. This module ensures
synchronization of solution fields and mesh updates during coupled solves.

The execution of `PVade` is coordinated through a main driver script,
`pvade_main.py`, which orchestrates interactions between all modules.
Simulations are launched from the command line and require a YAML configuration
file specifying geometry, physics, solver, and runtime parameters. Default
input templates are provided for supported geometries and physics
configurations, and parameters may be overridden via command-line arguments to
facilitate testing and parametric studies.

The runtime workflow consists of input validation, mesh construction or loading,
physics initialization (including variational form definition and boundary
condition setup), solver configuration and matrix assembly, and finally the
solve phase. During the solve stage, each active physics module is executed,
coupled data are propagated as required, and solution fields are written to
disk. All physics models are discretized using finite element methods within
`FEniCSx`, which internally leverages scalable linear algebra and parallel
communication backends for high-performance execution.

![Flowchart view of `PVade` structure.](figures/PVade_flowchart2.png){ width=100% }


`PVade` follows a modular design philosophy that promotes extensibility and
maintainability. The framework is structured such that geometry definition,
physics modules, and input/output handling are encapsulated within independent
components. This separation enables the addition of new physics models,
geometries, or I/O capabilities without major restructuring of the existing
codebase. The modular organization minimizes cross-dependencies between
subsystems and supports incremental feature development.

New physics models can be incorporated within the existing Fluid or Structure
modules, depending on the governing equations and domain of application. Each
physics model defines its own variational formulation, material properties, and
boundary condition logic. Integration of a new physics capability is achieved
by registering it within the corresponding FluidMain or StructureMain driver,
which coordinates initialization, assembly, and solution procedures. This
approach preserves a consistent execution workflow while allowing expansion of
the supported multiphysics capabilities.

`PVade` is designed to operate seamlessly across computing environments ranging
from personal laptops to distributed-memory high-performance computing
(HPC) clusters. The framework relies exclusively on MPI-based parallelism and
does not currently support OpenMP threading or GPU acceleration. To simplify
deployment, an environment.yaml file is provided for installation via Conda or
Mamba (e.g., Miniforge), ensuring reproducible dependency management. This
environment specification enables straightforward setup across heterogeneous
systems with minimal configuration effort.

A comprehensive testing strategy is implemented using the pytest framework. Unit
and regression tests cover core functionality, including mesh generation,
boundary condition application, variational form assembly, and physics solves.
Automated testing ensures correctness across geometry configurations and
physics models, reducing the likelihood of regression errors as new features
are introduced.

Version control is managed through Git, with continuous integration
(CI) workflows hosted on GitHub. All tests are automatically executed on both
development and main branches upon code updates, ensuring stability and
consistency before changes are merged into the primary codebase.

For reproducibility, `PVade` is currently installable via Miniforge using the
provided Conda environment specification. Ongoing development efforts aim to
further enhance portability through containerized distributions and potentially
through the publication of a dedicated Conda package channel. These efforts are
intended to streamline deployment and ensure long-term reproducibility across
computational platforms.


# Research impact statement

`PVade` has been used to quantify the wind load on agrivoltaics systems
[@young:2024], the motion of floating PV systems [@rasmussen:2026], and the
wind flow profile through single-axis tracking arrays [@stanislawski:2026], all
enabled through partnerships with industry. Additionally, `PVade` is being
explored by renewable energy system insurers to quantify the risk associated
for different weather events, system layouts, and hardware choices. The
spatially varying load profiles from `PVade` are being used to inform new
tracker testing standards, specifically, the specification of non-uniform
mechanical loads. Finally, the outputs from `PVade` have been used by
colleagues at the Colorado School of Mines to construct datasets which can be
used to train fast, machine-learned surrogate models that can accurately
predict structural deformations without the large computational expense.


<!-- # Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }
 -->

# AI usage disclosure

No generative AI tools were used in the development of this software, the
writing of this manuscript, or the preparation of supporting materials.

# Acknowledgements

This work was authored by the National Laboratory of the Rockies for the U.S.
Department of Energy (DOE), operated under Contract No. DE-AC36-08GO28308.
Funding provided as part of the Durable Module Materials Consortium 2
(DuraMAT 2), funded by the U.S. Department of Energy Office of Critical
Minerals and Energy Innovation Integrated Energy Systems Office, agreement
number 38259. The views expressed in the article do not necessarily represent
the views of the DOE or the U.S. Government. The U.S. Government retains and
the publisher, by accepting the article for publication, acknowledges that the
U.S. Government retains a nonexclusive, paid-up, irrevocable, worldwide license
to publish or reproduce the published form of this work, or allow others to do
so, for U.S. Government purposes.

# References
