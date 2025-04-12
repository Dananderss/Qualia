import numpy as np
from . import config # Use relative import within the package

class Simulation:
    """Manages the state and physics of the particle simulation."""

    def __init__(self, num_particles, num_types, width, height):
        self.num_particles = num_particles
        self.num_types = num_types
        self.width = width
        self.height = height

        self.interaction_matrix = config.create_interaction_matrix(self.num_types)
        self.reset() # Initialize particle states

    def reset(self):
        """Resets particle positions, velocities, and types."""
        self.positions = np.random.rand(self.num_particles, 2) * np.array([self.width, self.height])
        self.velocities = (np.random.rand(self.num_particles, 2) - 0.5) * 2 # Small random velocities
        self.types = np.random.randint(0, self.num_types, self.num_particles)
        # Optionally randomize interactions on reset:
        # self.interaction_matrix = config.create_interaction_matrix(self.num_types)

    def _calculate_forces(self, radius, force_scale): # Accept radius here
        """Calculates forces between particles using NumPy vectorization."""
        delta_pos = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
        dist_sq = np.sum(delta_pos**2, axis=2)

        dist_sq[dist_sq == 0] = 1e-6
        np.fill_diagonal(dist_sq, np.inf)

        distances = np.sqrt(dist_sq)
        mask_radius = distances < radius # Use the passed radius

        with np.errstate(invalid='ignore'):
            direction = delta_pos / distances[..., np.newaxis]
            direction[distances == 0] = 0

        force_magnitudes = self.interaction_matrix[self.types[:, np.newaxis], self.types[np.newaxis, :]]
        force = force_magnitudes * force_scale
        force_matrix = force[..., np.newaxis] * direction
        force_matrix[~mask_radius] = 0

        total_force = np.sum(force_matrix, axis=1)
        return total_force

    def _update_physics(self, forces, friction, dt):
        """Updates velocities and positions based on forces."""
        self.velocities = self.velocities * friction + forces * dt
        self.positions = self.positions + self.velocities * dt

    def _handle_boundaries(self):
        """Wraps particles around the screen boundaries."""
        self.positions[:, 0] = self.positions[:, 0] % self.width
        self.positions[:, 1] = self.positions[:, 1] % self.height

    # Modify the step method signature and internal call
    def step(self, dt, friction, radius, force_scale): # radius is now an argument
        """Performs one simulation step."""
        forces = self._calculate_forces(radius, force_scale) # Pass radius down
        self._update_physics(forces, friction, dt)
        self._handle_boundaries()

    # --- Getters for rendering ---
    def get_positions(self):
        return self.positions

    def get_types(self):
        return self.types