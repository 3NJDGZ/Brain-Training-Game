import pygame
from pygame.sprite import AbstractGroup
from maze_generation import * 

pygame.init()

class Player(pygame.sprite.Sprite):
    """
    A class to represent the Player

    ...

    Attributes
    ----------
    width : int
        width of player image. 
    height : int 
        height of player image. 
    initial_x : int 
        initial x co-ordinate. 
    inital_y : int 
        initial y co-ordinate. 
    player_up : image 
        image of player 'up' animation.
    player_down : image 
        image of player 'down' animation. 
    player_right : image 
        image of player 'right' animation. 
    player_left : image 
        image of player 'left' animation.
    images : array 
        array of the player image animations.
    frame_index : int
        integer value used to represent what frame from 'images' should be shown.
    velocity : int
        how mnay pixels the player can move across x, y plane. 
    rect : rect 
        pygame rect object of the player image from 'images'.
    
    Methods
    -------
    get_player_image():
        returns the current player image frame.
    get_player_positioning():
        returns x, y position of player relative to the center of its rect.
    get_frame_index():
        returns the current value of the frame index.
    set_frame_index(index_to_be_set: int):
        sets the frame index to the value from 'index_to_be_set'.
    get_rect():
        returns player rect.
    get_index():
        returns the index value of the rect that has collided with the player rect.
    check_current_cell(rects, cols, grid_of_cells):
        checks the current cell that the player is in and what corresponding walls it has are present.
    player_input(rects, cols, grid_of_cells, event):
        used for player movement and player collision with walls of the maze.
    """
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
        """
        Returns the index value of the rect that has collided with the player, aka the current cell.

        Parameters
        ----------
        rects : 1D array
            a list of all the rects generated from each cell from 'grid_of_cells'.
        
        Returns
        -------
        index : int 
            integer value representing the index positioning.
        """
        index = self.get_rect().collidelist(rects)
        return index

    def check_current_cell(self, rects, cols, grid_of_cells):
        """
        Checks the current cell that the player is in and the walls present for that current cell.
        Also calculates the corresponding position in the two dimensional array 'grid_of_cells' from the 1 dimensional array 'rects'.
            
        Parameters
        ----------
        rects : 1D array
            a list of all the rects generated from each cell from 'grid_of_cells'.
        cols : int 
            decimal integer of the number of columns calculated from the tile size of each cell.
        grid_of_cells : 2D array
            2D array representation of the cells used for the creation of the maze.
    
        Returns
        -------
        walls : dict 
            dict object that stores the values of what walls are present for the current cell.
        """
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

        # Checks if the Player has Arrived at the exit of the maze
        if grid_of_cells[row_number][cols_number].get_exit_value():
            print("Arrived at the exit!")

        walls = grid_of_cells[row_number][cols_number].get_walls()
        return walls    

    def player_input(self, rects, cols, grid_of_cells, event): # gets player input for movement
        """
        Used for Player Input and Movement aswell as collision theory with the walls of the maze.

        Parameters
        ----------
        rects : 1D array 
            a list of all the rects generated from each cell from 'grid_of_cells'.
        cols : int 
            decimal integer of the number of columns calculated from the tile size of each cell.
        grid_of_cells : 2D array
            2D array representation of the cells used for the creation of the maze.
        event : pygame object 
            a pygame event that will be evaluated (this allows the single button key presses required for player movement as well as maze collision theory).
        
        Returns
        -------
        None
        """
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