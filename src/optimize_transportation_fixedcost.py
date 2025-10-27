#!/usr/bin/env python3
"""optimize_transportation_fixedcost.py
Menambahkan fixed cost per gudang yang digunakan. Gunakan MIP (binary y_i).
Jika gudang i mengirim >0 unit, y_i = 1 dan kita incur fixed_cost[i].
"""
import os
import pulp

def main():
    warehouses = ["W1", "W2"]
    stores = ["S1", "S2", "S3", "S4"]

    capacity = {"W1": 100, "W2": 150}
    demand = {"S1": 80, "S2": 60, "S3": 50, "S4": 40}

    cost = {
        ("W1", "S1"): 4, ("W1", "S2"): 6, ("W1", "S3"): 8, ("W1", "S4"): 5,
        ("W2", "S1"): 5, ("W2", "S2"): 4, ("W2", "S3"): 3, ("W2", "S4"): 7,
    }

    fixed_cost = {"W1": 200, "W2": 150}  # biaya tetap jika gudang dipakai

    prob = pulp.LpProblem("Transportation_MinCost_FixedCost", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", (warehouses, stores), lowBound=0, cat="Continuous")
    y = pulp.LpVariable.dicts("y", warehouses, cat="Binary")  # 1 jika gudang dipakai

    # Big-M approach: cap* y >= sum x
    prob += (pulp.lpSum(cost[(i,j)] * x[i][j] for i in warehouses for j in stores)
             + pulp.lpSum(fixed_cost[i] * y[i] for i in warehouses)), "Total_Cost_With_Fixed"

    for i in warehouses:
        prob += pulp.lpSum(x[i][j] for j in stores) <= capacity[i]*y[i], f"Cap_link_{i}"

    for j in stores:
        prob += pulp.lpSum(x[i][j] for i in warehouses) == demand[j], f"Demand_{j}"

    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)

    status = pulp.LpStatus[prob.status]
    total_cost = pulp.value(prob.objective)
    solution = {(i,j): x[i][j].varValue for i in warehouses for j in stores}
    used = {i: y[i].varValue for i in warehouses}

    print("Status:", status)
    print("Total cost (with fixed costs):", total_cost)
    print("Used warehouses:")
    for i in warehouses:
        print(f"  {i}: {used[i]}")
    print("Allocations:")
    for i in warehouses:
        for j in stores:
            val = solution[(i,j)]
            if val and val > 0:
                print(f"  {i} -> {j}: {val}")

    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_fixedcost.txt')
    with open(out_path, "w") as f:
        f.write(f"Status: {status}\nTotal cost: {total_cost}\n\nUsed warehouses:\n")
        for i in warehouses:
            f.write(f"{i}: {used[i]}\n")
        f.write("\nAllocations:\n")
        for i in warehouses:
            for j in stores:
                val = solution[(i,j)]
                if val and val > 0:
                    f.write(f"{i} -> {j}: {val}\n")

if __name__ == "__main__":
    main()
