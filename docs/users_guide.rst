User's Guide
============

Installation
------------

The Simple Golf Simulator is written in Python. Before running the program, install the
required packages:

.. code-block:: bash

   pip install matplotlib numpy

Python 3.12+ is recommended. On Linux, ``tkinter`` may need to be installed separately:

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt-get install python3-tk

   # Fedora
   sudo dnf install python3-tkinter

The main files are ``AppFunc.py``, ``AppFunc2.py``, ``BasicFunc.py``,
``BasicFunc2.py``, ``Plot.py``, ``Plot2.py`` and ``Main.py``. All must be in the same
directory. The case files ``Case1.py`` through ``Case10.py`` are standalone demonstration scripts.

To start the main program:

.. code-block:: bash

   python Main.py

The Main Control Panel
----------------------

The panel has two columns: the left column is for golf swing simulation, and the right column
is for golf ball trajectory simulation. Default values are pre-filled. Users follow the item numbers
from top to bottom, left to right, step-by-step.

**Color coding:**

- **White fields** -- user-editable parameters
- **Yellow fields** -- auto-filled by clicking yellow buttons (can also be manually set)
- **Blue fields** -- simulation results, auto-filled by clicking blue buttons

Golfer Parameters (I)
^^^^^^^^^^^^^^^^^^^^^^

1. **Gender** -- Male, Female or Average. Affects the percentages of weights for arm segments.
2. **Weight (kg)** -- The golfer's weight.
3. **Shoulder radius (m)** -- :math:`R_S`, the shoulder radius.
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
19. **Wrist-cock torque (N-m)** -- :math:`Q_\beta`, positive is clockwise. Auto-filled by optimization.
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

24. **Simulation method** -- Solution 1, 2 or 3 (default: Solution 3).
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
40. **Launch speed (m/s)** -- Auto-calculated from clubhead velocity and COR.
41. **Launch elevation angle (degree)** -- Auto-calculated from impact angle + loft.
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
