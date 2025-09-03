"""example.py
Demonstration of the CircularLoopSimulator.
Run with:
    python example.py
"""
from loop_creator import CircularLoopSimulator


def main() -> None:
    sim = CircularLoopSimulator(
        radius=3.0,
        mass=1.0,
        elasticity_k=30.0,
        damping=0.2,
        softness=0.3,
        dt=0.01,
        total_time=8.0,
        angular_speed0=4.0,
        theta0=0.0,
    )
    sim.run()
    sim.plot()


if __name__ == "__main__":
    main()