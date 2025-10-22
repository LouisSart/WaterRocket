import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt

# Physics constants
g = 9.81 # gravity acceleration
rho = 10 ** 3 # water density
Pa = 10 ** 5 # Atmospheric pressure
gam = 1.4 # air adiabatic index Cp/Cv

class Tank:
    def __init__(self, H = 1.0, D = 0.3, d = 0.02):
        self.H = H # height of tank
        self.D = D # diameter of tank
        self.d = d # diameter of ejection tube
        self.S = 3.1416 * (0.5 * D) ** 2 # cross section area of water tank
        self.s = 3.1416 * (0.5 * d) ** 2 # cross section area of ejection tube
        self.beta = self.s / self.S # convenient constant

InitialConditions = namedtuple("InitialConditions", ["P0", "z0"])

def pressure(z, tank, ic):
    assert(z < tank.H)
    return ic.P0 * ((tank.H - ic.z0) / (tank.H - z)) ** gam
    
def F(z, tank, ic):
    return - tank.beta *  np.sqrt((2. / rho) * (pressure(z, tank, ic) - Pa))

def stop(z, f, tank, ic):
    if z < 0:
        return True, "water level hit the bottom"
    if abs(f) < 0.001:
        return True, f"flow reached slow speed: {abs(f)} m/s"
    if pressure(z, tank, ic) < Pa:
        return True, "internal pressure is lower than atmospheric pressure"
    return False, ""

    
def euler(tank, ic, verbose = True):
    assert(ic.P0 > Pa)
    assert(ic.z0 > 0)

    dt = 10**-4 * tank.H / abs(F(ic.z0, tank, ic))
    z = [ic.z0]
    v = [abs(F(ic.z0, tank, ic) * tank.S / tank.s)]
    p = [pressure(z[0], tank, ic)]
    stop_now, reason = stop(z[0], v[0], tank, ic)

    while not stop_now:
        zn = z[-1]
        f = F(zn, tank, ic)
        z.append(zn + dt * f)
        v.append(abs(f * tank.S / tank.s))
        p.append(pressure(zn, tank, ic))
        stop_now, reason = stop(zn, f, tank, ic)

    t = dt * np.arange(len(z))
    if verbose : print("Simulation stopped because", reason)
    return t, z, v, p

if __name__ == "__main__":
    # Simus
    tank = Tank(d = 0.02)
    f, (w_ax, p_ax) = plt.subplots(2, 1, constrained_layout=True, figsize = (8, 8))
    w_ax.set_title("Water level (m)")
    w_ax.set_xlabel("t(s)", loc="right")
    p_ax.set_title("Tank pressure (bar)")
    p_ax.set_xlabel("t(s)", loc="right")

    for c in (0.5, 0.4, 0.3):
        ic = InitialConditions(P0 = 2. * Pa, z0 = c * tank.H)
        t, z, v, p = euler(tank, ic)
        PoP = "${\\frac{P_0}{P_a}}$"
        zoH = "${\\frac{z_0}{H}}$"
        soS = "${\\frac{s}{S}}$"
        legend = f"{PoP}={ic.P0/Pa}, {zoH}={ic.z0/tank.H:.2f}, {soS}={tank.S / tank.s:.2f}"
        w_ax.plot(t, z, label = legend)
        p_ax.plot(t, np.array(p) / Pa, label = legend)

    w_ax.legend()
    p_ax.legend()
    plt.show()