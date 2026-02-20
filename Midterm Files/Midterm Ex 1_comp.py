import numpy as np
import matplotlib.pyplot as plt
from math import *
import pandas as pd
#import functions and libraries

plt.style.use('seaborn-v0_8-colorblind')
#use specific style for matplot

g = 9.81 #m/s^2
C_d = 0.15 #dimensionless
rho = 1.235 #kg/m^3
A = 4.7E-3 #m^2
r = 0.0213 #m
S = (2/3)*rho*r**3*pi #kg
m = 4.575E-2 #kg
N = 350 #number of time steps.
k=N #time variable used later
#set up constants

vel_vec_aray = np.zeros((N,3))
vel_vec_aray[0] = np.array([77*cos(radians(10)),0,77*sin(radians(10))])
# use radians() function on degress.
pos_vec_aray = np.zeros((N,3))
pos_vec_aray[0]=np.array([0,0,0.03])
omega_vec_aray = np.zeros((N,3))
omega_vec_aray[0]=np.array([0,-330,0])
#set up initial vectors

delta_t = 1/50
t = np.arange(0,7,delta_t)
#make 350 time points, from 1-7.

def Magnitude(vec):
    sq_vec = np.zeros(len(vec))
    for i,j in enumerate(vec):
        sq_vec[i] = j**2
        mag = np.sqrt(sum(sq_vec))
    return mag
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
        return g_a+drag_a+magnus_a
    else:
        return (m*g_a,m*drag_a,m*magnus_a) #again, don't forget gravity
        #importantly, this one is a 3-tuple, instead of a 
        # 2-tuple, make sure future calls can handle that
#Define our acceleration in z as a function of velocity

acc_vec_aray = np.zeros((N,3))
acc_vec_aray[0]=np.array([Dot_v_x(vel_vec_aray[0],omega_vec_aray[0]),
               Dot_v_y(vel_vec_aray[0],omega_vec_aray[0]),
               Dot_v_z(vel_vec_aray[0],omega_vec_aray[0])])

for i in range(1,N):
    vel_x = vel_vec_aray[i-1][0] + acc_vec_aray[i-1][0]*delta_t
    vel_y = vel_vec_aray[i-1][1] + acc_vec_aray[i-1][1]*delta_t
    vel_z = vel_vec_aray[i-1][2] + acc_vec_aray[i-1][2]*delta_t
    vel_vec_aray[i] = np.array([vel_x,vel_y,vel_z])
    #Euler velocity update
    pos_x = pos_vec_aray[i-1][0] + vel_vec_aray[i][0]*delta_t
    pos_y = pos_vec_aray[i-1][1] + vel_vec_aray[i][1]*delta_t
    pos_z = pos_vec_aray[i-1][2] + vel_vec_aray[i][2]*delta_t
    pos_vec_aray[i] = np.array([pos_x,pos_y,pos_z])
    if pos_vec_aray[i][2] <= 1E-3:
        k = i
        break #this simulates hitting the ground and no more force being applied.
    #Euler-Cromer position update
    omega_y = omega_vec_aray[i-i][1]#*0.964
    omega_z = omega_vec_aray[i-1][2]#*0.964
    omega_vec_aray[i] = np.array([0,omega_y,omega_z])
    #exponential decay of angular velocity
    acc_x = Dot_v_x(vel_vec_aray[i],omega_vec_aray[i])
    acc_y = Dot_v_y(vel_vec_aray[i],omega_vec_aray[i])
    acc_z = Dot_v_z(vel_vec_aray[i],omega_vec_aray[i])
    acc_vec_aray[i] = np.array([acc_x,acc_y,acc_z])
    #Euler acceleration update
if k != N:
    for i in range(k+1,N):
        pos_vec_aray[i] = np.array([pos_vec_aray[i-1][0],pos_vec_aray[i-1][1],0])
        #this updates the position array with the final x and y positions, while keeping z zero.
