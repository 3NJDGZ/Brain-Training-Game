import pygame
import time
from screens import * 
from random import randint
import random
import sys

sys.setrecursionlimit(10**6)

pygame.init()

# Initialise Variables
CLOCK = pygame.time.Clock()
WIDTH = 1280
STARTING_TILE_SIZE = 8 # common factors between 1280, 720: 80, 40, 16, 8, 4, 2, 1
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
    
    def get_walls(self):
        return self.__walls
    
    def set_walls(self, wall_to_be_changed, value: bool):
        self.__walls[f'{wall_to_be_changed}'] = value
    
    def set_visited(self, value: bool):
        self.__visited = value
    
    def get_row_column_positioning(self):
        return [self.__x // STARTING_TILE_SIZE, self.__y // STARTING_TILE_SIZE]
            
    def check_adjacent_cells(self):

        adjacent_cells = []
        current_cell_column_row_positioning = self.get_row_column_positioning()
        current_column = current_cell_column_row_positioning[0]
        current_row = current_cell_column_row_positioning[1]

        # check for adjacent nodes
        if current_column - 1 >= 0: # cell to the left
            adjacent_cells.append(grid_of_cells[current_row][current_column - 1])
        if current_column + 1 < cols: # cell to the right 
            adjacent_cells.append(grid_of_cells[current_row][current_column + 1])
        if current_row - 1 >= 0: # cell above current cell
            adjacent_cells.append(grid_of_cells[current_row - 1][current_column])
        if current_row + 1 < rows: # cell beneath the current cell 
            adjacent_cells.append(grid_of_cells[current_row + 1][current_column])
        
        random.shuffle(adjacent_cells)
        return adjacent_cells
    
    def draw_cell(self):
        # print(f"x: {self.__x}, y: {self.__y}.")
        if self.__visited == True:
            pygame.draw.rect(WIN, (255, 255, 255), (self.__x, self.__y, STARTING_TILE_SIZE, STARTING_TILE_SIZE))
        if self.__walls['top'] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x, self.__y), (self.__x + STARTING_TILE_SIZE, self.__y), 4)
        if self.__walls['right'] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x + STARTING_TILE_SIZE, self.__y), (self.__x + STARTING_TILE_SIZE, self.__y + STARTING_TILE_SIZE), 4)
        if self.__walls['bottom'] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x + STARTING_TILE_SIZE, self.__y + STARTING_TILE_SIZE), (self.__x, self.__y + STARTING_TILE_SIZE), 4)
        if self.__walls['left'] == True:
            pygame.draw.line(WIN, LINE_COLOUR, (self.__x, self.__y + STARTING_TILE_SIZE), (self.__x, self.__y), 4)


class Maze_Screen(Screen):
    def __init__(self, Title: str, Initial_Cell: Cell):
        self.stack = Stack(len(grid_of_cells) * cols)
        self.stack.push(Initial_Cell)
        self.visited_cells = []
        self.grid_of_cells = []
        for a in range(rows):
            row = []
            for b in range(cols):
                row.append(Cell(STARTING_TILE_SIZE * b, STARTING_TILE_SIZE * a))
            grid_of_cells.append(row)

    def dfs(self):
        current_cell = self.stack.peek()
        if current_cell is not None:
            current_cell.set_visited(True)
            self.visited_cells.append(stack.peek())
            adjacent_cells = current_cell.check_adjacent_cells()
            
            for connected_cell in adjacent_cells:
                if connected_cell not in self.visited_cells:
                    if connected_cell is not None:
                        self.stack.push(connected_cell)
                        self.remove_walls(current_cell, connected_cell)
                        self.dfs()
            self.stack.pop()
    
    def remove_walls(self, current_cell: Cell, next_cell: Cell):
        current_cell_column_row_positioning = current_cell.get_row_column_positioning()
        next_cell_column_row_positioning = next_cell.get_row_column_positioning()

        # column then row [column, row]
        print(f"Current: {current_cell_column_row_positioning}, Next: {next_cell_column_row_positioning}")
        current_x = current_cell_column_row_positioning[0]
        current_y = current_cell_column_row_positioning[1]
        next_x = next_cell_column_row_positioning[0]
        next_y = next_cell_column_row_positioning[1]

        # check if top cell is next cell relative to current cell
        if current_y - next_y == 1:
            next_cell.set_walls('bottom', False)
            current_cell.set_walls('top', False)
        
        # check if bottom cell is next cell relative to current cell
        if current_y - next_y == -1:
            next_cell.set_walls('top', False)
            current_cell.set_walls('bottom', False)
        
        # check if right cell is next cell relative to current cell
        if current_x - next_x == -1:
            next_cell.set_walls('left', False)
            current_cell.set_walls('right', False)
        
        # check if left cell is next cell relative to current cell
        if current_x - next_x == 1:
            next_cell.set_walls('right', False)
            current_cell.set_walls('left', False)
        
        print(f"Current: {current_cell.get_walls()}, Next: {next_cell.get_walls()}")
    
    def show_UI_elements(self):
        return super().show_UI_elements()

    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def check_for_user_interaction_with_UI(self):
        return super().check_for_user_interaction_with_UI()

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

print(f"Number of Cells: {len(grid_of_cells) * cols}")

stack = Stack(len(grid_of_cells) * cols)
stack.push(current_cell)
visited_cells = []

def main():
    running = True
    CLOCK.tick(60)
    dfs()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        WIN.fill((255, 120, 50))

        # Draw the cells
        for row in grid_of_cells:
            for cell in row:
                cell.draw_cell()
    
        pygame.display.update()

    pygame.quit()

def dfs():
    current_cell = stack.peek()
    if current_cell is not None:
        current_cell.set_visited(True)
        visited_cells.append(stack.peek())
        adjacent_cells = current_cell.check_adjacent_cells()
        
        for connected_cell in adjacent_cells:
            if connected_cell not in visited_cells:
                if connected_cell is not None:
                    stack.push(connected_cell)
                    remove_walls(current_cell, connected_cell)
                    dfs()
        stack.pop()

def remove_walls(current_cell: Cell, next_cell: Cell):
    current_cell_column_row_positioning = current_cell.get_row_column_positioning()
    next_cell_column_row_positioning = next_cell.get_row_column_positioning()

    # column then row [column, row]
    print(f"Current: {current_cell_column_row_positioning}, Next: {next_cell_column_row_positioning}")
    current_x = current_cell_column_row_positioning[0]
    current_y = current_cell_column_row_positioning[1]
    next_x = next_cell_column_row_positioning[0]
    next_y = next_cell_column_row_positioning[1]

    # check if top cell is next cell relative to current cell
    if current_y - next_y == 1:
        next_cell.set_walls('bottom', False)
        current_cell.set_walls('top', False)
    
    # check if bottom cell is next cell relative to current cell
    if current_y - next_y == -1:
        next_cell.set_walls('top', False)
        current_cell.set_walls('bottom', False)
    
    # check if right cell is next cell relative to current cell
    if current_x - next_x == -1:
        next_cell.set_walls('left', False)
        current_cell.set_walls('right', False)
    
    # check if left cell is next cell relative to current cell
    if current_x - next_x == 1:
        next_cell.set_walls('right', False)
        current_cell.set_walls('left', False)
    
    print(f"Current: {current_cell.get_walls()}, Next: {next_cell.get_walls()}")

if __name__ == "__main__":
    main()