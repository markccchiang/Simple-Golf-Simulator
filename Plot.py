#!/usr/bin/env python
from tkinter import *

import matplotlib.pyplot as plt
import AppFunc as func
import BasicFunc as base
import UIFunc as ui

PI = 3.141592653589793

SWING_HINT = ('Items 26 and 28 (clubhead impact velocity and angle) are not set yet. '
              'Click "Simulate / Plot Golf Swing" first.')

def _check_swing_geometry(R_S, R_A):
    """Reject shoulder/arm dimensions the two-rod model cannot represent."""
    if not 0.0 < R_S < R_A:
        raise ui.UserFacingError(
            "The shoulder radius (item 3) must be greater than 0 and smaller "
            "than the arm length (item 4).")

def _set_entry(entry, value):
    """Update a ttk Entry field (handles readonly state)."""
    try:
        entry.state(['!readonly'])
    except AttributeError:
        pass
    entry.delete(0, END)
    entry.insert(0, value)
    try:
        entry.state(['readonly'])
    except AttributeError:
        pass

@ui.validate_inputs
def get_ball_velocity(entries):
    #
    # Calculate ball velocity
    #
    tmp_M_C_head = ui.get_float(entries, 'M_C_head') # mass of the club head (kg)
    ball_mass    = ui.get_float(entries, 'ball_mass') # (degree) 
    COR          = ui.get_float(entries, 'COR') # (degree) 
    VC           = ui.require_result(entries, 'VC', SWING_HINT)
    ans_ball_velocity = base.Ball_velocity(VC, tmp_M_C_head, ball_mass, COR)
    tmp_ans_ball_velocity = ("%5.2f" % ans_ball_velocity).strip()
    _set_entry(entries['ball_U'], tmp_ans_ball_velocity)
    #
    # Calculate the elevation angle of ball
    #
    tmp_theta_final   = ui.get_float(entries, 'theta_final') # (degree) 
    tmp_beta_final    = ui.get_float(entries, 'beta_final') # (degree) 
    tmp_VC_angle      = ui.require_result(entries, 'VC_angle', SWING_HINT) # (degree)
    tmp_clubhead_loft = ui.get_float(entries, 'clubhead_loft') # (degree) 
    tmp_ans_elevation = tmp_theta_final + tmp_beta_final + tmp_clubhead_loft + tmp_VC_angle
    tmp2_ans_elevation= ("%5.2f" % tmp_ans_elevation).strip()
    _set_entry(entries['ball_theta'], tmp2_ans_elevation)

def _read_swing_params(entries):
    """Read swing parameters from UI entries."""
    Sex        = str(entries['Gender'].get())
    Weight     = ui.get_float(entries, 'Weight')
    R_S        = ui.get_float(entries, 'R_S')
    R_A        = ui.get_float(entries, 'R_A')
    _check_swing_geometry(R_S, R_A)
    M_C_head   = ui.get_float(entries, 'M_C_head')
    M_C_shaft  = ui.get_float(entries, 'M_C_shaft')
    L_C_head   = ui.get_float(entries, 'L_C_head')
    L_C_shaft  = ui.get_float(entries, 'L_C_shaft')
    phi        = ui.get_float(entries, 'phi')
    theta      = ui.get_float(entries, 'theta')
    theta_final= ui.get_float(entries, 'theta_final')
    beta       = ui.get_float(entries, 'beta')
    beta_final = ui.get_float(entries, 'beta_final')
    a_x        = ui.get_float(entries, 'a_x')
    a_y        = ui.get_float(entries, 'a_y')
    Type       = str(entries['Type'].get())
    Q_alpha    = ui.get_float(entries, 'Q_alpha')
    tau_Q_alpha= ui.get_float(entries, 'tau_Q_alpha')
    Set_theta  = ui.get_float(entries, 'set_theta')
    tau_Q_beta = ui.get_float(entries, 'tau_Q_beta')
    Q_beta_min = ui.get_float(entries, 'Q_beta_min')
    Q_beta_max = ui.get_float(entries, 'Q_beta_max')
    if (Q_beta_min > Q_beta_max):
        raise ui.UserFacingError("The minimum wrist-cock torque (item 22) must not be greater than "
                                 "the maximum (item 23).")
    Method     = str(entries['Method'].get())
    return dict(
        Sex=Sex, Weight=Weight, R_S=R_S, R_A=R_A,
        M_C_head=M_C_head, M_C_shaft=M_C_shaft,
        L_C_head=L_C_head, L_C_shaft=L_C_shaft,
        phi=phi, theta=theta, theta_final=theta_final,
        beta=beta, beta_final=beta_final, a_x=a_x, a_y=a_y,
        Type=Type, Q_alpha=Q_alpha, tau_Q_alpha=tau_Q_alpha,
        Set_theta=Set_theta, tau_Q_beta=tau_Q_beta,
        Q_beta_min=Q_beta_min, Q_beta_max=Q_beta_max, Method=Method)

