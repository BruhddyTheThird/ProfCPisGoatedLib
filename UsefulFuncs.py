

def SHO_acc(x,v):
    return -x

def RK2O_gen(x_0,v_0,t_0,tf,dt,acc_func=SHO_acc,fargs=tuple|None):
    """
    Integrates two first-order ODEs that are the reduction of a single second-order ODE.
    Takes initial values of the position and velocity (x_0,v_0), 
    the start and end times (t_0, tf), 
    the time-step (dt), and
    an acceleration function (d^2x/dt^2) plus its additional arguments (fargs).
    Returns the time, position, and velocity arrays of the integrated equations of motion.
    """
    import numpy as np
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

def Gen_Phase_Space(x_lim,v_lim,grid_size,acc_func=SHO_acc,fargs=tuple|None):
    """
    Generates a phase space mesh and vectors for a given acceleration function.
    Takes the limits of the limits of the variables (x_lim, v_lim),
    a grid size (grid_size),
    and an acceleration function plus its arguments.
    Returns the grid 'X,V' and the changes in variable values at each point, 'dX, dV'.
    """
    import numpy as np
    X_space = np.linspace(x_lim[0],x_lim[1], grid_size)
    V_space = np.linspace(v_lim[0],v_lim[1], grid_size)
    # intitalize our axes
    X,V = np.meshgrid(X_space,V_space)
    # combine axes
    try:
        dX,dV = V, acc_func(X,V,*fargs)
    except:
        dX,dV = V, acc_func(X,V)
    # calculate change in axes values
    return X,V,dX,dV

def func(a):
    return (a,1)