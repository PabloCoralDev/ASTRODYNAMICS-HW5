import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt

from transfers import hohmann_dv, bielliptic_dv, biparabolic_dv

S_VALUES = (2, 5, 10, 11, 12, 15)

# make a function for each total
def hohmann_total(R):
    dv1, dv2 = hohmann_dv(R)
    return dv1 + dv2

def biparabolic_total(R):
    dv1, dv2 = biparabolic_dv(R)
    return dv1 + dv2

def bielliptic_total(R, S):
    dv1, dv2, dv3 = bielliptic_dv(R, S)
    return dv1 + dv2 + dv3

# part (a): Hohmann vs. bi-parabolic crossover rootfinding
f_bp = lambda R: hohmann_total(R) - biparabolic_total(R)
R_bp = brentq(f_bp, 2, 50)
print(f"(a) Hohmann = bi-parabolic at R = {R_bp:.4f}")

# part (b): Hohmann vs. bi-elliptic crossover with 1 root per S-val. 
R_be = []
for S in S_VALUES:
    f_be = lambda R, S=S: hohmann_total(R) - bielliptic_total(R, S)
    R_root = brentq(f_be, 2, 50)
    R_be.append(R_root)
    print(f"(b) S = {S:2d}: Hohmann = bi-elliptic at R = {R_root:.4f}")

# part (c): plotting
fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(S_VALUES, R_be, "o-", color="tab:blue", label="Hohmann = Bi-Elliptic")
ax.axhline(R_bp, color="k", linestyle="--", label=f"Hohmann = Bi-Parabolic (R = {R_bp:.3f})")

ax.set_xlabel(r"$S = r_i/r_2$")
ax.set_ylabel(r"$R = r_2/r_1$ at crossover")

ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()

fig.savefig("report/figures/problem2_roots.png")

