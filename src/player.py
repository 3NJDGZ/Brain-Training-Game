import pygame
import os
from pygame.sprite import AbstractGroup

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):

        self.__width = 80
        self.__height = 80

        self.__initial_x = 50
        self.__initial_y = 50

        player_up = pygame.transform.scale(pygame.image.load("src/player images/player_up.png"), (self.__width, self.__height)).convert_alpha()
        player_down = pygame.transform.scale(pygame.image.load("src/player images/player_down.png"), (self.__width, self.__height)).convert_alpha()
        player_right = pygame.transform.scale(pygame.image.load("src/player images/player_right.png"), (self.__width, self.__height)).convert_alpha()
        player_left = pygame.transform.scale(pygame.image.load("src/player images/player_left.png"), (self.__width, self.__height)).convert_alpha()

        self.__images = [player_up, player_down, player_right, player_left]
        self.__frame_index = 0
        self.__image = self.__images[self.__frame_index]
        self.__velocity = 5
        self.__rect = self.__image.get_rect(center= (self.__initial_x, self.__initial_y))
    
    def get_player_image(self):
        self.__image = self.__images[self.get_frame_index()] # updates the player image before returning it to be blitted onto the screen
        return self.__image

    def get_frame_index(self):
        return self.__frame_index
    
    def set_frame_index(self, index_to_be_set: int):
        self.__frame_index = index_to_be_set
    
    def get_rect(self):
        return self.__rect
    
    def player_input(self): # gets player input for movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: # Movement up
            self.__rect.y -= self.__velocity
            self.set_frame_index(0)
        
        elif keys[pygame.K_s]: # Movement down 
            self.__rect.y += self.__velocity
            self.set_frame_index(1)

        elif keys[pygame.K_d]: # Movement right
            self.__rect.x += self.__velocity 
            self.set_frame_index(2)
        
        elif keys[pygame.K_a]: # Movement left
            self.__rect.x -= self.__velocity
            self.set_frame_index(3)
