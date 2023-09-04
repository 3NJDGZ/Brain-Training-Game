# pygame modules
import pygame_gui
from pygame_gui.core import ObjectID
import pygame

# custom modules (player + maze)
from player import Player
from Maze_Generation import Maze

# data handling
from mysqlmodel import MySQLDatabaseConnection, PlayerDataManager

# miscellaneous 
from abc import ABC, abstractmethod

pygame.display.set_caption("Brain Training Game")

PDM = PlayerDataManager(MySQLDatabaseConnection())

class Screen(ABC): # An abstract base class to represent a Screen in a Pygame GUI.
    def __init__(self, Title: str):
        # setup protected attributes which will be used by inherited classes
        self.Title = Title
        self._WIDTH = 1600
        self._HEIGHT = 900
        self._MANAGER = pygame_gui.UIManager((self._WIDTH, self._HEIGHT), 'Theme/theme.json')
        self._WIN = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        # self._UI_REFRESH_RATE = CLOCK.tick(60)
        self._screen_colour = (191, 191, 191)
    
    def _get_WIN(self):
        return self._WIN

    def _get_MANAGER(self):
        # refactored code to try and avoid the use of global variables such as the MANAGER for the pygame_gui 
        return self._MANAGER 

    def _fill_with_colour(self):
        self._WIN.fill((self._screen_colour))
    
    # Abstract methods that are required for every sub-class of 'Screen'
    @abstractmethod
    def show_UI_elements(self):
        pass

    @abstractmethod
    def remove_UI_elements(self):
        pass

    @abstractmethod
    def check_for_user_interaction_with_UI(self):
        pass

