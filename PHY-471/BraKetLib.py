import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq

def MakeKet(badKetPsi,global_var_dict,input_maps) -> spq.Ket:
    try:
        psiStr = list(badKetPsi)
        ordPsiStr = [[]]
        j = 0
        for z,i in enumerate(psiStr):
            if i=="|":
                j+=1
                ordPsiStr.append([])
            ordPsiStr[j].append(i)
            if i == ">":
                j+= 1
                if z != len(psiStr)-1:
                    ordPsiStr.append([])
        state = 0 * spq.Ket(sp.Symbol("null"))
        for i in range(len(ordPsiStr)):
            if i % 2 == 1:
                eigStateList = ordPsiStr[i]
                coeff = sp.parse_expr(("".join(ordPsiStr[i-1])).replace(" ",""),
                                      global_dict=global_var_dict,
                                      local_dict=input_maps,
                                      transformations='all')
                if coeff == 0:
                    coeff = 1
                eigStateList.remove("|")
                eigStateList.remove(">")
                eigStateStr = "".join(eigStateList)
                eigStateSym = sp.Symbol(eigStateStr)
                eigState = spq.Ket(eigStateSym)
                state = coeff*eigState + state
        return state
    except ValueError:
        pass