from typing import List, Optional, Union
import numpy as np

class Walker:
    """
    Represents an individual 2D random walker.
    """
    def __init__(
        self,
        walker_id: Union[int, str],
        initial_position: Union[np.ndarray, List[float], tuple] = (0.0, 0.0),
        speed: float = 1.0,
        color: Optional[str] = None
    ):
        self.walker_id = walker_id
        pos = np.array(initial_position, dtype=float)
        if pos.shape != (2,):
            raise ValueError("Position must be a 2D coordinate (x, y).")
        self.position = pos
        self.speed = float(speed)
        self.color = color
        self.history: List[np.ndarray] = [self.position.copy()]

    def record_step(self, step_vector: np.ndarray) -> None:
        """Move walker by step_vector scaled by speed and record in history."""
        self.position = self.position + step_vector * self.speed
        self.history.append(self.position.copy())

    def get_trajectory(self) -> np.ndarray:
        """Returns trajectory as 2D numpy array of shape (num_steps + 1, 2)."""
        return np.array(self.history)
