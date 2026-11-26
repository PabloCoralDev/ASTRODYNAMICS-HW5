import numpy as np
import matplotlib.pyplot as plt

from orbit_utils import MU_EARTH, R_EARTH, elements_to_rv, orbit_points

# constants 
ALT1 = 350.0 # km
INC1 = np.radians(28.0)
R2 = 26558.0 # km
INC2 = np.radians(55.0)
OMEGA = 0.0 # Omega1 = Omega2 = 0

def h_direction(i, Omega):
    # unit angular momentum vec from i and Omega
    return np.array([np.sin(i)*np.sin(Omega), -np.sin(i)*np.cos(Omega), np.cos(i)])

def format_vec(v):
    # print vec as (x, y, z) for ease of output
    return "(" + ", ".join(f"{x + 0.0:.1f}" for x in v) + ")"

mu = MU_EARTH
r1 = R_EARTH + ALT1
r2 = R2

# props
a = (r1 + r2)/2
e = (r2 - r1)/(r2 + r1)

## a. line of intersection
h1_dir = h_direction(INC1, OMEGA)
h2_dir = h_direction(INC2, OMEGA)
ell = np.cross(h1_dir, h2_dir)
ell = ell / np.linalg.norm(ell)

## b. impulse positions
r1_vec = r1*ell
r2_vec = -r2*ell

## f. plane rotation angle (needed for c)
theta = np.arccos(np.dot(h1_dir, h2_dir))

## c. impulse magnitudes

# initial orbit
v1_circ = np.sqrt(mu/r1)
v1_peri = np.sqrt(2*mu/r1 - mu/a)
dv1 = v1_peri - v1_circ

# final orbit
v2_apo = np.sqrt(2*mu/r2 - mu/a)
v2_circ = np.sqrt(mu/r2)
dv2 = np.sqrt(v2_apo**2 + v2_circ**2 - 2*v2_apo*v2_circ*np.cos(theta))

# totals
dv_total = dv1 + dv2

## d. ttc
T_transfer = 2*np.pi*np.sqrt((a**3)/mu)
tof_hours = (T_transfer/2)/3600.0

# print out for report
print(f"(a) line of intersection (unit vector): {format_vec(ell)}")
print(f"(b) r1 = {format_vec(r1_vec)} km, r2 = {format_vec(r2_vec)} km")
print(f"(c) dv1 = {dv1:.4f} km/s, dv2 = {dv2:.4f} km/s, total dV = {dv_total:.4f} km/s")
print(f"(d) time of flight = {tof_hours:.4f} hours")
print(f"(e) eccentricity of transfer orbit = {e:.6f}")
print(f"(f) theta = {np.degrees(theta):.4f} deg")

# ======== g. 3D plotting ====== # (same as p4)

# build x, y, z arrays for each orbit curve (includes transfer)
x1, y1, z1 = orbit_points(r1, 0.0, OMEGA, INC1, 0.0)
x2, y2, z2 = orbit_points(r2, 0.0, OMEGA, INC2, 0.0)
xt, yt, zt = orbit_points(a, e, OMEGA, INC1, 0.0, nu_range=(0, np.pi))

# prep first impulse vec
r_peri, v_peri_minus = elements_to_rv(r1, 0.0, OMEGA, INC1, 0.0, 0.0, mu=mu)
u1 = v_peri_minus / np.linalg.norm(v_peri_minus) # build unit vec in first dir
dv1_vec = dv1 * u1 # include magnitude

# prep second impulse vec
r_apo, v_apo_minus = elements_to_rv(a, e, OMEGA, INC1, 0.0, np.pi, mu=mu)
r_apo_hat = r_apo / np.linalg.norm(r_apo) # get dir of apoapsis
v2_dir = np.cross(h2_dir, r_apo_hat) # find tangential vel dir in GPS plane - diff from p4
v_apo_plus_vec = v2_circ * v2_dir
dv2_vec = v_apo_plus_vec - v_apo_minus

## draw orbit ##
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection="3d")

# plot initial, final and transf curves
ax.plot(x1, y1, z1, label="Initial LEO ($i_1=28^\\circ$)", color="tab:blue")
ax.plot(x2, y2, z2, label="Terminal GPS orbit ($i_2=55^\\circ$)", color="tab:green")
ax.plot(xt, yt, zt, "--", label="Transfer orbit", color="tab:orange")

ell_plot = ell * r2 # fit ell to r2
# plot fitted ell line
ax.plot([-ell_plot[0], ell_plot[0]], [-ell_plot[1], ell_plot[1]], [-ell_plot[2], ell_plot[2]], ":", color="gray", label="Line of intersection")

# burn locns
ax.scatter(*r_peri, color="red", s=30)
ax.scatter(*r_apo, color="purple", s=30)

#scale up
scale = 3000

ax.quiver(*r_peri, *(dv1_vec * scale), color="red", linewidth=2, label=r"$\Delta^I v_1$")
ax.quiver(*r_apo, *(dv2_vec * scale), color="purple", linewidth=2, label=r"$\Delta^I v_2$")

## labeling
ax.set_xlabel("x [km]")
ax.set_ylabel("y [km]")
ax.set_zlabel("z [km]")
ax.legend(fontsize=8)
ax.set_box_aspect([1, 1, 0.5])
fig.tight_layout()
fig.savefig("report/figures/problem5_transfer.png", dpi=150)
