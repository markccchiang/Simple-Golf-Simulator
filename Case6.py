#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

import matplotlib.pyplot as plt
import AppFunc as func
import BasicFunc as base

PI = 3.141592653589793

Sex        = 'Male'
Weight     = 70.0 # golfer's weight (kg)
R_S        = 0.17 # shoulder length (m)
R_A        = 0.6 # arm length (m)
#M_C_head   = 0.2 # mass of the club head (kg)
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
theta      = 135.0 # (degree) 
theta_final= 0.0 # (degree) 
beta_final = 0.0 # (degree) 
alpha      = 0.0 # (degree)
alpha_dot  = 0.0 # (degree/sec)
alpha_ddot = 0.0 # (degree/sec^2) 
beta       = 120.0 # (degree) 
beta_dot   = 0.0 # (degree/sec)
beta_ddot  = 0.0 # (degree/sec^2)
t          = 0.0 # (sec)
Type       = 'Type I'
Q_beta_min = -50.0 # (N-m)
Q_beta_max = 0.0 # (N-m)
Method     = 'Solution 3'
Set_theta  = theta # (degree) 
M_ball     = 0.0458 # (kg)
COR        = 0.775

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
    # Print results
    #
    tmp2_set_Q_beta = ("%5.2f" % tmp2_set_Q_beta).strip()
    tmp_VC = ("%5.2f" % tmp_VC).strip()
    #print '********************************************'
    #print 'The optimized wrist-cock torque:', tmp2_set_Q_beta, '(N-m)' 
    #print 'The clubhead velocity:', tmp2_VC, '(m/sec)'
    #print '********************************************'
    return float(tmp2_set_Q_beta), float(tmp_VC)

if __name__ == '__main__':
    array_M_C_head = []
    array_Q_beta = []
    array_VC = []
    array_V_ball = []
    #
    # Do loop
    #
    #for i in range(50, 401, 1):
    for i in range(50, 301, 1):
    #for i in range(300, 401, 1):
      set_M_C_head = i*0.001
      Q_beta, VC = Optimize_Q_beta(Weight, R_S, R_A, \
                                   set_M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                                   a_x, a_y, t, \
                                   Q_alpha, phi, theta, \
                                   alpha, alpha_dot, alpha_ddot, \
                                   beta, beta_dot, beta_ddot, \
                                   theta_final, Type, Sex, Method, \
                                   tau_Q_alpha, tau_Q_beta, Set_theta)
      V_ball = base.Ball_velocity(VC, set_M_C_head, M_ball, COR)
      array_M_C_head.append(set_M_C_head)
      array_Q_beta.append(-1*Q_beta)
      array_VC.append(VC)
      array_V_ball.append(V_ball)
      print '********************************************'
      print 'The clubhead mass:', set_M_C_head, '(kg)' 
      print 'The optimized wrist-cock torque:', Q_beta, '(N-m)' 
      print 'The clubhead velocity:', VC, '(m/sec)'
      print 'The golf ball velocity:', V_ball, '(m/sec)'
      print '********************************************'
    #print array_M_C_head, array_Q_beta, array_VC

    #
    # Plot results
    #
    plt.figure(1)
    plt.xlabel('Clubhead mass (kg)', fontsize=20)
    plt.ylabel('Clubhead velocity (m/sec)', fontsize=20, color="b")
    plt.tick_params(axis="y", labelcolor="b")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(array_M_C_head, array_VC, 'b.-', markersize=10, linewidth=5)
    plt.twinx()
    plt.ylabel('Golf ball velocity (m/sec)', fontsize=20, color="r")
    plt.tick_params(axis="y", labelcolor="r")
    plt.yticks(fontsize=20)
    plt.plot(array_M_C_head, array_V_ball, 'r.-', markersize=10, linewidth=5)    
    plt.savefig('Case6-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
    #
    plt.figure(2)
    plt.xlabel('Clubhead mass (kg)', fontsize=20)
    plt.ylabel(r'$-Q_\beta$ (N-m)', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(array_M_C_head, array_Q_beta, 'k.-', markersize=10, linewidth=5)
    plt.savefig('Case6-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')

