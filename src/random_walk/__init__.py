"""
Random Walk Simulation Package (2D)
"""

from .walker import Walker
from .simulation import Simulation, NeighborhoodType
from .visualization import plot_walks

__version__ = "0.1.0"
__all__ = [
    "Walker",
    "Simulation",
    "NeighborhoodType",
    "plot_walks",
]
