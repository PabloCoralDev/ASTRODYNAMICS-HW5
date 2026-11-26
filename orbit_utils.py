import numpy as np

MU_EARTH = 398600.0 # km^3/s^2
R_EARTH = 6378.0 # km


## useful funcs that repeat throughout hw
def rot3(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def rot1(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def perifocal_to_eci(Omega, i, omega):
    # 3-1-3 rotation, perifocal -> ECI 
    return rot3(Omega) @ rot1(i) @ rot3(omega)

# get elements and turn into radius/velocity
def elements_to_rv(a, e, Omega, i, omega, nu, mu=MU_EARTH):
    p = a * (1 - e ** 2)
    r = p / (1 + e * np.cos(nu))
    r_pf = r * np.array([np.cos(nu), np.sin(nu), 0.0])
    v_pf = np.sqrt(mu / p) * np.array([-np.sin(nu), e + np.cos(nu), 0.0])
    T = perifocal_to_eci(Omega, i, omega)
    return T @ r_pf, T @ v_pf

# pass orbital elements to get discrete pts for plotting. 
def orbit_points(a, e, Omega, i, omega, nu_range=(0, 2 * np.pi), n=400, mu=MU_EARTH):
    nus = np.linspace(nu_range[0], nu_range[1], n)
    pts = np.array([elements_to_rv(a, e, Omega, i, omega, nu, mu)[0] for nu in nus])
    return pts[:, 0], pts[:, 1], pts[:, 2]
