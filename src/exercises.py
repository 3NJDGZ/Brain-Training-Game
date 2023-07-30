import pygame
import time
from random import randint
from abc import ABC
from abc import abstractmethod
from mysqlmodel import PlayerDataManager


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
    def show_UI_elements(self):
        pass

    @abstractmethod
    def remove_UI_elements(self):
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
    
    def show_UI_elements(self):
        return super().show_UI_elements()
    
    def remove_UI_elements(self):
        return super().remove_UI_elements()

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
            controls = "LEFT 'Z', EQUAL 'X', RIGHT 'C'"
            controls_surface = font.render(controls, True, (255, 255, 255))
            text_to_be_shown_surface = font.render(text_to_be_shown, True, (255, 255, 255))

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
        self.__trails_left = 3
        self.__tile_size = 100
        self.__grid_of_cells = []
        self.__stored_pattern = []

        self.__current_time = 0 
        self.__spacebar_press_time = 0
        self.__space_bar_pressed = False

        # Controls the Size of the grid
        self.__rows = 6
        self.__cols = 10

        # Controls how many highlighted cells there will be (must be less than 60)
        self.__number_of_highlighted_cells = 20

        # Setup the grid of cells 
        for a in range(self.__rows):
            row = []
            for b in range(self.__cols):
                row.append(MMCell(self.__tile_size * b, self.__tile_size * a, self.__tile_size, self.__cols, self.__rows, (0, 0, 0)))
            self.__grid_of_cells.append(row)
        
        self.generate_cell_pattern()
        self.store_pattern()
    
    def store_pattern(self):
        # creating and storing the pattern, 1s representing a a highlighted cell
        for row in self.__grid_of_cells:
            pattern_row = []
            for cell in row:
                if cell.get_highlighted_cell():
                    pattern_row.append(1)
                else:
                    pattern_row.append(0)
            self.__stored_pattern.append(pattern_row)
        
        # Printing the stored pattern
        for row in self.__stored_pattern:
            print(row)
        print("\n")
        
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
    
    def reset_grid_of_cells(self):
        for row in self.__grid_of_cells:
            for cell in row:
                cell.set_highlighted(False)

    def calculate_points(self):
        return super().calculate_points()
    
    def record_points_on_DB(self, points):
        return super().record_points_on_DB(points)
    
    def show_UI_elements(self):
        return super().show_UI_elements()
    
    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def draw_exercise_on_screen(self, WIN):
        pygame.draw.rect(WIN, (255, 216, 107), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
        self.__current_time = pygame.time.get_ticks()
        if self.__space_bar_pressed: # checks if the space bar button has been pressed
            self.draw_cells(WIN, True)
            if self.__current_time - self.__spacebar_press_time > 4000:
                self.draw_cells(WIN, False)
                self.__space_bar_pressed = False
        else:
            self.draw_cells(WIN, False)

        self.show_times()
        # https://www.youtube.com/watch?v=YOCt8nsQqEo pygame timers
    
    def show_times(self):
        print(f"Space Bar Press Time: {self.__spacebar_press_time}, Current Time: {self.__current_time}")
    
    def draw_cells(self, WIN, show_highlights: bool):
        for row in self.__grid_of_cells:
                for cell in row:
                    cell.draw_cell(WIN, show_highlights)

    def user_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.__spacebar_press_time = pygame.time.get_ticks()
                self.__space_bar_pressed = True

class MMCell():
    def __init__(self, x: int, y: int, tile_size: int, cols: int, rows: int, LINE_COLOUR):
        self.__x = x + 180
        self.__y = y + 130
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
    
    def set_highlighted(self, value_to_be_set: bool):
        self.__highlighted = value_to_be_set
    
    def get_highlighted_cell(self):
        return self.__highlighted
    
    def draw_cell(self, WIN, draw_highlighted: bool):
        if self.__highlighted and draw_highlighted: 
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
    
    def show_UI_elements(self):
        return super().show_UI_elements()
    
    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def draw_exercise_on_screen(self, WIN):
        pygame.draw.rect(WIN, (122, 51, 255), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
# End of Test Exercise Code