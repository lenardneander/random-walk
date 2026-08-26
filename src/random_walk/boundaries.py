from enum import Enum, auto
from typing import Tuple, List, Optional
import numpy as np

class BoundaryType(Enum):
    INFINITE = auto()
    REFLECTIVE = auto()
    ABSORBING = auto()

class Boundary:
    def __init__(
        self,
        dimension: int = 2,
        boundary_type: BoundaryType = BoundaryType.INFINITE,
        limits: Optional[List[Tuple[float, float]]] = None
    ):
        self.dimension = dimension
        self.boundary_type = boundary_type
        
        if limits is None:
            if boundary_type != BoundaryType.INFINITE:
                # Default box: [-10, 10] along each dimension
                self.limits = [(-10.0, 10.0) for _ in range(dimension)]
            else:
                self.limits = []
        else:
            if len(limits) != dimension:
                raise ValueError(f"Expected {dimension} limit tuples, got {len(limits)}")
            self.limits = [(float(low), float(high)) for low, high in limits]

    def is_inside(self, position: np.ndarray) -> bool:
        """Check if position is inside boundary limits."""
        if self.boundary_type == BoundaryType.INFINITE:
            return True
        for i in range(self.dimension):
            low, high = self.limits[i]
            if position[i] < low or position[i] > high:
                return False
        return True

    def process_step(
        self, current_pos: np.ndarray, step_vec: np.ndarray
    ) -> Tuple[np.ndarray, bool]:
        """
        Applies boundary conditions to a proposed step from current_pos using step_vec.
        Returns:
            Tuple[np.ndarray, bool]: (new_position, is_active)
        """
        if self.boundary_type == BoundaryType.INFINITE:
            return current_pos + step_vec, True

        proposed_pos = current_pos + step_vec
        
        if self.boundary_type == BoundaryType.ABSORBING:
            if not self.is_inside(proposed_pos):
                # Clamp to boundary edge and deactivate walker
                clamped_pos = proposed_pos.copy()
                for i in range(self.dimension):
                    low, high = self.limits[i]
                    clamped_pos[i] = np.clip(clamped_pos[i], low, high)
                return clamped_pos, False
            return proposed_pos, True

        elif self.boundary_type == BoundaryType.REFLECTIVE:
            new_pos = proposed_pos.copy()
            for i in range(self.dimension):
                low, high = self.limits[i]
                box_width = high - low
                if box_width <= 0:
                    continue
                # Handle reflective boundary with elastic rebound
                while new_pos[i] < low or new_pos[i] > high:
                    if new_pos[i] < low:
                        new_pos[i] = low + (low - new_pos[i])
                    elif new_pos[i] > high:
                        new_pos[i] = high - (new_pos[i] - high)
            return new_pos, True

        return proposed_pos, True
