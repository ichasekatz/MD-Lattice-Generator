#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:13:58 2024

@author: chasekatz
"""

import numpy as np
import os
import random

# Inputs
folder_directory = os.getcwd()

# Input unit cell dimensions
a = 3.97
b = 3.97
c = 7.49

# Input POSCAR file name
poscar_file = os.path.join(folder_directory, 'H2O2.poscar')

# Input number of unit cells in each direction
nx, ny, nz = 7, 7, 3

def read_poscar(poscar_file):
    unit_cell_atoms = []

    with open(poscar_file, 'r') as file:
        lines = file.readlines()

    element_line = lines[5].strip().split()
    count_line = lines[6].strip().split()

    elements = []
    for i, count in enumerate(count_line):
        elements.extend([element_line[i]] * int(count))

    positions_start = 8 if "Selective dynamics" in lines[7] else 8
    positions = lines[positions_start:positions_start + len(elements)]

    for i, line in enumerate(positions):
        x, y, z = map(float, line.split()[:3])
        unit_cell_atoms.append((elements[i], x, y, z, 1))

    return unit_cell_atoms

def positions(a, b, c, unit_cell_atoms, nx, ny, nz):
    positions = []
    unit = 0
    for i in range(nx):
        for j in range(ny):
            rand2 = random.sample(range(1, 148), 16)
            for k in range(nz):
                place = 0
                rand = random.sample(range(1, 5), 2)
                for atom in unit_cell_atoms:
                    element, x_frac, y_frac, z_frac, num = atom
                    if element == 'Nd':
                        place += 1
                        list1 = [1, 4, 5, 8]
                        list2 = [1, 2]
                        for m in list1:
                            if place == m:
                                for n in list2:
                                    for q in rand:
                                        if q == n:
                                            element = 'Dy'
                    if num == 1:
                        x = (i + x_frac) * a
                        y = (j + y_frac) * b
                        z = (k + z_frac) * c
                        positions.append((element, x, y, z))
                    if num >= 2:
                        for v in rand2:
                            if v == unit:
                                x = (i + x_frac) * a
                                y = (j + y_frac) * b
                                z = (k + z_frac) * c
                                positions.append((element, x, y, z))
                unit += 1
    return positions

unit_cell_atoms = read_poscar(os.path.join(folder_directory, poscar_file))

positions = positions(a, b, c, unit_cell_atoms, nx, ny, nz)


def write_lammps_data_file(positions, a, b, c, nx, ny, nz, filename):
    xlo, xhi = 0.0, nx * a
    ylo, yhi = 0.0, ny * b
    zlo, zhi = 0.0, nz * c

    with open(filename, 'w') as f:
        f.write("LAMMPS data file\n\n")
        f.write(f"{len(positions)} atoms\n")
        f.write(f"{len(set([pos[0] for pos in positions]))} atom types\n\n")
        f.write(f"{xlo} {xhi} xlo xhi\n")
        f.write(f"{ylo} {yhi} ylo yhi\n")
        f.write(f"{zlo} {zhi} zlo zhi\n\n")
        f.write("Atoms\n\n")

        element_types = {element: idx + 1 for idx, element in enumerate(set([pos[0] for pos in positions]))}

        for atom_id, (element, x, y, z) in enumerate(positions, start=1):
            atom_type = element_types[element]
            f.write(f"{atom_id} {atom_type} {x:.6f} {y:.6f} {z:.6f}\n")
            print(atom_type, element)

    print(f"LAMMPS data file written to {filename}")
    
output_path = f'{folder_directory}/lattice1.xyz'

write_lammps_data_file(positions, a, b, c, nx, ny, nz, filename=output_path)




