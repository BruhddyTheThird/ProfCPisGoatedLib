import numpy as np
import matplotlib.pyplot as plt
from math import *
import pandas as pd
#import functions and libraries

plt.style.use('seaborn-v0_8-colorblind')
#use specific style for matplot

g = 9.81
C_d = 0.25
rho = 1.225
A = 1.45E-3
S = 0.2
m = 4.575E-2
#set up constants

vel_vec_init=[[77*cos(degrees(8.75)),0,77*sin(degrees(8.75))]]
pos_vec_init=[[0,0,0]]
omega_vec_init=[0,-330,0]
#set up initial vectors

delta_t = 1/100
t = np.arange(0,7,delta_t)
#make 700 time points, from 1-7.

def Magnitude(vec):
    sq_vec=[]
    for i,j in enumerate(vec):
        sq_vec[i] = j**2
    return np.sqrt(sum(sq_vec))
#Define a simple magnitude function for any vector

def Dot_v_x(vel_vec,omega_vec=[0,0,0],component=False):
    drag_a = -(1/(2*m))*(C_d*rho*A*vel_vec[0])*Magnitude(vel_vec)
    magnus_a = (S/m)*(omega_vec[1]*vel_vec[2]-omega_vec[2]*vel_vec[1])
    #directly from the analytic equations
    if component==False:
        return drag_a+magnus_a
    else:
        return (m*drag_a,m*magnus_a) 
        #this would be for showing the individual forces instead of acceleration.
#Define our acceleration in x as a function of velocity

def Dot_v_y(vel_vec,omega_vec=[0,0,0], component=False):
    drag_a = -(1/(2*m))*(C_d*rho*A*vel_vec[1])*Magnitude(vel_vec)
    magnus_a = (S/m)*omega_vec[2]*vel_vec[0]
    #from analytic equations
    if component==False:
        return drag_a+magnus_a
    else:
        return (m*drag_a,m*magnus_a) 
        #same as before.
#Define our acceleration in y as a function of velocity

def Dot_v_z(vel_vec,omega_vec=[0,0,0],component=False):
    g_a = -g
    #dont forget gravity in the z-direction.
    drag_a = -(1/(2*m))*(C_d*rho*A*vel_vec[2])*Magnitude(vel_vec)
    magnus_a = -(S/m)*omega_vec[1]*vel_vec[0]
    #this one is negative
    if component==False:
        return g_a+drag_a+magnus_a #dont forget gravity
    else:
        return (m*g_a,m*drag_a,m*magnus_a) #again, don't forget gravity
        #importantly, this one is a 3-tuple, instead of a 
        # 2-tuple, make sure future calls can handle that
#Define our acceleration in z as a function of velocity


