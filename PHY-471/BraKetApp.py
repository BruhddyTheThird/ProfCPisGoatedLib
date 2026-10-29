import sympy as sp
from sympy import sqrt
from sympy.physics import quantum as spq

from tkinter import *
from tkinter import ttk

import os
import json

from BraKetLib import *
#for variable retention between sessions

BRA_KET_FILE = "BRA_KET_STATES.json"

if os.path.exists(BRA_KET_FILE):
    with open(BRA_KET_FILE, "r") as file:
        runTimeState = deserialize_state(json.load(file))
else:
    runTimeState = {'exec_num':0,'input_maps': {'i':sp.I}}
    dict_loc={'x':sp.Symbol('x'),'y':sp.Symbol('y'),'z':sp.Symbol('z')}
    runTimeState['global_var_dict'] = dict_loc
    runTimeState['overlap_registry'] = {}

runTimeState['exec_num'] += 1
input_maps = runTimeState['input_maps']
runTimeState['global_var_dict'].update(sp.__dict__)
global_var_dict=runTimeState['global_var_dict']
overlap_registry=runTimeState['overlap_registry']

LibMan._registry = overlap_registry

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
    ketPsi_loc = MakeKet(ketPsi.get(),global_var_dict,input_maps)
    if ketPsi_loc == 0:
        braPsiPsiket.set("0")
    else:
        braPsi_loc = spq.Dagger(ketPsi_loc)
        braPsiPsiket_loc = spq.qapply((braPsi_loc*ketPsi_loc).expand(quantum=True)).doit()
        braPsiPsiket.set(str(braPsiPsiket_loc).replace("*",""))

def TryRealInnerProd(*args):
    ketPsi_loc = MakeKet(ketPsi.get(),global_var_dict,input_maps)
    braPhi_loc = spq.Dagger(MakeKet(ketPhi.get(),global_var_dict,input_maps,))
    braPhiPsiket_loc = spq.qapply((braPhi_loc*ketPsi_loc).expand(quantum=True)).doit()
    braPhiPsiket.set(str(braPhiPsiket_loc).replace("*",""))
def ClearOrthDict(*args):
    LibMan.clear_reg()
def AddOrthStates(*args):
    stateDict = StrtoReg(orthStates.get())
    for i in stateDict.keys():
        indices = [state.strip() for state in i.split(",")]
        related_doubles=list(itertools.combinations(indices,2))
        for j in related_doubles:
            LibMan.set_overlap(j[0],j[1],stateDict[i])

root = Tk()
root.title("Ket to Bra Calculator")

mainframe = ttk.Frame(root, padding=(9,12,9,12))
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

sympyVars = StringVar()
sympyVarsEntry = ttk.Entry(mainframe, width=36, textvariable=sympyVars)
sympyVarsEntry.grid(column=2,row=1,sticky=(W,E))

ttk.Button(mainframe, text="Initialize Variables",command=Initialize).grid(column=3,row=1,sticky=(W,S))

ketPsi = StringVar()
ketPsiEntry = ttk.Entry(mainframe, width=36, textvariable=ketPsi)
ketPsiEntry.grid(column=2,row=2,sticky=(W,E))

ttk.Button(mainframe, text="Calculate <\u03c8|",command=TryDual).grid(column=3,row=2, sticky=(W,S))

braPsi = StringVar()
ttk.Label(mainframe,textvariable=braPsi).grid(column=2,row=3,sticky=(W,E))

braPsiPsiket = StringVar()
ttk.Label(mainframe,textvariable=braPsiPsiket).grid(column=2,row=4,sticky=(W,E))

ttk.Button(mainframe, text="Calculate <\u03c8|\u03c8>",command=TryInnerProd).grid(column=3,row=4,sticky=(W,S))

ketPhi = StringVar()
ketPhiEntry = ttk.Entry(mainframe,width=36,textvariable=ketPhi)
ketPhiEntry.grid(column=2,row=6,sticky=(W,E))

ttk.Button(mainframe,text="Calculate <\u03c6|\u03c8>",command=TryRealInnerProd).grid(column=3,row=6,sticky=(W,S))

braPhiPsiket = StringVar()
ttk.Label(mainframe,textvariable=braPhiPsiket).grid(column=2,row=7,sticky=(W,E))

orthStates = StringVar()
orthStatesEntry = ttk.Entry(mainframe,width=36,textvariable=orthStates)
orthStatesEntry.grid(column=2,row=8,sticky=(W,E))

ttk.Button(mainframe,text="Update orthonormal dictionary",command=AddOrthStates).grid(column=1,row=8,sticky=(E))

ttk.Button(mainframe,text="Clear orthonormal dictionary",command=ClearOrthDict).grid(column=1,row=9,sticky=(E))

ttk.Label(mainframe,text="Scalar variables, separated by commas: ").grid(column=1,row=1,sticky=(E,S))
ttk.Label(mainframe,text="|\u03c8> =").grid(column=1,row=2,sticky=(E))
ttk.Label(mainframe,text="<\u03c8| =").grid(column=1,row=3,sticky=(E))
ttk.Label(mainframe,text="<\u03c8|\u03c8> =").grid(column=1,row=4,sticky=(E))
ttk.Label(mainframe, text="|\u03c6> =").grid(column=1,row=6,sticky=(E))
ttk.Label(mainframe, text="<\u03c6|\u03c8> =").grid(column=1,row=7,sticky=(E))
ttk.Label(mainframe, text="Orthonormal state dictionary, use brackets to denote sets of distinct bases.").grid(column=3,row=8,sticky=(W,S))


root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(2,weight=1)
for i in mainframe.winfo_children():
    i.grid_configure(padx=5,pady=5)
    if isinstance(i,ttk.Label):
        i.configure(wraplength=400)

sympyVarsEntry.focus()

root.mainloop()

runTimeState['global_var_dict'] = global_var_dict
runTimeState['overlap_registry'] = LibMan._registry
with open(BRA_KET_FILE, "w") as file:
    json.dump(Serialize(runTimeState),file,indent=4)