def _run_tracking(p, set_Q_beta):
    """Run a single tracking simulation and return the final beta angle (degrees)."""
    result = func.Tracking(
        p['Weight'], p['R_S'], p['R_A'],
        p['M_C_head'], p['M_C_shaft'], p['L_C_head'], p['L_C_shaft'],
        p['a_x'], p['a_y'], 0.0,
        p['Q_alpha'], set_Q_beta, p['phi'], p['theta'],
        0.0, 0.0, 0.0,
        p['beta'], 0.0, 0.0,
        p['theta_final'], p['Type'], p['Sex'], p['Method'],
        p['tau_Q_alpha'], p['tau_Q_beta'], p['Set_theta'])
    show_beta = result[12]
    return show_beta[len(show_beta)-1] * 180.0 / PI, result

def _best_Q_beta(array_Q_beta, array_beta, beta_final, Q_beta_min, Q_beta_max):
    """Pick the tried wrist-cock torque (within its allowed range) whose impact wrist-cock angle is closest to the target."""
    tried = [(-q, b) for q, b in zip(array_Q_beta, array_beta) if Q_beta_min <= -q <= Q_beta_max]
    if not any(b <= beta_final for _, b in tried):
        q, b = min(tried, key=lambda s: s[0])
        raise ui.UserFacingError(
            "No wrist-cock torque in the allowed range reaches the target. At %.2f N-m, the lowest torque tried, "
            "the wrist-cock angle is still %.2f degree at impact, above the target of %.2f degree (item 13). "
            "Lower the minimum wrist-cock torque (item 22)." % (q, b, beta_final))
    if not any(b >= beta_final for _, b in tried):
        q, b = max(tried, key=lambda s: s[0])
        raise ui.UserFacingError(
            "No wrist-cock torque in the allowed range reaches the target. At %.2f N-m, the highest torque tried, "
            "the wrist-cock angle is already %.2f degree at impact, below the target of %.2f degree (item 13). "
            "Raise the maximum wrist-cock torque (item 23)." % (q, b, beta_final))
    return min(tried, key=lambda s: abs(s[1] - beta_final))[0]

def _plot_optimization(entries, array_Q_beta, array_beta, k, beta_final, Q_beta_min, Q_beta_max):
    """Display optimization results and plot."""
    _set_entry(entries['Q_beta'], 'N/A') # stays N/A if no torque in the range reaches the target
    best_Q_beta = _best_Q_beta(array_Q_beta, array_beta, beta_final, Q_beta_min, Q_beta_max)
    _set_entry(entries['Q_beta'], ("%5.2f" % best_Q_beta).strip())
    #
    array_dQ_beta = []
    array_Q_beta2 = []
    for j in range(1, len(array_Q_beta)):
        tmp_dQ_beta = array_Q_beta[j] - array_Q_beta[j-1]
        tmp_dbeta = array_beta[j] - array_beta[j-1]
        array_dQ_beta.append(tmp_dbeta/tmp_dQ_beta)
        array_Q_beta2.append(array_Q_beta[j])
    #
    plt.close('all')
    plt.figure(0)
    plt.clf()
    #
    plt.subplot(2, 1, 1)
    plt.grid(True)
    plt.ylabel(r'$\beta$ (degree)')
    # The refinement restarts at the second-to-last coarse point, so the last coarse point is left out
    # to keep the coarse line from overlapping the refined one
    plt.plot(array_Q_beta[:k-1], array_beta[:k-1], 'r.-', markersize=10, linewidth=1)
    plt.plot(array_Q_beta[k:], array_beta[k:], 'r.-', markersize=10, linewidth=1)
    #
    plt.subplot(2, 1, 2)
    plt.grid(True)
    plt.xlabel(r'$-Q_\beta$ (N-m)')
    plt.ylabel(r'$-d\beta/dQ_\beta$ (degree/N-m)')
    plt.plot(array_Q_beta2, array_dQ_beta, 'r.', markersize=10, linewidth=1)
    plt.show()

