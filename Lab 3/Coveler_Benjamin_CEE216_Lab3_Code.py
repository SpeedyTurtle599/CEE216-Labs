# Benjamin Coveler
# Lab 3 (CIV_ENV 216-0)
# 11 May 2023

# Find length L and width b given values of P and W

import sympy as sym

# Parameters given
L = sym.symbols(r'L')
b = sym.symbols(r'b')
sigma = 1800
tau = 120

# Cross-section parameters
base = b
height = 8 * b
area = base * height


# Moment of inertia calculator (rectangular section)
# Inputs: base [length], height [length]
# Output: moment of inertia [length^4]
def MoI(MoI_base, MoI_height):
    moment = 1/12 * MoI_base * MoI_height ** 3
    return moment


# Main function
# Inputs: point load [force], distributed load [force/length]
# Output: L [length], b [length]
def dimensionFinder(point_load, distributed_load):
    V = distributed_load * L + point_load
    M = (distributed_load * L ** 2) / 2 + point_load * L
    sigmaEq = sym.Eq(sigma, M * (4 * b) / MoI(base, height))
    tauEq = sym.Eq(tau, 3/2 * V / area)
    results = sym.nonlinsolve([sigmaEq, tauEq], [L, b])
    return results


# Call dimensionFinder for each set of inputs
print('The results for Part A are:')
partA = dimensionFinder(1000, 0)
print('L = %.2f inches\nb = %.2f inches' % (list(list(partA)[1])[0], list(list(partA)[1])[1]))

print('\nThe results for Part B are:')
partB = dimensionFinder(0, 12.5)
print('L = %.2f inches\nb = %.2f inches' % (list(list(partB)[0])[0], list(list(partB)[0])[1]))

print('\nThe results for Part C are:')
partC = dimensionFinder(500, 12.5)
print('L = %.2f inches\nb = %.2f inches' % (list(list(partC)[1])[0], list(list(partC)[1])[1]))
