from math import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import BasicFunc as func

def Tracking(Weight, R_S, R_A, \
             M_C_head, M_C_shaft, L_C_head, L_C_shaft, \
             a_x, a_y, t, \
             Q_alpha, Q_beta, phi, theta, \
             alpha, alpha_dot, alpha_ddot, \
             beta, beta_dot, beta_ddot, \
             theta_final, Type, Sex, Method, \
             tau_Q_alpha, tau_Q_beta, Set_theta):
    #
    # Check theta settings
    #
    if (Set_theta > theta):
       Set_theta = theta
    if (theta_final > theta):
       theta_final = theta
    #
    # Calculate club and arm parameters
    #
    M_C, L, S_C, I = func.club_para(M_C_head, M_C_shaft, L_C_head, L_C_shaft)
    R_A1 = R_A/2 # upper arm length (m)
    R_A2 = R_A/2 # forearm length (m) 
    #
    if (Sex == 'Male'):
        percentage_of_upperarm = 0.0325 # percentage of upperarm
        percentage_of_forearm  = 0.0187 # percentage of forearm
        percentage_of_hand     = 0.0065 # percentage of hand
    elif (Sex == 'Female'):
        percentage_of_upperarm = 0.0290 # percentage of upperarm
        percentage_of_forearm  = 0.0157 # percentage of forearm
        percentage_of_hand     = 0.0050 # percentage of hand
    else:
        percentage_of_upperarm = 0.03075 # percentage of upperarm
        percentage_of_forearm  = 0.01720 # percentage of forearm
        percentage_of_hand     = 0.00575 # percentage of hand
    #
    #rho_S  = Weight*percentage_of_upperarm/(2*R_A1)
    rho_S  = 0.0 # do not consider 1st and 2nd moments of shoulder
    rho_A1 = Weight*percentage_of_upperarm/(2*R_A1)
    rho_A2 = Weight*(percentage_of_forearm+percentage_of_hand)/(2*R_A2)
    omega_min = func.bending_arm_angle_min(R_S, R_A)
    PI = 3.141592653589793
    h = func.h  
    #
    # Set initial loop conditions
    #
    elements        = 20000 # sumulate within 2 seconds 
    show_t          = np.zeros(elements)
    show_alpha      = np.zeros(elements)
    show_alpha_dot  = np.zeros(elements) 
    show_alpha_ddot = np.zeros(elements) 
    show_beta       = np.zeros(elements) 
    show_beta_dot   = np.zeros(elements) 
    show_beta_ddot  = np.zeros(elements) 
    show_theta      = np.zeros(elements) 
    show_VC         = np.zeros(elements)
    show_VC_x       = np.zeros(elements)
    show_VC_y       = np.zeros(elements)
    show_VC_angle   = np.zeros(elements)
    show_VC_check   = np.zeros(elements)
    show_VC_check1  = np.zeros(elements)
    show_arm_x      = np.zeros(elements)
    show_arm_y      = np.zeros(elements)
    show_club_x     = np.zeros(elements)
    show_club_y     = np.zeros(elements)
    show_arm_rod_x  = np.zeros(elements)
    show_arm_rod_y  = np.zeros(elements)
    show_arm1_rod_x = np.zeros(elements)
    show_arm1_rod_y = np.zeros(elements)
    show_arm2_rod_x = np.zeros(elements)
    show_arm2_rod_y = np.zeros(elements)
    show_arm3_rod_x = np.zeros(elements)
    show_arm3_rod_y = np.zeros(elements)
    show_arm4_rod_x = np.zeros(elements)
    show_arm4_rod_y = np.zeros(elements)
    show_club_rod_x = np.zeros(elements)
    show_club_rod_y = np.zeros(elements)
    show_O_x        = np.zeros(elements)
    show_O_y        = np.zeros(elements)
    show_Q_alpha    = np.zeros(elements)
    show_Q_beta     = np.zeros(elements)
    show_omega      = np.zeros(elements)
    show_R          = np.zeros(elements)
    show_delta      = np.zeros(elements)
    show_lambda1    = np.zeros(elements)
    show_sigma      = np.zeros(elements) 
    show_J          = np.zeros(elements)
    show_S_A        = np.zeros(elements)
    show_arm1_x     = np.zeros(elements)
    show_arm2_x     = np.zeros(elements)
    show_arm3_x     = np.zeros(elements)
    show_arm1_y     = np.zeros(elements)
    show_arm2_y     = np.zeros(elements)
    show_arm3_y     = np.zeros(elements)
    show_t[0]          = t # (sec)
    show_alpha[0]      = alpha*PI/180.0 # (rad)
    show_alpha_dot[0]  = alpha_dot*PI/180.0 # (rad/sec)
    show_alpha_ddot[0] = alpha_ddot*PI/180.0 # (rad/sec^2) 
    show_beta[0]       = beta*PI/180.0 # (rad)  
    show_beta_dot[0]   = beta_dot*PI/180.0 # (rad/sec)  
    show_beta_ddot[0]  = beta_ddot*PI/180.0 # (rad/sec^2) 
    show_theta[0]      = theta*PI/180.0 # (rad)
    show_Q_alpha[0]    = Q_alpha
    show_Q_beta[0]     = Q_beta
    #-----------------------------------------------------------------------------------------------------------
    if (Type == 'Type I'):
        show_omega[0] = PI
    elif (Type == 'Type II'):
        show_omega[0] = omega_min
    else:
        show_omega[0] = PI
    #-----------------------------------------------------------------------------------------------------------
    #
    # do loop
    #
    i = 0
    step = 0
    tmp_angle = show_theta[0] # (rad)
    t0 = 0.0
    while (tmp_angle >= theta_final*PI/180.0 and i+1 < elements):
        #------------------------------------------------------------------
        if (Type == 'Type I'):
            show_omega[i] = PI
        elif (Type == 'Type II'):
            show_omega[i] = func.bending_arm_angle(show_theta[0], show_alpha[i], show_omega[0])
        else:
            show_omega[i] = PI
        #------------------------------------------------------------------
        show_R[i], show_delta[i], show_lambda1[i], show_sigma[i] = func.bending_arm_para(R_S, R_A, show_omega[i])
        show_J[i] = func.J_TypeII(R_S, R_A, rho_S, rho_A1, rho_A2, show_R[i], show_delta[i], show_lambda1[i], show_sigma[i])
        show_S_A[i] = func.S_A_TypeII(R_S, R_A, rho_S, rho_A1, rho_A2, show_R[i], show_delta[i], show_lambda1[i], show_sigma[i])  
        #------------------------------------------------------------------
        show_theta[i] = show_theta[0] - show_alpha[i] 
        #------------------------------------------------------------------
        show_Q_alpha[i] = func.func_Q_alpha(show_t[i], tau_Q_alpha, Q_alpha)
        #------------------------------------------------------------------
        if (show_theta[i] > Set_theta*PI/180.0):
            t0 = show_t[i]
        #print t0
        #show_Q_beta[i]  = func.func_Q_beta(show_t[i], tau_Q_beta, Q_beta, show_theta[i], show_theta[0], t0)
        show_Q_beta[i]  = func.func_Q_beta(show_t[i], tau_Q_beta, Q_beta, show_theta[i], Set_theta*PI/180.0, t0)
        #------------------------------------------------------------------
        show_arm_x[i], show_arm_y[i]   = func.func_arm_xy(show_theta[i], show_R[i])
        show_club_x[i], show_club_y[i] = func.func_club_xy(show_theta[i], show_beta[i], show_R[i], L)
        show_O_x[i], show_O_y[i]       = func.func_O_xy(show_t[i])
        #------------------------------------------------------------------
        arm_phase_angle1 = func.nrom_rad - show_theta[i] + PI - show_sigma[i]
        arm_phase_angle2 = arm_phase_angle1 + PI - show_omega[i]
        arm_phase_angle3 = arm_phase_angle2 + PI + show_lambda1[i]
        arm_length1 = R_A/2
        arm_length2 = R_A/2
        arm_length3 = R_S*2 
        show_arm1_x[i], show_arm1_y[i] = func.func_general_xy(show_arm_x[i], show_arm_y[i], arm_phase_angle1, arm_length1)
        show_arm2_x[i], show_arm2_y[i] = func.func_general_xy(show_arm1_x[i], show_arm1_y[i], arm_phase_angle2, arm_length2)
        show_arm3_x[i], show_arm3_y[i] = func.func_general_xy(show_arm2_x[i], show_arm2_y[i], arm_phase_angle3, arm_length3)
        #print (show_arm3_x[i]-show_arm_x[i])**2+(show_arm3_y[i]-show_arm_y[i])**2, \
        #      (show_arm2_x[i]-show_arm_x[i])**2+(show_arm2_y[i]-show_arm_y[i])**2
        #------------------------------------------------------------------
        show_VC[i] = func.func_VC(show_alpha_dot[i], show_beta[i], show_beta_dot[i], show_R[i], L)
        show_VC_x[i], show_VC_y[i], show_VC_angle[i], show_VC_check[i]= \
        func.func_VC_xy(show_O_x[i], show_O_y[i], \
                        show_arm_x[i], show_arm_y[i], \
                        show_club_x[i], show_club_y[i], \
                        show_alpha_dot[i], \
                        show_beta[i], show_beta_dot[i], \
                        show_t[i], show_R[i], L)
        #------------------------------------------------------------------
        if (Method == 'Solution 3'):
            show_alpha[i+1], show_alpha_dot[i+1], show_alpha_ddot[i+1], \
            show_beta[i+1], show_beta_dot[i+1], show_beta_ddot[i+1]= \
            func.RK4_III(a_x, a_y, phi, I, S_C, M_C, \
                         show_J[i], show_S_A[i], show_R[i], \
                         show_Q_alpha[i], show_Q_beta[i], \
                         show_alpha[i] , show_alpha_dot[i] , show_alpha_ddot[i] , \
                         show_beta[i] , show_beta_dot[i] , \
                         show_theta[i])
        elif (Method == 'Solution 2'):
            show_alpha[i+1], show_alpha_dot[i+1], show_alpha_ddot[i+1], \
            show_beta[i+1], show_beta_dot[i+1], show_beta_ddot[i+1]= \
            func.RK4_II(a_x, a_y, phi, I, S_C, M_C, \
                        show_J[i], show_S_A[i], show_R[i], \
                        show_Q_alpha[i], show_Q_beta[i], \
                        show_alpha[i] , show_alpha_dot[i] , \
                        show_beta[i] , show_beta_dot[i] , show_beta_ddot[i], \
                        show_theta[i])
        else:
            show_alpha[i+1], show_alpha_dot[i+1], show_alpha_ddot[i+1], \
            show_beta[i+1], show_beta_dot[i+1], show_beta_ddot[i+1]= \
            func.RK4_I(a_x, a_y, phi, I, S_C, M_C, \
                       show_J[i], show_S_A[i], show_R[i], \
                       show_Q_alpha[i], show_Q_beta[i], \
                       show_alpha[i] , show_alpha_dot[i] , show_alpha_ddot[i] , \
                       show_beta[i] , show_beta_dot[i] , show_beta_ddot[i], \
                       show_theta[i])
        #------------------------------------------------------------------
        tmp_angle = show_theta[i]
        step = i
        #------------------------------------------------------------------
        show_t[i+1] = show_t[0] + h*i
        i = i+1
        #------------------------------------------------------------------
        print_beta     = show_beta[step]*180/PI
        print_VC_angle = show_VC_angle[step]*180.0/PI
        #------------------------------------------------------------------
    print '    Swing time:        ', ("%5.4f" % show_t[step]).strip(), '(sec)'
    print '    Clubhead velocity: ', ("%5.2f" % show_VC[step]).strip(), '(m/sec)'
    print '    Clubhead angle:    ', ("%5.2f" % print_VC_angle).strip(), '(degree)' 
    print '    Wrist-cock angle:  ', ("%5.2f" % print_beta).strip(), '(degree)'  
    print '--------------------------------------------'
    #
    # correct the length of array
    #
    step = step+1
    #
    # Input data for drawing rod and arm
    #
    for j in range(step):
        show_arm_rod_x[j*2]    = show_O_x[j]
        show_arm_rod_x[j*2+1]  = show_arm_x[j]
        show_arm_rod_y[j*2]    = show_O_y[j]
        show_arm_rod_y[j*2+1]  = show_arm_y[j]

        show_arm1_rod_x[j*2]    = show_arm_x[j]
        show_arm1_rod_x[j*2+1]  = show_arm1_x[j]
        show_arm1_rod_y[j*2]    = show_arm_y[j]
        show_arm1_rod_y[j*2+1]  = show_arm1_y[j]

        show_arm2_rod_x[j*2]    = show_arm1_x[j]
        show_arm2_rod_x[j*2+1]  = show_arm2_x[j]
        show_arm2_rod_y[j*2]    = show_arm1_y[j]
        show_arm2_rod_y[j*2+1]  = show_arm2_y[j]

        show_arm3_rod_x[j*2]    = show_arm2_x[j]
        show_arm3_rod_x[j*2+1]  = show_arm3_x[j]
        show_arm3_rod_y[j*2]    = show_arm2_y[j]
        show_arm3_rod_y[j*2+1]  = show_arm3_y[j]

        show_arm4_rod_x[j*2]    = show_arm3_x[j]
        show_arm4_rod_x[j*2+1]  = show_arm_x[j]
        show_arm4_rod_y[j*2]    = show_arm3_y[j]
        show_arm4_rod_y[j*2+1]  = show_arm_y[j]

        show_club_rod_x[j*2]   = show_arm_x[j]
        show_club_rod_x[j*2+1] = show_club_x[j]
        show_club_rod_y[j*2]   = show_arm_y[j]
        show_club_rod_y[j*2+1] = show_club_y[j]
    #
    # Return
    #
    return show_O_x[:step], show_O_y[:step], \
           show_arm_x[:step], show_arm_y[:step], \
           show_club_x[:step], show_club_y[:step], \
           show_arm_rod_x[:step*2], show_arm_rod_y[:step*2], \
           show_club_rod_x[:step*2], show_club_rod_y[:step*2], \
           show_t[:step], \
           show_alpha[:step], show_beta[:step], \
           show_theta[:step], show_VC_angle[:step], show_omega[:step], \
           show_alpha_dot[:step], show_beta_dot[:step], \
           show_alpha_ddot[:step], show_beta_ddot[:step], \
           show_VC[:step], \
           show_Q_alpha[:step], show_Q_beta[:step], \
           show_R[:step], show_J[:step], show_S_A[:step], \
           show_arm1_rod_x[:step*2], show_arm1_rod_y[:step*2], \
           show_arm2_rod_x[:step*2], show_arm2_rod_y[:step*2], \
           show_arm3_rod_x[:step*2], show_arm3_rod_y[:step*2], \
           show_arm4_rod_x[:step*2], show_arm4_rod_y[:step*2]

