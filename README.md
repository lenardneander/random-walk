# Random Walk Simulation

A modern Python repository built from scratch for simulating, analyzing, and visualizing 2D random walks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- **Multi-Walker Simulation**: Simulate multiple random walkers simultaneously.
- **Speed & Starting Point Randomization**: Support for custom or randomized walker speeds and initial starting positions.
- **Neighborhood Movement Patterns**:
  - **von Neumann**: 4 axis-aligned directions (up, down, left, right).
  - **Moore**: 8 directions including diagonals.
- **Custom Color Palette**: Automatic or custom color assignment per walker for clear visualization.
- **Data Export**: Export trajectory data to pandas DataFrames and CSV files.
- **Plotting**: Matplotlib 2D trajectory plots with start (O) and end (X) markers.
- **Multiple Runs**: Option to automatically run simulations multiple times and export plots and CSVs for each run.

---

## Project Structure

```
random_walk/
├── LICENSE                    # MIT License
├── README.md                  # Documentation
├── requirements.txt           # Package dependencies
├── pyproject.toml             # Build configuration
├── main.py                    # Main executable script
├── src/
│   └── random_walk/
│       ├── __init__.py        # Package exports
│       ├── walker.py          # Walker class & trajectory tracker
│       ├── simulation.py      # Simulation manager & step generator
│       ├── visualization.py   # Matplotlib 2D plotting module
│       └── cli.py             # Command Line Interface
└── tests/
    └── test_simulation.py     # Unit test suite
```

---

## Installation

```bash
cd Documents/DataAnnotation/random_walk
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start & Usage

### 1. Command Line Interface (CLI)

Run a 2D simulation with 5 walkers, randomized speeds, and randomized starting points:

```bash
python main.py -w 5 -s 100 -n moore --random-start --random-speed --output-csv data.csv --output-plot plot.png
```

Run 3 simulation runs automatically:

```bash
python main.py -w 4 -s 50 --runs 3 --output-csv run.csv --output-plot run.png
```

#### CLI Options Summary

| Option | Description | Default |
| :--- | :--- | :--- |
| `-w`, `--num-walkers` | Number of random walkers | `5` |
| `-s`, `--num-steps` | Number of steps per walker | `100` |
| `-n`, `--neighborhood` | Neighborhood pattern (`von_neumann` or `moore`) | `von_neumann` |
| `--random-start` | Randomize initial starting positions | `False` |
| `--random-speed` | Randomize walker speeds | `False` |
| `--runs` | Number of simulation runs to execute | `1` |
| `--seed` | Random number generator seed | `None` |
| `--output-csv` | Filepath to export CSV data | `None` |
| `--output-plot` | Filepath to save plot image | `None` |

---

### 2. Python API Usage

```python
from random_walk import Simulation, NeighborhoodType, plot_walks

# 1. Initialize simulation with Moore neighborhood (8 directions)
sim = Simulation(neighborhood_type=NeighborhoodType.MOORE, seed=42)

# 2. Create walkers with randomized speeds and starting points
sim.create_walkers(num_walkers=5, random_starts=True, random_speeds=True)

# 3. Execute 100 steps
sim.run(num_steps=100)

# 4. Save results to CSV
sim.save_csv("trajectory_data.csv")

# 5. Plot trajectories
plot_walks(sim, save_path="random_walk_plot.png", show=True)
```

---

## Running Tests

Execute unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## License

This project is licensed under the [MIT License](LICENSE).
