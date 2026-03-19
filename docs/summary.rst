Summary
=======

The Simple Golf Simulator should be verified by experimental data. There are many variables
in the golf swing model and golf ball flight trajectory. They can be very different with different
golfers, clubs, swing types and golf balls they use. However through the simulation and analysis
of the data, we can understand the mechanism behind it and provide valuable information to
optimize the performance for a golfer.

Future Work: Golf Club Swing Model
------------------------------------

- The functions of arm and wrist-cock torques with respect to time during the swing
  may be different for golfers. The torque model may need to be re-modeled.
- The function of arm bending angle for Type II (full-length) backswing may be different
  for golfers and may require a different model.
- The flexibility of a club shaft may need to be considered.
- The first and second moments of golfer's arm or club may need to be re-calculated for
  special cases.

Future Work: Golf Ball Flight Trajectory
-----------------------------------------

- The drag and lift coefficients :math:`C_D` and :math:`C_L` as functions of the ratio of rotational speed
  to stream speed and Reynolds number should be obtained from experimental data.
- The asymmetry of carry and time for a golf ball may need to be considered.
- The bouncing and rolling of a golf ball after touching the ground may need to be considered.

Additionally, the interaction between the clubhead and golf ball may need more detailed modeling
beyond the simple coefficient of restitution equation.
