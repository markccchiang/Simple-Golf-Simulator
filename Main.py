#!/usr/bin/env python
import glob
import os
import sys

# In a venv (e.g. uv), Tcl searches for init.tcl next to the venv's python
# symlink instead of the base install; point it at the base install.
if sys.prefix != sys.base_prefix and 'TCL_LIBRARY' not in os.environ:
   for tcl_dir in sorted(glob.glob(os.path.join(sys.base_prefix, 'lib', 'tcl[89].*')), reverse=True):
       if os.path.isfile(os.path.join(tcl_dir, 'init.tcl')):
           os.environ['TCL_LIBRARY'] = tcl_dir
           break

from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
import Plot as pl
import Plot2 as pl2

if __name__ == '__main__':

   root = Tk()
   root.title("The Simple Golf Simulator (Copyright @ 2026 C.-C. Chiang)")

   # Window icon (PNG needs Tk 8.6+; skip silently on older Tk)
   icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.png')
   try:
       root.icon = PhotoImage(file=icon_path)
       root.iconphoto(True, root.icon)
   except TclError:
       pass

   style = ttk.Style()
   if sys.platform == 'darwin':
       style.theme_use('aqua')
   else:
       style.theme_use('clam')

   style.configure('Section.TLabelframe.Label', font=('Helvetica', 11, 'bold'))
   style.configure('Action.TButton', font=('Helvetica', 10, 'bold'))

   entries = {}

   title_size = 10
   font_size = 10
   label_font = ("Helvetica", font_size)
   entry_width = 12
   border_width = 2
   pad_x = 6
   pad_y = 3
   section_pad = (10, 5)

   # --- Scrollable canvas ---
   canvas = Canvas(root, highlightthickness=0)
   scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
   outer_frame = ttk.Frame(canvas)

   outer_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
   canvas.create_window((0, 0), window=outer_frame, anchor="nw")
   canvas.configure(yscrollcommand=scrollbar.set)

   def _on_mousewheel(event):
       if sys.platform == 'darwin':
           canvas.yview_scroll(-1 * event.delta, "units")
       else:
           canvas.yview_scroll(-1 * (event.delta // 120), "units")
   canvas.bind_all("<MouseWheel>", _on_mousewheel)

   scrollbar.pack(side=RIGHT, fill=Y)
   canvas.pack(side=LEFT, fill=BOTH, expand=True)

   # Two-column layout: left panel and right panel
   left_panel = ttk.Frame(outer_frame)
   left_panel.grid(row=0, column=0, sticky="n", padx=10, pady=10)

   sep = ttk.Separator(outer_frame, orient=VERTICAL)
   sep.grid(row=0, column=1, sticky="ns", padx=5, pady=10)

   right_panel = ttk.Frame(outer_frame)
   right_panel.grid(row=0, column=2, sticky="n", padx=10, pady=10)

   # =========================================================================
   # LEFT PANEL
   # =========================================================================

   def add_label_entry(parent, row, text, default, key):
       ttk.Label(parent, text=text, font=label_font, anchor='w').grid(
           row=row, column=0, sticky='w', padx=pad_x, pady=pad_y)
       ent = ttk.Entry(parent, width=entry_width)
       ent.insert(0, default)
       ent.grid(row=row, column=1, sticky='e', padx=pad_x, pady=pad_y)
       ent.label = text.lstrip('*').rstrip(':')  # named in input error messages
       entries[key] = ent
       return ent

   def add_option_menu(parent, row, text, default, options, key):
       ttk.Label(parent, text=text, font=label_font, anchor='w').grid(
           row=row, column=0, sticky='w', padx=pad_x, pady=pad_y)
       variable = StringVar(parent)
       variable.set(default)
       om = ttk.OptionMenu(parent, variable, default, *options)
       om.grid(row=row, column=1, sticky='ew', padx=pad_x, pady=pad_y)
       entries[key] = variable

   # --- Section I: Golfer Parameters ---
   sec1 = ttk.LabelFrame(left_panel, text="  (I) Golfer Parameters  ", style='Section.TLabelframe')
   sec1.grid(row=0, column=0, sticky='ew', pady=section_pad)

   add_option_menu(sec1, 0, "1. Gender:", "Male", ["Male", "Female", "Average"], 'Gender')
   add_label_entry(sec1, 1, "2. Weight (kg):", "70.0", 'Weight')
   add_label_entry(sec1, 2, "3. Shoulder radius (m):", "0.17", 'R_S')
   add_label_entry(sec1, 3, "4. Arm length (m):", "0.6", 'R_A')

   # --- Section II: Club Parameters ---
   sec2 = ttk.LabelFrame(left_panel, text="  (II) Club Parameters  ", style='Section.TLabelframe')
   sec2.grid(row=1, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec2, 0, "5. Head mass (kg):", "0.2", 'M_C_head')
   add_label_entry(sec2, 1, "6. Shaft mass (kg):", "0.1", 'M_C_shaft')
   add_label_entry(sec2, 2, "7. Head length (m):", "0.1", 'L_C_head')
   add_label_entry(sec2, 3, "8. Shaft length (m):", "1.0", 'L_C_shaft')

   # --- Section III: Swing Conditions ---
   sec3 = ttk.LabelFrame(left_panel, text="  (III) Swing Conditions  ", style='Section.TLabelframe')
   sec3.grid(row=2, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec3, 0, "9. Swing plane angle (deg):", "60", 'phi')
   add_label_entry(sec3, 1, "10. Initial arm angle (deg):", "135", 'theta')
   add_label_entry(sec3, 2, "*11. Impact arm angle (deg):", "0", 'theta_final')
   add_label_entry(sec3, 3, "12. Initial wrist-cock angle (deg):", "120", 'beta')
   add_label_entry(sec3, 4, "*13. Impact wrist-cock angle (deg):", "0", 'beta_final')
   add_label_entry(sec3, 5, "*14. Horizontal accel. (m/s\u00b2):", "0", 'a_x')
   add_label_entry(sec3, 6, "*15. Vertical accel. (m/s\u00b2):", "0", 'a_y')
   add_option_menu(sec3, 7, "16. Swing type:", "Type I", ["Type I", "Type II"], 'Type')

   # --- Section IV: Swing Torques ---
   sec4 = ttk.LabelFrame(left_panel, text="  (IV) Swing Torques  ", style='Section.TLabelframe')
   sec4.grid(row=3, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec4, 0, "17. Arm torque (N-m):", "100", 'Q_alpha')
   add_label_entry(sec4, 1, "*18. Raising time of arm torque (s):", "0.01", 'tau_Q_alpha')

   ttk.Label(sec4, text="19. Wrist-cock torque (N-m):", font=label_font, anchor='w').grid(
       row=2, column=0, sticky='w', padx=pad_x, pady=pad_y)
   ent = ttk.Entry(sec4, width=entry_width)
   ent.insert(0, "N/A")
   ent.state(['readonly'])
   ent.grid(row=2, column=1, sticky='e', padx=pad_x, pady=pad_y)
   entries['Q_beta'] = ent

   add_label_entry(sec4, 3, "**20. Wrist-cock torque start angle (deg):", "135", 'set_theta')

   note = ttk.Label(sec4, text="(**) Item 20 should be \u2264 item 10.",
                     foreground="red", font=("Helvetica", 9))
   note.grid(row=4, column=0, columnspan=2, sticky='w', padx=pad_x, pady=(0, pad_y))

   add_label_entry(sec4, 5, "*21. Raising time of wrist-cock torque (s):", "0.01", 'tau_Q_beta')
   add_label_entry(sec4, 6, "*22. Min wrist-cock torque (N-m):", "-50", 'Q_beta_min')
   add_label_entry(sec4, 7, "*23. Max wrist-cock torque (N-m):", "0", 'Q_beta_max')

   ents1 = entries

   btn_frame1 = ttk.Frame(sec4)
   btn_frame1.grid(row=8, column=0, columnspan=2, sticky='ew', padx=pad_x, pady=pad_y)
   Button(btn_frame1, text='Optimize wrist-cock torque (fast)',
          relief=GROOVE, borderwidth=border_width,
          command=(lambda e1=ents1: pl.Optimize_Q_beta(e1)),
          font=("Helvetica", 9, "bold"), bg="#FFD700", activebackground="#FFE44D"
          ).pack(fill=X, pady=2)
   Button(btn_frame1, text='Optimize wrist-cock torque (complete)',
          relief=GROOVE, borderwidth=border_width,
          command=(lambda e1=ents1: pl.Optimize_Q_beta_2(e1)),
          font=("Helvetica", 9, "bold"), bg="#FFD700", activebackground="#FFE44D"
          ).pack(fill=X, pady=2)

   # --- Section V: Simulate the Swing ---
   sec5 = ttk.LabelFrame(left_panel, text="  (V) Simulate the Swing  ", style='Section.TLabelframe')
   sec5.grid(row=4, column=0, sticky='ew', pady=section_pad)

   add_option_menu(sec5, 0, "24. Simulation method:", "Solution 3",
                   ["Solution 1", "Solution 2", "Solution 3"], 'Method')

   ttk.Label(sec5, text="25. Results to plot:", font=label_font, anchor='w').grid(
       row=1, column=0, columnspan=2, sticky='w', padx=pad_x, pady=pad_y)

   check_frame = ttk.Frame(sec5)
   check_frame.grid(row=2, column=0, columnspan=2, sticky='w', padx=pad_x)

   fig_checks = [
       ("Tracks", 'Fig1'),
       ("Angles", 'Fig2'),
       ("Angular velocities", 'Fig3'),
       ("Angular accelerations", 'Fig4'),
       ("Clubhead velocity", 'Fig5'),
       ("Torques", 'Fig6'),
       ("Arm length", 'Fig8'),
       ("1st and 2nd moments", 'Fig7'),
   ]
   for idx, (label, key) in enumerate(fig_checks):
       var = BooleanVar()
       c = ttk.Checkbutton(check_frame, text=label, variable=var)
       c.grid(row=idx // 2, column=idx % 2, sticky='w', padx=8, pady=2)
       entries[key] = var

   # =========================================================================
   # RIGHT PANEL
   # =========================================================================

   # --- Swing Results ---
   sec_res = ttk.LabelFrame(right_panel, text="  Swing Results  ", style='Section.TLabelframe')
   sec_res.grid(row=0, column=0, sticky='ew', pady=section_pad)

   result_fields = [
       ("26. Clubhead impact velocity (m/s):", 'VC'),
       ("27. Systematic error of velocity (m/s):", 'error_VC'),
       ("28. Clubhead impact angle (deg):", 'VC_angle'),
       ("29. Systematic error of angle (deg):", 'error_VC_angle'),
   ]
   for idx, (text, key) in enumerate(result_fields):
       ttk.Label(sec_res, text=text, font=label_font, anchor='w').grid(
           row=idx, column=0, sticky='w', padx=pad_x, pady=pad_y)
       ent = ttk.Entry(sec_res, width=entry_width)
       ent.insert(0, "N/A")
       ent.state(['readonly'])
       ent.grid(row=idx, column=1, sticky='e', padx=pad_x, pady=pad_y)
       entries[key] = ent

   ents2 = entries

   Button(sec_res, text='Simulate / Plot Golf Swing',
          relief=GROOVE, borderwidth=border_width,
          command=(lambda e2=ents2: pl.Plot(e2)),
          font=("Helvetica", 10, "bold"), bg="#87CEEB", activebackground="#A8DCED"
          ).grid(row=4, column=0, columnspan=2, sticky='ew', padx=pad_x, pady=(8, pad_y))

   # --- Section VI: Golf Ball Parameters ---
   sec6 = ttk.LabelFrame(right_panel, text="  (VI) Golf Ball Parameters  ", style='Section.TLabelframe')
   sec6.grid(row=1, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec6, 0, "30. Mass (kg):", "0.0458", 'ball_mass')
   add_label_entry(sec6, 1, "31. Diameter (m):", "0.0428", 'ball_diameter')
   add_label_entry(sec6, 2, "32. COR:", "0.775", 'COR')
   add_label_entry(sec6, 3, "33. Drag coefficient:", "0.285", 'C_D')
   add_label_entry(sec6, 4, "34. Lift coefficient:", "0.1", 'C_L')

   # --- Section VII: Environmental Conditions ---
   sec7 = ttk.LabelFrame(right_panel, text="  (VII) Environmental Conditions  ", style='Section.TLabelframe')
   sec7.grid(row=2, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec7, 0, "*35. Air density (kg/m\u00b3):", "1.2", 'rho_air')
   add_label_entry(sec7, 1, "36. Wind speed (m/s):", "0", 'v_wind')
   add_label_entry(sec7, 2, "37. Wind elevation angle (deg):", "0", 'wind_theta')
   add_label_entry(sec7, 3, "38. Wind direction angle (deg):", "0", 'wind_phi')

   # --- Section VIII: Launch Conditions ---
   sec8 = ttk.LabelFrame(right_panel, text="  (VIII) Launch Conditions  ", style='Section.TLabelframe')
   sec8.grid(row=3, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec8, 0, "39. Loft angle of clubhead (deg):", "15", 'clubhead_loft')

   ttk.Label(sec8, text="40. Launch speed (m/s):", font=label_font, anchor='w').grid(
       row=1, column=0, sticky='w', padx=pad_x, pady=pad_y)
   ent = ttk.Entry(sec8, width=entry_width)
   ent.insert(0, "N/A")
   ent.state(['readonly'])
   ent.grid(row=1, column=1, sticky='e', padx=pad_x, pady=pad_y)
   entries['ball_U'] = ent

   ttk.Label(sec8, text="41. Launch elevation angle (deg):", font=label_font, anchor='w').grid(
       row=2, column=0, sticky='w', padx=pad_x, pady=pad_y)
   ent = ttk.Entry(sec8, width=entry_width)
   ent.insert(0, "N/A")
   ent.state(['readonly'])
   ent.grid(row=2, column=1, sticky='e', padx=pad_x, pady=pad_y)
   entries['ball_theta'] = ent

   add_label_entry(sec8, 3, "*42. Launch direction angle (deg):", "0", 'ball_phi')
   add_label_entry(sec8, 4, "43. Spin elevation angle (deg):", "0", 'ball_w_theta')
   add_label_entry(sec8, 5, "44. Spin direction angle (deg):", "-90", 'ball_w_phi')

   ents4 = entries

   Button(sec8, text='Calculate launch speed and\nelevation angle from impact',
          relief=GROOVE, borderwidth=border_width,
          command=(lambda e4=ents4: pl.get_ball_velocity(e4)),
          font=("Helvetica", 9, "bold"), bg="#FFD700", activebackground="#FFE44D"
          ).grid(row=6, column=0, columnspan=2, sticky='ew', padx=pad_x, pady=(8, pad_y))

   # --- Section IX: Ball Trajectory ---
   sec9 = ttk.LabelFrame(right_panel, text="  (IX) Ball Trajectory  ", style='Section.TLabelframe')
   sec9.grid(row=4, column=0, sticky='ew', pady=section_pad)

   add_label_entry(sec9, 0, "*45. Target altitude (m):", "0", 'Altitude')

   ttk.Label(sec9, text="46. Results to plot:", font=label_font, anchor='w').grid(
       row=1, column=0, columnspan=2, sticky='w', padx=pad_x, pady=pad_y)

   check_frame2 = ttk.Frame(sec9)
   check_frame2.grid(row=2, column=0, columnspan=2, sticky='w', padx=pad_x)

   fig2_checks = [
       ("X-Z", 'Figure1'),
       ("X-Y", 'Figure2'),
       ("Y-Z", 'Figure3'),
       ("X-Y-Z (3D)", 'Figure4'),
   ]
   for idx, (label, key) in enumerate(fig2_checks):
       var = BooleanVar()
       c = ttk.Checkbutton(check_frame2, text=label, variable=var)
       c.grid(row=idx // 2, column=idx % 2, sticky='w', padx=8, pady=2)
       entries[key] = var

   # Trajectory results
   traj_results = [
       ("47. Drop location X (m):", 'X_final'),
       ("48. Drop location Y (m):", 'Y_final'),
       ("49. Flight distance X-Y (m):", 'Distance'),
   ]
   for idx, (text, key) in enumerate(traj_results):
       ttk.Label(sec9, text=text, font=label_font, anchor='w').grid(
           row=3 + idx, column=0, sticky='w', padx=pad_x, pady=pad_y)
       ent = ttk.Entry(sec9, width=entry_width)
       ent.insert(0, "N/A")
       ent.state(['readonly'])
       ent.grid(row=3 + idx, column=1, sticky='e', padx=pad_x, pady=pad_y)
       entries[key] = ent

   ents5 = entries

   Button(sec9, text='Simulate / Plot Ball Trajectory',
          relief=GROOVE, borderwidth=border_width,
          command=(lambda e5=ents5: pl2.Plot(e5)),
          font=("Helvetica", 10, "bold"), bg="#87CEEB", activebackground="#A8DCED"
          ).grid(row=6, column=0, columnspan=2, sticky='ew', padx=pad_x, pady=(8, pad_y))

   # --- Footer ---
   note_label = ttk.Label(right_panel, text="(*) Suggested default value.",
                           foreground="red", font=("Helvetica", 9))
   note_label.grid(row=5, column=0, sticky='w', padx=pad_x, pady=(8, 0))

   # Set minimum window size and initial geometry
   root.update_idletasks()
   root.minsize(800, 600)
   root.geometry("1050x750")

   root.mainloop()
