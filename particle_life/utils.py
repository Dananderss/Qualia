import random
import numpy as np

def generate_type_colors(num_types):
    """Generates somewhat distinct random colors for particle types."""
    return [tuple(random.randint(50, 255) for _ in range(3)) for _ in range(num_types)]