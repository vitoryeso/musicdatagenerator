"""loop_creator.py

Circular Loop Simulator
=======================

This module provides a minimal yet flexible physics simulator capable of generating
2-D circular (or near-circular) trajectories that respect:

1. Elasticity (Hookean restoring force)
2. Moment of inertia (i.e. classical Newtonian second law for a point mass)
3. Fluidity / damping (viscous friction)
4. Softening of the material (parameter that effectively reduces the spring
   constant over time)

The goal is NOT to be a high-fidelity finite-element solver, but a lightweight
utility to create smooth looping animations or parameter studies where an
object traces concentric or evolving circular loops depending on its material
properties.

Example
-------
>>> from loop_creator import CircularLoopSimulator
>>> sim = CircularLoopSimulator(
...     radius=5.0,
...     mass=1.0,
...     elasticity_k=20.0,
...     damping=0.5,
...     softness=0.1,
...     dt=0.01,
...     total_time=10.0,
... )
>>> t, xy = sim.run()

A helper ``plot`` method is also available:
>>> sim.plot()
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


class CircularLoopSimulator:
    """Simulate an object constrained *approximately* to a circle via elastic forces.

    Parameters
    ----------
    radius : float
        Target radius of the circular path.
    mass : float, default=1.0
        Mass of the object (kg).
    elasticity_k : float, default=10.0
        Base spring constant (N/m). Larger values keep the object closer to the
        desired radius.
    damping : float, default=0.1
        Viscous damping coefficient (kg/s). Higher values increase fluidity and
        reduce oscillations.
    softness : float, default=0.0
        [0, 1] factor that linearly reduces the spring constant over the course
        of the simulation. 0 -> rigid (no softening). 1 -> spring fully loses
        stiffness by final step.
    dt : float, default=0.01
        Simulation time step (s).
    total_time : float, default=5.0
        Total simulation time (s).
    theta0 : float, default=0.0
        Initial polar angle (rad).
    angular_speed0 : float, default=2 * pi (rad/s)
        Initial angular speed around the center. This determines the initial
        tangential velocity, thereby controlling how many loops occur.
    rng : np.random.Generator | None
        Optional random generator for small radial perturbation to prevent the
        trajectory from collapsing into a perfect circle (makes animation more
        interesting).
    """

    def __init__(
        self,
        radius: float,
        *,
        mass: float = 1.0,
        elasticity_k: float = 10.0,
        damping: float = 0.1,
        softness: float = 0.0,
        dt: float = 0.01,
        total_time: float = 5.0,
        theta0: float = 0.0,
        angular_speed0: float | None = None,
        rng: np.random.Generator | None = None,
    ) -> None:
        self.radius = float(radius)
        self.mass = float(mass)
        self.elasticity_k = float(elasticity_k)
        self.damping = float(damping)
        self.softness = float(np.clip(softness, 0.0, 1.0))
        self.dt = float(dt)
        self.total_time = float(total_time)
        self.theta0 = float(theta0)
        if angular_speed0 is None:
            angular_speed0 = 2 * np.pi  # one loop per second by default
        self.angular_speed0 = float(angular_speed0)
        self.rng = rng if rng is not None else np.random.default_rng()

        # Will hold results after run()
        self._t: np.ndarray | None = None
        self._xy: np.ndarray | None = None

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
    def _radial_force(self, r_curr: float, step_frac: float) -> float:
        """Return radial restoring force magnitude (directed toward/away center)."""
        k_eff = self.elasticity_k * (1.0 - self.softness * step_frac)
        return -k_eff * (r_curr - self.radius)

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def run(self) -> tuple[np.ndarray, np.ndarray]:
        """Run the simulation and return time array and xy positions."""
        n_steps = int(self.total_time / self.dt) + 1
        t = np.linspace(0.0, self.total_time, n_steps)
        xy = np.zeros((n_steps, 2), dtype=float)

        # Initial state in cartesian coordinates
        x0 = self.radius * np.cos(self.theta0)
        y0 = self.radius * np.sin(self.theta0)
        xy[0] = np.array([x0, y0])

        # Velocities (tangential)
        v = np.zeros((n_steps, 2), dtype=float)
        v0 = self.angular_speed0 * np.array([-y0, x0]) / self.radius  # tangential
        v[0] = v0

        for i in range(1, n_steps):
            # Current state
            r_vec = xy[i - 1]
            r_mag = np.linalg.norm(r_vec)

            # Forces
            step_frac = t[i - 1] / self.total_time  # 0 -> 1
            F_radial = self._radial_force(r_mag, step_frac)
            F_vec = F_radial * (r_vec / (r_mag + 1e-12))  # radial direction
            # Damping force
            F_vec -= self.damping * v[i - 1]

            # Acceleration
            a = F_vec / self.mass

            # Velocity Verlet integration
            v_half = v[i - 1] + 0.5 * a * self.dt
            xy[i] = xy[i - 1] + v_half * self.dt
            # Recompute radial force with predicted position for better stability
            r_vec_new = xy[i]
            r_mag_new = np.linalg.norm(r_vec_new)
            F_radial_new = self._radial_force(r_mag_new, step_frac)
            F_vec_new = F_radial_new * (r_vec_new / (r_mag_new + 1e-12)) - self.damping * v_half
            a_new = F_vec_new / self.mass
            v[i] = v_half + 0.5 * a_new * self.dt

        self._t = t
        self._xy = xy
        return t, xy

    def plot(self, *, show: bool = True, ax: plt.Axes | None = None) -> plt.Axes:
        """Plot the trajectory in the XY plane."""
        if self._xy is None:
            self.run()
        assert self._xy is not None
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(self._xy[:, 0], self._xy[:, 1])
        ax.set_aspect("equal")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_title("Circular Loop Trajectory")
        if show:
            plt.show()
        return ax

    # Convenience
    def get_trajectory(self) -> np.ndarray:
        """Return cached xy trajectory (run() if necessary)."""
        if self._xy is None:
            self.run()
        assert self._xy is not None
        return self._xy.copy()