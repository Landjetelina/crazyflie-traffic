import numpy as np
import pandas as pd

def check_collisions(df1, df2, min_dist=0.2):
    # Definiramo zajednički vremenski raspon od početka do kraja najdužeg leta
    t_start = min(df1["t"].min(), df2["t"].min())
    t_end = max(df1["t"].max(), df2["t"].max())
    
    # Rezolucija provjere (npr. svakih 0.1 sekundu)
    common_times = np.arange(t_start, t_end + 0.1, 0.1)
    
    # Interpoliramo oba drona na istu vremensku mrežu
    # np.interp će zadržati zadnju poziciju drona ako je on završio let (hovering na cilju)
    p1x = np.interp(common_times, df1["t"], df1["x"])
    p1y = np.interp(common_times, df1["t"], df1["y"])
    p1z = np.interp(common_times, df1["t"], df1["z"])
    
    p2x = np.interp(common_times, df2["t"], df2["x"])
    p2y = np.interp(common_times, df2["t"], df2["y"])
    p2z = np.interp(common_times, df2["t"], df2["z"])
    
    collisions = []
    for i, t in enumerate(common_times):
        d = np.sqrt((p1x[i]-p2x[i])**2 + (p1y[i]-p2y[i])**2 + (p1z[i]-p2z[i])**2)
        if d < min_dist:
            collisions.append((t, d))
    return collisions

def interpolate(df, times):
    # Ova funkcija ostaje slična, ali koristi se za pripremu podataka
    return pd.DataFrame({
        "t": times,
        "x": np.interp(times, df["t"], df["x"]),
        "y": np.interp(times, df["t"], df["y"]),
        "z": np.interp(times, df["t"], df["z"]),
    })