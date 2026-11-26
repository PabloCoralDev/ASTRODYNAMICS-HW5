import numpy as np
import matplotlib.pyplot as plt

from orbit_utils import MU_EARTH, R_EARTH, elements_to_rv, orbit_points

# constants reqd
ALT1 = 300.0 # km
INC1 = np.radians(57.0)
OMEGA = np.radians(60.0)
T_GEO = 23.934*3600.0 # s
ISP = 320.0 # s
G0 = 9.80665e-3 # km/s^2

mu = MU_EARTH
r1 = R_EARTH + ALT1
r2 = (mu*T_GEO**2/(4*np.pi**2))**(1/3) # from orbital period eqn.

# basic orbit props
a = (r1 + r2)/2
e = (r2 - r1)/(r2 + r1)

## a. impulse magnitudes

# initial orbit
v1_circ = np.sqrt(mu/r1)
v1_peri = np.sqrt(2*mu/r1 - mu/a)
dv1 = v1_peri - v1_circ

# final orbit
v2_apo = np.sqrt(2*mu/r2 - mu/a)
v2_circ = np.sqrt(mu/r2)
dv2 = np.sqrt(v2_apo**2 + v2_circ**2 - 2*v2_apo*v2_circ*np.cos(INC1))

# totals
dv_total = dv1 + dv2

## c. ttc
T_transfer = 2*np.pi*np.sqrt((a**3)/mu)
tof_hours = (T_transfer/2)/3600.0

## d. mass ratios
ratio1 = np.exp(dv1 / (ISP*G0))
ratio2 = np.exp(dv2 / (ISP*G0))

# print out for report
print(f"r1 = {r1:.3f} km, r2 = {r2:.3f} km, a = {a:.3f} km")
print(f"(a) dv1 = {dv1:.4f} km/s, dv2 = {dv2:.4f} km/s")
print(f"(b) total dV = {dv_total:.4f} km/s")
print(f"(c) time of flight = {tof_hours:.4f} hours")
print(f"(d) m0/mf = {ratio1:.4f} (impulse 1), {ratio2:.4f} (impulse 2)")

# ======== e. 3D plotting ====== #

# build x, y, z arrays for each orbit curve (includes transfer)
x1, y1, z1 = orbit_points(r1, 0.0, OMEGA, INC1, 0.0)
x2, y2, z2 = orbit_points(r2, 0.0, 0.0, 0.0, 0.0)
xt, yt, zt = orbit_points(a, e, OMEGA, INC1, 0.0, nu_range=(0, np.pi))

# prep first impulse vec
r_peri, v_peri_minus = elements_to_rv(r1, 0.0, OMEGA, INC1, 0.0, 0.0, mu=mu)
u1 = v_peri_minus / np.linalg.norm(v_peri_minus) # build unit vec in first dir
dv1_vec = dv1 * u1 # include magnitude

# prep second impulse vec
r_apo, v_apo_minus = elements_to_rv(a, e, OMEGA, INC1, 0.0, np.pi, mu=mu)
r_apo_hat = r_apo / np.linalg.norm(r_apo) # get dir of apoapsis
v2_dir = np.cross([0, 0, 1], r_apo_hat) # find tangential vel dir (prograde)
v_apo_plus_vec = v2_circ * v2_dir
dv2_vec = v_apo_plus_vec - v_apo_minus

# line of intersection between initial and terminal orbital planes
h1 = np.cross(r_peri, v_peri_minus)
h2 = np.array([0, 0, 1])  # terminal orbit is equatorial (in Iz); only direction matters

# build line of intersection for orbit planes (cursive l --> will call 'ell')
ell = np.cross(h1, h2)
ell = ell / np.linalg.norm(ell) * r2

## use everything above to draw orbit! ##
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection="3d")

# plot initial, final and transf curves
ax.plot(x1, y1, z1, label="Initial LEO", color="tab:blue")
ax.plot(x2, y2, z2, label="Terminal GEO", color="tab:green")
ax.plot(xt, yt, zt, "--", label="Transfer orbit", color="tab:orange")

# can plot straight line for ell. ([-x, x], [-y,y], [-z, z]) of ell ; ':' => dotted line
ax.plot([-ell[0], ell[0]], [-ell[1], ell[1]], [-ell[2], ell[2]], ":", color="gray", label="Line of intersection")

# dot each burn locn (easier to view)
ax.scatter(*r_peri, color="red", s=30)
ax.scatter(*r_apo, color="purple", s=30)

#scale up so we can see the vecs & quiver
scale = 3000
ax.quiver(*r_peri, *(dv1_vec * scale), color="red", linewidth=2, label=r"$\Delta^I v_1$")
ax.quiver(*r_apo, *(dv2_vec * scale), color="purple", linewidth=2, label=r"$\Delta^I v_2$")

## labeling stuffs
ax.set_xlabel("x [km]")
ax.set_ylabel("y [km]")
ax.set_zlabel("z [km]")
ax.legend(fontsize=8)
ax.set_box_aspect([1, 1, 0.6])
fig.tight_layout()
fig.savefig("report/figures/problem4_transfer.png", dpi=150)
