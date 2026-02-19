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

vel_vec_init=[77*cos(degrees(8.75)),0,77*sin(degrees(8.75))]
pos_vec_init=[0,0,0]
omega_vec_init=[0,-330,0]
#set up initial vectors

delta_t = 1/100
t = np.arange(0,7,delta_t)

#def a_x(v_vec):
print(len(t)+1)