#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

import numpy as np
from math import *
import matplotlib.pyplot as plt
import AppFunc2 as func
import BasicFunc as base

def initial(entries):
    #
    # Declare global values
    #
    global ball_mass, ball_diameter, COR, C_D, C_L, \
           rho_air, v_wind, wind_theta, wind_phi, \
           ball_U, ball_theta, ball_phi, \
           ball_w_theta, ball_w_phi, Altitude, \
           Figure1, Figure2, Figure3, Figure4
    #
    # Load global values from UI panel
    # 
    ball_mass    = float(entries['ball_mass'].get())
    ball_diameter= float(entries['ball_diameter'].get())
    COR          = float(entries['COR'].get())
    C_D          = float(entries['C_D'].get())
    C_L          = float(entries['C_L'].get())
    rho_air      = float(entries['rho_air'].get())
    v_wind       = float(entries['v_wind'].get())
    wind_theta   = float(entries['wind_theta'].get())
    wind_phi     = float(entries['wind_phi'].get())
    ball_U       = float(entries['ball_U'].get())
    ball_theta   = float(entries['ball_theta'].get())
    ball_phi     = float(entries['ball_phi'].get())
    ball_w_theta = float(entries['ball_w_theta'].get())
    ball_w_phi   = float(entries['ball_w_phi'].get())
    Altitude     = float(entries['Altitude'].get())
    Figure1      = str(entries['Figure1'].get())
    Figure2      = str(entries['Figure2'].get())
    Figure3      = str(entries['Figure3'].get())
    Figure4      = str(entries['Figure4'].get())

def Plot(entries):
    #
    # Set initial values
    #
    initial(entries)
    #
    # Tarcking
    #
    show_x, show_y, show_z = \
    func.TRACK(ball_mass, ball_diameter, rho_air, C_D, C_L, \
          ball_U, ball_theta, ball_phi, \
          ball_w_theta, ball_w_phi, \
          v_wind, wind_theta, wind_phi, \
          Altitude)
    #
    # get the length of arrays 
    #
    step = len(show_x)
    #
    # show results
    #
    print_x = ("%5.3f" % show_x[step-1]).strip()
    entries['X_final'].delete(0, END)
    entries['X_final'].config(fg = "red", bg = "cyan")
    entries['X_final'].insert(0, print_x)
    #
    print_y = ("%5.3f" % show_y[step-1]).strip()
    entries['Y_final'].delete(0, END)
    entries['Y_final'].config(fg = "red", bg = "cyan")
    entries['Y_final'].insert(0, print_y)
    #
    tmp_distance = sqrt(show_x[step-1]**2 + show_y[step-1]**2)
    if (show_x[step-1] >= 0.0):
        print_distance = ("%5.3f" % tmp_distance).strip()
    else: 
        print_distance = ("-%5.3f" % tmp_distance).strip()
    entries['Distance'].delete(0, END)
    entries['Distance'].config(fg = "red", bg = "cyan")
    entries['Distance'].insert(0, print_distance)
    #
    # plot results
    #
    plt.close('all')
    if (Figure1 == 'True'): 
      plt.figure(9)
      plt.clf()
      plt.xlabel('X (m)')
      plt.ylabel('Z (m)')
      plt.ylim(min(show_z), max(show_z)+1.0)
      plt.plot(show_x, show_z, 'k-', markersize=10, linewidth=5)
    #--------------------------------------------------
    if (Figure2 == 'True'): 
      plt.figure(10)
      plt.clf()
      plt.xlabel('X (m)')
      plt.ylabel('Y (m)')
      plt.ylim(min(show_y)-1.0, max(show_y)+1.0)
      plt.plot(show_x, show_y, 'k-', markersize=10, linewidth=5)
    #--------------------------------------------------
    if (Figure3 == 'True'): 
      plt.figure(11)
      plt.clf()
      plt.xlabel('Y (m)')
      plt.xlim(min(show_y)-1.0, max(show_y)+1.0)
      plt.ylabel('Z (m)')
      plt.ylim(min(show_z), max(show_z)+1.0)
      plt.plot(show_y, show_z, 'k-', markersize=10, linewidth=5)
    #--------------------------------------------------
    if (Figure4 == 'True'): 
      fig = plt.figure(12)
      fig.clf()
      ax = fig.gca(projection='3d')
      ax.set_zlim3d(min(show_z), max(show_z)+1.0)
      ax.set_ylim(min(show_y)-1.0, max(show_y)+1.0)
      ax.set_xlabel('\n' + 'X (m)', fontweight='bold', fontsize=22, linespacing=0.9)
      ax.set_ylabel('\n' + 'Y (m)', fontweight='bold', fontsize=22, linespacing=1.05)
      ax.set_zlabel('\n' + 'Z (m)', fontweight='bold', fontsize=22, linespacing=0.5)
      ax.plot(show_x, show_y, show_z, 'k-', markeredgecolor = 'none', linewidth=5)
    #--------------------------------------------------
    plt.show()

