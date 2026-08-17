# LatticeFlow

## Parametric CFD Analysis of Additively Manufactured Lattice Structures

LatticeFlow is a computational materials engineering project investigating how the geometry and porosity of additively manufactured lattice structures influence fluid-flow behavior.

The project combines **parametric CAD, Python automation, and OpenFOAM computational fluid dynamics (CFD)** to create a reproducible workflow from lattice design to fluid-flow analysis.

---

## Project Objective

The initial objective is to investigate the relationship between:

* Lattice topology
* Porosity
* Strut diameter
* Fluid velocity
* Pressure drop
* Permeability

The first study will focus on a **Body-Centered Cubic (BCC)** lattice structure.

The eventual workflow will be:

```text
Target Porosity
       ↓
Python Parametric Calculator
       ↓
Strut Diameter
       ↓
Fusion 360 Parametric CAD
       ↓
Lattice Geometry
       ↓
STL
       ↓
OpenFOAM
       ↓
CFD Simulation
       ↓
Pressure Drop / Velocity Field
       ↓
Permeability
       ↓
Python Analysis
```

---

# Milestone 1 — Parametric BCC Geometry

The first milestone establishes the parametric CAD foundation for the project.

### Initial geometry

The baseline BCC unit cell currently uses:

| Parameter              |      Value |
| ---------------------- | ---------: |
| Topology               |        BCC |
| Unit-cell size         |       5 mm |
| Initial strut diameter |     0.5 mm |
| CAD software           | Fusion 360 |

The initial BCC geometry has a measured solid volume of:

[
V_{solid}=6.183\text{ mm}^3
]

The total unit-cell volume is:

[
V_{cell}=5^3=125\text{ mm}^3
]

Therefore, the measured initial porosity is approximately:

[
\epsilon
========

1-\frac{6.183}{125}
]

[
\boxed{\epsilon\approx95.05%}
]

This measurement will be used as an initial reference point for calibrating the parametric geometry model.

---

## Parametric Design Strategy

Rather than manually creating separate CAD models for every porosity, the lattice will be driven by a small set of design parameters.

The primary parameters will be:

```text
unit_cell_size
strut_diameter
target_porosity
lattice_dimensions
```

The desired long-term relationship is:

```text
Target Porosity
       ↓
Calculate Strut Diameter
       ↓
Update Fusion Parameter
       ↓
Regenerate Lattice
       ↓
Verify Actual Porosity
```

### Why use porosity as the design variable?

Porosity is more useful for comparing different lattice structures than strut diameter alone.

A future comparison between BCC, FCC, and Gyroid structures should allow equivalent porosities to be compared:

```text
BCC       ─┐
           ├── 70% porosity
FCC       ─┤
           ├── 80% porosity
Gyroid    ─┘
           └── 90% porosity
```

This allows differences in fluid behavior to be attributed more directly to **topology and geometry**, rather than simply differences in material volume.

---

# Python Parametric Calculator

A preliminary Python calculator will estimate the strut diameter required for a target BCC porosity.

The initial analytical model treats the lattice members as cylindrical struts.

For a BCC unit cell, the approximate total strut length associated with one unit cell is:

[
L=(3+\sqrt{3})a
]

The approximate solid volume is therefore:

[
V_s =
\frac{\pi d^2}{4}(3+\sqrt{3})a
]

where:

* (a) = unit-cell size
* (d) = strut diameter

Porosity is:

[
\epsilon =
1-\frac{V_s}{a^3}
]

This provides an initial estimate for (d).

### Important limitation

The analytical model is an approximation.

The actual Fusion geometry contains intersecting struts, and the resulting solid volume may differ from the idealized cylindrical calculation.

Therefore, the project will eventually use measured Fusion geometry to establish an empirical relationship:

[
\epsilon=f(d)
]

This relationship can then be inverted to determine:

[
d=f^{-1}(\epsilon)
]

for a desired target porosity.

---

# Planned Automation

The eventual CAD workflow will connect the Python calculator directly to Fusion 360's parametric model.

The intended workflow is:

