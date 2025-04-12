import pygame
import sys
import pygame_widgets # Import widgets
from pygame_widgets.slider import Slider # Import the specific Slider class

from . import config
from .simulation import Simulation
from .renderer import Renderer
from .interaction import handle_events
from .utils import generate_type_colors

def run():
    """Initializes and runs the main application loop."""
    simulation = Simulation(
        config.NUM_PARTICLES,
        config.NUM_TYPES,
        config.SCREEN_WIDTH,
        config.SCREEN_HEIGHT
    )

    renderer = Renderer(
        config.SCREEN_WIDTH,
        config.SCREEN_HEIGHT,
        config.WINDOW_TITLE
    )
    renderer.set_particle_colors(generate_type_colors(config.NUM_TYPES))

    # --- Create Slider ---
    radius_slider = Slider(
        renderer.screen, # Surface to draw on
        10, 35,          # X, Y position (below the status text)
        200, 15,         # Width, Height
        min=config.RADIUS_SLIDER_MIN,
        max=config.RADIUS_SLIDER_MAX,
        step=1,
        initial=config.INITIAL_RADIUS,
        colour=config.SLIDER_COLOR,
        handleColour=config.SLIDER_HANDLE_COLOR
    )
    # Create a label for the slider
    slider_label_font = pygame.font.SysFont(None, 20)
    slider_label_text = "Radius:"

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        # --- Handle User Input & Widgets ---
        # Get events and high-level actions
        events, actions = handle_events()

        if actions['quit']:
            running = False
        if actions['toggle_pause']:
            paused = not paused
        if actions['reset']:
            simulation.reset()
            radius_slider.setValue(config.INITIAL_RADIUS) # Reset slider visually
            paused = False

        # # IMPORTANT: Update widgets with the events BEFORE drawing
        # pygame_widgets.update(events)

        # --- Get Current Slider Value ---
        current_radius = radius_slider.getValue()

        # --- Update Simulation State ---
        if not paused:
            simulation.step(
                config.DT,
                config.FRICTION,
                current_radius, # Use the value from the slider
                config.FORCE_FACTOR
            )

        # --- Render Frame ---
        renderer.clear_screen(config.BACKGROUND_COLOR)
        renderer.draw_particles(
            simulation.get_positions(),
            simulation.get_types(),
            config.PARTICLE_SIZE
        )

    # IMPORTANT: Update widgets with the events BEFORE drawing
        pygame_widgets.update(events)



        # Draw UI Text
        status_text = "Paused" if paused else "Running"
        renderer.draw_ui(status_text, clock.get_fps())

        # Draw Slider Label
        label_surface = slider_label_font.render(f"{slider_label_text} {current_radius}", True, config.INFO_COLOR)
        renderer.screen.blit(label_surface, (radius_slider.getX() + radius_slider.getWidth() + 10, radius_slider.getY()))

        # Draw the slider itself (pygame-widgets handles this)
        # Note: slider.draw() is implicitly called by pygame_widgets.update(events)
        # if you needed manual control, you'd call radius_slider.draw() here.
        # Let's keep using pygame_widgets.update() as it handles events and drawing.

        renderer.update_display() # Flip the buffer

        # --- Control Frame Rate ---
        clock.tick(config.FPS_LIMIT)

    # --- Cleanup ---
    renderer.cleanup()
    sys.exit()