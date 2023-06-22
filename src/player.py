import pygame
from pygame.sprite import AbstractGroup
from maze_generation import * 

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):

        self.__width = 60
        self.__height = 60

        self.__initial_x = 50
        self.__initial_y = 50

        player_up = pygame.transform.scale(pygame.image.load("src/player images/player_up.png"), (self.__width, self.__height)).convert_alpha()
        player_down = pygame.transform.scale(pygame.image.load("src/player images/player_down.png"), (self.__width, self.__height)).convert_alpha()
        player_right = pygame.transform.scale(pygame.image.load("src/player images/player_right.png"), (self.__width, self.__height)).convert_alpha()
        player_left = pygame.transform.scale(pygame.image.load("src/player images/player_left.png"), (self.__width, self.__height)).convert_alpha()

        self.__images = [player_up, player_down, player_right, player_left]
        self.__frame_index = 0
        self.__image = self.__images[self.__frame_index]
        self.__velocity = 100
        self.__rect = self.__image.get_rect(center=(self.__initial_x, self.__initial_y))

        self.cell_walls_visited = []
    
    def get_player_image(self):
        self.__image = self.__images[self.get_frame_index()] # updates the player image before returning it to be blitted onto the screen
        return self.__image

    def get_player_positioning(self): # https://stackoverflow.com/questions/75347619/how-do-i-find-the-position-coordinates-of-my-rect
        x, y = self.__rect.center
        return [x, y]

    def get_frame_index(self):
        return self.__frame_index
    
    def set_frame_index(self, index_to_be_set: int):
        self.__frame_index = index_to_be_set
    
    def get_rect(self): # get rect positioning of image 
        return self.__rect
    
    def get_index(self, rects):
        index = self.get_rect().collidelist(rects)
        return index

    def check_current_cell(self, rects, cols, grid_of_cells):
        index = self.get_index(rects)
        row_number = index // cols
        cols_number = index - (cols * row_number)
        if (self.get_rect().left >= rects[index].left and self.get_rect().right <= rects[index].right and self.get_rect().top >= rects[index].top and self.get_rect().bottom <= rects[index].bottom):
            print(f'player is inside cell at {grid_of_cells[row_number][cols_number].get_row_column_positioning()}')
            print(f"Walls of current_cell: {grid_of_cells[row_number][cols_number].get_walls()}")
            print(f"Index of cell in rects list: {index}")
            print("\n")
        else:
            print("\nNot in a cell!")
        walls = grid_of_cells[row_number][cols_number].get_walls()
        return walls
            

    def player_input(self, rects, cols, grid_of_cells, event): # gets player input for movement
        walls = self.check_current_cell(rects, cols, grid_of_cells)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not walls['top']: # Movement Up
                self.__rect.y -= self.__velocity
                self.set_frame_index(0)
                    
            elif event.key == pygame.K_s and not walls['bottom']: # Movement down 
                self.__rect.y += self.__velocity
                self.set_frame_index(1)

            elif event.key == pygame.K_d and not walls['right']: # Movement right
                self.__rect.x += self.__velocity 
                self.set_frame_index(2)
            
            elif event.key == pygame.K_a and not walls['left']: # Movement left
                self.__rect.x -= self.__velocity
                self.set_frame_index(3)