import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the width and height of the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Define the maze
maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "X         X             X",
    "X XXXXX XXXXXXX XXXXX X X",
    "X       X       X     X X",
    "X X XXX XXX XXX XXXXX X X",
    "X X   X   X X   X     X X",
    "X XXX XXXXX XXX XXXXX X X",
    "X X     X   X   X     X X",
    "X X XXX X XXXXXXX XXXXX X",
    "X X X   X         X     X",
    "X X X XXXXXXXXXXXXX XXX X",
    "X     X             X   X",
    "XXXXX XXXXXXXXXXXXX XXX X",
    "X   X          X       X",
    "XXX XXXX XXXX XXXXXXXXX X",
    "X     X    X           X",
    "X XXXXX XXXX XXXXXXXXX X",
    "X       X   X           X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Calculate the size of each cell in the maze
cell_width = screen_width // len(maze[0])
cell_height = screen_height // len(maze)

# Find the player's starting position in the maze
start_x, start_y = 1, 1

# Set the initial player position
player_x = start_x * cell_width
player_y = start_y * cell_height

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Move the player based on key press
            if event.key == pygame.K_UP:
                if maze[(player_y - cell_height) // cell_height][player_x // cell_width] != "X":
                    player_y -= cell_height
            elif event.key == pygame.K_DOWN:
                if maze[(player_y + cell_height) // cell_height][player_x // cell_width] != "X":
                    player_y += cell_height
            elif event.key == pygame.K_LEFT:
                if maze[player_y // cell_height][(player_x - cell_width) // cell_width] != "X":
                    player_x -= cell_width
            elif event.key == pygame.K_RIGHT:
                if maze[player_y // cell_height][(player_x + cell_width) // cell_width] != "X":
                    player_x += cell_width

    # Draw the maze
    screen.fill(BLACK)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "X":
                pygame.draw.rect(screen, WHITE, (x * cell_width, y * cell_height, cell_width, cell_height))

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, cell_width, cell_height))

    # Update the display
    pygame.display.flip()
