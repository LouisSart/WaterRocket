from main import *

def midpoint(x, y):
    # Integrate y with midpoint method
    ret = 0.0
    for i in range(len(y) - 1):
        mid = (y[i + 1] + y[i]) / 2.0
        ret += mid * (x[i + 1] - x[i])
    return ret

def thrust(v, tank):
    # Thrust exerted by the ejected fluid onto the tank/rocket
    return rho * tank.s * v**2

if __name__ == "__main__":
    # Run the simulation
    tank = Tank(d = 0.02)
    ic = InitialConditions(P0 = 2. * Pa, z0 = 0.33 * tank.H)
    dt = 10**-5 * tank.H / abs(F(ic.z0, tank, ic))
    z, v, p = euler(dt, tank, ic)
    t = dt * np.arange(len(z))

    # Compute the thrust produced over the different time steps
    th = [thrust(vv, tank) for vv in v]
    mean_th = midpoint(t, th) / t[-1]
    print(f"Peak thrust : {max(th):.2f} N")
    print(f"Mean thrust : {mean_th:.2f} N")

    # Cinetic energy is the integral of this temp array
    temp = [tth * vv for tth, vv in zip(v, th)]
    cinetic = midpoint(t, temp)
    print(f"Propulsion energy : {cinetic:.2f} J")

    # Pressure forces work
    V = [(tank.H - zz) * tank.S for zz in z]
    pW = midpoint(V, p)
    print(f"Pressure forces work: {pW:.2f} J")