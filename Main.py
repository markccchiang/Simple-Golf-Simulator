#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    import ttk
else:
    from tkinter import *
    import ttk

import matplotlib.pyplot as plt
import Plot as pl
import Plot2 as pl2

if __name__ == '__main__':

   root = Tk()

   root.title("The Simple Golf Simulator (Copyright @ 2016 C.-C. Chiang)")

   entries = {}

   row = Frame(root)

   title_size = 10
   font_size = 10
   set_width = 50
   border_width = 2

   i = 0

   #
   # 1. Set golfer parameters
   # 
   lab = Label(row, width=set_width, text="(I) Set golfer parameters", background="lightgreen", font=("bold", title_size)).grid(row=i, columnspan=2)
   i = i+1

   lab = Label(row, width=set_width, text="  1. Gender: ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   variable = StringVar(row)
   variable.set("Male")
   w = OptionMenu(row, variable, "Male", "Female", "Average").grid(row=i, column=1, sticky="ew")
   entries['Gender'] = variable
   i = i+1

   lab = Label(row, width=set_width, text="  2. Weight (kg): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"70.0")
   ent.grid(row=i, column=1)
   entries['Weight'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="  3. Shoulder radius (m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.17")
   ent.grid(row=i, column=1)
   entries['R_S'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="  4. Arm length (m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.6")
   ent.grid(row=i, column=1)
   entries['R_A'] = ent
   i = i+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   #
   # 2. Set club parameters
   #
   lab = Label(row, width=set_width, text="(II) Set club parameters", background="lightgreen", font=("bold", title_size)).grid(row=i, columnspan=2)
   i = i+1

   lab = Label(row, width=set_width, text="  5. Head mass (kg): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.2")
   ent.grid(row=i, column=1)
   entries['M_C_head'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="  6. Shaft mass (kg): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.1")
   ent.grid(row=i, column=1)
   entries['M_C_shaft'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="  7. Head length (m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.1")
   ent.grid(row=i, column=1)
   entries['L_C_head'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="  8. Shaft length (m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"1.0")
   ent.grid(row=i, column=1)
   entries['L_C_shaft'] = ent
   i = i+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   #
   # 3. Set swing conditions
   #
   lab = Label(row, width=set_width, text="(III) Set swing conditions", background="lightgreen", font=("bold", title_size)).grid(row=i, columnspan=2)
   i = i+1

   lab = Label(row, width=set_width, text="  9. Swing plane angle (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"60")
   ent.grid(row=i, column=1)
   entries['phi'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="10. Initial arm angle (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"135")
   ent.grid(row=i, column=1)
   entries['theta'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*11. Impact arm angle (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=i, column=1)
   entries['theta_final'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="12. Initial wrist-cock angle (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"120")
   ent.grid(row=i, column=1)
   entries['beta'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*13. Impact wrist-cock angle (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=i, column=1)
   entries['beta_final'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*14. Horizontal acceleration (m/sec^2): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=i, column=1)
   entries['a_x'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*15. Vertical acceleration (m/sec^2): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=i, column=1)
   entries['a_y'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="16. Choose swing type: ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   variable = StringVar(row)
   variable.set("Type I")
   w = OptionMenu(row, variable, "Type I", "Type II").grid(row=i, column=1, sticky="ew")
   entries['Type'] = variable
   i = i+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   #
   # 4. Set swing torques
   #
   lab = Label(row, width=set_width, text="(IV) Set swing torques", background="lightgreen", font=("bold", title_size)).grid(row=i, columnspan=2)
   i = i+1

   lab = Label(row, width=set_width, text="17. Arm torque (N-m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"100")
   ent.grid(row=i, column=1)
   entries['Q_alpha'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*18. Raising time of arm torque (sec): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.01")
   ent.grid(row=i, column=1)
   entries['tau_Q_alpha'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="19. Wrist-cock torque (N-m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.config(fg = "grey", bg = "yellow")
   ent.insert(0,"N/A")
   ent.grid(row=i, column=1)
   entries['Q_beta'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="**20. At which arm angle the wrist-cock torque started (degree): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"135")
   ent.grid(row=i, column=1)
   entries['set_theta'] = ent
   i = i+1

   lab = Label(row, width=set_width, \
               text="(**) The angle in item 20 should be equal or smaller than the initial arm angle in item 10.", \
               fg="red", font=("Times", font_size), anchor='w').grid(row=i, column=0, columnspan=2, sticky="ew")
   i = i+1

   lab = Label(row, width=set_width, text="*21. Raising time of wrist-cock torque (sec): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0.01")
   ent.grid(row=i, column=1)
   entries['tau_Q_beta'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*22. Minimum of wrist-cock torque (N-m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"-50")
   ent.grid(row=i, column=1)
   entries['Q_beta_min'] = ent
   i = i+1

   lab = Label(row, width=set_width, text="*23. Maximum of wrist-cock torque (N-m): ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=i, column=1)
   entries['Q_beta_max'] = ent
   i = i+1

   ents1 = entries

   b1 = Button(row, text='Click to optimize wrist-cock torque (fast)', \
               relief=GROOVE, borderwidth=border_width, command=(lambda e1=ents1: pl.Optimize_Q_beta(e1)), \
               font=("bold", title_size), bg="yellow")
   b1.grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   b11 = Button(row, text='Click to optimize wrist-cock torque (complete)', \
                relief=GROOVE, borderwidth=border_width, command=(lambda e1=ents1: pl.Optimize_Q_beta_2(e1)), \
                font=("bold", title_size), bg="yellow")
   b11.grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=i, columnspan=2, sticky="ew")
   i = i+1

   #
   # 5. Simulate the swing
   #
   lab = Label(row, width=set_width, text="(V) Simulate the swing", background="lightgreen", font=("bold", title_size)).grid(row=i, columnspan=2)
   i = i+1
 
   lab = Label(row, width=set_width, text="24. Choose simulation method: ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   variable = StringVar(row)
   variable.set("Solution 3")
   w = OptionMenu(row, variable, "Solution 1", "Solution 2", "Solution 3").grid(row=i, column=1, sticky="ew")
   entries['Method'] = variable
   i = i+1

   lab = Label(row, width=set_width, text="25. Choose the results to plot: ", font=("Times", font_size), anchor='w').grid(row=i, column=0)
   i = i+1

   var = BooleanVar()
   c = Checkbutton(row, text="Tracks", font=("Times", font_size), variable=var)
   c.grid(row=i, column=0, sticky="w")
   entries['Fig1'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="Angles", font=("Times", font_size), variable=var)
   c.grid(row=i, column=1, sticky="w")
   entries['Fig2'] = var
   i = i+1

   var = BooleanVar()
   c = Checkbutton(row, text="Angular velocities", font=("Times", font_size), variable=var)
   c.grid(row=i, column=0, sticky="w")
   entries['Fig3'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="Angular accelerations", font=("Times", font_size), variable=var)
   c.grid(row=i, column=1, sticky="w")
   entries['Fig4'] = var
   i = i+1

   var = BooleanVar()
   c = Checkbutton(row, text="Clubhead velocity", font=("Times", font_size), variable=var)
   c.grid(row=i, column=0, sticky="w")
   entries['Fig5'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="Torques", font=("Times", font_size), variable=var)
   c.grid(row=i, column=1, sticky="w")
   entries['Fig6'] = var
   i = i+1

   var = BooleanVar()
   c = Checkbutton(row, text="Arm length", font=("Times", font_size), variable=var)
   c.grid(row=i, column=0, sticky="w")
   entries['Fig8'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="1st and 2nd moments", font=("Times", font_size), variable=var)
   c.grid(row=i, column=1, sticky="w")
   entries['Fig7'] = var
   i = i+2

   sep = ttk.Separator(row, orient = "vertical")
   sep.rowconfigure(0, weight = 1)
   sep.columnconfigure(1, weight = 1)
   sep.grid(row = 0, rowspan=i, column = 2, padx = 5, sticky = "nesw")

   #print i
   ttk.Separator(row, orient=HORIZONTAL).grid(row=i, columnspan=5, sticky="ew")

   j = 0

   lab = Label(row, width=set_width, text="26. Clubhead impact velocity (m/sec): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['VC'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="27. Systematic error of clubhead impact velocity (m/sec): ", \
               font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['error_VC'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="28. Clubhead impact angle (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['VC_angle'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="29. Systematic error of clubhead impact angle (degree): ", \
               font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['error_VC_angle'] = ent
   j = j+1

   #####
   ents2 = entries

   b2 = Button(row, text='Click to simulate / plot golf swing', relief=GROOVE, borderwidth=border_width, command=(lambda e2=ents2: pl.Plot(e2)), font=("bold", title_size), bg="cyan")
   b2.grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1
   #####

   ttk.Separator(row, orient=HORIZONTAL).grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1

   #
   # 6. Set golf ball parameters
   #
   lab = Label(row, width=set_width, text="(VI) Set golf ball parameters", background="lightgreen", font=("bold", title_size)).grid(row=j, column=3, columnspan=2)
   j = j+1

   lab = Label(row, width=set_width, text="30. Mass (kg): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0.0458")
   ent.grid(row=j, column=4)
   entries['ball_mass'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="31. Diameter (m): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0.0428")
   ent.grid(row=j, column=4)
   entries['ball_diameter'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="32. COR: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0.775")
   ent.grid(row=j, column=4)
   entries['COR'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="33. Drag coefficient: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0.285")
   ent.grid(row=j, column=4)
   entries['C_D'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="34. Lift coefficient: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0.1")
   ent.grid(row=j, column=4)
   entries['C_L'] = ent
   j = j+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1

   #
   # 7. Set environmental conditions
   #
   lab = Label(row, width=set_width, text="(VII) Set environmental conditions", background="lightgreen", font=("bold", title_size)).grid(row=j, column=3, columnspan=2)
   j = j+1

   lab = Label(row, width=set_width, text="*35. Air density (kg/m^3): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"1.2")
   ent.grid(row=j, column=4)
   entries['rho_air'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="36. Wind speed (absolute value) (m/sec): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['v_wind'] = ent
   j = j+1
 
   lab = Label(row, width=set_width, text="37. Wind elevation angle: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['wind_theta'] = ent
   j = j+1
 
   lab = Label(row, width=set_width, text="38. Wind direction angle: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['wind_phi'] = ent
   j = j+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1

   #
   # 8. Set initial conditions of golf ball
   #
   lab = Label(row, width=set_width, text="(VIII) Set launch conditions of golf ball", background="lightgreen", font=("bold", title_size)).grid(row=j, column=3, columnspan=2)
   j = j+1

   lab = Label(row, width=set_width, text="39. Loft angle of clubhead (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"15")
   ent.grid(row=j, column=4)
   entries['clubhead_loft'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="40. Launch speed (absolute value) (m/sec): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(fg = "grey", bg = "yellow")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['ball_U'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="41. Launch elevation angle (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(fg = "grey", bg = "yellow")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['ball_theta'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="*42. Launch direction angle (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['ball_phi'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="43. Spin elevation angle (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['ball_w_theta'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="44. Spin direction angle (degree): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"-90")
   ent.grid(row=j, column=4)
   entries['ball_w_phi'] = ent
   j = j+1

   #####
   ents4 = entries

   b4 = Button(row, text='Click to calculate golf ball launch speed and elevation angle \n(based on clubhead impact velocity and loft angle)', \
               relief=GROOVE, borderwidth=border_width,command=(lambda e4=ents4: pl.get_ball_velocity(e4)), font=("bold", title_size), bg="yellow")
   b4.grid(row=j, rowspan=3, column=3, columnspan=2, sticky="ew")
   j = j+3
   #####

   ttk.Separator(row, orient=HORIZONTAL).grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1

   #
   # 9. Simulate the golf ball trajectory
   #
   lab = Label(row, width=set_width, text="(IX) Simulate the golf ball trajectory", background="lightgreen", font=("bold", title_size)).grid(row=j, column=3, columnspan=2)
   j = j+1

   lab = Label(row, width=set_width, text="*45. Altitude of target (m): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.insert(0,"0")
   ent.grid(row=j, column=4)
   entries['Altitude'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="46. Choose the results to plot: ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   j = j+1

   var = BooleanVar()
   c = Checkbutton(row, text="X-Z", font=("Times", font_size), variable=var)
   c.grid(row=j, column=3, sticky="w")
   entries['Figure1'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="X-Y", font=("Times", font_size), variable=var)
   c.grid(row=j, column=4, sticky="w")
   entries['Figure2'] = var
   j = j+1

   var = BooleanVar()
   c = Checkbutton(row, text="Y-Z", font=("Times", font_size), variable=var)
   c.grid(row=j, column=3, sticky="w")
   entries['Figure3'] = var

   var = BooleanVar()
   c = Checkbutton(row, text="X-Y-Z (3-D plot)", font=("Times", font_size), variable=var)
   c.grid(row=j, column=4, sticky="w")
   entries['Figure4'] = var
   j = j+1

   lab = Label(row, width=set_width, text="47. Drop location in X (m): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['X_final'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="48. Drop location in Y (m): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['Y_final'] = ent
   j = j+1

   lab = Label(row, width=set_width, text="49. Flight distance in X-Y plane (m): ", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   ent = Entry(row)
   ent.config(bg="cyan", fg="grey")
   ent.insert(0,"N/A")
   ent.grid(row=j, column=4)
   entries['Distance'] = ent
   j = j+1

   #####
   ents5 = entries

   b5 = Button(row, text='Click to simulate / plot golf ball trajectory', relief=GROOVE, borderwidth=border_width, \
               command=(lambda e5=ents5: pl2.Plot(e5)), font=("bold", title_size), bg="cyan")
   b5.grid(row=j, rowspan=1, column=3, columnspan=2, sticky="ew")
   j = j+1

   ttk.Separator(row, orient=HORIZONTAL).grid(row=j, column=3, columnspan=2, sticky="ew")
   j = j+1

   lab = Label(row, width=set_width, \
               text="(*) The suggested default value.", \
               fg="red", font=("Times", font_size), anchor='w').grid(row=j, column=3)
   #j = j+1
   ###############

   row.pack()

   root.mainloop()

