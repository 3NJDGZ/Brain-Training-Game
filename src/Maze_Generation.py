import pygame
import time
from random import randint

# Initialise Variables
CLOCK = pygame.time.Clock()
WIDTH = 1280
STARTING_TILE_SIZE = 80 # common factors between 1280, 720: 80, 40, 16, 8, 4, 2, 1
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
LINE_COLOUR = (255, 0, 0)
cols = WIDTH // STARTING_TILE_SIZE
rows = HEIGHT // STARTING_TILE_SIZE
pygame.display.set_caption("Maze Generation Algorithm Test")

class Stack:
    def __init__(self, maxsize):
        self.items = [None] * maxsize
        self.stackpointer = -1
    
    def push(self, item):
        if self.stackpointer != len(self.items)-1:
            self.stackpointer += 1
            self.items[self.stackpointer] = item
    
    def pop(self):
        if self.stackpointer != -1:
            self.stackpointer -= 1
            return self.items[self.stackpointer + 1]
    
    def is_full(self):
        if self.stackpointer == len(self.items) - 1:
            return True
        else:
            return False
    
    def is_empty(self):
        if self.stackpointer == -1:
            return True
        else:
            return False
    
    def print_data(self):
        for i in self.items:
            print(i)

    def peek(self):
        return self.items[self.stackpointer]

class Cell:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__walls = {"top": True,
                      "right": True,
                      "bottom": True,
                      "left": True}
        self.__visited = False
        self.__current = False
    
    def set_visited(self, value: bool):
        self.__visited = value
    
    def get_row_column_positioning(self):
        return [self.__x // STARTING_TILE_SIZE, self.__y // STARTING_TILE_SIZE]

    def draw_current_cell(self):
        if self.__current == True:
            pygame.draw.rect(WIN, (255, 255, 0), (self.__x, self.__y, STARTING_TILE_SIZE, STARTING_TILE_SIZE))
            
    
    def draw_cell(self, WIN: WIN):
        # print(f"x: {self.__x}, y: {self.__y}.")
        if self.__visited == True:
            pygame.draw.rect(WIN, (255, 255, 255), (self.__x, self.__y, STARTING_TILE_SIZE, STARTING_TILE_SIZE))
        if self.__walls["top"] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x, self.__y), (self.__x + STARTING_TILE_SIZE, self.__y))
        if self.__walls["right"] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x + STARTING_TILE_SIZE, self.__y), (self.__x + STARTING_TILE_SIZE, self.__y - STARTING_TILE_SIZE))
        if self.__walls["bottom"] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x + STARTING_TILE_SIZE, self.__y - STARTING_TILE_SIZE), (self.__x, self.__y - STARTING_TILE_SIZE))
        if self.__walls["left"] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x, self.__y - STARTING_TILE_SIZE), (self.__x, self.__y))
        
class RecursiveDepthFirstSearch:
    def __init__(self, grid_of_cells, stack: Stack):
        self.grid_of_cells = grid_of_cells
        self.stack = stack
        self.visited_cells = []
    
    def _dfs(self):
        current_cell = stack.peek()
        current_cell.draw_cell(WIN)
        self.visited_cells.append(current_cell)
        current_cell_column_row_positioning = current_cell.get_row_column_positioning()
        current_column = current_cell_column_row_positioning[0]
        current_row = current_cell_column_row_positioning[1]
        adjacent_cells = []

        # check for adjacent nodes
        if current_column - 1 >= 0: # cell to the left
            adjacent_cells.append(grid_of_cells[current_row][current_column - 1])
        if current_column + 1 < cols: # cell to the right 
            adjacent_cells.append(grid_of_cells[current_row][current_column + 1])
        if current_row - 1 >= 0: # cell above current cell
            adjacent_cells.append(grid_of_cells[current_row - 1][current_column])
        if current_row + 1 < rows: # cell beneath the current cell 
            adjacent_cells.append(grid_of_cells[current_row + 1][current_column])

        for connected_cell in adjacent_cells:
            if connected_cell not in self.visited_cells:
                connected_cell.set_visited(True)
                stack.push(connected_cell)
                self._dfs()
        stack.pop()
            
print(f"Columns: {cols}")
print(f"Rows: {rows}")

grid_of_cells = []

for a in range(rows):
    row = []
    for b in range(cols):
        row.append(Cell(STARTING_TILE_SIZE * b, STARTING_TILE_SIZE * a))
    grid_of_cells.append(row)

row = 0
column = 0
current_cell = grid_of_cells[row][column]

print(f"Number of Cells: {len(grid_of_cells)}")

stack = Stack(len(grid_of_cells) * cols)
stack.push(current_cell)
dfs = RecursiveDepthFirstSearch(grid_of_cells, stack)
dfs._dfs()


def main():
    running = True
    CLOCK.tick(60)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        WIN.fill((255, 120, 50))


        # Draw the cells
        for row in grid_of_cells:
            for cell in row:
                cell.draw_cell(WIN)
    
        pygame.display.update()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()