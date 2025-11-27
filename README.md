# Emergent Systems Lab

A collection of agent-based simulations exploring swarm intelligence, flocking behaviors, and autonomous self-assembly. These simulations demonstrate how complex group behaviors emerge from simple local rules.

## The Simulations

### 1. Boids Flocking (boids_flocking.py)
A implementation of Craig Reynolds' famous "Boids" algorithm using `numpy` and `matplotlib`.
* **The Logic:** Each agent follows three simple vectors:
  1. **Separation:** Steer to avoid crowding local flockmates.
  2. **Alignment:** Steer towards the average heading of local flockmates.
  3. **Cohesion:** Steer to move toward the average position of local flockmates.
* **Tech Stack:** Vectorized NumPy operations for performance.

### 2. Autonomous Self-Assembly (self_assembly.py)
A particle system demonstrating state-dependent behavior using Python's `turtle` graphics.
* **The Logic:** Particles are assigned a target position to form a circle. They exhibit a "Dual-Mode" approach:
  1. **Fast Mode:** High velocity and high separation force (to avoid clumping) when far from target.
  2. **Precision Mode:** Activates when distance is less than 30. Applies friction, lowers speed, and increases steering force to lock into position.
* **Goal:** To demonstrate how individual agents can transition from chaotic movement to an ordered structure without a central controller.

## How to Run

1. Install dependencies:

    pip install -r requirements.txt

2. Run the Boids simulation:

    python boids_flocking.py

3. Run the Assembly simulation (opens a Turtle window):

    python self_assembly.py

## Tech Stack
* Python 3.x
* NumPy (Vector math)
* Matplotlib (Animation)
* Turtle (Real-time graphics)

## License
MIT License