```text
Python
  │
  ├── Target porosity
  ├── Unit-cell size
  └── Topology
          │
          ↓
   Calculate strut diameter
          │
          ↓
    Fusion 360 parameter
          │
          ↓
    Regenerate geometry
          │
          ↓
       Export STL
```

This will allow multiple lattice designs to be generated without manually remodeling each case.

---

# Planned CFD Study

Once the parametric BCC geometry has been validated, the project will transition to OpenFOAM.

The initial CFD investigation will examine:

### Independent variables

* Lattice topology
* Porosity
* Strut diameter
* Fluid velocity

### Dependent variables

* Pressure drop
* Velocity distribution
* Permeability
* Reynolds number
* Wall shear stress

The primary relationship of interest is:

[
K=\frac{\mu L U}{\Delta P}
]

where:

* (K) = permeability
* (\mu) = dynamic viscosity
* (L) = lattice length
* (U) = superficial velocity
* (\Delta P) = pressure drop

At higher flow rates, the study may be extended to the Darcy–Forchheimer relationship:

[
\frac{\Delta P}{L}
==================

\frac{\mu}{K}U+\beta\rho U^2
]

This will allow the project to investigate both viscous and inertial contributions to pressure loss.

---

# Planned Lattice Study

The initial parameter space will eventually include multiple porosity levels:

```text
70%
75%
80%
85%
90%
```

and multiple lattice topologies:

```text
BCC
FCC
Gyroid
```

The first phase, however, will focus exclusively on **BCC** to establish and validate the workflow before introducing additional geometries.

---

# Validation Strategy

The CFD results will not be treated as valid simply because the solver converges.

The project will include:

### Mesh independence

A representative case will be simulated using multiple mesh resolutions.

```text
Coarse
   ↓
Medium
   ↓
Fine
```

Pressure drop and permeability will be compared to determine whether the solution is sufficiently mesh-independent.

### Analytical comparison

Results will be compared with appropriate porous-flow relationships, including Darcy's law where applicable and Darcy–Forchheimer behavior at higher Reynolds numbers.

### Geometry verification

The actual CAD porosity will be calculated from the Fusion solid volume rather than assuming that the analytical geometry exactly matches the manufactured CAD representation.

---

# Future Development

After the CFD workflow is established, the project may be expanded to include:

* FCC lattice structures
* Gyroid structures
* Automated Fusion geometry generation
* Automated OpenFOAM case generation
* CFD parameter sweeps
* Mesh-convergence automation
* Darcy–Forchheimer analysis
* Permeability prediction
* CFD result visualization
* Machine-learning surrogate modeling
* Lattice topology optimization

The eventual goal is to create a workflow capable of answering:

> **Given a desired porosity and flow requirement, which lattice geometry provides the best balance between permeability and pressure drop?**

---

# Current Status

### Milestone 1 — Parametric Geometry

* [x] Select project scope
* [x] Select BCC as initial topology
* [x] Create initial 5 mm BCC unit cell
* [x] Establish initial 0.5 mm strut diameter
* [x] Measure CAD solid volume
* [x] Calculate initial actual porosity
* [ ] Create Fusion user parameters
* [ ] Make strut diameter fully parametric
* [ ] Develop Python porosity calculator
* [ ] Validate calculated diameter against Fusion geometry
* [ ] Automate Fusion parameter updates
* [ ] Generate first multi-porosity geometry set

### Upcoming

**Next milestone:**

> Establish a fully parametric BCC unit cell where target porosity can be converted into a strut diameter and verified against the resulting Fusion geometry.

---

## Technology Stack

**CAD**

* Autodesk Fusion 360

**Programming**

* Python
* NumPy
* Pandas
* Matplotlib

**CFD**

* OpenFOAM

**Geometry**

* STL

**Analysis**

* Darcy's law
* Darcy–Forchheimer model
* Mesh independence analysis
* Parametric design analysis

---

## Project Philosophy

The goal of LatticeFlow is not simply to produce CFD visualizations.

The project is designed as a **reproducible computational engineering workflow** in which:

> **CAD geometry → physical parameters → numerical simulation → engineering quantities → validated conclusions**

Each stage will be automated and validated where practical, with computational efficiency and reproducibility treated as engineering requirements rather than afterthoughts.
