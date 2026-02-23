import numpy as np
import matplotlib.pyplot as plt
from math import *
import pandas as pd
import os #needed for file outputs
import sys
#import functions and libraries

plt.style.use('seaborn-v0_8-colorblind')
#use specific style for matplot

output_folder_name = "midterm_output_files"
output_folder = os.path.join(os.getcwd(), output_folder_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)
# os black magic i found on google to output to correct places.


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
vel_vec_aray[0] = np.array([77*cos(radians(13.6)),0,77*sin(radians(13.6))])
# use radians() function on degress.
pos_vec_aray = np.zeros((N,3))
pos_vec_aray[0]=np.array([0,0,0.03])
omega_vec_aray = np.zeros((N,3))
omega_vec_aray[0]=np.array([0,-50*pi,0])
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
        return np.array([m*drag_a,m*magnus_a]) 
        #this would be for showing the individual forces instead of acceleration.
#Define our acceleration in x as a function of velocity

def Dot_v_y(vel_vec,omega_vec=[0,0,0], component=False):
    drag_a = -(1/(2*m))*(C_d*rho*A*vel_vec[1])*Magnitude(vel_vec)
    magnus_a = (S/m)*omega_vec[2]*vel_vec[0]
    #from analytic equations
    if component==False:
        return drag_a+magnus_a
    else:
        return np.array([m*drag_a,m*magnus_a])
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
        return np.array([m*g_a,m*drag_a,m*magnus_a]) #again, don't forget gravity
        #importantly, this one is a 3-vector, instead of a 
        # 2-vector, make sure future calls can handle that
#Define our acceleration in z as a function of velocity

def Drag(vel_vec):
    a_x = -(1/(2*m))*(C_d*rho*A*vel_vec[0])*Magnitude(vel_vec)
    a_y = -(1/(2*m))*(C_d*rho*A*vel_vec[1])*Magnitude(vel_vec)
    a_z = -(1/(2*m))*(C_d*rho*A*vel_vec[2])*Magnitude(vel_vec)
    return np.array([a_x,a_y,a_z])
#strict drag acceleration

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
#Thus, we complete our magnus effect situation.

pos_orth_aray = np.transpose(pos_vec_aray)
vel_orth_aray = np.transpose(vel_vec_aray)
#transpose for easy plotting of trajectory.

v_i_1 = np.array([77*cos(radians(13.6)),0,77*sin(radians(13.6))])
pos_1 = np.zeros((N,3))
pos_1[0] = np.array([0,0,0.02])
x,y,z = pos_1[0]
for i in range(1,N):
    if z <= 0:
        pos_1[i] = np.array([x,y,0])
    else:
        x = pos_1[0][0] + v_i_1[0]*t[i]
        y = pos_1[0][1] + v_i_1[1]*t[i]
        z = pos_1[0][2] + v_i_1[2]*t[i] - (9.8/2)*(t[i])**2   
        #these are exactly the kinematic equations from high-school physics. 
        # Doesn't conservative, constant accelerations, make things so easy?
        pos_1[i] = np.array([x,y,z])
# position of ball under only gravitational force.
pos_1 = np.transpose(pos_1)
# transpose for plotting

acc_2 = np.zeros((N,3))
vel_2 = np.zeros((N,3))
pos_2 = np.zeros((N,3))
vel_2[0] = np.array([77*cos(radians(13.6)),0,77*sin(radians(13.6))])
pos_2[0] = np.array([0,0,0.02])
acc_2[0] = np.array([
    Drag(vel_2[0])[0],
    Drag(vel_2[0])[1],
    Drag(vel_2[0])[2] - g
])
x,y,z = pos_2[0]
for i in range(1,N):
    if z <= 0:
        acc_2[i] = np.array([0,0,-g])
        vel_2[i] = np.array([0,0,0])
        pos_2[i] = np.array([x,y,0])
    else:
        vel_x = vel_2[i-1][0] + acc_2[i-1][0]*delta_t
        vel_y = vel_2[i-1][1] + acc_2[i-1][1]*delta_t
        vel_z = vel_2[i-1][2] + acc_2[i-1][2]*delta_t
        vel_2[i] = np.array([vel_x,vel_y,vel_z])
        x = pos_2[i-1][0] + vel_2[i][0]*delta_t
        y = pos_2[i-1][1] + vel_2[i][1]*delta_t
        z = pos_2[i-1][2] + vel_2[i][2]*delta_t
        pos_2[i] = np.array([x,y,z])
        acc_x = Drag(vel_2[i])[0]
        acc_y = Drag(vel_2[i])[1]
        acc_z = Drag(vel_2[i])[2] - g
        acc_2[i] = np.array([acc_x,acc_y,acc_z])
#Euler-Cromer integration of just drag and gravity

pos_orth_2 = np.transpose(pos_2)
#transpose for plotting

"""
filename_1 = "log_1.txt"
output_path_1 = os.path.join(output_folder,filename_1)
with open(output_path_1,'w') as output:
    with np.printoptions(threshold=sys.maxsize):
        print(pos_1,file=output)
"""
# I used this during testing to output a log of the gravity only ball, as I had some trouble getting the function to work.

