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

import tkinter.font as tkfont
from tkinter import BooleanVar, Canvas, PhotoImage, StringVar, TclError, Tk
from tkinter import ttk

import matplotlib.pyplot as plt
import Plot as pl
import Plot2 as pl2
import UIFunc as ui
import Workflow as wf

#
# Input fields: (key, item number, label, default, first step that uses it (1-4), tab, group).
# Keys are the ones Plot.py and Plot2.py read; item numbers match the user's guide.
# The 'Advanced' group of each tab is folded away until opened.
#
TABS = (('golfer', 'Golfer & club'), ('swing', 'Swing'), ('ball', 'Ball & conditions'))

FIELDS = (
    ('Gender',        1,  'Gender',                                  'Male',       1, 'golfer', 'Golfer'),
    ('Weight',        2,  'Weight (kg)',                             '70.0',       1, 'golfer', 'Golfer'),
    ('R_S',           3,  'Shoulder radius (m)',                     '0.17',       1, 'golfer', 'Golfer'),
    ('R_A',           4,  'Arm length (m)',                          '0.6',        1, 'golfer', 'Golfer'),
    ('M_C_head',      5,  'Head mass (kg)',                          '0.2',        1, 'golfer', 'Club'),
    ('M_C_shaft',     6,  'Shaft mass (kg)',                         '0.1',        1, 'golfer', 'Club'),
    ('L_C_head',      7,  'Head length (m)',                         '0.1',        1, 'golfer', 'Club'),
    ('L_C_shaft',     8,  'Shaft length (m)',                        '1.0',        1, 'golfer', 'Club'),

    ('phi',           9,  'Swing plane angle (deg)',                 '60',         1, 'swing',  'Swing'),
    ('theta',         10, 'Initial arm angle (deg)',                 '135',        1, 'swing',  'Swing'),
    ('beta',          12, 'Initial wrist-cock angle (deg)',          '120',        1, 'swing',  'Swing'),
    ('Type',          16, 'Swing type',                              'Type I',     1, 'swing',  'Swing'),
    ('Method',        24, 'Solver',                                  'Solution 4', 1, 'swing',  'Swing'),
    ('Q_alpha',       17, 'Arm torque (N-m)',                        '100',        1, 'swing',  'Torques'),
    ('Q_beta',        19, 'Wrist-cock torque (N-m)',                 '',           2, 'swing',  'Torques'),
    ('set_theta',     20, 'Wrist torque starts at arm angle (deg)',  '135',        1, 'swing',  'Torques'),
    ('beta_final',    13, 'Target wrist-cock angle at impact (deg)', '0',          1, 'swing',  'Wrist-torque search'),
    ('Q_beta_min',    22, 'Lowest torque to try (N-m)',              '-50',        1, 'swing',  'Wrist-torque search'),
    ('Q_beta_max',    23, 'Highest torque to try (N-m)',             '0',          1, 'swing',  'Wrist-torque search'),
    ('Optimizer',     '', 'Search',                                  'Fast',       1, 'swing',  'Wrist-torque search'),
    ('theta_final',   11, 'Impact arm angle (deg)',                  '0',          1, 'swing',  'Advanced'),
    ('a_x',           14, 'Horizontal hand accel. (m/s²)',           '0',          1, 'swing',  'Advanced'),
    ('a_y',           15, 'Vertical hand accel. (m/s²)',             '0',          1, 'swing',  'Advanced'),
    ('tau_Q_alpha',   18, 'Arm torque rise time (s)',                '0.01',       1, 'swing',  'Advanced'),
    ('tau_Q_beta',    21, 'Wrist torque rise time (s)',              '0.01',       1, 'swing',  'Advanced'),

    ('ball_mass',     30, 'Mass (kg)',                               '0.0458',     3, 'ball',   'Golf ball'),
    ('ball_diameter', 31, 'Diameter (m)',                            '0.0428',     4, 'ball',   'Golf ball'),
    ('COR',           32, 'Coefficient of restitution',              '0.775',      3, 'ball',   'Golf ball'),
    ('C_D',           33, 'Drag coefficient',                        '0.285',      4, 'ball',   'Golf ball'),
    ('C_L',           34, 'Lift coefficient',                        '0.1',        4, 'ball',   'Golf ball'),
    ('clubhead_loft', 39, 'Clubhead loft (deg)',                     '15',         3, 'ball',   'Launch'),
    ('ball_U',        40, 'Launch speed (m/s)',                      '',           4, 'ball',   'Launch'),
    ('ball_theta',    41, 'Launch elevation (deg)',                  '',           4, 'ball',   'Launch'),
    ('ball_phi',      42, 'Launch direction (deg)',                  '0',          4, 'ball',   'Launch'),
    ('ball_w_theta',  43, 'Spin elevation (deg)',                    '0',          4, 'ball',   'Launch'),
    ('ball_w_phi',    44, 'Spin direction (deg)',                    '-90',        4, 'ball',   'Launch'),
    ('v_wind',        36, 'Wind speed (m/s)',                        '0',          4, 'ball',   'Wind'),
    ('wind_theta',    37, 'Wind elevation (deg)',                    '0',          4, 'ball',   'Wind'),
    ('wind_phi',      38, 'Wind direction (deg)',                    '0',          4, 'ball',   'Wind'),
    ('rho_air',       35, 'Air density (kg/m³)',                     '1.2',        4, 'ball',   'Advanced'),
    ('Altitude',      45, 'Landing height vs. tee (m)',              '0',          4, 'ball',   'Advanced'),
)

