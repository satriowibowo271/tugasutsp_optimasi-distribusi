#!/usr/bin/env python3
"""optimize_transportation.py
Pemecahan Transportation Problem untuk studi kasus TokoKita menggunakan PuLP.
"""

import os
import pulp

def main():
    # Indeks
    warehouses = ["W1", "W2"]
    stores = ["S1", "S2", "S3", "S4"]

    # Kapasitas gudang (supply)
    capacity = {"W1": 100, "W2": 150}

    # Permintaan toko (demand)
    demand = {"S1": 80, "S2": 60, "S3": 50, "S4": 40}

    # Biaya per unit c[i][j]
    cost = {
        ("W1", "S1"): 4, ("W1", "S2"): 6, ("W1", "S3"): 8, ("W1", "S4"): 5,
        ("W2", "S1"): 5, ("W2", "S2"): 4, ("W2", "S3"): 3, ("W2", "S4"): 7,
    }

    # Problem
    prob = pulp.LpProblem("Transportation_MinCost", pulp.LpMinimize)

    # Variabel keputusan x_{i,j} >= 0 (continuous)
    x = pulp.LpVariable.dicts("x", (warehouses, stores), lowBound=0, cat="Continuous")

    # Fungsi tujuan
    prob += pulp.lpSum(cost[(i,j)] * x[i][j] for i in warehouses for j in stores), "Total_Transport_Cost"

    # Kendala: supply (kapasitas gudang)
    for i in warehouses:
        prob += pulp.lpSum(x[i][j] for j in stores) <= capacity[i], f"Capacity_{i}"

    # Kendala: demand (kebutuhan toko)
    for j in stores:
        prob += pulp.lpSum(x[i][j] for i in warehouses) == demand[j], f"Demand_{j}"

    # Solve
    solver = pulp.PULP_CBC_CMD(msg=0)  # msg=0 : non-verbose
    prob.solve(solver)

    # Hasil
    status = pulp.LpStatus[prob.status]
    total_cost = pulp.value(prob.objective)
    solution = {(i,j): x[i][j].varValue for i in warehouses for j in stores}

    print("Status:", status)
    print("Total cost (minimum):", total_cost)
    print("\nAllocation (units from warehouse -> store):")
    for i in warehouses:
        for j in stores:
            val = solution[(i,j)]
            if val and val > 0:
                print(f"  {i} -> {j}: {val}")

    # Tulis hasil ke file results/results_example.txt
    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_example.txt')
    with open(out_path, "w") as f:
        f.write(f"Status: {status}\n")
        f.write(f"Total cost (minimum): {total_cost}\n\n")
        f.write("Allocation (units from warehouse -> store):\n")
        for i in warehouses:
            for j in stores:
                val = solution[(i,j)]
                if val and val > 0:
                    f.write(f"{i} -> {j}: {val}\n")

if __name__ == "__main__":
    main()