@ui.validate_inputs
def Optimize_Q_beta(entries):
    p = _read_swing_params(entries)
    beta_final = p['beta_final']
    Q_beta_min = p['Q_beta_min']
    Q_beta_max = p['Q_beta_max']
    dQ_beta = 1.0
    #
    # Step 1: coarse search
    #
    array_Q_beta = []
    array_beta = []
    i = 0
    k = 0
    tmp_beta = 180.0
    set_Q_beta = Q_beta_max
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max - i*dQ_beta
        print('>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<')
        tmp_beta, _ = _run_tracking(p, set_Q_beta)
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1
        k = i
    #
    # Step 2: medium refinement
    #
    i = 0
    tmp_beta = 180.0
    Q_beta_max1 = set_Q_beta + dQ_beta
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max1 - i*dQ_beta/10
        print('>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<')
        tmp_beta, _ = _run_tracking(p, set_Q_beta)
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1
    #
    # Step 3: fine refinement
    #
    i = 0
    tmp_beta = 180.0
    Q_beta_max2 = set_Q_beta + dQ_beta/10
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max2 - i*dQ_beta/100
        print('>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<')
        tmp_beta, _ = _run_tracking(p, set_Q_beta)
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1
    #
    _plot_optimization(entries, array_Q_beta, array_beta, k, beta_final, Q_beta_min, Q_beta_max)

@ui.validate_inputs
def Optimize_Q_beta_2(entries):
    p = _read_swing_params(entries)
    beta_final = p['beta_final']
    Q_beta_min = p['Q_beta_min']
    Q_beta_max = p['Q_beta_max']
    dQ_beta = 1.0
    #
    # Step 1: coarse search
    #
    array_Q_beta = []
    array_beta = []
    i = 0
    k = 0
    tmp_beta = 180.0
    set_Q_beta = Q_beta_max
    while (tmp_beta > beta_final and set_Q_beta >= Q_beta_min):
        set_Q_beta = Q_beta_max - i*dQ_beta
        print('>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<')
        tmp_beta, _ = _run_tracking(p, set_Q_beta)
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
        i = i+1
        k = i
    #
    # Step 2: complete search with variable step size
    #
    tmp_beta = 180.0
    Q_beta_max1 = set_Q_beta + dQ_beta
    for i in range(111):
        if (i<=100):
            set_Q_beta = Q_beta_max1 - i*dQ_beta/100
        else:
            set_Q_beta = Q_beta_max1 - (i+1-100)*dQ_beta
        print('>>>>> Try wrist-cock torque:', set_Q_beta, '(N-m) <<<<<')
        tmp_beta, _ = _run_tracking(p, set_Q_beta)
        array_Q_beta.append(-1*set_Q_beta)
        array_beta.append(tmp_beta)
    #
    _plot_optimization(entries, array_Q_beta, array_beta, k, beta_final, Q_beta_min, Q_beta_max)

