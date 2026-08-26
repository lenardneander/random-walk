import argparse
import os
from .simulation import Simulation, NeighborhoodType
from .visualization import plot_walks

def main():
    parser = argparse.ArgumentParser(
        description="Simulate 2D random walks with multiple walkers, customizable speeds, start points, and neighborhoods."
    )
    parser.add_argument("-w", "--num-walkers", type=int, default=5, help="Number of random walkers")
    parser.add_argument("-s", "--num-steps", type=int, default=100, help="Number of steps per walker")
    parser.add_argument(
        "-n", "--neighborhood", type=str, choices=["von_neumann", "moore"], default="von_neumann",
        help="Neighborhood movement pattern (von_neumann: 4 directions, moore: 8 directions)"
    )
    parser.add_argument("--random-start", action="store_true", help="Randomize walker starting positions")
    parser.add_argument("--random-speed", action="store_true", help="Randomize walker speeds")
    parser.add_argument("--runs", type=int, default=1, help="Number of simulation runs to execute")
    parser.add_argument("--seed", type=int, default=None, help="Random number generator seed")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory where generated output files are stored")
    parser.add_argument("--output-csv", type=str, default=None, help="Filename or path to export trajectory CSV data")
    parser.add_argument("--output-plot", type=str, default=None, help="Filename or path to save trajectory plot image")
    parser.add_argument("--no-show", action="store_true", help="Do not display plot interactively")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    n_type = NeighborhoodType.VON_NEUMANN if args.neighborhood == "von_neumann" else NeighborhoodType.MOORE

    for run_idx in range(args.runs):
        run_prefix = f"Run {run_idx + 1}/{args.runs}: " if args.runs > 1 else ""
        print(f"{run_prefix}Starting simulation (2D, {n_type.name}, {args.num_walkers} walkers, {args.num_steps} steps)...")

        sim = Simulation(neighborhood_type=n_type, seed=args.seed)
        sim.create_walkers(
            num_walkers=args.num_walkers,
            random_starts=args.random_start,
            random_speeds=args.random_speed
        )

        sim.run(args.num_steps)
        print(f"{run_prefix}Simulation completed.")

        for s in sim.get_summary():
            w_id = s["walker_id"]
            start_p = s["start_position"]
            final_p = s["final_position"]
            speed = s["speed"]
            disp = s["displacement"]
            print(f"  Walker {w_id}: Start={start_p}, End={final_p}, Speed={speed:.2f}, Displacement={disp:.2f}")

        # Determine CSV output path
        csv_filename = args.output_csv or "data.csv"
        if args.runs > 1:
            csv_filename = f"run_{run_idx + 1}_{csv_filename}"
        csv_path = os.path.join(args.output_dir, os.path.basename(csv_filename)) if not os.path.isabs(csv_filename) else csv_filename

        sim.save_csv(csv_path)
        print(f"Data saved to CSV: {csv_path}")

        # Determine Plot output path
        plot_filename = args.output_plot or "plot.png"
        if args.runs > 1:
            plot_filename = f"run_{run_idx + 1}_{plot_filename}"
        plot_path = os.path.join(args.output_dir, os.path.basename(plot_filename)) if not os.path.isabs(plot_filename) else plot_filename

        plot_walks(sim, save_path=plot_path, show=not args.no_show)

if __name__ == "__main__":
    main()
