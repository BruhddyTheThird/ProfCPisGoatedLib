import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq

from tkinter import *
from tkinter import ttk

input_maps = {'i':sp.I}
global_var_dict={'x':sp.Symbol('x'),'y':sp.Symbol('y'),'z':sp.Symbol('z')}
global_var_dict.update(sp.__dict__)

from BraKetLib import *

def TryDual(*args):
    ketPsi_1 = MakeKet(ketPsi.get(),global_var_dict,input_maps)
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

def TryInnerProd(*args):
    ketPsi_loc = MakeKet(ketPsi.get(),global_var_dict,input_maps,StrToBool(orth.get()))
    if ketPsi_loc == 0:
        braPsiPsiket.set("0")
    else:
        braPsi_loc = spq.Dagger(ketPsi_loc)
        braPsiPsiket_loc = spq.qapply((braPsi_loc*ketPsi_loc).expand(quantum=True)).doit()
        braPsiPsiket.set(str(braPsiPsiket_loc).replace("*",""))

def ToggleOrth(*args):
    val = orth.get()
    truthNegationMap = {"True":"False","False":"True"}
    orth.set(truthNegationMap[val])

def TryRealInnerProd(*args):
    ketPsi_loc = MakeKet(ketPsi.get(),global_var_dict,input_maps,StrToBool(orth.get()))
    braPhi_loc = spq.Dagger(MakeKet(ketPhi.get(),global_var_dict,input_maps,StrToBool(orth.get())))
    braPhiPsiket_loc = spq.qapply((braPhi_loc*ketPsi_loc).expand(quantum=True)).doit()
    braPhiPsiket.set(str(braPhiPsiket_loc).replace("*",""))

root = Tk()
root.title("Ket to Bra Calculator")

mainframe = ttk.Frame(root, padding=(9,12,9,12))
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

sympyVars = StringVar()
sympyVarsEntry = ttk.Entry(mainframe, width=12, textvariable=sympyVars)
sympyVarsEntry.grid(column=2,row=1,sticky=(W,E))

ttk.Button(mainframe, text="Initialize Variables",command=Initialize).grid(column=3,row=1,sticky=(W,S))

ketPsi = StringVar()
ketPsiEntry = ttk.Entry(mainframe, width=12, textvariable=ketPsi)
ketPsiEntry.grid(column=2,row=2,sticky=(W,E))

ttk.Button(mainframe, text="Calculate <\u03c8|",command=TryDual).grid(column=3,row=2, sticky=(W,S))

braPsi = StringVar()
ttk.Label(mainframe,textvariable=braPsi).grid(column=2,row=3,sticky=(W,E))

braPsiPsiket = StringVar()
ttk.Label(mainframe,textvariable=braPsiPsiket).grid(column=2,row=4,sticky=(W,E))

ttk.Button(mainframe, text="Calculate <\u03c8|\u03c8>",command=TryInnerProd).grid(column=3,row=4,sticky=(W,S))

orth = StringVar(value="True")
ttk.Label(mainframe,textvariable=orth).grid(column=3,row=5,sticky=(W,E))

ttk.Button(mainframe, text="Toggle implicit orthonormality of kets",command=ToggleOrth).grid(column=1,row=5,sticky=(W,E))

ketPhi = StringVar()
ketPhiEntry = ttk.Entry(mainframe,width=12,textvariable=ketPhi)
ketPhiEntry.grid(column=2,row=6,sticky=(W,E))

ttk.Button(mainframe,text="Calculate <\u03c6|\u03c8>",command=TryRealInnerProd).grid(column=3,row=6,sticky=(W,S))

braPhiPsiket = StringVar()
ttk.Label(mainframe,textvariable=braPhiPsiket).grid(column=2,row=7,sticky=(W,E))

ttk.Label(mainframe,text="Scalar variables, separated by commas: ").grid(column=1,row=1,sticky=(E,S))
ttk.Label(mainframe,text="|\u03c8> =").grid(column=1,row=2,sticky=(E))
ttk.Label(mainframe,text="<\u03c8| =").grid(column=1,row=3,sticky=(E))
ttk.Label(mainframe,text="<\u03c8|\u03c8> =").grid(column=1,row=4,sticky=(E))
ttk.Label(mainframe, text="Orthonormality of kets: ").grid(column=2,row=5,sticky=(E))
ttk.Label(mainframe, text="|\u03c6> =").grid(column=1,row=6,sticky=(E))
ttk.Label(mainframe, text="<\u03c6|\u03c8> =").grid(column=1,row=7,sticky=(E))

root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(2,weight=1)
for i in mainframe.winfo_children():
    i.grid_configure(padx=5,pady=5)

sympyVarsEntry.focus()

root.mainloop()