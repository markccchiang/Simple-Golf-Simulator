User's Guide
============

Installation
------------

The Simple Golf Simulator is written in Python. The recommended way to install it is with
`uv <https://docs.astral.sh/uv/>`_, which installs Python 3.12 (including ``tkinter``) and all
required packages into a local ``.venv``:

.. code-block:: bash

   uv sync

Alternatively, install the required packages with pip (Python 3.12+ recommended):

.. code-block:: bash

   pip install matplotlib numpy

With pip on Linux, ``tkinter`` may need to be installed separately:

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt-get install python3-tk

   # Fedora
   sudo dnf install python3-tkinter

The program files are in ``src/``: ``AppFunc.py``, ``AppFunc2.py``, ``BasicFunc.py``,
``BasicFunc2.py``, ``Plot.py``, ``Plot2.py``, ``UIFunc.py`` and ``Main.py``. The case files ``Case1.py``
through ``Case10.py`` in ``examples/`` are standalone demonstration scripts; run one with, for example,
``uv run examples/Case1.py`` (or ``python examples/Case1.py``).

To start the main program:

.. code-block:: bash

   uv run src/Main.py     # or, with pip: python src/Main.py

The Main Panel
--------------

The window has two parts. On the left, the inputs are grouped in three tabs: **Golfer & club**,
**Swing** and **Ball & conditions**. On the right are the steps to run, the results and the choice of
plots. Default values are pre-filled, and each input keeps the item number used in this guide.

Running the Simulation
^^^^^^^^^^^^^^^^^^^^^^

A full run has four steps, each using the results of the ones before it:

1. **Optimize wrist torque** -- finds the wrist-cock torque (item 19) that brings the wrist-cock angle
   to its target at impact (item 13).
2. **Simulate swing** -- computes the clubhead speed and angle at impact.
3. **Launch conditions** -- computes the launch speed and elevation (items 40 and 41) from the impact.
4. **Ball flight** -- computes the carry distance, apex and flight time.

Click **Run all steps** (or press Return) to run them in order, or click a single step to run it
together with any earlier step it needs. The line under each step shows its state:

- **Not run** -- the step has not run yet.
- **Up to date** -- the step ran with the current inputs.
- **Stale: inputs changed** -- an input the step uses changed after it ran. Its results stay visible,
  greyed and marked *stale*, until the next run; only the stale steps run again.
- **Skipped: typed by hand** -- the value the step computes was typed in (see below).

The pointer shows a busy cursor while the steps run, and the line below the steps says which step is
running. If a step fails, the later steps do not run and a message explains why (see :ref:`error-messages`).

Values the Steps Fill In
^^^^^^^^^^^^^^^^^^^^^^^^

The wrist-cock torque (item 19) and the launch speed and elevation (items 40 and 41) are filled in by the
steps, marked *auto*. They can also be typed in: the field is then marked *manual* and the step that would
compute it is skipped, which lets you try a torque by hand or study the ball flight on its own. Click
**↺** next to the field, or clear it, to let the step compute the value again.

Checking the Inputs
^^^^^^^^^^^^^^^^^^^

Inputs are checked as you type: a problem is shown in red under the field, and the tab's title shows how
many inputs need fixing. The steps do not run until every input is valid.

Inputs: Golfer & club
^^^^^^^^^^^^^^^^^^^^^

- **1. Gender** -- Male, Female or Average. Affects the percentages of weights for arm segments.
- **2. Weight (kg)** -- The golfer's weight.
- **3. Shoulder radius (m)** -- :math:`R_S`, the shoulder radius. Must be smaller than the arm length (item 4).
- **4. Arm length (m)** -- :math:`R_A`, the arm length.
- **5. Head mass (kg)** -- Mass of the clubhead.
- **6. Shaft mass (kg)** -- Mass of the club shaft.
- **7. Head length (m)** -- Length of the clubhead :math:`L_\text{head}`.
- **8. Shaft length (m)** -- Length of the shaft :math:`L_\text{shaft}`.

Inputs: Swing
^^^^^^^^^^^^^

*Swing*

- **9. Swing plane angle (degree)** -- The angle :math:`\varphi`.
- **10. Initial arm angle (degree)** -- Start angle :math:`\theta_0`.
- **12. Initial wrist-cock angle (degree)** -- Start angle :math:`\beta_0`.
- **16. Swing type** -- Type I (restricted backswing) or Type II (full-length backswing).
- **24. Solver** -- Solution 1, 2, 3 or 4 (default: Solution 4). Solution 4 is the most accurate and
  the fastest; Solutions 1--3 are the original methods, kept for comparison. See :ref:`numerical-solutions`.

*Torques*

- **17. Arm torque (N-m)** -- :math:`Q_\alpha`, positive is counter-clockwise.
- **19. Wrist-cock torque (N-m)** -- :math:`Q_\beta`, positive is clockwise. Filled in by step 1, or typed in.
- **20. Wrist torque starts at arm angle (degree)** -- The arm angle at which the wrist-cock torque starts.
  Must not exceed :math:`\theta_0` (item 10).

*Wrist-torque search* (used by step 1)

