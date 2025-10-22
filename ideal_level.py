from thrust import *

if __name__ == "__main__":

    fig, ax = plt.subplots()
    ax.set_title("Impulse (Ns)")
    ax.set_xlabel("$\\frac{z_0}{H}$", loc="right")
    for c in (2., 3., 4., 5.):
        lvl, imp = [], []
        for r in (0.15, 0.2, 0.25, 0.30, 0.33, 0.35, 0.4, 0.44, 0.5, 0.55):
            ic = InitialConditions(P0 = c * Pa, z0 = r * rocket.H)
            dt = 10**-5 * rocket.H / abs(F(ic.z0, rocket, ic))
            t, z, v, p = euler(rocket, ic, verbose = False)

            weight = [rho * g * rocket.S * zz for zz in z]
            th = [thrust(vv, rocket) for vv in v]
            force = np.array(th) - np.array(weight)
            impulse = midpoint(t, force)

            if impulse > 0:
                lvl.append(r)
                imp.append(impulse)
        ax.plot(lvl, imp, label = "$P_0=$" + f"{c} bar")
    ax.legend()
    plt.show()

            