import pygame

def handle_events():
    """
    Processes Pygame events, returns the raw event list for widgets,
    and a dictionary of specific high-level actions detected.
    """
    actions = {'quit': False, 'toggle_pause': False, 'reset': False}
    events = pygame.event.get() # Get all events first

    for event in events:
        if event.type == pygame.QUIT:
            actions['quit'] = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                actions['quit'] = True
            if event.key == pygame.K_SPACE:
                actions['toggle_pause'] = True
            if event.key == pygame.K_r:
                actions['reset'] = True
        # Widgets handle their own mouse events via pygame_widgets.update(events)

    return events, actions # Return both raw events and parsed actions