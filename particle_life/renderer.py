import pygame
from . import config

class Renderer:
    """Handles drawing the simulation state onto the Pygame screen."""

    def __init__(self, width, height, title):
        pygame.init()
        pygame.font.init() # Initialize font module explicitly
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont(None, 24) # Use default system font
        self.particle_colors = [] # Will be set externally

    def set_particle_colors(self, colors):
        self.particle_colors = colors

    def draw_particles(self, positions, types, particle_size):
        """Draws all particles onto the screen."""
        if not self.particle_colors:
            print("Warning: Particle colors not set in Renderer.")
            return

        for i in range(len(positions)):
            try:
                pos_int = positions[i].astype(int)
                color = self.particle_colors[types[i]]
                pygame.draw.circle(self.screen, color, pos_int, particle_size)
            except IndexError:
                print(f"Error drawing particle {i}: Type index {types[i]} out of bounds for colors list.")
            except Exception as e:
                 print(f"Error drawing particle {i} at {positions[i]}: {e}")


    def draw_ui(self, status_text, fps):
        """Draws status text and FPS counter."""
        text_surface = self.font.render(f'[SPACE] {status_text} | [R] Reset | FPS: {fps:.1f}', True, config.INFO_COLOR)
        self.screen.blit(text_surface, (5, 5))

    def clear_screen(self, color):
        """Fills the screen with the background color."""
        self.screen.fill(color)

    def update_display(self):
        """Updates the full screen surface to show drawn elements."""
        pygame.display.flip()

    def cleanup(self):
        """Cleans up Pygame resources."""
        pygame.quit()