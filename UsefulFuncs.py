import numpy as np
import matplotlib.pyplot as plt

def SHO_acc(x,v):
    return -x

def RK2O_gen(x_0,v_0,t_0,tf,dt,acc_func:function,fargs=tuple|None):
    """
    Integrates two first-order ODEs that are the reduction of a single second-order ODE.
    Takes initial values of the position and velocity (x_0,v_0), 
    the start and end times (t_0, tf), 
    the time-step (dt), and
    an acceleration function (d^2x/dt^2) plus its additional arguments (fargs).
    Returns the time, position, and velocity arrays of the integrated equations of motion.
    """
    #here, x,v are arbitrary parameters, we simply need a name for them.
    t = np.arange(t_0, tf, dt)
    x = np.zeros(t.shape)
    v = np.zeros(t.shape)
    x[0], v[0] = x_0,v_0
    
    for i in range(1,len(t)):
        x_prev = x[i-1]
        v_prev = v[i-1]

        k_1x = v_prev * dt
        try:
            k_1v = dt * acc_func(x_prev,v_prev,*fargs)
        except:
            k_1v = dt * acc_func(x_prev,v_prev)
        k_2x = dt * (v_prev + k_1v)
        try:
            k_2v = dt * (acc_func(x_prev+k_1x,v_prev+k_1v,*fargs))
        except:
            k_2v = dt * (acc_func(x_prev+k_1x,v_prev+k_1v))
        x[i] = x_prev + 0.5 * (k_1x+k_2x)
        v[i] = v_prev + 0.5 * (k_1v+k_2v)
    return t,x,v

