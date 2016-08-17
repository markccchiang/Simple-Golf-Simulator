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

def get_ball_velocity(entries):
    #
    # Calculate ball velocity
    #
    tmp_M_C_head = float(entries['M_C_head'].get()) # mass of the club head (kg)
    ball_mass    = float(entries['ball_mass'].get()) # (degree) 
    COR          = float(entries['COR'].get()) # (degree) 
    VC           = float(entries['VC'].get())
    ans_ball_velocity = base.Ball_velocity(VC, tmp_M_C_head, ball_mass, COR)
    tmp_ans_ball_velocity = ("%5.2f" % ans_ball_velocity).strip()
    entries['ball_U'].delete(0, END)
    entries['ball_U'].config(fg = "red", bg = "yellow")
    entries['ball_U'].insert(0, tmp_ans_ball_velocity)
    #
    # Calculate the elevation angle of ball
    #
    tmp_theta_final   = float(entries['theta_final'].get()) # (degree) 
    tmp_beta_final    = float(entries['beta_final'].get()) # (degree) 
    tmp_VC_angle      = float(entries['VC_angle'].get()) # (degree) 
    tmp_clubhead_loft = float(entries['clubhead_loft'].get()) # (degree) 
    tmp_ans_elevation = tmp_theta_final + tmp_beta_final + tmp_clubhead_loft + tmp_VC_angle
    tmp2_ans_elevation= ("%5.2f" % tmp_ans_elevation).strip()
    entries['ball_theta'].delete(0, END)
    entries['ball_theta'].config(fg = "red", bg = "yellow")
    entries['ball_theta'].insert(0, tmp2_ans_elevation)

def Optimize_Q_beta(entries):
    #
    # Set initial values
    #
    Sex        = str(entries['Gender'].get())
    Weight     = float(entries['Weight'].get()) # golfer's weight (kg)
    R_S        = float(entries['R_S'].get()) # shoulder length (m)
    R_A        = float(entries['R_A'].get()) # arm length (m)
    M_C_head   = float(entries['M_C_head'].get()) # mass of the club head (kg)
    M_C_shaft  = float(entries['M_C_shaft'].get()) # mass of the club shaft (kg)
    L_C_head   = float(entries['L_C_head'].get()) # club head length (m)
    L_C_shaft  = float(entries['L_C_shaft'].get()) # club shaft length (m)
    phi        = float(entries['phi'].get()) # swing plane angle (degree)
    theta      = float(entries['theta'].get()) # (degree) 
    theta_final= float(entries['theta_final'].get()) # (degree) 
    beta       = float(entries['beta'].get()) # (degree) 
    beta_final = float(entries['beta_final'].get()) # (degree) 
    a_x        = float(entries['a_x'].get()) # arm acceleration in horizontal direction (m/sec^2)
    a_y        = float(entries['a_y'].get()) # arm acceleration in vertical direction (m/sec^2)
    Type       = str(entries['Type'].get())
    Q_alpha    = float(entries['Q_alpha'].get()) # (N-m)
    tau_Q_alpha= float(entries['tau_Q_alpha'].get()) # (sec)
    Set_theta  = float(entries['set_theta'].get()) # (degree) 
    tau_Q_beta = float(entries['tau_Q_beta'].get()) # (sec)
    Q_beta_min = float(entries['Q_beta_min'].get()) # (N-m)
    Q_beta_max = float(entries['Q_beta_max'].get()) # (N-m)
    Method     = str(entries['Method'].get())
    alpha      = 0.0 # (degree)
    alpha_dot  = 0.0 # (degree/sec)
    alpha_ddot = 0.0 # (degree/sec^2) 
    beta_dot   = 0.0 # (degree/sec)
    beta_ddot  = 0.0 # (degree/sec^2)
    t          = 0.0 # (sec)
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
    entries['Q_beta'].delete(0, END)
    entries['Q_beta'].config(fg = "red", bg = "yellow")
    entries['Q_beta'].insert(0, tmp2_set_Q_beta)
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
    #
    plt.close('all')
    plt.figure(0)
    plt.clf()
    #
    plt.subplot(2, 1, 1)
    plt.grid(True)
    plt.ylabel(r'$\beta$ (degree)')
    plt.plot(array_Q_beta[:k-1], array_beta[:k-1], 'r.-', markersize=10, linewidth=1)
    plt.plot(array_Q_beta[k:], array_beta[k:], 'r.-', markersize=10, linewidth=1)
    #
    plt.subplot(2, 1, 2)
    plt.grid(True)
    plt.xlabel(r'$-Q_\beta$ (N-m)')
    plt.ylabel(r'$-d\beta/dQ_\beta$ (degree/N-m)')
    plt.plot(array_Q_beta2, array_dQ_beta, 'r.', markersize=10, linewidth=1)
    plt.show()

