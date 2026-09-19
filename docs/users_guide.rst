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

The main files are ``AppFunc.py``, ``AppFunc2.py``, ``BasicFunc.py``,
``BasicFunc2.py``, ``Plot.py``, ``Plot2.py``, ``UIFunc.py`` and ``Main.py``. All must be in the same
directory. The case files ``Case1.py`` through ``Case10.py`` are standalone demonstration scripts.

To start the main program:

.. code-block:: bash

   uv run Main.py     # or, with pip: python Main.py

The Main Control Panel
----------------------

The panel has two columns: the left column is for golf swing simulation, and the right column
is for golf ball trajectory simulation. Default values are pre-filled. Users follow the item numbers
from top to bottom, left to right, step-by-step.

**Field types:**

- **Editable fields** -- input parameters, pre-filled with default values.
- **Read-only fields** (items 19, 26--29, 40, 41 and 47--49) -- show "N/A" until they are filled
  in by clicking the buttons. They cannot be typed into.

**Workflow:** each step uses the results of the previous one, so click the buttons in this order:

1. **Optimize wrist-cock torque** (fast or complete) -- fills item 19.
2. **Simulate / Plot Golf Swing** -- fills items 26--29.
3. **Calculate launch speed and elevation angle from impact** -- fills items 40 and 41.
4. **Simulate / Plot Ball Trajectory** -- fills items 47--49.

If a step is skipped, an error message names the button to click first. See :ref:`error-messages`.

Golfer Parameters (I)
^^^^^^^^^^^^^^^^^^^^^^

1. **Gender** -- Male, Female or Average. Affects the percentages of weights for arm segments.
2. **Weight (kg)** -- The golfer's weight.
3. **Shoulder radius (m)** -- :math:`R_S`, the shoulder radius. Must be smaller than the arm length (item 4).
4. **Arm length (m)** -- :math:`R_A`, the arm length.

Club Parameters (II)
^^^^^^^^^^^^^^^^^^^^^

5. **Head mass (kg)** -- Mass of the clubhead.
6. **Shaft mass (kg)** -- Mass of the club shaft.
7. **Head length (m)** -- Length of the clubhead :math:`L_\text{head}`.
8. **Shaft length (m)** -- Length of the shaft :math:`L_\text{shaft}`.

Swing Conditions (III)
^^^^^^^^^^^^^^^^^^^^^^

9. **Swing plane angle (degree)** -- The angle :math:`\varphi`.
10. **Initial arm angle (degree)** -- Start angle :math:`\theta_0`.
11. **Impact arm angle (degree)** -- Final angle :math:`\theta_f` at impact.
12. **Initial wrist-cock angle (degree)** -- Start angle :math:`\beta_0`.
13. **Impact wrist-cock angle (degree)** -- Final angle :math:`\beta_f` at impact.
14. **Horizontal acceleration (m/s**\ :sup:`2`\ **)** -- :math:`a_x`.
15. **Vertical acceleration (m/s**\ :sup:`2`\ **)** -- :math:`a_y` (positive is toward the ground).
16. **Swing type** -- Type I (restricted backswing) or Type II (full-length backswing).

Swing Torques (IV)
^^^^^^^^^^^^^^^^^^

17. **Arm torque (N-m)** -- :math:`Q_\alpha`, positive is counter-clockwise.
18. **Rising time of arm torque (sec)** -- :math:`\tau_{Q_\alpha}`.
19. **Wrist-cock torque (N-m)** -- :math:`Q_\beta`, positive is clockwise. Read-only; filled by the optimization buttons.
20. **Starting arm angle for wrist-cock torque (degree)** -- Must be :math:`\leq \theta_0` (item 10).
21. **Rising time of wrist-cock torque (sec)** -- :math:`\tau_{Q_\beta}`.
22. **Minimum wrist-cock torque (N-m)** -- Lower bound for optimization.
23. **Maximum wrist-cock torque (N-m)** -- Upper bound for optimization.

**Optimization buttons:**

- **Fast** -- Scans wrist-cock torque from maximum to the optimized value.
- **Complete** -- Scans from maximum to 10 N-m beyond the optimized value for thorough analysis.

The optimized value is filled into item 19. Plots of :math:`\beta` vs :math:`-Q_\beta` are shown.

