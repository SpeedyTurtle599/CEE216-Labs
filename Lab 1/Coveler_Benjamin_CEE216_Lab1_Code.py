import numpy as np
import pandas as pd
import openpyxl

# Create a range from 0 to 1 for tan(alpha)
tanAlpha = np.arange(0, np.tan(np.deg2rad(45)) + 0.1, 0.1)
# Convert the range to radians using arctan (inverse tangent)
alphaR = np.arctan(np.array(tanAlpha))
# Create another range, converted to 0->45 degrees.
# The numpy tangent function only takes/makes radian arguments without additional conversion.
alpha = np.rad2deg(np.array(alphaR))

# Perform the same operations for beta
tanBeta = np.arange(0, np.tan(np.deg2rad(45)) + 0.1, 0.1)
betaR = np.arctan(np.array(tanBeta))
beta = np.rad2deg(np.array(betaR))

# Define parameters from the problem statement
# P is the force exerted on the system, 4 kips
P = 4
# fUlt is the ultimate load (needed for FoS), 25 kips
fUlt = 25


# Define function to compute factor of safety for given alpha and beta arrays
def fos(a, b):
    numerator = 30 * np.cos(a) + 15 * np.sin(a)
    denominator = 15 * np.cos(b) + 12 * np.sin(b)
    tension = P * (numerator / denominator)
    factor = fUlt / tension
    return factor


resultMatrix = np.empty([tanAlpha.size, tanBeta.size])

for i in range(1, tanAlpha.size):
    for j in range(1,  tanBeta.size):
        resultMatrix[i, j] = fos(alphaR[i], betaR[j])

# Concatenate the matrices to get one unified matrix with axes
# Setting alpha as horizontal axis and beta as horizontal axis
resultMatrixBeta = np.column_stack((beta, resultMatrix))
# Append a 0 to the beginning of beta to match horizontal dimensions with alpha+results matrix
alpha0 = np.insert(alpha, 0, 0)
resultMatrixAlphaBeta = np.row_stack((alpha0, resultMatrixBeta))
print(resultMatrixAlphaBeta)
print('The maximum FoS of this system is', resultMatrix.max())

# Convert the result matrix into a dataframe
df = pd.DataFrame(resultMatrixAlphaBeta)

# Save to Excel spreadsheet in this .py file's project directory
filepath = 'FoSresults.xlsx'
df.to_excel(filepath, index=False)
