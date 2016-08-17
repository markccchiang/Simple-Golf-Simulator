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
M_C_head   = 0.2 # mass of the club head (kg)
M_C_shaft  = 0.1 # mass of the club shaft (kg)
L_C_head   = 0.1 # club head length (m)
L_C_shaft  = 1.0 # club shaft length (m)
Q_alpha    = 100.0 # (N-m)
Q_beta     = -20.64 # (N-m)
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
#Method     = 'Solution 1'
Set_theta  = theta # (degree) 

#
# Tarcking Solution 1
#
print '>>>>> Tarcking Solution 1 <<<<<'
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
              theta_final, Type, Sex, 'Solution 1', \
              tau_Q_alpha, tau_Q_beta, Set_theta)

#
# Tarcking Solution 2
#
print '>>>>> Tarcking Solution 2 <<<<<'
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
              theta_final, Type, Sex, 'Solution 2', \
              tau_Q_alpha, tau_Q_beta, Set_theta)

#
# Tarcking Solution 3
#
print '>>>>> Tarcking Solution 3 <<<<<'
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
              theta_final, Type, Sex, 'Solution 3', \
              tau_Q_alpha, tau_Q_beta, Set_theta)

#
# get the length of arrays 
#
step = len(show_club_x)

#
# plot results
#
plt.figure(1)
plt.clf()
plt.xlabel('x (m)', fontsize=25)
plt.ylabel('y (m)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
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
plt.savefig('Case1-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(2)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Angle (degree)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
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
plt.savefig('Case1-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(3)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Anglular velocity (degree/sec)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:step], show_alpha_dot[:step]*180.0/PI, 'r-', \
         label=r"$\dot{\alpha}$", markersize=10, linewidth=5)
plt.plot(show_t[:step], show_beta_dot[:step]*180.0/PI, 'b-', \
         label=r"$\dot{\beta}$", markersize=10, linewidth=5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('Case1-Fig3.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(4)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Anglular acceleration (degree/sec$^2$)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:step], show_alpha_ddot[:step]*180.0/PI, 'r-', \
         label=r"$\ddot{\alpha}$", markersize=10, linewidth=5)
plt.plot(show_t[:step], show_beta_ddot[:step]*180.0/PI, 'b-', \
         label=r"$\ddot{\beta}$", markersize=10, linewidth=5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('Case1-Fig4.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(5)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Clubhead velocity (m/sec)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:step], show_VC[:step], 'k-', markersize=10, linewidth=5)
plt.savefig('Case1-Fig5.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(6)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Torque (N-m)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.ylim(min(-1*show_Q_beta)-10.0, max(show_Q_alpha)+10.0)
plt.plot(show_t[:step], show_Q_alpha[:step], 'r-', \
         label=r"$Q_\alpha$", markersize=10, linewidth=5)
plt.plot(show_t[:step], -1*show_Q_beta[:step], 'b-', \
         label=r"$-Q_\beta$", markersize=10, linewidth=5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('Case1-Fig6.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(7)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel(r'$J$ (kg-m$^2$)', color="b", fontsize=25)
plt.tick_params(axis="y", labelcolor="b")
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:step], show_J[:step], 'b-', markersize=10, linewidth=5)
plt.twinx()
plt.ylabel(r'$S_A$ (kg-m)', color="r", fontsize=25)
plt.tick_params(axis="y", labelcolor="r")
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:step], show_S_A[:step], 'r-', markersize=10, linewidth=5)
plt.savefig('Case1-Fig7.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------
plt.figure(8)
plt.clf()
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel(r'$R$ (m)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.tick_params(axis="y")
plt.plot(show_t[:step], show_R[:step], 'k-', markersize=10, linewidth=5)
plt.savefig('Case1-Fig8.eps', format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------

