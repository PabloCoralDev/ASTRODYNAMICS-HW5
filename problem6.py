import numpy as np
import matplotlib.pyplot as plt

from orbit_utils import MU_EARTH, R_EARTH

ALT1 = 300.0 # km
T_GEO = 24.0*3600.0 # s
INC_TOTAL = np.radians(28.5)

# consts
mu = MU_EARTH
r1 = R_EARTH + ALT1
r2 = (mu*T_GEO**2/(4*np.pi**2))**(1/3)
a = (r1 + r2)/2

# individual impulse reqs
v1_circ = np.sqrt(mu/r1)
v1_peri = np.sqrt(2*mu/r1 - mu/a)
v2_apo = np.sqrt(2*mu/r2 - mu/a)
v2_circ = np.sqrt(mu/r2)

# helper to find total deltV as a function of init LEO fraction of incl change 'f'
def total_dv(f):
    di1 = f*INC_TOTAL
    di2 = (1 - f)*INC_TOTAL
    dv1 = np.sqrt(v1_circ**2 + v1_peri**2 - 2*v1_circ*v1_peri*np.cos(di1))
    dv2 = np.sqrt(v2_apo**2 + v2_circ**2 - 2*v2_apo*v2_circ*np.cos(di2))
    return dv1 + dv2

print(f"r1 = {r1:.3f} km, r2 = {r2:.3f} km, a = {a:.3f} km")

# a. case for f=0 (all at apo)
dv_a = total_dv(0.0)
print(f"(a) total impulse, inclination change at apoapsis (f=0): {dv_a:.4f} km/s")

# b. case for f=1 (all at LEO)
dv_b = total_dv(1.0)
print(f"(b) total impulse, inclination change at LEO (f=1): {dv_b:.4f} km/s")

# c. & d. f in increments of 0.01 (the + 1e-9 makes arange include f = 1)
f_vals = np.arange(0.0, 1.0 + 1e-9, 0.01)
dv_norm = np.array([total_dv(f)/v1_circ for f in f_vals])

# find values at min
best_idx = np.argmin(dv_norm)
f_best = f_vals[best_idx]
print(f"(d) minimum-impulse fraction: f = {f_best:.2f}, dV/vc1 = {dv_norm[best_idx]:.4f}")

#plot and save!
fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.plot(f_vals, dv_norm, color="tab:blue")
ax.plot(f_best, dv_norm[best_idx], "o", color="red", label=f"Minimum at $f={f_best:.2f}$")

ax.set_xlabel(r"$f$ (fraction of inclination change at initial LEO)")
ax.set_ylabel(r"$\Delta V / v_{c1}$")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("report/figures/problem6_dv_vs_f.png")
