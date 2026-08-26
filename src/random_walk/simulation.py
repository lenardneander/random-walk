from enum import Enum, auto
from typing import List, Optional, Union, Dict, Any
import itertools
import numpy as np
import pandas as pd

from .boundaries import Boundary, BoundaryType
from .walker import Walker

class NeighborhoodType(Enum):
    VON_NEUMANN = auto()  # Axis-aligned steps
    MOORE = auto()        # Includes diagonal steps

class Simulation:
    """
    Main Simulation manager for multiple random walkers in 2D or 3D.
    """
    def __init__(
        self,
        dimension: int = 2,
        neighborhood_type: NeighborhoodType = NeighborhoodType.VON_NEUMANN,
        boundary: Optional[Boundary] = None,
        seed: Optional[int] = None
    ):
        if dimension not in (2, 3):
            raise ValueError("Dimension must be 2 or 3.")
            
        self.dimension = dimension
        self.neighborhood_type = neighborhood_type
        self.boundary = boundary or Boundary(dimension=dimension, boundary_type=BoundaryType.INFINITE)
        self.rng = np.random.default_rng(seed)
        self.walkers: List[Walker] = []
        self.step_set = self._generate_step_set()

    def _generate_step_set(self) -> np.ndarray:
        """Generates the set of allowable unit step vectors."""
        if self.neighborhood_type == NeighborhoodType.VON_NEUMANN:
            steps = []
            for i in range(self.dimension):
                pos_step = [0] * self.dimension
                neg_step = [0] * self.dimension
                pos_step[i] = 1
                neg_step[i] = -1
                steps.append(pos_step)
                steps.append(neg_step)
            return np.array(steps, dtype=float)
            
        elif self.neighborhood_type == NeighborhoodType.MOORE:
            combos = list(itertools.product([-1, 0, 1], repeat=self.dimension))
            # Remove zero vector
            zero_vec = (0,) * self.dimension
            combos = [c for c in combos if c != zero_vec]
            return np.array(combos, dtype=float)

        else:
            raise ValueError(f"Unknown neighborhood type: {self.neighborhood_type}")

    def add_walker(self, walker: Walker) -> None:
        if walker.dimension != self.dimension:
            raise ValueError(f"Walker dimension ({walker.dimension}) does not match simulation ({self.dimension}).")
        self.walkers.append(walker)

    def create_walkers(
        self,
        num_walkers: int,
        start_positions: Optional[Union[np.ndarray, List[List[float]]]] = None,
        speeds: Optional[List[float]] = None,
        colors: Optional[List[str]] = None
    ) -> List[Walker]:
        """Convenience factory to create and add multiple walkers."""
        new_walkers = []
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]
        
        for i in range(num_walkers):
            w_id = i + 1
            
            if start_positions is not None:
                pos = np.array(start_positions[i], dtype=float)
            else:
                pos = np.zeros(self.dimension, dtype=float)

            speed = speeds[i] if (speeds is not None and i < len(speeds)) else 1.0
            color = colors[i] if (colors is not None and i < len(colors)) else palette[i % len(palette)]

            w = Walker(walker_id=w_id, initial_position=pos, speed=speed, color=color)
            self.add_walker(w)
            new_walkers.append(w)
            
        return new_walkers

    def step(self) -> None:
        """Executes a single simulation step for all active walkers."""
        num_steps_available = len(self.step_set)
        
        for walker in self.walkers:
            if not walker.active:
                # Retain position if absorbed/inactive
                walker.record_position(walker.position, active=False)
                continue
                
            idx = self.rng.integers(0, num_steps_available)
            raw_direction = self.step_set[idx]
            step_vec = raw_direction * walker.speed
            
            new_pos, is_active = self.boundary.process_step(walker.position, step_vec)
            walker.record_position(new_pos, active=is_active)

    def run(self, num_steps: int) -> None:
        """Runs simulation for specified number of steps."""
        for _ in range(num_steps):
            self.step()

    def to_dataframe(self) -> pd.DataFrame:
        """Exports trajectory data of all walkers to pandas DataFrame."""
        rows = []
        for walker in self.walkers:
            trajectory = walker.get_trajectory()
            for step_idx, pos in enumerate(trajectory):
                row: Dict[str, Any] = {
                    "step": step_idx,
                    "walker_id": walker.walker_id,
                    "x": pos[0],
                    "y": pos[1],
                    "speed": walker.speed,
                    "active": walker.active if step_idx == len(trajectory) - 1 else True
                }
                if self.dimension == 3:
                    row["z"] = pos[2]
                rows.append(row)
        return pd.DataFrame(rows)

    def save_csv(self, filepath: str) -> None:
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)

    def get_summary(self) -> List[Dict[str, Any]]:
        """Calculates summary metrics for all walkers."""
        summaries = []
        for walker in self.walkers:
            traj = walker.get_trajectory()
            start_pos = traj[0]
            final_pos = traj[-1]
            displacement = float(np.linalg.norm(final_pos - start_pos))
            max_distance = float(np.max(np.linalg.norm(traj - start_pos, axis=1)))
            
            summaries.append({
                "walker_id": walker.walker_id,
                "start_position": start_pos.tolist(),
                "final_position": final_pos.tolist(),
                "displacement": displacement,
                "max_distance_from_origin": max_distance,
                "total_steps": len(traj) - 1,
                "active": walker.active
            })
        return summaries
