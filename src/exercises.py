import pygame
from abc import ABC
from abc import abstractmethod
from mysqlmodel import PlayerDataManager, MySQLDatabaseConnection

pygame.init()

class Exercises(ABC):
    def __init__(self, CognitiveAreaName: str, CognitiveAreaID: int):
        self._CognitiveAreanName = CognitiveAreaName
        self._CognitiveAreaID = CognitiveAreaID
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
    def draw_surface_on_screen(self):
        pass

class TestExercise (Exercises):
    def __init__(self, CognitiveAreaName: str, CognitiveAreaID: int):
        super().__init__(CognitiveAreaName, CognitiveAreaID)
    
    def calculate_points(self):
        return super().calculate_points()
    
    def record_points_on_DB(self, points):
        return super().record_points_on_DB(points)
    
    def show_UI_elements(self):
        return super().show_UI_elements()
    
    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def draw_surface_on_screen(self, WIN):
        pygame.draw.rect(WIN, (122, 51, 255), pygame.Rect(160, 90, self._WIDTH, self._HEIGHT))
    