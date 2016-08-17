from math import *
#import numpy as np
import cmath 

#
# Fixed parameters
#
h = 0.0001 # time interval for step-by-step calculation (sec)

#
# Physical parameters
#
g_vertical = 9.806 # (m/sec^2)

#
# Other parameters
#
PI       = 3.141592653589793
norm     = 270.0 # (degree)
nrom_rad = norm*PI/180.0 # (rad)

#
# sub-functions
#
def func_Q_alpha(t, tau, Set_Q_alpha):
    ans_Q_alpha = Set_Q_alpha*(1-exp(-1*t/tau))
    return ans_Q_alpha

def func_Q_beta(t, tau, Set_Q_beta, theta, Set_theta, t0):
    if (theta > Set_theta):
        ans_Q_beta = 0.0
    else:
        ans_Q_beta = Set_Q_beta*(1-exp(-1*(t-t0)/tau))
    return ans_Q_beta

def club_para(M_C_head, M_C_shaft, L_C_head, L_C_shaft):
    M_C = M_C_head + M_C_shaft
    L = L_C_head/2.0 + L_C_shaft
    L_eff = (M_C_head*(L_C_shaft + L_C_head/2.0) + M_C_shaft*L_C_shaft/2.0)/M_C
    S_C = M_C*L_eff
    I = M_C*L_eff**2
    return M_C, L, S_C, I

def func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, \
                    J, S_A, R, \
                    set_Q_alpha, \
                    alpha_dot_rad, \
                    beta_rad, beta_dot_rad, beta_ddot_rad, \
                    theta_rad):
    g = g_vertical*sin(phi*PI/180.0) - a_y
    alpha_part1 = J + I + M_C*R**2 + 2*R*S_C*cos(beta_rad)
    alpha_part2 = (I + R*S_C*cos(beta_rad))*beta_ddot_rad
    alpha_part3 = -1*(beta_dot_rad**2 - 2*alpha_dot_rad*beta_dot_rad)*R*S_C*sin(beta_rad)
    alpha_part4 = S_C*(g*sin(theta_rad+beta_rad) - a_x*cos(theta_rad+beta_rad))
    alpha_part5 = (S_A + M_C*R)*(g*sin(theta_rad) - a_x*cos(theta_rad))
    alpha_ddot_ans = (1/alpha_part1)*(set_Q_alpha + alpha_part2 + alpha_part3 + alpha_part4 + alpha_part5)
    return alpha_ddot_ans

def func_beta_ddot(a_x, a_y, phi, I, S_C, \
                   R, set_Q_beta, \
                   alpha_dot_rad, alpha_ddot_rad, \
                   beta_rad, \
                   theta_rad): 
    g = g_vertical*sin(phi*PI/180.0) - a_y
    beta_part1 = (I + R*S_C*cos(beta_rad))*alpha_ddot_rad
    beta_part2 = -1*alpha_dot_rad**2*R*S_C*sin(beta_rad)
    beta_part3 = -1*S_C*(g*sin(theta_rad+beta_rad) - a_x*cos(theta_rad+beta_rad))
    beta_ddot_ans = (1/I)*(set_Q_beta + beta_part1 + beta_part2 + beta_part3)
    return beta_ddot_ans

def func_VC(alpha_dot_rad, beta_rad, beta_dot_rad, R, L):
    VC_part1 = (R**2 + L**2 + 2*R*L*cos(beta_rad))*alpha_dot_rad**2
    VC_part2 = L**2*beta_dot_rad**2
    VC_part3 = -2*(L**2 + R*L*cos(beta_rad))*alpha_dot_rad*beta_dot_rad
    VC_sum = VC_part1 + VC_part2 + VC_part3
    if (VC_sum >= 0):
      return sqrt(VC_sum)
    else:
      return 'V_C value is not a real number!'

def func_general_xy(o_x, o_y, angle, length):
    ans_general_x = o_x + cos(angle)*length
    ans_general_y = o_y + sin(angle)*length 
    return ans_general_x, ans_general_y

def func_arm_xy(theta_rad, R):
    ans_arm_x = cos(nrom_rad-theta_rad)*R 
    ans_arm_y = sin(nrom_rad-theta_rad)*R 
    return ans_arm_x, ans_arm_y

def func_club_xy(theta_rad, beta_rad, R, L):
    ans_club_x = cos(nrom_rad-theta_rad)*R + cos(nrom_rad-theta_rad-beta_rad)*L 
    ans_club_y = sin(nrom_rad-theta_rad)*R + sin(nrom_rad-theta_rad-beta_rad)*L 
    return ans_club_x, ans_club_y

