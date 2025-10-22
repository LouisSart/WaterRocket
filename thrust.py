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
    tank = Tank(D = 0.09, d = 0.01)
    fig, ax = plt.subplots()
    ax.set_title("Thrust (N)")
    ax.set_xlabel("t(s)", loc="right")

    for c in (2., 3., 4., 5.):
        ic = InitialConditions(P0 = c * Pa, z0 = 0.33 * tank.H)
        dt = 10**-5 * tank.H / abs(F(ic.z0, tank, ic))
        t, z, v, p = euler(tank, ic)

        # Compute the thrust produced over the different time steps
        th = [thrust(vv, tank) for vv in v]
        impulse = midpoint(t, th)
        mean_th = impulse / t[-1]
        # print(f"Peak thrust : {max(th):.2f} N")
        # print(f"Mean thrust : {mean_th:.2f} N")
        ax.plot(t, th, label = f"$P_0$ = {c} bar, Impulse = {impulse:.2f} Ns")

    ax.legend()
    plt.show()

    # Cinetic energy is the integral of this temp array
    temp = [tth * vv for tth, vv in zip(v, th)]
    cinetic = midpoint(t, temp)
    # print(f"Propulsion energy : {cinetic:.2f} J")

    # Pressure forces work
    V = [(tank.H - zz) * tank.S for zz in z]
    pW = midpoint(V, p)
    # print(f"Pressure forces work: {pW:.2f} J")
