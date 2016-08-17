#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import AppFunc as func
import BasicFunc as base

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

def Optimize_Q_beta_2(Weight, R_S, R_A, \
                      M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                      a_x, a_y, t, \
                      Q_alpha, phi, theta, \
                      alpha, alpha_dot, alpha_ddot, \
                      beta, beta_dot, beta_ddot, \
                      theta_final, Type, Sex, Method, \
                      tau_Q_alpha, tau_Q_beta, Set_theta):
    #
    # Initialize the arrows
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
    d_beta = 0.0
    tmp_set_Q_beta = 0.0 
    for i in range(111):
        d_Beta = abs(tmp_beta-beta_final)
        #
        if (i<=100):
            set_Q_beta = Q_beta_max1 - i*dQ_beta/100
        else:
            set_Q_beta = Q_beta_max1 - (i+1-100)*dQ_beta
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
        #
    #
    if (tmp_set_Q_beta < Q_beta_min):
        tmp2_set_Q_beta = Q_beta_min
    elif (tmp_set_Q_beta > Q_beta_max):
        tmp2_set_Q_beta = Q_beta_max
    else:
        tmp2_set_Q_beta = tmp_set_Q_beta
    #
    # plot result
    #
    array_dQ_beta = []
    array_Q_beta2 = []
    for j in range(len(array_Q_beta)):
      if (j>0):
        tmp_dQ_beta = array_Q_beta[j] - array_Q_beta[j-1]
        tmp_dbeta = array_beta[j] - array_beta[j-1]
        array_dQ_beta.append(tmp_dbeta/tmp_dQ_beta)
        tmp_Q_beta2 = array_Q_beta[j]
        array_Q_beta2.append(tmp_Q_beta2)
    return tmp2_set_Q_beta, k, array_Q_beta, array_beta, array_Q_beta2, array_dQ_beta

def Track(Weight, R_S, R_A, \
          M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
          a_x, a_y, t, \
          Q_alpha, Q_beta, phi, theta, \
          alpha, alpha_dot, alpha_ddot, \
          beta, beta_dot, beta_ddot, \
          theta_final, Type, Sex, Method, \
          tau_Q_alpha, tau_Q_beta, Set_theta):
    #
    # Tarcking
    #
    print '>>>>> For Wrist-cock torque:', Q_beta+0.01, '(N-m) <<<<<'
    show1_O_x, show1_O_y, \
    show1_arm_x, show1_arm_y, \
    show1_club_x, show1_club_y, \
    show1_arm_rod_x, show1_arm_rod_y, \
    show1_club_rod_x, show1_club_rod_y, \
    show1_t, \
    show1_alpha, show1_beta, \
    show1_theta, show1_VC_angle, show1_omega, \
    show1_alpha_dot, show1_beta_dot, \
    show1_alpha_ddot, show1_beta_ddot, \
    show1_VC, \
    show1_Q_alpha, show1_Q_beta, \
    show1_R, show1_J, show1_S_A, \
    show1_arm1_rod_x, show1_arm1_rod_y, \
    show1_arm2_rod_x, show1_arm2_rod_y, \
    show1_arm3_rod_x, show1_arm3_rod_y, \
    show1_arm4_rod_x, show1_arm4_rod_y = \
    func.Tracking(Weight, R_S, R_A, \
                  M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                  a_x, a_y, t, \
                  Q_alpha, Q_beta+0.01, phi, theta, \
                  alpha, alpha_dot, alpha_ddot, \
                  beta, beta_dot, beta_ddot, \
                  theta_final, Type, Sex, Method, \
                  tau_Q_alpha, tau_Q_beta, Set_theta)
    #
    print '>>>>> For Wrist-cock torque:', Q_beta, '(N-m) <<<<<'
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
                  Q_alpha, Q_beta, phi, theta, \
                  alpha, alpha_dot, alpha_ddot, \
                  beta, beta_dot, beta_ddot, \
                  theta_final, Type, Sex, Method, \
                  tau_Q_alpha, tau_Q_beta, Set_theta)
    #
    print '>>>>> For Wrist-cock torque:', Q_beta-0.01, '(N-m) <<<<<'
    show2_O_x, show2_O_y, \
    show2_arm_x, show2_arm_y, \
    show2_club_x, show2_club_y, \
    show2_arm_rod_x, show2_arm_rod_y, \
    show2_club_rod_x, show2_club_rod_y, \
    show2_t, \
    show2_alpha, show2_beta, \
    show2_theta, show2_VC_angle, show2_omega, \
    show2_alpha_dot, show2_beta_dot, \
    show2_alpha_ddot, show2_beta_ddot, \
    show2_VC, \
    show2_Q_alpha, show2_Q_beta, \
    show2_R, show2_J, show2_S_A, \
    show2_arm1_rod_x, show2_arm1_rod_y, \
    show2_arm2_rod_x, show2_arm2_rod_y, \
    show2_arm3_rod_x, show2_arm3_rod_y, \
    show2_arm4_rod_x, show2_arm4_rod_y = \
    func.Tracking(Weight, R_S, R_A, \
                  M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                  a_x, a_y, t, \
                  Q_alpha, Q_beta-0.01, phi, theta, \
                  alpha, alpha_dot, alpha_ddot, \
                  beta, beta_dot, beta_ddot, \
                  theta_final, Type, Sex, Method, \
                  tau_Q_alpha, tau_Q_beta, Set_theta)
    #
    # get the length of arrays 
    #
    step = len(show_club_x)
    step1 = len(show1_club_x)
    step2 = len(show2_club_x)
    #
    # show results
    #
    print_VC = ("%5.2f" % show_VC[step-1]).strip()
    print1_VC = ("%5.2f" % show1_VC[step1-1]).strip()
    print2_VC = ("%5.2f" % show2_VC[step2-1]).strip()
    #
    print_VC_angle = show_VC_angle[step-1]*180.0/PI
    print1_VC_angle = show1_VC_angle[step1-1]*180.0/PI
    print2_VC_angle = show2_VC_angle[step2-1]*180.0/PI
    print_VC_angle = ("%5.2f" % print_VC_angle).strip()
    print1_VC_angle = ("%5.2f" % print1_VC_angle).strip()
    print2_VC_angle = ("%5.2f" % print2_VC_angle).strip()
    #
    return float(print_VC), float(print1_VC), float(print2_VC), \
           float(print_VC_angle), float(print1_VC_angle), float(print2_VC_angle)

