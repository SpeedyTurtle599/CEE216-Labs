import numpy as np
import sympy as sym
import pandas as pd
import openpyxl
from IPython.display import Markdown, display

# Steps for problem setup:
# 1) Discretize body into elements and define nodes
# @ each end of the element
#     Typically, each element has the same geometry area (A) and
#     material Young’s modulus (E)
# 2) Define geometry and loads
# 3) Set up governing equations

# Relevant equations:
# sigma = E * epsilon
# F = k * delta


# Define functions for each task
def stiffness_matrix(num_bars, num_nodes, cross_area,
                     length, young_modulus):
    K = np.zeros((num_nodes, num_nodes))
    k = young_modulus * cross_area / length
    k_i = np.array([[k, -k], [-k, k]])
    for i in range(num_nodes - 2):
        K[i:i+2, i:i+2] = K[i, i] + k_i
    return K


def support_reactions(num_bars, num_nodes, cross_area,
                      length, young_modulus, load, gap_size):

    f = sym.Matrix(num_nodes, 1)
    u = sym.Matrix(num_nodes, 1)
    display(f)
    display(u)

    # 3d matrix (matrices for each k, aligned along z axis)
    element_matrices = sym.zeros(num_nodes, num_nodes, num_bars)

    for i in range(np.length(num_nodes)):
        for j in range(np.length(num_nodes)):
            element_matrices[i, j] = 1
        pass

    pass


def internal_forces(num_bars, num_nodes, cross_area,
                    length, young_modulus, load, gap_size):
    pass


def element_stresses(num_bars, num_nodes, cross_area,
                     length, young_modulus, load, gap_size):
    pass


# Define testing constants
bars = 2   # number of bars
nodes = 3  # number of nodes
A = 250        # mm^2
L = 150        # mm
E = 2 * 10**4  # N/mm^2
P = 6 * 10**4  # N
delta = 1.2    # mm

# Test the code on the example problem
# 1. Find support reaction forces at ends of bar
# 2. Find internal forces at each element
# 3. Find stresses at each element

stiff_mat = stiffness_matrix(bars, nodes, A, L, E)
display(stiff_mat)
