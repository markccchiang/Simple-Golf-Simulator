#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import AppFunc as func
import BasicFunc as base
import numpy as np

PI = 3.141592653589793

Sex        = 'Male'
Weight     = 70.0 # golfer's weight (kg)
R_S        = 0.17 # shoulder length (m)
R_A        = 0.6 # arm length (m)
M_C_head   = 0.2 # mass of the club head (kg)
M_C_shaft  = 0.1 # mass of the club shaft (kg)
L_C_head   = 0.1 # club head length (m)
L_C_shaft  = 1.0 # club shaft length (m)
Q_alpha    = 100.0 # (N-m)
#Q_beta     = -20.64 # (N-m)
tau_Q_alpha= 0.01 # (sec)
tau_Q_beta = 0.01 # (sec)
a_x        = 0.0 # arm acceleration in horizontal direction (m/sec^2)
a_y        = 0.0 # arm acceleration in vertical direction (m/sec^2)
phi        = 60.0 # swing plane angle (degree)
#theta      = 135.0 # (degree) 
theta_final= 0.0 # (degree) 
beta_final = 0.0 # (degree) 
alpha      = 0.0 # (degree)
alpha_dot  = 0.0 # (degree/sec)
alpha_ddot = 0.0 # (degree/sec^2) 
#beta       = 120.0 # (degree) 
beta_dot   = 0.0 # (degree/sec)
beta_ddot  = 0.0 # (degree/sec^2)
t          = 0.0 # (sec)
Type       = 'Type I'
Q_beta_min = -50.0 # (N-m)
Q_beta_max = 0.0 # (N-m)
Method     = 'Solution 3'
#Set_theta  = theta # (degree) 

def Optimize_Q_beta(Weight, R_S, R_A, \
                    M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                    a_x, a_y, t, \
                    Q_alpha, phi, theta, \
                    alpha, alpha_dot, alpha_ddot, \
                    beta, beta_dot, beta_ddot, \
                    theta_final, Type, Sex, Method, \
                    tau_Q_alpha, tau_Q_beta, Set_theta):
    #
    # Set initial values
    #
    array_Q_beta = []
    array_beta = []
    #
    # Do loop 
    #
    dQ_beta = 1.0 # (N-m)
    i = 0
    k = 0
    tmp_beta = 180.0 # (degree)
    set_Q_beta = Q_beta_max
    #
    # Step 1
    #
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max - i*dQ_beta
        print '>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<'
        #
        show_O_x, show_O_y, \
        show_arm_x, show_arm_y, \
        show_club_x, show_club_y, \
        show_arm_rod_x, show_arm_rod_y, \
        show_club_rod_x, show_club_rod_y, \
        show_t, \
        show_alpha, show_beta, \
        show_theta, show_VC_angle, show_omega, \
        show_alpha_dot, show_beta_dot, \
        show_alpha_ddot, show_beta_ddot, \
        show_VC, \
        show_Q_alpha, show_Q_beta, \
        show_R, show_J, show_S_A, \
        show_arm1_rod_x, show_arm1_rod_y, \
        show_arm2_rod_x, show_arm2_rod_y, \
        show_arm3_rod_x, show_arm3_rod_y, \
        show_arm4_rod_x, show_arm4_rod_y = \
        func.Tracking(Weight, R_S, R_A, \
                      M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                      a_x, a_y, t, \
                      Q_alpha, set_Q_beta, phi, theta, \
                      alpha, alpha_dot, alpha_ddot, \
                      beta, beta_dot, beta_ddot, \
                      theta_final, Type, Sex, Method, \
                      tau_Q_alpha, tau_Q_beta, Set_theta)
        #
        End = len(show_beta)-1
        tmp_beta = show_beta[End]*180.0/PI
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1
        k = i   
    #
    # Step 2
    #
    i = 0
    tmp_beta = 180.0 # (degree)
    Q_beta_max1 = set_Q_beta + dQ_beta 
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max1 - i*dQ_beta/10
        print '>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<'
        #
        show_O_x, show_O_y, \
        show_arm_x, show_arm_y, \
        show_club_x, show_club_y, \
        show_arm_rod_x, show_arm_rod_y, \
        show_club_rod_x, show_club_rod_y, \
        show_t, \
        show_alpha, show_beta, \
        show_theta, show_VC_angle, show_omega, \
        show_alpha_dot, show_beta_dot, \
        show_alpha_ddot, show_beta_ddot, \
        show_VC, \
        show_Q_alpha, show_Q_beta, \
        show_R, show_J, show_S_A, \
        show_arm1_rod_x, show_arm1_rod_y, \
        show_arm2_rod_x, show_arm2_rod_y, \
        show_arm3_rod_x, show_arm3_rod_y, \
        show_arm4_rod_x, show_arm4_rod_y = \
        func.Tracking(Weight, R_S, R_A, \
                      M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                      a_x, a_y, t, \
                      Q_alpha, set_Q_beta, phi, theta, \
                      alpha, alpha_dot, alpha_ddot, \
                      beta, beta_dot, beta_ddot, \
                      theta_final, Type, Sex, Method, \
                      tau_Q_alpha, tau_Q_beta, Set_theta)
        #
        End = len(show_beta)-1
        tmp_beta = show_beta[End]*180.0/PI
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1   
    #
    # Step 3
    #
    i = 0
    tmp_beta = 180.0 # (degree)
    tmp_VC = 0.0
    Q_beta_max2 = set_Q_beta + dQ_beta/10
    d_beta = 0.0
    tmp_set_Q_beta = 0.0 
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        d_Beta = abs(tmp_beta-beta_final)
        #
        set_Q_beta = Q_beta_max2 - i*dQ_beta/100
        print '>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<'
        #
        show_O_x, show_O_y, \
        show_arm_x, show_arm_y, \
        show_club_x, show_club_y, \
        show_arm_rod_x, show_arm_rod_y, \
        show_club_rod_x, show_club_rod_y, \
        show_t, \
        show_alpha, show_beta, \
        show_theta, show_VC_angle, show_omega, \
        show_alpha_dot, show_beta_dot, \
        show_alpha_ddot, show_beta_ddot, \
        show_VC, \
        show_Q_alpha, show_Q_beta, \
        show_R, show_J, show_S_A, \
        show_arm1_rod_x, show_arm1_rod_y, \
        show_arm2_rod_x, show_arm2_rod_y, \
        show_arm3_rod_x, show_arm3_rod_y, \
        show_arm4_rod_x, show_arm4_rod_y = \
        func.Tracking(Weight, R_S, R_A, \
                      M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                      a_x, a_y, t, \
                      Q_alpha, set_Q_beta, phi, theta, \
                      alpha, alpha_dot, alpha_ddot, \
                      beta, beta_dot, beta_ddot, \
                      theta_final, Type, Sex, Method, \
                      tau_Q_alpha, tau_Q_beta, Set_theta)
        #
        End = len(show_beta)-1
        tmp_beta = show_beta[End]*180.0/PI
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        #
        if (d_Beta > abs(tmp_beta-beta_final)):
            tmp_set_Q_beta = set_Q_beta            
            tmp_VC = show_VC[End]
        #
        i = i+1   
    #
    if (tmp_set_Q_beta < Q_beta_min):
        tmp2_set_Q_beta = Q_beta_min
    elif (tmp_set_Q_beta > Q_beta_max):
        tmp2_set_Q_beta = Q_beta_max
    else:
        tmp2_set_Q_beta = tmp_set_Q_beta

    #
    # return results
    #
    tmp2_set_Q_beta = ("%5.2f" % tmp2_set_Q_beta).strip()
    tmp_VC = ("%5.2f" % tmp_VC).strip()
    return float(tmp2_set_Q_beta), float(tmp_VC)

