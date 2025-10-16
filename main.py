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
P0 = 10. * Pa  # Initial tank pressure
z0 = 0.5 * H # Inital water height
#V0 = (2 * g * z0 + 2 * (P0 - Pa) / rho) ** 0.5 # initial jet speed


def p(z):
    return P0 * (H - z0) / (H - z)
    
def F(z):
    return - np.sqrt((2. / beta) * ((g * z) + (p(z)-Pa)/rho))

def stop(z, f, dt):
    if z < 0:
        return True, "water level hit the bottom"
    if abs(f) < 0.001:
        return True, f"flow reached slow speed: {abs(f)} m/s"
    if (g * z) + (p(z)-Pa)/rho < 0:
        return True, f"hydrostatic equilibrium went wrong, reduce dt"
    return False, ""

dt = 0.001 * H / abs(F(z0))
    
def euler():
    z = [z0]
    v = [abs(F(z0) * S/s)]
    stop_now, reason = stop(z0, F(z0), dt)
    while not stop_now:
        zn = z[-1]
        f = F(zn)
        z.append(zn + dt * f)
        v.append(abs(f * S/s))
        stop_now, reason = stop(zn, f, dt)
    print("Simulation stopped because", reason)
    return z, v
    
z, v = euler()
# plt.plot(dt * np.arange(len(z)), z)
plt.plot(dt * np.arange(len(v)), v)
plt.title("Ejection speed (m/s) with P0 = 10Pa and z0 = H/2")
plt.show()