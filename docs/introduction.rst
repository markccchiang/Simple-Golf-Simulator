Introduction
============

The Physics behind the golf sport has been studied and discussed in many papers or books.
Many of studies are just focused in one special topic, maybe we could not get the whole picture
how much does it affect our golf performance. Also, these theories or experiments might be not
easy to be understood by public. In this report I would like to re-examine and clarify some
theories. I also intend to combine these theories in a calculation software, which makes them
easy for us to use, evaluate and apply in the real world. The Simple Golf Simulator calculates
the swing of a golf club, the launch speed of a golf ball which given by a clubhead, and the flight
trajectory of a golf ball.

In this report, the swing of golf club is explained in :doc:`swing`, which includes the two-rod
model theory and the numerical solutions for this model. The trajectory of golf ball is discussed
in :doc:`trajectory`, which includes the aerodynamic forces on a golf ball and the numerical solution for
the flight trajectory. The user's guide of Simple Golf Simulator is in :doc:`users_guide`. The summary is
in :doc:`summary`, where some works to be done are listed in order to make this simulator more practical.

The numerical solution used in this simulator is the Runge-Kutta method, which is an explicit
iterative method often used in temporal discretization for the approximation of solutions
of differential equations. It is suitable for golf ball trajectory calculation. However, for the golf
swing, since there are many parameters in the model, we have to deal with this method carefully.
Three kinds of numerical solutions are listed in :ref:`numerical-solutions`, and if they agree with each other, then we
can safely use it under such conditions.

The numerical solutions of fluid dynamics for a golf ball dimple is another big subject which
is not included in this report. Usually it relies on Finite Element Method or Finite Volume
Method and a huge computational work to solve the model.
