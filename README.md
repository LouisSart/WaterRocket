# WaterRocket

Simulation of the emptying speed of a water tank when put under pressure. The water jet at the bottom can be used as propulsion to make a water rocket.  

![equation](rocket.jpg)

Bernoulli's theorem associated with conservation of mass allows the following relations between $v$, $z$, and $p$:

$$\begin{align*}
p(t)&= \frac{p_0 (H - z_0)}{H-z(t)}\\
v(t)&= -\frac{S}{s}\frac{dz}{dt}\\
p(t)&-p_a + \frac{1}{2} \rho \left( (\frac{dz}{dt})^2 - v^2) \right) + \rho g z = 0
\end{align*}$$

Which yields the following non-linear ODE on z: $(\frac{dz}{dt})^2(\frac{S^2}{s^2}-1) = \frac{2}{\rho}(p(t)-p_a) + 2gz$ and then taking the negative root (because the water level is decreasing as the tank drains) we get:

$$\frac{dz}{dt} = - \sqrt{\frac{2}{\beta}\frac{p(z(t))-p_a}{\rho} + 2gz(t)} = F(t,z(t))$$  

where $\beta = (\frac{S^2}{s^2}-1)$. We can then use explicit Euler's method to solve this ODE with any starting parameters:

$$z_{n+1}=z_n + \Delta t \ F(t_n, z_n)$$

## Results

For a given set of inital conditions and tank dimensions, $z_n$ is computed until one of these 2 conditions are met:

1. The water level has reached the bottom of the tank
2. The water level speed comes close to zero (meaning hydrostatic equilibrium is reached)

If the term $\frac{p(z_n)-p_a}{\rho} + 2gz_n$ becomes negative, then that means the water level is passing sub hydrostatic equilibrium, which is physically impossible. When this happens the simulation is stopped and the user is informed that the time step should be reduced to ensure physical consistency.

### Impact of the initial water height in tank

![water_level](water_level.png)

The figure above shows the water level and ejection speed over the time of the simulation for a starting pressure of 2 bars and three different initial water levels. When the starting water height is half the tank's height, then the tank fully empties as the tank pressure reaches atmospheric pressure. If we increase the water level, the pressures balance out before the tank is emptied. On the other hand, a less full water tank gets emptied faster, and keeps a higher internal pressure up to the end.