def Optimize_Q_beta_2(entries):
    #
    # Set initial values
    #
    Sex        = str(entries['Gender'].get())
    Weight     = float(entries['Weight'].get()) # golfer's weight (kg)
    R_S        = float(entries['R_S'].get()) # shoulder length (m)
    R_A        = float(entries['R_A'].get()) # arm length (m)
    M_C_head   = float(entries['M_C_head'].get()) # mass of the club head (kg)
    M_C_shaft  = float(entries['M_C_shaft'].get()) # mass of the club shaft (kg)
    L_C_head   = float(entries['L_C_head'].get()) # club head length (m)
    L_C_shaft  = float(entries['L_C_shaft'].get()) # club shaft length (m)
    phi        = float(entries['phi'].get()) # swing plane angle (degree)
    theta      = float(entries['theta'].get()) # (degree) 
    theta_final= float(entries['theta_final'].get()) # (degree) 
    beta       = float(entries['beta'].get()) # (degree) 
    beta_final = float(entries['beta_final'].get()) # (degree) 
    a_x        = float(entries['a_x'].get()) # arm acceleration in horizontal direction (m/sec^2)
    a_y        = float(entries['a_y'].get()) # arm acceleration in vertical direction (m/sec^2)
    Type       = str(entries['Type'].get())
    Q_alpha    = float(entries['Q_alpha'].get()) # (N-m)
    tau_Q_alpha= float(entries['tau_Q_alpha'].get()) # (sec)
    Set_theta  = float(entries['set_theta'].get()) # (degree) 
    tau_Q_beta = float(entries['tau_Q_beta'].get()) # (sec)
    Q_beta_min = float(entries['Q_beta_min'].get()) # (N-m)
    Q_beta_max = float(entries['Q_beta_max'].get()) # (N-m)
    Method     = str(entries['Method'].get())
    alpha      = 0.0 # (degree)
    alpha_dot  = 0.0 # (degree/sec)
    alpha_ddot = 0.0 # (degree/sec^2) 
    beta_dot   = 0.0 # (degree/sec)
    beta_ddot  = 0.0 # (degree/sec^2)
    t          = 0.0 # (sec)
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
    # Print results
    #
    tmp2_set_Q_beta = ("%5.2f" % tmp2_set_Q_beta).strip()
    entries['Q_beta'].delete(0, END)
    entries['Q_beta'].config(fg = "red", bg = "yellow")
    entries['Q_beta'].insert(0, tmp2_set_Q_beta)
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
    #
    plt.close('all')
    plt.figure(0)
    plt.clf()
    #
    plt.subplot(2, 1, 1)
    plt.grid(True)
    plt.ylabel(r'$\beta$ (degree)')
    plt.plot(array_Q_beta[:k-1], array_beta[:k-1], 'r.-', markersize=10, linewidth=1)
    plt.plot(array_Q_beta[k:], array_beta[k:], 'r.-', markersize=10, linewidth=1)
    #
    plt.subplot(2, 1, 2)
    plt.grid(True)
    plt.xlabel(r'$-Q_\beta$ (N-m)')
    plt.ylabel(r'$-d\beta/dQ_\beta$ (degree/N-m)')
    plt.plot(array_Q_beta2, array_dQ_beta, 'r.', markersize=10, linewidth=1)
    plt.show()

