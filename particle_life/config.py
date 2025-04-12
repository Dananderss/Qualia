import numpy as np

# --- Screen Configuration ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WINDOW_TITLE = "Python Particle Life"
FPS_LIMIT = 60

# --- Simulation Parameters ---
NUM_PARTICLES = 300
NUM_TYPES = 5
# MAX_RADIUS = 70       # Initial radius - now set by slider default
FORCE_FACTOR = 15     # Strength of interaction forces
FRICTION = 0.95       # Velocity damping factor (0 to 1)
DT = 0.02             # Simulation time step (smaller = more stable, slower)
PARTICLE_SIZE = 3

# --- Slider Specific Config ---
RADIUS_SLIDER_MIN = 10
RADIUS_SLIDER_MAX = 150
INITIAL_RADIUS = 70   # Default starting radius

# --- Colors ---
BACKGROUND_COLOR = (20, 10, 50)
INFO_COLOR = (200, 200, 200)
SLIDER_COLOR = (100, 100, 100)
SLIDER_HANDLE_COLOR = (250, 250, 250)

# --- Interaction Matrix Generation ---
# (keep the create_interaction_matrix function as is)
def create_interaction_matrix(num_types):
    """Creates the interaction matrix."""
    matrix = np.random.uniform(-1, 1, (num_types, num_types))
    # Optional: Make interactions symmetric
    # matrix = (matrix + matrix.T) / 2
    # Optional: Reduce self-interaction strength
    # np.fill_diagonal(matrix, matrix.diagonal() * 0.5)
    print("Interaction Matrix:\n", matrix)
    return matrix