Simulate the Swing (V)
^^^^^^^^^^^^^^^^^^^^^^^

24. **Simulation method** -- Solution 1, 2, 3 or 4 (default: Solution 4). Solution 4 is the most accurate and
    the fastest; Solutions 1--3 are the original methods, kept for comparison. See :ref:`numerical-solutions`.
25. **Results to plot** -- Check any combination of: Tracks, Angles, Angular velocities,
    Angular accelerations, Clubhead velocity, Torques, Arm length, 1st and 2nd moments.

**Swing Results:**

26. **Clubhead impact velocity (m/s)**
27. **Systematic error of velocity (m/s)** -- Change when :math:`Q_\beta \pm 0.01` N-m.
28. **Clubhead impact angle (degree)** -- Elevation angle :math:`\theta_{\vec{V_C}}`.
29. **Systematic error of angle (degree)** -- Change when :math:`Q_\beta \pm 0.01` N-m.

Golf Ball Parameters (VI)
^^^^^^^^^^^^^^^^^^^^^^^^^^

30. **Mass (kg)** -- Golf ball mass.
31. **Diameter (m)** -- Golf ball diameter.
32. **COR** -- Coefficient of restitution.
33. **Drag coefficient** -- :math:`C_D`.
34. **Lift coefficient** -- :math:`C_L`.

Environmental Conditions (VII)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

35. **Air density (kg/m**\ :sup:`3`\ **)** -- Depends on weather and altitude.
36. **Wind speed (m/s)** -- Absolute value.
37. **Wind elevation angle (degree)** -- :math:`\theta_\text{wind}`.
38. **Wind direction angle (degree)** -- :math:`\varphi_\text{wind}`.

Launch Conditions (VIII)
^^^^^^^^^^^^^^^^^^^^^^^^^

39. **Loft angle of clubhead (degree)** -- Elevation angle given to the ball.
40. **Launch speed (m/s)** -- Read-only; calculated from clubhead velocity and COR.
41. **Launch elevation angle (degree)** -- Read-only; calculated from impact angle + loft.
42. **Launch direction angle (degree)** -- :math:`\varphi`.
43. **Spin elevation angle (degree)** -- :math:`\theta_w`.
44. **Spin direction angle (degree)** -- :math:`\varphi_w`.

**Calculate button** computes items 40 and 41 from the swing results and loft angle.

Ball Trajectory (IX)
^^^^^^^^^^^^^^^^^^^^^

45. **Target altitude (m)** -- Altitude relative to launch point (default: 0).
46. **Results to plot** -- X-Z, X-Y, Y-Z, or X-Y-Z (3D plot).

**Trajectory Results:**

47. **Drop location X (m)**
48. **Drop location Y (m)**
49. **Flight distance in X-Y plane (m)** -- Negative means behind the golfer.

.. _error-messages:

Error Messages
--------------

Problems are reported in a dialog instead of stopping the program.

**Input Error** -- something to fix in the panel:

- *"<item>" must be a number* -- the named field contains text that is not a number.
- *Item(s) ... are not set yet. Click "..." first* -- a step of the workflow was skipped; click the
  named button, then try again.
- *The shoulder radius (item 3) must be greater than 0 and smaller than the arm length (item 4).*
- *No wrist-cock torque in the allowed range reaches the target* -- no torque between items 22 and 23
  brings the wrist-cock angle to the impact target (item 13). The message says whether to lower item 22
  or raise item 23. Item 19 stays "N/A" until the optimization succeeds.
- *The minimum wrist-cock torque (item 22) must not be greater than the maximum (item 23).*

**Simulation Error** -- the inputs are valid numbers, but the simulation cannot produce a result:

- *Swing did not reach the impact arm angle within 2.0 sec* -- the arm torque (item 17) is too weak
  to bring the arm down to the impact angle (item 11). Increase the arm torque.
- *Ball never reaches the target altitude* -- the target altitude (item 45) is higher than the top of
  the ball's flight. Lower the target altitude or increase the launch speed.
- *Ball is still in flight after 100 sec* -- the target altitude (item 45) is too far below the
  launch point.
- *Launch speed must be positive.*
- *The simulation could not be computed with these inputs* -- the golfer and club dimensions are not
  physically consistent for the chosen swing type. Check items 3, 4 and 16; Type II needs a
  shoulder radius well below the arm length.