SELECTS = {
    'Gender':    ('Male', 'Female', 'Average'),
    'Type':      ('Type I', 'Type II'),
    'Method':    ('Solution 4', 'Solution 1', 'Solution 2', 'Solution 3'),
    'Optimizer': ('Fast', 'Complete'),
}

HELP = {
    'Method':    'Solution 4 is the accurate RK4 solver; 1–3 are the report’s original methods.',
    'Q_beta':    'Filled by step 1, or type a torque to skip the optimizer.',
    'Optimizer': 'Complete scans a wider range of torques (slower).',
    'ball_U':    'Filled by step 3, or type both launch values to study the ball flight on its own.',
}

ADVANCED_HINT = {'swing': 'rise times, accelerations, impact arm angle', 'ball': 'air density, landing height'}

#
# Plots, shown in their own windows: (key, label, on by default)
#
SWING_PLOTS = (('Fig1', 'Swing tracks', True), ('Fig2', 'Angles', False), ('Fig3', 'Angular velocities', False),
               ('Fig4', 'Angular accelerations', False), ('Fig5', 'Clubhead speed', False), ('Fig6', 'Torques', False),
               ('Fig8', 'Arm length', False), ('Fig7', '1st and 2nd moments', False), ('Fig0', 'Wrist-torque search', False))
BALL_PLOTS = (('Figure1', 'Side view (X-Z)', True), ('Figure2', 'Top view (X-Y)', False),
              ('Figure3', 'Rear view (Y-Z)', False), ('Figure4', '3D', False))

RESULT_KEYS = ('VC', 'error_VC', 'VC_angle', 'error_VC_angle', 'X_final', 'Y_final', 'Distance', 'Apex', 'Flight_time')

STAGE = {f[0]: f[4] for f in FIELDS}
NUMERIC_KEYS = [f[0] for f in FIELDS if f[0] not in SELECTS]

def palette(root):
    """Text colors readable on the window background (light or dark appearance)."""
    try:
        r, g, b = root.winfo_rgb('systemWindowBackgroundColor')
    except TclError:
        r, g, b = root.winfo_rgb(ttk.Style().lookup('TFrame', 'background') or 'white')
    dark = (0.299*r + 0.587*g + 0.114*b) / 65535 < 0.5
    if dark:
        return dict(muted='#a3a8b0', ok='#6fcf97', stale='#f2c14e', error='#ff8a78', manual='#8fb4ff')
    return dict(muted='#5f6368', ok='#1d7a4f', stale='#8a5a00', error='#c0392b', manual='#2456a8')

