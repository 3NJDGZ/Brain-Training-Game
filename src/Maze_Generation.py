# Import necessary Modules
import pygame
import random
from exercises import QuestionAnswerExercise, Aiming, SchulteTable, MemoryMatrix, ChalkboardChallenge, CognitiveExercise

# Stack implementation necessary to facilitate the functionality of the randomised recursive DFS used for maze generation
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
    def __init__(self, x: int, y: int, WIN, STARTING_TILE_SIZE: int, grid_of_cells, cols: int, rows: int, LINE_COLOUR):
        # Setup attributes for Cell(s)
        # Size of cell + Colour
        self.STARTING_TILE_SIZE = STARTING_TILE_SIZE
        self.LINE_COLOUR = LINE_COLOUR
        self.LINE_WIDTH = 5

        # The main screen that the cell will be drawn on
        self.WIN = WIN

        # Attributes to identify positioning of cell in the 2D array
        self.grid_of_cells = grid_of_cells
        self.cols = cols
        self.rows = rows

        # These attributes are private as they are specific to each instance of a Cell
        self.__exit = False # Specifies if is is the exit cell
        self.__exercise_present = False # Checking if it has an exercise cell
        self.__exercise = None # The actual exercise object itself, note that its default value is 'None'
        self.__start = False # Specifies if it is the starting cell
        self.__x = x # x positioning on the pygame x, y plane (origin in the top left corner)
        self.__y = y # y positioning on the pygame x, y plane 
        self.__walls = {"top": True, # Walls of the cell
                      "right": True,
                      "bottom": True,
                      "left": True}
        self.__visited = False # Value used to check if the cell has been visited by the recursive DFS algo during maze generation (aka removing walls between adjacent cells)
        self.__visited_by_hints = False # Value used to check if the cell has been visited iterative DFS algo when finding a valid path between current player position and the exit cell
    
    def set_visited_hints(self, value_to_be_set: bool):
        self.__visited_by_hints = value_to_be_set
    
    def get_visited_hints(self):
        return self.__visited_by_hints

    def get_exercise(self):
        return self.__exercise

    def set_exercise(self, exercise: CognitiveExercise):
        self.__exercise = exercise
    
    def get_exercise_present(self):
        return self.__exercise_present
    
    def set_exercise_present(self, value_to_be_set: bool):
        self.__exercise_present = value_to_be_set

    def create_rect(self): # creates the rect the same size as the cell; this is used for determining collisions by using pygame's rect collision modules
        rect = pygame.Rect(self.__x, self.__y, self.STARTING_TILE_SIZE, self.STARTING_TILE_SIZE)
        return rect

    def set_exit_value(self, value_to_be_set: bool):
        self.__exit = value_to_be_set
    
    def get_exit_value(self):
        return self.__exit
    
    def set_start_value(self, value_to_be_set: bool):
        self.__start = value_to_be_set
    
    def get_start_value(self):
        return self.__start

    def get_walls(self):
        return self.__walls
    
    def set_walls(self, wall_to_be_changed, value: bool):
        self.__walls[f'{wall_to_be_changed}'] = value
    
    def set_visited(self, value: bool):
        self.__visited = value
        
    def get_row_column_positioning(self): # returns the column and row positioning of the cell (essentially its index positioning in reverse)
        return [self.__x // self.STARTING_TILE_SIZE, self.__y // self.STARTING_TILE_SIZE]

    # Function used to check adjacent cells to the current cell
    def check_adjacent_cells(self, shuffle: bool):

        adjacent_cells = []

        # get current cell positioning
        current_cell_column_row_positioning = self.get_row_column_positioning()
        current_column = current_cell_column_row_positioning[0] 
        current_row = current_cell_column_row_positioning[1]

        # check for adjacent nodes
        if current_column - 1 >= 0: # cell to the left
            adjacent_cells.append(self.grid_of_cells[current_row][current_column - 1])
        if current_column + 1 < self.cols: # cell to the right 
            adjacent_cells.append(self.grid_of_cells[current_row][current_column + 1])
        if current_row - 1 >= 0: # cell above current cell
            adjacent_cells.append(self.grid_of_cells[current_row - 1][current_column])
        if current_row + 1 < self.rows: # cell beneath the current cell 
            adjacent_cells.append(self.grid_of_cells[current_row + 1][current_column])
        
        # shuffle the 'adjacent_shells' list in order to keep the 'randomness' of the recursive DFS
        if shuffle:
            random.shuffle(adjacent_cells)

        return adjacent_cells

    def draw_cell(self):
        
        # if the cell has been visited by recursive DFS, then draw the cell as white (all cells will be visited so the main background of the cell will be white)
        if self.__visited:
            pygame.draw.rect(self.WIN, (255, 255, 255), (self.__x, self.__y, self.STARTING_TILE_SIZE, self.STARTING_TILE_SIZE))
        
        # if the cell has been visited by the iterative DFS, then draw the cell as yellow (for hints option)
        if self.__visited_by_hints:
            pygame.draw.rect(self.WIN, (255, 203, 59), (self.__x, self.__y, self.STARTING_TILE_SIZE, self.STARTING_TILE_SIZE))

        if self.__exit:  # Checks if the cell is the Exit cell; if it is then make it red 
            pygame.draw.rect(self.WIN, (255, 0, 0), (self.__x+5, self.__y+5, self.STARTING_TILE_SIZE-10, self.STARTING_TILE_SIZE-10))
        
        if self.__start: # Checks if the cell is the Start cell; if it is make it green
            pygame.draw.rect(self.WIN, (0, 255, 0), (self.__x+5, self.__y+5, self.STARTING_TILE_SIZE-10, self.STARTING_TILE_SIZE-10))

        if self.__exercise_present: # Checks if the cell is an exercise cell; if it is make it blue
            pygame.draw.rect(self.WIN, (0, 0, 255), (self.__x+5, self.__y+5, self.STARTING_TILE_SIZE-10, self.STARTING_TILE_SIZE-10))
        

        # Draws cells depending on what walls are currently active (if they are set to 'True' within the cell's corresponding 'walls' dictionary)
        if self.__walls['top']:
            pygame.draw.line(self.WIN, self.LINE_COLOUR, (self.__x, self.__y), (self.__x + self.STARTING_TILE_SIZE, self.__y), self.LINE_WIDTH)
        if self.__walls['right']:
            pygame.draw.line(self.WIN, self.LINE_COLOUR, (self.__x + self.STARTING_TILE_SIZE, self.__y), (self.__x + self.STARTING_TILE_SIZE, self.__y + self.STARTING_TILE_SIZE), self.LINE_WIDTH)
        if self.__walls['bottom']:
            pygame.draw.line(self.WIN, self.LINE_COLOUR, (self.__x + self.STARTING_TILE_SIZE, self.__y + self.STARTING_TILE_SIZE), (self.__x, self.__y + self.STARTING_TILE_SIZE), self.LINE_WIDTH)
        if self.__walls['left']:
            pygame.draw.line(self.WIN, self.LINE_COLOUR, (self.__x, self.__y + self.STARTING_TILE_SIZE), (self.__x, self.__y), self.LINE_WIDTH)

    def set_random_exercise(self, exercises):

        # exercises is a 1D array with exercise objects
        random_index = random.randint(0, len(exercises) - 1)
        self.set_exercise(exercises[random_index])

    def create_exercise_for_cell(self, PDM):

        # https://www.w3schools.com/python/ref_random_choices.asp random.choices, python module used to use the weight values are percent chances of getting a specific exercise

        if self.get_exercise_present():
            weight_values = PDM.extract_corresponding_weights() # extract weights from Database using PDM 
            cognitive_areas = ["Memory", "Attention", "Speed", "Problem Solving"]
            selected_cognitive_area = random.choices(cognitive_areas, weight_values, k=1)[0]
            
            Memory_Exercises = [MemoryMatrix(1, PDM), QuestionAnswerExercise(1, PDM)]
            Attention_Exercises = [SchulteTable(2, PDM)]
            Speed_Exercises = [Aiming(3, PDM)]
            ProblemSolving_Exercises = [ChalkboardChallenge(4, PDM)]

            # set the exercise correspondingly
            if selected_cognitive_area == "Memory":
                self.set_random_exercise(Memory_Exercises)
            elif selected_cognitive_area == "Attention":
                self.set_random_exercise(Attention_Exercises)
            elif selected_cognitive_area == "Speed":
                self.set_random_exercise(Speed_Exercises)
            elif selected_cognitive_area == "Problem Solving":
                self.set_random_exercise(ProblemSolving_Exercises)

class Maze():
    def __init__(self, STARTING_TILE_SIZE: int, LINE_COLOUR: tuple, WIDTH: int, HEIGHT: int, WIN, PDM, min_exercise_cells: int, max_exercise_cells: int):
        # Size + Colour for each individual cell
        self.__STARTING_TILE_SIZE = STARTING_TILE_SIZE
        self.__LINE_COLOUR = LINE_COLOUR

        # Grid dimensions of the cells
        self.__rows = HEIGHT // self.__STARTING_TILE_SIZE
        self.__cols = WIDTH // self.__STARTING_TILE_SIZE

        # Arrays 
        self.__visited_cells = [] # visited cells from recursive maze generation, array created outside of subroutine as the subroutine is recursive
        self.__grid_of_cells = [] # stores the grid of cells (the maze) as a 2 Dimensional array
        self.__rects = [] # stores the rects for each individual cell as a 1 Dimensional array
        self.__exercise_cells = [] # Stores the cells that have exercises in them

        # PDM Manager
        self.__PDM = PDM

        # The screen that everything will be drawn on
        self.WIN = WIN

        # Variable used to stop from calling the recursive DFS continuously in the background
        self.__call_dfs = False

        # Setup for recursive DFS for maze generation, cells are in a grid (2D array)
        for row_number in range(self.__rows):
            row = []
            for col_number in range(self.__cols):
                row.append(Cell(self.__STARTING_TILE_SIZE * col_number, self.__STARTING_TILE_SIZE * row_number, self.WIN, self.__STARTING_TILE_SIZE, self.__grid_of_cells, self.__cols, self.__rows, self.__LINE_COLOUR))
            self.__grid_of_cells.append(row)
        
        # creating the exit cell by choosing a random cell in the grid of cells
        random_exit_cell = self.__grid_of_cells[random.randint(self.__rows // 1.5, self.__rows - 1)][random.randint(self.__cols // 1.5, self.__cols - 1)]
        random_exit_cell.set_exit_value(True)
        self.__exit_cell = random_exit_cell

        # Generating Exercise(s) Cells; only visualising them as blue cells; functionality has not yet been implemented.
        for x in range(random.randint(min_exercise_cells, max_exercise_cells)):
            # Selects random cell in grid of cells
            row_number = random.randint(4, self.__rows)
            cols_number = random.randint(4, self.__cols)
            exercise_cell = self.__grid_of_cells[row_number-1][cols_number-1]
            # Checks if the selected cell is not the exit cell, and not the start cell, and not an already existing exercise cell
            if not exercise_cell.get_exit_value() and not exercise_cell.get_start_value() and exercise_cell not in self.__exercise_cells:
                # If it is valid, then set a random exercise to that exercise cell, append it to the array of exercise cells, and set its exercise_present value to True
                exercise_cell.set_exercise_present(True)
                exercise_cell.create_exercise_for_cell(self.__PDM)
                self.__exercise_cells.append(exercise_cell)
        
        # Creating the start cell
        self.__grid_of_cells[0][0].set_start_value(True)
        
        # Initial setup for the Maze Generation
        self.__STACK = Stack(len(self.__grid_of_cells) * self.__cols) # creates a stack large enough to store all cells from the 2D array (aka grid of cells)
        self.__initial_cell = self.__grid_of_cells[0][0]
        self.__STACK.push(self.__initial_cell) # pushes the first cell to the stack

        # Setup for the Hints path finding option
        self.__find_exit_stack = Stack(len(self.__grid_of_cells) * self.__cols) # creating a large enough stack; handles worst case scenario if all cells will need to be visited 
                                                                                # to find the exit cell

        # Create the rect for each individual cell and append it to the self.__rects array (1D array)
        for row in self.__grid_of_cells:
            for cell in row:
                rect = cell.create_rect()
                self.__rects.append(rect)
    
    def check_if_all_exercise_cells_are_complete(self):
        # method required as all exercise cells need to be finished before the user can proceed onto the next level
        not_complete = False
        for cell in self.__exercise_cells:
            if not cell.get_exercise().get_completely_finished():
                not_complete = True
        return not_complete
        
    def get_grid_of_cells(self):
        return self.__grid_of_cells

    def get_rects(self):
        return self.__rects

    def get_cols(self):
        return self.__cols

    # sets up the actual maze itself and then draws it onto the screen
    def setup_maze(self):
        if not self.__call_dfs:
            self.maze_generation_dfs()
            self.__call_dfs = True
        self.draw_cells_on_screen()

    def draw_cells_on_screen(self):
        for row in self.__grid_of_cells:
            for cell in row:
                cell.draw_cell()
        
    def maze_generation_dfs(self):
        # Recursive Implementation of DFS (Depth First Search Graph Traversal Algorithm)
        current_cell = self.__STACK.peek()
        if current_cell is not None:
            # Set the current cell to visited and append it 'visited_cells' array
            current_cell.set_visited(True)
            self.__visited_cells.append(self.__STACK.peek())

            # Get the adjacent cells from the current cell in a shuffled order to preserve overall randomness of the maze 
            adjacent_cells = current_cell.check_adjacent_cells(True)
            
            # iterate though each cell in adjacent cells
            for connected_cell in adjacent_cells:

                # check if the cell has not yet been visited and that the cell is not a 'None' value
                if connected_cell not in self.__visited_cells:
                    if connected_cell is not None: 

                        # Push the connected cell to the top of the Stack
                        self.__STACK.push(connected_cell)

                        # Remove walls separating the connected cell and the current cell
                        self.remove_walls(current_cell, connected_cell)

                        # Call the method again
                        self.maze_generation_dfs()
            
            # Pop the cells from the stack to 'backtrack' to a previous cell that has adjacent cells that have not yet been visited
            self.__STACK.pop()
    
    # hints option
    def find_exit_dfs(self, Player_Current_Cell: Cell):
        # iterative version used as it is faster, and easier to code with in terms of traversing through the graph

        # Push the current cell that the Player is in to the top of the Stack
        self.__find_exit_stack.push(Player_Current_Cell)

        # Create set for the visited cells, faster to look for a certain item within a set compared to a linear search through an array
        visited_cells = set()

        # Create a dictionary for the path to the exit in reverse
        PathToExit = {}

        while not self.__find_exit_stack.is_empty():
            # Get Current cell by popping the top cell off of the stack
            current_cell = self.__find_exit_stack.pop()

            # Check base case if the current cell is the exit cell, if it is then break out of this while loop
            if current_cell is self.__exit_cell:
                break

            # Append the current cell to the 'visited_cells' array
            visited_cells.add(current_cell)

            # Get adjacent cells and create a new array called 'valid_cells'
            adjacent_cells = current_cell.check_adjacent_cells(False)
            valid_cells = []
            
            # Checking the validity of the adjacent cells; if they can be travsersed to (no walls separating the current cell to the next cell to be checked)
            for cell_to_be_checked in adjacent_cells:
                # get walls of the current cell and the cell that is going to be checked (aka the adjacent cell)
                current_cell_walls = current_cell.get_walls()
                cell_to_be_checked_walls = cell_to_be_checked.get_walls()
                
                # get row column positioning for both the current cell and the adjacent cell
                current_cell_position = current_cell.get_row_column_positioning()
                cell_to_be_checked_position = cell_to_be_checked.get_row_column_positioning()

                if current_cell_walls['right'] == False and cell_to_be_checked_walls['left'] == False: # checking adjacent cell to the right of current cell (if there is a valid path, no wall between the cells)
                    if current_cell_position[0] == (cell_to_be_checked_position[0] - 1): # line here is used to validate that the adjcent cell that is being currently looked at is the correct one

                        # Checking if the cell has not yet been visited by the algorithm
                        if not cell_to_be_checked.get_visited_hints():

                            # If it has not yet been visited then append it to the 'valid_cells' array
                            valid_cells.append(cell_to_be_checked)
                if current_cell_walls['left'] == False and cell_to_be_checked_walls['right'] == False: # checking adjacent cell to the left of the current cell (if there is a valid path, no wall between the cells)
                    if current_cell_position[0] == (cell_to_be_checked_position[0] + 1): # line here is used to validate that the adjcent cell that is being currently looked at is the correct one
                        if not cell_to_be_checked.get_visited_hints():
                            valid_cells.append(cell_to_be_checked)
                if current_cell_walls['top'] == False and cell_to_be_checked_walls['bottom'] == False: # checking adjacent cell to the top of the current cell (if there is a valid path, no wall between the cells)
                    if current_cell_position[1] == (cell_to_be_checked_position[1] + 1): # line here is used to validate that the adjcent cell that is being currently looked at is the correct one
                        if not cell_to_be_checked.get_visited_hints():
                            valid_cells.append(cell_to_be_checked)
                if current_cell_walls['bottom'] == False and cell_to_be_checked_walls['top'] == False: # checking adjacent cell to the bottom of the current cell (if there is a valid path, no wall between the cells)
                    if current_cell_position[1] == (cell_to_be_checked_position[1] - 1): # line here is used to validate that the adjcent cell that is being currently looked at is the correct one
                        if not cell_to_be_checked.get_visited_hints():
                            valid_cells.append(cell_to_be_checked)

            # Check each cell that is valid
            for cell in valid_cells:

                # Check if the cell has not yet been visited
                if cell not in visited_cells:

                    # Push the cell to the top of the stack
                    self.__find_exit_stack.push(cell)

                    # Create a key value pair for the Path 
                    # Essentially connects the two cells together forming a path
                    PathToExit[cell] = current_cell
        
        ForwardPath = {} # https://www.youtube.com/watch?v=sTRK9mQgYuc&t=1214s makes the forward path by reversing PathToExit
        cell = self.__exit_cell
        while cell != Player_Current_Cell:
            ForwardPath[PathToExit[cell]] = cell
            cell = PathToExit[cell]
        
        for cell in ForwardPath.values(): # goes to each value within the dictionary and makes it visible to the player
            cell.set_visited_hints(True)
                                    
    def remove_walls(self, current_cell: Cell, next_cell: Cell):
        # Get row column positioning from both cells 
        current_cell_column_row_positioning = current_cell.get_row_column_positioning()
        next_cell_column_row_positioning = next_cell.get_row_column_positioning()

        # column then row [column, row]
        # x, y positions is under the assumption that the 'grid of cells' will act as the x, y plane
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
