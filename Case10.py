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
C_D          = 0.285
C_L          = 0.1
rho_air      = 1.2
v_wind       = 5.0
wind_theta   = 0.0
#wind_phi     = 0.0
ball_v       = 45.0
ball_theta   = 15.0
ball_phi     = 0.0
#ball_w_theta = 0.0
ball_w_phi   = -90.0
Altitude     = 0.0

def Drop_location(set_ball_w_theta, set_wind_phi): 
    show_x, show_y, show_z = \
    func.TRACK(ball_mass, ball_diameter, rho_air, C_D, C_L, \
               ball_v, ball_theta, ball_phi, \
               set_ball_w_theta, ball_w_phi, \
               v_wind, wind_theta, set_wind_phi, \
               Altitude)
    step = len(show_x)-1
    return show_x, show_y, step

#
# plot 
#
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 120)
ax.set_ylim(-10, 10)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('y (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for k in range(0, 181, 1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 0.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
for k in range(359, 180, -1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 0.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
ax.annotate('',xytext=(10, 4),xy=(30, 4),arrowprops=dict(facecolor='black', shrink=0.05)) # i=1
ax.text(5, 7, r'Wind speed: 5 (m/sec)', fontsize=15)
ax.text(5, 6, r'Wind direction: $\phi_{\rm{wind}}=0^\circ$', fontsize=15)
#
plt.savefig('Case10-Fig1.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 120)
ax.set_ylim(-10, 10)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('y (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for k in range(0, 181, 1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 90.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
for k in range(359, 180, -1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 90.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
ax.annotate('',xytext=(20, 2.5),xy=(20, 5.5),arrowprops=dict(facecolor='black', shrink=0.05)) # j=1
ax.text(5, 7, r'Wind speed: 5 (m/sec)', fontsize=15)
ax.text(5, 6, r'Wind direction: $\phi_{\rm{wind}}=90^\circ$', fontsize=15)
#
plt.savefig('Case10-Fig2.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 120)
ax.set_ylim(-10, 10)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('y (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for k in range(0, 181, 1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 180.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
for k in range(359, 180, -1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 180.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
ax.annotate('',xytext=(30, 4),xy=(10, 4),arrowprops=dict(facecolor='black', shrink=0.05)) # i=-1
ax.text(5, 7, r'Wind speed: 5 (m/sec)', fontsize=15)
ax.text(5, 6, r'Wind direction: $\phi_{\rm{wind}}=180^\circ$', fontsize=15)
#
plt.savefig('Case10-Fig3.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0, 120)
ax.set_ylim(-10, 10)
ax.set_xlabel('x (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.set_ylabel('y (m)', fontweight='bold', fontsize=25, linespacing=1.0)
ax.tick_params(labelsize=15) 
#
for k in range(0, 181, 1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 270.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
for k in range(359, 180, -1):
  set_ball_w_theta = 1.0*k
  set_wind_phi = 270.0
  show_x, show_y, step = Drop_location(set_ball_w_theta, set_wind_phi)
  ax.plot(show_x, show_y, 'r-', markeredgecolor = 'none', linewidth=0.01)
  ax.plot(show_x[step], show_y[step], 'g.', markeredgecolor = 'none', markersize=10)
  if (k%5 == 0):
    ax.text(show_x[step], show_y[step], r'$\theta_w = %s^\circ$'%(set_ball_w_theta), fontweight='bold', fontsize=10)
  print set_ball_w_theta
#
ax.annotate('',xytext=(20, 5.5),xy=(20, 2.5),arrowprops=dict(facecolor='black', shrink=0.05)) # j=1
ax.text(5, 7, r'Wind speed: 5 (m/sec)', fontsize=15)
ax.text(5, 6, r'Wind direction: $\phi_{\rm{wind}}=270^\circ$', fontsize=15)
#
plt.savefig('Case10-Fig4.eps', format='eps', dpi=1000, bbox_inches='tight')
#----------------------------------------------------------------------------------------