def func_O_xy(t):
    ans_O_x = 0.0 
    ans_O_y = 0.0  
    return ans_O_x, ans_O_y

def func_VC_xy(O_x, O_y, arm_x, arm_y, club_x, club_y, alpha_dot_rad, beta_rad, beta_dot_rad, t, R, L):
    vec_r_x = club_x - O_x
    vec_r_y = club_y - O_y 
    vec_r_x_bot = -1*(club_y - O_y)
    vec_r_y_bot = club_x - O_x
    vec_r_x_bot_hat = -1*(club_y - O_y)/sqrt(vec_r_x_bot**2+vec_r_y_bot**2)
    vec_r_y_bot_hat = (club_x - O_x)/sqrt(vec_r_x_bot**2+vec_r_y_bot**2)
    vec_L_x = club_x - arm_x
    vec_L_y = club_y - arm_y 
    vec_L_x_bot = -1*(club_y - arm_y)
    vec_L_y_bot = club_x - arm_x
    vec_L_x_bot_hat = -1*(club_y - arm_y)/sqrt(vec_L_x_bot**2+vec_L_y_bot**2)
    vec_L_y_bot_hat = (club_x - arm_x)/sqrt(vec_L_x_bot**2+vec_L_y_bot**2)
    r = sqrt(R**2 + L**2 + 2*R*L*cos(beta_rad))
    vec_VC_x = r*alpha_dot_rad*vec_r_x_bot_hat - L*beta_dot_rad*vec_L_x_bot_hat 
    vec_VC_y = r*alpha_dot_rad*vec_r_y_bot_hat - L*beta_dot_rad*vec_L_y_bot_hat 
    vec_VC_check = sqrt(vec_VC_x**2 + vec_VC_y**2)
    vec_VC_angle_rad_tmp = cmath.phase(complex(vec_VC_x, vec_VC_y))
    if (PI/2 <= vec_VC_angle_rad_tmp <= PI):
        vec_VC_angle_rad = vec_VC_angle_rad_tmp - 2*PI
    else:
         vec_VC_angle_rad = vec_VC_angle_rad_tmp
    return vec_VC_x, vec_VC_y, vec_VC_angle_rad, vec_VC_check

def RK4_I(a_x, a_y, phi, I, S_C, M_C, \
          J, S_A, R, \
          set_Q_alpha, set_Q_beta, \
          alpha_rad, alpha_dot_rad, alpha_ddot_rad, \
          beta_rad,  beta_dot_rad,  beta_ddot_rad, \
          theta_rad):
    #----------------------------------------------------------------------------------------------------------------
    k1 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad, beta_rad, beta_dot_rad, beta_ddot_rad, theta_rad)
    q1 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad, alpha_ddot_rad, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k2 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k1*h, beta_rad, beta_dot_rad + (1/2)*q1*h, beta_ddot_rad, theta_rad)
    q2 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k1*h, alpha_ddot_rad, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k3 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k2*h, beta_rad, beta_dot_rad + (1/2)*q2*h, beta_ddot_rad, theta_rad)
    q3 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k2*h, alpha_ddot_rad, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k4 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + k3*h, beta_rad, beta_dot_rad + q3*h, beta_ddot_rad, theta_rad)
    q4 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + k3*h, alpha_ddot_rad, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    alpha_dot_rad_n1 = alpha_dot_rad + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    beta_dot_rad_n1 = beta_dot_rad + (h/6)*(q1 + 2*q2 + 2*q3 + q4)
    #----------------------------------------------------------------------------------------------------------------
    alpha_rad_n1 = alpha_rad +  alpha_dot_rad_n1*h
    beta_rad_n1 = beta_rad + beta_dot_rad_n1*h
    #----------------------------------------------------------------------------------------------------------------
    return alpha_rad_n1, alpha_dot_rad_n1, k1, beta_rad_n1, beta_dot_rad_n1, q1

def RK4_II(a_x, a_y, phi, I, S_C, M_C, \
           J, S_A, R, \
           set_Q_alpha, set_Q_beta, \
           alpha_rad, alpha_dot_rad, \
           beta_rad,  beta_dot_rad, beta_ddot_rad, \
           theta_rad):
    #----------------------------------------------------------------------------------------------------------------
    k1 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad, beta_rad, beta_dot_rad, beta_ddot_rad, theta_rad)
    q1 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad, k1, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k2 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k1*h, beta_rad, beta_dot_rad + (1/2)*q1*h, q1, theta_rad)
    q2 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k1*h, k2, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k3 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k2*h, beta_rad, beta_dot_rad + (1/2)*q2*h, q2, theta_rad)
    q3 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k2*h, k3, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    k4 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + k3*h, beta_rad, beta_dot_rad + q3*h, q3, theta_rad)
    q4 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + k3*h, k4, beta_rad, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    alpha_dot_rad_n1 = alpha_dot_rad + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    beta_dot_rad_n1 = beta_dot_rad + (h/6)*(q1 + 2*q2 + 2*q3 + q4)
    #----------------------------------------------------------------------------------------------------------------
    alpha_rad_n1 = alpha_rad +  alpha_dot_rad_n1*h
    beta_rad_n1 = beta_rad + beta_dot_rad_n1*h
    #----------------------------------------------------------------------------------------------------------------
    return alpha_rad_n1, alpha_dot_rad_n1, k1, beta_rad_n1, beta_dot_rad_n1, q1

