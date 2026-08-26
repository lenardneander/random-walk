from enum import Enum, auto
from typing import List, Optional, Union, Dict, Any
import itertools
import numpy as np
import pandas as pd

from .walker import Walker

class NeighborhoodType(Enum):
    VON_NEUMANN = auto()  # 4 directions: (dx, dy) in {(-1,0), (1,0), (0,-1), (0,1)}
    MOORE = auto()        # 8 directions: includes diagonals

class Simulation:
    """
    2D Random Walk Simulation manager for multiple walkers.
    """
    def __init__(
        self,
        neighborhood_type: NeighborhoodType = NeighborhoodType.VON_NEUMANN,
        seed: Optional[int] = None
    ):
        self.neighborhood_type = neighborhood_type
        self.rng = np.random.default_rng(seed)
        self.walkers: List[Walker] = []
        self.step_set = self._generate_step_set()

    def _generate_step_set(self) -> np.ndarray:
        """Generates allowable 2D unit step vectors."""
        if self.neighborhood_type == NeighborhoodType.VON_NEUMANN:
            return np.array([
                [-1.0, 0.0], [1.0, 0.0],
                [0.0, -1.0], [0.0, 1.0]
            ], dtype=float)
        elif self.neighborhood_type == NeighborhoodType.MOORE:
            combos = [
                (dx, dy) for dx, dy in itertools.product([-1.0, 0.0, 1.0], repeat=2)
                if (dx, dy) != (0.0, 0.0)
            ]
            return np.array(combos, dtype=float)
        else:
            raise ValueError(f"Unknown neighborhood type: {self.neighborhood_type}")

    def add_walker(self, walker: Walker) -> None:
        self.walkers.append(walker)

    def create_walkers(
        self,
        num_walkers: int,
        start_positions: Optional[Union[np.ndarray, List[List[float]]]] = None,
        speeds: Optional[List[float]] = None,
        colors: Optional[List[str]] = None,
        random_starts: bool = False,
        random_start_range: float = 10.0,
        random_speeds: bool = False,
        speed_range: tuple = (0.5, 3.0)
    ) -> List[Walker]:
        """Convenience factory to generate and register multiple walkers."""
        new_walkers = []
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]

        for i in range(num_walkers):
            w_id = i + 1

            # Determine position
            if random_starts:
                pos = self.rng.uniform(-random_start_range, random_start_range, size=2)
            elif start_positions is not None:
                pos = np.array(start_positions[i], dtype=float)
            else:
                pos = np.array([0.0, 0.0], dtype=float)

            # Determine speed
            if random_speeds:
                speed = float(self.rng.uniform(speed_range[0], speed_range[1]))
            elif speeds is not None and i < len(speeds):
                speed = float(speeds[i])
            else:
                speed = 1.0

            # Determine color
            color = colors[i] if (colors is not None and i < len(colors)) else palette[i % len(palette)]

            w = Walker(walker_id=w_id, initial_position=pos, speed=speed, color=color)
            self.add_walker(w)
            new_walkers.append(w)

        return new_walkers

    def step(self) -> None:
        """Executes a single step for all walkers."""
        num_steps_avail = len(self.step_set)
        for walker in self.walkers:
            idx = self.rng.integers(0, num_steps_avail)
            step_vec = self.step_set[idx]
            walker.record_step(step_vec)

    def run(self, num_steps: int) -> None:
        """Runs simulation for a given number of steps."""
        for _ in range(num_steps):
            self.step()

    def to_dataframe(self) -> pd.DataFrame:
        """Exports trajectory data for all walkers into a pandas DataFrame."""
        rows = []
        for walker in self.walkers:
            trajectory = walker.get_trajectory()
            for step_idx, pos in enumerate(trajectory):
                rows.append({
                    "step": step_idx,
                    "walker_id": walker.walker_id,
                    "x": pos[0],
                    "y": pos[1],
                    "speed": walker.speed
                })
        return pd.DataFrame(rows)

    def save_csv(self, filepath: str) -> None:
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)

    def get_summary(self) -> List[Dict[str, Any]]:
        """Calculates summary statistics for all walkers."""
        summaries = []
        for walker in self.walkers:
            traj = walker.get_trajectory()
            start_pos = traj[0]
            final_pos = traj[-1]
            displacement = float(np.linalg.norm(final_pos - start_pos))
            max_dist = float(np.max(np.linalg.norm(traj - start_pos, axis=1)))

            summaries.append({
                "walker_id": walker.walker_id,
                "start_position": start_pos.tolist(),
                "final_position": final_pos.tolist(),
                "displacement": displacement,
                "max_distance": max_dist,
                "steps": len(traj) - 1,
                "speed": walker.speed
            })
        return summaries
