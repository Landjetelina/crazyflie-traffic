import numpy as np
import pandas as pd
import glob
import os
from pathlib import Path

def check_collisions(df1, df2, min_dist=0.2):

    t_start = min(df1["t"].min(), df2["t"].min())
    t_end = max(df1["t"].max(), df2["t"].max())
    
    common_times = np.arange(t_start, t_end + 0.1, 0.1)
   
    p1x = np.interp(common_times, df1["t"], df1["x"])
    p1y = np.interp(common_times, df1["t"], df1["y"])
    p1z = np.interp(common_times, df1["t"], df1["z"])
    
    p2x = np.interp(common_times, df2["t"], df2["x"])
    p2y = np.interp(common_times, df2["t"], df2["y"])
    p2z = np.interp(common_times, df2["t"], df2["z"])
    
    collisions = []
    for i, t in enumerate(common_times):
        distance = np.sqrt((p1x[i]-p2x[i])**2 + (p1y[i]-p2y[i])**2 + (p1z[i]-p2z[i])**2)
        if distance < min_dist:
            collisions.append((t, distance))
    return collisions

def solve_and_verify(min_dist=0.3, lift_amount=0.5):
    input_dir = "new_trajectories"
    search_pattern = os.path.join(input_dir, "timed_traj_cf*.csv")
    files = sorted(glob.glob(search_pattern))
    
    if not files:
        print(f"No files found in directory: '{input_dir}'!")
        return

    trajectories = {}
    for f in files:

        df = pd.read_csv(f, sep=None, engine='python')
        df.columns = df.columns.str.strip()
       
        for col in ['t', 'x', 'y', 'z']:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        
        trajectories[f] = df

    file_paths = list(trajectories.keys())

    for i in range(len(file_paths)):
        for j in range(i + 1, len(file_paths)):
            path1, path2 = file_paths[i], file_paths[j]
            df1, df2 = trajectories[path1], trajectories[path2]
            
            detected_collisions = check_collisions(df1, df2, min_dist)
            
            if detected_collisions:
                collision_times = [c[0] for c in detected_collisions]
                t_start_col = min(collision_times)
                t_end_col = max(collision_times)
                
                print(f"Collision detected between {os.path.basename(path1)} and {os.path.basename(path2)}.")
                print(f"  -> Duration: from {t_start_col:.2f}s to {t_end_col:.2f}s. Fixing...")
                
                for t_col, _ in detected_collisions:
                    mask = (df1['t'] >= t_col - 0.05) & (df1['t'] <= t_col + 0.05)
                    df1.loc[mask, 'z'] += lift_amount

    output_dir = "safe_trajectories"
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir)
    
    safe_files = []
    for original_path, df in trajectories.items():
        file_name = os.path.basename(original_path)
        out_path = os.path.join(output_dir, f"safe_{file_name}")
       
        df.to_csv(out_path, index=False, sep=',')
        safe_files.append(out_path)
    
    print("-" * 30)
    print("VERIFICATION PHASE:")
    
    all_clear = True
    for i in range(len(safe_files)):
        for j in range(i + 1, len(safe_files)):
            df_safe1 = pd.read_csv(safe_files[i])
            df_safe2 = pd.read_csv(safe_files[j])
            
            final_check = check_collisions(df_safe1, df_safe2, min_dist)
            
            if final_check:
                remaining_times = [c[0] for c in final_check]
                print(f"WARNING: Collision still exists between {os.path.basename(safe_files[i])} and {os.path.basename(safe_files[j])} at {min(remaining_times):.2f}s!")
                all_clear = False
            else:
                print(f"No collisions between {os.path.basename(safe_files[i])} and {os.path.basename(safe_files[j])}")

    if all_clear:
        print("\nSUCCESS: All trajectories are now collision-free!")

if __name__ == "__main__":
    solve_and_verify()