import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq

#Subclass shenanigans

class UnderOrthogonalBra(spq.OrthogonalBra):
    @classmethod
    def dual_class(cls):
        return UnderOrthogonalKet


class UnderOrthogonalKet(spq.OrthogonalKet):
    @classmethod
    def dual_class(cls):
        return UnderOrthogonalBra
    def _dagger_eval(self):
        return UnderOrthogonalBra(*self.label)
    def _eval_innerproduct(self, bra, **hints):
        if self.label == bra.label:
            return 1
        else:
            return 0

UnderOrthogonalBra._dagger_eval = lambda self: UnderOrthogonalKet(*self.label)
#real shit

truthMap = {"True":True,
            "true":True,
            "t":True,
            "T":True,
            "False":False,
            "false":False,
            "f":False,
            "F":False}

def MakeKet(badKetPsi:str,global_var_dict:dict,input_maps:dict,orthogonal=True) -> spq.Ket|spq.OrthogonalKet:
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
        state = 0
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
                if orthogonal==True:
                    eigState = UnderOrthogonalKet(eigStateSym)
                else:
                    eigState = spq.Ket(eigStateSym)
                state = coeff*eigState + state
        return state
    except ValueError:
        pass
def StrToBool(string:str) -> bool:
    try:
        val = truthMap[string]
        return val
    except TypeError("Non-truth value string cannot be interpreted as bool! The Law of Excluded Middle does hold, you know."):
        pass

def BooltoStr(boole:bool) -> str:
    inverseTruthMap = {j: i for i, j in truthMap.items()}
    try:
        string = inverseTruthMap[boole]
        return string
    except TypeError(f"BooltoStr expects input of type 'bool', got input of type {type(boole)}."):
        pass
