import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from collision_detection import check_collisions, interpolate
from optimization import *

folder = os.path.dirname(os.path.abspath(__file__))

csv_files = sorted([
    f for f in os.listdir(folder)
    if f.startswith("timed_traj_") and f.endswith(".csv")
])

csv_paths = [os.path.join(folder, f) for f in csv_files]
dfs = [pd.read_csv(path) for path in csv_paths]

print(f"Učitane {len(dfs)} trajektorije:")
for f in csv_files:
    print(" -", f)

all_times = np.unique(np.concatenate([df["t"].values for df in dfs]))
dfs_interp = [interpolate(df, all_times) for df in dfs]

pairs = [(i, j) for i in range(len(dfs_interp)) for j in range(i + 1, len(dfs_interp))]

print("\nProvjera sudara PRIJE optimizacije:")

for i, j in pairs:
    collisions = check_collisions(dfs_interp[i], dfs_interp[j])
    name1, name2 = csv_files[i], csv_files[j]

    if collisions:
        print(f"\nSudar između {name1} i {name2}:")
        for t, d in collisions:
            print(f"  t = {t:.2f} s, udaljenost = {d:.3f} m")
    else:
        print(f"\nNema sudara između {name1} i {name2}")

print("\nPokretanje CP-SAT optimizacije vremenskog pomaka...")
dfs_optimized = time_shift_cp_sat(dfs_interp)

print("\nProvjera sudara NAKON optimizacije:")

for i, j in pairs:
    collisions = check_collisions(dfs_optimized[i], dfs_optimized[j])
    name1, name2 = csv_files[i], csv_files[j]

    if collisions:
        print(f"Sudar I DALJE postoji između {name1} i {name2}")
    else:
        print(f"Nema sudara između {name1} i {name2}")

for df, name in zip(dfs_optimized, csv_files):
    out_name = "optimized_" + name
    out_path = os.path.join(folder, out_name)
    df.to_csv(out_path, index=False)

print("\nOptimizirane trajektorije spremljene kao:")
for f in csv_files:
    print(" - optimized_" + f)