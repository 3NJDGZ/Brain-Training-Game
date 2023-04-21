import pygame

# Initialise Variables
WIDTH = 1280
TILE = 100
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
cols = WIDTH // TILE
rows = HEIGHT // TILE
pygame.display.set_caption("Maze Generation Algorithm Test")

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()