class Intro_Screen(Screen):
    def __init__(self, Title: str):
        super(Intro_Screen, self).__init__(Title)

        # UI
        self.__LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#login_button"), text="LOGIN")
        self.__REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#register_button"), text="REGISTER")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 350), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="BRAIN TRAINING GAME")

    def check_for_user_interaction_with_UI(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#login_button":
                return "Login"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#register_button":
                return "Register"

            self._MANAGER.process_events(event)
        return None

    def remove_UI_elements(self):
        self.__LOGIN_BUTTON.hide()
        self.__REGISTER_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.__LOGIN_BUTTON.show()
        self.__REGISTER_BUTTON.show()
        self.__TITLE_LABEL.show()

# A type of 'Screen' which is mainly used to get essential info from the player, such as username, and password (e.g., being used in register/login screens)
# basically was made to avoid repeating bits of code here and there
class Get_User_Info_Screen(Screen):
    def __init__(self, Title: str, error_msg):
        super(Get_User_Info_Screen, self).__init__(Title)

        # UI
        self._USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(placeholder_text='Type Username Here',relative_rect=pygame.Rect((600, ((self._HEIGHT/2)-70)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#username_text_entry"))
        self._PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(placeholder_text='Type Password Here',relative_rect=pygame.Rect((600, ((self._HEIGHT/2)+30)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#password_text_entry"))
        self._GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self._TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((625, 250), (350, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self._ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 600), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#error_label"), text=error_msg)

        # Other
        self._username = ""
        self._password = ""

    # Getters + Setters for Protected Attributes
    
    def set_username(self, username):
        self._username = username
    
    def set_password(self, password):
        self._password = password

    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password

    def remove_UI_elements(self):
        self._USERNAME_INPUT.hide()
        self._PASSWORD_INPUT.hide()
        self._GO_BACK_BUTTON.hide()
        self._TITLE_LABEL.hide()
        self._ERROR_LABEL.hide()
    
    def show_UI_elements(self):
        self._USERNAME_INPUT.show()
        self._PASSWORD_INPUT.show()
        self._GO_BACK_BUTTON.show()
        self._TITLE_LABEL.show()
    
    def show_error(self):
        self._ERROR_LABEL.show()

class Register_Screen(Get_User_Info_Screen):
    def __init__(self, Title: str, error_msg):
        super().__init__(Title, error_msg)

        self.__PW_ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 600), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#error_label"), text="PASSWORD IS TOO SHORT (>=5 CHAR)")
        self.__USERNAME_TAKEN_ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 600), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#error_label"), text="USERNAME IS ALREADY TAKEN")
    
    def show_PW_error(self):
        self.__PW_ERROR_LABEL.show()
    
    def show_USERNAME_error(self):
        self.__USERNAME_TAKEN_ERROR_LABEL.show()

    def remove_UI_elements(self):
        self._USERNAME_INPUT.hide()
        self._PASSWORD_INPUT.hide()
        self._GO_BACK_BUTTON.hide()
        self._TITLE_LABEL.hide()
        self._ERROR_LABEL.hide()
        self.__PW_ERROR_LABEL.hide()
        self.__USERNAME_TAKEN_ERROR_LABEL.hide()
    
    def check_for_user_interaction_with_UI(self):
        ui_finished = ""
         
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                self.set_username(self._USERNAME_INPUT.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                self.set_password(self._PASSWORD_INPUT.text)
                
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(self.get_username()) > 0:
                    if len(self.get_password()) >= 5:
                        PDM.check_if_username_is_available(self.get_username())
                        if PDM.get_username_available():
                            self.register(self.get_username(), self.get_password())
                            ui_finished = "TEXT_ENTRY"
                            return ui_finished
                        else:
                            self.show_USERNAME_error()
                    else:
                        self.show_PW_error()
                else:
                    self.show_error()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished

            self._MANAGER.process_events(event)

    def register(self, username, password):
        PDM.register_new_player_data(username, password)

class Login_Screen(Get_User_Info_Screen):
    def __init__(self, Title: str, error_msg):
        super().__init__(Title, error_msg)

    def check_for_user_interaction_with_UI(self):
         
        ui_finished = ""
         
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                self.set_username(self._USERNAME_INPUT.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                self.set_password(self._PASSWORD_INPUT.text)
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if self.login(self.get_username(), self.get_password()):
                    ui_finished = "TEXT_ENTRY"
                else:
                    self.show_error()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
            
            self._MANAGER.process_events(event)
        return ui_finished
    
    def login(self, username: str, password: str):
        return PDM.check_user_login(username, password)

# same concept as the 'Get_User_Info_Screen'; may change later as it is kind of redundant but cba
class Confirmation_Screen(Screen):
    
    def __init__(self, Title: str, subtitle: str):
        super(Confirmation_Screen, self).__init__(Title)
        
        self.__subtitle = subtitle
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((540, 350), (520, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self.__SUBTITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600, 450), (400, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#subtitle_label"), text=self.__subtitle)

    def check_for_user_interaction_with_UI(self):
         keys = pygame.key.get_pressed()
         
         if keys[pygame.K_SPACE]:
            return True
         return False 

    def show_UI_elements(self):
         self.__TITLE_LABEL.show()
         self.__SUBTITLE_LABEL.show()
    
    def remove_UI_elements(self):
         self.__TITLE_LABEL.hide()
         self.__SUBTITLE_LABEL.hide()

class Registration_Confirmation_Screen(Confirmation_Screen):
    def __init__(self, Title: str, subtitle: str):        
        super(Registration_Confirmation_Screen, self).__init__(Title, subtitle)

class Login_Confirmation_Screen(Confirmation_Screen):
    def __init__(self, Title: str, subtitle: str):        
        super(Login_Confirmation_Screen, self).__init__(Title, subtitle)

class Skill_Selection_Screen(Screen):
    def __init__(self, Title: str):
        super(Skill_Selection_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 150), (900, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels", object_id="#title_label"), text=Title)
        
        # Labels for each Slider
        self.__MEMORY_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 253), (130, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#memory_subtitle_label"), text="MEMORY")
        self.__ATTENTION_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 353), (150, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#attention_subtitle_label"), text="ATTENTION")
        self.__SPEED_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 453), (100, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#speed_subtitle_label"), text="SPEED")
        self.__PROBLEM_SOLVING_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 553), (250, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#problem_solving_subtitle_label"), text="PROBLEM SOLVING")

        # Sliders for each Category
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 250), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider1_memory"))
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 350), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider2_attention"))
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 450), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider3_speed"))
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 550), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider4_problem_solving"))
        self.__CONFIRM_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 650), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#confirm_button"), text="CONFIRM")

        # Error Message
        self.__ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 775), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#error_label"), text="EACH SLIDER MUST BE > 0")

    # Get values from each Horiztonal Slider
    def get_value_from_slider(self):
        memory_value = self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.get_current_value()
        attention_value = self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.get_current_value()
        speed_value = self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.get_current_value()
        problem_solving_value = self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.get_current_value()
        array_of_values = [memory_value, attention_value, speed_value, problem_solving_value] # in order of the cognitive areas entity within the database
        return array_of_values

    def check_for_user_interaction_with_UI(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#confirm_button":
                values = self.get_value_from_slider()
                weight_values = self.calculate_weighted_values_for_player(values[0], values[1], values[2], values[3])
                if weight_values is None:
                    self.show_error_msg()
                else:
                    self.register_weights_onto_DB(weight_values)
                    return True

            self._MANAGER.process_events(event)
    
    # simple algorithm used to calculate weight values for the player 
    def calculate_weighted_values_for_player(self, memory_value: int, attention_value: int, speed_value: int, problem_solving_value: int):
        # checks if values are valid (each score value is above 0)
        if memory_value == 0 or attention_value == 0 or speed_value == 0 or problem_solving_value == 0:
            return None
        else:
            
            # calculate each weight value
            total_value = speed_value + attention_value + memory_value + problem_solving_value
            
            weight_speed_value = speed_value / total_value
            weight_attention_value = attention_value / total_value
            weight_memory_value = memory_value / total_value
            weight_problem_solving_value = problem_solving_value / total_value

            return (weight_memory_value, weight_attention_value, weight_speed_value, weight_problem_solving_value)

    def register_weights_onto_DB(self, weights):
        PDM.register_weights_onto_DB(weights)
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.hide()
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.hide()
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.hide()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.hide()
        self.__CONFIRM_BUTTON.hide()
        self.__SPEED_LABEL.hide()
        self.__ATTENTION_LABEL.hide()
        self.__MEMORY_LABEL.hide()
        self.__PROBLEM_SOLVING_LABEL.hide()
        self.__ERROR_LABEL.hide()
    
    def show_error_msg(self):
        self.__ERROR_LABEL.show()
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.show()
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.show()
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.show()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.show()
        self.__CONFIRM_BUTTON.show()
        self.__SPEED_LABEL.show()
        self.__ATTENTION_LABEL.show()
        self.__MEMORY_LABEL.show()
        self.__PROBLEM_SOLVING_LABEL.show()
    
class Main_Menu_Screen(Screen):
    def __init__(self, Title: str):
        super(Main_Menu_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 175), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="MAIN MENU")
        self.__PLAY_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 300), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#play_button"), text="PLAY")
        self.__SETTINGS_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 400), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#settings_button"), text="SETTINGS")
        self.__TUTORIAL_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#tutorial_button"), text="TUTORIAL")
        self.__STATS_AND_PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 600), (450, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#stats_and_performance_button"), text="STATS & PERFORMANCE")
        self.__LEADERBOARD_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 700), (300, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#leaderboard_button"), text="LEADERBOARD")
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__PLAY_BUTTON.show()
        self.__SETTINGS_BUTTON.show()
        self.__TUTORIAL_BUTTON.show()
        self.__STATS_AND_PERFORMANCE_BUTTON.show()
        self.__LEADERBOARD_BUTTON.show()
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__PLAY_BUTTON.hide()
        self.__SETTINGS_BUTTON.hide()
        self.__TUTORIAL_BUTTON.hide()
        self.__STATS_AND_PERFORMANCE_BUTTON.hide()
        self.__LEADERBOARD_BUTTON.hide()

    def check_for_user_interaction_with_UI(self):
        ui_finished = ""
        
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#play_button":
                ui_finished = "PLAY"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#settings_button":
                ui_finished = "SETTINGS"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#tutorial_button":
                ui_finished = "TUTORIAL"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#stats_and_performance_button":
                ui_finished = "STATS"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#leaderboard_button":
                ui_finished = "LEADERBOARD"
            
            self._MANAGER.process_events(event)
        return ui_finished

class Maze_Screen(Screen):
    def __init__(self, Title: str, STARTING_TILE_SIZE: int, LINE_COLOUR: tuple):
        super(Maze_Screen, self).__init__(Title)

        # Size + Colour of the cells 
        self.LINE_COLOUR = LINE_COLOUR
        self.starting_tile_size = STARTING_TILE_SIZE

        # Initial parameters dictating the range of exercise cells to be loaded into the level
        self.__min_exercise_cells = 3
        self.__max_exercise_cells = 5
        
        # attributes for time
        self.__time_limit = 60
        self.__spacebar_down = False
        self.__current_time = pygame.time.get_ticks()
        self.__spacebar_down_time = 0
        self.__time_added = 0

        # checking if the game has ended (the player has run out of time to clear the level)
        self.__game_over = False

        # Creating the Maze and Player objects within the Maze Screen Object
        self.__maze = Maze(self.starting_tile_size, self.LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN, PDM, self.__min_exercise_cells, self.__max_exercise_cells)
        self.__player = Player(60, 60, 50, 50, 100)
        
        # Initial Level
        self.__maze_level = 1

        # Amount of hints allowed for the Player 
        self.__amounts_of_hints = 3
        
        # Attributes to detect whether or not the User has used a hint already, and to stop them from spamming it for the same level, if they have already used it for that specified level
        self.__use_hints = False
        self.__already_used_hints_for_current_level = False

        # Boolean value to check whether the application should return back to the Main Menu
        self.__return_to_main_menu = False

        # Calculate Player CPS upon instantiation of Maze Screen as the application now knows the User's PlayerID
        PDM.calculate_CPS() 

    def maze_level_game_loop(self):
        font = pygame.font.Font(None, 50) # Declaring Font for text surfaces to be shown to the User
        if self.__spacebar_down and not self.__game_over:

            # Sets up the actual Maze itself and draw it onto the Screen
            self.__maze.setup_maze()
            self._WIN.blit(self.__player.get_player_image(), self.__player.get_rect()) # Draws the sprite of the Player onto the Maze
            self.check_and_then_draw_exercise_cell() # Draws the exercise cell if the Player has collided with an exercise Cell (calls the Player's draw_exercise_cell() method)

            # checks if the current exercise cell is finished, if it is then add 15s to the timer. bool value required to avoid continuously adding extra time
            if self.check_if_exercise_cell_is_finished() and not self.get_current_cell().get_exercise().get_already_added_time():
                self.__time_added += 15
                self.get_current_cell().get_exercise().set_already_added_time(True)
            
            # Checks if the player wants to use a hint, also avoids from the Player from using another hint again on the same level
            if self.__use_hints and not self.__already_used_hints_for_current_level:
                if self.__amounts_of_hints > 0:
                    current_cell = self.get_current_cell()
                    self.__maze.find_exit_dfs(current_cell)
                    self.__use_hints = False
                    self.__amounts_of_hints -= 1
                    self.__already_used_hints_for_current_level = True
                else:
                    print("Ran out of hints!")
                    
            # Calculating the Time to be displayed to the User
            self.__current_time = pygame.time.get_ticks()
            elapsed_time = (self.__current_time - self.__spacebar_down_time) // 1000
            time_left = (self.__time_limit - elapsed_time) + self.__time_added

            # Text Surfaces to be drawn on to the Screen (amount of hints, and the time left to clear the level)
            time_text = f"Time Left: {time_left}s"
            time_text_surface = font.render(time_text, True, (255, 114, 48))
            self._WIN.blit(time_text_surface, (20, 860))
            hints_text = f"Hints: {self.__amounts_of_hints}"
            hints_text_surface = font.render(hints_text, True, (255, 114, 48))
            self._WIN.blit(hints_text_surface, (20, 820))

            # Checking base case if the User has no more time left to clear the Level
            if time_left <= 0:
                self.__game_over = True

            # Checking if the User has completed all exercise cells, and is at the exit cell.
            # If that evaluates to True then it will move them onto the next level
            if not self.__maze.check_if_all_exercise_cells_are_complete() and self.check_collision_with_exit_cell():

                # Increment Maze level
                self.__maze_level += 1

                # Increase the range of possible exercise cells to be loaded into the level therefore overall difficulty increases
                self.__min_exercise_cells += 2
                self.__max_exercise_cells += 2

                if self.__maze_level >= 2: # phase 1 of mazes
                    self.reset_values_for_new_level(90) # reset values for new level and change time allocated to clear the level

                    # change player size + create new Maze
                    self.__player = Player(60, 60, 50, 50, 100)
                    self.__maze = Maze(100, self.LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN, PDM, self.__min_exercise_cells, self.__max_exercise_cells)

                if self.__maze_level >= 5: # phase 2 of mazes
                    self.reset_values_for_new_level(120) # reset values for new level and change time allocated to clear the level

                    # change player size + Create new Maze
                    self.__player = Player(30, 30, 25, 25, 50)
                    self.__maze = Maze(50, self.LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN, PDM, self.__min_exercise_cells, self.__max_exercise_cells)

                if self.__maze_level >= 9: # phase 3 of mazes
                    self.reset_values_for_new_level(150) # reset values for new level and change time allocated to clear the level

                    # change player size + Create new Maze
                    self.__player = Player(15, 15, 12.5, 12.5, 25)
                    self.__maze = Maze(25, self.LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN, PDM, self.__min_exercise_cells, self.__max_exercise_cells)

        # Checking if the game has ended
        elif self.__game_over:

            # Draw black screen with corrsponding text
            pygame.draw.rect(self._WIN, (0, 0, 0), pygame.Rect(0, 0, self._WIDTH, self._HEIGHT))
            game_over_text = "GAME OVER!"
            game_over_text_surface = font.render(game_over_text, True, (255, 255, 255))
            self._WIN.blit(game_over_text_surface, ((1600 - game_over_text_surface.get_width()) / 2, (900 - game_over_text_surface.get_height()) / 2))
            levels_cleared_text = f"Levels Cleared: {self.__maze_level - 1}"
            levels_cleared_text_surface = font.render(levels_cleared_text, True, (255, 255, 255))
            self._WIN.blit(levels_cleared_text_surface, ((1600 - levels_cleared_text_surface.get_width()) / 2, 550))
            return_to_main_menu_text = "PRESS 'SPACE' TO RETURN TO MAIN MENU"
            return_to_main_menu_text_surface = font.render(return_to_main_menu_text, True, (255, 255, 255))
            self._WIN.blit(return_to_main_menu_text_surface, ((1600 - return_to_main_menu_text_surface.get_width()) / 2, 490))

        else:
            # Draws the screen showing current maze level before the actual maze
            pygame.draw.rect(self._WIN, (0, 0, 0), pygame.Rect(0, 0, self._WIDTH, self._HEIGHT))

            # text
            text_to_be_shown = "PRESS 'SPACE' TO START THE MAZE"
            text_to_be_shown_surface = font.render(text_to_be_shown, True, (255, 255, 255))
            self._WIN.blit(text_to_be_shown_surface, ((1600 - text_to_be_shown_surface.get_width()) / 2, (900 - text_to_be_shown_surface.get_height()) / 2))
            level_text = f"Maze Level: {self.__maze_level}"
            level_text_surface = font.render(level_text, True, (255, 255, 255))
            self._WIN.blit(level_text_surface, ((1600 - level_text_surface.get_width()) / 2, 600))

    def reset_values_for_new_level(self, new_time_limit_for_level: int):
        self.__spacebar_down_time = new_time_limit_for_level
        self.__spacebar_down = False
        self.__time_limit = 90
        self.__time_added = 0
        self.__already_used_hints_for_current_level = False
        self.__use_hints = False

    def get_return_to_main_menu(self):
        return self.__return_to_main_menu

    def get_current_cell(self):
        return self.__player.get_current_cell(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells())

    def check_collision_with_exit_cell(self):
        return self.__player.check_collision_with_exit_cell(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells())
    
    def check_and_then_draw_exercise_cell(self):
        self.__player.check_and_then_draw_exercise_cell(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells(), self._WIN)
    
    def check_type_of_exercise_cell(self):
        return self.__player.get_exercise_cell(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells())
    
    def check_if_exercise_cell_is_finished(self):
        return self.__player.check_if_exercise_cell_is_complete(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells())
    
    def player_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.__spacebar_down:
                self.__spacebar_down = True
                self.__spacebar_down_time = pygame.time.get_ticks()
            elif event.key == pygame.K_SPACE and self.__game_over:
                self.__return_to_main_menu = True
            elif event.key == pygame.K_h and not self.__use_hints:
                self.__use_hints = True
        
        if self.__spacebar_down:
            self.__player.player_input(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells(), event)
    
    def show_UI_elements(self):
        return super().show_UI_elements()

    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def check_for_user_interaction_with_UI(self):
        return super().check_for_user_interaction_with_UI()  

class Settings_Screen(Screen):
    def __init__(self, Title: str):
        super(Settings_Screen, self).__init__(Title)

        # Temporary Storage for Question + Answer for Question Recall Exercise
        self.__question = ''
        self.__answer = ''

        # UI 
        self.__DROP_DOWN_MENU_MM = pygame_gui.elements.UIDropDownMenu(['Easy', 'Medium', 'Hard'], 'Easy',relative_rect=pygame.Rect((162.5, 175), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@drop_down_menus",object_id="#drop_down_menu_memory_matrix"))
        self.__MEMORY_MATRIX_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((162.5, 115), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#memory_matrix_label"), text="MEMORY MATRIX")

        self.__DROP_DOWN_MENU_A = pygame_gui.elements.UIDropDownMenu(['Easy (15s, +25pts)', 'Medium (10s, +50pts)', 'Hard (5s, +100pts)'], 'Easy (15s, +25pts)',relative_rect=pygame.Rect((687.5, 175), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@drop_down_menus",object_id="#drop_down_menu_aiming"))
        self.__AIMING_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((687.5, 115), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#aiming_label"), text="AIMING")

        self.__DROP_DOWN_MENU_ST = pygame_gui.elements.UIDropDownMenu(['Easy (4*4)', 'Hard (5*5)', 'Easy (4*4 + colour)', 'Hard (5*5 + colour)'], 'Easy (4*4)',relative_rect=pygame.Rect((1212.5, 175), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@drop_down_menus",object_id="#drop_down_menu_schulte_table"))
        self.__SCHULTE_TABLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1212.5, 115), (225, 50)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#schulte_table_label"), text="SCHULTE TABLE")

        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self.__SAVE_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1385, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#save_button"), text="SAVE")

        self.__QUESTION_EXERCISE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((682.5, 350), (235, 45)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#question_exercise_label"), text="QUESTION RECALL")
        self.__QUESTION_INPUT = pygame_gui.elements.UITextEntryLine(placeholder_text='Type Question Here', relative_rect=pygame.Rect((600, 400), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#question_text_entry"))
        self.__ANSWER_INPUT = pygame_gui.elements.UITextEntryLine(placeholder_text='Type Corresponding Answer Here',relative_rect=pygame.Rect((600, 450), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#answer_text_entry"))

        self.__NONE_QUESTION_ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, 650), (1000, 45)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#question_error_label"), text="YOU NEED TO INPUT BOTH A QUESTION AND AN ANSWER BEFORE SAVING")
        self.__SETTINGS_SAVED_SUCCESSFULLY_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 650), (500, 45)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#settings_saved_label"), text="SETTINGS SAVED SUCCESSFULLY!")
    
    def check_for_user_interaction_with_UI(self):
        ui_finished = ""

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#save_button":
                if self.__answer == '' or self.__question == '':
                    self.show_question_ERROR()
                    self.hide_settings_saved()
                else:
                    self.change_settings()
                    self.show_settings_saved()
                    self.hide_question_error()
                    print('saved settings!')
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "#drop_down_menu_memory_matrix":
                print(self.__DROP_DOWN_MENU_MM.selected_option)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#question_text_entry":
                self.__question = event.text
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#answer_text_entry":
                self.__answer = event.text
            
            self._MANAGER.process_events(event)
    
    def change_settings(self):
        # Retrieve selected options from each drop down menu and use them as parameters for the method 'change_settings_according_to_user()'
        difficulty_mm = self.__DROP_DOWN_MENU_MM.selected_option
        difficulty_a = self.__DROP_DOWN_MENU_A.selected_option
        difficulty_st = self.__DROP_DOWN_MENU_ST.selected_option
        PDM.change_settings_according_to_user(difficulty_mm, difficulty_a, difficulty_st, self.__question, self.__answer)


    def remove_UI_elements(self):
        self.__DROP_DOWN_MENU_MM.hide()
        self.__DROP_DOWN_MENU_A.hide()
        self.__DROP_DOWN_MENU_ST.hide()
        self.__GO_BACK_BUTTON.hide()
        self.__SAVE_BUTTON.hide()
        self.__MEMORY_MATRIX_LABEL.hide()
        self.__AIMING_LABEL.hide()
        self.__SCHULTE_TABLE_LABEL.hide()
        self.__QUESTION_INPUT.hide()
        self.__ANSWER_INPUT.hide()
        self.__QUESTION_EXERCISE_LABEL.hide()
        self.hide_settings_saved()
        self.hide_question_error()
    
    def show_question_ERROR(self):
        self.__NONE_QUESTION_ERROR_LABEL.show()

    def hide_question_error(self):
        self.__NONE_QUESTION_ERROR_LABEL.hide()
    
    def show_settings_saved(self):
        self.__SETTINGS_SAVED_SUCCESSFULLY_LABEL.show()

    def hide_settings_saved(self):
        self.__SETTINGS_SAVED_SUCCESSFULLY_LABEL.hide()

    def show_UI_elements(self):
        self.__DROP_DOWN_MENU_MM.show()
        self.__DROP_DOWN_MENU_A.show()
        self.__DROP_DOWN_MENU_ST.show()
        self.__GO_BACK_BUTTON.show()
        self.__SAVE_BUTTON.show()
        self.__MEMORY_MATRIX_LABEL.show()
        self.__AIMING_LABEL.show()
        self.__SCHULTE_TABLE_LABEL.show()
        self.__QUESTION_INPUT.show()
        self.__ANSWER_INPUT.show()
        self.__QUESTION_EXERCISE_LABEL.show()
    
class Stats_and_Performance_Screen(Screen):
    def __init__(self, Title: str):
        super().__init__(Title)

        # UI
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((400, 100), (800, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="CPS (COGNITIVE PERFORMANCE SCORE)")

    def show_stats(self):
        # retireve cps values array
        cps_values = PDM.get_CPS()

        # depending on the length of the array above, record them into appropiate variables to be displayed to the user
        if len(cps_values) == 5:
            cps_value_1 = cps_values[0]
            cps_value_2 = cps_values[1]
            cps_value_3 = cps_values[2]
            cps_value_4 = cps_values[3]
            cps_value_5 = cps_values[4]
        elif len(cps_values) == 4:
            cps_value_1 = cps_values[0]
            cps_value_2 = cps_values[1]
            cps_value_3 = cps_values[2]
            cps_value_4 = cps_values[3]
            cps_value_5 = ['NA', 'NA']
        elif len(cps_values) == 3:
            cps_value_1 = cps_values[0]
            cps_value_2 = cps_values[1]
            cps_value_3 = cps_values[2]
            cps_value_4 = ['NA', 'NA']
            cps_value_5 = ['NA', 'NA']
        elif len(cps_values) == 2:
            cps_value_1 = cps_values[0]
            cps_value_2 = cps_values[1]
            cps_value_3 = ['NA', 'NA']
            cps_value_4 = ['NA', 'NA']
            cps_value_5 = ['NA', 'NA']
        elif len(cps_values) == 1:
            cps_value_1 = cps_values[0]
            cps_value_2 = ['NA', 'NA']
            cps_value_3 = ['NA', 'NA']
            cps_value_4 = ['NA', 'NA']
            cps_value_5 = ['NA', 'NA']
        else:
            cps_value_1 = ['NA', 'NA']
            cps_value_2 = ['NA', 'NA']
            cps_value_3 = ['NA', 'NA']
            cps_value_4 = ['NA', 'NA']
            cps_value_5 = ['NA', 'NA']

        font = pygame.font.Font(None, 50) # declare the font for text surfaces

        # create the text surfaces and display them onto the screen
        cps_value_1_text = f"CPS: {cps_value_1[0]}, Date Calculated: {cps_value_1[1]}"
        cps_value_1_surface = font.render(cps_value_1_text, True, (255, 255, 255))
        self._WIN.blit(cps_value_1_surface, ((1600 - cps_value_1_surface.get_width()) / 2, 200))

        cps_value_2_text =  f"CPS: {cps_value_2[0]}, Date Calculated: {cps_value_2[1]}"
        cps_value_2_surface = font.render(cps_value_2_text, True, (255, 255, 255))
        self._WIN.blit(cps_value_2_surface, ((1600 - cps_value_2_surface.get_width()) / 2, 300))

        cps_value_3_text =  f"CPS: {cps_value_3[0]}, Date Calculated: {cps_value_3[1]}"
        cps_value_3_surface = font.render(cps_value_3_text, True, (255, 255, 255))
        self._WIN.blit(cps_value_3_surface, ((1600 - cps_value_3_surface.get_width()) / 2, 400))

        cps_value_4_text =  f"CPS: {cps_value_4[0]}, Date Calculated: {cps_value_4[1]}"
        cps_value_4_surface = font.render(cps_value_4_text, True, (255, 255, 255))
        self._WIN.blit(cps_value_4_surface, ((1600 - cps_value_4_surface.get_width()) / 2, 500))

        cps_value_5_text =  f"CPS: {cps_value_5[0]}, Date Calculated: {cps_value_5[1]}"
        cps_value_5_surface = font.render(cps_value_5_text, True, (255, 255, 255))
        self._WIN.blit(cps_value_5_surface, ((1600 - cps_value_5_surface.get_width()) / 2, 600))

    def check_for_user_interaction_with_UI(self):
        ui_finished = ""

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished
            self._MANAGER.process_events(event)

    def remove_UI_elements(self):
        self.__GO_BACK_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.show_stats()
        self.__GO_BACK_BUTTON.show()
        self.__TITLE_LABEL.show()

class Leaderboard_Screen(Screen):
    def __init__(self, Title: str):
        super().__init__(Title)

        # UI
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
    
    def show_leaderboard(self):
        # same principle as the method in the 'Stats and Performance Screen' object
        top_5 = PDM.retrieve_top_5_players()
        if len(top_5) == 5:
            first_place = top_5[0]
            second_place = top_5[1]
            third_place = top_5[2]
            fourth_place = top_5[3]
            fifth_place = top_5[4]
        elif len(top_5) == 4:
            first_place = top_5[0]
            second_place = top_5[1]
            third_place = top_5[2]
            fourth_place = top_5[3]
            fifth_place = ['TBD', 'NA']
        elif len(top_5) == 3:
            first_place = top_5[0]
            second_place = top_5[1]
            third_place = top_5[2]
            fourth_place = ['TBD', 'NA']
            fifth_place = ['TBD', 'NA']
        elif len(top_5) == 2:
            first_place = top_5[0]
            second_place = top_5[1]
            third_place = ['TBD', 'NA']
            fourth_place = ['TBD', 'NA']
            fifth_place = ['TBD', 'NA']
        elif len(top_5) == 1:
            first_place = top_5[0]
            second_place = ['TBD', 'NA']
            third_place = ['TBD', 'NA']
            fourth_place = ['TBD', 'NA']
            fifth_place = ['TBD', 'NA']
        else:
            first_place = ['TBD', 'NA']
            second_place = ['TBD', 'NA']
            third_place = ['TBD', 'NA']
            fourth_place = ['TBD', 'NA']
            fifth_place = ['TBD', 'NA']
        
        font = pygame.font.Font(None, 50)

        first_place_text = f"1. {first_place[0]}, CPS: {first_place[1]}"
        first_place_text_surface = font.render(first_place_text, True, (255, 255, 255))
        self._WIN.blit(first_place_text_surface, ((1600 - first_place_text_surface.get_width()) / 2, 200))

        second_place_text = f"2. {second_place[0]}, CPS: {second_place[1]}"
        second_place_text_surface = font.render(second_place_text, True, (255, 255, 255))
        self._WIN.blit(second_place_text_surface, ((1600 - second_place_text_surface.get_width()) / 2, 300))

        third_place_text = f"3. {third_place[0]}, CPS: {third_place[1]}"
        third_place_text_surface = font.render(third_place_text, True, (255, 255, 255))
        self._WIN.blit(third_place_text_surface, ((1600 - third_place_text_surface.get_width()) / 2, 400))

        fourth_place_text = f"4. {fourth_place[0]}, CPS: {fourth_place[1]}"
        fourth_place_text_surface = font.render(fourth_place_text, True, (255, 255, 255))
        self._WIN.blit(fourth_place_text_surface, ((1600 - fourth_place_text_surface.get_width()) / 2, 500))
        
        fifth_place_text = f"5. {fifth_place[0]}, CPS: {fifth_place[1]}"
        fifth_place_text_surface = font.render(fifth_place_text, True, (255, 255, 255))
        self._WIN.blit(fifth_place_text_surface, ((1600 - fifth_place_text_surface.get_width()) / 2, 600))



    def show_UI_elements(self):
        self.show_leaderboard()
        self.__GO_BACK_BUTTON.show()
    
    def remove_UI_elements(self):
        self.__GO_BACK_BUTTON.hide()
    
    def check_for_user_interaction_with_UI(self):
        ui_finished = ""

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished
            self._MANAGER.process_events(event)

class Tutorial_Screen(Screen):
    def __init__(self, Title: str):
        super().__init__(Title)

        # UI
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")

    def show_UI_elements(self):
        self.__GO_BACK_BUTTON.show()

        font = pygame.font.Font(None, 36)
        mm_text = "Memory Matrix (Memory): Remember the pattern of highlighted cells. Remember them, pick them, get points."
        mm_text_surface = font.render(mm_text, True, (255, 255, 255))
        self._WIN.blit(mm_text_surface, ((1600 - mm_text_surface.get_width()) / 2, 200))

        cc_text = "Chalkboard Challenge (Problem Solving): See the equations, pick which one is larger, get points."
        cc_text_surface = font.render(cc_text, True, (255, 255, 255))
        self._WIN.blit(cc_text_surface, ((1600 - cc_text_surface.get_width()) / 2, 250))

        st_text = "Schulte Table (Attention): See the numbers, pick them in order, get points."
        st_text_surface = font.render(st_text, True, (255, 255, 255))
        self._WIN.blit(st_text_surface, ((1600 - st_text_surface.get_width()) / 2, 300))

        a_text = "Aiming (Speed): Find the targets, select them, get points."
        a_text_surface = font.render(a_text, True, (255, 255, 255))
        self._WIN.blit(a_text_surface, ((1600 - a_text_surface.get_width()) / 2, 350))

        q_text = "Question Recall (Memory): Create a Question, recall and answer it correctly, get points."
        q_text_surface = font.render(q_text, True, (255, 255, 255))
        self._WIN.blit(q_text_surface, ((1600 - q_text_surface.get_width()) / 2, 400))

        big_font = pygame.font.Font(None, 40)
        aim_of_the_game_text = "Aim: Endlessly navigate through mazes whilst also completing cognitive exercises under a time constraint."
        aim_of_the_game_text_surface = big_font.render(aim_of_the_game_text, True, (255, 255, 255))
        self._WIN.blit(aim_of_the_game_text_surface, ((1600 - aim_of_the_game_text_surface.get_width()) / 2, 500))

    def remove_UI_elements(self):
        self.__GO_BACK_BUTTON.hide()

    def check_for_user_interaction_with_UI(self):
        ui_finished = ""

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished
            self._MANAGER.process_events(event)
    