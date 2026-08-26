import argparse
import sys
import numpy as np

from .simulation import Simulation, NeighborhoodType
from .boundaries import Boundary, BoundaryType
from .visualization import plot_walks

def main():
    parser = argparse.ArgumentParser(
        description="Simulate 2D or 3D random walks with customizable parameters, boundaries, and outputs."
    )
    parser.add_argument("-d", "--dimension", type=int, choices=[2, 3], default=2, help="Grid dimension (2 or 3)")
    parser.add_argument("-w", "--num-walkers", type=int, default=5, help="Number of random walkers")
    parser.add_argument("-s", "--num-steps", type=int, default=100, help="Number of steps per walker")
    parser.add_argument(
        "-n", "--neighborhood", type=str, choices=["von_neumann", "moore"], default="von_neumann",
        help="Neighborhood movement pattern (von_neumann or moore)"
    )
    parser.add_argument(
        "-b", "--boundary", type=str, choices=["infinite", "reflective", "absorbing"], default="infinite",
        help="Boundary condition mode"
    )
    parser.add_argument("--box-size", type=float, default=15.0, help="Boundary box half-width (defines [-box_size, box_size])")
    parser.add_argument("--random-start", action="store_true", help="Randomize initial walker positions within boundary")
    parser.add_argument("--seed", type=int, default=None, help="Random number generator seed")
    parser.add_argument("--output-csv", type=str, default=None, help="File path to export trajectory CSV data")
    parser.add_argument("--output-plot", type=str, default=None, help="File path to save trajectory plot image")
    parser.add_argument("--no-show", action="store_true", help="Do not display plot interactively")

    args = parser.parse_args()

    # Map neighborhood enum
    n_type = NeighborhoodType.VON_NEUMANN if args.neighborhood == "von_neumann" else NeighborhoodType.MOORE

    # Map boundary enum
    b_type_map = {
        "infinite": BoundaryType.INFINITE,
        "reflective": BoundaryType.REFLECTIVE,
        "absorbing": BoundaryType.ABSORBING
    }
    b_type = b_type_map[args.boundary]

    limits = [(-args.box_size, args.box_size) for _ in range(args.dimension)] if b_type != BoundaryType.INFINITE else None
    boundary = Boundary(dimension=args.dimension, boundary_type=b_type, limits=limits)

    sim = Simulation(dimension=args.dimension, neighborhood_type=n_type, boundary=boundary, seed=args.seed)

    # Determine starting positions
    if args.random_start and b_type != BoundaryType.INFINITE:
        rng = np.random.default_rng(args.seed)
        start_positions = rng.uniform(-args.box_size * 0.8, args.box_size * 0.8, size=(args.num_walkers, args.dimension))
    else:
        start_positions = np.zeros((args.num_walkers, args.dimension))

    sim.create_walkers(num_walkers=args.num_walkers, start_positions=start_positions)
    
    print(f"Starting simulation ({args.dimension}D, {n_type.name}, {b_type.name} boundary, {args.num_walkers} walkers, {args.num_steps} steps)...")
    sim.run(args.num_steps)
    print("Simulation completed.")

    # Output metrics summary
    summaries = sim.get_summary()
    for s in summaries:
        print(f" Walker {s['walker_id']}: Start={s['start_position']}, End={s['final_position']}, Displacement={s['displacement']:.2f}, Active={s['active']}")

    if args.output_csv:
        sim.save_csv(args.output_csv)
        print(f"Data saved to CSV: {args.output_csv}")

    plot_walks(sim, save_path=args.output_plot, show=not args.no_show)

if __name__ == "__main__":
    main()
