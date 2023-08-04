import pygame
from random import randint
from abc import ABC
from abc import abstractmethod
from mysqlmodel import PlayerDataManager
import pygame_gui
from pygame_gui.core import ObjectID


# Class Errors
class NumberOfOperandError(Exception):
    def __init__(self, message = "Number of Operands not in (1, 5) range."):
        self.message = message
        super().__init__(self.message)

class NoEquations(Exception):
    def __init__(self, message = "No Equations present/generated for the Chalkboard Challenge Exercise"):
        self.message = message
        super().__init__(self.message)

class CognitiveExercise(ABC):
    def __init__(self, CognitiveAreaID: int, PDM: PlayerDataManager):
        self._CognitiveAreaID = CognitiveAreaID
        self._PDM = PDM
        self._WIDTH = 1280
        self._HEIGHT = 720

    @abstractmethod
    def calculate_points(self):
        pass

    @abstractmethod
    def record_points_on_DB(self, points):
        pass

    @abstractmethod
    def draw_exercise_on_screen(self, WIN):
        pass

    @abstractmethod
    def user_input(self, event):
        pass

# Chalboard Challenge Code (Cognitive Area: Problem-Solving)
class ChalkboardChallenge(CognitiveExercise):
    def __init__(self, CognitiveAreaID: int, PDM: PlayerDataManager):
        super().__init__(CognitiveAreaID, PDM)
        self.__EQUATIONS = []
        self.__number_of_equations_to_do = 5
        self.__amount_of_correct_answers = 0
        self.__amount_of_incorrect_answers = 0
        self.__points_earned = 0
        self.__record_points = False
        self.lower_threshold = 0
        self.higher_threshold = 10

    def set_record_points(self, value_to_be_set: bool):
        self.__record_points = value_to_be_set

    def calculate_points(self):
        self.__amount_of_incorrect_answers = 5 - self.__amount_of_correct_answers
        self.__points_earned = (self.__amount_of_correct_answers * 200) + (self.__amount_of_incorrect_answers * -200)
        print(self.__points_earned) 
        return self.__points_earned
    
    def record_points_on_DB(self, points):
        self._PDM.record_points_from_exercises_on_DB(points, self._CognitiveAreaID)

    def user_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.__number_of_equations_to_do != 0:
                if event.key == pygame.K_z:
                    self.__number_of_equations_to_do -= 1
                    if self.__EQUATIONS[0].get_answer() > self.__EQUATIONS[1].get_answer():
                        self.__amount_of_correct_answers += 1
                    self.generate_new_set_of_equations()
                elif event.key == pygame.K_x:
                    self.__number_of_equations_to_do -= 1
                    if self.__EQUATIONS[0].get_answer() == self.__EQUATIONS[1].get_answer():
                        self.__amount_of_correct_answers += 1
                    self.generate_new_set_of_equations()
                elif event.key == pygame.K_c:
                    self.__number_of_equations_to_do -= 1
                    if self.__EQUATIONS[0].get_answer() < self.__EQUATIONS[1].get_answer():
                        self.__amount_of_correct_answers += 1
                    self.generate_new_set_of_equations()
    
    def show_final_score(self, font, WIN):
        self.__EQUATIONS = []
        text = f"Final Score: {self.__amount_of_correct_answers} / 5"
        text_surface = font.render(text, True, (255, 255, 255))
        WIN.blit(text_surface, ((1600 - text_surface.get_width()) / 2, (900 - text_surface.get_height()) / 2))
 
    def draw_exercise_on_screen(self, WIN):
        pygame.draw.rect(WIN, (2, 5, 25), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))

        # font
        font = pygame.font.Font(None, 36) 
        if self.__number_of_equations_to_do > 0:

            pygame.draw.rect(WIN, (50, 50, 50), pygame.Rect(180, 110, 610, 680)) # left tile
            pygame.draw.rect(WIN, (50, 50, 100), pygame.Rect(810, 110, 610, 680)) # right tile
            pygame.draw.rect(WIN, (100, 50, 100), pygame.Rect(600, 610, 400, 200)) # middle selection tile

            # Middle Selection Tile 
            text_to_be_shown = "Determine which side is larger"
            text_to_be_shown_surface = font.render(text_to_be_shown, True, (255, 255, 255))
            controls = "LEFT 'Z', EQUAL 'X', RIGHT 'C'"
            controls_surface = font.render(controls, True, (255, 255, 255))

            # First Equation
            equation1 = self.__EQUATIONS[0].get_equation()
            equation1_surface = font.render(equation1, True, (255, 255, 255))

            # Second Equation 
            equation2 = self.__EQUATIONS[1].get_equation()
            equation2_surface = font.render(equation2, True, (255, 255, 255))

            WIN.blit(equation1_surface, ((610 + 180) / 2, (680 + 110) / 2))
            WIN.blit(equation2_surface, (610 + ((610 + 180) / 2), (680 + 110) / 2))
            WIN.blit(text_to_be_shown_surface, ((1600 - text_to_be_shown_surface.get_width()) / 2, 625))
            WIN.blit(controls_surface, ((1600 - controls_surface.get_width()) / 2, 675))
        else:
            self.show_final_score(font, WIN)
            if not self.__record_points:
                points = self.calculate_points()
                self.record_points_on_DB(points)
                self.set_record_points(True)
        
    def generate_equation(self):
        operands = []
        no_of_operands = randint(2, 5)
        for x in range(no_of_operands):
            random_operand = randint(self.lower_threshold, self.higher_threshold)
            operands.append(random_operand)
        self.__EQUATIONS.append(Equation(operands))

    def generate_new_set_of_equations(self):
        self.__EQUATIONS = []
        self.generate_equation()
        self.generate_equation()
    
    def show_every_equation(self):
        if len(self.__EQUATIONS) > 0:
            for equation in self.__EQUATIONS:
                print(f"{equation.get_equation()} = {equation.get_answer()}")
        else:
            raise NoEquations()