def Plot(entries):
    #
    # Set initial values
    #
    Sex        = str(entries['Gender'].get())
    Weight     = float(entries['Weight'].get()) # golfer's weight (kg)
    R_S        = float(entries['R_S'].get()) # shoulder length (m)
    R_A        = float(entries['R_A'].get()) # arm length (m)
    M_C_head   = float(entries['M_C_head'].get()) # mass of the club head (kg)
    M_C_shaft  = float(entries['M_C_shaft'].get()) # mass of the club shaft (kg)
    L_C_head   = float(entries['L_C_head'].get()) # club head length (m)
    L_C_shaft  = float(entries['L_C_shaft'].get()) # club shaft length (m)
    phi        = float(entries['phi'].get()) # swing plane angle (degree)
    theta      = float(entries['theta'].get()) # (degree) 
    theta_final= float(entries['theta_final'].get()) # (degree) 
    beta       = float(entries['beta'].get()) # (degree) 
    beta_final = float(entries['beta_final'].get()) # (degree) 
    a_x        = float(entries['a_x'].get()) # arm acceleration in horizontal direction (m/sec^2)
    a_y        = float(entries['a_y'].get()) # arm acceleration in vertical direction (m/sec^2)
    Type       = str(entries['Type'].get())
    Q_alpha    = float(entries['Q_alpha'].get()) # (N-m)
    tau_Q_alpha= float(entries['tau_Q_alpha'].get()) # (sec)
    Q_beta     = float(entries['Q_beta'].get()) # (N-m)
    Set_theta  = float(entries['set_theta'].get()) # (degree) 
    tau_Q_beta = float(entries['tau_Q_beta'].get()) # (sec)
    Q_beta_min = float(entries['Q_beta_min'].get()) # (N-m)
    Q_beta_max = float(entries['Q_beta_max'].get()) # (N-m)
    Method     = str(entries['Method'].get())
    alpha      = 0.0 # (degree)
    alpha_dot  = 0.0 # (degree/sec)
    alpha_ddot = 0.0 # (degree/sec^2) 
    beta_dot   = 0.0 # (degree/sec)
    beta_ddot  = 0.0 # (degree/sec^2)
    t          = 0.0 # (sec)
    Fig1       = str(entries['Fig1'].get())
    Fig2       = str(entries['Fig2'].get())
    Fig3       = str(entries['Fig3'].get())
    Fig4       = str(entries['Fig4'].get())
    Fig5       = str(entries['Fig5'].get())
    Fig6       = str(entries['Fig6'].get())
    Fig7       = str(entries['Fig7'].get())
    Fig8       = str(entries['Fig8'].get())
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
    entries['VC'].delete(0, END)
    entries['VC'].config(fg = "red", bg = "cyan")
    entries['VC'].insert(0, print_VC)
    #
    print_VC_angle = show_VC_angle[step-1]*180.0/PI
    print1_VC_angle = show1_VC_angle[step1-1]*180.0/PI
    print2_VC_angle = show2_VC_angle[step2-1]*180.0/PI
    print_VC_angle = ("%5.2f" % print_VC_angle).strip()
    print1_VC_angle = ("%5.2f" % print1_VC_angle).strip()
    print2_VC_angle = ("%5.2f" % print2_VC_angle).strip()
    entries['VC_angle'].delete(0, END)
    entries['VC_angle'].config(fg = "red", bg = "cyan")
    entries['VC_angle'].insert(0, print_VC_angle)
    #
    #
    error1_VC = float(print1_VC) - float(print_VC)
    error2_VC = float(print2_VC) - float(print_VC)
    print_error_VC = '['+("%5.2f" % error1_VC).strip()+', '+("%5.2f" % error2_VC).strip()+']'
    entries['error_VC'].delete(0, END)
    entries['error_VC'].config(fg = "red", bg = "cyan")
    entries['error_VC'].insert(0, print_error_VC)
    #
    error1_VC_angle = float(print1_VC_angle) - float(print_VC_angle)
    error2_VC_angle = float(print2_VC_angle) - float(print_VC_angle)
    print_error_VC_angle = '['+("%5.2f" % error1_VC_angle).strip()+', '+("%5.2f" % error2_VC_angle).strip()+']'
    entries['error_VC_angle'].delete(0, END)
    entries['error_VC_angle'].config(fg = "red", bg = "cyan")
    entries['error_VC_angle'].insert(0, print_error_VC_angle)

    #
    # plot results
    #
    plt.ion()
    plt.close('all')
    if (Fig1 == 'True'): 
      plt.figure(1)
      plt.clf()
      plt.xlabel('x (m)')
      plt.ylabel('y (m)')
      plt.plot(show_arm_x, show_arm_y, 'r-', label="Wrist-cock", markersize=13, linewidth=5)
      plt.plot(show_club_x, show_club_y, 'b-', label="Club head", markersize=13, linewidth=5)
      plt.plot(show_club_rod_x[0:2], show_club_rod_y[0:2], 'k-', linewidth=2)
      plt.plot(show_arm_rod_x[0:2], show_arm_rod_y[0:2], 'k:', linewidth=2)
      plt.plot(show_arm1_rod_x[0:2], show_arm1_rod_y[0:2], 'k-', linewidth=2)
      plt.plot(show_arm2_rod_x[0:2], show_arm2_rod_y[0:2], 'k-', linewidth=2)
      plt.plot(show_arm3_rod_x[0:2], show_arm3_rod_y[0:2], 'k-', linewidth=2)
      plt.plot(show_arm4_rod_x[0:2], show_arm4_rod_y[0:2], 'k-', linewidth=2)
      interval_steps = 9
      for k in range(interval_steps):
          interval = int(step/interval_steps)
          plt.plot(show_club_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_club_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k-', \
                   linewidth=2)
          plt.plot(show_arm_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_arm_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k:', \
                   linewidth=2)
          plt.plot(show_arm1_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_arm1_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k-', \
                   linewidth=2)
          plt.plot(show_arm2_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_arm2_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k-', \
                   linewidth=2)
          plt.plot(show_arm3_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_arm3_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k-', \
                   linewidth=2)
          plt.plot(show_arm4_rod_x[step*2-2-k*interval*2:step*2-k*interval*2], \
                   show_arm4_rod_y[step*2-2-k*interval*2:step*2-k*interval*2], 'k-', \
                   linewidth=2)
      plt.plot(show_O_x, show_O_y, 'm.-', label="Arm axis", markersize=13, linewidth=5)
      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #--------------------------------------------------
    if (Fig2 == 'True'): 
      plt.figure(2)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Angle (degree)')
      plt.plot(show_t[:step], show_alpha[:step]*180.0/PI, 'r-', \
               label=r"$\alpha$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_beta[:step]*180.0/PI, 'b-', \
               label=r"$\beta$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_theta[:step]*180.0/PI, 'c-', \
               label=r"$\theta$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], (show_beta[:step]+show_theta[:step])*180.0/PI, 'k-', \
               label=r"$\theta+\beta$", markersize=10, linewidth=5)
      plt.plot(show_t[1:step], show_VC_angle[1:step]*180.0/PI, 'g-', \
               label=r"$\theta_{\overrightarrow{V_C}}$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_omega[:step]*180.0/PI, 'y-', \
               label=r"$\omega$", markersize=10, linewidth=5)
      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #--------------------------------------------------
    if (Fig3 == 'True'): 
      plt.figure(3)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Anglular velocity (degree/sec)')
      plt.plot(show_t[:step], show_alpha_dot[:step]*180.0/PI, 'r-', \
               label=r"$\dot{\alpha}$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_beta_dot[:step]*180.0/PI, 'b-', \
               label=r"$\dot{\beta}$", markersize=10, linewidth=5)
      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #--------------------------------------------------
    if (Fig4 == 'True'): 
      plt.figure(4)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Anglular acceleration (degree/sec$^2$)')
      plt.plot(show_t[:step], show_alpha_ddot[:step]*180.0/PI, 'r-', \
               label=r"$\ddot{\alpha}$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_beta_ddot[:step]*180.0/PI, 'b-', \
               label=r"$\ddot{\beta}$", markersize=10, linewidth=5)
      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #--------------------------------------------------
    if (Fig5 == 'True'): 
      plt.figure(5)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Clubhead velocity (m/sec)')
      plt.plot(show_t[:step], show_VC[:step], 'k-', markersize=10, linewidth=5)
    #--------------------------------------------------
    if (Fig6 == 'True'): 
      plt.figure(6)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Torque (N-m)')
      plt.ylim(min(-1*show_Q_beta)-10.0, max(show_Q_alpha)+10.0)
      plt.plot(show_t[:step], show_Q_alpha[:step], 'r-', \
               label=r"$Q_\alpha$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], -1*show_Q_beta[:step], 'b-', \
               label=r"$-Q_\beta$", markersize=10, linewidth=5)
      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #--------------------------------------------------
    if (Fig7 == 'True'):
        plt.figure(7)
        plt.clf()
        plt.xlabel('Time (sec)')
        plt.ylabel(r'$J$ (kg-m$^2$)', color="b")
        plt.tick_params(axis="y", labelcolor="b")
        plt.plot(show_t[:step], show_J[:step], 'b-', markersize=10, linewidth=5)
        plt.twinx()
        plt.ylabel(r'$S_A$ (kg-m)', color="r")
        plt.tick_params(axis="y", labelcolor="r")
        plt.plot(show_t[:step], show_S_A[:step], 'r-', markersize=10, linewidth=5)
    #--------------------------------------------------
    if (Fig8 == 'True'):
        plt.figure(8)
        plt.clf()
        plt.xlabel('Time (sec)')
        plt.ylabel(r'$R$ (m)')
        plt.tick_params(axis="y")
        plt.plot(show_t[:step], show_R[:step], 'k-', markersize=10, linewidth=5)
    #--------------------------------------------------
    plt.show()

