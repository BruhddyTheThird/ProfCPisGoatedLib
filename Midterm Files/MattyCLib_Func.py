## IMPORTED FROM MattyCLib/FUNCTIONLIB/MTHFunctions.py
from sys import argv
import warnings
def InteriorProduct(Array1, Array2):
    if len(Array1) != len(Array2):
        raise ValueError('The arrays do not have the same length!')
    productExpr = 0
    for i in range(len(Array1)):
        productExpr = productExpr + Array1[i]*Array2[i]
    return productExpr
def CrossProduct(Array1, Array2):
    if len(Array1) != len(Array2):
        raise ValueError('The arrays do not have the same length!')
    if len(Array1) == 3:
        ProductList = [
            (Array1[1]*Array2[2]-Array1[2]*Array2[1]),
            (Array1[2]*Array2[0]-Array1[0]*Array2[2]),
            (Array1[0]*Array2[1]-Array1[1]*Array2[0])
            ]
        return ProductList
    if len(Array1)==2:
        ProductList = [
            0,
            0,
            (Array1[0]*Array2[1]-Array1[1]*Array2[0])
        ]
        return ProductList
    else:
        raise IndexError('Expected arrays of length 2 or 3, instead got arrays of length:',len(Array1))
