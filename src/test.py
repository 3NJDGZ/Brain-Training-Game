import pygame
import random
import time

pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Matrix Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)

# Set up the game clock
clock = pygame.time.Clock()

# Define constants for the game
GRID_SIZE = 5
TILE_SIZE = 100
PADDING = 10
FLASH_TIME = 1000  # Time in milliseconds to flash each tile
PAUSE_TIME = 500  # Time in milliseconds to pause between the flash and player input
COLOR_OFF = GREY
COLOR_ON = WHITE


class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(col * (TILE_SIZE + PADDING), row * (TILE_SIZE + PADDING), TILE_SIZE, TILE_SIZE)
        self.color = COLOR_OFF
        self.is_flashing = False


def create_grid():
    return [[Tile(row, col) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]


def flash_sequence(grid):
    sequence = []

    for _ in range(GRID_SIZE * 2):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        sequence.append((row, col))

    for row, col in sequence:
        grid[row][col].is_flashing = True
        grid[row][col].color = COLOR_ON
        pygame.display.update()
        time.sleep(FLASH_TIME / 1000)
        grid[row][col].is_flashing = False
        grid[row][col].color = COLOR_OFF
        pygame.display.update()
        time.sleep(PAUSE_TIME / 1000)

    return sequence


def main():
    grid = create_grid()
    sequence = flash_sequence(grid)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the grid
        screen.fill(BLACK)
        for row in grid:
            for tile in row:
                pygame.draw.rect(screen, tile.color, tile.rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
