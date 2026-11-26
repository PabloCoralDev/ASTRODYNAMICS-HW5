import numpy as np
import matplotlib.pyplot as plt

from transfers import hohmann_dv, bielliptic_dv, biparabolic_dv

# canonical units
MIU = 1.0

def circular_orbit(r, n=400):
    theta = np.linspace(0, 2 * np.pi, n)
    return r * np.cos(theta), r * np.sin(theta)

def transfer_ellipse(r1, r2, n=400):
    a = (r1 + r2) / 2
    e = (r2 - r1) / (r2 + r1)
    p = a * (1 - e ** 2)
    nu = np.linspace(0, np.pi, n)
    r = p / (1 + e * np.cos(nu))
    return r * np.cos(nu), r * np.sin(nu)

# given circular speeds 
vc1 = 1.0
vc2 = 0.5

r1 = MIU / vc1 ** 2
r2 = MIU / vc2 ** 2
R = r2 / r1

# calculate normalized impulses & destruct
dvH1, dvH2 = hohmann_dv(R)
dvBP1, dvBP2 = biparabolic_dv(R)

S_test = (2, 5, 10, 11, 12, 15)  # same S values as Problem 2
dvBE_totals = {S: sum(bielliptic_dv(R, S)) for S in S_test} # one line loop

print(f"Hohmann total/vc1: {dvH1 + dvH2:.4f}")
print(f"Bi-parabolic total/vc1: {dvBP1 + dvBP2:.4f}")
for S, total in dvBE_totals.items():
    print(f"Bi-elliptic (S={S}) total/vc1: {total:.4f}")

# organize candidates and find min total
candidates = {"Hohmann": dvH1 + dvH2, 
              "Bi-parabolic": dvBP1 + dvBP2, 
              **{f"Bi-elliptic S={S}": v for S, v in dvBE_totals.items()}} # ** unpacks dict for all BE_n

best = min(candidates, key=candidates.get)
print(f"\nLowest total impulse: {best} ({candidates[best]:.4f} vc1)")

# Build plot for Hohmann (winning transfer in this case)
x1, y1 = circular_orbit(r1)
x2, y2 = circular_orbit(r2)
xt, yt = transfer_ellipse(r1, r2)

dv1 = dvH1 * vc1
dv2 = dvH2 * vc1

# set up plots
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(x1, y1, label=f"Initial orbit ($r_1={r1:.1f}$)", color="tab:blue")
ax.plot(x2, y2, label=f"Terminal orbit ($r_2={r2:.1f}$)", color="tab:green")
ax.plot(xt, yt, "--", label="Transfer orbit", color="tab:orange")
ax.plot(0, 0, "k+", markersize=10)

# impulse 1 at periapsis (r1, 0), tangential (+y direction)
ax.quiver(r1, 0, 0, dv1, color="red", angles="xy", scale_units="xy", scale=1, width=0.01, label=r"$\Delta v_1$")
# impulse 2 at apoapsis (-r2, 0), tangential (-y direction, continuing prograde motion)
ax.quiver(-r2, 0, 0, -dv2, color="purple", angles="xy", scale_units="xy", scale=1, width=0.01, label=r"$\Delta v_2$")

ax.set_xlabel("x [DU]")
ax.set_ylabel("y [DU]")
ax.set_aspect("equal")
ax.legend(fontsize=8, loc="upper left")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("report/figures/problem3_transfer.png")
