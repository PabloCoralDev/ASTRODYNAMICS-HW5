import numpy as np
import matplotlib.pyplot as plt

from transfers import hohmann_dv, bielliptic_dv, biparabolic_dv

S_VALUES = (2, 5, 10, 11, 12, 15)

def make_plot(R, fname, ylim=None):
    fig, ax = plt.subplots(figsize=(8, 5.5))

    dv1, dv2 = hohmann_dv(R)
    ax.plot(R, dv1 + dv2, label="Hohmann Transfer", linewidth=1.5)

    for S in S_VALUES:
        dv1, dv2, dv3 = bielliptic_dv(R, S)
        ax.plot(R, dv1 + dv2 + dv3, label=f"Bi-Elliptic Transfer (S = {S})", linewidth=1.25)

    dv1, dv2 = biparabolic_dv(R)
    ax.plot(R, dv1 + dv2, "k--", label="Bi-Parabolic Transfer", linewidth=1.5)

    ax.set_xlabel(r"$R = r_2/r_1$")
    ax.set_ylabel(r"$\Delta v / v_{c1}$")

    # for focusing on certain y-vals
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"report/figures/{fname}")


R1 = np.linspace(1, 20, 2000)
make_plot(R1, "problem1_full.png")

R2 = np.linspace(10, 16, 2000)
make_plot(R2, "problem1_zoom.png", ylim=(0.51, 0.55))