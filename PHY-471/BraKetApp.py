import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq

from tkinter import *
from tkinter import ttk

input_maps = {'i':sp.I}
global_var_dict={'x':sp.Symbol('x'),'y':sp.Symbol('y'),'z':sp.Symbol('z')}
global_var_dict.update(sp.__dict__)

def MakeKet(badKetPsi) -> spq.Ket:
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

def TryDual(*args):
    ketPsi_1 = MakeKet(ketPsi.get())
    if ketPsi_1 == 0:
        braPsi.set("0")
    else:
        braPsi_1 = spq.Dagger(ketPsi_1)
        braPsi.set(str(braPsi_1).replace("*","").replace("conjugate","*"))

def Initialize(*args):
    try:
        varsStr = (sympyVars.get()).split(",")
        varsStr = [i.replace(" ","") for i in varsStr]
        for i in varsStr:
            global_var_dict[i] = sp.Symbol(i,complex=True)
    except ValueError:
        print("Initialization string error.")
        pass

root = Tk()
root.title("Ket to Bra Calculator")

mainframe = ttk.Frame(root, padding=(3,3,9,12))
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

sympyVars = StringVar()
sympyVarsEntry = ttk.Entry(mainframe, width=12, textvariable=sympyVars)
sympyVarsEntry.grid(column=2,row=1,sticky=(W,E))

ketPsi = StringVar()
ketPsiEntry = ttk.Entry(mainframe, width=12, textvariable=ketPsi)
ketPsiEntry.grid(column=2,row=2,sticky=(W,E))

braPsi = StringVar()
ttk.Label(mainframe,textvariable=braPsi).grid(column=2,row=3,sticky=(W,E))

ttk.Button(mainframe, text="Calculate",command=TryDual).grid(column=3,row=2, sticky=(W,S))
ttk.Button(mainframe, text="Initialize Variables",command=Initialize).grid(column=3,row=1,sticky=(W,S))

ttk.Label(mainframe,text="Scalar variables, separated by commas: ").grid(column=1,row=1,sticky=(E,S))
ttk.Label(mainframe,text="|\u03c8> =").grid(column=1,row=2,sticky=(E,S))
ttk.Label(mainframe,text="<\u03c8| =").grid(column=1,row=3,sticky=(E,S))

root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(2,weight=1)
for i in mainframe.winfo_children():
    i.grid_configure(padx=5,pady=5)

ketPsiEntry.focus()

root.mainloop()