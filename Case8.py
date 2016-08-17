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
from matplotlib import cm

#
# Set initial values
#
ball_mass    = 0.0458
ball_diameter= 0.0428
#COR          = 0.775
C_D          = 0.3
C_L          = 0.0
rho_air      = 1.2
v_wind       = 0.0
wind_theta   = 0.0
wind_phi     = 0.0
ball_v       = 45.0
#ball_theta   = 15.0
ball_phi     = 0.0
ball_w_theta = 0.0
ball_w_phi   = -90.0
Altitude     = 0.0

def Distance(set_C_D, set_C_L): 
    array_distance = []
    for i in range(0, 91, 1):
      set_ball_theta = 1.0*i
      show_x, show_y, show_z = \
      func.TRACK(ball_mass, ball_diameter, rho_air, set_C_D, set_C_L, \
                 ball_v, set_ball_theta, ball_phi, \
                 ball_w_theta, ball_w_phi, \
                 v_wind, wind_theta, wind_phi, \
                 Altitude)
      step = len(show_x)-1
      if (show_x[step] >= 0.0):
        distance = sqrt(show_x[step]**2 + show_y[step]**2)
      else:
        distance = -1.0*sqrt(show_x[step]**2 + show_y[step]**2)
      array_distance.append(distance)
      print set_ball_theta, set_C_D, set_C_L
    return array_distance

show_ball_theta = []

for j in range(0, 91, 1):
  set_ball_theta = j*1.0
  show_ball_theta.append(set_ball_theta)

#
# plot 
#
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 90)
ax.set_ylim(0, 180)
ax.set_xlabel('Launch elevation angle (degree)', fontsize=25, linespacing=1.0)
ax.set_ylabel('Flight distance (m)', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for k in range(1, 7, 1):
  set_C_D = 0.1*k
  set_C_L = 0.0
  show_distance = Distance(set_C_D, set_C_L)
  index = show_distance.index(max(show_distance))
  ax.text(show_ball_theta[index], max(show_distance)+2, r'$C_D = %s$'%(set_C_D), fontweight='bold', fontsize=15)
  ax.plot(show_ball_theta, show_distance, 'r-', markeredgecolor = 'none', linewidth=2)
#
plt.savefig('Case8-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 90)
ax.set_ylim(-50, 150)
ax.set_xlabel('Launch elevation angle (degree)', fontsize=25, linespacing=1.0)
ax.set_ylabel('Flight distance (m)', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for l in range(0, 4, 1):
  set_C_D = 0.3
  set_C_L = 0.1*l
  show_distance = Distance(set_C_D, set_C_L)
  index = show_distance.index(max(show_distance))
  ax.text(show_ball_theta[index], max(show_distance)+2, r'$C_L = %s$'%(set_C_L), fontweight='bold', fontsize=15)
  ax.plot(show_ball_theta, show_distance, 'r-', markeredgecolor = 'none', linewidth=2)
#
plt.savefig('Case8-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------

