import pygame
from exercises import *
from Maze_Generation import * 

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, initial_x, inital_y, velocity):

        self.__width = width
        self.__height = height

        self.__initial_x = initial_x
        self.__initial_y = inital_y

        player_up = pygame.transform.scale(pygame.image.load("src/player images/player_up.png"), (self.__width, self.__height)).convert_alpha()
        player_down = pygame.transform.scale(pygame.image.load("src/player images/player_down.png"), (self.__width, self.__height)).convert_alpha()
        player_right = pygame.transform.scale(pygame.image.load("src/player images/player_right.png"), (self.__width, self.__height)).convert_alpha()
        player_left = pygame.transform.scale(pygame.image.load("src/player images/player_left.png"), (self.__width, self.__height)).convert_alpha()

        self.__images = [player_up, player_down, player_right, player_left]
        self.__frame_index = 0
        self.__image = self.__images[self.__frame_index]
        self.__velocity = velocity
        self.__rect = self.__image.get_rect(center=(self.__initial_x, self.__initial_y))
    
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
    
    def get_index(self, rects): # Returns the index value of the rect that has collided with the player, aka the current cell.
        index = self.get_rect().collidelist(rects)
        return index

    def check_current_cell(self, rects, cols, grid_of_cells):
        # Checks the current cell that the player is in and the walls present for that current cell.
        # Also calculates the corresponding position in the two dimensional array 'grid_of_cells' from the 1 dimensional array 'rects'.
        index = self.get_index(rects)
        row_number = index // cols
        cols_number = index - (cols * row_number)
        # if (self.get_rect().left >= rects[index].left and self.get_rect().right <= rects[index].right and self.get_rect().top >= rects[index].top and self.get_rect().bottom <= rects[index].bottom):
        #     print(f'player is inside cell at {grid_of_cells[row_number][cols_number].get_row_column_positioning()}')
        #     print(f"Walls of current_cell: {grid_of_cells[row_number][cols_number].get_walls()}")
        #     print(f"Index of cell in rects list: {index}")
        #     print("\n")
        # else:
        #     print("\nNot in a cell!")

        walls = grid_of_cells[row_number][cols_number].get_walls()
        return walls  
    
    def calculate_row_cols(self, rects, cols):
        index = self.get_index(rects)
        row_number = index // cols
        cols_number = index - (cols * row_number)
        return row_number, cols_number
    
    def get_current_cell(self, rects, cols, grid_of_cells):
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        return grid_of_cells[row_number][cols_number]
        
    def check_type_of_exercise_cell(self, rects, cols, grid_of_cells):
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        if grid_of_cells[row_number][cols_number].get_exercise_present():
            return grid_of_cells[row_number][cols_number].get_exercise()
    
    def check_if_exercise_cell_is_complete(self, rects, cols, grid_of_cells):
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        if grid_of_cells[row_number][cols_number].get_exercise_present():
            return grid_of_cells[row_number][cols_number].get_exercise().get_completely_finished()

    def check_collision_with_exercise_cell(self, rects, cols, grid_of_cells, WIN):
        row_number, cols_number = self.calculate_row_cols(rects, cols)

        if grid_of_cells[row_number][cols_number].get_exercise_present():
            grid_of_cells[row_number][cols_number].get_exercise().draw_exercise_on_screen(WIN)
            return grid_of_cells[row_number][cols_number].get_exercise()

    def check_collision_with_exit_cell(self, rects, cols, grid_of_cells):
        row_number, cols_number = self.calculate_row_cols(rects, cols)

        if grid_of_cells[row_number][cols_number].get_exit_value():
            return True
        else:
            return False

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