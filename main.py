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
        self.beta = (S/s) ** 2 - 1 # convenient constant

InitialConditions = namedtuple("InitialConditions", ["P0", "z0"])

def p(z, tank, ic):
    return ic.P0 * (tank.H - ic.z0) / (tank.H - z)
    
def F(z, tank, ic):
    return - np.sqrt((2. / tank.beta) * ((g * z) + (p(z, tank, ic) - Pa) / rho))

def stop(z, f, tank, ic):
    if z < 0:
        return True, "water level hit the bottom"
    if abs(f) < 0.001:
        return True, f"flow reached slow speed: {abs(f)} m/s"
    if (g * z) + (p(z, tank, ic) - Pa) / rho < 0:
        return True, f"hydrostatic equilibrium went wrong, reduce dt"
    return False, ""

    
def euler(dt, tank, ic):
    z = [ic.z0]
    v = []
    stop_now, reason = stop(ic.z0, F(ic.z0, tank, ic), tank, ic)
    while not stop_now:
        zn = z[-1]
        f = F(zn, tank, ic)
        z.append(zn + dt * f)
        v.append(abs(f * tank.S / tank.s))
        stop_now, reason = stop(zn, f, tank, ic)
    print("Simulation stopped because", reason)
    return z, v


if __name__ == "__main__":
    # Simu
    tank = Tank()
    ic = InitialConditions(P0 = 2. * Pa, z0 = 0.8 * tank.H)
    dt = 0.01 * tank.H / abs(F(ic.z0, tank, ic))
    z, v = euler(dt, tank, ic)

    # Plot
    f, (water, flow) = plt.subplots(2, 1, constrained_layout=True, figsize = (8, 8))
    water.set_title("Water level (m)")
    water.set_xlabel("t(s)", loc="right")
    flow.set_title("Ejection speed (m/s)")
    flow.set_xlabel("t(s)", loc="right")

    simu_params = f"P0={ic.P0/10**5} atm, z0/H = {ic.z0/H:.2f}, S/s={tank.S / tank.s:.2f}"
    water_plot = water.plot(dt * np.arange(len(z)), z, label = simu_params)
    flow_plot = flow.plot(dt * np.arange(len(v)), v, label = simu_params)
    water.legend()
    flow.legend()
    plt.show()