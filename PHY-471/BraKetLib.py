import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq
import re
import itertools

class OverlappingMan:
    def __init__(self):
        self._registry={}

    def _normalize_label(self,label):
        if isinstance(label, (tuple,list)) and len(label)==1:
            return label[0]
        return label
    def set_overlap(self,label_1,label_2,value):
        l_1 = self._normalize_label(label_1)
        l_2 = self._normalize_label(label_2)
        key = tuple(sorted([l_1,l_2]))
        self._registry[key]=value

    def clear_reg(self):
        self._registry.clear()

    def get_overlap(self,label_1,label_2):
        l_1 = self._normalize_label(label_1)
        l_2 = self._normalize_label(label_2)
        if l_1 == l_2:
            return sp.S.One
        key = tuple(sorted([l_1,l_2]))
        return self._registry.get(key,None)

LibMan = OverlappingMan()

class GenKet(spq.Ket):
    def _eval_innerproduct(self, bra, **hints):
        bra_label=bra.label[0] if isinstance(bra.label, tuple) else bra.label
        ket_label=self.label[0] if isinstance(self.label, tuple) else self.label

        res = LibMan.get_overlap(bra_label.name,ket_label.name)
        if res is not None:
            return res
        return None
truthMap = {"True":True,
            "true":True,
            "t":True,
            "T":True,
            "False":False,
            "false":False,
            "f":False,
            "F":False}

def MakeKet(badKetPsi:str,global_var_dict:dict,input_maps:dict) -> GenKet:
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
                coeffStr="".join(ordPsiStr[i-1]).replace(" ","")
                if coeffStr == "" or coeffStr == "+":
                    coeff = 1
                elif coeffStr =="-":
                    coeff = -1
                else:
                    coeff = sp.parse_expr(coeffStr,
                                      global_dict=global_var_dict,
                                      local_dict=input_maps,
                                      transformations='all') or 0
                eigStateList.remove("|")
                eigStateList.remove(">")
                eigStateStr = "".join(eigStateList)
                eigStateSym = sp.Symbol(eigStateStr)
                eigState = GenKet(eigStateSym)
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

def StrtoReg(string:str,kroneckerDelta=None) -> dict:
    lstring = re.findall(r"\{[^}]+\}",string)
    lstring = [i.strip("{}") for i in lstring]
    cond = {}
    if kroneckerDelta is None:
        kroneckerDelta=[0]*len(lstring)
    for i,j in enumerate(lstring):
        cond[j] = kroneckerDelta[i]
    return cond

def Serialize(state):
    """Converts a runtime state containing SymPy objects into a JSON-serializable dict."""
    global_vars = state.get('global_var_dict') or {}
    overlap_reg = state.get('overlap_registry') or {}
    serialized_registry = {}
    for tuple_key, val in overlap_reg.items():
        if isinstance(tuple_key, tuple) and len(tuple_key) == 2:
            # FIX: Explicitly convert individual elements to strings so we don't save tuple brackets or commas
            str_key = f"{str(tuple_key[0])}|{str(tuple_key[1])}"
            serialized_registry[str_key] = str(val)

    serialized = {
        'exec_num': state.get('exec_num', 0),
        'input_maps': {k: str(v) for k, v in (state.get('input_maps') or {}).items()},
        'global_var_dict': {
            k: str(v) for k, v in global_vars.items()
            if isinstance(v, sp.Basic) and type(v).__name__ not in ('SymbolicConstant', 'FunctionClass')
            and k not in ('I', 'oo', 'nan', 'pi')
        },
        'overlap_registry': serialized_registry
    }
    return serialized

def deserialize_state(json_data):
    """Restores SymPy objects and proper structures from a JSON-loaded dict."""
    input_maps = {k: sp.sympify(v) for k, v in json_data.get('input_maps', {}).items()}
    global_var_dict = {k: sp.sympify(v) for k, v in json_data.get('global_var_dict', {}).items()}
    global_var_dict.update(sp.__dict__)
    overlap_registry = {}
    for k, v in json_data.get('overlap_registry', {}).items():
        parts = k.split('|')
        tuple_key = (str(parts[0]), str(parts[1]))
        overlap_registry[tuple_key] = sp.sympify(v)
    return {
        'exec_num': json_data.get('exec_num', 0),
        'input_maps': input_maps,
        'global_var_dict': global_var_dict,
        'overlap_registry': overlap_registry
    }