class Equation():
    def __init__(self, operands):
        self.operators = ["+", "-", "*", "//"]
        self.__operands = operands
        self.__difficulty = len(operands) -1
        self.__answer = 0
        self.__equation = self.create_equation()
    
    def get_equation(self):
        return self.__equation

    def get_answer(self):
        return self.__answer
    
    def get_random_operator(self):
        random_operator = self.operators[randint(0, 3)]
        return random_operator

    def create_equation(self):
        # lowest number is the easiest, largest is the hardest
        if len(self.__operands) <= 5:
            while True:
                try:
                    if self.__difficulty == 1:
                        self.__equation = f"{self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}"
                    elif self.__difficulty == 2:
                        self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} {self.__operands[2]}"
                    elif self.__difficulty == 3:
                        self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})"
                    elif self.__difficulty == 4:
                        self.__equation = f"(({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})) {self.get_random_operator()} {self.__operands[4]}"
                    self.__answer = eval(self.__equation) # https://www.geeksforgeeks.org/python-evaluate-expression-given-in-string/
                    if isinstance(self.__answer, int):
                        break
                except ZeroDivisionError:
                    print("Cannot Divide By Zero!")
            return self.__equation
        else:
            raise NumberOfOperandError()
# End of Chalkboard Challenge Code

# Memory Matrix Code (Cognitive Area: Memory)
class MemoryMatrix(CognitiveExercise):
    def __init__(self, CognitiveAreaID: int, PDM: PlayerDataManager):
        super().__init__(CognitiveAreaID, PDM)
        # Necessary Attributes
        self.__points_earned = 0
        self.__trail_active = False

        # Patterns
        number_of_highlighted_cells_one = randint(4, 10)
        number_of_highlighted_cells_two = randint(12, 18)
        number_of_highlighted_cells_three = randint(20, 26)
        self.__patterns = [MMPattern(number_of_highlighted_cells_one), MMPattern(number_of_highlighted_cells_two), MMPattern(number_of_highlighted_cells_three)]
        self.__current_pos = 0
        self.__current_pattern = self.__patterns[self.__current_pos]

        # Inputs
        self.__space_bar_down = False
        self.__space_bar_press_time = 0

        # Mouse
        self.__mouse_position = 0
        self.__mouse_x = 0
        self.__mouse_y = 0

    def find_mouse_pos(self): # https://www.youtube.com/watch?v=OYw9D75d7Lw
        self.__mouse_position = pygame.mouse.get_pos()
        self.__mouse_x = self.__mouse_position[0]
        self.__mouse_y = self.__mouse_position[1]
        print(f"[{self.__mouse_x}, {self.__mouse_y}]")
    
    def find_cell_position(self):
        cell_column_positioning = (self.__mouse_x - 180) // 100
        cell_row_positioining = (self.__mouse_y - 110) // 100
        return cell_column_positioning, cell_row_positioining
    
    def user_selection_cells(self):
        if self.__mouse_x >= 180 and self.__mouse_y >= 110 and self.__mouse_x <= 980 and self.__mouse_y <= 710:
            col_pos, row_pos = self.find_cell_position()

            # Checking if the user has made 3 errors, if so, it will automatically move to the next trail
            if self.__current_pattern.get_number_of_errors() == 3:
                print("wrong")
                self.go_to_next_trail()

            # Abstract the user selected patterns
            if self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].get_highlighted_cell():
                self.__current_pattern.dynamically_update_user_selected_cells(col_pos, row_pos)

            # Checking if the user has selected the right cell
            if self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].get_highlighted_cell() and not self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].get_selected_by_user():
                self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].set_selected_by_user(True)
                # increase the points 
                print("correct cell")
                self.__points_earned += 20 
            elif self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].get_highlighted_cell() and self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].get_selected_by_user():
                print("you have already selected this cell!!!")
            else:
                self.__current_pattern.increment_number_of_errors()
                self.__current_pattern.get_grid_of_cells()[row_pos][col_pos].set_incorrect(True)
                print("you selected a wrong cell")
    
    def go_to_next_trail(self):
        if self.__current_pos < 2:
            self.__current_pattern.set_finished(True)
            self.__current_pos += 1
            self.__current_pattern = self.__patterns[self.__current_pos]

            # Reset all base values back to original state
            self.__space_bar_down = False
            self.__trail_active = False
        else:
            print("No more trails!")

    def calculate_points(self):
        return super().calculate_points()
    
    def record_points_on_DB(self, points):
        return super().record_points_on_DB(points)
    
    def draw_exercise_on_screen(self, WIN):
        # Drawing
        pygame.draw.rect(WIN, (255, 216, 107), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
        self.__current_pattern.draw_cells(WIN)

        # font
        font = pygame.font.Font(None, 50) 

        # Text 
        score_text = f"Total Score: {self.__points_earned}"
        score_text_surface = font.render(score_text, True, (255, 255, 255))
        WIN.blit(score_text_surface, (1000, 110))
        trail_number_text = f"Trail: {self.__current_pos + 1}"
        trail_number_text_surface = font.render(trail_number_text, True, (255, 255, 255))
        WIN.blit(trail_number_text_surface, (1000, 160))

        # Checking Timers
        self.__current_time = pygame.time.get_ticks()
        if self.__space_bar_down:
            self.__current_pattern.set_show_value(True)
            if self.__current_time - self.__space_bar_press_time > 4000: # Checks if 4 seconds have passed since the player has last pressed the space bar
                self.__space_bar_down = False
                self.__trail_active = True
                self.__current_pattern.set_show_value(False)
                self.__current_pattern.set_user_selected_cells(True)

        # print(f"Current Time: {self.__current_time}, Button Press Time: {self.__space_bar_press_time}")

        # https://www.youtube.com/watch?v=YOCt8nsQqEo pygame timers
    
    def user_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.__space_bar_down and not self.__trail_active:
                self.__space_bar_press_time = pygame.time.get_ticks() 
                self.__space_bar_down = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left mouse button
                # print("Left mouse button has been clicked!")
                self.find_mouse_pos()
                if self.__trail_active:
                    self.user_selection_cells()
                # print(f"Mouse Position: {self.__mouse_position}")

class MMPattern():
    def __init__(self, number_of_highlighted_cells: int):
        self.__grid_of_cells = []
        self.__abstracted_pattern = [] # Abstracted Pattern of the Highlighted Cells represented as a 2D matrix with 1s and 0s
        self.__user_selected_grid_of_cells = [] # Abstracted Pattern of the selected cells by the user represented in the same way as mentioned above
        self.__tile_size = 100
        self.__rows = 6
        self.__cols = 8
        self.__number_of_highlighted_cells = number_of_highlighted_cells
        self.__finished = False
        self.__show_highlights = False
        self.__show_user_selected_cells = False
        self.__errors = 0 # cap at three

        # Setup the grid of cells 
        for a in range(self.__rows):
            row = []
            for b in range(self.__cols):
                row.append(MMCell(self.__tile_size * b, self.__tile_size * a, self.__tile_size, self.__cols, self.__rows, (0, 0, 0)))
            self.__grid_of_cells.append(row)
        
        # Setup an empty grid of cells
        for a in range(self.__rows):
            row = []
            for b in range(self.__cols):
                row.append(0)
            self.__user_selected_grid_of_cells.append(row)
    
        self.generate_cell_pattern()
        self.store_pattern()
    
    def get_user_selected_grid_of_cells(self):
        return self.__user_selected_grid_of_cells
    
    def get_abstracted_pattern(self):
        return self.__abstracted_pattern
    
    def set_finished(self, value_to_be_set: bool):
        self.__finished = value_to_be_set
    
    def get_finished(self):
        return self.__finished
    
    def get_number_of_errors(self):
        return self.__errors

    def increment_number_of_errors(self):
        self.__errors += 1
    
    def get_grid_of_cells(self):
        return self.__grid_of_cells
    
    def set_show_value(self, value_to_be_set: bool):
        self.__show_highlights = value_to_be_set
    
    def set_user_selected_cells(self, value_to_be_set: bool):
        self.__show_user_selected_cells = value_to_be_set
    
    def generate_cell_pattern(self):
        for x in range(0, self.__number_of_highlighted_cells):
                    # Generate Random Positioning for Cell
                    random_row = randint(0, self.__rows)
                    random_col = randint(0, self.__cols)
                    random_cell = self.__grid_of_cells[random_row-1][random_col-1]

                    # Check if current cell is not highlighted
                    if random_cell.get_highlighted_cell() == False:
                        random_cell.set_highlighted(True)
                    else:
                        # If it is highlighted, then find another position 
                        while True:
                            random_row = randint(0, self.__rows)
                            random_col = randint(0, self.__cols)
                            random_cell = self.__grid_of_cells[random_row-1][random_col-1]
                            if not random_cell.get_highlighted_cell():
                                random_cell.set_highlighted(True)
                                break
    
    def store_pattern(self):
        # creating and storing the pattern, 1s representing a a highlighted cell
        for row in self.__grid_of_cells:
            pattern_row = []
            for cell in row:
                if cell.get_highlighted_cell():
                    pattern_row.append(1)
                else:
                    pattern_row.append(0)
            self.__abstracted_pattern.append(pattern_row)
        
        # Printing the stored pattern
        for row in self.__abstracted_pattern:
            print(row)
        print("\n")
    
    def dynamically_update_user_selected_cells(self, col_pos: int, row_pos: int):
        self.__user_selected_grid_of_cells[row_pos][col_pos] = 1
        print("\n")
        for row in self.__user_selected_grid_of_cells:
            print(row)

    def draw_cells(self, WIN):
        for row in self.__grid_of_cells:
                for cell in row:
                    cell.draw_cell(WIN, self.__show_highlights, self.__show_user_selected_cells)

class MMCell():
    def __init__(self, x: int, y: int, tile_size: int, cols: int, rows: int, LINE_COLOUR):
        self.__x = x + 180
        self.__y = y + 110
        self.tile_size = tile_size
        self.cols = cols
        self.rows = rows
        self.LINE_COLOUR = LINE_COLOUR
        self.LINE_WIDTH = 5
        self.__walls = {"top": True,
                      "right": True,
                      "bottom": True,
                      "left": True}
        
        self.__highlighted = False
        self.__selected_by_user = False
        self.__incorrect = False
    
    def set_incorrect(self, value_to_be_set: bool):
        self.__incorrect = value_to_be_set

    def set_highlighted(self, value_to_be_set: bool):
        self.__highlighted = value_to_be_set
    
    def get_highlighted_cell(self):
        return self.__highlighted

    def set_selected_by_user(self, value_to_be_set: bool):
        self.__selected_by_user = value_to_be_set
    
    def get_selected_by_user(self):
        return self.__selected_by_user
    
    def draw_cell(self, WIN, draw_highlighted: bool, draw_user_selection: bool):

        if self.__incorrect:
            pygame.draw.rect(WIN, (255, 0, 0), (self.__x+5, self.__y+5, self.tile_size-10, self.tile_size-10))
        if self.__selected_by_user and draw_user_selection: # draw the selected cells by the user
            pygame.draw.rect(WIN, (176, 206, 255), (self.__x+5, self.__y+5, self.tile_size-10, self.tile_size-10))
        if self.__highlighted and draw_highlighted: # draw the highlighted cells from the pattern to show to the user
            pygame.draw.rect(WIN, (0, 213, 255), (self.__x+5, self.__y+5, self.tile_size-10, self.tile_size-10))
        if self.__walls['top']:
            pygame.draw.line(WIN, self.LINE_COLOUR, (self.__x, self.__y), (self.__x + self.tile_size, self.__y), self.LINE_WIDTH)
        if self.__walls['right']:
            pygame.draw.line(WIN, self.LINE_COLOUR, (self.__x + self.tile_size, self.__y), (self.__x + self.tile_size, self.__y + self.tile_size), self.LINE_WIDTH)
        if self.__walls['bottom']:
            pygame.draw.line(WIN, self.LINE_COLOUR, (self.__x + self.tile_size, self.__y + self.tile_size), (self.__x, self.__y + self.tile_size), self.LINE_WIDTH)
        if self.__walls['left']:
            pygame.draw.line(WIN, self.LINE_COLOUR, (self.__x, self.__y + self.tile_size), (self.__x, self.__y), self.LINE_WIDTH)

# End of Memory Matrix Code


# Test Exercise Code
class TestExercise(CognitiveExercise):
    def __init__(self, CognitiveAreaID: int, PDM: PlayerDataManager):
        super().__init__(CognitiveAreaID, PDM)
    
    def user_input(self, event):
        return super().user_input(event)
    
    def calculate_points(self):
        return super().calculate_points()
    
    def record_points_on_DB(self, points):
        return super().record_points_on_DB(points)
    
    def draw_exercise_on_screen(self, WIN):
        pygame.draw.rect(WIN, (122, 51, 255), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
# End of Test Exercise Code
