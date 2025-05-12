
# 🚚 Smart Delivery Route Optimizer (TSP Solver with OR-Tools)

This project solves the **Traveling Salesman Problem (TSP)** using **Google OR-Tools**, based on real logistics data from [Kaggle's Large-Scale Route Optimization dataset](https://www.kaggle.com/datasets/mexwell/large-scale-route-optimization).

It calculates the most efficient route between cities to minimize total travel distance.

---

## 📁 Dataset Used

Download from Kaggle:
- `order_small.csv`: List of delivery orders with source and destination cities
- `distance.csv`: Pairwise distances (in meters) between cities

Place both files in a folder called `data/`.

---

## 📦 Project Structure

```
route-optimizer/
├── data/
│   ├── order_small.csv
│   └── distance.csv
├── scripts/
│   └── tsp_solver.py
├── outputs/
│   └── tsp_route.csv
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run This Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the TSP solver script

```bash
python scripts/tsp_solver.py
```

### 3. View the result

Output will be saved to:

```
outputs/tsp_route.csv
```

---

## 🧠 What This Project Does

- ✅ Reads city-level delivery and distance data
- ✅ Builds a distance matrix
- ✅ Solves TSP using Google OR-Tools
- ✅ Outputs the optimal route as a CSV
- ✅ (Optional): Can be extended to multi-truck VRP later

---

## 📜 Full Code: `scripts/tsp_solver.py`

```python
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import os

# === Load Data ===
orders = pd.read_csv("data/order_small.csv")
distances = pd.read_csv("data/distance.csv")

# === Build City List and Index Mappings ===
cities = sorted(set(distances["Source"]).union(set(distances["Destination"])))
city_idx = {city: idx for idx, city in enumerate(cities)}
idx_city = {v: k for k, v in city_idx.items()}

# === Build Distance Matrix ===
n = len(cities)
matrix = [[0] * n for _ in range(n)]

for _, row in distances.iterrows():
    i = city_idx[row["Source"]]
    j = city_idx[row["Destination"]]
    dist = row["Distance(M)"]
    matrix[i][j] = dist
    matrix[j][i] = dist  # symmetric

# === OR-Tools TSP Solver ===
manager = pywrapcp.RoutingIndexManager(n, 1, 0)
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    return matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_params = pywrapcp.DefaultRoutingSearchParameters()
search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

solution = routing.SolveWithParameters(search_params)

# === Extract and Save Route ===
route = []
if solution:
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(idx_city[node])
        index = solution.Value(routing.NextVar(index))
    route.append(idx_city[manager.IndexToNode(index)])

    os.makedirs("outputs", exist_ok=True)
    pd.DataFrame({"TSP_Route": route}).to_csv("outputs/tsp_route.csv", index=False)
    print("✅ Optimized route saved to outputs/tsp_route.csv")
else:
    print("❌ No solution found.")
```

---

## 📄 requirements.txt

```text
pandas
ortools
```

---

## ✅ Example Output (`tsp_route.csv`)

```csv
TSP_Route
City_61
City_34
City_45
City_12
City_61
```

---

## 🚀 Next Steps (Enhancement Ideas)

- ➕ Convert to VRP: multiple vehicles and capacity limits
- 📦 Use weight/demand from `order_small.csv`
- 🕒 Add delivery time windows using the `Deadline` column
- 🗺️ Visualize results using `folium` or `geopandas`
- 📈 Optimize runtime using heuristics or GurobiPy

---

## 🙌 Credits

- 📦 Dataset: [Kaggle - Large-Scale Route Optimization](https://www.kaggle.com/datasets/mexwell/large-scale-route-optimization)
- 🧠 Solver: [Google OR-Tools](https://developers.google.com/optimization)

---

## 📄 License

MIT License
