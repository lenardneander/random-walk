from typing import List, Optional, Tuple, Union
import numpy as np

class Walker:
    """
    Represents an individual random walker.
    """
    def __init__(
        self,
        walker_id: Union[int, str],
        initial_position: np.ndarray,
        speed: float = 1.0,
        color: Optional[str] = None
    ):
        self.walker_id = walker_id
        self.position = np.array(initial_position, dtype=float)
        self.speed = float(speed)
        self.color = color
        self.active = True
        self.history: List[np.ndarray] = [self.position.copy()]

    @property
    def dimension(self) -> int:
        return len(self.position)

    def record_position(self, new_position: np.ndarray, active: bool = True) -> None:
        self.position = np.array(new_position, dtype=float)
        self.active = active
        self.history.append(self.position.copy())

    def get_trajectory(self) -> np.ndarray:
        """Returns trajectory as 2D numpy array of shape (num_steps + 1, dimension)."""
        return np.array(self.history)
