from typing import Optional
import matplotlib.pyplot as plt

from .simulation import Simulation

def plot_walks(
    simulation: Simulation,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (9, 7)
) -> plt.Figure:
    """
    Renders 2D trajectories of all walkers in the simulation.
    """
    fig, ax = plt.subplots(figsize=figsize)

    for walker in simulation.walkers:
        traj = walker.get_trajectory()
        x, y = traj[:, 0], traj[:, 1]
        color = walker.color or "#1f77b4"

        # Plot path
        ax.plot(
            x, y,
            label=f"Walker {walker.walker_id} (speed={walker.speed:.1f})",
            color=color,
            alpha=0.8,
            linewidth=1.5
        )
        # Start position marker
        ax.scatter(x[0], y[0], color=color, marker="o", s=60, edgecolors="black", zorder=5)
        # End position marker
        ax.scatter(x[-1], y[-1], color=color, marker="X", s=80, edgecolors="black", zorder=5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle=":", alpha=0.6)
    default_title = f"2D Random Walk Simulation ({simulation.neighborhood_type.name})"
    ax.set_title(title or default_title)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize="small")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig
