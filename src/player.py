import pygame
from exercises import *
from Maze_Generation import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, initial_x, inital_y, velocity):
        # Size of the Player when it is drawn onto the screen
        self.__width = width
        self.__height = height

        # Initial X position, initial Y position
        self.__initial_x = initial_x
        self.__initial_y = inital_y

        # Individual Frames showing left, right, up, down
        player_up = pygame.transform.scale(pygame.image.load("src/player images/player_up.png"), (self.__width, self.__height)).convert_alpha()
        player_down = pygame.transform.scale(pygame.image.load("src/player images/player_down.png"), (self.__width, self.__height)).convert_alpha()
        player_right = pygame.transform.scale(pygame.image.load("src/player images/player_right.png"), (self.__width, self.__height)).convert_alpha()
        player_left = pygame.transform.scale(pygame.image.load("src/player images/player_left.png"), (self.__width, self.__height)).convert_alpha()

        # Current Frame; allows the ease of changing frames when required
        self.__images = [player_up, player_down, player_right, player_left]
        self.__frame_index = 0
        self.__image = self.__images[self.__frame_index]

        # Speed of the player when traversing through the maze
        self.__velocity = velocity

        # Rect of the player which is needed for collisions with cells within the maze
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
    
    def get_index(self, rects): # Returns the index positioning value of the rect that has collided with the player, aka the current cell.
        index = self.get_rect().collidelist(rects) # rects is a 1 dimensional array which is created within the Maze Object, stores all rects for every cell
        return index
    
    def calculate_row_cols(self, rects, cols):
        # This subroutine gets the index value from a 1D array (rects) and converts it into two index values which are used to identify the same exact cell rect if it were structured in a 2D array (GRID)
        index = self.get_index(rects) 
        row_number = index // cols
        cols_number = index - (cols * row_number)
        return row_number, cols_number
    
    def get_current_cell_walls(self, rects, cols, grid_of_cells):
        # Checks the current cell that the player is in and the walls present for that current cell.
        # Also calculates the corresponding position in the two dimensional array 'grid_of_cells' from the 1 dimensional array 'rects'.
        row_number, cols_number = self.calculate_row_cols(rects, cols)

        walls = grid_of_cells[row_number][cols_number].get_walls()
        return walls  
    
    def get_current_cell(self, rects, cols, grid_of_cells):
        # Gets the current cell that the Player is in
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        return grid_of_cells[row_number][cols_number]
        
    def get_exercise_cell(self, rects, cols, grid_of_cells):
        # Checks if the player is at an exercise cell
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        if grid_of_cells[row_number][cols_number].get_exercise_present():
            return grid_of_cells[row_number][cols_number].get_exercise()
    
    def check_if_exercise_cell_is_complete(self, rects, cols, grid_of_cells):
        # used to identify what exercise is currently active; used for player input, called within the 'main.py' file
        row_number, cols_number = self.calculate_row_cols(rects, cols)
        if grid_of_cells[row_number][cols_number].get_exercise_present():
            return grid_of_cells[row_number][cols_number].get_exercise().get_completely_finished()

    def check_and_then_draw_exercise_cell(self, rects, cols, grid_of_cells, WIN):
        # Used to identify that the player is at an exercise cell, and calls the exercise's draw method
        row_number, cols_number = self.calculate_row_cols(rects, cols)

        if grid_of_cells[row_number][cols_number].get_exercise_present():
            grid_of_cells[row_number][cols_number].get_exercise().draw_exercise_on_screen(WIN)

    def check_collision_with_exit_cell(self, rects, cols, grid_of_cells):
        # Checks if the user is at the exit
        row_number, cols_number = self.calculate_row_cols(rects, cols)

        if grid_of_cells[row_number][cols_number].get_exit_value():
            return True
        else:
            return False

    def player_input(self, rects, cols, grid_of_cells, event): # gets player input for movement
        # Retrieve walls of current cell that the user is in
        walls = self.get_current_cell_walls(rects, cols, grid_of_cells)

        # Used to check what walls are present and therefore restrict movement accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not walls['top']: # Movement Up
                self.__rect.y -= self.__velocity # change position of user accordingly
                self.set_frame_index(0) # change frame accordingly
                    
            elif event.key == pygame.K_s and not walls['bottom']: # Movement down 
                self.__rect.y += self.__velocity # change position of user accordingly
                self.set_frame_index(1) # change frame accordingly

            elif event.key == pygame.K_d and not walls['right']: # Movement right
                self.__rect.x += self.__velocity # change position of user accordingly
                self.set_frame_index(2) # change frame accordingly
            
            elif event.key == pygame.K_a and not walls['left']: # Movement left
                self.__rect.x -= self.__velocity # change position of user accordingly
                self.set_frame_index(3) # change frame accordingly