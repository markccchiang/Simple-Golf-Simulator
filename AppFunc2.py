from math import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import BasicFunc2 as func

def TRACK(m, D, rho_air, C_D, C_L, \
          v_ball, theta, phi, \
          w_theta, w_phi, \
          v_wind, wind_theta, wind_phi, \
          altitude):
    ##########################################################################
    #
    # set initial conditions
    #
    #---------------------------------------------------
    PI             = 3.141592653589793
    theta_rad      = theta*PI/180 # (rad)
    phi_rad        = phi*PI/180 # (rad)
    w_theta_rad    = w_theta*PI/180 # (rad)
    w_phi_rad      = w_phi*PI/180 # (rad)
    wind_theta_rad = wind_theta*PI/180 # (rad)
    wind_phi_rad   = wind_phi*PI/180 # (rad)
    #
    t0          = 0.0 
    x0          = 0.0
    y0          = 0.0
    z0          = 0.0
    v_x0        = v_ball*cos(theta_rad)*cos(phi_rad)
    v_y0        = v_ball*cos(theta_rad)*sin(phi_rad)
    v_z0        = v_ball*sin(theta_rad)
    w_unit_i    = cos(w_theta_rad)*cos(w_phi_rad)              # angular unit vector in i
    w_unit_j    = cos(w_theta_rad)*sin(w_phi_rad)              # angular unit vector in j
    w_unit_k    = sin(w_theta_rad)                             # angular unit vector in k
    v_wind_i    = v_wind*cos(wind_theta_rad)*cos(wind_phi_rad) # wind velocity vector in i
    v_wind_j    = v_wind*cos(wind_theta_rad)*sin(wind_phi_rad) # wind velocity vector in j
    v_wind_k    = v_wind*sin(wind_theta_rad)                   # wind velocity vector in k
    #---------------------------------------------------
    #
    # set arrays and input initial conditions
    #
    elements   = 100000 # simulate within 100 seconds
    show_t     = np.zeros(elements)
    show_x     = np.zeros(elements)
    show_y     = np.zeros(elements)
    show_z     = np.zeros(elements)
    show_vx    = np.zeros(elements)
    show_vy    = np.zeros(elements)
    show_vz    = np.zeros(elements)
    show_t[0]  = t0
    show_x[0]  = x0
    show_y[0]  = y0
    show_z[0]  = z0
    show_vx[0] = v_x0
    show_vy[0] = v_y0
    show_vz[0] = v_z0
    #
    # do loop
    #
    j     = 0
    tmp_z = z0
    tmp_vz= 0
    step  = 0
    while (tmp_z >= altitude or tmp_vz >= 0 and j+1 < elements):
        show_t[j+1], show_vx[j+1], show_vy[j+1], show_vz[j+1], \
        show_x[j+1],  show_y[j+1], show_z[j+1] = \
        func.RK4(show_t[j], \
                 show_x[j],  show_y[j], show_z[j], \
                 show_vx[j], show_vy[j], show_vz[j], \
                 v_wind_i, v_wind_j, v_wind_k, \
                 w_unit_i, w_unit_j, w_unit_k, \
                 C_D, C_L, rho_air, m, D)
        tmp_z = show_z[j+1]
        tmp_vz= show_vz[j+1]
        j=j+1
        step=j
    print_show_x = ("%5.3f" % show_x[step]).strip()
    print_show_y = ("%5.3f" % show_y[step]).strip()
    print_show_t = ("%5.3f" % show_t[step]).strip()
    tmp_distance = sqrt(show_x[step]**2 + show_y[step]**2)
    print_distance = ("%5.3f" % tmp_distance).strip()
    print '    Fly time:           ', print_show_t, '(sec)'
    print '    Fly distance:       ', print_distance, '(m)'
    print '    Drop location in X: ', print_show_x, '(m)'
    print '    Drop location in Y: ', print_show_y, '(m)'
    print '--------------------------------------------'
    return show_x[:step+1], show_y[:step+1], show_z[:step+1]
    ##########################################################################

