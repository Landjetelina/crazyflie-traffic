import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collision_detection import check_collisions, interpolate

folder = os.path.dirname(os.path.abspath(__file__))
csv_files = [f for f in os.listdir(folder) if f.startswith("timed_traj_") and f.endswith(".csv")]
csv_paths = [os.path.join(folder, f) for f in csv_files]
dfs = [pd.read_csv(path) for path in csv_paths]

all_times = np.unique(np.concatenate([df["t"].values for df in dfs]))

dfs_interp = [interpolate(df, all_times) for df in dfs]

pairs = [(i, j) for i in range(len(dfs_interp)) for j in range(i + 1, len(dfs_interp))]

print("\nProvjere sudara prije optimizacije: ")
for i, j in pairs:
    col = check_collisions(dfs_interp[i], dfs_interp[j])
    name1, name2 = csv_files[i], csv_files[j]

    if col:
        print(f"\n Sudar između {name1} i {name2}:")
        for t, d in col:
            print(f"   t = {t:.2f} s, udaljenost = {d:.3f} m")
    else:
        print(f"\n Nema sudara između {name1} i {name2}")
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ["blue", "red", "green"]

for df, fname, color in zip(dfs_interp, csv_files, colors):
    ax.plot(df["x"], df["y"], df["z"], label=fname, color=color)

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_zlabel("Z [m]")
ax.legend()
plt.title("Putanje dronova prije optimizacije")
plt.show()

