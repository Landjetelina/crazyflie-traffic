import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

MIN_DIST = 0.2 

def check_collisions(df1, df2):
    collisions = []
    for i in range(len(df1)):
        p1 = df1.loc[i, ["x", "y", "z"]].values
        p2 = df2.loc[i, ["x", "y", "z"]].values
        d = np.linalg.norm(p1 - p2)
        if d < MIN_DIST:
            collisions.append((df1.loc[i, "t"], d))
    return collisions

def interpolate(df, times):
    return pd.DataFrame({
        "t": times,
        "x": np.interp(times, df["t"], df["x"]),
        "y": np.interp(times, df["t"], df["y"]),
        "z": np.interp(times, df["t"], df["z"]),
    })

        