if __name__ == '__main__':
    array_set_Q_beta = []
    array_VC = []
    array1_VC = []
    array2_VC = []
    array_VC_angle = []
    array1_VC_angle = []
    array2_VC_angle = []
    #
    #for i in range(0, 2, 1):
    for i in range(0, 16, 1):
      Q_beta, k, array_Q_beta, array_beta, array_Q_beta2, array_dQ_beta = \
      Optimize_Q_beta_2(Weight, R_S, R_A, \
                        M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
                        a_x, a_y, t, \
                        Q_alpha, phi, theta, \
                        alpha, alpha_dot, alpha_ddot, \
                        beta, beta_dot, beta_ddot, \
                        theta_final, Type, Sex, Method, \
                        tau_Q_alpha, tau_Q_beta, Set_theta-i)

      vc, vc1, vc2, vc_angle, vc1_angle, vc2_angle = \
      Track(Weight, R_S, R_A, \
            M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
            a_x, a_y, t, \
            Q_alpha, Q_beta, phi, theta, \
            alpha, alpha_dot, alpha_ddot, \
            beta, beta_dot, beta_ddot, \
            theta_final, Type, Sex, Method, \
            tau_Q_alpha, tau_Q_beta, Set_theta-i)

      array_set_Q_beta.append(-1*Q_beta)
      array_VC.append(vc)
      array1_VC.append(vc1)
      array2_VC.append(vc2)
      array_VC_angle.append(vc_angle)
      array1_VC_angle.append(vc1_angle)
      array2_VC_angle.append(vc2_angle)

      plt.figure(1)
      plt.grid(True)
      plt.xlabel(r'$-Q_\beta$ (N-m)', fontsize=25)
      plt.ylabel(r'$\beta_f$ (degree)', fontsize=25)
      plt.xticks(fontsize=25)
      plt.yticks(fontsize=25)
      if (i<8):
        plt.text(array_Q_beta[k], 0.0+10*i, r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), fontweight='bold', fontsize=15)
      else:
        plt.text(array_Q_beta[k], 0.0+10*(i-8), r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), fontweight='bold', fontsize=15)
      plt.plot(array_Q_beta[:k-1], array_beta[:k-1], 'r.-', markersize=10, linewidth=1)
      plt.plot(array_Q_beta[k:], array_beta[k:], 'r.-', markersize=10, linewidth=1)
    plt.savefig('Case3-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
    #
    plt.figure(2)
    plt.grid(True)
    plt.xlabel(r'$-Q_\beta$ (N-m)', fontsize=25)
    plt.ylabel('Clubhead velocity (m/sec)', fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.plot(array_set_Q_beta, array_VC, 'k--', markersize=15, linewidth=5, label='Most closed solution')
    plt.fill_between(array_set_Q_beta, array1_VC, array2_VC, facecolor='yellow')
    plt.plot([], [], color='yellow', label='Systematic error range', linewidth=15)
    for i in range(0, 16, 1):
      if (i%2==0):
        plt.text(array_set_Q_beta[i], array_VC[i]+1.0, \
                 r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), color='red', fontweight='bold', fontsize=15)
      else:
        plt.text(array_set_Q_beta[i], array_VC[i]-0.5, \
                 r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), color='red', fontweight='bold', fontsize=15)
    plt.legend(loc='upper left')
    plt.savefig('Case3-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
    #
    plt.figure(3)
    plt.grid(True)
    plt.xlabel(r'$-Q_\beta$ (N-m)', fontsize=25)
    plt.ylabel(r'Clubhead velocity angle $\theta_{\overrightarrow{V_C}}$ (degree)', fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.plot(array_set_Q_beta, array_VC_angle, 'k--', markersize=15, linewidth=5, label='Most closed solution')
    plt.fill_between(array_set_Q_beta, array1_VC_angle, array2_VC_angle, facecolor='yellow')
    plt.plot([], [], color='yellow', label='Systematic error range', linewidth=15)
    for i in range(0, 16, 1):
      if (i%2==0):
        plt.text(array_set_Q_beta[i], array_VC_angle[i]+3.0, \
                 r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), color='red', fontweight='bold', fontsize=15)
      else:
        plt.text(array_set_Q_beta[i], array_VC_angle[i]-3.0, \
                 r'$t_{\theta = %5.0f^{\circ}}$' %(Set_theta-i), color='red', fontweight='bold', fontsize=15)
    plt.legend(loc='upper left')
    plt.savefig('Case3-Fig3.eps', format='eps', dpi=1000, bbox_inches='tight')

