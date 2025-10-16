import numpy as np
import matplotlib.pyplot as plt

# Tank dimensions
H = 1.0 # height of tank
D = 0.3 # diameter of tank
d = 0.02 # diameter of expulsion tube
S = 3.1416 * (0.5 * D) ** 2 # cross section area of water tank
s = 3.1416 * (0.5 * d) ** 2 # cross section area of expulsion tube
beta = (S/s) ** 2 - 1 # convenient constant
g = 9.81 # gravity acceleration
rho = 10 ** 3 # water density
Pa = 10 ** 5 # Atmospheric pressure
P0 = 3 * Pa  # Initial tank pressure
z0 = 0.67 * H # Inital water height
#V0 = (2 * g * z0 + 2 * (P0 - Pa) / rho) ** 0.5 # initial jet speed


def p(z):
    return P0 * (H - z0) / (H - z)
    
def F(z):
    return - np.sqrt((2. / beta) * ((g * z) + (p(z)-Pa)/rho))

def stop(z, f, dt, t, tf):
    if z + dt * f < 0:
        return True, "water level hit the bottom"
    if abs(f) < 0.001:
        return True, f"flow reached slow speed: {f} m/s"
    if (g * z) + (p(z)-Pa)/rho < 0:
        return True, f"hydrostatic equilibrium went wrong, reduce dt"
    if t > tf:
        return True, f"final time was reached"
    return False, ""

dt = 0.001 * H / abs(F(z0))
    
def euler(tf):
    ret = [z0]
    z = z0
    f = F(z0)
    t = 0
    stop_now = False
    while not stop_now:
        # iterate first
        ret.append(z + dt * f)
        
        # compute for loop stop condition
        z = ret[-1]
        f = F(z)
        t += dt
        stop_now, reason = stop(z, f, dt, t, tf)
    print("Simulation stopped because", reason)
    return ret
    
z = euler(60)
plt.plot(dt * np.arange(len(z)), z)
plt.show()