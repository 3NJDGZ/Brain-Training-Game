import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paragraphs in Pygame")

# Colors
white = (255, 255, 255)

# Font setup
font = pygame.font.Font(None, 24)  # You can choose a font and size

# Sample text paragraphs
paragraphs = [
    "This is the first paragraph. It can contain multiple lines of text.",
    "Each paragraph needs to be managed separately and broken into lines.",
    "Pygame's font module provides functions for rendering text on the screen.",
    "Remember to account for line breaks and text wrapping to fit within the screen.",
    "Creating visually pleasing text layouts can involve complex calculations.",
]

# Calculate the y-coordinate for each line of text
line_spacing = font.get_height() + 5  # Adjust the line spacing as needed
y = 50

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Render each paragraph
    for paragraph in paragraphs:
        lines = paragraph.split('\n')  # Split paragraph into lines
        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))  # Render the line
            screen.blit(text_surface, (50, y))  # Draw the line on the screen
            y += line_spacing  # Move down for the next line
        y += line_spacing * 2  # Add extra space between paragraphs

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
