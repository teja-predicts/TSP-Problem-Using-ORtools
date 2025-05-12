import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# === Step 1: Load data ===
orders = pd.read_csv("data/order_small.csv")
distances = pd.read_csv("data/distance.csv")

# === Step 2: Create list of unique cities involved ===
cities = sorted(set(distances["Source"]).union(set(distances["Destination"])))
city_idx = {city: idx for idx, city in enumerate(cities)}
idx_city = {v: k for k, v in city_idx.items()}

# === Step 3: Build distance matrix ===
n = len(cities)
matrix = [[0]*n for _ in range(n)]

for _, row in distances.iterrows():
    i = city_idx[row["Source"]]
    j = city_idx[row["Destination"]]
    dist = row["Distance(M)"]
    matrix[i][j] = dist
    matrix[j][i] = dist  # assuming symmetric distances

# === Step 4: OR-Tools TSP solver ===
manager = pywrapcp.RoutingIndexManager(n, 1, 0)
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    return matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


search_params = pywrapcp.DefaultRoutingSearchParameters()
search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

solution = routing.SolveWithParameters(search_params)

# === Step 5: Extract and Save Route ===
route = []
if solution:
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(idx_city[node])
        index = solution.Value(routing.NextVar(index))
    route.append(idx_city[manager.IndexToNode(index)])

    # Save to CSV
    pd.DataFrame({"TSP_Route": route}).to_csv("outputs/tsp_route.csv", index=False)
    print("✅ Optimized route saved to outputs/tsp_route.csv")
else:
    print("No solution found.")