if __name__ == '__main__':
    array_theta = []
    array_beta = []
    array_Q_beta = []
    array_VC = []
    #
    # Do loop
    #
    ##for i in range(90, 136, 1):
    ##  for j in range(90, 136, 1):
    for i in range(0, 91, 1):
      for j in range(0, 91, 1):
    #for i in range(0, 7, 1):
    #  for j in range(0, 7, 1):
        set_theta = 90+i/2.0
        set_beta = 90+j/2.0
        #print set_theta, set_beta
        set_theta2 = set_theta
        Q_beta, VC = Optimize_Q_beta(Weight, R_S, R_A, \
                                     M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                                     a_x, a_y, t, \
                                     Q_alpha, phi, set_theta, \
                                     alpha, alpha_dot, alpha_ddot, \
                                     set_beta, beta_dot, beta_ddot, \
                                     theta_final, Type, Sex, Method, \
                                     tau_Q_alpha, tau_Q_beta, set_theta2)
        array_theta.append(set_theta)
        array_beta.append(set_beta)
        array_Q_beta.append(-1*Q_beta)
        array_VC.append(VC)
        #print '********************************************'
        #print 'The initial arm angle:', set_theta, '(degree)'
        #print 'The initial wrist-cock angle:', set_beta, '(degree)'
        #print 'The optimized wrist-cock torque:', Q_beta, '(N-m)' 
        #print 'The clubhead velocity:', VC, '(m/sec)'
        #print '********************************************'
    #print array_theta
    #print array_beta
    #print array_VC
    #print array_Q_beta 
    #np.savetxt('Case4.dat', (array_theta, array_beta, array_VC, array_Q_beta), fmt='%5.3f')
    #
    # Plot results
    #
    plt.figure(1)
    plt.xlabel(r'$\theta_0$ (degree)', fontsize=25)
    plt.ylabel(r'$\beta_0$ (degree)', fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.hexbin(array_theta, array_beta, C=array_VC, gridsize=45, cmap=cm.jet, bins=None)
    plt.axis([min(array_theta)-1, max(array_theta)+1, min(array_beta)-1, max(array_beta)+1])
    #cb = plt.colorbar(image,spacing='uniform',extend='max')
    cb = plt.colorbar()
    cb.set_label('Clubhead velocity (m/sec)', fontsize=25)
    plt.savefig('Case4-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
    #
    plt.figure(2)
    plt.xlabel(r'$\theta_0$ (degree)', fontsize=25)
    plt.ylabel(r'$\beta_0$ (degree)', fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.hexbin(array_theta, array_beta, C=array_Q_beta, gridsize=45, cmap=cm.jet, bins=None)
    plt.axis([min(array_theta)-1, max(array_theta)+1, min(array_beta)-1, max(array_beta)+1])
    #cb = plt.colorbar(image,spacing='uniform',extend='max')
    cb = plt.colorbar()
    cb.set_label(r'$-Q_\beta$ (N-m)', fontsize=25)
    plt.savefig('Case4-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
    #plt.show()