def RK4_III(a_x, a_y, phi, I, S_C, M_C, \
            J, S_A, R, \
            set_Q_alpha, set_Q_beta, \
            alpha_rad, alpha_dot_rad, alpha_ddot_rad, \
            beta_rad,  beta_dot_rad, \
            theta_rad):
    #----------------------------------------------------------------------------------------------------------------
    q1 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad, alpha_ddot_rad, beta_rad, theta_rad)
    k1 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad, beta_rad, beta_dot_rad, q1, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    q2 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k1*h, k1, beta_rad, theta_rad)
    k2 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k1*h, beta_rad, beta_dot_rad + (1/2)*q1*h, q2, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    q3 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + (1/2)*k2*h, k2, beta_rad, theta_rad)
    k3 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + (1/2)*k2*h, beta_rad, beta_dot_rad + (1/2)*q2*h, q3, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    q4 = func_beta_ddot(a_x, a_y, phi, I, S_C, R, set_Q_beta, alpha_dot_rad + k3*h, k3, beta_rad, theta_rad)
    k4 = func_alpha_ddot(a_x, a_y, phi, I, S_C, M_C, J, S_A, R, set_Q_alpha, alpha_dot_rad + k3*h, beta_rad, beta_dot_rad + q3*h, q4, theta_rad)
    #----------------------------------------------------------------------------------------------------------------
    alpha_dot_rad_n1 = alpha_dot_rad + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    beta_dot_rad_n1 = beta_dot_rad + (h/6)*(q1 + 2*q2 + 2*q3 + q4)
    #----------------------------------------------------------------------------------------------------------------
    alpha_rad_n1 = alpha_rad +  alpha_dot_rad_n1*h
    beta_rad_n1 = beta_rad + beta_dot_rad_n1*h
    #----------------------------------------------------------------------------------------------------------------
    return alpha_rad_n1, alpha_dot_rad_n1, k1, beta_rad_n1, beta_dot_rad_n1, q1

def Ball_velocity(V_head, M_head, M_ball, COR):
    ans_Ball_velocity = V_head*(1+COR)*M_head/(M_ball+M_head)
    return ans_Ball_velocity 

def inner_angle_TypeI(R_S, R_A):
    inner_angle_TypeI_ans = acos(R_S/R_A)
    return inner_angle_TypeI_ans

def arm_length_TypeI(R_S, R_A):
    arm_length_TypeI_ans = sqrt(R_A**2-R_S**2)
    return arm_length_TypeI_ans

def Integrate1(R_S, inner_angle_original, r_A):
    inner_angle = abs(inner_angle_original)
    Integrate1_ans = (R_S**2)*r_A + (r_A**3)/3 - R_S*(r_A**2)*cos(inner_angle)
    return Integrate1_ans

def Integrate2(R_S, inner_angle_original, r_A):
    inner_angle = abs(inner_angle_original)
    Integrate2_part1 = (r_A-R_S*cos(inner_angle))/(R_S*sin(inner_angle))
    Integrate2_part2 = sqrt(R_S**2+r_A**2-2*R_S*r_A*cos(inner_angle))
    #Integrate2_part3 = (R_S**2)*(sin(inner_angle)**2)*np.arcsinh(Integrate2_part1)
    Integrate2_part3 = (R_S**2)*(sin(inner_angle)**2)*asinh(Integrate2_part1)
    Integrate2_part4 = (r_A-R_S*cos(inner_angle))*Integrate2_part2
    Integrate2_ans = Integrate2_part3 + Integrate2_part4
    return Integrate2_ans

def J_TypeI(R_S, R_A, rho_S, rho_A1, rho_A2, inner_angle):
    J_TypeI_part1 = 2*rho_A1*Integrate1(R_S, inner_angle, R_A/2) - 0.0
    J_TypeI_part2 = 2*rho_A2*Integrate1(R_S, inner_angle, R_A) - 2*rho_A2*Integrate1(R_S, inner_angle, R_A/2)
    J_TypeI_part3 = 2*rho_S*(R_S**3)/3
    J_TypeI_ans = J_TypeI_part1 + J_TypeI_part2 + J_TypeI_part3 
    return J_TypeI_ans

