import numpy as np

# Shared co-planar transfer formulas that will be reused
def hohmann_dv(R):
    dv1 = np.sqrt(2 * R / (1 + R)) - 1
    dv2 = np.sqrt(1 / R) - np.sqrt(2 / (R * (1 + R)))
    return dv1, dv2

def bielliptic_dv(R, S):
    dv1 = np.sqrt(2 * R * S / (1 + R * S)) - 1
    dv2 = np.sqrt(1 / (R * S)) * (np.sqrt(2 / (1 + S)) - np.sqrt(2 / (1 + R * S)))
    dv3 = np.sqrt(2 * S / (R + R * S)) - np.sqrt(1 / R)
    return dv1, dv2, dv3

def biparabolic_dv(R):
    dv1 = np.sqrt(2) - 1
    dv2 = (np.sqrt(2) - 1) * np.sqrt(1 / R)
    return dv1, dv2

# sanity check vs. the closed forms in Eqs. (5.20) and (5.44) of notes
# (guarded so it only runs when this file is run directly, not when imported)
if __name__ == "__main__":
    R = 4.0
    dv1, dv2 = hohmann_dv(R)
    print("Hohmann total/vc1:", dv1 + dv2)

    dv1, dv2 = biparabolic_dv(R)
    print("Bi-parabolic total/vc1:", dv1 + dv2, (np.sqrt(2) - 1) * (1 + np.sqrt(1 / R)))

    dv1, dv2, dv3 = bielliptic_dv(R, 1e6)
    print("Bi-elliptic (S->inf) total/vc1:", dv1 + dv2 + dv3)