- **13. Target wrist-cock angle at impact (degree)** -- Final angle :math:`\beta_f` at impact.
- **22. Lowest torque to try (N-m)** -- Lower bound of the search.
- **23. Highest torque to try (N-m)** -- Upper bound of the search.

- **Search** -- *Fast* scans from the highest torque down to the result; *Complete* also scans past the
  result for a thorough analysis (slower).

*Advanced* (click to show)

- **11. Impact arm angle (degree)** -- Final angle :math:`\theta_f` at impact.
- **14. Horizontal hand acceleration (m/s**\ :sup:`2`\ **)** -- :math:`a_x`.
- **15. Vertical hand acceleration (m/s**\ :sup:`2`\ **)** -- :math:`a_y` (positive is toward the ground).
- **18. Arm torque rise time (sec)** -- :math:`\tau_{Q_\alpha}`.
- **21. Wrist torque rise time (sec)** -- :math:`\tau_{Q_\beta}`.

Inputs: Ball & conditions
^^^^^^^^^^^^^^^^^^^^^^^^^

*Golf ball*

- **30. Mass (kg)** -- Golf ball mass.
- **31. Diameter (m)** -- Golf ball diameter.
- **32. Coefficient of restitution** -- COR of the club-ball impact.
- **33. Drag coefficient** -- :math:`C_D`.
- **34. Lift coefficient** -- :math:`C_L`.

*Launch*

- **39. Clubhead loft (degree)** -- Elevation angle given to the ball.
- **40. Launch speed (m/s)** -- Filled in by step 3 from the clubhead speed and COR, or typed in.
- **41. Launch elevation (degree)** -- Filled in by step 3 from the impact angle and loft, or typed in.
- **42. Launch direction (degree)** -- :math:`\varphi`.
- **43. Spin elevation (degree)** -- :math:`\theta_w`.
- **44. Spin direction (degree)** -- :math:`\varphi_w`.

*Wind*

- **36. Wind speed (m/s)** -- Absolute value.
- **37. Wind elevation (degree)** -- :math:`\theta_\text{wind}`.
- **38. Wind direction (degree)** -- :math:`\varphi_\text{wind}`.

*Advanced* (click to show)

- **35. Air density (kg/m**\ :sup:`3`\ **)** -- Depends on weather and altitude.
- **45. Landing height vs. tee (m)** -- Height of the landing point relative to the launch point (default: 0).

Results
^^^^^^^

The results are shown in six cards:

- **Wrist-cock torque** -- item 19, found by the optimizer or entered by hand.
- **Clubhead speed at impact** -- in m/s and mph, with its systematic error: the change when the
  wrist-cock torque changes by :math:`\pm 0.01` N-m.
- **Clubhead angle at impact** -- the elevation angle :math:`\theta_{\vec{V_C}}`, with its systematic error.
- **Launch** -- the launch speed and elevation (items 40 and 41).
- **Carry distance** -- the flight distance in the X-Y plane, in meters and yards (negative means behind
  the golfer), and the lateral distance of the landing point.
- **Apex and flight time** -- the highest point of the flight and the time to land.

Plots
^^^^^

Choose the plots to show under **Plots to show**; each opens in its own window when its step runs, and
replaces that step's earlier plots.

- *Swing* -- swing tracks, angles, angular velocities, angular accelerations, clubhead speed, torques,
  arm length, 1st and 2nd moments, and the wrist-torque search (:math:`\beta` vs :math:`-Q_\beta`).
- *Ball flight* -- side view (X-Z), top view (X-Y), rear view (Y-Z) and 3D.

.. _error-messages:

Error Messages
--------------

Problems are reported in a dialog instead of stopping the program.

**Input Error** -- something to fix in the panel:

- *"<item>" must be a number* -- the named field contains text that is not a number.
- *... is not set yet. Run step N (...) first* -- a value a step fills in is missing; run that step,
  or type the value in.
- *The shoulder radius (item 3) must be greater than 0 and smaller than the arm length (item 4).*
- *No wrist-cock torque in the allowed range reaches the target* -- no torque between items 22 and 23
  brings the wrist-cock angle to the impact target (item 13). The message says whether to lower item 22
  or raise item 23. Item 19 stays empty until the optimization succeeds.
- *The minimum wrist-cock torque (item 22) must not be greater than the maximum (item 23).*

Inputs that are not numbers, a shoulder radius not smaller than the arm length, a wrist torque start angle
above the initial arm angle, and a torque range whose lowest value is above its highest are also shown in
red under the field as you type (see Checking the Inputs above).

**Simulation Error** -- the inputs are valid numbers, but the simulation cannot produce a result:

- *Swing did not reach the impact arm angle within 2.0 sec* -- the arm torque (item 17) is too weak
  to bring the arm down to the impact angle (item 11). Increase the arm torque.
- *Ball never reaches the target altitude* -- the landing height (item 45) is higher than the top of
  the ball's flight. Lower the landing height or increase the launch speed.
- *Ball is still in flight after 100 sec* -- the landing height (item 45) is too far below the
  launch point.
- *Launch speed must be positive.*
- *The simulation could not be computed with these inputs* -- the golfer and club dimensions are not
  physically consistent for the chosen swing type. Check items 3, 4 and 16; Type II needs a
  shoulder radius well below the arm length.
