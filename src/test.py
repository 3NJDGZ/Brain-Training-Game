import pygame
import pygame_gui

pygame.init()

# Set up the display surface
DISPLAY_SURFACE = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Drop-down menu")

# Create the UI manager
UI_MANAGER = pygame_gui.UIManager((640, 480))

# Create the drop-down menu
options = ["Option 1", "Option 2", "Option 3"]
dropdown_menu = pygame_gui.elements.UIDropDownMenu(
    options_list=options,
    starting_option=options[0],
    relative_rect=pygame.Rect(50, 50, 200, 30),
    manager=UI_MANAGER,
)

# Run the game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass events to the UI manager
        UI_MANAGER.process_events(event)

    # Update the UI manager
    UI_MANAGER.update(clock.tick(60) / 1000.0)

    # Get the selected option
    selected_option = dropdown_menu.selected_option
    print(selected_option)

    # Draw the UI manager
    DISPLAY_SURFACE.fill((255, 255, 255))
    UI_MANAGER.draw_ui(DISPLAY_SURFACE)

    pygame.display.update()

pygame.quit()
