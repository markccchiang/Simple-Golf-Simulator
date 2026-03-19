The Trajectory of Golf Ball
===========================

Aerodynamic Forces
------------------

The trajectory of a golf ball is determined by its launch speed, angle, direction and aerodynamic
forces. The drag force :math:`F_D` is caused by air friction and backward turbulence. The
lift force :math:`F_L` (Magnus force) is caused by the rotation of a ball, based on Bernoulli's principle.
These forces are proportional to the cross-sectional area of a ball
:math:`A = \pi R^2`, air density :math:`\rho_\text{air}` and the square of stream velocity :math:`U^2`:

.. math::

   F_D = C_D \cdot A \cdot \rho_\text{air} \cdot \frac{U^2}{2}

.. math::

   F_L = C_L \cdot A \cdot \rho_\text{air} \cdot \frac{U^2}{2}

where :math:`R` is the radius of a ball. The stream velocity is:

.. math::

   \vec{U} = -\vec{v}_\text{ball} + \vec{v}_\text{wind}

:math:`C_D` and :math:`C_L` are the coefficients of drag and lift, respectively, and they are usually changed
with the ratio of the circumferential (rotational) speed :math:`|\vec{V}|` of a ball to the stream speed :math:`|\vec{U}|`,
where :math:`\vec{V} = \vec{w} \times \vec{R}`.
Studies of the effects of :math:`|\vec{V}|/|\vec{U}|` and Reynolds number on :math:`C_D` and :math:`C_L`
can be found in [Aoki2010]_, [Kharlamov2007]_, and [Penner2003]_.

The Reynolds number is defined as:

.. math::

   Re = \frac{\rho_\text{air} \cdot |\vec{U}| \cdot D}{\mu_\text{air}}

where :math:`\mu_\text{air}` is the dynamic viscosity of air and :math:`D = 2R` is the diameter of the ball.

Mathematical Formula and Solution
-----------------------------------

Let the standard basis of vectors :math:`(\hat{x}, \hat{y}, \hat{z})`, where :math:`\hat{x}` and :math:`\hat{y}` are
orthogonal unit vectors in horizontal directions, and :math:`\hat{z}` is a unit vector in vertical direction.

The velocity of a golf ball in three dimensions is:

.. math::

   v_{\text{ball},x} &= v_\text{ball} \cdot \cos\theta \cdot \cos\varphi \\
   v_{\text{ball},y} &= v_\text{ball} \cdot \cos\theta \cdot \sin\varphi \\
   v_{\text{ball},z} &= v_\text{ball} \cdot \sin\theta

where :math:`\theta` and :math:`\varphi` are the elevation and direction angles.

Similarly, the wind velocity is:

.. math::

   v_{\text{wind},x} &= v_\text{wind} \cdot \cos\theta_\text{wind} \cdot \cos\varphi_\text{wind} \\
   v_{\text{wind},y} &= v_\text{wind} \cdot \cos\theta_\text{wind} \cdot \sin\varphi_\text{wind} \\
   v_{\text{wind},z} &= v_\text{wind} \cdot \sin\theta_\text{wind}

The rotational angular velocity is:

.. math::

   w_x &= w \cdot \cos\theta_w \cdot \cos\varphi_w \\
   w_y &= w \cdot \cos\theta_w \cdot \sin\varphi_w \\
   w_z &= w \cdot \sin\theta_w

The drag force direction is along :math:`\vec{U}` and the lift force direction is the cross product of
:math:`\vec{U}` and :math:`\vec{w}`:

.. math::

   \frac{\vec{F}_D}{|F_D|} = \frac{\vec{U}}{|\vec{U}|}, \qquad
   \frac{\vec{F}_L}{|F_L|} = \frac{\vec{U}}{|\vec{U}|} \times \frac{\vec{w}}{|\vec{w}|}

The gravitation is :math:`\vec{F}_G = -mg\hat{z}`. The total acceleration on the ball is:

.. math::

   a_x &= \frac{1}{m}(F_{D,x} + F_{L,x}) \\
   a_y &= \frac{1}{m}(F_{D,y} + F_{L,y}) \\
   a_z &= \frac{1}{m}(F_{D,z} + F_{L,z}) - g

The ball velocity is integrated step-by-step with the fourth-order Runge-Kutta method
(time step :math:`h = 0.001` sec), and the position is calculated as:

.. math::

   x_{n+1} = x_n + \frac{v_{x,n} + v_{x,n+1}}{2}h

(and similarly for :math:`y` and :math:`z`).

Simulation Studies
------------------

The basic settings of parameters for golf ball trajectory simulations:

.. list-table:: Basic parameters for golf ball trajectory simulations
   :header-rows: 1
   :widths: 60 20

   * - Parameter
     - Value
   * - Ball mass (kg)
     - 0.0458
   * - Ball diameter (m)
     - 0.0428
   * - Drag coefficient :math:`C_D`
     - 0.285
   * - Lift coefficient :math:`C_L`
     - 0.1
   * - Launch speed (m/s)
     - 45
   * - Launch elevation angle :math:`\theta` (degree)
     - 15
   * - Launch direction angle :math:`\varphi` (degree)
     - 0
   * - Spin elevation angle :math:`\theta_w` (degree)
     - 0
   * - Spin direction angle :math:`\varphi_w` (degree)
     - -90
   * - Air density (kg/m\ :sup:`3`)
     - 1.2
   * - Wind speed (m/s)
     - 0

Case 7: The Effect of Drag and Lift Coefficients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Varying :math:`C_D = 0.1 \sim 0.6` and :math:`C_L = 0 \sim 0.3`:
the flight distance is roughly proportional to :math:`1/C_D` and :math:`C_L`
(for :math:`\theta_w = 0^\circ` and :math:`\varphi_w = -90^\circ`).

Case 8: The Effect of Launch Elevation Angle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Varying the golf ball launch elevation angle :math:`\theta = 0^\circ \sim 90^\circ` with different
:math:`C_D` and :math:`C_L` values. There exists an optimal launch angle that maximizes flight distance,
which depends on the aerodynamic coefficients.

Case 9: The Effect of Spin Direction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Varying the golf ball spin direction :math:`\theta_w = 0^\circ \sim 360^\circ` with :math:`\varphi_w = -90^\circ`.
The spin direction determines the lateral deviation (draw/fade) of the ball trajectory.

Case 10: The Effect of Wind
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding wind speed of 5 m/s in directions :math:`\varphi_\text{wind} = 0^\circ, 90^\circ, 180^\circ, 270^\circ`.
Wind significantly affects both the distance and lateral deviation of the ball trajectory,
with headwind reducing distance and tailwind increasing it.
