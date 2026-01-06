# POSCAR Supercell Generator with Random Substitution (LAMMPS Output)

This script generates a **3D supercell** from a VASP `POSCAR`-style file, applies **random atomic substitutions**, and exports the resulting structure in **LAMMPS data format**.

It is intended for **atomistic simulation setup**, particularly for studying **random dopant distributions** in crystalline materials.

---

## Overview

Given:
- A unit cell defined in a POSCAR-like file
- Lattice parameters
- Supercell dimensions

The script:
1. Reads atomic species and fractional coordinates from the POSCAR
2. Replicates the unit cell into a supercell (`nx × ny × nz`)
3. Applies **random element substitution logic** during replication
4. Converts fractional coordinates to Cartesian coordinates
5. Writes a **LAMMPS-compatible data file**

---

## Input Files

### Required
- **POSCAR file** (VASP format)
