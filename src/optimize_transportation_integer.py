#!/usr/bin/env python3
"""optimize_transportation_integer.py
Versi integer (semua x_{i,j} harus integer) menggunakan PuLP.
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

    prob = pulp.LpProblem("Transportation_MinCost_Integer", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", (warehouses, stores), lowBound=0, cat="Integer")


    prob += pulp.lpSum(cost[(i,j)] * x[i][j] for i in warehouses for j in stores), "Total_Transport_Cost"

    for i in warehouses:
        prob += pulp.lpSum(x[i][j] for j in stores) <= capacity[i], f"Capacity_{i}"

    for j in stores:
        prob += pulp.lpSum(x[i][j] for i in warehouses) == demand[j], f"Demand_{j}"

    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)

    status = pulp.LpStatus[prob.status]
    total_cost = pulp.value(prob.objective)
    solution = {(i,j): x[i][j].varValue for i in warehouses for j in stores}

    print("Status:", status)
    print("Total cost (minimum):", total_cost)
    print("Allocation:")
    for i in warehouses:
        for j in stores:
            val = solution[(i,j)]
            if val and val > 0:
                print(f"  {i} -> {j}: {val}")

    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_integer.txt')
    with open(out_path, "w") as f:
        f.write(f"Status: {status}\nTotal cost: {total_cost}\n\nAllocation:\n")
        for i in warehouses:
            for j in stores:
                val = solution[(i,j)]
                if val and val > 0:
                    f.write(f"{i} -> {j}: {val}\n")

if __name__ == "__main__":
    main()