force_x = np.zeros((N,2))
force_y = np.zeros((N,2))
force_z = np.zeros((N,3))
#initialize force arrays
# two forces possible in x and y directions, three in z, these do not all have same shape!
force_x[0] = Dot_v_x(vel_vec_aray[0],omega_vec_aray[0],True)
force_y[0] = Dot_v_y(vel_vec_aray[0],omega_vec_aray[0],True)
force_z[0] = Dot_v_z(vel_vec_aray[0],omega_vec_aray[0],True)
for i in range(1,N):
    force_x[i] = Dot_v_x(vel_vec_aray[i],omega_vec_aray[i],True)
    force_y[i] = Dot_v_y(vel_vec_aray[i],omega_vec_aray[i],True)
    force_z[i] = Dot_v_z(vel_vec_aray[i],omega_vec_aray[i],True)
force_x = np.transpose(force_x)
force_y = np.transpose(force_y)
force_z = np.transpose(force_z)

#look upon my plots, ye mighty and despair.
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111,projection="3d")
ax.plot(pos_orth_aray[0],pos_orth_aray[1],pos_orth_aray[2],label="Magnus Effect, Drag, Gravity")
ax.plot(pos_1[0],pos_1[1],pos_1[2], label="Gravity")
ax.plot(pos_orth_2[0],pos_orth_2[1],pos_orth_2[2], label="Drag, Gravity")
ax.set_title("Golf Ball Trajectory, 13.6 degree Launch Angle")
ax.set_xlabel("X-position (m)")
ax.set_ylabel("Y-position (m)")
ax.set_zlabel("Z-position (m)")
ax.set_zbound((0,40))
ax.legend()
ax.grid(True)
filename_2 = "Plot I - PHY321 Midterm I Exercise I.png"
output_path_2 = os.path.join(output_folder,filename_2)
fig.savefig(output_path_2)
#First plot of trajectory in 3-d space.

fig, ax = plt.subplots(3,1,figsize=(7,12))
fig.suptitle("Golf Ball Velocity vs Time w/Magnus Effect")
ax[0].plot(t,vel_orth_aray[0],label="x-velocity")
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Velocity (m/s)")
ax[0].legend()
ax[0].grid(True)
# plot x velocity 
ax[1].plot(t,vel_orth_aray[1],label="y-velocity")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Velocity (m/s)")
ax[1].legend()
ax[1].grid(True)
# plot y velocity
ax[2].plot(t,vel_orth_aray[2],label="z-velocity")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Velocity (m/s)")
ax[2].legend()
ax[2].grid(True)
#plot z velocity
filename_3 = "Plot II - PHY321 Midterm I Exercise I.png"
output_path_3 = os.path.join(output_folder,filename_3)
fig.savefig(output_path_3)
#filename shenanigans.

fig,ax = plt.subplots(3,3,figsize=(13,13))
fig.suptitle("Forces Acting on Golf Ball")
ax[0][0].set_title("Force in X-direction")
ax[0][0].plot(t,force_x[0],label="x-drag")
ax[0][0].set_xlabel("Time (s)")
ax[0][0].set_ylabel("Force(N)")
ax[0][0].legend()
ax[0][0].grid(True)

ax[1][0].plot(t,force_x[1],label="x-magnus")
ax[1][0].set_xlabel("Time (s)")
ax[1][0].set_ylabel("Force(N)")
ax[1][0].legend()
ax[1][0].grid(True)

ax[0][1].set_title("Force in Y-direction")
ax[0][1].plot(t,force_y[0],label="y-drag")
ax[0][1].set_xlabel("Time (s)")
ax[0][1].set_ylabel("Force(N)")
ax[0][1].legend()
ax[0][1].grid(True)

ax[1][1].plot(t,force_y[1],label="y-magnus")
ax[1][1].set_xlabel("Time (s)")
ax[1][1].set_ylabel("Force(N)")
ax[1][1].legend()
ax[1][1].grid(True)

ax[0][2].set_title("Force in Z-direction")
ax[0][2].plot(t,force_z[1],label="z-drag")
ax[0][2].set_xlabel("Time (s)")
ax[0][2].set_ylabel("Force(N)")
ax[0][2].legend()
ax[0][2].grid(True)

ax[1][2].plot(t,force_z[2],label="z-magnus")
ax[1][2].set_xlabel("Time (s)")
ax[1][2].set_ylabel("Force(N)")
ax[1][2].legend()
ax[1][2].grid(True)

ax[2][2].plot(t,force_z[0],label="gravity")
ax[2][2].set_xlabel("Time (s)")
ax[2][2].set_ylabel("Force(N)")
ax[2][2].legend()
ax[2][2].grid(True)
#Plot all forces.
fig.subplots_adjust(hspace=0.4,wspace=0.4)
filename_4 = "Plot III - PHY321 Midterm I Exercise I"
output_path_4 = os.path.join(output_folder,filename_4)
fig.savefig(output_path_4)
#save to this filename in a diff folder.
#we should be donezo with this one.
