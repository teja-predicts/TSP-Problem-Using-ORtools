
# Smart Delivery Route Optimizer (TSP Solver with OR-Tools)

This project solves the **Traveling Salesman Problem (TSP)** using **Google OR-Tools**, based on real logistics data from [Kaggle's Large-Scale Route Optimization dataset](https://www.kaggle.com/datasets/mexwell/large-scale-route-optimization).

It calculates the most efficient route between cities to minimize total travel distance.

---

## 📁 Dataset Used

Download from Kaggle:
- `order_small.csv`: List of delivery orders with source and destination cities
- `distance.csv`: Pairwise distances (in meters) between cities



---

## Project Structure

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

##  How to Run This Project

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

## What This Project Does

- Reads city-level delivery and distance data
- Builds a distance matrix
- Solves TSP using Google OR-Tools
- Outputs the optimal route as a CSV
  

---

## requirements.txt

```text
pandas
ortools
```

---

## Example Output (`tsp_route.csv`)

```csv
TSP_Route
City_61
City_34
City_45
City_12
City_61
```

---

## Next Steps (Enhancement Ideas)

- Convert to VRP: multiple vehicles and capacity limits
- Visualize results using `folium` or `geopandas`
- Optimize runtime using heuristics or GurobiPy

---

## Credits

- Dataset: [Kaggle - Large-Scale Route Optimization](https://www.kaggle.com/datasets/mexwell/large-scale-route-optimization)
- Solver: [Google OR-Tools](https://developers.google.com/optimization)

---


