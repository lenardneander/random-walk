from typing import Optional
import matplotlib.pyplot as plt
import numpy as np

from .simulation import Simulation
from .boundaries import BoundaryType

def plot_walks(
    simulation: Simulation,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (9, 7)
) -> plt.Figure:
    """
    Renders 2D or 3D trajectories of all walkers in the simulation.
    """
    dim = simulation.dimension
    fig = plt.figure(figsize=figsize)
    
    if dim == 2:
        ax = fig.add_subplot(111)
        
        for walker in simulation.walkers:
            traj = walker.get_trajectory()
            x, y = traj[:, 0], traj[:, 1]
            color = walker.color or 'blue'
            
            # Trajectory path
            ax.plot(x, y, label=f"Walker {walker.walker_id} (speed={walker.speed})", color=color, alpha=0.8, linewidth=1.5)
            # Start position
            ax.scatter(x[0], y[0], color=color, marker='o', s=60, edgecolors='black', zorder=5)
            # End position
            end_marker = 'x' if walker.active else 'X'
            ax.scatter(x[-1], y[-1], color=color, marker=end_marker, s=80, linewidths=2, zorder=5)

        # Plot boundary box if defined
        bnd = simulation.boundary
        if bnd.boundary_type != BoundaryType.INFINITE and bnd.limits:
            (xmin, xmax), (ymin, ymax) = bnd.limits[:2]
            box_x = [xmin, xmax, xmax, xmin, xmin]
            box_y = [ymin, ymin, ymax, ymax, ymin]
            linestyle = '--' if bnd.boundary_type == BoundaryType.REFLECTIVE else ':'
            box_label = f"Boundary ({bnd.boundary_type.name})"
            ax.plot(box_x, box_y, color='red', linestyle=linestyle, linewidth=2, label=box_label)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_aspect('equal', 'datalim')
        ax.grid(True, linestyle=':', alpha=0.6)
        
    elif dim == 3:
        ax = fig.add_subplot(111, projection='3d')
        
        for walker in simulation.walkers:
            traj = walker.get_trajectory()
            x, y, z = traj[:, 0], traj[:, 1], traj[:, 2]
            color = walker.color or 'blue'
            
            ax.plot(x, y, z, label=f"Walker {walker.walker_id} (speed={walker.speed})", color=color, alpha=0.8, linewidth=1.5)
            ax.scatter(x[0], y[0], z[0], color=color, marker='o', s=60, edgecolors='black', depthshade=False)
            end_marker = 'x' if walker.active else 'X'
            ax.scatter(x[-1], y[-1], z[-1], color=color, marker=end_marker, s=80, linewidths=2, depthshade=False)

        # Plot 3D boundary wireframe box if defined
        bnd = simulation.boundary
        if bnd.boundary_type != BoundaryType.INFINITE and bnd.limits:
            (xmin, xmax), (ymin, ymax), (zmin, zmax) = bnd.limits[:3]
            # 12 edges of cubic bounding box
            edges = [
                ([xmin, xmax], [ymin, ymin], [zmin, zmin]),
                ([xmin, xmax], [ymax, ymax], [zmin, zmin]),
                ([xmin, xmax], [ymin, ymin], [zmax, zmax]),
                ([xmin, xmax], [ymax, ymax], [zmax, zmax]),
                ([xmin, xmin], [ymin, ymax], [zmin, zmin]),
                ([xmax, xmax], [ymin, ymax], [zmin, zmin]),
                ([xmin, xmin], [ymin, ymax], [zmax, zmax]),
                ([xmax, xmax], [ymin, ymax], [zmax, zmax]),
                ([xmin, xmin], [ymin, ymin], [zmin, zmax]),
                ([xmax, xmax], [ymin, ymin], [zmin, zmax]),
                ([xmin, xmin], [ymax, ymax], [zmin, zmax]),
                ([xmax, xmax], [ymax, ymax], [zmin, zmax]),
            ]
            linestyle = '--' if bnd.boundary_type == BoundaryType.REFLECTIVE else ':'
            for i, (ex, ey, ez) in enumerate(edges):
                lbl = f"Boundary ({bnd.boundary_type.name})" if i == 0 else None
                ax.plot(ex, ey, ez, color='red', linestyle=linestyle, linewidth=1.5, label=lbl)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    default_title = f"{dim}D Random Walk Simulation ({simulation.neighborhood_type.name})"
    ax.set_title(title or default_title)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize='small')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig
