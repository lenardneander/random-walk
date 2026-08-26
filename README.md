# Random Walk Simulation

A modern, modular Python repository built from scratch for simulating, analyzing, and visualizing random walks in 2D and 3D.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- **2D and 3D Simulation**: Full support for both 2D planar and 3D spatial random walk trajectories.
- **Neighborhood Movement Patterns**:
  - **von Neumann**: Axis-aligned steps (4 directions in 2D, 6 directions in 3D).
  - **Moore**: Extended grid steps including diagonals (8 directions in 2D, 26 directions in 3D).
- **Custom Boundary Conditions**:
  - `INFINITE`: Unbounded grid space.
  - `REFLECTIVE`: Elastic rebound off user-specified rectangular or cubic bounding boxes.
  - `ABSORBING`: Walker terminates/freezes upon contact with boundary box.
- **Multi-Walker Simulations**: Run multiple independent walkers with variable speeds, colors, and initial positions (origin or randomized).
- **Data Export**: Export trajectory history to pandas DataFrames and CSV files.
- **Visualization**: Beautiful Matplotlib 2D and 3D path plots with start/end markers and boundary outlines.

---

## Project Structure

```
random_walk/
├── LICENSE                    # MIT License
├── README.md                  # Documentation
├── requirements.txt           # Package dependencies
├── pyproject.toml             # Build configuration
├── main.py                    # Main executable entry script
├── src/
│   └── random_walk/
│       ├── __init__.py        # Package exports
│       ├── boundaries.py      # Boundary logic (Infinite, Reflective, Absorbing)
│       ├── walker.py          # Walker class & trajectory tracker
│       ├── simulation.py      # Simulation manager & step generation
│       ├── visualization.py   # Matplotlib 2D/3D plotting routines
│       └── cli.py             # Command line interface parser
└── tests/
    └── test_simulation.py     # Unit test suite
```

---

## Installation

### Prerequisites
- Python 3.8+
- numpy, matplotlib, pandas

### Setup

```bash
cd Documents/DataAnnotation/random_walk
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start & Usage

### 1. Command Line Interface (CLI)

Run a 2D simulation with 5 walkers and reflective boundaries:

```bash
python main.py -d 2 -w 5 -s 100 -n moore -b reflective --output-csv data.csv --output-plot plot.png
```

Run a 3D simulation with absorbing boundaries:

```bash
python main.py -d 3 -w 3 -s 150 -n von_neumann -b absorbing --box-size 15 --output-csv 3d_data.csv --output-plot 3d_plot.png
```

---

### 2. Python API Usage

```python
from random_walk import Simulation, Boundary, BoundaryType, NeighborhoodType, plot_walks

# 1. Configure boundaries
boundary = Boundary(
    dimension=3,
    boundary_type=BoundaryType.REFLECTIVE,
    limits=[(-10.0, 10.0), (-10.0, 10.0), (-10.0, 10.0)]
)

# 2. Initialize simulation
sim = Simulation(
    dimension=3,
    neighborhood_type=NeighborhoodType.MOORE,
    boundary=boundary,
    seed=42
)

# 3. Add walkers
sim.create_walkers(num_walkers=4)

# 4. Execute simulation steps
sim.run(num_steps=100)

# 5. Export data to CSV
sim.save_csv("trajectory_results.csv")

# 6. Plot trajectories
plot_walks(sim, save_path="trajectory_plot.png", show=True)
```

---

## Running Tests

Execute unit tests with unittest:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## License

This project is licensed under the [MIT License](LICENSE).
