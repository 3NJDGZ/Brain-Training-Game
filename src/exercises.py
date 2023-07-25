import pygame
from random import randint
from abc import ABC
from abc import abstractmethod
from mysqlmodel import PlayerDataManager

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

# Chalboard Challenge Code
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
    
# End of Chalkboard Challenge code
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
    