# HW5 - how to run this

For TA: Quick guide on how to run the code:

## Setup (if on a MAC / if not it's slightly different)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (from this folder)

```bash
python problem1.py  # Problem 5-1: Hohmann/bi-elliptic/bi-parabolic dv/vc1 vs R=r2/r1, two plot ranges
python problem2.py  # Problem 5-2: root-finding for Hohmann/bi-elliptic/bi-parabolic crossover R
python problem3.py  # Problem 5-3: vc1=1, vc2=0.5 rendezvous, picks the lowest-impulse transfer
python problem4.py  # Problem 5-4: LEO (300 km, 57 deg) to GEO Hohmann transfer with plane change
python problem5.py  # Problem 5-5: LEO (350 km, 28 deg) to GPS orbit (26558 km, 55 deg) two-impulse transfer
python problem6.py  # Problem 5-6: LEO (300 km, 28.5 deg) to GEO, inclination split between the two impulses
```

`transfers.py` holds the normalized Hohmann/bi-elliptic/bi-parabolic impulse formulas shared by
Problems 5-1 to 5-3. `orbit_utils.py` holds the orbital-elements-to-ECI conversion and line-of-intersection
routines shared by Problems 5-4 and 5-5.