class ScrollFrame(ttk.Frame):
    """A frame whose content scrolls vertically when it is taller than the window."""
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = Canvas(self, highlightthickness=0, borderwidth=0)
        self.bar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, padding=(12, 4, 16, 12))
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.canvas.configure(yscrollcommand=self.bar.set)
        self.inner.bind('<Configure>', self._layout)
        self.canvas.bind('<Configure>', self._layout)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.bind('<Enter>', lambda e: self._wheel(True))
        self.bind('<Leave>', lambda e: self._wheel(False))

    def _layout(self, event=None):
        # The content always fills the visible area (so no bare canvas shows below it);
        # the scrollbar appears only when the content is taller than the area.
        need, have, width = self.inner.winfo_reqheight(), self.canvas.winfo_height(), self.canvas.winfo_width()
        self.canvas.itemconfigure(self.window, width=width, height=max(need, have))
        self.canvas.configure(scrollregion=(0, 0, width, max(need, have)))
        if need > have and not self.bar.winfo_ismapped():
            self.bar.pack(side='right', fill='y', before=self.canvas)
        elif need <= have and self.bar.winfo_ismapped():
            self.bar.pack_forget()
            self.canvas.yview_moveto(0)

    def _wheel(self, on):
        if not on:
            for seq in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                self.unbind_all(seq)
            return
        def scroll(event):
            if getattr(event, 'num', None) in (4, 5):
                step = -1 if event.num == 4 else 1
            elif sys.platform == 'darwin':
                step = -event.delta
            else:
                step = -(event.delta // 120)
            if self.inner.winfo_height() > self.canvas.winfo_height():
                self.canvas.yview_scroll(step, 'units')
        self.bind_all('<MouseWheel>', scroll)
        self.bind_all('<Button-4>', scroll)
        self.bind_all('<Button-5>', scroll)

class Panel:
    def __init__(self, root):
        self.root = root
        self.flow = wf.Workflow()
        self.entries = {}     # what Plot.py / Plot2.py read: Entry widgets, StringVars, BooleanVars, results
        self.vars = {}        # key -> StringVar of each input
        self.rows = {}        # key -> dict of that field's extra widgets (error, badge, reset)
        self.tab_of = {}      # key -> tab frame
        self.busy = False     # a step is writing into the fields: not a user edit
        self.running = False
        self.active = None    # step running now
        self.message = None   # (text, kind) shown instead of the usual status line
        self.colors = palette(root)
        base = tkfont.nametofont('TkDefaultFont')
        self.small = base.copy()
        self.small.configure(size=max(base.cget('size') - 1, 9))
        self.bold = base.copy()
        self.bold.configure(weight='bold')
        self.big = base.copy()
        self.big.configure(size=base.cget('size') + 8)

        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)
        self.build_header()
        self.build_inputs()
        self.build_right()
        self.refresh()

    # --- Layout ---------------------------------------------------------------------------------

    def build_header(self):
        bar = ttk.Frame(self.root, padding=(16, 10))
        bar.grid(row=0, column=0, columnspan=2, sticky='ew')
        bar.columnconfigure(2, weight=1)
        try:
            self.logo = PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     os.pardir, 'assets', 'logo.png')).subsample(14)
            ttk.Label(bar, image=self.logo).grid(row=0, column=0, rowspan=2, padx=(0, 10))
        except TclError:
            pass
        ttk.Label(bar, text='Simple Golf Simulator', font=self.bold).grid(row=0, column=1, sticky='w')
        ttk.Label(bar, text='Swing mechanics → ball flight', font=self.small,
                  foreground=self.colors['muted']).grid(row=1, column=1, sticky='w')
        ttk.Button(bar, text='Reset to defaults', command=self.reset).grid(row=0, column=3, rowspan=2)
        ttk.Separator(self.root).grid(row=0, column=0, columnspan=2, sticky='sew')

    def build_inputs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=(12, 6), pady=12)
        self.tabs = {}
        for tab_key, title in TABS:
            frame = ScrollFrame(self.notebook)
            self.notebook.add(frame, text=title)
            self.tabs[tab_key] = frame
            grid = frame.inner
            grid.columnconfigure(1, weight=1)
            row = 0
            group = None
            self.advanced_rows = getattr(self, 'advanced_rows', {})
            for key, num, label, default, stage, tab, grp in FIELDS:
                if tab != tab_key:
                    continue
                if grp != group:
                    group = grp
                    row = self.add_group_title(grid, row, tab_key, grp)
                row = self.add_field(grid, row, key, num, label, default, tab_key, grp == 'Advanced')
            for widget in self.advanced_rows.get(tab_key, []):
                widget.grid_remove()

    def add_group_title(self, grid, row, tab_key, title):
        if title != 'Advanced':
            ttk.Label(grid, text=title.upper(), font=self.small, foreground=self.colors['muted']).grid(
                row=row, column=0, columnspan=5, sticky='w', pady=(14, 2))
            return row + 1
        self.advanced_open = getattr(self, 'advanced_open', {})
        self.advanced_open[tab_key] = False
        button = ttk.Button(grid, style='Toolbutton', command=lambda: self.toggle_advanced(tab_key))
        button.grid(row=row, column=0, columnspan=5, sticky='w', pady=(14, 2))
        self.advanced_buttons = getattr(self, 'advanced_buttons', {})
        self.advanced_buttons[tab_key] = button
        self.set_advanced_text(tab_key)
        return row + 1

    def set_advanced_text(self, tab_key):
        opened = self.advanced_open[tab_key]
        self.advanced_buttons[tab_key].configure(
            text=('▾ Advanced' if opened else '▸ Advanced  (%s)' % ADVANCED_HINT[tab_key]))

    def toggle_advanced(self, tab_key):
        self.advanced_open[tab_key] = not self.advanced_open[tab_key]
        for widget in self.advanced_rows[tab_key]:
            if self.advanced_open[tab_key]:
                widget.grid()
            else:
                widget.grid_remove()
        self.set_advanced_text(tab_key)
        self.refresh()

    def add_field(self, grid, row, key, num, label, default, tab_key, advanced):
        placed = []
        def place(widget, **kw):
            widget.grid(**kw)
            placed.append(widget)
        place(ttk.Label(grid, text=str(num), font=self.small, foreground=self.colors['muted'], width=3, anchor='e'),
              row=row, column=0, sticky='e', padx=(0, 8))
        place(ttk.Label(grid, text=label), row=row, column=1, sticky='w', pady=3)
        var = StringVar(self.root, value=default)
        self.vars[key] = var
        if key in SELECTS:
            widget = ttk.Combobox(grid, textvariable=var, values=SELECTS[key], state='readonly', width=11)
            self.entries[key] = var
        else:
            widget = ttk.Entry(grid, textvariable=var, width=12, justify='right')
            widget.label = '%s. %s' % (num, label) # named in input error messages
            self.entries[key] = widget
        place(widget, row=row, column=2, sticky='e', pady=3)
        extra = {'widget': widget}
        if key in wf.AUTO_FIELDS:
            badge = ttk.Label(grid, font=self.small, width=7, anchor='center')
            place(badge, row=row, column=3, padx=(6, 0))
            reset = ttk.Button(grid, text='↺', width=2, command=lambda: self.use_computed(key))
            place(reset, row=row, column=4, padx=(4, 0))
            extra.update(badge=badge, reset=reset)
        row += 1
        if key in HELP:
            place(ttk.Label(grid, text=HELP[key], font=self.small, foreground=self.colors['muted'], wraplength=330),
                  row=row, column=1, columnspan=4, sticky='w', pady=(0, 4))
            row += 1
        error = ttk.Label(grid, font=self.small, foreground=self.colors['error'], wraplength=330)
        error.grid(row=row, column=1, columnspan=4, sticky='w', pady=(0, 4))
        error.grid_remove()
        extra['error'] = error
        row += 1
        if advanced:
            self.advanced_rows.setdefault(tab_key, []).extend(placed)
        extra['advanced'] = advanced
        self.rows[key] = extra
        self.tab_of[key] = self.tabs[tab_key]
        var.trace_add('write', lambda *args: self.on_edit(key))
        return row

    def build_right(self):
        right = ttk.Frame(self.root, padding=(6, 12, 16, 12))
        right.grid(row=1, column=1, sticky='nsew')
        right.columnconfigure(0, weight=1)

        # Steps
        steps = ttk.LabelFrame(right, text='Run', padding=12)
        steps.grid(row=0, column=0, sticky='ew')
        for c in range(1, 5):
            steps.columnconfigure(c, weight=1, uniform='step')
        self.run_button = ttk.Button(steps, text='Run all steps', default='active', command=lambda: self.run(3))
        self.run_button.grid(row=0, column=0, sticky='n', padx=(0, 12))
        self.root.bind('<Return>', lambda e: self.run(3))
        self.step_buttons, self.step_labels = [], []
        for i, name in enumerate(wf.STEP_BUTTONS):
            button = ttk.Button(steps, text='%d · %s' % (i + 1, name), command=lambda i=i: self.run(i))
            button.grid(row=0, column=i + 1, sticky='ew', padx=3)
            status = ttk.Label(steps, font=self.small, anchor='center')
            status.grid(row=1, column=i + 1, sticky='ew', padx=3, pady=(4, 0))
            self.step_buttons.append(button)
            self.step_labels.append(status)
        self.status = ttk.Label(steps, wraplength=640)
        self.status.grid(row=2, column=0, columnspan=5, sticky='w', pady=(10, 0))

        # Results
        results = ttk.Frame(right)
        results.grid(row=1, column=0, sticky='ew', pady=(12, 0))
        self.cards = []
        for i in range(6):
            results.columnconfigure(i % 3, weight=1, uniform='card')
            box = ttk.LabelFrame(results, padding=(10, 4, 10, 8))
            box.grid(row=i // 3, column=i % 3, sticky='nsew', padx=(0 if i % 3 == 0 else 6, 0), pady=(0, 6))
            box.columnconfigure(0, weight=1)
            value = ttk.Label(box, font=self.big)
            value.grid(row=0, column=0, sticky='w')
            tag = ttk.Label(box, font=self.small, foreground=self.colors['stale'])
            tag.grid(row=0, column=1, sticky='ne')
            detail = ttk.Label(box, font=self.small, foreground=self.colors['muted'])
            detail.grid(row=1, column=0, columnspan=2, sticky='w')
            self.cards.append((box, value, detail, tag))
        for key in RESULT_KEYS:
            self.entries[key] = ui.ResultField(StringVar(self.root, value='N/A'))
            self.entries[key].var.trace_add('write', lambda *args: self.refresh())

        # Plots
        plots = ttk.LabelFrame(right, text='Plots to show (each opens in its own window)', padding=12)
        plots.grid(row=2, column=0, sticky='ew', pady=(6, 0))
        for column, (title, items) in enumerate((('Swing', SWING_PLOTS), ('Ball flight', BALL_PLOTS))):
            plots.columnconfigure(column, weight=1)
            box = ttk.Frame(plots)
            box.grid(row=0, column=column, sticky='nw')
            ttk.Label(box, text=title.upper(), font=self.small, foreground=self.colors['muted']).grid(
                row=0, column=0, columnspan=2, sticky='w', pady=(0, 4))
            for n, (key, label, on) in enumerate(items):
                var = BooleanVar(self.root, value=on)
                self.entries[key] = var
                ttk.Checkbutton(box, text=label, variable=var).grid(row=1 + n // 2, column=n % 2, sticky='w', padx=(0, 16), pady=1)

    # --- Behavior -------------------------------------------------------------------------------

    def on_edit(self, key):
        if self.busy:
            return
        self.message = None
        stage = STAGE[key]
        if key in wf.AUTO_FIELDS:
            if self.vars[key].get().strip() == '':
                self.flow.use_computed(key, stage) # cleared: let its step compute it again
            else:
                self.flow.auto_field_edited(key, stage)
        else:
            self.flow.input_changed(stage)
        self.refresh()

    def use_computed(self, key):
        value = self.flow.use_computed(key, STAGE[key])
        self.busy = True
        try:
            self.vars[key].set(value)
        finally:
            self.busy = False
        self.refresh()

    def errors(self):
        return wf.check_inputs({k: v.get() for k, v in self.vars.items()}, NUMERIC_KEYS)

    def run(self, upto):
        if self.running:
            return
        errors = self.errors()
        if errors:
            first = next(f[0] for f in FIELDS if f[0] in errors)
            self.notebook.select(self.tab_of[first])
            if self.rows[first]['advanced'] and not self.advanced_open[self.tab_key(first)]:
                self.toggle_advanced(self.tab_key(first))
            self.rows[first]['widget'].focus_set()
            self.message = ('Fix the highlighted input first.', 'error')
            self.refresh()
            return
        self.running = True
        self.message = None
        optimize = pl.Optimize_Q_beta_2 if self.vars['Optimizer'].get() == 'Complete' else pl.Optimize_Q_beta
        steps = (optimize, pl.Plot, pl.get_ball_velocity, pl2.Plot)
        try:
            with ui.batch_plots():
                for i in self.flow.plan(upto):
                    if self.flow.skips(i):
                        self.flow.skipped(i)
                        continue
                    self.active = i
                    self.refresh()
                    self.root.update_idletasks()
                    kept = {k: self.vars[k].get() for k in self.flow.manual}
                    self.busy = True
                    try:
                        ok = steps[i](self.entries)
                        outputs = {k: self.vars[k].get() for k, s in wf.AUTO_FIELDS.items() if s == i}
                        for k, v in kept.items(): # a step never overwrites a value typed by hand
                            self.vars[k].set(v)
                    finally:
                        self.busy = False
                    if not ok:
                        self.message = ('Step %d (%s) stopped; see the error message. Later steps did not run.'
                                        % (i + 1, wf.STEP_LABELS[i]), 'error')
                        break
                    self.flow.finished(i, outputs)
        finally:
            self.active = None
            self.running = False
            self.refresh()

    def tab_key(self, key):
        return next(f[5] for f in FIELDS if f[0] == key)

    def reset(self):
        plt.close('all')
        self.busy = True
        try:
            for key, num, label, default, *rest in FIELDS:
                self.vars[key].set(default)
            for key in RESULT_KEYS:
                self.entries[key].var.set('N/A')
            for key, label, on in SWING_PLOTS + BALL_PLOTS:
                self.entries[key].set(on)
        finally:
            self.busy = False
        self.flow.reset()
        self.message = None
        self.refresh()

    # --- Display --------------------------------------------------------------------------------

    def refresh(self):
        c = self.colors
        errors = self.errors()
        for key, extra in self.rows.items():
            if key in errors and (not extra['advanced'] or self.advanced_open[self.tab_key(key)]):
                extra['error'].configure(text=errors[key])
                extra['error'].grid()
            else:
                extra['error'].grid_remove()
        for tab_key, title in TABS:
            count = sum(1 for k in errors if self.tab_key(k) == tab_key)
            self.notebook.tab(self.tabs[tab_key], text=title + ('  (%d to fix)' % count if count else ''))

        # Steps
        texts = {wf.IDLE: ('Not run', c['muted']), wf.DONE: ('✓ Up to date', c['ok']),
                 wf.STALE: ('Stale: inputs changed', c['stale']), wf.MANUAL: ('Skipped: typed by hand', c['manual'])}
        for i, label in enumerate(self.step_labels):
            text, color = ('Running…', c['ok']) if i == self.active else texts[self.flow.states[i]]
            label.configure(text=text, foreground=color)
        state = ['disabled'] if self.running else ['!disabled']
        for button in self.step_buttons + [self.run_button]:
            button.state(state)
        if self.active is not None:
            text, kind = 'Step %d of 4 · %s' % (self.active + 1, wf.STEP_ACTIVITY[self.active]), 'ok'
        elif self.message:
            text, kind = self.message
        elif errors:
            text, kind = '%d input%s to fix before running.' % (len(errors), '' if len(errors) == 1 else 's'), 'error'
        else:
            text, kind = self.flow.status()
        self.status.configure(text=text, foreground=c.get(kind, c['muted']))

        # In-between values: auto, typed by hand, or stale
        for key, step in wf.AUTO_FIELDS.items():
            extra = self.rows[key]
            if key in self.flow.manual:
                extra['badge'].configure(text='manual', foreground=c['manual'])
                extra['reset'].grid()
            else:
                stale = self.flow.states[step] == wf.STALE and self.vars[key].get().strip() not in ('', 'N/A')
                extra['badge'].configure(text='stale' if stale else 'auto', foreground=c['stale'] if stale else c['ok'])
                extra['reset'].grid_remove()

        # Results
        values = {k: self.entries[k].get() for k in RESULT_KEYS}
        values.update({k: self.vars[k].get() for k in wf.AUTO_FIELDS})
        for (box, value, detail, tag), (label, text, sub, kind) in zip(self.cards, wf.result_cards(values, self.flow)):
            box.configure(text=label)
            value.configure(text=text, foreground=c['muted'] if kind == 'stale' else '')
            detail.configure(text=sub)
            tag.configure(text='stale' if kind == 'stale' else '')

if __name__ == '__main__':

   root = Tk()
   root.title("The Simple Golf Simulator (Copyright @ 2026 C.-C. Chiang)")

   # Window icon (PNG needs Tk 8.6+; skip silently on older Tk)
   icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'assets', 'logo.png')
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

   panel = Panel(root)
   entries = panel.entries

   root.update_idletasks()
   root.minsize(1000, 640)
   root.geometry("1220x800")

   root.mainloop()
