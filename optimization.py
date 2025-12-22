from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from collision_detection import check_collisions

def insert_wait_at_collision(df, t_collision, wait_time):
    df = df.copy().reset_index(drop=True)
    
    # Pretpostavljamo uniformni dt iz podataka ili fiksni 0.1s
    dt = 0.1
    if len(df) > 1:
        dt = np.round(df["t"].iloc[1] - df["t"].iloc[0], 2)

    # Pronađi indeks najbliži sudaru
    idx = (df['t'] - t_collision).abs().idxmin()
    
    # Pomakni točku čekanja jedan korak unatrag (idx - 1)  kako bi dron stao PRIJE nego što uđe u zonu sudara
    wait_idx = max(0, idx - 1)
    t_start_waiting = df.loc[wait_idx, "t"]
    
    df_before = df.iloc[:wait_idx + 1].copy()
    df_after = df.iloc[wait_idx + 1:].copy()
    
    # Generiraj redove za mirovanje (hovering)
    wait_steps = int(np.ceil(wait_time / dt))
    last_pos = df_before.iloc[-1]
    
    wait_data = []
    for k in range(1, wait_steps + 1):
        wait_data.append({
            "t": t_start_waiting + (k * dt),
            "x": last_pos["x"],
            "y": last_pos["y"],
            "z": last_pos["z"],
            "yaw": last_pos["yaw"] if "yaw" in df.columns else 0.0
        })
    
    df_wait = pd.DataFrame(wait_data)
    
    # Pomakni vrijeme za cijeli ostatak trajektorije
    df_after["t"] += wait_time
    
    return pd.concat([df_before, df_wait, df_after], ignore_index=True)

def solve_collision_with_cpsat(i, j):
   
    model = cp_model.CpModel()
    
    # Varijabla: tko će čekati (0 ili 1)
    who_waits = model.NewIntVar(0, 1, f"who_waits_{i}_{j}")
    
    # Ovdje možeš dodati kompleksnije uvjete. 
    # Trenutno: minimiziramo varijablu što će dati prednost dronu j.
    model.Minimize(who_waits)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.Value(who_waits)
    return 0

def time_shift_cp_sat(dfs_interp, min_dist=0.2, max_wait=5.0):
    
    num_drones = len(dfs_interp)
    optimized_dfs = [df.copy() for df in dfs_interp]
    
    # Sigurnosni brojač iteracija
    max_iterations = 15
    
    for iteration in range(max_iterations):
        collision_found = False
        
        for i in range(num_drones):
            for j in range(i + 1, num_drones):
                # Provjera sudara
                collisions = check_collisions(optimized_dfs[i], optimized_dfs[j], min_dist)
                
                if collisions:
                    collision_found = True
                    t_coll, dist = collisions[0]
                    
                    print(f"  [Iteracija {iteration}] Sudar drona {i} i {j} na t={t_coll:.2f}s (razmak {dist:.3f}m)")
                    
                    # CP-SAT odluka
                    decision = solve_collision_with_cpsat(i, j)
                    
                    if decision == 0:
                        print(f"    -> CP-SAT odlučio: Dron {i} čeka.")
                        optimized_dfs[i] = insert_wait_at_collision(optimized_dfs[i], t_coll, max_wait)
                    else:
                        print(f"    -> CP-SAT odlučio: Dron {j} čeka.")
                        optimized_dfs[j] = insert_wait_at_collision(optimized_dfs[j], t_coll, max_wait)
                    
                    # Čim se dogodi jedna promjena, izlazi i re-evaluiraj sve
                    break
            if collision_found: break
            
        if not collision_found:
            print("\n  Čestitamo: Svi sudari su uspješno izbjegnuti!")
            break
            
    return optimized_dfs