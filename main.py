import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt

# Physics constants
g = 9.81 # gravity acceleration
rho = 10 ** 3 # water density
Pa = 10 ** 5 # Atmospheric pressure

class Tank:
    def __init__(self, H = 1.0, D = 0.3, d = 0.02):
        self.H = H # height of tank
        self.D = D # diameter of tank
        self.d = d # diameter of ejection tube
        self.S = 3.1416 * (0.5 * D) ** 2 # cross section area of water tank
        self.s = 3.1416 * (0.5 * d) ** 2 # cross section area of ejection tube
        self.beta = (self.S / self.s) ** 2 - 1 # convenient constant

InitialConditions = namedtuple("InitialConditions", ["P0", "z0"])

def pressure(z, tank, ic):
    return ic.P0 * (tank.H - ic.z0) / (tank.H - z)
    
def F(z, tank, ic):
    return - np.sqrt((2. / tank.beta) * ((g * z) + (pressure(z, tank, ic) - Pa) / rho))

def stop(z, f, tank, ic):
    if z < 0:
        return True, "water level hit the bottom"
    if abs(f) < 0.001:
        return True, f"flow reached slow speed: {abs(f)} m/s"
    if (g * z) + (pressure(z, tank, ic) - Pa) / rho < 0:
        return True, f"hydrostatic equilibrium went wrong, reduce dt"
    return False, ""

    
def euler(dt, tank, ic):
    z = [ic.z0]
    v = [abs(F(ic.z0, tank, ic) * tank.S / tank.s)]
    p = [pressure(z[0], tank, ic) / Pa]
    stop_now, reason = stop(z[0], v[0], tank, ic)
    while not stop_now:
        zn = z[-1]
        f = F(zn, tank, ic)
        z.append(zn + dt * f)
        v.append(abs(f * tank.S / tank.s))
        p.append(pressure(zn, tank, ic))
        stop_now, reason = stop(zn, f, tank, ic)
    print("Simulation stopped because", reason)
    return z, v, p

def plot(data, tank, ic, ax):
    PoP = "${\\frac{P_0}{P_a}}$"
    zoH = "${\\frac{z_0}{H}}$"
    soS = "${\\frac{s}{S}}$"
    simu_params = f"{PoP}={ic.P0/Pa}, {zoH}={ic.z0/tank.H:.2f}, {soS}={tank.S / tank.s:.2f}"
    ax.plot(dt * np.arange(len(data)), data, label = simu_params)

if __name__ == "__main__":
    # Simus
    tank = Tank(d = 0.02)
    ic = InitialConditions(P0 = 2. * Pa, z0 = 0.6 * tank.H)
    dt = 10**-4 * tank.H / abs(F(ic.z0, tank, ic))
    z, v, p = euler(dt, tank, ic)
    # ----------------------
    ic1 = InitialConditions(P0 = 2. * Pa, z0 = 0.5 * tank.H)
    dt = 10**-4  * tank.H / abs(F(ic1.z0, tank, ic1))
    z1, v1, p1 = euler(dt, tank, ic1)
    # ----------------------
    ic2 = InitialConditions(P0 = 2. * Pa, z0 = 0.4 * tank.H)
    dt = 10**-4  * tank.H / abs(F(ic2.z0, tank, ic2))
    z2, v2, p2 = euler(dt, tank, ic2)

    # Plot
    f, (w_ax, p_ax) = plt.subplots(2, 1, constrained_layout=True, figsize = (8, 8))
    plot(z, tank, ic, w_ax)
    plot(z1, tank, ic1, w_ax)
    plot(z2, tank, ic2, w_ax)
    plot(np.array(p) / Pa, tank, ic, p_ax)
    plot(np.array(p1) / Pa, tank, ic1, p_ax)
    plot(np.array(p2) / Pa, tank, ic2, p_ax)
    w_ax.set_title("Water level (m)")
    w_ax.set_xlabel("t(s)", loc="right")
    p_ax.set_title("Tank pressure (bar)")
    p_ax.set_xlabel("t(s)", loc="right")

    
    w_ax.legend()
    p_ax.legend()
    plt.show()