@ui.validate_inputs
def Plot(entries):
    #
    # Set initial values
    #
    Sex        = str(entries['Gender'].get())
    Weight     = ui.get_float(entries, 'Weight') # golfer's weight (kg)
    R_S        = ui.get_float(entries, 'R_S') # shoulder length (m)
    R_A        = ui.get_float(entries, 'R_A') # arm length (m)
    _check_swing_geometry(R_S, R_A)
    M_C_head   = ui.get_float(entries, 'M_C_head') # mass of the club head (kg)
    M_C_shaft  = ui.get_float(entries, 'M_C_shaft') # mass of the club shaft (kg)
    L_C_head   = ui.get_float(entries, 'L_C_head') # club head length (m)
    L_C_shaft  = ui.get_float(entries, 'L_C_shaft') # club shaft length (m)
    phi        = ui.get_float(entries, 'phi') # swing plane angle (degree)
    theta      = ui.get_float(entries, 'theta') # (degree) 
    theta_final= ui.get_float(entries, 'theta_final') # (degree) 
    beta       = ui.get_float(entries, 'beta') # (degree) 
    beta_final = ui.get_float(entries, 'beta_final') # (degree) 
    a_x        = ui.get_float(entries, 'a_x') # arm acceleration in horizontal direction (m/sec^2)
    a_y        = ui.get_float(entries, 'a_y') # arm acceleration in vertical direction (m/sec^2)
    Type       = str(entries['Type'].get())
    Q_alpha    = ui.get_float(entries, 'Q_alpha') # (N-m)
    tau_Q_alpha= ui.get_float(entries, 'tau_Q_alpha') # (sec)
    Q_beta     = ui.require_result(entries, 'Q_beta',
                                   'Item 19 (wrist-cock torque) is not set yet. '
                                   'Click "Optimize wrist-cock torque" first.') # (N-m)
    Set_theta  = ui.get_float(entries, 'set_theta') # (degree) 
    tau_Q_beta = ui.get_float(entries, 'tau_Q_beta') # (sec)
    Q_beta_min = ui.get_float(entries, 'Q_beta_min') # (N-m)
    Q_beta_max = ui.get_float(entries, 'Q_beta_max') # (N-m)
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
    print('>>>>> For Wrist-cock torque:', Q_beta+0.01, '(N-m) <<<<<')
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
    print('>>>>> For Wrist-cock torque:', Q_beta, '(N-m) <<<<<')
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
    print('>>>>> For Wrist-cock torque:', Q_beta-0.01, '(N-m) <<<<<')
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
    _set_entry(entries['VC'], print_VC)
    #
    print_VC_angle = show_VC_angle[step-1]*180.0/PI
    print1_VC_angle = show1_VC_angle[step1-1]*180.0/PI
    print2_VC_angle = show2_VC_angle[step2-1]*180.0/PI
    print_VC_angle = ("%5.2f" % print_VC_angle).strip()
    print1_VC_angle = ("%5.2f" % print1_VC_angle).strip()
    print2_VC_angle = ("%5.2f" % print2_VC_angle).strip()
    _set_entry(entries['VC_angle'], print_VC_angle)
    #
    #
    error1_VC = float(print1_VC) - float(print_VC)
    error2_VC = float(print2_VC) - float(print_VC)
    print_error_VC = '['+("%5.2f" % error1_VC).strip()+', '+("%5.2f" % error2_VC).strip()+']'
    _set_entry(entries['error_VC'], print_error_VC)
    #
    error1_VC_angle = float(print1_VC_angle) - float(print_VC_angle)
    error2_VC_angle = float(print2_VC_angle) - float(print_VC_angle)
    print_error_VC_angle = '['+("%5.2f" % error1_VC_angle).strip()+', '+("%5.2f" % error2_VC_angle).strip()+']'
    _set_entry(entries['error_VC_angle'], print_error_VC_angle)

    #
    # plot results
    #
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
      plt.legend(loc='best')
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
      plt.legend(loc='best')
    #--------------------------------------------------
    if (Fig3 == 'True'): 
      plt.figure(3)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Angular velocity (degree/sec)')
      plt.plot(show_t[:step], show_alpha_dot[:step]*180.0/PI, 'r-', \
               label=r"$\dot{\alpha}$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_beta_dot[:step]*180.0/PI, 'b-', \
               label=r"$\dot{\beta}$", markersize=10, linewidth=5)
      plt.legend(loc='best')
    #--------------------------------------------------
    if (Fig4 == 'True'): 
      plt.figure(4)
      plt.clf()
      plt.xlabel('Time (sec)')
      plt.ylabel('Angular acceleration (degree/sec$^2$)')
      plt.plot(show_t[:step], show_alpha_ddot[:step]*180.0/PI, 'r-', \
               label=r"$\ddot{\alpha}$", markersize=10, linewidth=5)
      plt.plot(show_t[:step], show_beta_ddot[:step]*180.0/PI, 'b-', \
               label=r"$\ddot{\beta}$", markersize=10, linewidth=5)
      plt.legend(loc='best')
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
      plt.legend(loc='best')
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