def S_A_TypeI(R_S, R_A, rho_S, rho_A1, rho_A2, inner_angle):
    S_A_TypeI_part1 = rho_A1*(Integrate2(R_S, inner_angle, R_A/2)-Integrate2(R_S, inner_angle, 0.0))
    S_A_TypeI_part2 = rho_A2*(Integrate2(R_S, inner_angle, R_A)-Integrate2(R_S, inner_angle, R_A/2))
    S_A_TypeI_part3 = rho_S*R_S**2 - 0.0
    S_A_TypeI_ans = S_A_TypeI_part1 + S_A_TypeI_part2 + S_A_TypeI_part3
    return S_A_TypeI_ans

def bending_arm_para(R_S, R_A, bending_angle):
    R_Ap = R_A*sin(bending_angle/2)
    mu = PI/2 - bending_angle/2
    delta_part1 = (R_Ap**2 - R_A**2 - (2*R_S)**2)/(-2*(2*R_S)*R_A)
    delta = acos(delta_part1)
    lambda1_part1 = (R_A**2 - R_Ap**2 - (2*R_S)**2)/(-2*(2*R_S)*R_Ap)
    lambda1 = acos(lambda1_part1) - mu
    R_eff = sqrt(R_A**2 + R_S**2 - 2*R_A*R_S*cos(delta))
    epsilon_part1 = (R_S**2 - R_Ap**2 - R_eff**2)/(-2*R_Ap*R_eff)
    epsilon = acos(epsilon_part1)
    sigma = mu - epsilon
    return R_eff, delta, lambda1, sigma

def bending_arm_angle_min(R_S, R_A):
    L1 = (R_A-2*R_S)/2
    L2 = R_A/2
    bending_arm_angle_min_ans_tmp = 2*asin(L1/L2)
    if (bending_arm_angle_min_ans_tmp < PI/2):
        bending_arm_angle_min_ans = PI/2
    else:
        bending_arm_angle_min_ans = bending_arm_angle_min_ans_tmp
    return bending_arm_angle_min_ans

def bending_arm_angle(theta_ini, alpha, omega_ini):
    bending_arm_angle_ans = omega_ini + (alpha/theta_ini)*(PI-omega_ini)
    if (bending_arm_angle_ans <= PI):
      return bending_arm_angle_ans
    else:
      return PI

def J_TypeII(R_S, R_A, rho_S, rho_A1, rho_A2, R_eff, inner_angle1, inner_angle2, inner_angle3):
    J_TypeII_part1 = rho_A1*Integrate1(R_S, inner_angle1, R_A/2) - 0.0
    J_TypeII_part2 = rho_A2*Integrate1(R_S, inner_angle1, R_A) - rho_A2*Integrate1(R_S, inner_angle1, R_A/2)
    J_TypeII_part3 = rho_A1*Integrate1(R_S, inner_angle2, R_A/2) - 0.0
    J_TypeII_part4 = rho_A2*Integrate1(R_eff, inner_angle3, R_A/2) - 0.0
    J_TypeII_part5 = 2*rho_S*(R_S**3)/3
    J_TypeII_ans = J_TypeII_part1 + J_TypeII_part2 + J_TypeII_part3 + J_TypeII_part4 + J_TypeII_part5
    return J_TypeII_ans

def S_A_TypeII(R_S, R_A, rho_S, rho_A1, rho_A2, R_eff, inner_angle1, inner_angle2, inner_angle3):
    S_A_TypeII_part1 = (rho_A1/2)*(Integrate2(R_S, inner_angle1, R_A/2)-Integrate2(R_S, inner_angle1, 0.0))
    S_A_TypeII_part2 = (rho_A2/2)*(Integrate2(R_S, inner_angle1, R_A)-Integrate2(R_S, inner_angle1, R_A/2))
    S_A_TypeII_part3 = (rho_A1/2)*(Integrate2(R_S, inner_angle2, R_A/2)-Integrate2(R_S, inner_angle2, 0.0))
    S_A_TypeII_part4 = (rho_A2/2)*(Integrate2(R_eff, inner_angle3, R_A/2)-Integrate2(R_eff, inner_angle3, 0.0))
    S_A_TypeII_part5 = rho_S*R_S**2 - 0.0
    S_A_TypeII_ans = S_A_TypeII_part1 + S_A_TypeII_part2 + S_A_TypeII_part3 + S_A_TypeII_part4 + S_A_TypeII_part5
    return S_A_TypeII_ans

