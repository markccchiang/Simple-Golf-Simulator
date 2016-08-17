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
ball_theta   = 15.0
ball_phi     = 0.0
ball_w_theta = 0.0
ball_w_phi   = -90.0
Altitude     = 0.0

#
# plot 
#
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 100)
ax.set_ylim(0, 7)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('z (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
for i in range(1, 7, 1):
    set_C_D = i*0.1
    print set_C_D
    show_x, show_y, show_z = \
    func.TRACK(ball_mass, ball_diameter, rho_air, set_C_D, C_L, \
               ball_v, ball_theta, ball_phi, \
               ball_w_theta, ball_w_phi, \
               v_wind, wind_theta, wind_phi, \
               Altitude)
    step = len(show_x)-1
    index=np.argmax(show_z)
    ax.text(show_x[index], max(show_z)+0.05, \
            r'$C_D = %s$'%(set_C_D), fontweight='bold', fontsize=15)
    ax.plot(show_x, show_z, 'r-', markeredgecolor = 'none', linewidth=2)
plt.savefig('Case7-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 140)
ax.set_ylim(0, 18)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('z (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
for i in range(0, 4, 1):
    set_C_L = i*0.1
    print set_C_L
    show_x, show_y, show_z = \
    func.TRACK(ball_mass, ball_diameter, rho_air, C_D, set_C_L, \
               ball_v, ball_theta, ball_phi, \
               ball_w_theta, ball_w_phi, \
               v_wind, wind_theta, wind_phi, \
               Altitude)
    step = len(show_x)-1
    index=np.argmax(show_z)
    ax.text(show_x[index], max(show_z)+0.3, \
            r'$C_L = %s$'%(set_C_L), fontweight='bold', fontsize=15)
    ax.plot(show_x, show_z, 'r-', markeredgecolor = 'none', linewidth=2)
plt.savefig('Case7-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
array_set_C_D = []
array_set_C_L = []
array_distance = []
set_grid_sections = 50
for i in range(0, set_grid_sections*2+1, 1):
  for j in range(0, set_grid_sections*2+1, 1):
     set_C_D = 0.1 + i*0.5/(set_grid_sections*2)
     set_C_L = 0.0 + j*0.3/(set_grid_sections*2)
     print set_C_D, set_C_L
     show_x, show_y, show_z = \
     func.TRACK(ball_mass, ball_diameter, rho_air, set_C_D, set_C_L, \
                ball_v, ball_theta, ball_phi, \
                ball_w_theta, ball_w_phi, \
                v_wind, wind_theta, wind_phi, \
                Altitude)
     step = len(show_x)-1
     distance = show_x[step]
     array_set_C_D.append(set_C_D)
     array_set_C_L.append(set_C_L)
     array_distance.append(distance)
plt.figure(3)
ax = fig.add_subplot(111)
plt.xlabel(r'$C_D$', fontweight='bold', fontsize=25)
plt.ylabel(r'$C_L$', fontweight='bold', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.hexbin(array_set_C_D, array_set_C_L, C=array_distance, gridsize=set_grid_sections, cmap=cm.jet, bins=None)
plt.axis([min(array_set_C_D), max(array_set_C_D), min(array_set_C_L), max(array_set_C_L)])
#cb = plt.colorbar(image,spacing='uniform',extend='max')
cb = plt.colorbar()
cb.set_label('Flight distance (m)', fontsize=25)
cb.ax.tick_params(labelsize=15) 
plt.savefig('Case7-Fig3.eps', format='eps', dpi=1000, bbox_inches='tight')

