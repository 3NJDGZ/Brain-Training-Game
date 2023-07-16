import pygame
from random import randint
from abc import ABC
from abc import abstractmethod
from mysqlmodel import PlayerDataManager, MySQLDatabaseConnection

pygame.init()

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
    def __init__(self, CognitiveAreas):
        self._CognitiveAreas = CognitiveAreas
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

# Chalboard Challenge Code
class ChalkboardChallenge(CognitiveExercise):
    def __init__(self, CognitiveAreas):
        super().__init__(CognitiveAreas)
        self.__EQUATIONS = []

    def calculate_points(self):
        return super().calculate_points()
    
    def record_points_on_DB(self, points):
        return super().record_points_on_DB(points)
    
    def show_UI_elements(self):
        return super().show_UI_elements()
    
    def remove_UI_elements(self):
        return super().remove_UI_elements()

    def user_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and self.__EQUATIONS[0].get_answer() > self.__EQUATIONS[1].get_answer():
                print("Z has been pressed")
            elif event.key == pygame.K_x and self.__EQUATIONS[0].get_answer() == self.__EQUATIONS[1].get_answer():
                print("X has been pressed")
            elif event.key == pygame.K_c and self.__EQUATIONS[0].get_answer() < self.__EQUATIONS[1].get_answer():
                print("C has been pressed")
    
    def draw_exercise_on_screen(self, WIN):
        pygame.draw.rect(WIN, (2, 5, 25), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
        pygame.draw.rect(WIN, (50, 50, 50), pygame.Rect(180, 110, 610, 680)) # left tile
        pygame.draw.rect(WIN, (50, 50, 100), pygame.Rect(810, 110, 610, 680)) # right tile
        pygame.draw.rect(WIN, (100, 50, 100), pygame.Rect(600, 610, 400, 200)) # middle selection tile

        # fonts
        font = pygame.font.Font(None, 36) 

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
    
    def generate_equation(self):
        operands = []
        no_of_operands = randint(2, 5)
        for x in range(no_of_operands):
            random_operand = randint(1, 20)
            operands.append(random_operand)
        self.__EQUATIONS.append(Equation(operands))
    
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

    def check_equation(self):
        if self.__difficulty == 1:
            while not isinstance(self.__answer, int):
                self.__equation = f"{self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}"
                self.__answer = eval(self.__equation)
        elif self.__difficulty == 2:
            while not isinstance(self.__answer, int):
                self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} {self.__operands[2]}"
                self.__answer = eval(self.__equation)
        elif self.__difficulty == 3:
            while not isinstance(self.__answer, int):
                self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})"
                self.__answer = eval(self.__equation)
        elif self.__difficulty == 4:
            while not isinstance(self.__answer, int):
                self.__equation = f"(({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})) {self.get_random_operator()} {self.__operands[4]}"
                self.__answer = eval(self.__equation)

    def create_equation(self):
        # lowest number is the easiest, largest is the hardest
        if len(self.__operands) <= 5:
            if self.__difficulty == 1:
                self.__equation = f"{self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}"
                self.__answer = eval(self.__equation) # https://www.geeksforgeeks.org/python-evaluate-expression-given-in-string/
                self.check_equation()
            elif self.__difficulty == 2:
                self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} {self.__operands[2]}"
                self.__answer = eval(self.__equation)
                self.check_equation()
            elif self.__difficulty == 3:
                self.__equation = f"({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})"
                self.__answer = eval(self.__equation)
                self.check_equation()
            elif self.__difficulty == 4:
                self.__equation = f"(({self.__operands[0]} {self.get_random_operator()} {self.__operands[1]}) {self.get_random_operator()} ({self.__operands[2]} {self.get_random_operator()} {self.__operands[3]})) {self.get_random_operator()} {self.__operands[4]}"
                self.__answer = eval(self.__equation)
                self.check_equation()               

            return self.__equation
        else:
            raise NumberOfOperandError()
    
# End of Chalkboard Challenge code
class TestExercise(CognitiveExercise):
    def __init__(self, CognitiveAreas):
        super().__init__(CognitiveAreas)
    
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
    